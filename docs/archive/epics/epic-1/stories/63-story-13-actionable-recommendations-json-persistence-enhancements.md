# 6.3 Story 1.3 Actionable Recommendations & JSON Persistence Enhancements
**As someone** evaluating scammers  
**I want** clear guidance on what to do about a suspicious message  
**So that** I can take safe next steps without second-guessing.

**Acceptance Criteria**
1. `FR3` — API route maps risk tiers (low/medium/high) to tailored suggested actions (e.g., “block number,” “delete message,” “report to carrier”).
2. `FR5` — JSON data store captures the calculated risk score, explanation, and suggested actions for each submission.
3. `FR2` — UI displays suggested actions alongside the score, with expandable detail for the reasoning that led to them.
4. `NFR4` — Recommended actions are accessible (semantic markup, focus order, responsive layout) per UI design goals.
