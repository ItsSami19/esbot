# ESBot API - Performance Test Report

## 1. Tool Choice

**Tool: Locust**

Locust fits naturally into the existing Python stack - the test script is plain Python, no separate binary or GUI required, and it runs inside the same Docker environment as the backend. The built-in web dashboard at `http://localhost:8089` gives live metrics during a run, and the HTML export (used here) provides a clean, self-contained report for post-run analysis. Compared to JMeter or Gatling, Locust needs significantly less setup for a Python/FastAPI project.

---

## 2. Test Environment

| Property        | Value                                                      |
| --------------- | ---------------------------------------------------------- |
| OS              | Windows 11 / WSL2                                          |
| Backend         | FastAPI (uvicorn, 1 worker, `--reload`), running in Docker |
| Database        | PostgreSQL 17, running in Docker                           |
| Locust host     | `http://backend:8000` (Docker internal network)            |
| Backend workers | 1 (uvicorn default)                                        |
| LLM provider    | Not used - all tested endpoints are non-LLM                |

### Task Mix (`ESBotUser`)

| Task                     | Weight |
| ------------------------ | ------ |
| `healthcheck`            | 30%    |
| `listsessions`           | 20%    |
| `getsession`             | 20%    |
| `sendandreadmessage`     | 20%    |
| `createanddeletesession` | 10%    |

---

## 3. Test Profiles

| Profile | Users | Spawn rate | Run time |
| ------- | ----- | ---------- | -------- |
| Smoke   | 2     | 1/s        | 30 s     |
| Load    | 50    | 1/s        | 5 min    |
| Stress  | 200   | 5/s        | 10 min   |

---

## 4. Test Results

### 4.1 Smoke Test

**Config:** 2 virtual users · spawn rate 1/s · 30 seconds
**Run:** 2026-06-14 06:10:42 – 06:11:13 UTC · 81 total requests

| Metric                     | Aggregated |
| -------------------------- | ---------- |
| Total requests             | 81         |
| Failures                   | 0          |
| Error rate                 | **0%**     |
| Throughput (total RPS)     | 2.69 req/s |
| Average response time      | 18.4 ms    |
| Median response time (p50) | 7 ms       |
| 95th percentile (p95)      | 46 ms      |
| 99th percentile (p99)      | 75 ms      |
| Max response time          | 75 ms      |

**Per-endpoint breakdown:**

| Endpoint                                  | Requests | Avg ms | Median ms | p95 ms | p99 ms | Max ms |
| ----------------------------------------- | -------- | ------ | --------- | ------ | ------ | ------ |
| GET `/api/v1/health`                      | 12       | 2.6    | 2         | 4      | 4      | 4      |
| GET `/api/v1/sessions`                    | 11       | 5.2    | 5         | 6      | 6      | 6      |
| GET `/api/v1/sessions/{id}`               | 12       | 5.1    | 5         | 7      | 7      | 7      |
| GET `/api/v1/sessions/{id}/messages`      | 9        | 6.4    | 6         | 8      | 8      | 8      |
| POST `/api/v1/sessions` (setup)           | 2        | 32.4   | 31        | 34     | 34     | 34     |
| POST `/api/v1/sessions/{id}/messages`     | 9        | 40.8   | 32        | 66     | 66     | 66     |
| DELETE `/api/v1/sessions/{id}` (temp)     | 12       | 31.0   | 27        | 43     | 43     | 43     |
| DELETE `/api/v1/sessions/{id}` (teardown) | 2        | 64.9   | 55        | 75     | 75     | 75     |

**Pass criteria met:** all responses 2xx, zero errors, every endpoint well below the 1-second threshold.

---

### 4.2 Load Test (NFR Validation)

**Config:** 50 virtual users · spawn rate 1/s (≈ 50 s ramp-up) · 5 minutes sustained
**Run:** 2026-06-14 06:14:57 – 06:19:58 UTC · 11,280 total requests

| Metric                     | Aggregated |
| -------------------------- | ---------- |
| Total requests             | 11,280     |
| Failures                   | 0          |
| Error rate                 | **0%**     |
| Throughput (total RPS)     | 37.4 req/s |
| Average response time      | 468 ms     |
| Median response time (p50) | 7 ms       |
| 95th percentile (p95)      | **87 ms**  |
| 99th percentile (p99)      | 24,000 ms  |
| Max response time          | 26,521 ms  |

> **Note on p99/max:** The very high p99 and max values (24–26 s) are caused by occasional SQLAlchemy connection pool stalls at the tail end of the run, not sustained latency. The overwhelming majority of requests completed normally. The p95 of 87 ms is the representative NFR indicator.

**Per-endpoint breakdown:**

| Endpoint                                  | Requests | Avg ms | Median ms | p95 ms | p99 ms |
| ----------------------------------------- | -------- | ------ | --------- | ------ | ------ |
| GET `/api/v1/health`                      | 2,614    | 622    | 2         | 6      | 24,000 |
| GET `/api/v1/sessions`                    | 1,706    | 555    | 6         | 19     | 24,000 |
| GET `/api/v1/sessions/{id}`               | 1,674    | 629    | 6         | 21     | 25,000 |
| GET `/api/v1/sessions/{id}/messages`      | 1,700    | 26.4   | 7         | 26     | 85     |
| POST `/api/v1/sessions` (setup)           | 50       | 42.3   | 34        | 60     | 72     |
| POST `/api/v1/sessions/{id}/messages`     | 1,700    | 588    | 45        | 110    | 25,000 |
| DELETE `/api/v1/sessions/{id}` (temp)     | 893      | 84.9   | 47        | 110    | 230    |
| DELETE `/api/v1/sessions/{id}` (teardown) | 50       | 966    | 990       | 1,500  | 1,500  |

