FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_LINK_MODE=copy

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers 
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/

COPY ./app /app/app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

CMD ["fastapi", "run", "app/main.py"]