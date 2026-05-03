# 7.4 Story 2.4 Safety Education & Knowledge Hooks
**As someone** who wants to avoid future scams  
**I want** relevant safety tips when I get a result  
**So that** I learn how to recognize similar threats.

**Acceptance Criteria**
1. `FR3` — Introduce a dynamic “Safety Tips” panel that maps risk tiers and scam categories to educational content.
2. `FR2` — Tips pull from a JSON-driven knowledge base that is versioned and editable for later expansion.
3. `NFR2` — Lazy-load or cache tips to avoid slowing down the primary analysis response.
4. `NFR4` — Tips include clear headings, bullet lists, and optional links with accessible descriptions.
