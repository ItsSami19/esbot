# Manual API Testing - Summary

**Tool used:** Bruno (v2.x, Desktop App)  
**Backend:** FastAPI running locally at `http://localhost:8000`  
**Date:** June 2026

---

## Happy Path Workflow

The full happy-path workflow was executed in Bruno against the locally running backend. All seven steps completed without issues:

| #   | Request                                           | Expected         | Actual           |
| --- | ------------------------------------------------- | ---------------- | ---------------- |
| 1   | `GET /api/v1/health`                              | `200 OK`         | `200 OK`         |
| 2   | `POST /api/v1/sessions`                           | `201 Created`    | `201 Created`    |
| 3   | `GET /api/v1/sessions?user_identifier=student-42` | `200 OK`         | `200 OK`         |
| 4   | `GET /api/v1/sessions/{session_id}`               | `200 OK`         | `200 OK`         |
| 5   | `POST /api/v1/sessions/{session_id}/messages`     | `201 Created`    | `201 Created`    |
| 6   | `GET /api/v1/sessions/{session_id}/messages`      | `200 OK`         | `200 OK`         |
| 7   | `DELETE /api/v1/sessions/{session_id}`            | `204 No Content` | `204 No Content` |

All status codes matched expectations. The session created in step 2 was immediately visible in the listing in step 3. The message sent in step 5 appeared correctly in the history in step 6, with the right `order` value (`1`) and `sender` field set to `"user"`. The delete in step 7 returned an empty body, as expected for a `204` response.

---

## Error Scenarios

Two error scenarios were tested to verify that the API handles invalid input gracefully.

### Scenario 1 - Session Not Found

**Request:** `GET /api/v1/sessions/9999`  
**Expected:** `404 Not Found`  
**Actual:** `404 Not Found`

```json
{
  "detail": "Session not found"
}
```

The error message is clear and directly useful — it tells the client exactly what went wrong without exposing any internal details.

### Scenario 2 - Empty Title on Session Create

**Request:** `POST /api/v1/sessions` with `"title": ""`  
**Expected:** `422 Unprocessable Entity`  
**Actual:** `422 Unprocessable Entity`

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

FastAPI's automatic validation catches the empty string and returns a detailed error pointing directly to the offending field (`body → title`). This is very helpful for debugging on the client side.

---

## Observations

Everything behaved as expected throughout the workflow. The status codes were correct across all requests, and the response bodies contained all the fields documented in the API reference. The `422` validation errors from FastAPI are particularly informative — they include the field path, the type of violation, and a human-readable message, which makes it easy to understand what needs to be fixed.

One thing worth noting: the `GET /api/v1/sessions/{session_id}/messages` endpoint returns an empty `messages` array when no messages exist yet rather than a `404`. This is the correct behavior for a list endpoint and makes the client-side handling straightforward.

No unexpected behavior was observed during testing.
