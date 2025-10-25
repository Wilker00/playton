"""Shared pydantic schemas for trading endpoints."""

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Candle(BaseModel):
    """Historical OHLCV candle with engineered features."""

    timestamp: datetime
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = Field(default=None, alias="macdSignal")
    bb_upper: Optional[float] = Field(default=None, alias="bbUpper")
    bb_lower: Optional[float] = Field(default=None, alias="bbLower")
    rv: Optional[float] = None
    split: Literal["train", "test"] | None = None

    model_config = {
        "populate_by_name": True,
    }


class Balance(BaseModel):
    """Account balance summary."""

    currency: str
    equity: float
    buying_power: float


class Position(BaseModel):
    """Position details for a tracked symbol."""

    symbol: str
    qty: float
    avg_price: float
    market_value: float
    unrealized_pl: float


class OrderCreate(BaseModel):
    """Order placement request."""

    symbol: str
    side: Literal["buy", "sell"]
    qty: float
    type: Literal["market", "limit"] = "market"
    limit_price: Optional[float] = Field(default=None, alias="limitPrice")

    model_config = {
        "populate_by_name": True,
    }


class Order(BaseModel):
    """Placed order representation."""

    id: str
    symbol: str
    side: Literal["buy", "sell"]
    qty: float
    type: str
    status: Literal["open", "filled", "canceled"]
    created_at: datetime
    filled_qty: float = 0.0
    avg_fill_price: Optional[float] = None


class ExchangeStatus(BaseModel):
    """Status summary for an exchange adapter."""

    exchange: str
    status: Literal["online", "offline", "degraded"]
    mode: Literal["paper", "live"] = "paper"


class PortfolioMetricsRequest(BaseModel):
    """Input payload for metrics computation."""

    returns: List[float] = Field(default_factory=list)
    weights: Optional[List[float]] = None


class PortfolioMetrics(BaseModel):
    """Key performance indicators for the portfolio."""

    cumulative_return: float
    sharpe: float
    sortino: float
    cvar: float
    max_drawdown: float
    turnover: float


class RewardRequest(BaseModel):
    """Reward computation request payload."""

    returns: List[float]
    cvar_lambda: float = 1.0
    transaction_cost: float = 0.0


class RewardBreakdown(BaseModel):
    """Reward decomposition for monitoring."""

    differential_sortino: float
    cvar_penalty: float
    fee_penalty: float
    total: float


class RiskLimits(BaseModel):
    """Risk guard rails for the system."""

    max_leverage: float
    daily_loss_limit: float
    kill_switch: bool
    mode: Literal["paper", "live"]


class FailSafeStatus(BaseModel):
    """Fail safe state representation."""

    active: bool
    reason: Optional[str] = None
    activated_at: Optional[datetime] = None


class BusStatus(BaseModel):
    """Redis and Ray transport status."""

    redis: str
    ray: str


class WalletStatus(BaseModel):
    """Wallet integration summary."""

    signing_required: bool
    custody: Literal["client", "server"]
    connected: bool


class AgentConfig(BaseModel):
    """Configuration of trading agents."""

    name: str
    strategy: str
    regime: str
    risk_target: float


class AgentConfigResponse(BaseModel):
    """Aggregated agent configuration list."""

    agents: List[AgentConfig]


class EnvConfig(BaseModel):
    """Environment configuration used by RL training."""

    data_path: str
    window_size: int
    assets: List[str]
    transaction_cost: float
    slippage: float


class RegimeState(BaseModel):
    """Current detected market regime."""

    regime: str
    confidence: float
    updated_at: datetime
