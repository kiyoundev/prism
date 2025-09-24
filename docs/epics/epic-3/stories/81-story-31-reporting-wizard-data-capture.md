# 8.1 Story 3.1 Reporting Wizard & Data Capture
**As a** vigilant community member  
**I want** a guided reporting experience  
**So that** I can share scam details without worrying about format or sensitive information.

**Acceptance Criteria**
1. `FR4` — Multi-step wizard collects structured details (message text, phone number, scam category, optional notes) with validation and inline masking guidance.
2. `NFR4` — Wizard is responsive (mobile/desktop) and screen-reader friendly, including progress indicators and descriptive labels.
3. `FR5` — Submitted reports append to the JSON data store with schema separating reports vs. analyzed submissions.
4. `NFR3` — Input sanitation strips personal info (e.g., email addresses) before persisting, with notes in code comments.
