# E2E Test Setup - ESBot (Exercise 11.2)

## Framework

**Playwright** (TypeScript) - chosen for its built-in auto-waiting, cross-browser support, trace viewer, and seamless integration with a Next.js frontend.

| Property    | Value                              |
| ----------- | ---------------------------------- |
| Framework   | Playwright                         |
| Language    | TypeScript                         |
| Browser     | Chromium (headless by default)     |
| Test file   | `frontend/playwright/chat.spec.ts` |
| Run command | `npx playwright test`              |

---

## Prerequisites

- Node.js 20+
- The full Docker stack must be running before executing tests (frontend on `http://localhost:3000`)

---

## Installation

All dependencies are already declared in `frontend/package.json`. From the `frontend/` directory, run:

```bash
cd frontend
npm install
npx playwright install chromium
```

> Only Chromium is required. The other browsers (Firefox, WebKit) are not needed for this test suite.

---

## Starting the Application

The tests require the full stack to be running. Start it with Docker Compose from the project root:

```bash
docker compose -f docker-compose.dev.yml up
```

Wait until all services are healthy and `http://localhost:3000` is accessible in the browser before running tests.

---

## Running the Tests

### Headless (CI-style - default)

```bash
cd frontend
npx playwright test
```

All 6 tests run in a single Chromium worker. Expected output:

```
Running 6 tests using 1 worker

  ✓  1 [chromium] › playwright\chat.spec.ts › Session Management › TC-E2E-01
  ✓  2 [chromium] › playwright\chat.spec.ts › Session Management › TC-E2E-02
  ✓  3 [chromium] › playwright\chat.spec.ts › Chat Flow › TC-E2E-03
  ✓  4 [chromium] › playwright\chat.spec.ts › Chat Flow › TC-E2E-04
  ✓  5 [chromium] › playwright\chat.spec.ts › Negative / Error Cases › TC-E2E-05
  ✓  6 [chromium] › playwright\chat.spec.ts › Negative / Error Cases › TC-E2E-06

  6 passed (~6s)
```

### With Visible Browser

```bash
npx playwright test --headed
```

Opens a real Chromium window and executes the tests visibly - useful for debugging UI flows.

### Interactive UI Mode

```bash
npx playwright test --ui
```

Opens the Playwright UI - each test can be selected individually, with a live browser preview and step-by-step trace.

### Show Trace for a Failed Test

If a test fails, a trace archive is saved automatically in `test-results/`. Inspect it with:

```bash
npx playwright show-trace test-results/<test-folder>/trace.zip
```

---

## Playwright Configuration

Configuration lives in `frontend/playwright.config.ts`:

```ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './playwright',
  fullyParallel: false,
  retries: 1,
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
})
```

---

## Test Scenarios

### Helper: `createSessionAndOpen`

A shared helper function used across all tests. It creates a new session via the sidebar and waits until the chat window is fully open (i.e., `data-testid="message-input"` is visible). This prevents race conditions between the session creation API call and the UI rendering the chat panel.

### TC-E2E-01 - Health Badge Visible on Load

**Group:** Session Management  
**Scenario:** The health indicator dot in the sidebar header must be visible immediately after page load, confirming the API health check resolves correctly.

```
Given the user navigates to "/"
Then the element [data-testid="health-status"] is visible
```

### TC-E2E-02 - Create a New Session

**Group:** Session Management  
**Scenario:** A user creates a new session with a unique title. The session must appear in the sidebar session list after creation.

```
Given the user navigates to "/"
When they click the "New Session" button and enter a unique title
And confirm with Enter
Then the sidebar session list contains the new session title
```

### TC-E2E-03 - Send a Message and Receive AI Reply

**Group:** Chat Flow  
**Scenario:** A user sends a message in an active session. The user bubble appears immediately, and the AI reply bubble appears within 10 seconds.

```
Given an active chat session is open
When the user types a message and clicks Send
Then a user message bubble appears with the correct text
And an assistant message bubble appears within 10 seconds
And the AI reply text is non-empty
```

### TC-E2E-04 - Message History Persists

**Group:** Chat Flow  
**Scenario:** After sending one message and receiving one AI reply, the message list contains exactly one user bubble and one assistant bubble.

```
Given an active chat session is open
When the user sends one message
And the AI reply arrives
Then the message list contains exactly 1 user-message
And exactly 1 assistant-message
```

### TC-E2E-05 - Send Button Disabled on Empty Input _(Negative)_

**Group:** Negative / Error Cases  
**Scenario:** The send button must be disabled when the message input field is empty, preventing empty message submissions.

```
Given an active chat session is open
And the message input is empty
Then the send button [data-testid="send-message-btn"] is disabled
```

### TC-E2E-06 - Delete Session Removes It from Sidebar _(Negative)_

**Group:** Negative / Error Cases  
**Scenario:** A user deletes a session by hovering over it and clicking the delete button. The session must disappear from the sidebar list.

```
Given a session with a known title exists in the sidebar
When the user hovers over the session item
And clicks the delete button
Then the session list no longer contains the session title
```

---

## Selector Strategy

All selectors use `data-testid` attributes exclusively - never CSS classes or positional XPaths. This decouples tests from styling changes and DOM restructuring.

| Element                | Selector                            |
| ---------------------- | ----------------------------------- |
| Health dot             | `[data-testid="health-status"]`     |
| New session button     | `[data-testid="new-session-btn"]`   |
| Session list           | `[data-testid="session-list"]`      |
| Message input          | `[data-testid="message-input"]`     |
| Send button            | `[data-testid="send-message-btn"]`  |
| User message bubble    | `[data-testid="user-message"]`      |
| AI message bubble      | `[data-testid="assistant-message"]` |
| Message list container | `[data-testid="message-list"]`      |

---

## npm Script

The run command is registered in `frontend/package.json` for convenience:

```json
{
  "scripts": {
    "test:e2e:playwright": "playwright test"
  }
}
```

Run via:

```bash
npm run test:e2e:playwright
```
