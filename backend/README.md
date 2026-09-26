# LegiSim Backend

Asynchronous FastAPI backend service for the **LegiSim** multi-agent policy simulation platform.

---

## Tech Stack

- **Runtime:** Python 3.12+
- **Framework:** FastAPI 0.115+
- **Database:** PostgreSQL 16 + `pgvector`
- **ORM:** SQLAlchemy 2.0 (fully async via `asyncpg`)
- **Migrations:** Alembic (async configuration)
- **Data Validation & Settings:** Pydantic V2 & `pydantic-settings`
- **Cache & Pub/Sub:** Redis
- **Object Storage:** MinIO / AWS S3 (via `aioboto3`)
- **Linting & Formatting:** Ruff
- **Type Checking:** Mypy (strict mode)
- **Testing:** Pytest & `pytest-asyncio`

---

## Directory Layout

```text
backend/
├── app/
│   ├── api/                 # API routers and dependencies
│   │   └── routes/          # Domain endpoint routers
│   ├── core/                # Database engine, logging, exceptions, auth deps
│   │   ├── database.py      # Async session maker and get_db dependency
│   │   ├── exceptions.py    # Standard HTTP exception hierarchy
│   │   └── logging.py       # JSON / Dev structured logging
│   ├── data/                # Seed loaders, ETL, and data cubes
│   ├── engine/              # LangGraph simulation engine & agents
│   ├── models/              # SQLAlchemy 2.0 async models
│   │   ├── base.py          # DeclarativeBase, UUIDMixin, TimestampMixin
│   │   ├── notebook.py      # Notebooks and Sessions
│   │   └── officer.py       # Officers and Sessions
│   ├── schemas/             # Pydantic V2 schemas
│   │   └── common.py        # CamelModel, SuccessResponse, ErrorResponse
│   ├── services/            # Domain business logic
│   ├── config.py            # Pydantic BaseSettings singleton
│   └── main.py              # FastAPI application instance & lifespan
├── migrations/              # Alembic migration scripts
│   ├── versions/            # Migration version files
│   ├── env.py               # Async Alembic execution environment
│   └── script.py.mako       # Revision template
├── tests/                   # Pytest test suite
├── .env.example             # Example environment configuration
├── alembic.ini              # Alembic database configuration
├── pyproject.toml           # PEP 621 dependencies & tool configs
└── README.md                # Backend developer guide
```

---

## Getting Started

### 1. Prerequisites

- Python 3.12 or newer
- PostgreSQL 16 with the `vector` extension enabled
- Redis 7+
- MinIO (or AWS S3)
- `uv` (recommended) or `pip`

### 2. Environment Setup

Copy `.env.example` to `.env` and fill in necessary credentials:

```bash
cp .env.example .env
```

### 3. Installation

Using `uv` (fastest):

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

Or using standard `pip`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 4. Database Migrations

Run database migrations to initialize the schema:

```bash
# Upgrade to latest revision
alembic upgrade head

# Generate a new migration after model changes
alembic revision --autogenerate -m "describe changes"
```

### 5. Running the Development Server

Start the FastAPI application with live reloading:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Once running:
- **Interactive OpenAPI Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc Documentation:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check Endpoint:** [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## Code Standards & Conventions

1. **Async Everywhere:** All database interactions, file storage operations, and HTTP requests must be non-blocking async calls.
2. **SQLAlchemy 2.0 Style:** Use `Mapped[...]` and `mapped_column(...)`. Legacy `Column()` syntax is not permitted.
3. **camelCase API / snake_case DB:**
   - PostgreSQL table columns use `snake_case`.
   - API endpoints serialize/deserialize `camelCase` JSON fields using `CamelModel` from `app.schemas.common`.
4. **Primary Keys:** All database tables use UUID v4 primary keys inherited from `UUIDMixin`.
5. **Timestamps:** Timestamps must be timezone-aware using `DateTime(timezone=True)` with server defaults (`func.now()`).
6. **Linting & Formatting:**
   ```bash
   ruff check .
   ruff format .
   mypy .
   ```
7. **Testing:**
   ```bash
   pytest
   ```
