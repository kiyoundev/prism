# PRD: Prism — SMS Scam Detection (MVP v1)

**Status:** Active  
**Date:** 2026-05-03  
**Repo:** prism (monorepo)  
**Target:** Web MVP — public demo + internal dataset tooling

---

## Problem Statement

People receive suspicious SMS messages daily and have no fast, reliable way to evaluate them. Existing tools require technical knowledge or are unavailable to the general public. Vulnerable populations — elderly users, people targeted by delivery or banking scams — lack an accessible first line of defense. There is no tool that combines deterministic pattern detection, trained ML classification, and grounded AI reasoning into a single explainable score that a non-technical person can act on.

---

## Solution

Prism is a web application that accepts a raw SMS body, runs it through a four-phase sequential intelligence pipeline, and returns a scam likelihood percentage with plain-English explanations. Each phase enriches the context passed to the next:

- **Phase 0** normalizes the text and extracts structured artifacts (URLs, tokens, brand slug, category).
- **Phase 1** scores the artifacts against deterministic rule signals (URL heuristics, social engineering patterns, obfuscation, financial structuring).
- **Phase 2** applies a trained ML classifier (TF-IDF + Naive Bayes) using Phase 0 tokens and Phase 1 rule hits as features.
- **Phase 3** sends all prior artifacts to Claude, which produces an independent `ai_score` and a grounded plain-English explanation.

The final score is a weighted combination of all three phase scores. Every submission is persisted for history browsing and future model improvement.

---

## User Stories

### Submission & Scoring

1. As a user, I want to paste a suspicious SMS into a form and submit it, so that I can find out whether it is likely a scam.
2. As a user, I want to see a scam likelihood percentage clearly displayed after submission, so that I can immediately understand the risk level.
3. As a user, I want to see the specific reasons the system flagged the message (e.g., "suspicious TLD", "urgency pattern detected"), so that I understand what made it suspicious.
4. As a user, I want to read a plain-English explanation of why the message was scored the way it was, so that I can make sense of the result without technical knowledge.
5. As a user, I want to see the form clear after I submit, so that I can quickly analyze another message without manual clearing.
6. As a user, I want to see a loading state while the analysis is running, so that I know the system is working and haven't submitted twice.
7. As a user, I want analysis to complete in under three seconds, so that the tool feels responsive and useful in real time.

### History & Detail

8. As a user, I want to browse a list of previously submitted messages and their scam scores, so that I can refer back to past analyses.
9. As a user, I want to click into a specific submission to see the full analysis detail, so that I can review all three phase outputs in depth.
10. As a user, I want to see the rule reasons, ML score, and Claude explanation on the detail page, so that I have full transparency into how the score was produced.
11. As a user, I want the history list to show the message snippet and final score at a glance, so that I can scan past submissions quickly.

### Rule Engine Transparency

12. As a user, I want rule reasons to use human-readable display strings (not machine codes), so that I understand what each flag means.
13. As a user, I want to see which brand or category was detected in the message (e.g., "Canada Post — Delivery"), so that I understand the context the system used.
14. As a user, I want the system to detect URL manipulation techniques (typosquatting, suspicious TLDs, brand-domain mismatch), so that phishing links are caught even when text looks legitimate.
15. As a user, I want urgency and authority language to be flagged ("Your account has been suspended", "CRA tax debt"), so that social engineering patterns are surfaced explicitly.

### Pipeline Integrity

16. As a developer, I want Phase 0 to extract URLs before normalization, so that URL structure is preserved for accurate analysis.
17. As a developer, I want Phase 0 to flatten homoglyphs and zero-width characters, so that obfuscated text is normalized before any pattern matching.
18. As a developer, I want Phase 0 to output a structured `artifacts{}` bundle, so that all downstream phases receive identical, reproducible input.
19. As a developer, I want Phase 1 to receive only Phase 0 artifacts, so that rule scoring is deterministic and independent of ML or AI.
20. As a developer, I want Phase 2 to receive Phase 0 tokens and Phase 1 rule hits, so that the classifier benefits from structured signal context.
21. As a developer, I want Phase 3 to receive all prior phase outputs in a structured prompt, so that Claude never scores a message cold or without grounding.
22. As a developer, I want the combiner to apply tunable weights to `rule_score`, `ml_score`, and `ai_score`, so that scoring balance can be adjusted without touching pipeline logic.
23. As a developer, I want repeated identical messages to skip Phase 3 via a SHA-256 dedup cache, so that Claude API costs are not incurred for duplicates.

### Data Model & Persistence

24. As a developer, I want every SMS submission to be stored in the `messages` table with its `source` and `label`, so that seed and user-submitted data are tracked separately.
25. As a developer, I want every scoring run to produce a row in `message_analysis` with all three phase scores and the model version, so that analysis history is reproducible and auditable.
26. As a developer, I want to seed the database with labeled scam and legit messages from the UCI SMS Spam Collection, so that Phase 2 has a training corpus before any user submissions exist.

