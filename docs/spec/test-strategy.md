# Test Strategy for ESBot

## Introduction

This document outlines the test strategy for ESBot, defining the roles and execution patterns for unit tests and BDD/acceptance tests within the CI pipeline.

---

## Types of Tests

### Unit Tests

| Aspect | Description |
|--------|-------------|
| **Scope** | Individual components, functions, and classes in isolation |
| **Purpose** | Verify that each unit works correctly in isolation |
| **Execution Time** | Fast (milliseconds per test) |
| **Dependencies** | Mocks/stubs for all external dependencies |
| **Location** | `backend/tests/unit_tests/` |
| **Framework** | pytest |

### BDD/Acceptance Tests

| Aspect | Description |
|--------|-------------|
| **Scope** | End-to-end user workflows and feature behavior |
| **Purpose** | Verify that the system delivers value from a user perspective |
| **Execution Time** | Slower (seconds to minutes per scenario) |
| **Dependencies** | Mock AI provider, test database |
| **Location** | `backend/features/` |
| **Framework** | behave (Gherkin) |

---

## Key Differences

| Dimension | Unit Tests | BDD/Acceptance Tests |
|-----------|------------|---------------------|
| **What they test** | How something works | What the system does |
| **Perspective** | Developer | User/Business |
| **Failure impact** | Component-level bug | Feature not working |
| **Test Instability** | Low (isolated) | Higher (integrated) |
| **Debugging** | Easy (isolated failure) | Complex (multiple layers) |

---

## Execution Strategy

### Recommended CI Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    CI Pipeline Execution                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Commit/Push                                                 │
│         │                                                       │
│         ▼                                                       │
│  2. Unit Tests (Every Commit)                                   │
│     • Fast feedback                                             │
│     • Run in parallel                                           │
│     • Block merge if failing                                    │
│         │                                                       │
│         ▼                                                       │
│  3. BDD Tests (Pull Request)                                    │
│     • PR: Full suite                                            │
│                                                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Execution Frequency

| Trigger | Unit Tests | BDD Tests |
|---------|------------|-----------|
| Every commit | Yes | No |
| Pull Request | Yes | Yes |
| Merge to main | Yes | Yes |
| Release | Yes | Yes |

---

## Rationale

### Why Unit Tests Run on Every Commit

1. **Speed**: Unit tests execute in seconds, providing immediate feedback
2. **Isolation**: Failures are easy to locate and fix
3. **Frequency**: Developers commit frequently; fast feedback is essential
4. **Coverage**: High coverage catches regressions early

### Why BDD Tests Don't Run on Every Commit

1. **Execution Time**: BDD tests involve more components and take longer
2. **Resource Cost**: Requires database, mock AI, and more setup
3. **Flakiness**: More integration points increase transient failure risk
4. **Value Proposition**: BDD tests validate user workflows, which don't change as frequently as implementation details

### Recommended Approach for ESBot

**Unit Tests**: Run on every commit and pull request
- Fast feedback loop
- Catches implementation bugs early
- Blocks broken code from entering the codebase

**BDD Tests**: Run on pull requests and nightly builds
- Validates user-facing functionality
- Ensures features work end-to-end
- Catches integration issues that unit tests miss

---

## AI Mockability Impact

### Why Mock AI Makes BDD Tests Feasible in CI

1. **Deterministic Output**: Mock AI returns predictable responses, making tests repeatable
2. **No External Dependencies**: Tests don't rely on external API availability or rate limits
3. **Fast Execution**: No network latency or AI inference time
4. **Controlled Scenarios**: Can test edge cases that would be difficult to trigger with real AI

### Without Mock AI

- Tests would be non-deterministic (AI responses vary)
- Dependent on external service availability
- Slow execution (network + inference time)
- Difficult to test error scenarios reliably

### With Mock AI (ESBot Approach)

```
┌──────────────────┐      ┌──────────────────┐
│   BDD Scenario   │─────▶│   Mock AI        │
│   (Gherkin)      │      │   Provider       │
└──────────────────┘      └──────────────────┘
         │                        │
         ▼                        ▼
┌──────────────────┐      ┌──────────────────┐
│ Step Definitions │      │ Returns:         │
│                  │      │ - Quiz questions │
│                  │      │ - Evaluation     │
│                  │      │ - Explanations   │
└──────────────────┘      └──────────────────┘
```



## Summary

| Test Type | When to Run | Why |
|-----------|-------------|-----|
| Unit Tests | Every commit | Fast feedback, catches implementation bugs |
| BDD Tests | PR | Validates user workflows, integration correctness |
| Both | Before merge | Ensures quality and functionality |

The separation allows the team to get rapid feedback on code changes while still validating that the system works as a whole from the user's perspective.