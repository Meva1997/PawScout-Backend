# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PawScout Backend is a FastAPI REST API for an animal adoption platform. It uses Python 3.11.9, SQLModel (SQLAlchemy + Pydantic), PostgreSQL, JWT authentication with Argon2 hashing, and Cloudinary for media storage. Deployed on Render with Gunicorn + Uvicorn workers.

## Commands

**Development server (with hot reload):**
```bash
uvicorn app.main:app --reload --port 8000
# or
fastapi dev app/main.py
```

**Production startup:**
```bash
bash start.sh
# Runs: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Interactive API docs (after starting server):**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

There is no test suite currently. API testing is done via Swagger UI or curl.

## Required Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/pawscout
AUTH_SECRET_KEY=<generate with: openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=20160
CLOUD_NAME=<cloudinary cloud name>
API_KEY=<cloudinary api key>
API_SECRET=<cloudinary api secret>
FRONTEND_URL=https://your-frontend.vercel.app  # optional, for CORS
```

`DATABASE_URL`, `AUTH_SECRET_KEY`, `CLOUD_NAME`, `API_KEY`, and `API_SECRET` are required at startup — `app/config.py` will raise `pydantic.ValidationError` if any are missing.

## Database Migrations (Alembic)

Schema is managed by Alembic, not by `SQLModel.metadata.create_all()`. The production `start.sh` runs `alembic upgrade head` before launching Gunicorn.

**Apply migrations to the current database:**
```bash
alembic upgrade head
```

**Generate a new migration after editing models in `app/models/`:**
```bash
alembic revision --autogenerate -m "describe the change"
# review the generated file in alembic/versions/ before committing
alembic upgrade head
```

`alembic/env.py` reads `DATABASE_URL` from `app.config.settings` and uses `SQLModel.metadata` (populated by importing `app.models`) as the autogenerate target.

## Architecture

### Module Layout

The real app entry point is `app/main.py`. The root `main.py` is a shim that re-exports `app.main:app` for tooling compatibility.

```
app/
├── main.py              # FastAPI instance, CORS, router registration
├── config.py            # Settings (pydantic-settings) — single source of env vars
├── database.py          # SQLAlchemy engine, get_session, SessionDep
├── core/
│   ├── security.py      # Argon2 password hashing, JWT creation
│   ├── deps.py          # Auth middleware: get_current_user, get_current_admin_user, CurrentUser/AdminUser
│   └── cloudinary.py    # upload_media / delete_media async helpers
├── models/              # SQLModel table definitions (one file per entity)
│   ├── __init__.py      # re-exports all tables for `from app.models import ...`
│   ├── user.py          # PawUser
│   ├── animal.py        # Animal + AnimalStatus enum
│   ├── adoption.py      # AdoptionApplication + AdoptionStatus enum
│   ├── volunteer.py     # Volunteer + VolunteerStatus enum
│   ├── contact.py       # ContactMessage
│   ├── subscription.py  # Subscription
│   └── settings.py      # ShelterSettings
├── schemas/             # Pydantic request/response schemas (non-table)
│   ├── user.py          # LoginRequest
│   ├── settings.py      # ShelterSettingsUpdate
│   └── media.py         # MediaUploadResponse, MediaDeleteRequest
└── routers/             # Domain routers — endpoints only, no model definitions
    ├── animals.py       # Animal CRUD (public reads, admin writes)
    ├── adopt.py         # Adoption submission workflow
    ├── volunteer.py     # Volunteer CRUD
    ├── contact.py       # Contact form messages
    ├── users.py         # /users/register, /users/login, /users/me
    ├── subs.py          # Newsletter subscriptions
    ├── media.py         # /media/upload, /media/upload-multiple, /media/delete
    └── admin.py         # /admin/* (dashboard, user management, settings, logo)

alembic/                 # Migration history (versioned schema)
├── env.py               # configures target_metadata = SQLModel.metadata
└── versions/            # one file per migration
```

### Key Architectural Patterns

**Tables live in `app/models/`, not in routers.** Each table is in its own file and re-exported from `app/models/__init__.py`. Routers import tables via `from app.models import Animal`. Adding a new table: create the file in `app/models/`, add it to `__init__.py`, run `alembic revision --autogenerate -m "..."`.

**Dependency injection via type aliases.** `app/core/deps.py` exports `CurrentUser` and `AdminUser` as `Annotated` type aliases wrapping FastAPI `Depends()`. Routes declare these as parameters to get the authenticated user and automatically enforce permissions:
```python
async def create_animal(animal: Animal, session: SessionDep, admin: AdminUser):
    # admin is guaranteed to be an authenticated admin here
```

**Centralized configuration.** `app/config.py` defines a `Settings` class (pydantic-settings) loaded from `.env` at import time. Other modules import `from app.config import settings` instead of calling `os.getenv()` directly.

**Animal status is tightly coupled to adoption applications.** When a `POST /adopt/{animal_id}` is submitted, the animal's `availableForAdoption` flips to `pending`. When an admin updates an application's status via `PUT /adopt/{application_id}/status`, the animal status syncs accordingly: `approved` → `adopted`, `rejected` → `available`. Deleting a pending/rejected application also resets the animal to `available`.

**Cloudinary media flow.** Animal media is stored as a JSON array on the `Animal` model (`sa_column=Column(JSON)`). The expected workflow is: upload files first via `POST /media/upload-multiple` → get back `{url, public_id, ...}` objects → include that array in the `POST /animals/` body. Media deletion from Cloudinary is separate from animal deletion and must be done explicitly via `DELETE /media/delete`.

**CORS.** Allowed origins are `localhost:3000`, `localhost:5173`, and optionally `settings.FRONTEND_URL`. Credentials are allowed. Add new allowed origins in `app/main.py`.

### Authentication Flow

1. `POST /users/login` → verifies Argon2 hash → returns JWT with payload `{sub: email, user_id, isAdmin, name, lastName}`
2. JWT is decoded in `get_current_user()` (in `app/core/deps.py`) — it looks up the user by `user_id` from the token, not by email query
3. `get_current_admin_user()` chains from `get_current_user` and raises 403 if `isAdmin` is false
4. First admin must be created by manually setting `isAdmin = true` in the database, then subsequent admins can be promoted via `PATCH /admin/users/{id}/promote`

### Creating the First Admin

```bash
# 1. Register a user
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "name": "Admin", "lastName": "User", "password": "password123"}'

# 2. Promote via psql
psql $DATABASE_URL -c "UPDATE pawuser SET \"isAdmin\" = true WHERE email = 'admin@example.com';"
```

### Response Conventions

- Success responses use `{"success": "..."}` for mutations and named keys for lists (e.g., `{"animals": [...]}`, `{"requests": [...]}`)
- Error responses use `{"detail": "..."}` (FastAPI standard)
- Some messages in `admin.py` settings endpoints are in Spanish — this is intentional

## PostgreSQL-Specific Details

- `Volunteer.availability`, `Volunteer.availableDays`, `Volunteer.areasOfInterest` use PostgreSQL `ARRAY` type via `sa_column=Column(ARRAY(String))`
- `Animal.media` uses PostgreSQL `JSON` type via `sa_column=Column(JSON)` to store an array of media objects
- The database engine runs with `echo=True` — all SQL queries are logged to stdout in development
