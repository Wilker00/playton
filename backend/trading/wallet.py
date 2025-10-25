"""Wallet service endpoints enforcing client-side signing only."""

from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.trading.schemas import WalletStatus

router = APIRouter()


@router.get("/status", response_model=WalletStatus)
def wallet_status(_: User = Depends(get_current_user)) -> WalletStatus:
    """Return wallet integration status."""

    return WalletStatus(signing_required=True, custody="client", connected=False)
