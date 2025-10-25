"""Event bus integration using Redis and Ray."""

import asyncio
from urllib.parse import urlparse

from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.settings import get_settings
from backend.trading.schemas import BusStatus

router = APIRouter()


async def _check_redis(url: str) -> str:
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "localhost"
        port = parsed.port or 6379
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host=host, port=port), timeout=0.5)
        writer.close()
        await writer.wait_closed()
        return "online"
    except Exception:  # pragma: no cover - best effort
        return "offline"


@router.get("/status", response_model=BusStatus)
async def get_bus_status(_: User = Depends(get_current_user)) -> BusStatus:
    """Return Redis and Ray status."""

    settings = get_settings()
    redis_status = await _check_redis(settings.redis_url)
    return BusStatus(redis=redis_status, ray=settings.ray_status)
