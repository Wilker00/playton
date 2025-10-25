"""Custom gymnasium environment for trading simulation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import gymnasium as gym
import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends
from gymnasium import spaces

from backend.auth.security import User, get_current_user
from backend.settings import get_settings
from backend.trading import rewards
from backend.trading.schemas import EnvConfig

router = APIRouter()


@dataclass
class TradingEnvConfig:
    data_path: Path
    window_size: int = 32
    assets: List[str] | None = None
    transaction_cost: float = 0.001
    slippage: float = 0.0005
    split: str = "train"


class TradingEnv(gym.Env[np.ndarray, np.ndarray]):
    """Trading environment producing normalized feature windows and portfolio state."""

    metadata = {"render_modes": ["human"]}

    def __init__(self, config: Dict | TradingEnvConfig | None = None) -> None:
        cfg = config or {}
        if not isinstance(cfg, TradingEnvConfig):
            settings = get_settings()
            cfg = TradingEnvConfig(
                data_path=Path(cfg.get("data_path", settings.data_root) if cfg.get("data_path") else Path(settings.data_root) / "frozen" / "train.parquet"),
                window_size=int(cfg.get("window_size", 32)),
                assets=list(cfg.get("assets", ["SPY", "QQQ", "BTCUSD", "ETHUSD"])),
                transaction_cost=float(cfg.get("transaction_cost", 0.001)),
                slippage=float(cfg.get("slippage", 0.0005)),
                split=str(cfg.get("split", "train")),
            )
        self.config = cfg
        self.window_size = cfg.window_size
        self.assets = cfg.assets or ["SPY", "QQQ"]
        self.transaction_cost = cfg.transaction_cost
        self.slippage = cfg.slippage
        self.split = cfg.split

        self.feature_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "rsi",
            "macd",
            "macd_signal",
            "bb_upper",
            "bb_lower",
            "rv",
        ]
        self._data_tensor: np.ndarray | None = None
        self._close_prices: np.ndarray | None = None
        self._regime_labels: List[str] = []
        self._feature_mean: np.ndarray | None = None
        self._feature_std: np.ndarray | None = None
        self._current_step = 0
        self._weights = np.zeros(len(self.assets), dtype=np.float32)
        self._portfolio_value = 1.0
        self._returns_history: List[float] = []
        self._weight_history: List[np.ndarray] = []

        obs_size = self.window_size * len(self.assets) * len(self.feature_columns) + len(self.assets) + 2 + 3
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obs_size,), dtype=np.float32)
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(len(self.assets),), dtype=np.float32)

    # Data loading ---------------------------------------------------------
    def _load_dataset(self) -> None:
        data_path = Path(self.config.data_path)
        if data_path.is_dir():
            file_path = data_path / "train.parquet"
        else:
            file_path = data_path
        if not file_path.exists():
            raise FileNotFoundError(f"Dataset not found at {file_path}")
        df = pd.read_parquet(file_path)
        if "split" in df.columns:
            df = df[df["split"] == self.split]
        df = df[df["symbol"].isin(self.assets)].copy()
        df.sort_values("timestamp", inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        frames = {}
        for symbol in self.assets:
            symbol_df = df[df["symbol"] == symbol].set_index("timestamp")
            frames[symbol] = symbol_df
        common_index = None
        for frame in frames.values():
            common_index = frame.index if common_index is None else common_index.intersection(frame.index)
        if common_index is None or common_index.empty:
            raise RuntimeError("No overlapping timestamps across assets for environment")
        common_index = common_index.sort_values()
        tensor_list = []
        close_list = []
        regimes = []
        for timestamp in common_index:
            feature_stack = []
            for symbol in self.assets:
                row = frames[symbol].loc[timestamp]
                feature_stack.append(row[self.feature_columns].to_numpy(dtype=float))
            feature_array = np.stack(feature_stack, axis=0)
            tensor_list.append(feature_array)
            close_list.append([frames[symbol].loc[timestamp]["close"] for symbol in self.assets])
        self._data_tensor = np.stack(tensor_list, axis=0)
        self._close_prices = np.asarray(close_list, dtype=float)
        self._feature_mean = self._data_tensor.mean(axis=(0, 1))
        self._feature_std = np.clip(self._data_tensor.std(axis=(0, 1)), 1e-6, None)
        price_returns = np.diff(self._close_prices, axis=0) / self._close_prices[:-1]
        regimes.append("BULL_VOLATILE")  # first entry fallback
        for ret in price_returns:
            avg_ret = np.mean(ret)
            volatility = np.std(ret)
            if avg_ret > 0 and volatility > 0.01:
                regimes.append("BULL_VOLATILE")
            elif avg_ret < 0 and volatility > 0.01:
                regimes.append("BEAR_STABLE")
            else:
                regimes.append("SIDEWAYS_CHOPPY")
        self._regime_labels = regimes

    # Gym API -------------------------------------------------------------
    def reset(self, *, seed: int | None = None, options: Dict | None = None):
        super().reset(seed=seed)
        if self._data_tensor is None:
            self._load_dataset()
        self._current_step = self.window_size
        if self._current_step >= len(self._data_tensor):
            raise RuntimeError("Window size too large for dataset")
        self._weights = np.zeros(len(self.assets), dtype=np.float32)
        self._portfolio_value = 1.0
        self._returns_history = []
        self._weight_history = [self._weights.copy()]
        observation = self._build_observation()
        return observation, {}

    def step(self, action: np.ndarray):
        if self._data_tensor is None or self._close_prices is None:
            raise RuntimeError("Dataset not loaded; call reset first")
        action = np.clip(action, -1.0, 1.0)
        prev_prices = self._close_prices[self._current_step - 1]
        next_prices = self._close_prices[self._current_step]
        asset_returns = (next_prices - prev_prices) / prev_prices
        slippage = np.random.normal(0.0, self.slippage, size=len(self.assets))
        portfolio_return = float(np.dot(action, asset_returns))
        transaction_penalty = self.transaction_cost * float(np.sum(np.abs(action - self._weights)))
        slippage_penalty = float(np.sum(np.abs(action) * slippage))
        step_return = portfolio_return - transaction_penalty - slippage_penalty
        self._portfolio_value *= 1 + step_return
        self._weights = action.astype(np.float32)
        self._returns_history.append(step_return)
        self._weight_history.append(self._weights.copy())
        reward_breakdown = rewards.compute_reward(
            np.asarray(self._returns_history[-self.window_size :], dtype=float),
            cvar_lambda=1.0,
            fee_penalty=transaction_penalty + slippage_penalty,
        )
        done = self._current_step >= len(self._data_tensor) - 1
        self._current_step += 1
        observation = self._build_observation()
        info = {"portfolio_value": self._portfolio_value, "reward_breakdown": reward_breakdown.model_dump()}
        return observation, reward_breakdown.total, done, False, info

    # Helpers ------------------------------------------------------------
    def _build_observation(self) -> np.ndarray:
        assert self._data_tensor is not None
        start = self._current_step - self.window_size
        window = self._data_tensor[start : self._current_step]
        normalized = (window - self._feature_mean) / self._feature_std
        obs_features = normalized.reshape(-1)
        cash = max(0.0, 1.0 - np.sum(np.abs(self._weights)))
        pnl = self._portfolio_value - 1.0
        regime_vector = self._regime_one_hot(self._regime_labels[self._current_step - 1])
        portfolio_state = np.concatenate([self._weights, [cash, pnl]])
        observation = np.concatenate([obs_features, portfolio_state, regime_vector]).astype(np.float32)
        return observation

    @staticmethod
    def _regime_one_hot(label: str) -> np.ndarray:
        regimes = ["BULL_VOLATILE", "BEAR_STABLE", "SIDEWAYS_CHOPPY"]
        vector = np.zeros(len(regimes), dtype=np.float32)
        if label in regimes:
            vector[regimes.index(label)] = 1.0
        return vector


DEFAULT_ENV_CONFIG = EnvConfig(
    data_path="data/frozen/train.parquet",
    window_size=32,
    assets=["SPY", "QQQ", "BTCUSD", "ETHUSD"],
    transaction_cost=0.001,
    slippage=0.0005,
)


@router.get("/default", response_model=EnvConfig)
def get_default_env(_: User = Depends(get_current_user)) -> EnvConfig:
    """Return the default trading environment configuration."""

    return DEFAULT_ENV_CONFIG


def load_env_config(path: str | Path) -> Dict:
    """Load environment configuration from YAML for the RL pipeline."""

    import yaml

    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)
