# Exercise 7 - Test Design Techniques

## 7.1 Black-Box Testing Techniques

### Feature under test

`QuizRequest` has three relevant input parameters:

- `topic`
- `count`
- `difficulty`

A request is only valid if **all three parameters** are valid.

---

## Equivalence Class Partitioning

### Parameter: `topic`

**Rule:** `topic` must be a string with **3 to 100 characters (inclusive)**.

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|---|---|---|---|---|
| `topic` | EC-T-1 | Valid | Length is between 3 and 100 characters | `"Quality Assurance"` |
| `topic` | EC-T-2 | Invalid | Length is less than 3 | `"QA"` |
| `topic` | EC-T-3 | Invalid | Length is greater than 100 | `"Z"` repeated 101 times |
| `topic` | EC-T-4 | Invalid | Empty or blank topic | `""` / `"   "` |
| `topic` | EC-T-5 | Invalid | Missing or not a string | `null` / `12345` |

#### Justification for `topic`

- `"Quality Assurance"`
  - normal valid topic
  - clearly inside the allowed range
  - maps to **FR7**
  - invalid values also relate to **NFR3**

- `"QA"`
  - length is 2
  - directly below the minimum boundary
  - should be rejected

- `"Z"` repeated 101 times
  - directly above the maximum boundary
  - should be rejected

- `""`, `"   "`, `null`, `12345`
  - no useful topic for quiz generation
  - should be handled by input validation

---

### Boundary Value Analysis for `topic`

| Test Value | Length | Expected Result | Reason |
|---|---:|---|---|
| `"QA"` | 2 | Rejected | Just below the minimum boundary |
| `"CPU"` | 3 | Accepted | Minimum valid topic length |
| `"Java"` | 4 | Accepted | Just above the minimum boundary |
| `"Z"` repeated 99 times | 99 | Accepted | Just below the maximum boundary |
| `"Z"` repeated 100 times | 100 | Accepted | Maximum valid topic length |
| `"Z"` repeated 101 times | 101 | Rejected | Just above the maximum boundary |

**Requirement reference:** FR7, NFR3

---

### Parameter: `count`

**Rule:** `count` must be an integer between **1 and 10 (inclusive)**.

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|---|---|---|---|---|
| `count` | EC-C-1 | Valid | Integer between 1 and 10 | `5` |
| `count` | EC-C-2 | Invalid | Integer lower than 1 | `0` |
| `count` | EC-C-3 | Invalid | Integer greater than 10 | `11` |
| `count` | EC-C-4 | Invalid | Value is not an integer | `"five"` |
| `count` | EC-C-5 | Invalid | Value is missing or null | `null` |

#### Justification for `count`

- `5`
  - normal valid value
  - inside the allowed interval
  - maps to **FR7**
  - invalid values also relate to **NFR3**

- `0`
  - directly below the minimum boundary
  - should be rejected

- `11`
  - directly above the maximum boundary
  - should be rejected

- `"five"` and `null`
  - not valid integers
  - should be rejected by input validation

---

### Boundary Value Analysis for `count`

| Test Value | Expected Result | Reason |
|---:|---|---|
| `0` | Rejected | Just below the minimum boundary |
| `1` | Accepted | Minimum valid count |
| `2` | Accepted | Just above the minimum boundary |
| `9` | Accepted | Just below the maximum boundary |
| `10` | Accepted | Maximum valid count |
| `11` | Rejected | Just above the maximum boundary |

**Requirement reference:** FR7, NFR3

---

### Parameter: `difficulty`

**Rule:** `difficulty` must be one of:

- `easy`
- `medium`
- `hard`

| Parameter | Class ID | Class Type | Partition Description | Representative Test Value |
|---|---|---|---|---|
| `difficulty` | EC-D-1 | Valid | Difficulty is exactly `easy` | `"easy"` |
| `difficulty` | EC-D-2 | Valid | Difficulty is exactly `medium` | `"medium"` |
| `difficulty` | EC-D-3 | Valid | Difficulty is exactly `hard` | `"hard"` |
| `difficulty` | EC-D-4 | Invalid | Unsupported difficulty string | `"expert"` |
| `difficulty` | EC-D-5 | Invalid | Empty or blank difficulty | `""` / `"   "` |
| `difficulty` | EC-D-6 | Invalid | Missing or null difficulty | `null` |

