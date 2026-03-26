# Production-Grade FastAPI + Beanie Boilerplate Prompt

This document contains a **master prompt** designed to be fed into Large Language Models (LLMs)
to generate a **production-ready FastAPI backend** using **Beanie (MongoDB ODM)**.

The generated boilerplate follows **modern Python standards**, **enterprise-level architecture**,
and **real-world production best practices**.

---

## 🎯 Purpose

Use this prompt to generate:
- A scalable FastAPI backend
- MongoDB integration using Beanie
- JWT-based authentication
- Strict linting, formatting, and typing
- Production-grade logging
- Clean, maintainable folder structure
- DevOps and deployment readiness

---

## 🧠 MASTER PROMPT

Copy everything below and paste it into any LLM.

---

```text
You are a senior backend architect and Python expert who has built and scaled
multiple production FastAPI applications.

Your task is to generate a COMPLETE, PRODUCTION-READY FastAPI boilerplate
using Beanie (MongoDB ODM) as the backend database layer.

====================
TECH STACK
====================
- Python >= 3.11
- FastAPI (latest stable)
- Beanie ODM (async, Motor-based)
- MongoDB
- Pydantic v2
- Uvicorn / Gunicorn
- JWT authentication
- Async-first architecture

====================
CORE REQUIREMENTS
====================

1) MODERN CODING PRACTICES
- Fully async codebase
- Type hints everywhere (strict typing)
- Pydantic v2 models only
- Dependency Injection using FastAPI Depends
- Environment-based configuration (12-factor app)
- Clear separation of concerns
- No anti-patterns or shortcuts
- Explicit error handling (no silent failures)

2) PRODUCTION-GRADE PROJECT STRUCTURE
Use a scalable, domain-driven folder structure similar to:

app/
├── main.py
├── core/
│   ├── config.py
│   ├── security.py
│   ├── logging.py
│   ├── events.py
│   └── dependencies.py
├── api/
│   ├── v1/
│   │   ├── api.py
│   │   ├── endpoints/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── health.py
├── models/
│   ├── user.py
│   └── base.py
├── schemas/
│   ├── user.py
│   └── token.py
├── services/
│   ├── auth_service.py
│   └── user_service.py
├── repositories/
│   └── user_repository.py
├── db/
│   ├── mongo.py
│   └── init_db.py
├── exceptions/
│   ├── base.py
│   └── auth.py
├── utils/
│   ├── time.py
│   └── uuid.py
└── tests/

Include explanation of WHY this structure is used.

3) JWT AUTHENTICATION (PRODUCTION LEVEL)
- Access & refresh tokens
- Secure password hashing (bcrypt / argon2)
- Token expiration & rotation
- Role-based access control (RBAC)
- Proper HTTP status codes
- Secure dependency-based auth guards
- Configurable token expiry via env vars

4) LOGGING (ENTERPRISE LEVEL)
- Structured logging (JSON format)
- Correlation/request IDs
- Log levels via environment
- Separate app & access logs
- Logging middleware
- No print statements

5) LINTING, FORMATTING & QUALITY GATES
Provide config files and explain them:
- ruff (linting)
- black (formatting)
- mypy (static typing)
- pre-commit hooks
- .editorconfig

Rules:
- Strict linting enabled
- Fail CI on violations
- Type checking enforced

6) SECURITY BEST PRACTICES
- CORS configuration
- Trusted host middleware
- Rate limiting (optional but preferred)
- Secure headers
- Secret management via environment variables
- No hardcoded secrets
- Proper exception handling (no info leaks)

7) DATABASE SETUP
- Async MongoDB connection using Motor
- Beanie document models
- Indexes defined in models
- Startup/shutdown events
- Pagination-ready queries

8) CONFIGURATION MANAGEMENT
- Pydantic BaseSettings
- Separate configs for dev / staging / prod
- .env example file
- Validation for missing env vars

9) DEVOPS & RUNNING IN PROD
- Gunicorn + Uvicorn workers
- Dockerfile (multi-stage)
- docker-compose.yml (MongoDB + API)
- Health check endpoint
- Readiness/liveness probes

10) TESTING FOUNDATION
- pytest setup
- async test support
- dependency overrides
- example test case

====================
OUTPUT FORMAT
====================
- Show full folder structure
- Provide all critical files with code
- Explain important design decisions
- Use best practices ONLY (no shortcuts)
- Treat this as a real production codebase
- Assume this project will be deployed at scale

DO NOT:
- Skip files
- Use outdated patterns
- Write pseudo-code
- Over-simplify logic

DELIVER A FULL PRODUCTION BOILERPLATE.
