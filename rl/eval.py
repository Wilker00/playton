"""Evaluate trained policies using VectorBT."""

from __future__ import annotations

import argparse
import tempfile
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import vectorbt as vbt
from stable_baselines3 import PPO

from backend.trading.envs import TradingEnv
from rl.train import load_yaml


def run_backtest(run_id: str) -> Dict[str, float]:
    tmpdir = Path(tempfile.mkdtemp())
    artifact_dir = Path(mlflow.artifacts.download_artifacts(run_id=run_id, dst_path=tmpdir))
    model_path = next(artifact_dir.rglob("ppo_model_*.zip"))
    config_dir = artifact_dir / "configs"
    env_candidates = sorted(config_dir.glob("env*.yaml")) if config_dir.exists() else []
    if not env_candidates:
        raise FileNotFoundError("Environment config artifact not found")
    env_config = load_yaml(env_candidates[0])
    env_config["split"] = env_config.get("eval_split", "test")
    model = PPO.load(model_path)
    env = TradingEnv(env_config)
    with mlflow.start_run(run_id=run_id):
        obs, _ = env.reset()
        done = False
        truncated = False
        while not done and not truncated:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
        returns = np.array(env._returns_history, dtype=float)  # type: ignore[attr-defined]
        if returns.size == 0:
            returns = np.array([0.0])
        index = pd.RangeIndex(len(returns))
        portfolio = vbt.Portfolio.from_returns(pd.Series(returns, index=index), init_cash=1.0)
        equity_curve = portfolio.value()
        stats = portfolio.stats()
        report_path = artifact_dir / "report.txt"
        with open(report_path, "w", encoding="utf-8") as handle:
            handle.write("VectorBT Evaluation Report\n")
            handle.write(f"Total Return: {stats['total_return']:.4f}\n")
            handle.write(f"Sharpe Ratio: {stats['sharpe_ratio']:.4f}\n")
            handle.write(f"Sortino Ratio: {stats['sortino_ratio']:.4f}\n")
            handle.write(f"Max Drawdown: {stats['max_dd']:.4f}\n")
        fig, ax = plt.subplots(figsize=(10, 4))
        equity_curve.plot(ax=ax)
        ax.set_title("Equity Curve")
        ax.set_xlabel("Step")
        ax.set_ylabel("Portfolio Value")
        plot_path = artifact_dir / "equity_curve.png"
        fig.tight_layout()
        fig.savefig(plot_path)
        plt.close(fig)
        metrics = {
            "total_return": float(stats["total_return"]),
            "sharpe_ratio": float(stats["sharpe_ratio"]),
            "sortino_ratio": float(stats["sortino_ratio"]),
            "max_drawdown": float(stats["max_dd"]),
        }
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(report_path)
        mlflow.log_artifact(plot_path)
    return metrics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate trained PPO run")
    parser.add_argument("--run-id", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = run_backtest(args.run_id)
    print("Evaluation complete:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")


if __name__ == "__main__":  # pragma: no cover
    main()