### API & Security

27. As a developer, I want all `/v1/*` routes to require an `X-API-Key` header, so that the scoring API is not publicly accessible without authorization.
28. As a developer, I want the FastAPI backend URL to never be exposed to the browser, so that the scoring endpoint cannot be called directly from client-side code.
29. As a developer, I want the Next.js frontend to proxy all FastAPI calls via a server-side route, so that CORS issues are eliminated and the backend URL stays hidden.
30. As a developer, I want input to be sanitized before entering the pipeline, so that prompt injection and SQL injection are prevented at the system boundary.

### Infrastructure & Deployment

31. As a developer, I want a `docker-compose.yml` for local development that runs FastAPI and Postgres together, so that I can develop without depending on Supabase or Railway.
32. As a developer, I want `.env.example` files in both `backend/` and `frontend/`, so that environment setup is documented and reproducible.
33. As a developer, I want Alembic to manage all schema migrations, so that database changes are versioned and reproducible across environments.
34. As a developer, I want GitHub Actions to run Ruff linting and pytest on every PR, so that quality gates are enforced automatically.

### Dataset Management

35. As a developer, I want a dataset endpoint to add seed scam and legit messages to the database in bulk, so that the training corpus can be loaded without manual SQL.
36. As a developer, I want each seed message to carry a `source` tag (`seed_scam` or `seed_legit`), so that training data and user submissions are never mixed up in evaluation.

---

## Implementation Decisions

### Architecture
- Monorepo: `frontend/` (Next.js 15, App Router) + `backend/` (FastAPI, Python). Frontend never touches Postgres directly — all data access goes through FastAPI.
- Deployment: Vercel (frontend), Railway (backend), Supabase (Postgres + pgvector).
- The Next.js server-side proxy route forwards `/api/score` → FastAPI `POST /v1/score`. The FastAPI URL is set via environment variable on Vercel; it is never in client-side code.

### Phase 0 — Preprocessing & Extraction
- URL extraction runs on raw text before any normalization.
- Normalization order: lowercase → punctuation strip → Unicode NFKD (`unicodedata`) → homoglyph flatten (`unidecode`) → zero-width character removal.
- Tokenization produces word tokens; bi-gram and tri-gram sequences are generated for phrase matching.
- Fuzzy matching (`rapidfuzz`) catches near-miss brand names and keyword variants.
- Brand detection uses longest-match against `brand_variants.json`; keyword fallback scores against `category_keywords.json`; URL domain checked against `allowed_domains.json`.
- Resolution priority: URL brand (confidence 1.0) → text brand (0.9) → keyword density above threshold (0.8) → `unknown` (0.0).
- Output: `artifacts{}` — `extracted_urls[]`, `normalized_text`, `tokens[]`, `ngrams[]`, `brand_slug`, `category`.

### Phase 1 — Rule Engine
- Rule signals: URL analysis (typosquatting, suspicious TLDs, shorteners, brand-domain mismatch), homoglyph/zero-width detection, urgency/authority/scarcity patterns, financial structuring (gift cards, crypto, specific amounts), channel shifting (WhatsApp/Telegram/Signal), formatting abuse (emoji, all-caps, excessive punctuation).
- Config files (`brand_variants.json`, `category_keywords.json`, `allowed_domains.json`) load from disk at FastAPI startup — no DB tables required for rule definitions in MVP.
- Output: `rule_score [0,1]`, `rule_reasons[]` (machine code + display string per reason).

### Phase 2 — ML Classifier
- Input: Phase 0 `artifacts{}` + Phase 1 `rule_reasons[]` as feature context.
- TF-IDF vectorization (`scikit-learn TfidfVectorizer`) on Phase 0 tokens — weights keywords by frequency in message vs. corpus.
- NLTK `SentimentIntensityAnalyzer` produces urgency/negativity signal as secondary feature.
- Naive Bayes classifier (baseline); serialized to disk after training, loaded at startup.
- Training corpus: UCI SMS Spam Collection (~5.5k labeled ham/spam messages).
- Output: `ml_score [0,1]`, `ml_details{}` (TF-IDF feature weights, sentiment score).

### Phase 3 — Claude AI
- Claude receives a structured prompt: raw SMS + Phase 0 artifacts + Phase 1 rule signals that fired + Phase 2 `ml_score` and sentiment — never a cold call.
- SHA-256 hash of the raw SMS text is used as a dedup key; repeated messages skip Phase 3 and reuse the cached result.
- Output: `ai_score [0,1]`, `explanation` (plain English, grounded in detected artifacts).
- Provider: Anthropic Python SDK.

### Combiner
- `final_score = weighted_combiner(rule_score, ml_score, ai_score)`.
- Weights start equal; tunable without touching pipeline logic.

