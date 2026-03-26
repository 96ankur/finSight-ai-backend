# FastAPI + Beanie Production Boilerplate

A production-ready FastAPI backend with Beanie (MongoDB ODM), JWT authentication, structured logging, and enterprise-level architecture.

## Tech Stack

- **Python 3.11+** with fully async codebase
- **FastAPI** -- high-performance ASGI framework
- **Beanie** -- async MongoDB ODM built on Motor
- **Pydantic v2** -- data validation and settings management
- **JWT** -- access + refresh token authentication with RBAC
- **structlog** -- structured JSON logging with correlation IDs
- **Docker** -- multi-stage builds with Gunicorn + Uvicorn workers

## Project Structure

```
app/
├── main.py                  # Application factory and middleware setup
├── core/                    # Cross-cutting concerns
│   ├── config.py            # Pydantic BaseSettings (env-driven)
│   ├── security.py          # JWT + password hashing
│   ├── logging.py           # Structured logging setup
│   ├── events.py            # Lifespan (startup/shutdown)
│   └── dependencies.py      # Auth guards and RBAC
├── api/v1/                  # Versioned API layer
│   ├── api.py               # Router aggregation
│   └── endpoints/           # Route handlers
├── models/                  # Beanie document models
├── schemas/                 # Pydantic request/response DTOs
├── services/                # Business logic layer
├── repositories/            # Data access layer
├── db/                      # Database connection and init
├── exceptions/              # Custom exception hierarchy
├── middleware/              # Correlation ID + request logging
└── utils/                   # Shared helpers
tests/                       # pytest async test suite
```

## Quick Start

### 1. Clone and configure

```bash
cp .env.example .env
# Edit .env with your settings (especially JWT_SECRET_KEY)
```

### 2. Run with Docker Compose

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` with docs at `/docs`.

### 3. Local Development

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -e ".[dev]"
pre-commit install

uvicorn app.main:app --reload
```

### 4. Run Tests

```bash
pytest -v
```

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/v1/health` | Liveness probe | No |
| GET | `/api/v1/health/ready` | Readiness probe (DB check) | No |
| POST | `/api/v1/auth/register` | Register new user | No |
| POST | `/api/v1/auth/login` | Login (get tokens) | No |
| POST | `/api/v1/auth/refresh` | Refresh token pair | No |
| GET | `/api/v1/auth/me` | Current user profile | Bearer |
| GET | `/api/v1/users` | List users (paginated) | Admin |
| GET | `/api/v1/users/{id}` | Get user by ID | Admin |
| PATCH | `/api/v1/users/me` | Update own profile | Bearer |
| PATCH | `/api/v1/users/{id}` | Admin update user | Admin |
| DELETE | `/api/v1/users/{id}` | Delete user | Admin |

## Configuration

All settings are driven by environment variables (12-factor). See `.env.example` for the full list. Key settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ENV` | `development` | `development` / `staging` / `production` |
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `JWT_SECRET_KEY` | *(required)* | Minimum 32 characters |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Access token TTL |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` | Refresh token TTL |
| `LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `RATE_LIMIT_PER_MINUTE` | `60` | Requests per minute per IP |

## Code Quality

```bash
ruff check .          # Lint
ruff format .         # Format (or use black)
mypy app/             # Type checking
pre-commit run --all  # Run all hooks
```

## Production Deployment

The included `Dockerfile` uses multi-stage builds and runs as a non-root user. `gunicorn.conf.py` configures Uvicorn workers with sensible defaults:

```bash
docker compose -f docker-compose.yml up -d
```

Swagger docs are automatically disabled when `APP_ENV=production`.
