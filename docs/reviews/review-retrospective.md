# Review Retrospective

## 1. What worked well?

Overall, the review process worked well for us because the technical review gave us a clear structure without becoming too formal for the course project. We could divide the work between documentation, requirements, backend code, tests, BDD scenarios, and setup files. This made the review more focused and helped us avoid only looking at the implementation.

What worked especially well was reviewing documentation and code together. Some points only became visible because we compared the written artefacts with the actual implementation. For example, the backend already contained implemented functionality, tests, Docker setup, and BDD scenarios, while some planning documents still described tasks as not started or future-oriented. Without comparing both sides, this kind of consistency issue would have been easy to miss.

The course template was also helpful because it forced us to document findings in a structured way. Using fields such as location, type, severity, status, owner, and notes helped us keep the feedback objective. It also made it easier to separate real defects from questions and improvement suggestions. This was important for us because we wanted to give useful feedback without being too harsh toward the reviewed group.

## 2. What was difficult?

The most difficult part was deciding how strict the review should be. ESBot is still a course prototype, so not every missing detail should be treated as a serious defect. Some points are clearly future improvements rather than current problems. For that reason, we tried to use mostly minor severity levels and only mark findings as major when they could affect maintainability or error handling in an important way.

It was also challenging to review artefacts that describe future goals. Some documentation describes a complete system with frontend, monitoring, source-grounded AI responses, security goals, and quality metrics. The current implementation focuses mainly on the backend, persistence, AI integration, tests, and BDD scenarios. This is understandable for an iterative project, but it made the review more difficult because we had to distinguish between planned functionality and already implemented functionality.

## 3. Are formal reviews suitable for our team?

Yes, formal or semi-formal reviews are suitable for our team, especially for artefacts that define important project decisions. For our ESBot work, we would use this kind of review again for requirements, specifications, architecture documents, data models, API contracts, and test strategies.

For documentation and specifications, reviews are useful because unclear requirements can later lead to wrong implementation decisions. A structured review helps us check whether requirements are understandable, measurable, and consistent with the system scope.

For design and data model artefacts, reviews are also valuable because they reveal whether relationships, responsibilities, and boundaries are clear before too much code is written. This is especially relevant for ESBot because the system combines backend logic, persistence, AI integration, and tests.

For code, we would use a lighter version of the review process. A full inspection would probably be too time-consuming for every small change. However, a technical review is useful for important backend modules, API endpoints, AI service boundaries, database models, and test infrastructure. These areas affect maintainability and reliability and therefore benefit from structured feedback.

## 4. One concrete improvement for the next review round

For the next review round, we would prepare a smaller checklist before starting the review. The checklist should be separated by artefact type, for example:

- documentation and requirements: clarity, consistency, testability, measurable goals
- architecture and data model: separation of concerns, relationships, persistence strategy
- backend code: validation, error handling, service separation, maintainability
- tests and BDD: coverage of main flows, deterministic mocks, clear setup and cleanup
- setup files: reproducibility, Docker commands, environment variables, devcontainer paths

This would make the review faster and more consistent. It would also help each reviewer focus on the same quality criteria instead of relying only on individual interpretation. In addition, we would try to schedule a short clarification exchange with the reviewed group if something important is unclear.

---

_Comment: Used ChatGPT version 5.3 for translation, wording, grammar, and formatting._
