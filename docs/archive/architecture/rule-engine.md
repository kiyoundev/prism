# Rule-Based Scam Detection Engine

## Overview
- **Purpose**
  Describe the rule engine that detects fraudulent messages using curated patterns sourced from Supabase.
- **Audience**
  Engineers integrating ingestion pipelines, operations teams maintaining rule quality, and product stakeholders.
- **Context**
  Rules are currently curated in Markdown form at `data/rules/known-scams.md` and will be migrated into Supabase tables for runtime consumption.

## Scope & Goals
- **Detect** suspicious SMS/email payloads using deterministic pattern matching and metadata checks.
- **Ship** an API surface consumable by the Prism web app and automation workflows.
- **Enable** non-engineering contributors to author rules with review/approval before promotion to production.

### Non-Goals
- Machine-learning classification or anomaly detection (covered by future phases).
- Automated rule generation from unlabeled corpora.

## High-Level Architecture
```mermaid
document
    direction TB
    %% Sources
    subgraph Authoring
        md[Markdown rule specs `data/rules/known-scams.md`]
        git[Git Changes / Pull Requests]
    end

    md --> pipeline[Rule Publishing Pipeline]
    pipeline --> supabase[(Supabase Postgres: `public.rules`)]

    subgraph Runtime
        ingestion[Supabase Edge Function: `ingest_message`]
        cache[Rule Cache Service]
        engine[Rule Evaluation Service]
        decision[Decision API]
    end

    supabase --> cache
    ingestion --> engine
    cache --> engine
    engine --> decision
    decision -->|alerts| bus[(Event Bus / Webhooks)]
    decision -->|UI| app[Next.js App]
```

## Component Responsibilities
- **Rule Publishing Pipeline**
  Converts Markdown entries into normalized JSON, validates schema, and upserts into Supabase.
- **Supabase `public.rules` table**
  Authoritative store for active rules with metadata (category, patterns, tags, Unicode flags).
- **Rule Cache Service**
  Pulls latest rules from Supabase, applies sanity checks (duplicate pattern detection, regex compilation), and exposes in-memory snapshot to evaluation workers. Refresh interval configurable (default 60 s) with manual bust endpoint.
- **Rule Evaluation Service**
  Stateless service that accepts a message payload plus optional metadata (channel, locale, source). Evaluates rules in priority order and returns match results with explanations.
- **Decision API**
  Provides REST endpoints for external consumers (web app, automations). Handles rate limiting, authorization, and response normalization.
- **Event Bus / Webhooks**
  Emits detection events to downstream systems (notifications, case management, analytics).

## Data Model (Supabase)
- **`public.rules`**
  - `id` (uuid), `slug` (text, unique)
  - `title`, `category`, `severity`
  - `pattern_list` (jsonb array of tokens / regex snippets)
  - `message_template` (text) for reference/testing
  - `tags` (text[])
  - `notes`, `attachments` metadata
  - `unicode_flags` (jsonb) capturing homoglyph or zero-width usage
  - `status` (enum: draft, active, retired)
  - `version` (int), `created_at`, `updated_at`, `published_at`
- **`public.rule_sources`** (optional)
  - Links Markdown source commit SHA and section anchor to rule `id` for auditability.
- **`public.detections`**
  - Records evaluated messages: payload hash, matched rule IDs, decision outcome, latency metrics, actor metadata.

## Rule Authoring Workflow
- **Create / Update** rules in Markdown with the canonical schema found in `data/rules/known-scams.md`.
- **Validate** using CLI script `pnpm rules:validate` (planned) to ensure required fields and pattern rules.
- **Publish** via CI job that parses Markdown, emits `rules.json`, and calls Supabase admin API to upsert entries.
- **Review**: pull request review enforces QA checklist (duplicate detection, pattern conflicts, domain verification).
- **Rollbacks**: previous versions kept in Supabase; pipeline can demote or retire rules by toggling `status`.

## Runtime Evaluation Flow
1. **Message Intake**
   - API receives message payload (`content`, `channel`, `metadata`).
   - Hash and store minimal payload for traceability (PII stripped or encrypted at rest).
2. **Rule Snapshot Fetch**
   - Engine retrieves latest cached rules; if cache is stale or empty, fetch from Supabase with ETag-based diff.
3. **Normalization**
   - Normalize text (lowercase, remove zero-width chars, decode HTML entities) while keeping original for audit.
   - Extract features: URLs, phone numbers, keywords.
4. **Pattern Matching**
   - Evaluate deterministic checks in order: token inclusion, regex, domain allowlist/denylist, Unicode heuristics.
   - Short-circuit on first critical match; accumulate secondary matches for explainability.
5. **Decision & Response**
   - Return structured response `{ decision: 'flagged' | 'allowed', matches: [...], explanations: [...] }`.
   - Emit detection event to downstream queue/webhook when decision is `flagged`.

## Operational Considerations
- **Scaling**
  - Engine runs as Supabase Edge Function (latency-sensitive) and optional long-lived Node.js workers for bulk jobs.
  - Rule cache uses in-memory store with horizontal scaling supported by periodic sync from Supabase.
- **Monitoring**
  - Capture metrics: evaluation latency, match counts per rule, false-positive feedback loops.
  - Alert on cache refresh failures or rule sync errors.
- **Security**
  - Rules stored in Supabase with row-level security restricting write access to CI service role.
  - Detection API protected by service tokens; enforce per-client rate limits.
- **Auditability**
  - Store decision logs referencing rule version and providing redacted payload snippet.
  - Maintain link from detection to source Markdown commit for traceability.

## Dependencies & Integrations
- **Supabase Postgres** for rule storage and detection logging.
- **Next.js App** (`src/app/known-scams/page.tsx`) consumes Decision API for UI classification.
- **Supabase Storage** for hosting reference attachments (screenshots) referenced in rules.

## Risks & Mitigations
- **Rule Drift**: Introduce weekly QA reviews; automated regression suite ensures high-signal rules remain active.
- **Unicode & Encoding Variants**: Normalization pipeline with tests covering homoglyph examples from `known-scams.md`.
- **Publishing Gaps**: CI pipeline fails when Markdown schema changes are detected without corresponding migration.

## Open Questions
- What latency SLA is required for real-time detection (e.g., <100 ms)?
- Should bulk historical replays be supported (requires asynchronous job runner)?
- Does the engine need to support multi-language content immediately?

## Next Steps
- Create Supabase migrations for `public.rules` and `public.detections` tables.
- Implement Markdown-to-Supabase publishing script in `scripts/`. 
- Prototype Edge Function for message evaluation and integrate with web app submission flow.
- Define monitoring dashboards and alert thresholds.
