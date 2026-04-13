# Backend Unit Tests

This folder contains the backend unit tests for the ESBot domain and application logic.

## Run unit tests with Docker

From the repository root, execute:

```powershell
docker compose -f .\docker-compose.dev.yml run --rm backend pytest tests/unit_tests
```

This starts the backend container once, runs only the unit tests under `tests/unit_tests`, and then removes the container.

## Alternative local run

If you have Python and dependencies installed locally, you can run the same tests from the backend folder:

```powershell
cd backend
python -m pytest tests/unit_tests
```

## Notes

- These tests run without requiring a database service or external AI services.
- If you want to run all backend tests instead of only unit tests, remove the path filter:

```powershell
docker compose -f .\docker-compose.dev.yml run --rm backend pytest
```
