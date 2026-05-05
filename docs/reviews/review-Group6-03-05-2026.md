# Review template (inspection / technical review)

**Project / product:** ESBot <https://github.com/tzporter/esbot>  
**Review object(s):** ESBot documentation, requirements/specification, backend implementation, domain model, unit tests, BDD tests, Docker/devcontainer setup  
**Review type:** Technical review  
**Date (planned / actual):** 2026-05-03 / 2026-05-03  
**Moderator:** Sami Goekpinar  
**Author(s):** Melek Goekler, Zeynep Pektas, Truman Zachary Porter, Sena Zeynep Yamak  
**Reviewers:** Baran Bickici, Sema Dagci, Sami Goekpinar, Lydia Karapanagiotidi

---

## 1. General instructions

We used the course review template for this repository-based review.  
Our selected review process is a **technical review**.

We chose this review type because:

- the reviewed artefacts include documentation, requirements, backend code, data models, tests, and setup files
- it gives us enough structure for findings, severity levels, and follow-up actions
- it is less formal and less time-consuming than an inspection
- it fits the course timebox and the prototype scope of ESBot

No formal kick-off or feedback meeting with Group 6 was conducted.  
We performed the review as a repository-based review within Group 5.  
The review meeting mentioned below refers to our internal Group 5 consolidation of findings.

**Terminology**

| Acronym | Meaning           |
| ------- | ----------------- |
| **MP**  | Master Plan       |
| **DS**  | Data Summary      |
| **LoF** | Level of Findings |
| **RR**  | Review Report     |

### Phases of a review / inspection

| Phase                      | Description                                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Planning**               | We defined the scope, reviewed artefacts, roles, and review type within Group 5.                                |
| **Kick-off (optional)**    | We did not conduct a formal kick-off with Group 6. We used the repository files as input for the review.        |
| **Individual preparation** | We inspected documentation, requirements, backend code, tests, BDD files, Docker setup, and devcontainer setup. |
| **Review meeting**         | We internally consolidated our findings in Group 5 and aligned type, severity, and follow-up recommendations.   |
| **Reworking**              | Rework is owned by Group 6. We only provide findings and recommendations.                                       |
| **Follow-up**              | No formal follow-up meeting was planned. Group 6 can decide which findings to accept, defer, or reject.         |

---

## 2. Master Plan (MP)

### 2.1 Masterplan - header

| Field                    | Value                                                                  |
| ------------------------ | ---------------------------------------------------------------------- |
| Review No.               | REV-2026-001                                                           |
| Project                  | ESBot                                                                  |
| Project manager          | Truman Zachary Porter                                                  |
| Quality expert / manager | -                                                                      |
| Moderator                | Sami Goekpinar                                                         |
| Author(s)                | Melek Goekler, Zeynep Pektas, Truman Zachary Porter, Sena Zeynep Yamak |

### 2.2 Review objects

| #   | Review objects                                                                                | Abbr.     |
| --- | --------------------------------------------------------------------------------------------- | --------- |
| 1   | `docs/esbot.md`                                                                               | EB        |
| 2   | `docs/spec/requirements.md`                                                                   | REQ       |
| 3   | `docs/spec/spec.md`                                                                           | SPEC      |
| 4   | `docs/spec/data-model.md`                                                                     | DM        |
| 5   | `docs/spec/plan.md`                                                                           | PLAN      |
| 6   | `docs/spec/quality.md`                                                                        | QUAL      |
| 7   | `docs/spec/test-strategy.md`                                                                  | TS        |
| 8   | `docs/spec/use-cases.md`                                                                      | UC        |
| 9   | `docs/spec/ux-factors.md`, `docs/spec/ux-evaluation-plan.md`, `docs/spec/ux-quality-model.md` | UX        |
| 10  | `docs/setup.md`                                                                               | SETUP-DOC |
| 11  | `docs/Project_Outline.md`                                                                     | OUTLINE   |
| 12  | `backend/models.py`                                                                           | MOD       |
| 13  | `backend/main.py`                                                                             | API       |
| 14  | `backend/ai_service.py`                                                                       | AI        |
| 15  | `backend/tests/*.py`                                                                          | TEST      |
| 16  | `backend/features/*.feature`, `backend/features/steps/*.py`                                   | BDD       |
| 17  | `backend/Dockerfile`, `docker-compose.yml`, `.devcontainer/devcontainer.json`                 | DEV       |

### 2.3 Reference documents

We mainly used the review objects themselves as reference material.  
For context, we also used the Exercise 6 task description and the course review template.

| #   | Reference documents         | Abbr.    |
| --- | --------------------------- | -------- |
| 1   | Exercise 6 task description | EX6      |
| 2   | Course review template      | TEMPLATE |
| 3   | Group 6 ESBot repository    | REPO     |

### 2.4 Checklists / scenarios

