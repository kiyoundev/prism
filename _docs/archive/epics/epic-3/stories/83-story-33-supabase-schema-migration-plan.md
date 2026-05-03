# 8.3 Story 3.3 Supabase Schema & Migration Plan
**As a** technical lead  
**I want** a clear plan for moving from JSON persistence to Supabase  
**So that** we can scale storage and analytics without disrupting users.

**Acceptance Criteria**
1. `FR5` — Define Supabase schema (tables for submissions, reports, moderation actions) with column types and indexes reflecting current JSON structure.
2. `NFR2` — Provide a migration checklist covering data export/import, environment setup, and fallback strategy for downtime.
3. `NFR3` — Specify access controls (service roles, row-level policies) required to preserve user privacy.
4. `FR6` — Document how AI integration keys and logs will be stored securely in Supabase, including environment variable mapping.
