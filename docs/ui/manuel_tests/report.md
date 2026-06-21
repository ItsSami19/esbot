# Manual UI Test Report - ESBot Exercise 11.1

## Environment

| Property     | Value                                                     |
| ------------ | --------------------------------------------------------- |
| OS           | Windows 11 (Host) / Docker Desktop                        |
| Browser      | Google Chrome 125+                                        |
| Frontend URL | http://localhost:3000                                     |
| Backend URL  | http://localhost:8000                                     |
| LLM          | Deterministic mock (`generate_ai_reply`) - no real LLM    |
| Date         | 2026-06-21                                                |
| Tester       | ESBot Team                                                |
| Stack        | Next.js 15 (Frontend) · FastAPI (Backend) · PostgreSQL 17 |

---

## TC-UI-01 - Health Check Reachable and UI Renders Without Errors

**Related BDD Feature:** `contextualized_response.feature` (Precondition: system is available)  
**Related Requirement:** FR1, NFR3

**Steps Performed:**

1. Run `docker compose -f docker-compose.dev.yml up --build` from project root
2. Wait for all containers to be healthy (db → backend → frontend)
3. Open `http://localhost:3000` in Chrome
4. Observe the sidebar header area for the health indicator dot
5. Open `http://localhost:8000/api/v1/health` in a new tab

**Expected Result:**

- `http://localhost:3000` renders the ESBot chat UI without console errors
- The health dot (`data-testid="health-status"`) in the sidebar is green
- `http://localhost:8000/api/v1/health` returns `{"status": "ok"}`

**Actual Result:**

- UI rendered correctly, no console errors observed
- Green health dot visible in sidebar
- Health endpoint returned `{"status": "ok"}` with HTTP 200

**Result:** PASS

---

## TC-UI-02 - Create a New Learning Session (UC-001 Precondition)

**Related BDD Feature:** `resume_learning_session.feature`  
**Related Requirement:** FR10, FR12, NFR5

**Steps Performed:**

1. Open `http://localhost:3000`
2. Click the **"New Session"** button in the sidebar (`data-testid="new-session-btn"`)
3. Enter the title `"Testing Basics"` in the input field
4. Press **Enter** to confirm
5. Observe the sidebar session list and the main chat area

**Expected Result:**

- A new session `"Testing Basics"` appears in the sidebar session list (`data-testid="session-list"`)
- The main chat window opens with the session title in the header
- The message list is empty with a prompt to send a message
- Backend returns HTTP 201 for `POST /api/v1/sessions`

**Actual Result:**

- Session `"Testing Basics"` appeared immediately in the sidebar
- Chat window opened with correct title
- Empty state message displayed correctly
- Network tab confirmed HTTP 201 response

**Result:** PASS

---

## TC-UI-03 - Send a Message and Receive Deterministic AI Response

**Related BDD Feature:** `contextualized_response.feature` - _"Student asks a course-related question and receives a structured explanation"_  
**Related Requirement:** FR2, FR3, FR4, NFR1

**Steps Performed:**

1. Open an existing session (or create one)
2. Click the message input field (`data-testid="message-input"`)
3. Type `"What is unit testing?"`
4. Click the **Send** button (`data-testid="send-message-btn"`) or press Enter
5. Observe the chat bubble area

**Expected Result:**

- User message bubble (`data-testid="user-message"`) appears immediately
- Typing indicator (`data-testid="chat-loading"`) briefly visible
- AI reply bubble (`data-testid="assistant-message"`) appears with content:  
  `Hello, your question was: "What is unit testing?"`
- Backend returns HTTP 201 for `POST /api/v1/sessions/{id}/messages`

**Actual Result:**

- User bubble appeared instantly (optimistic UI)
- Loading dots animated for ~300ms
- AI reply appeared with expected deterministic content
- Network tab confirmed HTTP 201 with `user_message` + `ai_message` in response body

**Result:** PASS

---

## TC-UI-04 - Resume Session and Previous Messages are Available

**Related BDD Feature:** `resume_learning_session.feature` - _"Student resumes an existing session and previous context is available"_  
**Related Requirement:** FR4, FR11, FR18, NFR7

**Steps Performed:**

1. Open an existing session that already has messages
2. Click on a **different session** in the sidebar to switch away
3. Click back on the **original session**
4. Observe the message list

**Expected Result:**

- Previously sent messages (user + AI) are reloaded from the backend
- Message history is displayed in correct chronological order
- `GET /api/v1/sessions/{id}/messages` is called on session switch

**Actual Result:**

- Message history loaded correctly on re-selecting the session
- Both user and AI bubbles rendered in correct order
- Network tab confirmed `GET /messages` request fired on session switch

**Result:** PASS

---

## TC-UI-05 - Delete a Session

**Related BDD Feature:** `resume_learning_session.feature` - _"Student tries to resume a non-existing session"_  
**Related Requirement:** FR12, NFR5

**Steps Performed:**

1. Create a session titled `"Session to Delete"`
2. Hover over the session item in the sidebar
3. Click the **X delete button** that appears on hover
4. Observe the sidebar and main content area

**Expected Result:**

- Session is removed from the sidebar list
- Main content area returns to the Welcome screen
- Backend returns HTTP 204 for `DELETE /api/v1/sessions/{id}`

**Actual Result:**

- Session removed from sidebar immediately
- Welcome screen appeared
- Network tab confirmed HTTP 204

**Result:** PASS

---

## TC-UI-06 - Empty Message Input - Send Button Disabled

**Related BDD Feature:** `contextualized_response.feature` - _"Student submits an empty answer"_  
**Related Requirement:** FR2, NFR5

**Steps Performed:**

1. Open any session
2. Ensure the message input (`data-testid="message-input"`) is empty
3. Observe the state of the Send button (`data-testid="send-message-btn"`)
4. Try clicking the Send button
5. Enter a single space and observe

**Expected Result:**

- Send button is visually disabled (dimmed) when input is empty or whitespace-only
- No API call is made on click
- No message bubble is added

**Actual Result:**

- Send button correctly disabled for empty and whitespace-only input
- No network request fired
- Button became enabled only after at least one non-whitespace character

**Result:** PASS

---

## Reflection

**What was straightforward:**  
The happy-path flows (create session, send message, receive reply) were quick to verify manually. The UI feedback is immediate and clear - the optimistic user bubble and the deterministic AI reply made it easy to confirm correct behavior without waiting for network delays.

**What was tedious or error-prone:**  
Verifying transient states like the typing indicator (`data-testid="chat-loading"`) was difficult manually because it disappears within milliseconds. Repeatedly creating and deleting sessions to test isolation between test cases was repetitive. Confirming the exact request/response body required keeping the browser DevTools Network tab open throughout.

**How automation helps:**  
Automated E2E tests with Playwright eliminate all repetition and can assert transient states like the loading indicator reliably using `waitFor`. Tests run in isolation with unique session titles per run, removing manual cleanup.
