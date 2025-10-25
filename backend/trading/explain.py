"""Explainability endpoints for per-trade reasoning."""

from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.settings import get_settings

router = APIRouter()


@router.get("/shap", response_model=Dict[str, float])
def get_shap_summary(_: User = Depends(get_current_user)) -> Dict[str, float]:
    """Approximate SHAP-style contributions using feature correlations."""

    settings = get_settings()
    data_root = Path(settings.data_root)
    file_path = data_root / "frozen" / "train.parquet" if data_root.is_dir() else data_root
    if not file_path.exists():
        return {"price_momentum": 0.0, "volatility": 0.0, "volume_pressure": 0.0}
    df = pd.read_parquet(file_path)
    if df.empty:
        return {"price_momentum": 0.0, "volatility": 0.0, "volume_pressure": 0.0}
    df = df.sort_values("timestamp")
    grouped = df.groupby("timestamp").mean(numeric_only=True)
    returns = grouped["close"].pct_change().dropna()
    contributions = {}
    for feature in ["rsi", "macd", "rv", "volume"]:
        if feature in grouped.columns:
            feature_series = grouped[feature].loc[returns.index]
            corr = returns.corr(feature_series)
            contributions[feature] = float(corr if not np.isnan(corr) else 0.0)
    total = sum(abs(v) for v in contributions.values()) or 1.0
    normalized = {f"feature_{k}": float(v / total) for k, v in contributions.items()}
    return normalized
