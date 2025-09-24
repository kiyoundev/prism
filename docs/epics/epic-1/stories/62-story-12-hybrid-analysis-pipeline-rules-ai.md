# 6.2 Story 1.2 Hybrid Analysis Pipeline (Rules + AI)
**As a** worried user  
**I want** Prism to evaluate suspicious inputs against known patterns and AI heuristics  
**So that** I receive a trustworthy risk score grounded in both rules and intelligent analysis.

**Acceptance Criteria**
1. `FR6` — Backend integrates with a configurable AI API client (mocked via environment variables) to classify risk based on input content.
2. `FR5` — Keyword/number rule engine matches submissions against the JSON database, capturing rule hits alongside AI responses.
3. `FR2` — API route merges rule hits and AI output into a single risk score (0–100) plus human-readable explanation.
4. `NFR1` — Pipeline responds within three seconds under normal load; include logging to surface slow requests.
