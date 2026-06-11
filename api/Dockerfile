# syntax=docker/dockerfile:1

# --- Build stage: resolve dependencies into a virtualenv with uv ---
FROM python:3.13-slim-bookworm AS builder

# Pin uv by copying it from its official image (same version used locally).
COPY --from=ghcr.io/astral-sh/uv:0.11.21 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# --- Runtime stage: copy the venv + app, run as a non-root user ---
FROM python:3.13-slim-bookworm AS runtime

RUN groupadd --system app && useradd --system --gid app --no-create-home app

ENV PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY app ./app

USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
