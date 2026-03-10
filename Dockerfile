FROM ghcr.io/astral-sh/uv:latest AS uv_bin

FROM python:3.13-alpine

COPY --from=uv_bin /uv /uvx /bin/

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_COMPILE_BYTECODE=1

COPY pyproject.toml uv.lock ./

RUN uv sync --no-install-project --no-dev

COPY . .

RUN uv sync --no-dev

CMD ["python", "main.py"]