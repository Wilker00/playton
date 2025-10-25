"""FastAPI application entry point for the trading platform backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import PlainTextResponse

from backend.auth import security
from backend.settings import get_settings
from backend.trading import (
    agents,
    bus,
    envs,
    exchanges,
    fail_safe,
    metrics,
    regime,
    rewards,
    risk,
    wallet,
)

registry = CollectorRegistry()


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""

    settings = get_settings()
    app = FastAPI(title="Institutional Multi-Agent RL Trading Platform", openapi_url="/api/openapi.json")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    @app.get("/healthz", tags=["health"])
    def healthcheck() -> dict[str, str]:
        """Lightweight health endpoint."""

        return {"status": "ok", "mode": "paper"}

    @app.get("/metrics")
    def metrics_endpoint() -> PlainTextResponse:
        """Expose Prometheus metrics."""

        return PlainTextResponse(generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

    app.include_router(security.router, prefix="/api/auth", tags=["auth"])
    app.include_router(exchanges.router, prefix="/api/exchanges", tags=["exchanges"])
    app.include_router(envs.router, prefix="/api/envs", tags=["environment"])
    app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
    app.include_router(bus.router, prefix="/api/bus", tags=["bus"])
    app.include_router(risk.router, prefix="/api/risk", tags=["risk"])
    app.include_router(fail_safe.router, prefix="/api/fail-safe", tags=["fail-safe"])
    app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
    app.include_router(rewards.router, prefix="/api/rewards", tags=["rewards"])
    app.include_router(wallet.router, prefix="/api/wallet", tags=["wallet"])
    app.include_router(regime.router, prefix="/api/regime", tags=["regime"])

    return app


app = create_app()
