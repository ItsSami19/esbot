# Exercise 8.1 - Unit Testing Analysis: ESBot Domain Models

---

## Approach

To analyse the existing unit tests for the ESBot domain models, the following Black-Box test design techniques from the lecture were applied:

- **Equivalence Partitioning (EP)** - group inputs into valid and invalid classes to reduce redundant test cases
- **Boundary Value Analysis (BVA)** - test values at and just outside the boundaries of valid input ranges
- **Decision Table Testing** - test combinations of conditions and their expected outcomes
- **State Transition Testing** - test stateful fields and their valid/invalid transitions

---

## Current Test Coverage

### UserSession

Current tests cover:
- `test_can_create_with_valid_data`
- `test_title_is_required_and_non_nullable`

### Message

Current tests cover:
- `test_create_helper_builds_message`
- `test_content_is_required_and_non_nullable`
- `test_relationship_with_user_session_is_consistent`

### QuizRequest

Current tests cover:
- `test_create_helper_builds_quiz_request`
- `test_topic_is_required_and_non_nullable`
- `test_relationship_with_quiz_item_is_consistent`

### QuizItem

Current tests cover:
- `test_create_helper_builds_quiz_item`
- `test_required_fields_are_non_nullable`
- `test_relationship_with_submitted_answer_and_quiz_request`

### SubmittedAnswer

Current tests cover:
- `test_create_helper_builds_submitted_answer`
- `test_user_response_is_required_and_non_nullable`
- `test_relationship_with_quiz_item_is_consistent`

### EvaluationResult

Current tests cover:
- `test_create_helper_builds_evaluation_result`
- `test_feedback_is_required_and_non_nullable`
- `test_relationship_with_submitted_answer_is_consistent`

---

## Equivalence Partitioning

### UserSession

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `title` | Valid: non-empty string | `"Python Basics"` |
| `title` | Invalid: empty string | `""` |
| `title` | Invalid: null | `None` |
| `user_identifier` | Valid: non-empty string | `"user_42"` |
| `user_identifier` | Invalid: null | `None` |
| `status` | Valid: ACTIVE | `SessionStatus.ACTIVE` |
| `status` | Valid: ARCHIVED | `SessionStatus.ARCHIVED` |
| `status` | Valid: DELETED | `SessionStatus.DELETED` |

### Message

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `content` | Valid: non-empty string | `"What is a loop?"` |
| `content` | Invalid: empty string | `""` |
| `content` | Invalid: null | `None` |
| `sender` | Valid: USER | `Sender.USER` |
| `sender` | Valid: AI | `Sender.AI` |
| `order` | Valid: positive integer | `1` |
| `order` | Invalid: zero | `0` |
| `order` | Invalid: negative | `-1` |

### QuizRequest

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `topic` | Valid: non-empty string | `"Loops in Python"` |
| `topic` | Invalid: empty string | `""` |
| `topic` | Invalid: null | `None` |
| `status` | Valid: PENDING | `QuizStatus.PENDING` |
| `status` | Valid: GENERATED | `QuizStatus.GENERATED` |
| `status` | Valid: COMPLETED | `QuizStatus.COMPLETED` |

### QuizItem

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `question_text` | Valid: non-empty string | `"What does a for-loop do?"` |
| `question_text` | Invalid: empty string | `""` |
| `question_text` | Invalid: null | `None` |
| `correct_answer` | Valid: non-empty string | `"It iterates over a sequence"` |
| `correct_answer` | Invalid: null | `None` |
| `answer_options` | Valid: dict with entries | `{"A": "...", "B": "..."}` |
| `answer_options` | Valid: null (optional) | `None` |
| `difficulty` | Valid: known level | `"easy"`, `"medium"`, `"hard"` |
| `difficulty` | Valid: null (optional) | `None` |

### SubmittedAnswer

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `user_response` | Valid: non-empty string | `"A for-loop iterates."` |
| `user_response` | Invalid: empty string | `""` |
| `user_response` | Invalid: null | `None` |

### EvaluationResult

