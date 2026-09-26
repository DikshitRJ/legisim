# Infrastructure & Docker Deployment Plan (LegiSim)

## 1. Overview & Purpose
This component defines the complete containerized infrastructure for LegiSim. The platform is designed to be self-hostable on a single VPS using Docker Compose, with zero external dependencies other than the Z.ai GLM API for LLM calls.

The architecture comprises 12 distinct services across four categories:
- **Core Application**: `api`, `worker`, `frontend`
- **Data Services**: `db`, `redis`, `minio`
- **AI/ML Services**: `jev`, `searxng`
- **Infrastructure**: `traefik`, `keycloak`, `langfuse`, `glitchtip`

## 2. Environment Variables (`.env.example`)
```env
# ====== Core Configuration ======
ENVIRONMENT=production
DOMAIN=legisim.com
SECRET_KEY=generate_a_secure_random_string

# ====== Database (PostgreSQL + pgvector) ======
POSTGRES_USER=legisim
POSTGRES_PASSWORD=legisim_db_pass
POSTGRES_DB=legisim
DATABASE_URL=postgresql://legisim:legisim_db_pass@db:5432/legisim

# ====== Redis ======
REDIS_PASSWORD=redis_secure_pass
REDIS_URL=redis://:redis_secure_pass@redis:6379/0

# ====== MinIO ======
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=minio_admin_pass
MINIO_SERVER_URL=https://s3.${DOMAIN}
S3_ENDPOINT=minio:9000
S3_ACCESS_KEY=admin
S3_SECRET_KEY=minio_admin_pass
S3_BUCKET_NAME=legisim-data

# ====== Authentication (Keycloak) ======
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=keycloak_admin_pass
AUTH_URL=https://auth.${DOMAIN}
OIDC_CLIENT_ID=legisim-app
OIDC_CLIENT_SECRET=client_secret_here

# ====== AI & Search Services ======
ZAI_API_KEY=your_zai_api_key_here
SEARXNG_URL=http://searxng:8080
JEV_SERVICE_URL=http://jev:8000/predict

# ====== Observability ======
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://langfuse.${DOMAIN}
GLITCHTIP_DSN=https://...@glitchtip.${DOMAIN}/1
```

## 3. Docker Compose Configuration (`docker-compose.yml`)
```yaml
version: '3.8'

x-logging: &default-logging
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

services:
  # ==========================================
  # Infrastructure Services
  # ==========================================
  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=false"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=admin@legisim.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "traefik-certs:/letsencrypt"
    networks:
      - legisim-network
    restart: unless-stopped

  keycloak:
    image: quay.io/keycloak/keycloak:23.0
    command: start --optimized
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://db:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: ${POSTGRES_PASSWORD}
      KEYCLOAK_ADMIN: ${KEYCLOAK_ADMIN}
      KEYCLOAK_ADMIN_PASSWORD: ${KEYCLOAK_ADMIN_PASSWORD}
      KC_HOSTNAME: auth.${DOMAIN}
      KC_PROXY: edge
    depends_on:
      db:
        condition: service_healthy
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.keycloak.rule=Host(`auth.${DOMAIN}`)"
      - "traefik.http.routers.keycloak.entrypoints=websecure"
      - "traefik.http.routers.keycloak.tls.certresolver=myresolver"
    restart: unless-stopped

  # ==========================================
  # Data Services
  # ==========================================
  db:
    image: ankane/pgvector:v0.5.1
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_MULTIPLE_DATABASES: "legisim,keycloak,glitchtip"
    volumes:
      - pg-data:/var/lib/postgresql/data
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    networks:
      - legisim-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis-data:/data
    networks:
      - legisim-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  minio:
    image: minio/minio:RELEASE.2023-11-20T22-40-07Z
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
      MINIO_SERVER_URL: ${MINIO_SERVER_URL}
    volumes:
      - minio-data:/data
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.minio.rule=Host(`s3.${DOMAIN}`)"
      - "traefik.http.routers.minio.entrypoints=websecure"
      - "traefik.http.routers.minio.tls.certresolver=myresolver"
      - "traefik.http.services.minio.loadbalancer.server.port=9000"
      - "traefik.http.routers.minio-console.rule=Host(`s3-console.${DOMAIN}`)"
      - "traefik.http.routers.minio-console.entrypoints=websecure"
      - "traefik.http.routers.minio-console.tls.certresolver=myresolver"
      - "traefik.http.services.minio-console.loadbalancer.server.port=9001"
    restart: unless-stopped

  # ==========================================
  # Core Application Services
  # ==========================================
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      S3_ENDPOINT: ${S3_ENDPOINT}
      S3_ACCESS_KEY: ${S3_ACCESS_KEY}
      S3_SECRET_KEY: ${S3_SECRET_KEY}
      ZAI_API_KEY: ${ZAI_API_KEY}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.${DOMAIN}`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=myresolver"
    restart: unless-stopped

  worker:
    build:
      context: ./backend
      dockerfile: Dockerfile.worker
    environment:
      DATABASE_URL: ${DATABASE_URL}
      REDIS_URL: ${REDIS_URL}
      ZAI_API_KEY: ${ZAI_API_KEY}
    depends_on:
      - api
    networks:
      - legisim-network
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      NEXT_PUBLIC_API_URL: https://api.${DOMAIN}
      NEXT_PUBLIC_AUTH_URL: https://auth.${DOMAIN}
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`app.${DOMAIN}`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=myresolver"
    restart: unless-stopped

  # ==========================================
  # AI/ML Services
  # ==========================================
  jev:
    build:
      context: ./ai-services/jev
      dockerfile: Dockerfile
    environment:
      MODEL_PATH: "/models/jev-bert"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    networks:
      - legisim-network
    restart: unless-stopped

  searxng:
    image: searxng/searxng:latest
    volumes:
      - ./searxng:/etc/searxng
    networks:
      - legisim-network
    restart: unless-stopped

  # ==========================================
  # Observability
  # ==========================================
  langfuse:
    image: langfuse/langfuse:latest
    environment:
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/postgres
    depends_on:
      db:
        condition: service_healthy
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.langfuse.rule=Host(`langfuse.${DOMAIN}`)"
      - "traefik.http.routers.langfuse.entrypoints=websecure"
      - "traefik.http.routers.langfuse.tls.certresolver=myresolver"
    restart: unless-stopped

  glitchtip:
    image: glitchtip/glitchtip:latest
    environment:
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@db:5432/postgres
      REDIS_URL: ${REDIS_URL}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      db:
        condition: service_healthy
    networks:
      - legisim-network
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.glitchtip.rule=Host(`glitchtip.${DOMAIN}`)"
      - "traefik.http.routers.glitchtip.entrypoints=websecure"
      - "traefik.http.routers.glitchtip.tls.certresolver=myresolver"
    restart: unless-stopped

