FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /uvx /bin/

WORKDIR /app

COPY . .

RUN uv sync --locked 

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Railway requires binding to dynamic $PORT
CMD ["sh", "-c", "uv run uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"]
