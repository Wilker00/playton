"""Regime detection utilities."""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.settings import get_settings
from backend.trading.schemas import RegimeState

router = APIRouter()


def detect_regime() -> RegimeState:
    settings = get_settings()
    data_root = Path(settings.data_root)
    if data_root.is_dir():
        file_path = data_root / "frozen" / "train.parquet"
    elif data_root.is_file():
        file_path = data_root
    else:
        file_path = None
    regime = "SIDEWAYS_CHOPPY"
    confidence = 0.5
    if file_path and file_path.exists():
        df = pd.read_parquet(file_path)
        if "close" in df.columns:
            df = df.sort_values("timestamp")
            returns = df.groupby("timestamp")["close"].mean().pct_change().dropna()
            if not returns.empty:
                avg = returns.mean()
                vol = returns.std()
                if avg > 0 and vol > 0.01:
                    regime = "BULL_VOLATILE"
                    confidence = min(0.95, float(avg / (vol + 1e-6)))
                elif avg < 0 and vol > 0.01:
                    regime = "BEAR_STABLE"
                    confidence = min(0.95, float(-avg / (vol + 1e-6)))
                else:
                    regime = "SIDEWAYS_CHOPPY"
                    confidence = 0.6
    return RegimeState(regime=regime, confidence=confidence, updated_at=datetime.now(timezone.utc))


@router.get("/current", response_model=RegimeState)
def current_regime(_: User = Depends(get_current_user)) -> RegimeState:
    """Return the latest detected regime."""

    return detect_regime()
