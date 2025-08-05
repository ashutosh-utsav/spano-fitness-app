FROM ghcr.io/astral-sh/uv:debian

# Install curl and build deps for uv and some C extensions (bcrypt, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy pyproject and lock file first for caching
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies with uv
RUN uv sync

# Copy app
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default command
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

