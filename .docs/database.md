## Core Runtime Tables

### messages
Stores every SMS that enters Prism—seed scams, seed legit, and user submissions. Acts as the authoritative record for downstream scoring and UI retrieval. When payloads are non-textual (screenshots, MMS), store any OCR output in `text` (even if blank) and capture ingestion details in `metadata` (e.g., `{"has_image": true, "ocr_confidence": 0.42}`) so the rule engine can still operate on normalized data.
| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | Stable identifier shared across services |
| `created_at` | `TIMESTAMPTZ` NOT NULL DEFAULT `now()` | Initial ingestion timestamp |
| `text` | `TEXT` NOT NULL | Raw SMS body exactly as submitted |
| `source` | `TEXT` NOT NULL CHECK in (`'seed_scam'`, `'seed_legit'`, `'user_submitted'`) | Tracks provenance/origin |
| `label` | `TEXT` NOT NULL CHECK in (`'scam'`, `'legit'`, `'unknown'`) | Ground-truth or moderation outcome |
| `category` | `TEXT` NULL | High-level topic (delivery, banking, tax, etc.) set by Phase 0 at persist time. **v2 note:** if re-scoring is introduced, consider moving to `message_analysis` so each run has its own category. |
| `metadata` | `JSONB` NULL | Free-form attributes (channel, sender, etc.) |

Indexes:
- `INDEX (source)`
- `INDEX (label)`
- `INDEX (created_at DESC)`

### message_analysis
Captures every scoring run for a message so you retain rule/ML outputs, explanations, and model version history. Multiple rows can exist per message as models evolve. Every row is complete — the pipeline is fail-fast, so a partial row is never persisted.

`rule_reasons` uses a fixed-key object shape regardless of what fired: `{"brand_match": 0.0, "url_suspicious": 1.0, "unicode_obfuscation": 0.0, "urgency_pattern": 0.8, ...}`. All keys always present; zero means the signal didn't fire. This keeps Phase 2 feature extraction deterministic — no array iteration or missing-key handling needed.

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | Unique per analysis run |
| `message_id` | UUID NOT NULL REFERENCES `messages(id)` ON DELETE CASCADE | Links back to the source message |
| `rule_score` | `NUMERIC` NOT NULL CHECK (0–1) | Phase 1 deterministic score |
| `rule_reasons` | `JSONB` NOT NULL | Fixed-key object — all Phase 1 signal scores, zero if not fired |
| `ml_score` | `NUMERIC` NULL CHECK (0–1) | Phase 2 similarity/model score; NULL if classifier not yet trained |
| `ml_details` | `JSONB` NULL | TF-IDF feature weights, sentiment score |
| `ai_score` | `NUMERIC` NOT NULL CHECK (0–1) | Phase 3 Claude score — NOT NULL; fail-fast if Claude unavailable |
| `ai_explanation` | `TEXT` NOT NULL | Plain-English explanation from Claude — NOT NULL; always produced with `ai_score` |
| `final_score` | `NUMERIC` NOT NULL CHECK (0–1) | Weighted combiner result |
| `model_version` | `TEXT` NOT NULL | Git SHA from `MODEL_VERSION` env var; `"dev"` for local runs |
| `runtime_flags` | `JSONB` NOT NULL | Combiner weights used for this run: `{"rule_weight": 0.4, "ml_weight": 0.3, "ai_weight": 0.3}` |
| `created_at` | `TIMESTAMPTZ` NOT NULL DEFAULT `now()` | When the analysis completed |

Indexes:
- `INDEX (message_id, created_at DESC)` to fetch the latest analysis quickly
- `INDEX (model_version)`

### Optional: message_links
If you need to query extracted URLs separately, persist them in a dedicated table.

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | |
| `message_id` | UUID NOT NULL REFERENCES `messages(id)` ON DELETE CASCADE | Links back to the source message |
| `display` | `TEXT` NOT NULL | Original snippet from the SMS |
| `href` | `TEXT` NOT NULL | Normalized URL |
| `kind` | `TEXT` NULL | Optional tag (shortener, banking, etc.) |
| `created_at` | `TIMESTAMPTZ` NOT NULL DEFAULT `now()` | |

Use this table only if you need link-level analytics; otherwise links can remain inside `message_analysis.rule_reasons`.

### Optional: message_attachments
For screenshots or MMS payloads, persist each attachment separately so you can run OCR, deduplicate by hash, and reference files later.

| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | |
| `message_id` | UUID NOT NULL REFERENCES `messages(id)` ON DELETE CASCADE | Links back to the source message |
| `kind` | `TEXT` NOT NULL | e.g., `image`, `audio`, `pdf` |
| `mime_type` | `TEXT` NOT NULL | `image/jpeg`, `image/png`, etc. |
| `storage_key` | `TEXT` NOT NULL | Path or object key in blob storage |
| `sha256` | `TEXT` NOT NULL | Strong hash for exact dedupe |
| `phash` | `TEXT` NULL | Optional perceptual hash for fuzzy matching |
| `extracted_text` | `TEXT` NULL | OCR output (blank if not available) |
| `metadata` | `JSONB` NULL | Dimensions, OCR confidence, annotations |
| `created_at` | `TIMESTAMPTZ` NOT NULL DEFAULT `now()` | |

Use this table whenever the raw `messages.text` field can’t represent the payload (image-only scams, multi-part MMS, attachments needed for ML training).

> These tables form the MVP Postgres footprint required for Stage 1: store every message once, track each scoring run with explanations, and optionally persist extracted links and attachments.


---

## Pipeline Read/Write Map

When each table is touched across the full request lifecycle.

```
User submits SMS
    │
    ├── [Issue #36] READ message_analysis — SHA-256 dedup check before Phase 3
    │
    ├── Phase 0 → Phase 1 → Phase 2 → Phase 3 → Combiner   ← DB not touched
    │
    └── MessageRepository.save()
            WRITE messages          (one row)
            WRITE message_analysis  (one row, same transaction)
            [WRITE message_links]   (one row per URL, if implemented)

GET /v1/messages
    READ messages + message_analysis (join for final_score)

GET /v1/messages/{id}
    READ messages (raw text, source, label)
    READ message_analysis (all scores, explanation, model_version)
```

| Pipeline stage | `messages` | `message_analysis` | `message_links` | `message_attachments` |
|---|---|---|---|---|
| Phase 0 — Preprocessing | — | — | — | READ `extracted_text` (if MMS) |
| Phase 1 — Rule engine | — | — | — | — |
| Phase 2 — ML classifier | — | — | — | — |
| Phase 3 — Claude (pre-call) | — | READ (SHA-256 dedup, Issue #36) | — | — |
| Phase 3 — Claude (post-call) | — | — | — | — |
| Combiner | — | — | — | — |
| `MessageRepository.save()` | WRITE | WRITE | WRITE (if implemented) | WRITE (if MMS) |
| `GET /v1/messages` | READ | READ (`final_score`) | — | — |
| `GET /v1/messages/{id}` | READ | READ (full analysis) | — | — |

**Key invariant:** Phases 0–3 run entirely in memory against `artifacts{}`. The DB is not touched until `MessageRepository.save()` — except for the SHA-256 dedup read before Phase 3 in Issue #36.

---

## Schema Decisions

| Decision | Choice | Rationale |
| --- | --- | --- |
| Dedup strategy | No DB-level dedup — each submission gets its own row | Duplicate submissions are signal (multiple users reporting same scam). SHA-256 dedup (Issue #36) operates at the scoring layer to avoid re-calling Claude, not at storage. |
| Pipeline persistence | Process first, persist after — both rows written in one transaction | `MessageRepository.save(message, analysis)` is atomic. A `messages` row without a `message_analysis` row is never a valid state. |
| Failure handling | Fail-fast — if any phase fails, nothing is persisted | No partial rows. No async retry queue for MVP. User resubmits when the service recovers. |
| `model_version` format | Git SHA via `MODEL_VERSION` env var; `"dev"` for local | Automatically unique, ties directly to the code that produced the score. No manual semver bumping during frequent tuning. |
| `rule_reasons` shape | Fixed-key object — all signal keys always present, zero if not fired | Deterministic. Phase 2 feature extraction reads `rule_reasons["url_suspicious"]` directly without iteration or null checks. |
| Score range | CHECK (>= 0 AND <= 1) on all four score columns | Pipeline normalizes to 0–1 before persisting. DB constraint is a safety net against pipeline bugs. |
| `ai_score` / `ai_explanation` nullability | NOT NULL | Phase 3 is never optional. Fail-fast means a persisted row always has a complete Claude result. |
| `runtime_flags` | NOT NULL — stores combiner weights per run | Enables comparison across tuning iterations: which weights produced which `final_score`. |
| `category` placement | Stays on `messages` for MVP | Phase 0 sets it once at persist time. **v2:** consider moving to `message_analysis` if re-scoring is introduced. |
| Cascade delete | `ON DELETE CASCADE` on `message_analysis` | Input validation at API boundary (Issue #27) is the primary defense against garbage. Cascade exists for admin cleanup and PII scrubbing. |
