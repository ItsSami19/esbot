import pytest
from fastapi.testclient import TestClient


# Happy Path

class TestHappyPath:

    def test_health_check_returns_200_and_status_ok(self, client: TestClient):
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_create_session_returns_201_and_valid_body(self, client: TestClient):
        response = client.post(
            "/api/v1/sessions",
            json={"title": "Python Basics", "user_identifier": "student-42"},
        )

        assert response.status_code == 201
        body = response.json()
        assert isinstance(body["id"], int)
        assert body["title"] == "Python Basics"
        assert body["user_identifier"] == "student-42"
        assert body["status"] == "active"
        assert "created_at" in body
        assert "last_activity_at" in body

    def test_list_sessions_returns_200_and_includes_created_session(
        self, client: TestClient, created_session: dict
    ):
        response = client.get(
            "/api/v1/sessions",
            params={"user_identifier": created_session["user_identifier"]},
        )

        assert response.status_code == 200
        session_ids = [s["id"] for s in response.json()]
        assert created_session["id"] in session_ids

    def test_get_session_returns_200_and_correct_metadata(
        self, client: TestClient, created_session: dict
    ):
        response = client.get(f"/api/v1/sessions/{created_session['id']}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == created_session["id"]
        assert body["title"] == created_session["title"]

    def test_send_message_returns_201_and_valid_body(
        self, client: TestClient, created_session: dict
    ):
        response = client.post(
            f"/api/v1/sessions/{created_session['id']}/messages",
            json={"sender": "user", "content": "What is a decorator?"},
        )

        assert response.status_code == 201
        body = response.json()
        assert isinstance(body["id"], int)
        assert body["session_id"] == created_session["id"]
        assert body["sender"] == "user"
        assert body["content"] == "What is a decorator?"
        assert body["order"] == 1

    def test_get_message_history_returns_200_and_contains_sent_message(
        self, client: TestClient, created_session: dict
    ):
        client.post(
            f"/api/v1/sessions/{created_session['id']}/messages",
            json={"sender": "user", "content": "What is a decorator?"},
        )

        response = client.get(
            f"/api/v1/sessions/{created_session['id']}/messages"
        )

        assert response.status_code == 200
        messages = response.json()["messages"]
        assert len(messages) == 1
        assert messages[0]["content"] == "What is a decorator?"

    def test_delete_session_returns_204_and_session_is_gone(
        self, client: TestClient, created_session: dict
    ):
        delete_response = client.delete(
            f"/api/v1/sessions/{created_session['id']}"
        )
        assert delete_response.status_code == 204

        get_response = client.get(
            f"/api/v1/sessions/{created_session['id']}"
        )
        assert get_response.status_code == 404


# Negative / Edge Cases

class TestNegativeCases:

    def test_get_nonexistent_session_returns_404(self, client: TestClient):
        response = client.get("/api/v1/sessions/99999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Session not found"

    def test_create_session_with_empty_title_returns_422(
        self, client: TestClient
    ):
        response = client.post(
            "/api/v1/sessions",
            json={"title": "", "user_identifier": "student-42"},
        )

        assert response.status_code == 422

    def test_create_session_with_missing_user_identifier_returns_422(
        self, client: TestClient
    ):
        response = client.post(
            "/api/v1/sessions",
            json={"title": "Some Session"},
        )

        assert response.status_code == 422

    def test_send_message_with_empty_content_returns_422(
        self, client: TestClient, created_session: dict
    ):
        response = client.post(
            f"/api/v1/sessions/{created_session['id']}/messages",
            json={"sender": "user", "content": ""},
        )

        assert response.status_code == 422

    def test_send_message_with_content_exceeding_max_length_returns_422(
        self, client: TestClient, created_session: dict
    ):
        response = client.post(
            f"/api/v1/sessions/{created_session['id']}/messages",
            json={"sender": "user", "content": "x" * 2001},
        )

        assert response.status_code == 422

    def test_send_message_to_nonexistent_session_returns_404(
        self, client: TestClient
    ):
        response = client.post(
            "/api/v1/sessions/99999/messages",
            json={"sender": "user", "content": "Hello"},
        )

        assert response.status_code == 404
        assert response.json()["detail"] == "Session not found"

    def test_get_message_history_before_any_message_returns_empty_list(
        self, client: TestClient, created_session: dict
    ):
        response = client.get(
            f"/api/v1/sessions/{created_session['id']}/messages"
        )

        assert response.status_code == 200
        assert response.json()["messages"] == []

    def test_delete_nonexistent_session_returns_404(self, client: TestClient):
        response = client.delete("/api/v1/sessions/99999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Session not found"