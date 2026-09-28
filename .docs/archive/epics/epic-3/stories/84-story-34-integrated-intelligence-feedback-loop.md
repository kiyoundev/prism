# 8.4 Story 3.4 Integrated Intelligence Feedback Loop
**As a** curious contributor  
**I want** to see how my report helps the community  
**So that** I feel rewarded for participating.

**Acceptance Criteria**
1. `FR5` — Approved reports update the detection pipeline (e.g., keywords, phone numbers) with timestamps for when they become active.
2. `FR2` — Risk explanations highlight when a new report influenced the analysis (e.g., “Community report from 2 days ago flagged this number”).
3. `FR3` — UI sends an optional success confirmation (email/stubbed notification) summarizing how the report will be used.
4. `NFR1` — Pipeline maintains sub-three-second response times even with expanded datasets; add caching or batching as needed.
