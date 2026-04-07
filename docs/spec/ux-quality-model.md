# Exercise 3.2: ISO/IEC 25010 Mapping for UX

This document maps the five core UX factors identified in Exercise 3.1 to the official ISO/IEC 25010 quality characteristics. This ensures that the learning assistant's UX requirements are measurable and testable.

| UX Factor (from 3.1) | ISO 25010 Characteristic | Measurable Quality Criterion | Verification Method |
| :--- | :--- | :--- | :--- |
| **1. Learnability** | **Usability** (Learnability) | 90% of first-time users can successfully send a question and receive a "guided" response (e.g., "Would you like an example?") within 60 seconds. | **Usability Testing:** Direct observation and time-tracking of participants during their first session. |
| **2. Clarity / Comprehensibility** | **Usability** (Appropriateness Recognizability) | 100% of AI explanations must include at least one structured element (bullet points or code blocks) and start displaying within 3.0 seconds. | **Content Audit & Load Test:** Manual review of 20 logs for structure and automated measurement of response latency. |
| **3. Feedback Quality** | **Usability** (Operability / User Error Protection) | 100% of incorrect quiz answers must trigger a corrective explanation (e.g., explaining "why") instead of a simple binary "Wrong" status. | **Qualitative Log Analysis:** Review of interaction history to ensure pedagogical depth in AI-generated feedback. |
| **4. Trust & Transparency** | **Functional Suitability** (Functional Appropriateness) | 100% of AI-generated content must be visually labeled (e.g., "AI-generated") to communicate non-deterministic behavior and uncertainty. | **Expert Review:** Visual inspection of the UI to ensure users can distinguish between verified system facts and AI inference. |
| **5. Error Tolerance & Recovery** | **Reliability** (Fault Tolerance) | 100% of vague inputs or service timeouts must result in a clarifying prompt or a recovery message instead of a technical error (HTTP 500). | **Negative Testing:** Simulating "gibberish" inputs and backend service crashes to verify the system's "graceful" recovery UI. |

---

## Rationale for Metric Thresholds

To ensure the quality requirements are grounded in industry standards and pedagogical needs, the following rationale is applied:

* **90% Success Rate (Learnability):** Derived from the *Nielsen Norman Group* benchmarks. For a "supplementary tool," immediate success is required to prevent user churn.
* **3.0 Seconds Latency (Clarity/Efficiency):** Based on the *Doherty Threshold*. Delays in AI responses break the conversational "clarity" and lead to a loss of focus during the learning process.
* **Pedagogical Feedback (Feedback Quality):** Binary feedback (True/False) is insufficient for "mental model updates." Therefore, a 100% requirement for corrective explanations is set.
* **100% Transparency (Trust):** Due to the "non-deterministic nature" of LLMs, strict labeling is required to manage student trust and prevent the learning of misinformation.
* **Zero Technical Errors (Error Tolerance):** To maintain "Reliability," the system must mask technical stack traces with actionable guidance to ensure a smooth "recovery."

---

## Verification Approach Summary

To fulfill the "reviewable quality expectations" defined in the project constitution, we utilize:
1.  **Empirical Tests:** Quantitative measurements (Success Rates) during user sessions.
2.  **Technical Audits:** Automated benchmarks for performance and "Fault Injection" (Negative Testing).
3.  **Qualitative Review:** Expert audits of the AI’s pedagogical feedback and UI transparency markers.