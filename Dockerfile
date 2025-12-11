FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./

COPY src ./src

RUN uv sync --locked 

ENV PYTHONPATH=/app/src

ENV PYTHONUNBUFFERED=1


CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

