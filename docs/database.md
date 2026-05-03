## Core Runtime Tables

### messages
Stores every SMS that enters Prism—seed scams, seed legit, and user submissions. Acts as the authoritative record for downstream scoring and UI retrieval. When payloads are non-textual (screenshots, MMS), store any OCR output in `text` (even if blank) and capture ingestion details in `metadata` (e.g., `{"has_image": true, "ocr_confidence": 0.42}`) so the rule engine can still operate on normalized data.
| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | Stable identifier shared across services |
| `created_at` | `TIMESTAMPTZ` NOT NULL DEFAULT `now()` | Initial ingestion timestamp |
| `text` | `TEXT` NOT NULL | Raw SMS body exactly as submitted |
| `source` | `TEXT` CHECK in (`'seed_scam'`, `'seed_legit'`, `'user_submitted'`) | Tracks provenance/origin |
| `label` | `TEXT` CHECK in (`'scam'`, `'legit'`, `'unknown'`) | Ground-truth or moderation outcome |
| `category` | `TEXT` NULL | High-level topic (delivery, banking, tax, etc.) set by rules/ML |
| `metadata` | `JSONB` NULL | Free-form attributes (channel, sender, etc.) |

Indexes:
- `INDEX (source)`
- `INDEX (label)`
- `INDEX (created_at DESC)`

### message_analysis
Captures every scoring run for a message so you retain rule/ML outputs, explanations, and model version history. Multiple rows can exist per message as models evolve. Use `rule_reasons` / `ml_details` JSON to record whether detections came from attachment hashes, OCR tokens, or other signals to keep the audit trail complete.
| Column | Type | Notes |
| --- | --- | --- |
| `id` | UUID PK default `gen_random_uuid()` | Unique per analysis run |
| `message_id` | UUID NOT NULL REFERENCES `messages(id)` ON DELETE CASCADE | Links back to the source message |
| `rule_score` | `NUMERIC` NOT NULL | Phase 1 deterministic score (0–1) |
| `rule_reasons` | `JSONB` NOT NULL | Machine-readable codes/evidence for rule hits |
| `ml_score` | `NUMERIC` NULL | Phase 2 similarity/model score (0–1) |
| `ml_details` | `JSONB` NULL | Nearest neighbors, tactics, embeddings metadata |
| `final_score` | `NUMERIC` NOT NULL | Soft-OR combiner result (0–1) |
| `model_version` | `TEXT` NOT NULL | Identifier of model/pipeline build |
| `runtime_flags` | `JSONB` NULL | Any toggles or experimental settings used |
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