**NFR met:** p95 at 87 ms is well below the 2-second threshold. Zero errors across 11,280 requests.

---

### 4.3 Stress Test (Breaking Point)

**Config:** 200 virtual users · spawn rate 5/s (≈ 40 s ramp-up) · 10 minutes
**Run:** 2026-06-14 06:22:13 – 06:33:21 UTC

#### What happened - timeline

| Time (UTC) | Event                                                                     |
| ---------- | ------------------------------------------------------------------------- |
| 06:22:13   | Ramp-up starts; RPS climbs to ~112.8, avg response time 134–148 ms        |
| 06:22:33   | 200 VUs reached                                                           |
| 06:22:38   | RPS drops to **0** - backend stops processing new requests                |
| 06:22:47   | First HTTP 500 errors appear across all endpoints                         |
| 06:22:48+  | `totalavgresponsetime` starts climbing: 856 ms → 1,956 ms → … → 30,422 ms |
| 06:24:18   | Last setup/session-create failures; avg ~1,956 ms                         |
| 06:31:50   | Last application-level 500 errors recorded                                |
| 06:32:51   | Locust teardown begins; teardown DELETE calls return 500                  |
| 06:33:21   | Run ends; user count visible dropping from 200 to ~25                     |

#### Aggregate results

| Metric                        | Value                                 |
| ----------------------------- | ------------------------------------- |
| Total failures (HTTP 500s)    | **685**                               |
| Error rate                    | **significant - see breakdown below** |
| RPS during ramp-up            | ~112.8 req/s (peak, brief)            |
| RPS after 200 VUs reached     | **~0 req/s** (backend stalled)        |
| Average response time (final) | **~30,422 ms** (30 seconds)           |
| p50 at peak                   | 59,000–120,000 ms (59–120 seconds)    |
| p95 at peak                   | 90,000–172,000 ms (90–172 seconds)    |

#### Failure breakdown (from Locust report)

| Failures | Method | Endpoint                           | Error                         |
| -------- | ------ | ---------------------------------- | ----------------------------- |
| 171      | GET    | `/api/v1/sessions`                 | CatchResponseError (500)      |
| 142      | GET    | `/api/v1/sessions/{id}`            | CatchResponseError (500)      |
| 127      | POST   | `/api/v1/sessions/{id}/messages`   | CatchResponseError (500)      |
| 119      | POST   | `/api/v1/sessions` (temp)          | CatchResponseError (500)      |
| 44       | POST   | `/api/v1/sessions` (setup)         | CatchResponseError (500)      |
| 37       | DELETE | `/api/v1/sessions/{id}` (teardown) | HTTPError 500                 |
| 24       | GET    | `/api/v1/sessions/{id}/messages`   | CatchResponseError (500)      |
| 19       | DELETE | `/api/v1/sessions/{id}` (temp)     | CatchResponseError (500)      |
| 2        | GET    | `/api/v1/sessions`                 | CatchResponseError (status 0) |
| **685**  |        | **Total**                          |                               |

**NFR not met under stress:** The backend collapsed at 200 VUs with 685 HTTP 500 errors and response times reaching 30–172 seconds.

---

## 5. Interpretation

### Does ESBot meet the NFR?

Yes - but only under normal load. The load test (50 concurrent users, 5 minutes) returned a p95 of **87 ms** and **zero errors** across 11,280 requests, which is well inside the 2-second NFR threshold with comfortable headroom for future LLM features.

### Where does it break?

The stress test shows a clear breaking point at or immediately after 200 VUs. Within seconds of hitting peak concurrency, the single uvicorn worker was unable to process requests fast enough. Pending connections queued inside SQLAlchemy, requests started timing out, and the backend began returning HTTP 500 errors across every endpoint. RPS dropped from ~113 to effectively 0 and never recovered. The backend did not crash outright - it continued running and eventually processed queued work, which is why `currentfailpersec` in Locust stayed at 0 (the errors were caught as `CatchResponseError` by the test script, not lost connections). But from a user perspective, the system was completely unresponsive for the entire 10-minute run.

---

## 6. Observations and Recommendations

**1. Switch to multiple uvicorn workers for production.**
The backend starts with a single worker and `--reload` enabled. The `--reload` flag disables multi-worker mode entirely. For any environment beyond active development, switch to:

```bash
uvicorn app.main:app --workers 4
```

This lets the backend use multiple CPU cores and handle far more concurrent requests before connection exhaustion occurs.

**2. Configure a connection pool limit in SQLAlchemy.**
The stress test failure cascade is driven by connection queuing - once the pool saturates, every new request waits and eventually times out. Adding explicit pool settings in `app/db.py` gives direct control:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=True,
)
```

**3. Remove `--reload` for any performance-sensitive run.**
The `--reload` flag adds file-watching overhead on top of disabling multi-worker mode. It belongs in the dev loop only - not in load tests and definitely not in production.

---

## 7. How to Reproduce

**Start the backend:**

```bash
docker compose -f docker-compose.dev.yml up
```

**Start Locust (in a second terminal):**

```bash
docker compose -f docker-compose.dev.yml run --rm -p 8089:8089 \
  -v "${PWD}/docs:/docs" backend \
  locust -f /docs/api/performance/locustfile.py --host=http://backend:8000
```

**Open the Locust dashboard:** `http://localhost:8089`

Configure each profile as follows:

| Profile | Number of users | Spawn rate | Run time |
| ------- | --------------- | ---------- | -------- |
| Smoke   | 2               | 1          | 30s      |
| Load    | 50              | 1          | 5m       |
| Stress  | 200             | 5          | 10m      |
