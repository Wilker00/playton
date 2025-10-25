FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/
RUN pip install --upgrade pip && pip install -e .[dev]

COPY backend /app/backend
COPY rl /app/rl
COPY web /app/web
COPY dvc.yaml /app/dvc.yaml

ENV UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
