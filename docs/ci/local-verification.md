# Local Verification

All commands we run locally before pushing - CI mirrors these exact steps.

---

## Prerequisites

All commands run inside the Docker backend container. Start the dev environment first:

```bash
docker compose -f docker-compose.dev.yml up --build
```

---

## Running Tests

### Unit tests and smoke tests (pytest)

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest
```

### BDD acceptance tests (behave)

```bash
docker compose -f docker-compose.dev.yml run --rm backend behave
```

### Full test suite

```bash
docker compose -f docker-compose.dev.yml run --rm backend sh -c "PYTHONPATH=. pytest && PYTHONPATH=. behave"
```

---

## Static Analysis

### pylint

```bash
docker compose -f docker-compose.dev.yml run --rm backend pylint --rcfile=.pylintrc app
```

Config: `backend/.pylintrc`

### mypy

```bash
docker compose -f docker-compose.dev.yml run --rm backend mypy --config-file mypy.ini app
```

Config: `backend/mypy.ini`

---

## Environment Variables

The tests require **no running PostgreSQL instance** and **no live LLM**. pytest and behave use
SQLite in-memory and replace all AI calls with fakes and stubs. The `.env` file is only
needed for the running stack, not for the tests themselves.

| Variable                                              | Purpose                                                        |
| ----------------------------------------------------- | -------------------------------------------------------------- |
| `DATABASE_URL`                                        | PostgreSQL connection string for the running backend container |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | PostgreSQL configuration                                       |
| `NEXT_PUBLIC_API_BASE_URL`                            | Frontend → backend communication                               |

---
