"""Trading agent configuration endpoints."""

from fastapi import APIRouter, Depends

from backend.auth.security import User, get_current_user
from backend.trading.schemas import AgentConfig, AgentConfigResponse

router = APIRouter()

DEFAULT_AGENTS = [
    AgentConfig(name="momentum", strategy="ppo", regime="BULL_VOLATILE", risk_target=0.6),
    AgentConfig(name="mean_reversion", strategy="ppo", regime="SIDEWAYS_CHOPPY", risk_target=0.3),
    AgentConfig(name="volatility", strategy="ppo", regime="BEAR_STABLE", risk_target=0.1),
]


@router.get("/config", response_model=AgentConfigResponse)
def get_agent_config(_: User = Depends(get_current_user)) -> AgentConfigResponse:
    """Return the current agent configuration set."""

    return AgentConfigResponse(agents=DEFAULT_AGENTS)
