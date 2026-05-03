# 7.1 Story 2.1 Narrative Risk Explanations & Transparency
**As a** skeptical user  
**I want** to understand why Prism labeled my message as risky  
**So that** I can trust the recommendation and take appropriate action.

**Acceptance Criteria**
1. `FR2` — API augments risk payloads with structured factors (rule hits, AI indicators) and exposes them to the UI.
2. `FR3` — UI renders a human-readable explanation that references the specific signals contributing to the score.
3. `NFR4` — Explanations support screen readers with semantic markup and ARIA labels describing confidence levels.
4. `NFR1` — Added reasoning does not push response time above three seconds; log slow cases.
