"""Train a PPO agent on the custom trading environment."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict

import mlflow
import numpy as np
import yaml
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from backend.trading.envs import TradingEnv
from rl.tracker import RunTracker


def load_yaml(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def make_env(env_config: Dict[str, Any]) -> TradingEnv:
    return TradingEnv(env_config)


def evaluate(model: PPO, env_config: Dict[str, Any]) -> Dict[str, float]:
    eval_env = TradingEnv({**env_config, "split": env_config.get("eval_split", "test")})
    obs, _ = eval_env.reset()
    done = False
    truncated = False
    while not done and not truncated:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = eval_env.step(action)
    returns = np.array(eval_env._returns_history, dtype=float)  # type: ignore[attr-defined]
    cumulative_return = float((eval_env._portfolio_value - 1.0))  # type: ignore[attr-defined]
    return {
        "cumulative_return": cumulative_return,
        "episode_len": len(returns),
        "episode_reward_sum": float(np.sum(returns)),
        "episode_reward_mean": float(np.mean(returns)) if returns.size else 0.0,
    }


def train(env_config_path: Path, algo_config_path: Path) -> str:
    env_config = load_yaml(env_config_path)
    algo_config = load_yaml(algo_config_path)

    env = TradingEnv(env_config)
    check_env(env, warn=True)
    vec_env = DummyVecEnv([lambda: TradingEnv(env_config)])

    tracker = RunTracker()
    with tracker.start_run(run_name="ppo-training"):
        total_timesteps = int(algo_config.get("total_timesteps", 10_000))
        algo_params = {k: v for k, v in algo_config.items() if k != "total_timesteps"}
        tracker.log_params({**algo_params, "total_timesteps": total_timesteps, "env_config": json.dumps(env_config)})
        model = PPO("MlpPolicy", vec_env, **algo_params)
        start = time.time()
        model.learn(total_timesteps=total_timesteps)
        duration = time.time() - start
        eval_metrics = evaluate(model, env_config)
        tracker.log_metrics({"training_time": duration, **eval_metrics})
        model_path = Path("artifacts") / f"ppo_model_{int(time.time())}.zip"
        model_path.parent.mkdir(parents=True, exist_ok=True)
        model.save(model_path)
        tracker.log_artifact(model_path)
        mlflow.log_artifact(algo_config_path, artifact_path="configs")
        mlflow.log_artifact(env_config_path, artifact_path="configs")
        run_id = tracker.run_id
    return run_id


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train PPO baseline")
    parser.add_argument("--env-config", type=Path, required=True)
    parser.add_argument("--algo-config", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_id = train(args.env_config, args.algo_config)
    print(f"Training complete. MLflow run: {run_id}")


if __name__ == "__main__":  # pragma: no cover
    main()
