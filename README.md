# Institutional Grade Multi-Agent RL Trading Platform MVP

This repository implements a production-ready skeleton for a multi-agent reinforcement learning trading stack running exclusively in paper mode. It ships a FastAPI backend with JWT auth, a DVC-managed data pipeline, a Stable-Baselines3 PPO baseline with MLflow tracking, VectorBT evaluation, and a Vite React UI wired into the API.

## Repository Layout

```
backend/             FastAPI application, routers, risk/reward services
rl/                  Data pipeline, configs, PPO training and evaluation utilities
web/webapp/          Vite React application with live API integration
ops/                 Deployment and CI placeholders
```

## Prerequisites

* Python 3.11
* Node 18+
* DVC (installed automatically via `pip install -e .[dev]`)
* Redis (optional; status is probed but not required)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Install UI dependencies:

```bash
cd web/webapp
npm install
```

## Data Pipeline (DVC)

The pipeline produces engineered OHLCV features using public-market safe synthetic data by default.

```bash
# Ingest three years of 1h candles (synthetic demo data)
python -m rl.data ingest --symbols SPY QQQ BTCUSD ETHUSD --tf 1h --years 3

# Build the clean -> feature -> frozen stages
python -m rl.data build
# or via DVC
dvc repro
```

Outputs land in `data/frozen/{train,test}.parquet` with schema documented in `rl/data.py`.

## Training & Evaluation

Train the PPO baseline with MLflow logging:

```bash
python -m rl.train --env-config rl/configs/env.yaml --algo-config rl/configs/ppo_baseline.yaml
```

Evaluate the resulting run with VectorBT backtesting (logs stats + equity curve back to MLflow):

```bash
python -m rl.eval --run-id <MLFLOW_RUN_ID>
```

MLflow artifacts include the trained policy `.zip`, configs, evaluation report, and equity curve plot.

## Backend API

Run the FastAPI service:

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Key endpoints (JWT required, paper mode only):

* `POST /api/auth/token` – issue short-lived JWT (form: username/password/scope)
* `POST /api/metrics/portfolio` – compute return, Sharpe, Sortino, CVaR, drawdown
* `POST /api/rewards/compute` – differential Sortino with CVaR and fee penalties
* `POST /api/fail-safe/activate` – toggle kill switch for paper trading
* `GET /api/exchanges/*` – Alpaca paper order flow & IEX candle retrieval (mocked)
* `GET /metrics` – Prometheus exposition for observability

See `backend/trading/` modules for additional environment, regime, wallet, and explainability routes.

## React UI

Start the Vite dev server (proxying `/api` to FastAPI):

```bash
cd web/webapp
npm run dev
```

UI features:

* Login form issuing JWT tokens stored in localStorage
* Dashboard polling portfolio metrics and risk guardrails with a permanent red “LIVE MODE (DISABLED)” banner
* Paper sandbox for tweaking environment parameters and viewing agent configs
* Explainability view rendering SHAP-like contributions from the dataset
* Risk console with fail-safe activation
* Exchange, monitoring, wallet, settings, and docs sections backed by live API calls

All screens operate strictly in paper mode; no live execution occurs without human approval.

## Testing

```bash
pytest backend/tests
```

## Docker & Compose

Build and run the API together with Redis and MLflow tracking:

```bash
docker-compose up --build
```

The compose stack exposes FastAPI on `localhost:8000`, Redis on `6379`, and MLflow UI on `5000`.

## Operational Guardrails

* JWT auth with configurable secret key (`API_SECRET_KEY`)
* Fail-safe state stored server-side and surfaced via API/UI
* No private key custody – wallet endpoint asserts client-side signing requirement
* Paper mode default, live execution flagged visually and programmatically
