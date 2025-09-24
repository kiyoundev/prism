# 2. Requirements

## 2.1 Functional Requirements
1. **FR1:** The system must accept either an SMS text body or phone number input and run a scam analysis workflow on each submission.
2. **FR2:** The system must return a numerical risk score with an accompanying plain-language explanation for every analyzed input.
3. **FR3:** The system must surface recommended user actions (e.g., block, ignore, report) tailored to the analysis outcome.
4. **FR4:** The system must allow users to report suspected scams, storing the message/number in the shared database for future detection.
5. **FR5:** The system must cross-check submissions against a maintained database of known scam keywords and phone numbers.
6. **FR6:** The system must integrate with at least one external AI API to enrich scam detection beyond static rules.

## 2.2 Non-Functional Requirements
1. **NFR1:** Each analysis request must complete in under three seconds to maintain a responsive user experience.
2. **NFR2:** The platform must scale to handle high concurrent usage and an expanding scam-report database with minimal performance degradation.
3. **NFR3:** All user-submitted data and third-party API interactions must be secured in transit and at rest, complying with privacy best practices.
4. **NFR4:** The user interface must be intuitive and accessible for non-technical and vulnerable users while supporting power users.
5. **NFR5:** The codebase must be modular and well-documented so the development team can iterate quickly on new detections or integrations.