### Database Schema
- `messages`: `id (UUID PK)`, `created_at`, `text`, `source` (`seed_scam | seed_legit | user_submitted`), `label` (`scam | legit | unknown`), `category`, `metadata (JSONB)`.
- `message_analysis`: `id (UUID PK)`, `message_id (FK)`, `rule_score`, `rule_reasons (JSONB)`, `ml_score`, `ml_details (JSONB)`, `ai_score`, `ai_explanation`, `final_score`, `model_version`, `created_at`.
- Managed via Alembic migrations; two migrations for MVP (one per table).
- `pgvector` extension enabled from the start for v2 RAG pipeline (no schema change needed later).

### API Surface
- `POST /v1/score` — full pipeline + persist + return `ScoringResult`.
- `GET /v1/messages` — paginated list with `source`, `label`, `final_score` filter params.
- `GET /v1/messages/{id}` — single message with latest analysis.
- `GET /v1/messages/{id}/analysis/latest` — full analysis detail.
- `POST /v1/dataset/messages` — bulk seed data ingestion (admin).
- All `/v1/*` routes protected by `X-API-Key` middleware.

### Frontend Pages
- `/demo` — SMS textarea form, loading state, `ScoreCard` (final score + risk level), rule reasons list, Claude explanation panel.
- `/history` — server-fetched list of user-submitted messages with final score badges.
- `/messages/[id]` — full analysis detail: all three phase outputs, model version, timestamps.
- No client-side state management (no Zustand). Server Components fetch on demand; only `useState` for form input/loading/result on `/demo`.

### ORM & Schemas
- SQLAlchemy ORM models in `models/` map directly to `messages` and `message_analysis`.
- Pydantic schemas in `schemas/` describe API request/response payloads (`MessageCreate`, `ScoringResult`, `AnalysisResult`).

---

## Testing Decisions

**What makes a good test:** Tests should verify external behavior — inputs and outputs of a module's public interface — not implementation details like internal helper calls or intermediate state. A test should remain valid even if the internal implementation is refactored.

### Modules to test

| Module | What to test |
|---|---|
| `normalizer.py` | Given raw text inputs (with homoglyphs, zero-width chars, unicode), assert normalized output matches expected ASCII string |
| `url_extractor.py` | Given text with embedded URLs (incl. obfuscated), assert extracted URL list is correct and preserves pre-normalization form |
| `tokenizer.py` | Given normalized text, assert token list, bi/tri-gram sequences, and fuzzy match results are correct |
| `category_extractor.py` | Given token inputs matching brand variants or category keywords, assert correct `brand_slug` and `category` output |
| `url_checker.py` | Given a URL, assert the correct rule signals fire (allowlist hit, denylist hit, suspicious TLD, brand-domain mismatch) |
| `unicode_detector.py` | Given text with Cyrillic substitutions and zero-width chars, assert detection flags are set |
| `pattern_matcher.py` | Given text with urgency/authority/financial patterns, assert the correct `rule_reasons[]` codes are returned |
| `combiner.py` | Given three phase scores, assert `final_score` matches expected weighted combination |
| `POST /v1/score` | Integration test: submit a known scam SMS, assert response contains `final_score`, `rule_reasons`, `ai_explanation`, and that a `message_analysis` row was persisted |

### Testing approach
- Unit tests with `pytest` for all pipeline modules (Phases 0–2, combiner).
- Integration test for `POST /v1/score` against a real test database (not mocked — Phase 2 ML model and DB must be live).
- Playwright E2E for `/demo` submission flow: fill form → submit → assert `ScoreCard` renders with a non-zero score.
- No mocking of the database in integration tests.

---

## Out of Scope

- **v2 RAG pipeline**: `pgvector` embeddings, similarity retrieval, RAG-injected Phase 3 prompts — post-MVP.
- **Self-training loop**: moderation queue, auto-approval, Phase 2 retraining on user submissions — post-MVP.
- **Admin UI**: seed data management via browser, evaluation dashboard — post-MVP.
- **Phone number analysis**: only SMS text body is scored in MVP.
- **Native mobile apps**: web only for MVP.
- **Probability calibration**: tuning combiner weights requires evaluation data that doesn't exist yet.
- **Rate limiting**: planned but not required for MVP with API key protection in place.
- **PII stripping**: raw SMS text is stored as-is in MVP; a retention policy and PII scrubbing step is a pre-launch requirement before any public release.

---

## Further Notes

- The `category` field on `messages` is set by Phase 0 extraction and written at persist time — it reflects the Phase 0 classification outcome, not a user-provided label.
- `model_version` in `message_analysis` should be a string that identifies the pipeline build (e.g., a git SHA or a manually bumped semver). This enables future comparison across model iterations.
- The Phase 3 dedup cache (SHA-256 → cached result) lives in memory for MVP. In v2, move it to Redis or Supabase for durability across restarts.
- `pgvector` is enabled on Supabase from day one so that v2 RAG requires no infrastructure change — only a new migration for the `message_embeddings` table.
- Supabase Studio is the primary tool for manually curating and reviewing seed data; Railway hosts FastAPI with all DB credentials — Supabase RLS is enforced as a secondary layer.
