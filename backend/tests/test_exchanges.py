"""Exchange adapter tests."""

import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app


@pytest.fixture()
def auth_headers() -> dict[str, str]:
    client = TestClient(app)
    response = client.post(
        "/api/auth/token",
        data={"username": "tester", "password": "secret", "scope": "admin", "grant_type": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_alpaca_order_flow(auth_headers: dict[str, str]) -> None:
    client = TestClient(app)
    order_response = client.post(
        "/api/exchanges/alpaca/orders",
        headers=auth_headers,
        json={"symbol": "SPY", "side": "buy", "qty": 10},
    )
    assert order_response.status_code == 200
    orders = client.get("/api/exchanges/alpaca/orders", headers=auth_headers)
    assert orders.status_code == 200
    balance = client.get("/api/exchanges/alpaca/balance", headers=auth_headers)
    assert balance.status_code == 200
    position = client.get("/api/exchanges/alpaca/positions/SPY", headers=auth_headers)
    assert position.status_code == 200


def test_iex_candles(auth_headers: dict[str, str], mocker: MockerFixture) -> None:
    client = TestClient(app)
    fixture_path = Path(__file__).parent / "fixtures" / "iex_candles.json"
    payload = json.loads(fixture_path.read_text())
    mock_response = mocker.Mock()
    mock_response.json.return_value = payload
    mock_response.raise_for_status.return_value = None
    mocker.patch("backend.trading.exchanges._iex_adapter._client.get", return_value=mock_response)
    candles = client.get("/api/exchanges/iex/candles", headers=auth_headers, params={"symbol": "SPY", "tf": "1d"})
    assert candles.status_code == 200
    body = candles.json()
    assert len(body) == len(payload)
    assert body[0]["symbol"] == "SPY"
