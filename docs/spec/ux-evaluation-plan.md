# UX Evaluation Plan for ESBot

## 1. Purpose

This document defines a compact UX evaluation plan for ESBot that we can realistically execute within our team.

Our goal is not only to check whether ESBot works technically. We also want to verify whether students can use it in a clear and supportive way. Since ESBot is an AI-supported learning assistant, good UX means more than a clean interface. It also means understandable explanations, meaningful feedback, visible AI transparency, and graceful recovery when something goes wrong.

---

## 2. Evaluation Scope

### 2.1 UX Factors

The evaluation focuses on the UX factors already defined in Exercise **3.2**.

**Learnability**  
We want first-time users to understand ESBot quickly. A student should be able to open the application, send a first question, and receive a guided response without training.

**Clarity / Comprehensibility**  
We want AI explanations to be easy to follow and clearly structured. Users should not only receive an answer, but also understand it without unnecessary effort.

**Feedback Quality**  
We want the system to provide meaningful feedback, especially when a user gives an incorrect quiz answer. The feedback should help the user understand the mistake instead of only marking the answer as wrong.

**Trust & Transparency**  
We want users to clearly recognize which content is AI-generated. The interface should communicate uncertainty and non-deterministic behavior in a visible and trustworthy way.

**Error Tolerance & Recovery**  
We want unclear inputs, service failures, or timeouts to be handled gracefully. If something goes wrong, users should receive a clarifying or recovery message instead of a technical error.

### 2.2 User Journeys

We test these user journeys because they represent the core experience of ESBot:

**Journey 1: Start a first interaction**  
The user opens ESBot, sends a first course-related question, and receives a guided response.

**Journey 2: Read and understand an explanation**  
The user reads an AI-generated explanation and checks whether the answer is clearly structured and understandable.

**Journey 3: Receive corrective feedback**  
The user answers a quiz question incorrectly and receives a corrective explanation that helps them understand the mistake.

**Journey 4: Understand the response source**  
The user reads the interface and can distinguish AI-generated content from system-level UI messages.

**Journey 5: Handle unclear input or failure**  
The user enters a vague input or encounters a timeout and receives a clarifying or recovery message instead of a technical error.

---

## 3. Method Set

We use a small but balanced method set so that the evaluation is realistic for our team and still strong enough to support reviewable UX decisions.

### 3.1 Heuristic Evaluation

Before involving participants, we review ESBot ourselves based on basic usability principles. We check whether labels are clear, explanations are structured, feedback is understandable, and interface elements are used consistently.

This helps us detect obvious issues early and reduces the risk of wasting user sessions on problems we could have identified ourselves.

### 3.2 Cognitive Walkthrough

We go through the most important tasks from the perspective of a first-time student user. We ask simple but important questions such as:

- Would a new user know what to do here?
- Is the next step visible and understandable?
- Would the user understand the response or feedback?
- Would the user notice if something went wrong?

This method is especially useful for the first-question flow because this is the user's first contact with ESBot. At this point, the user must understand the purpose of the system, recognize how to start the interaction, and feel confident that the first step is clear and meaningful. If this entry point is confusing, the overall learning experience is weakened from the beginning.

### 3.3 Think-Aloud Sessions

We ask representative users to complete short, realistic tasks while speaking out loud about what they think, expect, and find confusing.

This helps us identify hidden UX problems such as hesitation, uncertainty, or misunderstanding. It is especially useful for ESBot because conversational AI can feel technically functional while still being unclear or untrustworthy to the user.

### 3.4 Post-Session Questionnaire

After each session, participants complete a short questionnaire. We use a compact post-session questionnaire to capture how clear, helpful, and trustworthy the interaction felt from the user’s perspective.

We may also add a few short open questions to better understand the user’s personal impression, for example:

- What felt unclear?
- What felt helpful or unhelpful?
- What felt trustworthy or untrustworthy?
- What would you improve first?

---

## 4. Participants and Setup

### 4.1 Participants

We plan to test with **5-8 participants**. For a compact usability evaluation, this is a suitable range. It usually provides enough observations to identify repeated UX problems while still being feasible for a small team to conduct and evaluate.

The participants should:

- belong to the general student target group of ESBot
- not need deep technical knowledge of the implementation
- ideally represent first-time or light returning users

Each session is conducted by **two team members**:

- one moderator
- one observer and note-taker

### 4.2 Session Duration

Each session should take about **30-40 minutes**.

A practical structure is:

- 5 minutes introduction
- 20-25 minutes guided task execution
- 5-10 minutes debrief and questionnaire

This is long enough to collect useful observations, but short enough to remain realistic for our team.

### 4.3 Materials and Test Environment

We use a simple and reproducible setup:

- ESBot running in a browser
- laptop or desktop test device
- prepared scenarios
- observation sheet
- timer
- post-session questionnaire
- optional notes for open feedback

Where useful, we also collect:

- task completion status
- time to first guided response
- visible hesitation or confusion
- perceived structure of explanations
- quality of corrective feedback
- clarity of AI labels and recovery messages
- short user quotes