#### Justification for `difficulty`

- `"easy"`, `"medium"`, `"hard"`
  - all three are explicitly allowed by the specification
  - each value should be tested once
  - maps to **FR7**

- `"expert"`
  - valid string format, but not an accepted value
  - should be rejected

- `""`, `"   "`, `null`
  - missing or empty difficulty
  - should be rejected
  - invalid values also relate to **NFR3**

- Boundary value analysis
  - not useful here
  - `difficulty` is a fixed set of values, not a numeric or length-based range

---

## Decision Table for Answer Evaluation

### Conditions

- Answer correctness:
  - Correct
  - Partially correct
  - Incorrect
- Answer is empty or blank:
  - Yes
  - No
- Quiz item still exists in session:
  - Yes
  - No

`-` means don't-care.

| Rule | Answer Correctness | Answer Empty / Blank | Quiz Item Exists in Session | Expected Action / Feedback | Requirement / Edge Case |
|---|---|---|---|---|---|
| R1 | - | - | No | Reject evaluation; quiz item not found or no longer available | FR8, FR9, NFR3, missing quiz item |
| R2 | - | Yes | Yes | Reject answer; ask student to enter a non-empty answer | FR8, FR9, NFR3, empty input |
| R3 | Correct | No | Yes | Return positive feedback | FR8, FR9 |
| R4 | Partially correct | No | Yes | Return constructive feedback with hints | FR8, FR9 |
| R5 | Incorrect | No | Yes | Return corrective feedback with explanation | FR8, FR9 |

---

## 7.2 State Transition Testing - Learning Session Lifecycle
### State Transition Diagram

![UserSession State Transition Diagram](images/UserSession_State_Transition_Diagram.png)

---

### State Transition Table

| Current State | Event | Next State | Output / Action |
|---|---|---|---|
| `NEW` | `submit_message` | `ACTIVE` | Message accepted; session becomes active |
| `NEW` | `request_quiz` | `ACTIVE` | Quiz request accepted; session becomes active |
| `NEW` | `submit_answer` | `ACTIVE` | Answer received; if no quiz item exists, return controlled evaluation error |
| `NEW` | `inactivity_timeout` | `-` | Invalid or no effect; no interaction happened yet |
| `NEW` | `session_timeout` | `EXPIRED` | Session lifetime exceeded |
| `NEW` | `close_session` | `EXPIRED` | Session explicitly closed |
| `NEW` | `resume_session` | `-` | Invalid; session is not idle |
| `ACTIVE` | `submit_message` | `ACTIVE` | Message accepted; session stays active |
| `ACTIVE` | `request_quiz` | `ACTIVE` | Quiz request accepted; session stays active |
| `ACTIVE` | `submit_answer` | `ACTIVE` | Answer evaluated; session stays active |
| `ACTIVE` | `inactivity_timeout` | `IDLE` | Session marked idle |
| `ACTIVE` | `session_timeout` | `EXPIRED` | Session expired |
| `ACTIVE` | `close_session` | `EXPIRED` | Session explicitly closed |
| `IDLE` | `submit_message` | `-` | Invalid unless session is resumed first |
| `IDLE` | `request_quiz` | `-` | Invalid unless session is resumed first |
| `IDLE` | `submit_answer` | `-` | Invalid unless session is resumed first |
| `IDLE` | `inactivity_timeout` | `IDLE` | No change; session remains idle |
| `IDLE` | `session_timeout` | `EXPIRED` | Idle session expired |
| `IDLE` | `close_session` | `EXPIRED` | Idle session closed |
| `IDLE` | `resume_session` | `ACTIVE` | Session restored |
| `EXPIRED` | `submit_message` | `EXPIRED` | Rejected; controlled error: session expired |
| `EXPIRED` | `request_quiz` | `EXPIRED` | Rejected; controlled error: session expired |
| `EXPIRED` | `submit_answer` | `EXPIRED` | Rejected; controlled error: session expired |
| `EXPIRED` | `inactivity_timeout` | `-` | Invalid or no effect; already expired |
| `EXPIRED` | `session_timeout` | `-` | Invalid or no effect; already expired |
| `EXPIRED` | `close_session` | `EXPIRED` | No change; already closed |
| `EXPIRED` | `resume_session` | `EXPIRED` | Rejected; expired sessions cannot be resumed |