| Parameter | Equivalence Class | Representative |
| :-- | :-- | :-- |
| `is_correct` | Valid: True | `True` |
| `is_correct` | Valid: False | `False` |
| `feedback` | Valid: non-empty string | `"Correct! Well done."` |
| `feedback` | Invalid: empty string | `""` |
| `feedback` | Invalid: null | `None` |
| `explanation` | Valid: non-empty string | `"A for-loop goes through each item."` |
| `explanation` | Valid: null (optional) | `None` |

---

## Boundary Value Analysis

### UserSession - `title`

| Boundary | Value | Expected Result |
| :-- | :-- | :-- |
| Just below minimum | `""` | Not accepted |
| Minimum valid | `"A"` (1 char) | Accepted |

### Message - `content`

| Boundary | Value | Expected Result |
| :-- | :-- | :-- |
| Just below minimum | `""` | Not accepted |
| Minimum valid | `"A"` (1 char) | Accepted |

### Message - `order`

| Boundary | Value | Expected Result |
| :-- | :-- | :-- |
| Below minimum | `-1` | Not accepted |
| Boundary | `0` | Not accepted |
| Minimum valid | `1` | Accepted |

### QuizRequest - `topic`

| Boundary | Value | Expected Result |
| :-- | :-- | :-- |
| Just below minimum | `""` | Not accepted |
| Minimum valid | `"A"` (1 char) | Accepted |

### SubmittedAnswer - `user_response`

| Boundary | Value | Expected Result |
| :-- | :-- | :-- |
| Just below minimum | `""` | Not accepted |
| Minimum valid | `"A"` (1 char) | Accepted |

---

## Decision Table Testing

### QuizItem - `answer_options` and `correct_answer`

| Rule | `answer_options` | `correct_answer` | Expected Result |
| :-- | :-- | :-- | :-- |
| 1 | `{"A": "...", "B": "..."}` | `"A"` (in options) | Valid |
| 2 | `{"A": "...", "B": "..."}` | `"C"` (not in options) | Invalid |
| 3 | `None` | `"A"` | Valid (options optional) |

### EvaluationResult - `is_correct` and `feedback`

| Rule | `is_correct` | `feedback` | Expected Result |
| :-- | :-- | :-- | :-- |
| 1 | `True` | non-empty string | Valid |
| 2 | `False` | non-empty string | Valid |
| 3 | `True` | `""` | Invalid |
| 4 | `False` | `""` | Invalid |

---

## State Transition Testing

### QuizRequest - `QuizStatus`

```
PENDING --> GENERATED --> COMPLETED
```

| Test Case | Start State | Event | Expected End State |
| :-- | :-- | :-- | :-- |
| TC-1 | PENDING | quiz generated | GENERATED |
| TC-2 | GENERATED | quiz completed | COMPLETED |
| TC-3 | COMPLETED | further transition attempted | No change |

### UserSession - `SessionStatus`

```
ACTIVE --> ARCHIVED
ACTIVE --> DELETED
```

| Test Case | Start State | Event | Expected End State |
| :-- | :-- | :-- | :-- |
| TC-1 | ACTIVE | session archived | ARCHIVED |
| TC-2 | ACTIVE | session deleted | DELETED |
| TC-3 | ARCHIVED | re-activation attempted | No change / invalid |

---

## Gaps in Current Tests

| Model | What is missing | Technique |
| :-- | :-- | :-- |
| UserSession | Only ACTIVE status tested; no invalid `title` or `user_identifier` | EP |
| Message | No empty `content` test; only one `Sender` value tested; no `order` edge cases | EP, BVA |
| QuizRequest | Only PENDING tested; no empty `topic`; no status transitions | EP, BVA, State Transition |
| QuizItem | No combination test for `answer_options` + `correct_answer` | Decision Table |
| SubmittedAnswer | No empty or null `user_response` test | EP, BVA |
| EvaluationResult | No combination test for `is_correct` + `feedback` | Decision Table |

---

## Test Coverage

| Metric | Current | Target |
| :-- | :-- | :-- |
| Test Coverage | ~60% | 85% |
| Equivalence Class Coverage | ~20% | 80% |
| Boundary Value Coverage | ~10% | 80% |
