# Board API

A course exercise implementing a REST API with FastAPI, PostgreSQL, SQLAlchemy, bcrypt, and JWT authentication.

## Local setup

Requirements: Python 3.13+, uv, and PostgreSQL. Create a dedicated database named `board_api` first. Do not use a shared course database. Startup refuses the default `postgres` and template databases.

1. Run `uv sync --frozen`.
2. Copy `.env.example` to `.env` in the project root.
3. Replace `DATABASE_URL` with your dedicated database connection string.
4. Replace `JWT_SECRET_KEY` with a random secret of at least 64 bytes. For example, generate one locally with `python -c "import secrets; print(secrets.token_hex(64))"`. Keep it private.
5. Run `uv run uvicorn src.main:app --host 127.0.0.1 --port 8000`.
6. Open http://127.0.0.1:8000/docs.

Startup creates missing tables in the configured database. It does not migrate existing tables. Keep `.env`, credentials, private keys, and database dumps out of Git.

## API

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/signup` | Create an account using email and password |
| POST | `/auth/login` | Obtain an access token |
| GET | `/posts` | List posts with offset and limit |
| GET | `/posts/{post_id}` | Read one post |
| POST | `/posts` | Create a post; authentication required |
| PUT | `/posts/{post_id}` | Replace title and content; author only |
| DELETE | `/posts/{post_id}` | Delete a post; author only |

In Swagger, sign up and log in, then enter the returned access token in **Authorize**. Post requests accept `title` and `content`; the server assigns the author from the authenticated user. Tokens expire after 60 minutes. Passwords must contain at least 8 characters and at most 72 UTF-8 bytes.

## Structure

- `src/auth`: authentication routes, JWT, and request dependencies
- `src/user/infrastructure`: user model
- `src/board/presentation`: post routes and request/response schemas
- `src/board/application`: post existence and author checks
- `src/board/infrastructure/sqlalchemy`: post model and repository
- `src/shared/core`: database sessions and model base

Each request commits before a successful response; errors roll back its transaction.

## Deployment status

Public HTTPS endpoint verification is pending. No public endpoint is advertised in this repository yet. EC2 setup and credentials are intentionally not included.