**Requirement reference:** FR4, FR10, FR11, FR12, NFR3

---

### Test Sequences for All-Transitions Coverage

The following sequences cover all valid transitions at least once. Invalid transitions are covered in ST-008.

#### ST-001: Message, idle, resume

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `submit_message` | `ACTIVE` | Message accepted |
| 2 | `inactivity_timeout` | `IDLE` | Session marked idle |
| 3 | `resume_session` | `ACTIVE` | Session restored |

**Requirement:** FR2, FR4, FR10, FR11

---

#### ST-002: Quiz and answer while active

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `request_quiz` | `ACTIVE` | Quiz request accepted |
| 2 | `submit_answer` | `ACTIVE` | Answer evaluated |
| 3 | `submit_message` | `ACTIVE` | Message accepted |

**Requirement:** FR7, FR8, FR9, FR4

---

#### ST-003: Timeout from ACTIVE

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `submit_message` | `ACTIVE` | Message accepted |
| 2 | `session_timeout` | `EXPIRED` | Session expires |

**Requirement:** FR10, FR11, FR12

---

#### ST-004: Timeout from IDLE

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `submit_message` | `ACTIVE` | Message accepted |
| 2 | `inactivity_timeout` | `IDLE` | Session marked idle |
| 3 | `session_timeout` | `EXPIRED` | Idle session expires |

**Requirement:** FR10, FR11, FR12

---

#### ST-005: Explicit close from NEW

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `close_session` | `EXPIRED` | Session is closed |

**Requirement:** FR12

---

#### ST-006: Explicit close from ACTIVE

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `request_quiz` | `ACTIVE` | Quiz request accepted |
| 2 | `close_session` | `EXPIRED` | Active session is closed |

**Requirement:** FR7, FR12

---

#### ST-007: Explicit close from IDLE

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `NEW` | Session exists |
| 1 | `submit_message` | `ACTIVE` | Message accepted |
| 2 | `inactivity_timeout` | `IDLE` | Session marked idle |
| 3 | `close_session` | `EXPIRED` | Idle session is closed |

**Requirement:** FR10, FR11, FR12

---

#### ST-008: Invalid interaction after expiration

| Step | Event | Expected State | Expected Output |
|---:|---|---|---|
| Start | - | `EXPIRED` | Session already expired |
| 1 | `submit_message` | `EXPIRED` | Rejected; controlled error |
| 2 | `request_quiz` | `EXPIRED` | Rejected; controlled error |
| 3 | `submit_answer` | `EXPIRED` | Rejected; controlled error |
| 4 | `resume_session` | `EXPIRED` | Rejected; expired session cannot be resumed |

**Requirement:** NFR3, edge case: session expired

---

## 7.3 Reflection - Test Design Technique Comparison

### Complementarity

- **ECP / BVA**
  - best for input validation
  - ESBot example:
    - `topic` length
    - `count` range
    - allowed `difficulty` values
  - verifies **FR7** and **NFR3**

- **Decision Table**
  - best when several conditions influence one result
  - ESBot example:
    - answer is empty
    - quiz item is missing
    - answer is correct / partially correct / incorrect
  - verifies **FR8** and **FR9**

- **State Transition Testing**
  - best for lifecycle behaviour
  - ESBot example:
    - `ACTIVE -> IDLE`
    - `IDLE -> ACTIVE`
    - rejected interaction in `EXPIRED`
  - verifies **FR4**, **FR10**, **FR11**, **FR12**, and **NFR3**

### Gaps

- These techniques do not fully check the quality of generated AI content.
- Example:
  - a quiz can be valid by input rules, but still contain weak or unclear questions.
- Useful additional techniques:
  - use-case testing
  - scenario-based testing
  - manual review with a simple quality checklist

### Effort vs. value

- Best value for ESBot:
  - **ECP + BVA**
- Reason:
  - low effort
  - directly checks important quiz validation rules from **FR7**
  - catches boundary errors early
- State transition testing is also useful for session behaviour, but needs more effort.
- The decision table is small, but helpful for separating normal feedback from error cases.

---

_Comment: ChatGPT Version 5.3 was used for formatting, structuring, and translation (May 11, 2026; 7:54 PM)._