### 4.4 Additional Technical Checks

Because some criteria from **3.2** are system-level and not only user-observation-based, we also include technical checks as part of the evaluation package:

- **Content audit** for structured explanations
- **Load testing** for response start latency
- **Qualitative log analysis** for corrective quiz feedback
- **Expert review** for AI-generated content labels
- **Negative testing** for vague inputs and timeout recovery

This keeps the plan aligned with the architecture-aware and testable quality expectations defined in the task.

---

## 5. Metrics and Acceptance Criteria

The following metrics define how we judge the UX results of the evaluation in practice. They translate our quality expectations into concrete acceptance rules for the tested ESBot flows.

| Evaluation Area              | What We Measure                                                                                                       | Acceptance Rule                                                                                                  |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| First interaction            | Whether first-time users can send a question and receive a guided response within 60 seconds                          | At least 90% of participants succeed                                                                             |
| Explanation clarity          | Whether AI explanations include at least one structured element and begin quickly enough to support the learning flow | In all tested cases, explanations include at least one structured element and start within 3.0 seconds           |
| Corrective feedback          | Whether incorrect quiz answers trigger a corrective explanation instead of a simple wrong status                      | In all tested quiz-error cases, the system provides a corrective explanation                                     |
| Trust and transparency       | Whether users can clearly identify AI-generated content and distinguish it from system messages                       | In all tested flows, AI-generated content is clearly labeled                                                     |
| Error tolerance and recovery | Whether vague inputs, service failures, or timeouts result in a clarifying or recovery message                        | In all tested failure cases, the user receives a clarifying or recovery message instead of a raw technical error |
| Open findings                | Whether severe UX issues remain after the evaluation                                                                  | No critical issue may remain open before release                                                                 |

### 5.1 Why these criteria fit ESBot

These criteria fit ESBot because they reflect the most important expectations for a student-facing AI learning assistant. Users should be able to start quickly, understand explanations, receive helpful feedback, recognize AI-generated content, and recover from unclear inputs or technical failures without confusion.

Together, these criteria give us a practical basis for judging whether ESBot is not only functional, but also understandable and usable in a real learning context.

---

## 6. Findings Template

We document all UX findings in a structured way so that the results are easy to discuss, assign, and act on.

| Field             | Description                                                                                                       |
| ----------------- | ----------------------------------------------------------------------------------------------------------------- |
| ID                | Unique identifier of the finding                                                                                  |
| User Journey      | The journey in which the issue occurred                                                                           |
| UX Factor         | Learnability / Clarity & Comprehensibility / Feedback Quality / Trust & Transparency / Error Tolerance & Recovery |
| Issue Description | What happened and why it is relevant                                                                              |
| Severity          | Critical / Major / Minor                                                                                          |
| Evidence          | Observation, quote, timing data, test result, or questionnaire result                                             |
| Recommendation    | Concrete proposal for improvement                                                                                 |
| Owner             | Team member responsible for follow-up                                                                             |
| Status            | Open / In Progress / Resolved                                                                                     |

### Severity Definition

**Critical**  
The issue blocks a core task, breaks trust significantly, or violates a defined acceptance criterion in a release-relevant way.

**Major**  
The issue does not fully block the task, but it clearly harms usability, creates confusion, or weakens an important learning interaction.

**Minor**  
The issue is noticeable and should be improved, but users can still complete the task without major difficulty.

---

## 7. Quality Gate Proposal

UX findings should influence release readiness directly.

A release is **blocked** if one of the following conditions is true:

- the learnability criterion is not met
- explanations do not start within 3.0 seconds or lack structured presentation
- incorrect quiz answers do not trigger corrective explanations
- AI-generated content is not clearly labeled
- vague inputs, timeouts, or failures result in raw technical errors instead of clarifying or recovery messages
- at least one **critical** UX finding remains unresolved

A release may proceed if:

- all measurable acceptance criteria are met
- no critical findings remain open
- remaining major or minor issues are documented, understood, and accepted by the team

---

## 8. Alignment with Quality Requirements and Constitution Principles

The acceptance criteria in this plan are aligned with the ISO/IEC 25010-based quality model from Exercise **3.2**, especially in the areas of usability, functional suitability, and reliability.

They also reflect the constitution principles of the project:

- **Testability**, because each criterion is measurable through observation, timing, review, or testing
- **Architecture-aware contracts**, because the evaluation includes frontend interaction as well as explanation structure, AI labeling, and recovery behavior
- **Reviewable quality expectations**, because all thresholds are explicit and can be checked in a structured team evaluation

---

## 9. Execution Summary

We consider the UX evaluation complete when:

- heuristic evaluation has been performed
- cognitive walkthrough has been documented
- 5-8 representative users have completed the scenario-based think-aloud sessions
- post-session questionnaires have been collected and reviewed
- technical checks for explanation structure, latency, corrective feedback, labeling, and recovery behavior have been completed
- findings have been documented with severity and recommendation
- the release decision has been made based on the quality gate

---
