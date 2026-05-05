# Static Analysis for ESBot

## Overview

For Exercise 6.3, we selected two different static analysis categories for the ESBot backend:

- **Linter:** `pylint`
- **Type checker:** `mypy`

These two categories were chosen because they are highly relevant for a Python/FastAPI backend with persistence and service-layer logic.

- `pylint` helps detect maintainability and style issues such as formatting problems, overly long lines, missing final newlines, and general code smells.
- `mypy` helps detect type safety issues, which is especially useful in ESBot because the project uses `SQLModel`, optional database IDs, and several service methods that pass model data between persistence and application logic.

Both tools were executed **locally** inside the backend Docker container.  
For this exercise, we used **minimal project-specific configuration** to reduce unnecessary noise while keeping the results useful.

---

## Selected Categories and Tools

| Category     | Tool     | Why it matters for ESBot                                                                                              |
| ------------ | -------- | --------------------------------------------------------------------------------------------------------------------- |
| Linter       | `pylint` | Helps improve readability, maintainability, and code hygiene across backend modules, services, models, and setup code |
| Type checker | `mypy`   | Helps detect type mismatches in service logic and ORM-related code before runtime                                     |

---

## Installation and Local Setup

The tools were added to the backend Python dependencies and executed inside the Docker-based development environment.

### Installed tools

- `pylint`
- `mypy`

### Configuration files

We added two small configuration files to the backend:

- `backend/.pylintrc`
- `backend/mypy.ini`

The goal was to keep the configuration lightweight and practical for the current project stage.

### Configuration choices

#### `pylint`

We disabled some warnings that created a lot of low-value noise for this project stage, especially:

- missing module docstrings
- missing class docstrings
- missing function docstrings
- too few public methods

We kept formatting checks such as line length and final newline checks active.

#### `mypy`

We kept the configuration mostly strict around optional typing, but avoided overly strict settings that would create excessive noise for a student project.  
In particular, we kept optional-type checking active because this is relevant for `SQLModel` IDs and service-layer data flow.

---

## Local Execution Commands

### Run pylint on the backend application code

```bash
docker compose -f docker-compose.dev.yml run --rm backend pylint --rcfile=.pylintrc app
```

### Run mypy on the backend application code

```bash
docker compose -f docker-compose.dev.yml run --rm backend mypy --config-file mypy.ini app
```

---

## Results and Interpretation

## 1. pylint

### Command used

```bash
docker compose -f docker-compose.dev.yml run --rm backend pylint --rcfile=.pylintrc app
```

### Result

After applying the minimal configuration, `pylint` reported a score of:

- **9.12 / 10**

### Main findings

The remaining findings mainly reported:

- missing final newline at end of file
- line length violations
- one helper method with too many positional arguments

### Example findings

- `app/db.py`, `app/main.py`, and several service files miss a final newline
- `app/models/base.py` still contains several long lines
- `QuizItem.create()` still triggers `too-many-positional-arguments`
- `app/services/contextualized_response_service.py` contains one long line

### Evaluation

For ESBot, `pylint` was useful mainly as a **maintainability and style tool**.

It helped reveal:

- formatting issues
- readability problems
- small structure/code-smell issues

Compared to the default run, the configured run was much more useful because it reduced noise from missing docstrings and small service-class warnings.  
This made the remaining output easier to interpret and more relevant for the project.

Most `pylint` findings are **non-blocking**.  
They do not indicate broken functionality, but they highlight areas where the code can become more consistent and easier to maintain.

---

## 2. mypy

### Command used

```bash
docker compose -f docker-compose.dev.yml run --rm backend mypy --config-file mypy.ini app
```

### Result

The `mypy` run reported:

- **6 errors in 3 files**

### Reported issues

#### `app/services/resume_learning_session_service.py`

- `order_by(Message.order)` was flagged because `mypy` interpreted `Message.order` as a plain `int` instead of a SQLAlchemy/SQLModel column expression.

#### `app/services/contextualized_response_service.py`

- `session_entity.id` is typed as `Optional[int]`
- `mypy` therefore reported that `Message.create(session_id=...)` may receive `int | None` instead of `int`

#### `app/services/answer_evaluation_service.py`

- `quiz_item.id` is typed as `Optional[int]`
- `submitted_answer.id` is typed as `Optional[int]`
- `mypy` therefore reported that these values might still be `None` when passed to methods requiring `int`

### Evaluation

For ESBot, `mypy` was very useful because it found **real type-safety weaknesses** in the service layer.

These findings are more important than most of the `pylint` warnings because they affect how safely model IDs are passed between:

- persisted entities
- helper constructors
- service logic

In practice, these IDs are populated after `commit()` and `refresh()`, but this is not statically guaranteed by the current type annotations.  
Therefore, `mypy` correctly points out that the code relies on runtime knowledge that is not visible to the type checker.

This is valuable for ESBot because the backend uses ORM models and service logic heavily, and type mismatches in those areas can easily lead to subtle bugs or weak maintainability.

---

## Usefulness for ESBot

### Why these tools are a good fit

`pylint` and `mypy` complement each other well:

- `pylint` focuses more on **code quality, readability, and maintainability**
- `mypy` focuses more on **type correctness and interface safety**

For ESBot, both are relevant because the backend combines:

- API setup
- persistence with SQLModel
- service-layer logic
- test infrastructure
- AI-related integration boundaries

### Practical usefulness

- `pylint` is good for detecting style issues and general code smells early
- `mypy` is especially useful for model/service interactions and optional IDs

### Noise / false positives

Before configuration, `pylint` produced a lot of low-value warnings such as missing docstrings and warnings for very small service classes.  
With the minimal configuration, the output became much more focused and useful.

`mypy` produced less output overall, but the findings were more meaningful and technically relevant.

---

## Development Impact

Running both tools locally is feasible and useful, but they affect development differently:

- `pylint` provides broad feedback and is helpful for maintainability
- `mypy` gives fewer but more actionable results

For the current ESBot project stage, local execution is appropriate because:

- it keeps the feedback available to developers
- it does not yet force strict compliance during every small change
- it allows the team to decide which findings are worth fixing immediately

At this stage, we would prioritize automating `mypy` earlier than a full strict `pylint` run, because the type checker currently provides more focused and defect-relevant feedback.

---

_Comment: Used ChatGPT for wording, structuring, and summarizing the static analysis results._
