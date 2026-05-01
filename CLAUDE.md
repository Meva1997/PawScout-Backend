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

`DATABASE_URL` and `AUTH_SECRET_KEY` are required at startup — the app will raise `ValueError` if missing.

## Architecture

### Module Layout

The real app entry point is `app/main.py`. The root `main.py` is a shim that re-exports `app.main:app` for tooling compatibility.

```
app/
├── main.py              # FastAPI instance, CORS, router registration, startup hook
├── database.py          # SQLAlchemy engine, Session dependency, table creation
├── auth.py              # Argon2 password hashing, JWT creation
├── dependencies.py      # Auth middleware: get_current_user, get_current_admin_user, CurrentUser/AdminUser type aliases
├── cloudinary_config.py # upload_media / delete_media async helpers
├── models/
│   └── settings.py      # ShelterSettings table model + ShelterSettingsUpdate Pydantic schema
├── routers/             # Domain routers — each file owns its SQLModel table definition
│   ├── animals.py       # Animal model + CRUD (public reads, admin writes)
│   ├── adopt.py         # AdoptionApplication model + submission workflow
│   ├── volunteer.py     # Volunteer model + CRUD
│   ├── contact.py       # ContactMessage model + CRUD
│   ├── users.py         # PawUser model + register/login/me
│   └── subs.py          # Subscription model + newsletter endpoints
├── cloudinary/
│   └── routers/
│       └── media.py     # /media/upload, /media/upload-multiple, /media/delete
└── internal/
    └── admin.py         # /admin/* endpoints (dashboard, user management, settings, logo)
```

### Key Architectural Patterns

**SQLModel table definitions live in router files.** `Animal` is defined in `routers/animals.py`, `PawUser` in `routers/users.py`, etc. `database.py` imports all of them inside `create_db_and_tables()` to avoid circular imports, then calls `SQLModel.metadata.create_all(engine)`. There are no migration scripts — schema is created on startup.

**Dependency injection via type aliases.** `dependencies.py` exports `CurrentUser` and `AdminUser` as `Annotated` type aliases wrapping FastAPI `Depends()`. Routes declare these as parameters to get the authenticated user and automatically enforce permissions:
```python
async def create_animal(animal: Animal, session: SessionDep, admin: AdminUser):
    # admin is guaranteed to be an authenticated admin here
```

**Animal status is tightly coupled to adoption applications.** When a `POST /adopt/{animal_id}` is submitted, the animal's `availableForAdoption` flips to `pending`. When an admin updates an application's status via `PUT /adopt/{application_id}/status`, the animal status syncs accordingly: `approved` → `adopted`, `rejected` → `available`. Deleting a pending/rejected application also resets the animal to `available`.

**Cloudinary media flow.** Animal media is stored as a JSON array on the `Animal` model (`sa_column=Column(JSON)`). The expected workflow is: upload files first via `POST /media/upload-multiple` → get back `{url, public_id, ...}` objects → include that array in the `POST /animals/` body. Media deletion from Cloudinary is separate from animal deletion and must be done explicitly via `DELETE /media/delete`.

**Circular import handling.** `dependencies.py` imports `PawUser` inside function bodies (not at module level) to avoid the circular dependency between `dependencies.py` and `routers/users.py`.

**CORS.** Allowed origins are `localhost:3000`, `localhost:5173`, and optionally `FRONTEND_URL` from the environment. Credentials are allowed. Add new allowed origins in `app/main.py`.

### Authentication Flow

1. `POST /users/login` → verifies Argon2 hash → returns JWT with payload `{sub: email, user_id, isAdmin, name, lastName}`
2. JWT is decoded in `get_current_user()` (in `dependencies.py`) — it looks up the user by `user_id` from the token, not by email query
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
