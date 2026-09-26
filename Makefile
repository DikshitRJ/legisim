# ==============================================================================
# LegiSim Platform Makefile
# ==============================================================================
# Helper automation for running, testing, linting, and deploying LegiSim services.
# ==============================================================================

SHELL := /bin/bash
COMPOSE := docker compose
PYTHON := python3

.PHONY: help setup up down restart build logs logs-backend ps migrate migrate-create test test-local lint lint-fix format shell-backend shell-db clean

# Default target
help:
	@echo "========================================================================"
	@echo "LegiSim Platform Management Commands"
	@echo "========================================================================"
	@echo "  make setup         - Initialize .env and prepare local environment"
	@echo "  make up            - Launch all 12 services via Docker Compose in background"
	@echo "  make down          - Stop and remove all running containers"
	@echo "  make restart       - Restart all Docker services"
	@echo "  make build         - Build/rebuild Docker images"
	@echo "  make logs          - Follow live logs across all containers"
	@echo "  make logs-backend  - Follow live logs specifically for the FastAPI backend"
	@echo "  make ps            - Show container status and health"
	@echo "  make migrate       - Run Alembic database migrations (docker exec)"
	@echo "  make test          - Run backend Pytest test suite (docker exec)"
	@echo "  make test-local    - Run backend Pytest locally in virtual environment"
	@echo "  make lint          - Run Ruff linter and Mypy type checker"
	@echo "  make lint-fix      - Automatically fix Ruff linter and formatting issues"
	@echo "  make format        - Format Python codebase using Ruff"
	@echo "  make shell-backend - Open interactive bash session in backend container"
	@echo "  make shell-db      - Open interactive PostgreSQL psql session"
	@echo "  make clean         - Remove containers, volumes, and temporary files"
	@echo "========================================================================"

# Initial environment setup
setup:
	@echo "==> Setting up environment..."
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
	else \
		echo ".env already exists, skipping copy."; \
	fi
	@if [ ! -f backend/.env ]; then \
		echo "Creating backend/.env from backend/.env.example..."; \
		cp backend/.env.example backend/.env; \
	fi
	@chmod +x docker/postgres/init-db.sh 2>/dev/null || true
	@echo "==> Setup completed successfully."

# Start all Docker Compose services
up:
	@echo "==> Starting all services..."
	$(COMPOSE) up -d

# Stop all Docker Compose services
down:
	@echo "==> Stopping all services..."
	$(COMPOSE) down

# Restart all services
restart:
	@echo "==> Restarting all services..."
	$(COMPOSE) restart

# Build or rebuild images
build:
	@echo "==> Building container images..."
	$(COMPOSE) build

# Follow logs across all containers
logs:
	$(COMPOSE) logs -f

# Follow logs for backend service only
logs-backend:
	$(COMPOSE) logs -f fastapi-backend

# View status of services
ps:
	$(COMPOSE) ps

# Run database migrations inside running container
migrate:
	@echo "==> Applying database migrations..."
	@$(COMPOSE) exec fastapi-backend alembic upgrade head || ( \
		echo "Container not running, attempting local migration..."; \
		cd backend && alembic upgrade head \
	)

# Create a new migration revision
migrate-create:
	@read -p "Enter migration description: " desc; \
	$(COMPOSE) exec fastapi-backend alembic revision --autogenerate -m "$$desc" || ( \
		cd backend && alembic revision --autogenerate -m "$$desc" \
	)

# Run test suite inside backend container
test:
	@echo "==> Running tests in Docker container..."
	@$(COMPOSE) exec fastapi-backend pytest -v || ( \
		echo "Docker execution failed or containers not up. Try 'make test-local'." \
	)

# Run test suite locally using active virtual environment
test-local:
	@echo "==> Running tests locally..."
	@if [ -d backend/.venv ]; then \
		source backend/.venv/bin/activate && cd backend && pytest -v; \
	else \
		cd backend && pytest -v; \
	fi

# Lint codebase with Ruff and check types with Mypy
lint:
	@echo "==> Running Ruff linter..."
	@if [ -d backend/.venv ]; then \
		source backend/.venv/bin/activate && ruff check backend/; \
	else \
		ruff check backend/; \
	fi
	@echo "==> Running Mypy type checker..."
	@if [ -d backend/.venv ]; then \
		source backend/.venv/bin/activate && cd backend && mypy app; \
	else \
		cd backend && mypy app; \
	fi

# Fix auto-fixable Ruff issues and format code
lint-fix:
	@echo "==> Fixing linting and formatting issues..."
	@if [ -d backend/.venv ]; then \
		source backend/.venv/bin/activate && ruff check --fix backend/ && ruff format backend/; \
	else \
		ruff check --fix backend/ && ruff format backend/; \
	fi

# Format code with Ruff
format:
	@echo "==> Formatting code..."
	@if [ -d backend/.venv ]; then \
		source backend/.venv/bin/activate && ruff format backend/; \
	else \
		ruff format backend/; \
	fi

# Interactive shell in FastAPI backend container
shell-backend:
	$(COMPOSE) exec fastapi-backend bash

# Interactive PostgreSQL shell
shell-db:
	$(COMPOSE) exec postgres psql -U legisim -d legisim

# Clean up containers, volumes, and temporary caches
clean:
	@echo "==> Cleaning up containers and caches..."
	$(COMPOSE) down -v --remove-orphans
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "==> Cleanup complete."
