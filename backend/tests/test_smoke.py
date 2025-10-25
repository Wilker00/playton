"""Basic smoke tests for the FastAPI application."""

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app import app


def test_health_and_auth_flow() -> None:
    client = TestClient(app)
    health = client.get("/healthz")
    assert health.status_code == 200
    response = client.post(
        "/api/auth/token",
        data={"username": "tester", "password": "secret", "scope": "admin", "grant_type": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    metrics = client.post("/api/metrics/portfolio", json={"returns": [0.01, -0.02, 0.03]}, headers=headers)
    assert metrics.status_code == 200