| #   | Checklists / scenarios                                                                          |
| --- | ----------------------------------------------------------------------------------------------- |
| 1   | Documentation consistency: system description, requirements, specification, data model          |
| 2   | Requirement testability: clear, measurable, and realistic requirements                          |
| 3   | Architecture consistency: planned architecture compared with implementation                     |
| 4   | Backend maintainability: separation of API, service, model, and AI integration logic            |
| 5   | API validation and error-handling scenarios                                                     |
| 6   | Test coverage review: unit tests and BDD tests for main user flows                              |
| 7   | Setup and reproducibility: Docker, devcontainer, database, test commands, environment variables |

### 2.5 Reviewer assignment

| Reviewer | Names (and chapters / checklists or scenarios assigned to the review)                         | Abbr. |
| :------: | --------------------------------------------------------------------------------------------- | ----- |
|    1     | Baran Bickici - backend API, BDD scenarios, error handling                                    | BB    |
|    2     | Sema Dagci - documentation, requirements, specification, use cases                            | SD    |
|    3     | Sami Goekpinar - repository structure, Docker/devcontainer setup, data model, test setup      | SG    |
|    4     | Lydia Karapanagiotidi - quality documents, UX documents, test strategy, positive observations | LK    |

### 2.6 Kick-off

| Date / time / location                                                          |
| ------------------------------------------------------------------------------- |
| No formal kick-off meeting with Group 6. Repository-based review on 2026-05-03. |

### 2.7 Individual preparation

| Individual preparation    | Value                                                                                 | Unit  |
| ------------------------- | ------------------------------------------------------------------------------------- | ----- |
| Submission of findings by | 2026-05-03                                                                            | -     |
| Size of review objects    | Multiple documentation files, backend source files, tests, BDD files, and setup files | mixed |
| Optimal inspection rate   | Not measured precisely; lightweight course review                                     | -     |
| Optimal inspection time   | Approx. 4.00-5.00 total team hours                                                    | h     |

### 2.8 Review meeting

| Date / time / location                                 |
| ------------------------------------------------------ |
| 2026-05-03, internal Group 5 consolidation of findings |

### 2.9 Additional milestones (optional)

| Milestone                     | Planned date / time | Actual date / time |
| ----------------------------- | ------------------- | ------------------ |
| End of individual preparation | 2026-05-03          | 2026-05-03         |
| Rework deadline               | Not defined         | -                  |
| Follow-up / closure           | 2026-05-03          | 2026-05-03         |

---

## 3. List of findings (LoF)

**Type:** defect, question, suggestion  
**Severity scale:** blocking, major, minor, editorial  
**Status values:** open, accepted, rejected, deferred, fixed

| ID    | Location (file / section / module)                     | Summary                                                                                                                                                                                                            | Type       | Severity  | Status | Owner   | Notes / meeting decision                                                                                                             |
| ----- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | --------- | ------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| F-001 | `docs/spec/tasks.md`                                   | All tasks are marked as “Not Started”, although backend code, tests, Docker setup, and documentation already exist.                                                                                                | defect     | minor     | open   | Group 6 | Update task status so the task document reflects the current project state.                                                          |
| F-002 | `DM`, `MOD`                                            | The data model document describes the main entities, but it does not mention the relationship from `SubmittedAnswer` to `EvaluationResult`. The implementation contains this relationship.                         | defect     | minor     | open   | Group 6 | Add `SubmittedAnswer (1) ↔ (0..1 or 1) EvaluationResult` to the data model documentation.                                            |
| F-003 | `API`                                                  | Some endpoints use raw `dict` request bodies, for example `/chat` and `/quiz-request`. This works, but the API contract is less explicit.                                                                          | suggestion | minor     | open   | Group 6 | Use Pydantic request models for all API inputs, similar to `SubmitAnswerRequest`.                                                    |
| F-004 | `API`                                                  | API endpoint functions contain several responsibilities: validation, database access, AI calls, retry logic, parsing, and persistence.                                                                             | suggestion | major     | open   | Group 6 | Move business logic into service functions/classes to improve maintainability and testability.                                       |
| F-005 | `AI`                                                   | In `evaluate_answer()`, the final `except Exception as e` only re-raises `ValueError`. For other exception types, the function may end without a clear return value or clear error.                                | defect     | major     | open   | Group 6 | Add an explicit fallback, for example raising `ConnectionError` or another clear application-level error for unexpected AI failures. |
| F-006 | `BDD` (`backend/features/steps/request_quiz_steps.py`) | Suspicious imports at the top: `from numpy import select` and `from requests import Session, delete`. They are later overwritten by `sqlmodel` imports.                                                            | defect     | minor     | open   | Group 6 | Remove unused or incorrect imports to avoid confusion and static analysis warnings.                                                  |
| F-007 | `BDD` (`backend/features/steps/*.py`)                  | Each step file defines its own `after_scenario` cleanup function. In Behave, hooks are normally placed in `features/environment.py`; local cleanup functions may not be executed as intended.                      | question   | minor     | open   | Group 6 | Verify whether mocks are always stopped correctly. Consider moving cleanup to `features/environment.py`.                             |
| F-008 | `docker-compose.yml`                                   | Database credentials are hardcoded in the compose file. This is acceptable for local development, but should be marked clearly as development-only.                                                                | suggestion | minor     | open   | Group 6 | Use `.env.example` for local values and avoid presenting hardcoded credentials as production-ready.                                  |
| F-009 | `SETUP-DOC`, `DEV`                                     | The setup guide says to run Docker Compose from the `.devcontainer` directory. The compose file is at repository root, and the devcontainer also references `../docker-compose.yml`. This may confuse setup steps. | defect     | minor     | open   | Group 6 | Align setup instructions with the actual project structure. Clearly state from which directory each command should be executed.      |
| F-010 | `docs/spec/*.md`                                       | Some documentation contains spelling or wording issues, e.g. “recieve”, “persisent”, “spesific”, “performes”, “fromthe”, “Comprehensibiity”.                                                                       | suggestion | editorial | open   | Group 6 | Run a spelling/grammar pass before final submission.                                                                                 |
| F-011 | `TEST`, `BDD`                                          | Good coverage exists for domain models, API behavior, and BDD user flows. Some tests rely on fixed IDs such as `id=1`, which can become fragile as the test setup grows.                                           | suggestion | minor     | open   | Group 6 | Prefer generated IDs from committed objects and store them in context or fixtures.                                                   |

