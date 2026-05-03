# 6.1 Story 1.1 MVP Shell & Submission Flow
**As a** cautious consumer  
**I want** a secure Prism web app with clear input fields for SMS text or phone numbers  
**So that** I can quickly submit suspicious content for analysis without friction.

**Acceptance Criteria**
1. `FR1` — Landing page renders in Next.js, offering separate inputs for SMS body and phone number with validation for empty/invalid submissions.
2. `FR2` — Submission triggers a client-side request to an API route that returns a stubbed risk score payload (e.g., medium risk with placeholder explanation).
3. `FR3` — UI displays the returned score and explanation in an accessible format (WCAG AA color contrast; screen-reader labels).
4. `FR5` — JSON persistence layer (local file) records each submission with timestamp and input type for future analysis.
