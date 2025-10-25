"""Agent cooperation protocols."""

from typing import Dict

from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user

router = APIRouter()


@router.get("/protocols", response_model=Dict[str, str])
def list_protocols(_: User = Depends(get_current_user)) -> Dict[str, str]:
    """Return placeholder cooperation strategies."""
    return {
        "parameter_sharing": "shared_backbone_small_heads",
        "action_sharing": "broadcast_target_weights",
        "confidence_broadcast": "risk_adjusted_scores",
    }