networks:
  legisim-network:
    driver: bridge

volumes:
  traefik-certs:
  pg-data:
  redis-data:
  minio-data:
```

## 4. `docker-compose.dev.yml` (Development Overrides)
```yaml
version: '3.8'

services:
  traefik:
    # Disable ACME and use local ports
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
  
  api:
    build:
      context: ./backend
      target: development
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  
  worker:
    volumes:
      - ./backend:/app
    command: watchmedo auto-restart --directory=./ --pattern=*.py -- recursive -- celery -A worker.celery_app worker --loglevel=info

  frontend:
    build:
      context: ./frontend
      target: development
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev
```

## 5. Dockerfiles

### 5.1 Backend `api` (`backend/Dockerfile`)
```dockerfile
# Multi-stage Python build
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-slim as production
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 Backend `worker` (`backend/Dockerfile.worker`)
```dockerfile
FROM python:3.12-slim as builder
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-slim as production
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["celery", "-A", "app.worker.celery_app", "worker", "--loglevel=info"]
```

### 5.3 Frontend (`frontend/Dockerfile`)
```dockerfile
# Multi-stage Node build
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
```

### 5.4 JEV Service (`ai-services/jev/Dockerfile`)
```dockerfile
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Optional: Model download step here
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 6. Initialization Scripts

### PostgreSQL (`init-db.sh`)
```bash
#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE keycloak;
    CREATE DATABASE glitchtip;
    \c legisim
    CREATE EXTENSION IF NOT EXISTS vector;
EOSQL
```

## 7. Configuration Details
- **MinIO**: Initialize buckets via entrypoint script or MinIO MC client.
- **Keycloak**: Export realm from dev, mount `realm-export.json` to `/opt/keycloak/data/import` and set `KC_IMPORT=true`.
- **SearXNG**: Mount `settings.yml` to disable unwanted engines and restrict access.
- **GPU Passthrough**: Ensure Docker has the `nvidia-container-toolkit` installed on the host to pass the GPU to the JEV container.

## 8. Makefile (Common Commands)
```makefile
.PHONY: up down logs dev-up db-shell bash-api bash-frontend

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

dev-up:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

db-shell:
	docker compose exec db psql -U legisim -d legisim

bash-api:
	docker compose exec api bash

bash-frontend:
	docker compose exec frontend sh
```

## 9. Production Deployment Notes & Backup
- **VPS Requirements**: Minimum 16GB RAM, 4+ CPU Cores, NVMe storage. For JEV GPU support, an instance with a T4 or better is recommended.
- **Backup Strategy**: 
  - DB: Scheduled `pg_dump` via cron container pushing to external S3.
  - MinIO: Mirror command or external volume backup.
  - Redis: Mount `/data` to an EBS volume with snapshots.
- **Monitoring**: Host metrics via Node Exporter and Prometheus/Grafana (optional additions) tracking container health and resource limits.
