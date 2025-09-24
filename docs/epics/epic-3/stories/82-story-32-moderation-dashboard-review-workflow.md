# 8.2 Story 3.2 Moderation Dashboard & Review Workflow
**As a** product owner/moderator  
**I want** tools to review and approve community reports  
**So that** the intelligence database stays accurate and trustworthy.

**Acceptance Criteria**
1. `FR5` — Build an admin-only Next.js route showing pending reports with search/filter capabilities.
2. `FR5` — Moderation actions (approve, flag, discard) update the JSON data store with audit timestamps.
3. `NFR3` — Protect the admin route with basic authentication guard (e.g., environment-configured token) before merging into Supabase auth later.
4. `NFR2` — Document performance considerations (e.g., pagination) to keep moderation views responsive as dataset grows.
