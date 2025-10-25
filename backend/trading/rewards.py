"""Reward shaping utilities for the trading agents."""

from __future__ import annotations

import numpy as np
from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.trading.schemas import RewardBreakdown, RewardRequest

router = APIRouter()


def differential_sortino(returns: np.ndarray, target: float = 0.0) -> float:
    """Compute differential Sortino ratio."""

    if returns.size == 0:
        return 0.0
    downside = returns[returns < target]
    downside_deviation = np.sqrt(np.mean(np.square(np.clip(target - downside, 0, None)))) if downside.size else 1e-8
    mean_return = returns.mean() - target
    return float(mean_return / downside_deviation)


def conditional_value_at_risk(returns: np.ndarray, alpha: float = 0.95) -> float:
    """Estimate CVaR at the specified confidence level."""

    if returns.size == 0:
        return 0.0
    losses = np.sort(-returns)
    index = int(np.ceil(alpha * losses.size)) - 1
    index = max(min(index, losses.size - 1), 0)
    tail_losses = losses[: index + 1]
    return float(-tail_losses.mean())


def compute_reward(returns: np.ndarray, cvar_lambda: float, fee_penalty: float) -> RewardBreakdown:
    """Combine differential Sortino, CVaR penalty, and transaction fees."""

    returns = np.asarray(returns, dtype=float)
    if returns.size == 0:
        return RewardBreakdown(differential_sortino(returns), 0.0, fee_penalty, -fee_penalty)
    diff_sortino = differential_sortino(returns)
    cvar_value = conditional_value_at_risk(returns)
    cvar_penalty = cvar_lambda * max(cvar_value, 0.0)
    total = diff_sortino - cvar_penalty - fee_penalty
    return RewardBreakdown(
        differential_sortino=diff_sortino,
        cvar_penalty=cvar_penalty,
        fee_penalty=fee_penalty,
        total=total,
    )


@router.post("/compute", response_model=RewardBreakdown)
def compute_reward_endpoint(
    request: RewardRequest,
    _: User = Depends(get_current_user),
) -> RewardBreakdown:
    """Compute the reward breakdown for monitoring purposes."""

    returns = np.asarray(request.returns, dtype=float)
    fee_penalty = request.transaction_cost
    return compute_reward(returns, cvar_lambda=request.cvar_lambda, fee_penalty=fee_penalty)
