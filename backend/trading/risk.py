"""Risk controls and guardrails endpoints."""

from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.trading.fail_safe import fail_safe_state
from backend.trading.schemas import RiskLimits

router = APIRouter()


@router.get("/limits", response_model=RiskLimits)
def get_risk_limits(_: User = Depends(get_current_user)) -> RiskLimits:
    """Return current risk guard rails."""

    return RiskLimits(
        max_leverage=2.0,
        daily_loss_limit=-0.02,
        kill_switch=fail_safe_state["active"],
        mode="paper",
    )
