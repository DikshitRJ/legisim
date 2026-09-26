# ==============================================================================
# Stage 1: Builder
# ==============================================================================
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system build dependencies required for compiling native extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to a designated prefix directory
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==============================================================================
# Stage 2: Production Runner
# ==============================================================================
FROM python:3.12-slim AS runner

WORKDIR /app

# Install minimal runtime shared libraries and curl for container healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user and group
RUN groupadd -g 10001 legisim && \
    useradd -u 10001 -g legisim -s /bin/bash -m legisim

# Copy installed Python packages and binaries from the builder stage
COPY --from=builder /install /usr/local

# Copy application source code, Alembic migrations, and configurations
COPY --chown=legisim:legisim alembic.ini pyproject.toml ./
COPY --chown=legisim:legisim migrations ./migrations
COPY --chown=legisim:legisim app ./app

# Set runtime environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

# Switch to the non-root user
USER legisim

# Expose internal FastAPI port
EXPOSE 8000

# Container healthcheck using FastAPI health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
