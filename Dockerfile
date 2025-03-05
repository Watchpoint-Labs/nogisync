FROM ghcr.io/astral-sh/uv:python3.12-alpine

RUN mkdir /code
WORKDIR /code

# copy just the pyproject and uv.lock files and install before rest of code to avoid having to
# reinstall packages during build every time code changes
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache \
    uv sync --locked --no-dev

COPY nogisync /code/nogisync

CMD ["uv", "run", "--no-dev", "python", "-m", "nogisync.cli", "--help"]