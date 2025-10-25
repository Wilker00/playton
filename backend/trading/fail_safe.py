"""Fail-safe activation endpoints."""

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Body, Depends

from backend.auth.security import User, get_current_user
from backend.trading.schemas import FailSafeStatus

router = APIRouter()

fail_safe_state: Dict[str, Any] = {"active": False, "reason": None, "activated_at": None}


@router.post("/activate", response_model=FailSafeStatus)
def activate_fail_safe(
    reason: str | None = Body(default=None, embed=True),
    _: User = Depends(get_current_user),
) -> FailSafeStatus:
    """Enable the fail-safe mechanism to halt trading."""

    fail_safe_state["active"] = True
    fail_safe_state["reason"] = reason or "Manual activation"
    fail_safe_state["activated_at"] = datetime.now(timezone.utc)
    return FailSafeStatus(**fail_safe_state)


@router.post("/reset", response_model=FailSafeStatus)
def reset_fail_safe(_: User = Depends(get_current_user)) -> FailSafeStatus:
    """Reset the fail-safe back to idle state."""

    fail_safe_state["active"] = False
    fail_safe_state["reason"] = None
    fail_safe_state["activated_at"] = None
    return FailSafeStatus(**fail_safe_state)


@router.get("/status", response_model=FailSafeStatus)
def get_fail_safe_status(_: User = Depends(get_current_user)) -> FailSafeStatus:
    """Return the current fail-safe status."""

    return FailSafeStatus(**fail_safe_state)
