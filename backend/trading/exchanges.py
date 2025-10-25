"""Exchange connectivity adapters for Alpaca paper trading and IEX market data."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query

from backend.auth.security import User, get_current_user
from backend.settings import get_settings
from backend.trading.schemas import Balance, Candle, ExchangeStatus, Order, OrderCreate, Position

router = APIRouter()


class AlpacaPaperAdapter:
    """In-memory paper trading adapter that mimics a subset of Alpaca APIs."""

    def __init__(self) -> None:
        self._orders: Dict[str, Order] = {}
        self._positions: Dict[str, Position] = {}
        self._cash: float = 100_000.0

    def create_order(self, payload: OrderCreate) -> Order:
        """Create a market or limit order and apply immediate fills for paper trading."""

        order_id = str(uuid4())
        created_at = datetime.now(timezone.utc)
        symbol = payload.symbol.upper()
        fill_price = payload.limit_price if payload.type == "limit" and payload.limit_price else None
        if fill_price is None:
            # Simulate market price using simple heuristic
            fill_price = 100.0 if payload.side == "buy" else 99.5
        signed_qty = payload.qty if payload.side == "buy" else -payload.qty
        cost = fill_price * signed_qty
        self._cash -= cost
        position = self._positions.get(symbol)
        if position is None:
            position = Position(
                symbol=symbol,
                qty=signed_qty,
                avg_price=fill_price,
                market_value=signed_qty * fill_price,
                unrealized_pl=0.0,
            )
        else:
            new_qty = position.qty + signed_qty
            if new_qty == 0:
                avg_price = 0.0
            else:
                avg_price = ((position.avg_price * position.qty) + (fill_price * signed_qty)) / new_qty
            position = Position(
                symbol=payload.symbol,
                qty=new_qty,
                avg_price=avg_price,
                market_value=new_qty * fill_price,
                unrealized_pl=position.unrealized_pl,
            )
        self._positions[symbol] = position

        order = Order(
            id=order_id,
            symbol=symbol,
            side=payload.side,
            qty=payload.qty,
            type=payload.type,
            status="filled",
            created_at=created_at,
            filled_qty=payload.qty,
            avg_fill_price=fill_price,
        )
        self._orders[order_id] = order
        return order

    def get_open_orders(self) -> List[Order]:
        """Return orders that are not fully filled."""

        return [order for order in self._orders.values() if order.status != "canceled"]

    def get_balance(self) -> Balance:
        """Return current cash balance and simulated equity."""

        equity = self._cash + sum(position.market_value for position in self._positions.values())
        return Balance(currency="USD", equity=equity, buying_power=self._cash)

    def get_position(self, symbol: str) -> Position:
        """Return the tracked position for a symbol."""

        symbol = symbol.upper()
        if symbol not in self._positions:
            raise HTTPException(status_code=404, detail="Position not found")
        return self._positions[symbol]


class IEXDataAdapter:
    """Market data adapter for IEX Cloud candles."""

    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(timeout=10.0)

    def get_candles(self, symbol: str, tf: str, start: datetime | None, end: datetime | None) -> List[Candle]:
        settings = get_settings()
        params = {"range": tf, "token": settings.iex_token}
        if start:
            params["from"] = start.isoformat()
        if end:
            params["to"] = end.isoformat()
        url = f"{settings.iex_base_url}/stock/{symbol}/chart/{tf}"
        response = self._client.get(url, params={k: v for k, v in params.items() if v is not None})
        response.raise_for_status()
        data = response.json()
        candles: List[Candle] = []
        for entry in data:
            candle = Candle(
                timestamp=datetime.fromisoformat(entry["date"] + "T" + entry.get("minute", "00:00") + "+00:00"),
                symbol=symbol,
                open=float(entry.get("open", 0.0)),
                high=float(entry.get("high", 0.0)),
                low=float(entry.get("low", 0.0)),
                close=float(entry.get("close", 0.0)),
                volume=float(entry.get("volume", 0.0)),
            )
            candles.append(candle)
        return candles


_alpaca_adapter = AlpacaPaperAdapter()
_iex_adapter = IEXDataAdapter()


def get_alpaca_adapter() -> AlpacaPaperAdapter:
    return _alpaca_adapter


def get_iex_adapter() -> IEXDataAdapter:
    return _iex_adapter


@router.get("/", response_model=List[str])
def list_exchanges(_: User = Depends(get_current_user)) -> List[str]:
    """Return the list of available exchange adapters."""

    return ["alpaca", "iex"]


@router.get("/{exchange}/status", response_model=ExchangeStatus)
def get_exchange_status(exchange: str, _: User = Depends(get_current_user)) -> ExchangeStatus:
    """Return the status of a given exchange."""

    exchange_lower = exchange.lower()
    if exchange_lower not in {"alpaca", "iex"}:
        raise HTTPException(status_code=404, detail="Exchange not supported")
    status = "online"
    return ExchangeStatus(exchange=exchange_lower, status=status, mode="paper")


@router.post("/alpaca/orders", response_model=Order)
def place_order(
    payload: OrderCreate,
    adapter: AlpacaPaperAdapter = Depends(get_alpaca_adapter),
    _: User = Depends(get_current_user),
) -> Order:
    """Place a paper trade order using the Alpaca adapter."""

    return adapter.create_order(payload)


@router.get("/alpaca/orders", response_model=List[Order])
def list_orders(
    adapter: AlpacaPaperAdapter = Depends(get_alpaca_adapter),
    _: User = Depends(get_current_user),
) -> List[Order]:
    """List existing paper trade orders."""

    return adapter.get_open_orders()


@router.get("/alpaca/balance", response_model=Balance)
def get_balance(
    adapter: AlpacaPaperAdapter = Depends(get_alpaca_adapter),
    _: User = Depends(get_current_user),
) -> Balance:
    """Return the paper trading account balance."""

    return adapter.get_balance()


@router.get("/alpaca/positions/{symbol}", response_model=Position)
def get_position(
    symbol: str,
    adapter: AlpacaPaperAdapter = Depends(get_alpaca_adapter),
    _: User = Depends(get_current_user),
) -> Position:
    """Return the paper trading position for a symbol."""

    return adapter.get_position(symbol.upper())


@router.get("/iex/candles", response_model=List[Candle])
def get_candles(
    symbol: str = Query(..., description="Symbol to query"),
    tf: str = Query("1m", description="Time frame to request"),
    start: datetime | None = None,
    end: datetime | None = None,
    adapter: IEXDataAdapter = Depends(get_iex_adapter),
    _: User = Depends(get_current_user),
) -> List[Candle]:
    """Fetch candles from IEX Cloud."""

    try:
        return adapter.get_candles(symbol=symbol, tf=tf, start=start, end=end)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail="Failed to fetch candles") from exc
