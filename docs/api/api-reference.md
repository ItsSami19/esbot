# ESBot API Reference

All endpoints accept and return JSON.

---

## Base URL

```
http://localhost:8000
```

To run the backend locally you need the following environment variables (defined in the root `.env` file):

| Variable            | Example value                                                  | Purpose                    |
| ------------------- | -------------------------------------------------------------- | -------------------------- |
| `DATABASE_URL`      | `postgresql+psycopg://esbot_user:esbot_password@db:5432/esbot` | Database connection string |
| `POSTGRES_DB`       | `esbot`                                                        | PostgreSQL database name   |
| `POSTGRES_USER`     | `esbot_user`                                                   | PostgreSQL user            |
| `POSTGRES_PASSWORD` | `esbot_password`                                               | PostgreSQL password        |

---

## Setup Instructions

**1. Clone the repository and navigate into it.**

**2. Copy or create the `.env` file** in the project root with the values shown above.

**3. Start all services with Docker Compose:**

```bash
docker compose -f docker-compose.dev.yml up --build
```

This starts PostgreSQL, runs Alembic migrations automatically, and launches the FastAPI backend on port `8000`.

**4. Verify the backend is up:**

```bash
curl http://localhost:8000/api/v1/health
# → {"status": "ok"}
```

That's it - the API is ready.

---

## Endpoints

### Health Check

**`GET /api/v1/health`**

A simple liveness check. Useful to confirm the backend started correctly before running any other requests.

**Request:** No body, no parameters.

**Response `200 OK`:**

```json
{
  "status": "ok"
}
```

---

### Sessions

#### Create a Session

**`POST /api/v1/sessions`**

Creates a new learning session for a user.

**Request body:**

```json
{
  "title": "Python Basics",
  "user_identifier": "student-42"
}
```

| Field             | Type   | Required | Constraints      |
| ----------------- | ------ | -------- | ---------------- |
| `title`           | string | yes      | 1–200 characters |
| `user_identifier` | string | yes      | 1–100 characters |

**Response `201 Created`:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "created_at": "2026-06-14T06:00:00Z",
  "last_activity_at": "2026-06-14T06:00:00Z",
  "status": "active",
  "user_identifier": "student-42"
}
```

---

#### List Sessions

**`GET /api/v1/sessions?user_identifier={user_identifier}`**

Returns all sessions belonging to a specific user, ordered by creation date (oldest first).

**Query parameter:**

| Parameter         | Type   | Required |
| ----------------- | ------ | -------- |
| `user_identifier` | string | yes      |

**Response `200 OK`:**

```json
[
  {
    "id": 1,
    "title": "Python Basics",
    "created_at": "2026-06-14T06:00:00Z",
    "last_activity_at": "2026-06-14T06:00:00Z",
    "status": "active",
    "user_identifier": "student-42"
  }
]
```

Returns an empty array `[]` if no sessions exist for the given user.

---

#### Get Session

**`GET /api/v1/sessions/{session_id}`**

Retrieves the metadata for a single session by its ID.

**Path parameter:**

| Parameter    | Type    | Required |
| ------------ | ------- | -------- |
| `session_id` | integer | yes      |

**Response `200 OK`:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "created_at": "2026-06-14T06:00:00Z",
  "last_activity_at": "2026-06-14T06:00:00Z",
  "status": "active",
  "user_identifier": "student-42"
}
```

---

#### Delete Session

**`DELETE /api/v1/sessions/{session_id}`**

Deletes a session and all its associated messages.

**Path parameter:**

| Parameter    | Type    | Required |
| ------------ | ------- | -------- |
| `session_id` | integer | yes      |

**Response `204 No Content`:** Empty body on success.

---

### Messages

#### Send a Message

**`POST /api/v1/sessions/{session_id}/messages`**

Appends a new message (user or AI) to an existing session.

**Path parameter:**

| Parameter    | Type    | Required |
| ------------ | ------- | -------- |
| `session_id` | integer | yes      |

**Request body:**

```json
{
  "sender": "user",
  "content": "What is a decorator in Python?"
}
```

| Field     | Type                        | Required | Constraints                         |
| --------- | --------------------------- | -------- | ----------------------------------- |
| `sender`  | string (`"user"` or `"ai"`) | yes      | Must be a valid `Sender` enum value |
| `content` | string                      | yes      | 1–2000 characters                   |

**Response `201 Created`:**

```json
{
  "id": 5,
  "session_id": 1,
  "sender": "user",
  "content": "What is a decorator in Python?",
  "created_at": "2026-06-14T06:01:00Z",
  "order": 1
}
```

---

#### Get Message History

**`GET /api/v1/sessions/{session_id}/messages`**

Returns all messages for a session in chronological order (by `order` field).

**Path parameter:**

| Parameter    | Type    | Required |
| ------------ | ------- | -------- |
| `session_id` | integer | yes      |

**Response `200 OK`:**

```json
{
  "messages": [
    {
      "id": 5,
      "session_id": 1,
      "sender": "user",
      "content": "What is a decorator in Python?",
      "created_at": "2026-06-14T06:01:00Z",
      "order": 1
    },
    {
      "id": 6,
      "session_id": 1,
      "sender": "ai",
      "content": "A decorator is a function that wraps another function...",
      "created_at": "2026-06-14T06:01:05Z",
      "order": 2
    }
  ]
}
```

Returns `{"messages": []}` if no messages have been sent yet.

---

## Error Responses

All errors follow the same JSON structure returned by FastAPI:

```json
{
  "detail": "A human-readable description of what went wrong."
}
```

### `404 Not Found`

Returned when a session or resource with the given ID does not exist.

**Example - `GET /api/v1/sessions/9999`:**

```json
{
  "detail": "Session not found"
}
```

### `422 Unprocessable Entity`

Returned when the request body or query parameters fail validation (e.g., a required field is missing, a string is too short/long, or an enum value is invalid). FastAPI generates this automatically.

**Example - `POST /api/v1/sessions` with an empty title:**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": "",
      "ctx": { "min_length": 1 }
    }
  ]
}
```

### `500 Internal Server Error`

Returned when an unexpected error occurs on the server side (e.g., database connection failure).

**Example:**

```json
{
  "detail": "Internal Server Error"
}
```

---

## Notes

- All timestamps are in UTC and follow the ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`).
- `session_id` is always an integer (auto-incremented by the database).
- The `order` field on messages is 1-based and reflects insertion order within a session.
- The `status` field on sessions defaults to `"active"`. Other valid values are `"archived"` and `"deleted"`, though no endpoints currently change the status.
