# CI Pipeline

Here we document why we built the pipeline the way we did.

## Triggers

```yaml
on:
  push:
  pull_request:
```

We trigger on `push` (every commit on every branch) and `pull_request`. That means
everyone gets immediate feedback, even on feature branches before a PR is opened.
The `pull_request` trigger additionally ensures nothing unverified can land on the
main branch.

We deliberately left out `workflow_dispatch` - for manual re-runs the GitHub UI is
more than enough.

---

## Runner

```yaml
runs-on: ubuntu-latest
```

Our production image is based on `python:3.12-slim` (Linux), so `ubuntu-latest` is
the natural fit. The environment is close to what we run locally inside Docker, and
GitHub-hosted Ubuntu runners are fast and straightforward for our use case.

---

## Environment and Caching

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'
    cache-dependency-path: backend/requirements.txt
```

Python 3.12 matches our `Dockerfile.backend` exactly. The pip caching via
`cache-dependency-path` means packages don't get re-downloaded after the first run,
which makes every subsequent run noticeably faster. The cache is invalidated
automatically whenever `requirements.txt` changes.

---

## Jobs and Steps

The pipeline has a single job: `backend-test`.

| Step         | Command                           | Purpose                                 |
| ------------ | --------------------------------- | --------------------------------------- |
| Checkout     | `actions/checkout@v4`             | Fetch the repository                    |
| Python setup | `actions/setup-python@v5`         | Python 3.12 + pip cache                 |
| Dependencies | `pip install -r requirements.txt` | Install all backend packages            |
| pytest       | `PYTHONPATH=. pytest`             | Unit, repository, mock, and smoke tests |
| behave       | `PYTHONPATH=. behave`             | BDD acceptance tests (all 3 features)   |
| pylint       | `pylint --rcfile=.pylintrc app`   | Linting with our project config         |
| mypy         | `mypy --config-file mypy.ini app` | Static type checking                    |

`PYTHONPATH=.` is necessary because pytest and behave resolve `app.*` imports relative
to the `backend/` working directory. Docker handles this implicitly via `WORKDIR`;
in CI we need to set it explicitly.

### What we deliberately excluded from CI

- **PostgreSQL:** Tests use SQLite in-memory - a `services:` container would be
  slower and more fragile without any added coverage benefit.
- **Live LLM (Ollama/vLLM):** All AI calls are replaced by `FakeAIProvider` and
  `ExplanationAIProviderStub`. Non-deterministic behavior has no place in a CI pipeline.
- **Frontend:** The Next.js frontend has no tests yet. Once that changes, we'll add
  a separate `frontend-test` job.

---

## Parity: Local vs. CI

We make sure local and CI run exactly the same checks:

| Local (Docker)                                                    | CI                                |
| ----------------------------------------------------------------- | --------------------------------- |
| `docker compose run --rm backend pytest`                          | `PYTHONPATH=. pytest`             |
| `docker compose run --rm backend behave`                          | `PYTHONPATH=. behave`             |
| `docker compose run --rm backend pylint --rcfile=.pylintrc app`   | `pylint --rcfile=.pylintrc app`   |
| `docker compose run --rm backend mypy --config-file mypy.ini app` | `mypy --config-file mypy.ini app` |
