# 6.4 Story 1.4 Community-Friendly Reporting Stub
**As a** privacy-conscious user  
**I want** the ability to flag suspicious messages for community tracking  
**So that** Prism’s intelligence can grow even before the full reporting workflow ships.

**Acceptance Criteria**
1. `FR4` — UI includes a “Report this scam” affordance that opens a modal/wizard requesting minimal extra context.
2. `FR4` — API route appends reported data to JSON storage with a “pending review” flag.
3. `FR5` — Storage schema differentiates between analyzed submissions and user-reported incidents for later moderation.
4. `NFR3` — Submission sanitization removes personally identifiable information beyond the provided message/number; document assumptions in code comments.
