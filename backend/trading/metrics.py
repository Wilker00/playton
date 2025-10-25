"""Performance and risk metrics endpoints."""

from __future__ import annotations

import numpy as np
from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.trading.schemas import PortfolioMetrics, PortfolioMetricsRequest

router = APIRouter()


def sharpe_ratio(returns: np.ndarray, risk_free: float = 0.0) -> float:
    if returns.size == 0:
        return 0.0
    excess = returns - risk_free
    std = returns.std(ddof=1) if returns.size > 1 else 1e-8
    return float(np.sqrt(252) * excess.mean() / std)


def sortino_ratio(returns: np.ndarray, target: float = 0.0) -> float:
    if returns.size == 0:
        return 0.0
    downside = returns[returns < target]
    downside_std = np.sqrt(np.mean((downside - target) ** 2)) if downside.size else 1e-8
    return float(np.sqrt(252) * (returns.mean() - target) / downside_std)


def max_drawdown(equity_curve: np.ndarray) -> float:
    if equity_curve.size == 0:
        return 0.0
    peaks = np.maximum.accumulate(equity_curve)
    drawdowns = (equity_curve - peaks) / peaks
    return float(drawdowns.min())


def turnover(weights: np.ndarray) -> float:
    if weights.size == 0:
        return 0.0
    diffs = np.diff(weights, axis=0)
    if diffs.size == 0:
        return 0.0
    return float(np.abs(diffs).sum() / max(diffs.shape[0], 1))


def cvar95(returns: np.ndarray) -> float:
    if returns.size == 0:
        return 0.0
    sorted_returns = np.sort(returns)
    cutoff = int(np.ceil(0.05 * sorted_returns.size))
    tail = sorted_returns[:cutoff] if cutoff > 0 else sorted_returns
    return float(tail.mean())


def compute_metrics(request: PortfolioMetricsRequest) -> PortfolioMetrics:
    returns = np.asarray(request.returns, dtype=float)
    weights = np.asarray(request.weights, dtype=float) if request.weights else np.empty((0,))
    equity_curve = np.cumprod(1 + returns)
    metrics = PortfolioMetrics(
        cumulative_return=float(equity_curve[-1] - 1 if equity_curve.size else 0.0),
        sharpe=sharpe_ratio(returns),
        sortino=sortino_ratio(returns),
        cvar=cvar95(returns),
        max_drawdown=max_drawdown(equity_curve),
        turnover=turnover(weights) if weights.size else 0.0,
    )
    return metrics


@router.post("/portfolio", response_model=PortfolioMetrics)
def portfolio_metrics(
    request: PortfolioMetricsRequest,
    _: User = Depends(get_current_user),
) -> PortfolioMetrics:
    """Compute key portfolio metrics from returns and optional weights."""

    return compute_metrics(request)