---

## 4. Data Summary (DS)

| Metric                               | Value                                                                                               | Notes                                                                  |
| ------------------------------------ | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Size of review object                | 10+ documentation files, backend source files, unit tests, BDD files, Docker and devcontainer setup | Approximate scope based on reviewed repository content                 |
| Preparation effort (hours, optional) | Approx. 4.00-5.00 total team hours                                                                  | Lightweight technical review for course exercise                       |
| Number of findings (initial)         | 11                                                                                                  | Includes defects, questions, suggestions, and editorial issues         |
| Number of findings after meeting     | 11                                                                                                  | Findings were reduced and consolidated before final documentation      |
| Rework effort (hours, author)        | Not measured                                                                                        | Rework is performed by Group 6 if accepted                             |
| Re-inspection required?              | No                                                                                                  | No blocking issue found; changes can be handled without full re-review |

---

## 5. Review Report (RR)

### 5.1 Summary

We reviewed the ESBot repository of Group 6.  
Our review covered documentation, requirements, specification, data model, backend implementation, unit tests, BDD scenarios, Docker setup, devcontainer setup, and setup instructions.

Overall impression:

- clear project idea and suitable ESBot scope
- good amount of documentation
- backend prototype already implements important flows
- strong use of unit tests and BDD scenarios
- main improvement areas: consistency, maintainability, setup clarity, and separation between API endpoint logic and business logic

### 5.2 Review outcome

- **Review object state after review:** accepted with changes
- **Major risks or themes:**
  - Documentation and implementation are mostly aligned, but some documents should be updated to reflect the current project state.
  - Backend endpoint logic could be separated more clearly from business logic.
  - AI error handling should be checked in `evaluate_answer()`.
  - Some setup/devcontainer instructions may confuse developers.
  - No blocking issue found.

### 5.3 Decisions and follow-up

| Topic                    | Decision                                                                | Responsible | Due date    |
| ------------------------ | ----------------------------------------------------------------------- | ----------- | ----------- |
| Task documentation       | Update task status from “Not Started” to the current state              | Group 6     | Not defined |
| Data model documentation | Add missing `SubmittedAnswer` to `EvaluationResult` relationship        | Group 6     | Not defined |
| API request validation   | Consider Pydantic request models for `/chat` and `/quiz-request`        | Group 6     | Not defined |
| Service separation       | Consider moving endpoint business logic into a service layer            | Group 6     | Not defined |
| AI error handling        | Check `evaluate_answer()` fallback behavior                             | Group 6     | Not defined |
| Setup instructions       | Align `docs/setup.md` with actual Docker Compose and devcontainer paths | Group 6     | Not defined |

### 5.4 Positive observations (optional)

- Clear architecture idea: frontend, backend, database, AI inference.
- Useful Pydantic/SQLModel validation in model classes.
- Unit tests cover many entity validation and relationship cases.
- BDD feature files are readable and describe realistic student flows.
- AI service is mocked in tests, which makes acceptance tests deterministic.
- Docker Compose setup supports reproducible local development.

### 5.5 Lessons learned (optional)

- A technical review is suitable for ESBot because the project contains both documents and implementation artefacts.
- Reviewing documentation and code together helps reveal consistency issues.
- It is useful to separate real defects from future improvement suggestions.
- A respectful review style makes findings easier to accept and discuss.
- For the next review, a smaller checklist per artefact type could make the process faster.

### 5.6 Sign-off

| Role      | Name                                                                   | Signature / date                    |
| --------- | ---------------------------------------------------------------------- | ----------------------------------- |
| Moderator | Sami Goekpinar                                                         | Sami Goekpinar, 2026-05-03          |
| Author    | Melek Goekler, Zeynep Pektas, Truman Zachary Porter, Sena Zeynep Yamak | Not signed; repository-based review |

---

_Comment: Used ChatGPT version 5.3 for translation, wording, grammar, and formatting._
