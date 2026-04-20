# ESBot Setup

## Overview

The project uses the following backend-related technologies:

- **FastAPI** for the backend API
- **SQLModel** for database models
- **Next.js** as frontend framework
- **PostgreSQL** as the relational database
- **Alembic** for database migrations
- **pytest** for unit and smoke testing
- **behave** for BDD acceptance testing
- **Docker Compose** for local development setup

---

## Project Structure

```text
esbot/
├─ backend/
│  ├─ app/
│  ├─ tests/
│  ├─ features/
│  │  ├─ steps/
│  │  └─ environment.py
│  ├─ alembic/
│  ├─ requirements.txt
│  ├─ Dockerfile.backend
│  └─ alembic.ini
├─ frontend/
│  ├─ app/
│  ├─ package.json
│  └─ Dockerfile.frontend
├─ .env
└─ docker-compose.dev.yml
```

---

## Prerequisites

Make sure the following tools are installed:

- **Docker Desktop**
- **WSL2** (recommended on Windows)
- **Git**

No local installation of FastAPI, SQLModel, PostgreSQL, Next.js, pytest, or behave is required, because all services run in Docker containers.

---

## Environment Variables

Create a `.env` file in the project root directory.

Example:

```env
# PostgreSQL configuration
POSTGRES_DB=esbot
POSTGRES_USER=esbot_user
POSTGRES_PASSWORD=esbot_password

# pgAdmin configuration
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123

# Backend database connection
DATABASE_URL=postgresql+psycopg://esbot_user:esbot_password@db:5432/esbot

# Frontend configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

## Start the Development Environment

Run the following command from the project root:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This starts:

- PostgreSQL database
- FastAPI backend
- Next.js frontend
- pgAdmin

---

## Service URLs

After startup, the services are available at:

- **Frontend:** `http://localhost:3000`
- **Backend:** `http://localhost:8000`
- **Backend health endpoint:** `http://localhost:8000/health`
- **pgAdmin:** `http://localhost:5056`

---

## pgAdmin Database Connection

To view and manage the database in pgAdmin:

1. Open `http://localhost:5056` in your browser
2. Log in with:
   - Email: `admin@example.com`
   - Password: `admin123`
3. Right-click on "Servers" in the left sidebar and select "Register" > "Server..."
4. In the "General" tab:
   - Name: `esbot-db` (or any name you prefer)
5. In the "Connection" tab:
   - Host name/address: `db`
   - Port: `5432`
   - Username: `esbot_user`
   - Password: `esbot_password`
   - Maintenance database: `esbot`
6. Click "Save"

The database should now appear in the sidebar and you can explore tables, run queries, etc.

---

## Stop the Environment

To stop all containers:

```bash
docker compose -f docker-compose.dev.yml down
```

To stop everything and remove volumes as well:

```bash
docker compose -f docker-compose.dev.yml down -v
```

Use `down -v` if you want to reset the PostgreSQL database completely.

---

## Database Migrations

The project uses **Alembic** for schema migrations.

### Create a new migration

After changing or adding SQLModel entities, create a migration with:

```bash
docker compose -f docker-compose.dev.yml run --rm backend alembic revision --autogenerate -m "describe your change"
```

### Apply migrations manually

```bash
docker compose -f docker-compose.dev.yml run --rm backend alembic upgrade head
```

### Automatic migration on startup

The backend container is configured to run:

```bash
alembic upgrade head
```

before starting the FastAPI server.

This means that after a fresh database reset, all existing migrations are automatically applied when the backend starts.

---

## Running Tests

The backend uses **pytest** for unit and smoke tests and **behave** for BDD acceptance tests.

### Run unit and smoke tests

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest
```

### Run all BDD acceptance tests

```bash
docker compose -f docker-compose.dev.yml run --rm backend behave
```

### Run a single BDD feature file

```bash
docker compose -f docker-compose.dev.yml run --rm backend behave features/resume_learning_session.feature
```

Replace the feature path with another file if needed, for example:

```bash
docker compose -f docker-compose.dev.yml run --rm backend behave features/answer_evaluation.feature
docker compose -f docker-compose.dev.yml run --rm backend behave features/contextualized_response.feature
```

### Run the full backend test suite

To execute both the unit tests from Exercise 4 and the BDD acceptance tests from Exercise 5, run:

```bash
docker compose -f docker-compose.dev.yml run --rm backend sh -c "pytest && behave"
```

This command first runs the **pytest** test suite and then executes all **behave** feature tests.

---

## Smoke Test

A simple smoke test is included to verify that the backend application starts correctly and that the health endpoint works as expected.

The smoke test is implemented as a **pytest test** in the backend test suite.  
It checks whether the FastAPI app responds successfully to:

- `GET /health`

Expected response:

```json
{
  "status": "ok"
}
```

To run the smoke test and all other unit tests, use:

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest
```

To run only the smoke test file, use:

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest tests/test_smoke.py
```

To run one specific test function, use:

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest tests/test_smoke.py::test_health_endpoint
```

As an additional manual check, you can also open the backend health endpoint in the browser after starting the containers:
`http://localhost:8000/health`

---

## Development Notes

- Backend code changes are visible immediately because the backend source is mounted into the Docker container.
- Frontend code changes are also visible immediately because the frontend source is mounted into the frontend container.
- PostgreSQL data is stored in a Docker volume, so it persists unless the volume is removed manually.

---

## Troubleshooting

### Backend does not start

Check the backend logs:

```bash
docker compose -f docker-compose.dev.yml logs backend
```

### Database issues

If the database state is corrupted or outdated, reset the containers and volumes:

```bash
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up --build
```

### Migration issues

Make sure all models are imported in `app/models/__init__.py`, otherwise Alembic may not detect them.

### BDD step issues

If `behave` reports missing, undefined, or ambiguous steps, make sure that:

- the feature files are located in `backend/features/`
- the step definition files are located in `backend/features/steps/`
- all step texts in the feature files have matching step definitions

---
