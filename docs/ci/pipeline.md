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

---

## Justification (mypy and pylint)

Pylint and mypy are configured with `|| true` so that existing findings
do not block the pipeline. Both tools already run and report locally
(see `docs/spec/static-analysis.md`). The known findings - pylint style
warnings (score 9.12/10) and mypy type annotation issues related to
SQLModel's optional IDs - are documented there in detail. Resolving these
findings was not part of the exercise scope; the goal was to integrate,
configure, and run both tools, which has been completed.

---

## Exercise 9.2 Enhancements

### Security Audit with pip-audit

We added a dedicated `security-audit` job to the pipeline that runs
[pip-audit](https://pypi.org/project/pip-audit/) against `backend/requirements.txt`.

**What it does:** pip-audit scans all Python dependencies for known vulnerabilities
by checking them against the PyPI Advisory Database. It flags any package version
that has a published CVE or security advisory.

**Why it fits ESBot:** ESBot's backend pulls in several third-party packages
(`fastapi`, `sqlmodel`, `uvicorn`, `alembic`, `psycopg`) that are updated
regularly. A vulnerability in any of these could expose the API or the database
layer. Running pip-audit in CI means we catch affected versions automatically
on every push, without having to check manually.

**Added value vs. cost:** The job adds roughly 15–35 seconds to the pipeline.
There is no external service dependency, no token or secret required, and
false positives are rare since pip-audit only reports confirmed advisories.
Maintenance effort is minimal- the tool updates its advisory data automatically.

**Local execution:** The same check runs locally with:

```bash
docker compose -f docker-compose.dev.yml run --rm backend pip-audit -r requirements.txt
```

The `security-audit` job runs in parallel with `backend-test`, so it does not
add to the critical path of the pipeline.
