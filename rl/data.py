"""Data ingestion and preprocessing pipeline using DVC.

Schema:
    timestamp, symbol, open, high, low, close, volume,
    rsi, macd, macd_signal, bb_upper, bb_lower, rv, split(train|test)
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

DATA_ROOT = Path("data")
RAW_DIR = DATA_ROOT / "raw"
CLEAN_DIR = DATA_ROOT / "clean"
FEATURE_DIR = DATA_ROOT / "feature"
FROZEN_DIR = DATA_ROOT / "frozen"


def ensure_dirs() -> None:
    for path in [RAW_DIR, CLEAN_DIR, FEATURE_DIR, FROZEN_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def _freq_to_offset(tf: str) -> str:
    mapping = {"1h": "H", "1d": "D", "4h": "4H", "1m": "T"}
    return mapping.get(tf, "H")


def _simulate_candles(symbol: str, tf: str, years: int) -> pd.DataFrame:
    """Generate synthetic yet reproducible OHLCV data."""

    np.random.seed(abs(hash(symbol)) % 2**32)
    periods = years * 365
    if tf.endswith("h"):
        step = int(tf[:-1]) if tf[:-1].isdigit() else 1
        periods *= int(24 / max(step, 1))
    elif tf.endswith("m"):
        step = int(tf[:-1]) if tf[:-1].isdigit() else 1
        periods *= int((24 * 60) / max(step, 1))
    freq = _freq_to_offset(tf)
    end = datetime.now(timezone.utc)
    index = pd.date_range(end=end, periods=periods, freq=freq)
    prices = np.cumprod(1 + np.random.normal(0, 0.002, size=len(index))) * 100
    high = prices * (1 + np.random.normal(0.001, 0.002, size=len(index)))
    low = prices * (1 - np.random.normal(0.001, 0.002, size=len(index)))
    volume = np.abs(np.random.normal(1_000_000, 200_000, size=len(index)))
    df = pd.DataFrame(
        {
            "timestamp": index,
            "symbol": symbol,
            "open": prices,
            "high": high,
            "low": low,
            "close": prices * (1 + np.random.normal(0, 0.001, size=len(index))),
            "volume": volume,
        }
    )
    return df


def ingest(symbols: Iterable[str], tf: str, years: int) -> None:
    ensure_dirs()
    for symbol in symbols:
        df = _simulate_candles(symbol, tf, years)
        file_path = RAW_DIR / f"{symbol.upper()}.parquet"
        df.to_parquet(file_path)
        print(f"Ingested {symbol} -> {file_path}")


def clean() -> None:
    ensure_dirs()
    frames = []
    for file in RAW_DIR.glob("*.parquet"):
        df = pd.read_parquet(file)
        df.drop_duplicates(subset=["timestamp"], inplace=True)
        df.sort_values("timestamp", inplace=True)
        df.fillna(method="ffill", inplace=True)
        df.dropna(inplace=True)
        frames.append(df)
    if not frames:
        raise RuntimeError("No raw data available. Run ingest first.")
    clean_df = pd.concat(frames, ignore_index=True)
    clean_df.to_parquet(CLEAN_DIR / "combined.parquet")
    print("Clean stage complete")


def _compute_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / window, min_periods=window).mean()
    avg_loss = loss.ewm(alpha=1 / window, min_periods=window).mean()
    rs = avg_gain / (avg_loss + 1e-9)
    return 100 - (100 / (1 + rs))


def _compute_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple[pd.Series, pd.Series]:
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_series = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_series


def _compute_bollinger(series: pd.Series, window: int = 20, std: float = 2.0) -> tuple[pd.Series, pd.Series]:
    sma = series.rolling(window=window, min_periods=window).mean()
    rolling_std = series.rolling(window=window, min_periods=window).std()
    upper = sma + std * rolling_std
    lower = sma - std * rolling_std
    return upper, lower


def _realized_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
    return returns.rolling(window=window, min_periods=window).std() * np.sqrt(252)


def feature() -> None:
    ensure_dirs()
    clean_path = CLEAN_DIR / "combined.parquet"
    if not clean_path.exists():
        raise RuntimeError("Clean dataset missing. Run clean stage first.")
    df = pd.read_parquet(clean_path)
    feature_frames = []
    for symbol, group in df.groupby("symbol"):
        group = group.sort_values("timestamp").copy()
        close = group["close"]
        group["rsi"] = _compute_rsi(close)
        macd, signal = _compute_macd(close)
        group["macd"] = macd
        group["macd_signal"] = signal
        upper, lower = _compute_bollinger(close)
        group["bb_upper"] = upper
        group["bb_lower"] = lower
        returns = close.pct_change().fillna(0)
        group["rv"] = _realized_volatility(returns)
        feature_frames.append(group)
    feature_df = pd.concat(feature_frames, ignore_index=True).dropna()
    feature_df.to_parquet(FEATURE_DIR / "features.parquet")
    print("Feature stage complete")


def freeze(test_months: int = 12) -> None:
    ensure_dirs()
    feature_path = FEATURE_DIR / "features.parquet"
    if not feature_path.exists():
        raise RuntimeError("Feature dataset missing. Run feature stage first.")
    df = pd.read_parquet(feature_path)
    df.sort_values("timestamp", inplace=True)
    latest_time = df["timestamp"].max()
    split_time = latest_time - pd.DateOffset(months=test_months)
    train_df = df[df["timestamp"] < split_time].copy()
    test_df = df[df["timestamp"] >= split_time].copy()
    train_df["split"] = "train"
    test_df["split"] = "test"
    combined = pd.concat([train_df, test_df], ignore_index=True)
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(FROZEN_DIR / "dataset.parquet")
    train_df.to_parquet(FROZEN_DIR / "train.parquet")
    test_df.to_parquet(FROZEN_DIR / "test.parquet")
    print("Freeze stage complete")


def build() -> None:
    clean()
    feature()
    freeze()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="DVC-enabled data pipeline")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest_parser = sub.add_parser("ingest", help="Ingest raw data")
    ingest_parser.add_argument("--symbols", nargs="+", required=True)
    ingest_parser.add_argument("--tf", default="1h")
    ingest_parser.add_argument("--years", type=int, default=3)

    sub.add_parser("clean", help="Run clean stage")
    sub.add_parser("feature", help="Run feature engineering stage")
    freeze_parser = sub.add_parser("freeze", help="Freeze dataset")
    freeze_parser.add_argument("--test-months", type=int, default=12)
    sub.add_parser("build", help="Run clean, feature, and freeze stages")

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "ingest":
        ingest(args.symbols, args.tf, args.years)
    elif args.command == "clean":
        clean()
    elif args.command == "feature":
        feature()
    elif args.command == "freeze":
        freeze(test_months=args.test_months)
    elif args.command == "build":
        build()
    else:  # pragma: no cover
        raise RuntimeError(f"Unknown command {args.command}")


if __name__ == "__main__":
    main()
