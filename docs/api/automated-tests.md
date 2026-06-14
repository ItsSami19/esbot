# Automated API Tests

## Framework Choice

The test suite uses **pytest** together with **FastAPI's built-in TestClient** (powered by `httpx`). This combination was chosen because:

- Both `pytest` and `httpx` are already listed in `requirements.txt` - no extra dependencies needed.
- The TestClient runs the full FastAPI app in-process, so no separate server needs to be started before the tests.
- FastAPI's `dependency_overrides` mechanism lets us swap the production PostgreSQL database for an SQLite in-memory database cleanly, without touching any production code.

---

## How to Run

From the project root (where `docker-compose.dev.yml` lives), run:

```bash
docker compose -f docker-compose.dev.yml run --rm backend pytest tests/api/ -v
```

That's it. The suite sets up and tears down the in-memory database automatically for each test.

---

## Backend Configuration for Tests

The API tests do **not** require a running backend or a real database. The `conftest.py` in `tests/api/` does the following:

1. Creates a fresh SQLite in-memory engine with `StaticPool` (single shared connection, required for in-memory SQLite).
2. Overrides the `get_db_session` dependency from `app.api.dependencies` via `app.dependency_overrides` so every request handled by the TestClient uses the test database instead of PostgreSQL.
3. Drops all tables after each test via the `client` fixture's teardown, ensuring full test isolation.

---

## Test Groups

### Happy Path (`TestHappyPath`)

Covers the full end-to-end workflow through the API in logical order:

| Test                                                             | What it verifies                                                          |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `test_health_check_returns_200_and_status_ok`                    | Health endpoint returns `200` and `{"status": "ok"}`                      |
| `test_create_session_returns_201_and_valid_body`                 | Session creation returns `201`, correct fields, and `"active"` status     |
| `test_list_sessions_returns_200_and_includes_created_session`    | Listing sessions includes the freshly created one                         |
| `test_get_session_returns_200_and_correct_metadata`              | Retrieving a session by ID returns the correct metadata                   |
| `test_send_message_returns_201_and_valid_body`                   | Sending a message returns `201`, correct `sender`, `content`, and `order` |
| `test_get_message_history_returns_200_and_contains_sent_message` | Message history contains the previously sent message                      |
| `test_delete_session_returns_204_and_session_is_gone`            | Delete returns `204` and a subsequent GET returns `404`                   |

### Negative / Edge Cases (`TestNegativeCases`)

Covers invalid inputs and boundary conditions:

| Test                                                              | What it verifies                                               |
| ----------------------------------------------------------------- | -------------------------------------------------------------- |
| `test_get_nonexistent_session_returns_404`                        | Unknown session ID → `404` with correct detail message         |
| `test_create_session_with_empty_title_returns_422`                | Empty title → `422` validation error                           |
| `test_create_session_with_missing_user_identifier_returns_422`    | Missing required field → `422` validation error                |
| `test_send_message_with_empty_content_returns_422`                | Empty message content → `422` validation error                 |
| `test_send_message_with_content_exceeding_max_length_returns_422` | Content over 2000 characters → `422` validation error          |
| `test_send_message_to_nonexistent_session_returns_404`            | Message to unknown session → `404` with correct detail message |
| `test_get_message_history_before_any_message_returns_empty_list`  | History before any message → `200` with empty list, not `404`  |
| `test_delete_nonexistent_session_returns_404`                     | Delete unknown session → `404` with correct detail message     |
