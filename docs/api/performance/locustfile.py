"""
ESBot Performance Test Suite
=============================
Three test profiles in one file:

  Smoke  → 1-2 users, short run, sanity check
  Load   → 50 users, 5-minute sustained run, NFR validation
  Stress → ramp from 50 to 200+ users, breaking-point exploration

Run via Locust web UI (recommended):
  locust -f locustfile.py --host=http://backend:8000

Then open http://localhost:8089 and configure the profile manually.

Profile quick-reference:
  Smoke:  Users=2,  Spawn rate=1,  Run time=30s
  Load:   Users=50, Spawn rate=1,  Run time=5m  (ramp-up ~60s)
  Stress: Users=200,Spawn rate=5,  Run time=10m
"""

import random
import string

from locust import HttpUser, task, between, events


# Helpers

def random_identifier(prefix: str = "user") -> str:
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{prefix}-{suffix}"


# User behaviour – shared across all profiles

class ESBotUser(HttpUser):
    """
    Simulates a single user interacting with the ESBot API.

    Each user:
      1. Creates a session on start (on_start)
      2. Repeatedly calls the tasks weighted by @task(N)
      3. Cleans up the session on stop (on_stop)

    Wait time between requests is kept short (0.5–1.5 s) to generate
    realistic throughput without artificial throttling.
    """

    wait_time = between(0.5, 1.5)

    def on_start(self):
        """Create a dedicated session for this virtual user."""
        self.user_id = random_identifier("perf-user")
        self.session_id = None

        with self.client.post(
            "/api/v1/sessions",
            json={
                "title": f"Perf Session {self.user_id}",
                "user_identifier": self.user_id,
            },
            catch_response=True,
            name="[setup] POST /api/v1/sessions",
        ) as response:
            if response.status_code == 201:
                self.session_id = response.json()["id"]
                response.success()
            else:
                response.failure(
                    f"Session setup failed: {response.status_code}"
                )

    def on_stop(self):
        """Delete the session created in on_start."""
        if self.session_id is not None:
            self.client.delete(
                f"/api/v1/sessions/{self.session_id}",
                name="[teardown] DELETE /api/v1/sessions/{id}",
            )


    # Tasks

    @task(3)
    def health_check(self):
        """Lightweight liveness probe – highest weight, cheapest endpoint."""
        with self.client.get(
            "/api/v1/health",
            catch_response=True,
            name="GET /api/v1/health",
        ) as response:
            if response.status_code == 200 and response.json().get("status") == "ok":
                response.success()
            else:
                response.failure(f"Unexpected health response: {response.text}")

    @task(2)
    def list_sessions(self):
        """List all sessions for the current virtual user."""
        with self.client.get(
            "/api/v1/sessions",
            params={"user_identifier": self.user_id},
            catch_response=True,
            name="GET /api/v1/sessions",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"List sessions failed: {response.status_code}")

    @task(2)
    def get_session(self):
        """Retrieve metadata for the virtual user's own session."""
        if self.session_id is None:
            return

        with self.client.get(
            f"/api/v1/sessions/{self.session_id}",
            catch_response=True,
            name="GET /api/v1/sessions/{id}",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get session failed: {response.status_code}")

    @task(2)
    def send_and_read_message(self):
        """Send a message then immediately retrieve the history."""
        if self.session_id is None:
            return

        with self.client.post(
            f"/api/v1/sessions/{self.session_id}/messages",
            json={"sender": "user", "content": "What is unit testing?"},
            catch_response=True,
            name="POST /api/v1/sessions/{id}/messages",
        ) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Send message failed: {response.status_code}")
                return

        with self.client.get(
            f"/api/v1/sessions/{self.session_id}/messages",
            catch_response=True,
            name="GET /api/v1/sessions/{id}/messages",
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Get history failed: {response.status_code}")

    @task(1)
    def create_and_delete_session(self):
        """Create a throw-away session and immediately delete it."""
        temp_user = random_identifier("temp")
        session_id = None

        with self.client.post(
            "/api/v1/sessions",
            json={"title": "Temp Session", "user_identifier": temp_user},
            catch_response=True,
            name="POST /api/v1/sessions (temp)",
        ) as response:
            if response.status_code == 201:
                session_id = response.json()["id"]
                response.success()
            else:
                response.failure(f"Temp session create failed: {response.status_code}")
                return

        if session_id:
            with self.client.delete(
                f"/api/v1/sessions/{session_id}",
                catch_response=True,
                name="DELETE /api/v1/sessions/{id} (temp)",
            ) as response:
                if response.status_code == 204:
                    response.success()
                else:
                    response.failure(f"Temp session delete failed: {response.status_code}")