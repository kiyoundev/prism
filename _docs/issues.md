# Prism — Issue Backlog

Generated from PRD: `_docs/prd.md`  
Pace: solo part-time (~6 hrs/week across 3–4 projects)  
Total estimate: ~78 hours → **MVP target: end of August 2026**

All issues are AFK unless marked HITL (requires manual action outside the codebase).

---

## Timeline

| Milestone | Target | Groups |
|---|---|---|
| Tooling + hotfixes done | May 10, 2026 | Group 0 |
| Infra provisioned (Supabase, Railway, Vercel, Alembic, CI) | May 24, 2026 | Group 1 |
| Phase 0 preprocessing complete | June 7, 2026 | Group 2 |
| Phase 1 rule engine complete | June 28, 2026 | Group 3 |
| Phase 2 ML classifier complete | July 12, 2026 | Group 4 |
| Phase 3 Claude AI integrated | July 19, 2026 | Group 5 |
| Score combiner + full REST API complete | August 2, 2026 | Group 6 |
| Frontend UI complete | August 16, 2026 | Group 7 |
| **MVP: tests + polish done** | **August 30, 2026** | Group 8 |

---

## Dependency graph

**Phase 0 — Preprocessing**

```
#14 — normalizer.py
#15 — url_extractor.py
#16 — tokenizer.py: word tokens + n-grams
  └── #17 — tokenizer.py: rapidfuzz fuzzy matching
        └── #18 — extractor.py: artifacts{} bundle    [also needs #14, #15]
```

**Phase 1 — Rule Engine**

```
#18 — artifacts{} bundle (from Phase 0)
  ├── #19 — category_extractor: brand detection
  │     └── #20 — category_extractor: keyword scoring
  ├── #21 — url_checker: allowlist/denylist/TLD
  │     └── #22 — url_checker: brand-domain mismatch
  └── #26 — rule_score aggregator                   [also needs #20, #22, #23, #25]
        └── #27 — POST /v1/score Phase 1 stub

#23 — unicode_detector.py                           [no deps — feeds into #26]
#24 — pattern_matcher.py: urgency + authority
  └── #25 — pattern_matcher.py: financial + channel-shifting [feeds into #26]
#28 — X-API-Key middleware                          [no deps]
```

**Phase 2 — ML Classifier**

```
#29 — UCI SMS Spam Collection                       [HITL]
  └── #30 — features.py: TF-IDF pipeline            [also needs #18]
        └── #32 — classifier.py: train + serialize  [also needs #31]

#31 — sentiment.py: NLTK signal                     [no deps — feeds into #32]

#27 — Phase 1 stub (from Phase 1)
  └── #33 — Integrate Phase 2                       [also needs #32]
```

**Phase 3 — Claude AI**
> RAG context injection is v2 (out of scope for MVP). Phase 3 here is structured-prompt only — Claude receives all Phase 0–2 artifacts but no vector-retrieved examples.

```
#34 — client.py + prompts.py: Anthropic SDK + structured prompt  [no deps]
  └── #35 — Integrate Phase 3                       [also needs #33]
        └── #36 — SHA-256 dedup cache
```

**Combiner + Full API**

```
#35 — Phase 3 output
  └── #39 — combiner.py                             [also needs #26, #33]
        └── #40 — POST /v1/score full               [also needs #38]
              ├── #41 — GET /v1/messages
              │     ├── #42 — GET analysis/latest
              │     │     └── #48 — /messages/[id]  [also needs #43]
              │     └── #47 — /history page          [also needs #43]
              └── #43 — Next.js proxy route          [also needs #7]
                    └── #44 — /demo: SMS form
                          └── #45 — /demo: ScoreCard
                                └── #46 — /demo: Claude explanation panel
```

**Infrastructure**

```
#5 — Supabase: create project                    [HITL]
  ├── #6 — Railway: create project               [HITL]
  ├── #8 — .env.example files                    [also needs #6, #7]
  ├── #9 — docker-compose.yml for local dev
  └── #10 — Alembic: messages migration
        └── #11 — Alembic: message_analysis migration
              └── #37 — SQLAlchemy ORM models
                    └── #38 — Pydantic schemas   [feeds into #40]
```

**Phase 2 ML prerequisites**

```
#29 — UCI SMS Spam Collection                    [HITL]
  └── #30 — features.py: TF-IDF pipeline        [also needs #18]
        └── #32 — classifier.py: train + serialize [also needs #31]
              └── feeds into #33
```

**No-blocker starters**

```
#7  — Vercel: link frontend                      [HITL — feeds into #43]
#12 — GitHub Actions CI
#13 — Frontend: shadcn/ui + Lucide + base layout
#23 — unicode_detector.py                        [feeds into #26]
#24 — pattern_matcher.py: urgency + authority
  └── #25 — pattern_matcher.py: financial + channel-shifting [feeds into #26]
#28 — X-API-Key middleware
#31 — sentiment.py: NLTK signal                  [feeds into #32]
#34 — Anthropic client + prompts                 [feeds into #35]
```

**Testing**

```
#6.5  — Railway deployment smoke test            [needs #6]         HITL
#7.5  — Vercel deployment smoke test             [needs #7]         HITL
#8.6  — Env var validation smoke test            [needs #8.5]       HITL
#49   — pytest: Phase 0 unit tests               [needs #14–#17]
#50   — pytest: Phase 1 unit tests               [needs #19–#26]
#51   — pytest: Phase 2 unit tests               [needs #30–#32]
#52   — pytest: POST /v1/score integration test  [needs #40]
  └── #52.5 — pytest: GET endpoints              [also needs #41, #42]
#53   — Playwright E2E: /demo                    [needs #44, #52]
#54   — pytest: Phase 3 unit tests               [needs #34, #35, #36]
```

**Critical path:** `#5 → #10 → #11 → #37 → #38 → #40 → #41 → #47`  
**Start immediately (no blockers):** `#12, #13, #14, #15, #16, #23, #24, #28, #29, #31, #34`

---

## Group 0 — Hotfixes

---

## [✅] Issue #1 — Hotfixes: requirements.txt + Ruff/Prettier dev tooling 

**Type:** hotfix / AFK  
**Estimate:** ~1.5 hrs  
**Blocked by:** None

### What to build

Three grouped fixes shipped together: uncomment `unidecode==1.3.8` in `backend/requirements.txt` (startup crash fix), add all staged deps (`alembic`, `rapidfuzz`, `scikit-learn`, `anthropic`, `numpy`) with stage-level section comments, and configure Ruff (Python) and Prettier (frontend) with format-on-save in the editor.

### Acceptance criteria

- [x] `unidecode==1.3.8` is uncommented in `backend/requirements.txt`
- [x] `alembic`, `rapidfuzz`, `scikit-learn`, `anthropic`, `numpy` are present and pinned with stage comments
- [x] `pip install -r backend/requirements.txt` exits 0
- [x] `python -c "from unidecode import unidecode"` runs without error
- [x] Ruff extension installed in editor; Python files format on save
- [x] Prettier extension installed; TypeScript and JSON files format on save

---

## Group 1 — Infrastructure Setup

---

## [✅] Issue #5 — Supabase: create project, grab DATABASE_URL

**Type:** chore / HITL  
**Estimate:** ~30m  
**Blocked by:** None — start here

### What to build

Create the Supabase project that will serve as Prism's primary Postgres database. Enable the `pgvector` extension from the start so the v2 RAG pipeline requires no infrastructure change later. Capture the `DATABASE_URL` connection string (pooled, port 6543) for use in Railway and local dev.

### Acceptance criteria

- [x] Supabase project created and accessible in the dashboard
- [x] `pgvector` extension enabled under Database → Extensions
- [x] `DATABASE_URL` (pooled connection string) captured and stored securely

---

## [✅] Issue #6 — Railway: create project, set env vars

**Type:** chore / HITL  
**Estimate:** ~30m  
**Blocked by:** #5

### What to build

Create the Railway project that will host the FastAPI backend. Add a service pointed at the `backend/` directory. Set all required environment variables so the deployed service can connect to Supabase and call the Anthropic and internal APIs.

Variables to set: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `INTERNAL_API_KEY`.

### Acceptance criteria

- [x] Railway project created with a FastAPI service
- [x] `DATABASE_URL` set to the Supabase pooled connection string from #5
- [x] `ANTHROPIC_API_KEY` set to a valid Anthropic API key
- [x] `INTERNAL_API_KEY` set to a generated secret used by the X-API-Key middleware
- [x] Backend deployment pins Python 3.12 with `backend/runtime.txt`

---

## [ ] Issue #6.5 — Railway deployment smoke test

**Type:** test / HITL  
**Estimate:** ~15m  
**Blocked by:** #6

### What to build

Manual smoke test to verify the Railway FastAPI deployment is live, healthy, and correctly configured. Run from a terminal against the live Railway URL — no code changes needed.

### Acceptance criteria

- [ ] `GET https://<railway-url>/health` returns HTTP 200
- [ ] `POST /v1/score` with correct `X-API-Key` header and `{"text": "test"}` returns HTTP 200 with a `rule_score` field
- [ ] `POST /v1/score` with missing `X-API-Key` returns HTTP 401
- [ ] Railway deployment logs show no startup errors or missing env var warnings

---

## [✅] Issue #7 — Vercel: link frontend project, set FASTAPI_URL

**Type:** chore / HITL  
**Estimate:** ~30m  
**Blocked by:** None — parallel with #5

### What to build

Link the `frontend/` directory to a Vercel project. Set the `FASTAPI_URL` environment variable to the Railway service URL so the Next.js server-side proxy route can reach FastAPI without exposing the backend URL to the browser.

### Acceptance criteria

- [x] Vercel project created and linked to the `frontend/` directory in the monorepo
- [x] `FASTAPI_URL` environment variable set to the Railway backend URL
- [x] A preview deployment completes without build errors

---

## [ ] Issue #7.5 — Vercel deployment smoke test

**Type:** test / HITL  
**Estimate:** ~15m  
**Blocked by:** #7

### What to build

Manual smoke test to verify the Vercel Next.js deployment is live and the frontend shell loads correctly. Run from a browser against the deployed Vercel URL.

### Acceptance criteria

- [ ] Deployed Vercel URL returns HTTP 200
- [ ] `/demo` page loads without JavaScript console errors
- [ ] `/demo` page shows the SMS input form (not a blank page or error boundary)
- [ ] `next build` output in Vercel deployment logs shows 0 errors

---

## [✅] Issue #8 — `.env.example` files for backend and frontend

**Type:** infra / AFK  
**Estimate:** ~30m  
**Blocked by:** #5, #6, #7

### What to build

Create `.env.example` files in both `backend/` and `frontend/` documenting every required environment variable with placeholder values. These files are committed to the repo; the actual `.env` files are gitignored. Any developer cloning the repo should be able to copy `.env.example` → `.env` and know exactly what values to fill in.

`backend/.env.example` variables: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `INTERNAL_API_KEY`.  
`frontend/.env.example` variables: `FASTAPI_URL`, `INTERNAL_API_KEY`.

### Acceptance criteria

- [x] `backend/.env.example` exists and documents all required backend env vars with placeholder values
- [x] `frontend/.env.example` exists and documents all required frontend env vars with placeholder values
- [x] No real secrets are present in either file
- [x] Both files are committed; `.env` is in `.gitignore`

---

## [✅] Issue #8.5 — Validate required env vars at startup

**Type:** infra / AFK  
**Estimate:** ~45m  
**Blocked by:** #8

### What to build

Add backend and frontend environment validation so missing required variables fail fast during startup/build instead of causing runtime errors later. The backend should validate its Railway/local runtime variables when FastAPI starts. The frontend should validate only server-side Next.js variables used by the proxy route, without exposing secrets to browser code.

Backend required variables: `DATABASE_URL`, `ANTHROPIC_API_KEY`, `INTERNAL_API_KEY`.  
Frontend required variables: `FASTAPI_URL`, `INTERNAL_API_KEY`.

### Acceptance criteria

- [x] Backend validates `DATABASE_URL`, `ANTHROPIC_API_KEY`, and `INTERNAL_API_KEY` at startup with clear error messages
- [x] Frontend validates `FASTAPI_URL` and `INTERNAL_API_KEY` on the server side before proxy calls depend on them
- [x] Missing or empty env vars fail fast in local dev, Docker, Railway, and Vercel builds/previews
- [x] No secret values are logged or exposed to the browser
- [x] Validation stays in sync with `backend/.env.example` and `frontend/.env.example`

---

## [ ] Issue #8.6 — Smoke test: env var validation on startup

**Type:** test / AFK  
**Estimate:** ~30m  
**Blocked by:** #8.5

### What to build

Manual smoke tests to verify that `config.py` and `env.ts` fail fast with clear messages when required env vars are missing. No automated test framework needed — these are one-time verification steps run locally.

**Backend:** Start FastAPI with a missing env var and confirm it exits immediately with a readable error.  
**Frontend:** Start Next.js dev server without a required var and confirm the first request to `/api/score` throws a clear error, not a cryptic `undefined`.

### Acceptance criteria

- [ ] `DATABASE_URL` unset → FastAPI exits immediately with `Missing required environment variable: DATABASE_URL`
- [ ] `ANTHROPIC_API_KEY` unset → same fast exit
- [ ] `INTERNAL_API_KEY` unset → same fast exit
- [ ] `FASTAPI_URL` unset → first server-side request throws `Missing required environment variable: FASTAPI_URL`
- [ ] `INTERNAL_API_KEY` unset on frontend → same clear error
- [ ] No secret values appear in any error output

---

## [✅] Issue #9 — `docker-compose.yml` for local dev

**Type:** infra / AFK  
**Estimate:** ~1h  
**Blocked by:** #5

### What to build

A `docker-compose.yml` at the repo root that spins up FastAPI and a local Postgres instance for development without depending on Supabase or Railway. The local Postgres uses the same schema as Supabase (applied via Alembic). FastAPI should hot-reload on file changes.

### Acceptance criteria

- [x] `docker-compose up` starts both the FastAPI service and a local Postgres container
- [x] FastAPI is accessible at `http://localhost:8000`
- [x] FastAPI reloads on file changes in `backend/app/`
- [x] Local Postgres is reachable from the backend container for future Alembic migrations
- [x] FastAPI container uses the same Python version as Railway runtime
- [x] `docker-compose down` cleanly stops all services

---

## [ ] Issue #10 — Alembic init + `messages` table migration

**Type:** infra / AFK  
**Estimate:** ~2h  
**Blocked by:** #5

### What to build

Initialize Alembic in `backend/` and write the first migration that creates the `messages` table. The table stores every SMS that enters Prism — seed scam, seed legit, and user-submitted — with provenance and ground-truth label tracking.

**Schema:**
- `id`: UUID PK, `gen_random_uuid()`
- `created_at`: TIMESTAMPTZ NOT NULL DEFAULT now()
- `text`: TEXT NOT NULL
- `source`: TEXT CHECK IN (`seed_scam`, `seed_legit`, `user_submitted`)
- `label`: TEXT CHECK IN (`scam`, `legit`, `unknown`)
- `category`: TEXT NULL
- `metadata`: JSONB NULL

**Indexes:** `(source)`, `(label)`, `(created_at DESC)`

**Migration naming convention:** `YYYYMMDD_{rev}_{slug}.py` — date-prefixed for chronological filesystem ordering, hex rev ID for Alembic chaining. Configured via `file_template` in `alembic.ini`.

**SQLAlchemy note:** ORM column uses `metadata_` (Python attribute) mapped to `"metadata"` (SQL column name) to avoid shadowing `DeclarativeBase.metadata`.

### Acceptance criteria

- [ ] `alembic init` run; `alembic.ini` and `alembic/env.py` configured with `DATABASE_URL`
- [ ] First migration file created under `alembic/versions/`
- [ ] `alembic upgrade head` applies cleanly against both local Postgres and Supabase
- [ ] `messages` table exists with all columns, constraints, and indexes as specified
- [ ] `alembic downgrade -1` reverses the migration cleanly

---

## [ ] Issue #11 — `message_analysis` table migration

**Type:** infra / AFK  
**Estimate:** ~1h  
**Blocked by:** #10

### What to build

Second Alembic migration that creates the `message_analysis` table. This table stores one row per scoring run — all three phase scores, reasons, explanations, and model version — enabling full analysis history and reproducibility across model iterations.

**Schema:**
- `id`: UUID PK, `gen_random_uuid()`
- `message_id`: UUID NOT NULL REFERENCES `messages(id)` ON DELETE CASCADE
- `rule_score`: NUMERIC NOT NULL
- `rule_reasons`: JSONB NOT NULL
- `ml_score`: NUMERIC NULL
- `ml_details`: JSONB NULL
- `ai_score`: NUMERIC NULL
- `ai_explanation`: TEXT NULL
- `final_score`: NUMERIC NOT NULL
- `model_version`: TEXT NOT NULL
- `runtime_flags`: JSONB NULL
- `created_at`: TIMESTAMPTZ NOT NULL DEFAULT now()

**Indexes:** `(message_id, created_at DESC)`, `(model_version)`

### Acceptance criteria

- [ ] Second migration file created under `alembic/versions/`
- [ ] `alembic upgrade head` applies cleanly; `message_analysis` table exists with all columns and constraints
- [ ] Foreign key to `messages(id)` is enforced: inserting a row with a non-existent `message_id` raises an error
- [ ] ON DELETE CASCADE: deleting a `messages` row cascades to its `message_analysis` rows
- [ ] Both indexes present
- [ ] `alembic downgrade -1` reverses cleanly without touching the `messages` table

---

## [ ] Issue #12 — GitHub Actions CI: Ruff lint + pytest on PR

**Type:** ci / AFK  
**Estimate:** ~1h  
**Blocked by:** None — start anytime

### What to build

A GitHub Actions workflow file (`.github/workflows/ci.yml`) that runs on every pull request. The workflow runs Ruff linting on `backend/` and the pytest suite. A PR cannot merge if either step fails.

### Acceptance criteria

- [ ] `.github/workflows/ci.yml` exists and triggers on `pull_request` to `main`
- [ ] Ruff lint step fails the workflow if any lint errors are present
- [ ] pytest step runs the test suite under `backend/tests/`
- [ ] A PR with a deliberate lint error causes the workflow to fail
- [ ] A PR with a deliberate failing test causes the workflow to fail
- [ ] A clean PR passes both steps

---

## [ ] Issue #13 — Frontend: install shadcn/ui + Lucide React, base layout

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** None — start anytime

### What to build

Install and configure shadcn/ui (built on Radix UI) and Lucide React icons in the Next.js frontend. Create the root layout with a minimal top navigation (Prism wordmark + nav links to `/demo` and `/history`). The layout should be responsive and use TailwindCSS for styling. No functional pages yet — just the shell every page will inherit.

### Acceptance criteria

- [ ] `shadcn/ui` initialized; component CLI works (`npx shadcn-ui add button` succeeds)
- [ ] Lucide React installed and an icon renders in the layout without errors
- [ ] Root layout renders a top nav with the Prism wordmark and links to `/demo` and `/history`
- [ ] Layout is responsive (nav collapses correctly on mobile widths)
- [ ] `next build` completes without errors

---

## Group 2 — Phase 0: Preprocessing

---

## [ ] Issue #14 — `normalizer.py`: text normalization pipeline

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/preprocessing/normalizer.py` — a pure function `normalize(text: str) -> str` that runs the full normalization pipeline in order:

1. Lowercase conversion
2. Punctuation stripping
3. Unicode NFKD normalization (`unicodedata.normalize('NFKD', text)`) — reduces accented chars to base form (e.g., `é` → `e`)
4. Homoglyph flattening (`unidecode`) — transliterates Cyrillic/mathematical substitutes to ASCII equivalents
5. Zero-width character removal (`​`, `‌`, `‍`, `﻿`, etc.) — used by scammers to break keyword matching

The function must be idempotent (running it twice produces the same result as running it once).

### Acceptance criteria

- [ ] `normalize("Héllo Wörld")` returns `"hello world"`
- [ ] `normalize("Ηello")` (Eta, not H) returns `"hello"` — Cyrillic/Greek homoglyph flattened
- [ ] `normalize("hel​lo")` returns `"hello"` — zero-width char removed
- [ ] `normalize(normalize(text)) == normalize(text)` for arbitrary input (idempotent)
- [ ] Punctuation is stripped; alphanumeric characters and spaces are preserved
- [ ] Function has no side effects and no global state

---

## [ ] Issue #15 — `url_extractor.py`: extract URLs before normalization

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/preprocessing/url_extractor.py` — a function `extract_urls(text: str) -> list[str]` that extracts all URLs from the raw SMS text **before** any normalization. URLs must be captured in their original pre-normalization form so that domain structure (casing, punycode, percent-encoding) is preserved for Phase 1 URL analysis.

### Acceptance criteria

- [ ] Extracts standard `http://` and `https://` URLs from plain text
- [ ] Extracts bare domains without protocol (e.g., `bit.ly/abc123`)
- [ ] Handles multiple URLs in a single message
- [ ] Preserves the original form of each URL (no lowercasing or stripping)
- [ ] Returns an empty list for messages with no URLs
- [ ] Does not extract email addresses as URLs

---

## [ ] Issue #16 — `tokenizer.py`: word tokens + bi/tri-grams

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/preprocessing/tokenizer.py` — functions that take normalized text and produce:

- `tokenize(text: str) -> list[str]`: splits into word tokens (alphanumeric only, no punctuation)
- `ngrams(tokens: list[str], n: int) -> list[str]`: generates n-gram phrases joined by spaces
- `get_ngrams(tokens: list[str]) -> list[str]`: returns bi-grams + tri-grams combined

These outputs are consumed by both the brand/category extractor and the Phase 2 TF-IDF pipeline.

### Acceptance criteria

- [ ] `tokenize("Your package is ready")` returns `["your", "package", "is", "ready"]`
- [ ] `tokenize` strips punctuation and handles extra whitespace
- [ ] `ngrams(["a", "b", "c"], 2)` returns `["a b", "b c"]`
- [ ] `get_ngrams(tokens)` returns the union of bi-grams and tri-grams
- [ ] Empty string input returns empty lists without raising

---

## [ ] Issue #17 — `tokenizer.py`: rapidfuzz fuzzy matching

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #16

### What to build

Extend `tokenizer.py` with a `fuzzy_match(text: str, candidates: list[str], threshold: int = 85) -> list[str]` function that uses `rapidfuzz` to find near-miss matches between normalized text and a list of candidate strings (brand names, keyword variants). This catches obfuscated brand mentions that exact matching would miss (e.g., `"Cañada Post"` → `"Canada Post"`, `"Amaz0n"` → `"Amazon"`).

### Acceptance criteria

- [ ] `fuzzy_match("Cañada Post", ["Canada Post"])` returns `["Canada Post"]`
- [ ] `fuzzy_match("Amaz0n", ["Amazon"])` returns `["Amazon"]`
- [ ] A string with no near-miss at or above `threshold` returns an empty list
- [ ] Threshold is configurable; lowering it increases matches
- [ ] Exact matches always pass at any threshold

---

## [ ] Issue #18 — `extractor.py`: wire Phase 0 into `artifacts{}` bundle

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #14, #15, #16, #17

### What to build

`backend/app/core/preprocessing/extractor.py` — a function `extract(text: str) -> dict` that orchestrates the full Phase 0 pipeline and returns a single `artifacts{}` dict consumed by all downstream phases.

**Output keys:**
- `extracted_urls: list[str]` — from `url_extractor` (pre-normalization)
- `normalized_text: str` — from `normalizer`
- `tokens: list[str]` — from `tokenizer`
- `ngrams: list[str]` — bi + tri-grams from `tokenizer`
- `brand_slug: str | None` — set by #19/#20 (placeholder `None` here)
- `category: str` — set by #19/#20 (placeholder `"unknown"` here)

### Acceptance criteria

- [ ] `extract(text)` returns a dict with all six keys
- [ ] `extracted_urls` contains URLs from the raw text (not normalized)
- [ ] `normalized_text` passes through the full normalization pipeline
- [ ] `tokens` and `ngrams` are derived from `normalized_text`
- [ ] `brand_slug` is `None` and `category` is `"unknown"` until #19/#20 wire in classification
- [ ] Raises `ValueError` for empty or whitespace-only input

---

## Group 3 — Phase 1: Rule Engine

---

## [ ] Issue #19 — `category_extractor.py`: brand detection

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #18

### What to build

Implement brand detection in `backend/app/core/rules/category_extractor.py`. At startup, load `brand_variants.json` (maps brand slugs to lists of aliases). Given `artifacts{}`, scan the tokens and n-grams for brand aliases using a longest-match-first strategy. A multi-word alias (e.g., `"Canada Post"`) must win over a single-word alias (e.g., `"Canada"`). On match, write `brand_slug` and the resolved `category` back into `artifacts{}` and return immediately — no keyword scoring needed.

Also check the extracted URLs: if any URL's registered domain matches a brand's canonical domain in `allowed_domains.json`, that is a brand match with confidence 1.0.

### Acceptance criteria

- [ ] Text containing `"Canada Post"` resolves to `brand_slug="canada_post"`, `category="delivery"`
- [ ] Text containing only `"Canada"` does not match `canada_post` (multi-word alias requires full phrase)
- [ ] URL containing `canadapost.ca` resolves to `canada_post` regardless of text content
- [ ] URL brand match takes priority over text brand match
- [ ] `brand_variants.json` is loaded once at startup, not re-read per request
- [ ] Returns without modification if no brand is detected

---

## [ ] Issue #20 — `category_extractor.py`: keyword scoring + resolution logic

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #19

### What to build

Implement the keyword-based fallback in `category_extractor.py`. Load `category_keywords.json` (maps categories to lists of keyword phrases). If no brand was detected in #19, score each category by counting how many of its keyword phrases appear in the lemmatized tokens. The category with the highest density above a minimum threshold wins. Return `category="unknown"` if no category clears the threshold.

**Resolution priority (per PRD):**
1. URL brand match → confidence 1.0
2. Text brand match → confidence 0.9
3. Keyword density above threshold → confidence 0.8
4. Default: `unknown` → confidence 0.0

### Acceptance criteria

- [ ] Text with `"tracking number"`, `"missed delivery"`, `"return to sender"` resolves to `category="delivery"`
- [ ] Text with no brand and no keyword hits resolves to `category="unknown"`
- [ ] Brand detection from #19 always wins over keyword scoring
- [ ] Keyword threshold is configurable (not hardcoded)
- [ ] `category_keywords.json` is loaded once at startup

---

## [ ] Issue #21 — `url_checker.py`: allowlist/denylist + suspicious TLD detection

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #18

### What to build

`backend/app/core/rules/url_checker.py` — given a list of extracted URLs and the resolved `brand_slug`, check each URL against:

1. **Allowlist** (`allowed_domains.json`): brand-specific canonical domains. A match clears URL suspicion for that brand.
2. **Denylist**: known bad hosts, URL shorteners (bit.ly, tinyurl.com, etc.), previously-seen typosquats. A match is a strong risk signal.
3. **Suspicious TLD heuristic**: flag TLDs commonly used in phishing (`.xyz`, `.top`, `.click`, `.tk`, `.ml`, `.ga`, `.cf`, `.gq`, free hosting TLDs).

Use `tldextract` to extract the registered domain from each URL before comparison.

Emit rule signals as `(code, display_string)` tuples to be collected by the rule_score aggregator in #26.

### Acceptance criteria

- [ ] `https://canadapost.ca/track` with `brand_slug="canada_post"` produces no URL risk signals
- [ ] `https://bit.ly/x9k2p` produces a `url_shortener` signal
- [ ] `https://myparcel.xyz` produces a `suspicious_tld` signal
- [ ] A URL on a known denylist domain produces a `denylist_hit` signal
- [ ] `tldextract` is used to extract the registered domain; raw string matching is not used

---

## [ ] Issue #22 — `url_checker.py`: brand-domain mismatch detection

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #21

### What to build

Extend `url_checker.py` with brand-domain mismatch detection. If a brand was detected in the message text (e.g., `"Canada Post"`) but all extracted URLs belong to domains not in that brand's allowlist, emit a `brand_domain_mismatch` signal. This catches the core phishing pattern: impersonate a known brand in text while linking to an attacker-controlled domain.

### Acceptance criteria

- [ ] Message with `"Canada Post"` text and a URL on `canadapost.ca` produces no mismatch signal
- [ ] Message with `"Canada Post"` text and a URL on `parcel-track.xyz` produces a `brand_domain_mismatch` signal
- [ ] Mismatch signal is not emitted when `brand_slug` is `None`
- [ ] Mismatch signal is not emitted when there are no extracted URLs
- [ ] Signal includes a display string naming the detected brand and the mismatched domain

---

## [ ] Issue #23 — `unicode_detector.py`: homoglyph + zero-width character detection

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/rules/unicode_detector.py` — given the raw SMS text (before normalization), detect deliberate obfuscation via:

1. **Homoglyphs**: presence of Cyrillic, Greek, or mathematical alphanumeric characters that visually resemble Latin letters (e.g., Cyrillic `а` ≠ Latin `a`)
2. **Zero-width characters**: `​` (zero-width space), `‌` (ZWNJ), `‍` (ZWJ), `﻿` (BOM), etc. — inserted to break keyword matching

Emit a `homoglyph_detected` or `zero_width_detected` signal per type found.

### Acceptance criteria

- [ ] Text containing Cyrillic `а` (U+0430) emits `homoglyph_detected`
- [ ] Text containing only ASCII characters emits no signals
- [ ] Text containing `​` emits `zero_width_detected`
- [ ] Runs on raw text, not normalized text — normalization happens after detection
- [ ] Detection is based on Unicode character categories, not a hardcoded character list

---

## [ ] Issue #24 — `pattern_matcher.py`: urgency + authority social engineering patterns

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/rules/pattern_matcher.py` — regex-based detection of urgency and authority social engineering patterns in normalized text.

**Urgency patterns:** `"account suspended"`, `"immediate action required"`, `"within 24 hours"`, `"expires today"`, `"final notice"`, `"last chance"`, `"verify now"`, and variants.

**Authority impersonation patterns:** `"Canada Revenue Agency"` / `"CRA"`, `"Service Canada"`, `"RCMP"`, `"police"`, `"court order"`, `"government of canada"`, and variants.

Each match emits a `(code, display_string)` signal.

### Acceptance criteria

- [ ] `"Your account has been suspended. Verify now."` emits `urgency_language`
- [ ] `"CRA has issued a tax debt notice"` emits `authority_impersonation`
- [ ] A plain delivery notification with no urgency or authority language emits no signals
- [ ] Patterns are loaded from a config structure (not fully hardcoded in logic)
- [ ] Matching is case-insensitive and handles common punctuation variations

---

## [ ] Issue #25 — `pattern_matcher.py`: financial structuring + channel-shifting rules

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #24

### What to build

Extend `pattern_matcher.py` with two additional rule categories:

**Financial structuring:** gift card payment requests (`"iTunes gift card"`, `"Google Play card"`, `"Amazon gift card"`), cryptocurrency requests (`"Bitcoin"`, `"Ethereum"`, `"crypto wallet"`, `"send BTC"`), specific suspicious dollar amounts.

**Channel shifting:** requests to move the conversation off the current channel (`"WhatsApp"`, `"Telegram"`, `"Signal"`, `"contact us on"`, `"text us at"`).

### Acceptance criteria

- [ ] `"Send a $500 iTunes gift card"` emits `gift_card_request`
- [ ] `"Send Bitcoin to this wallet"` emits `crypto_request`
- [ ] `"Continue on WhatsApp: +1-800-..."` emits `channel_shifting`
- [ ] A message with none of these patterns emits no financial or channel-shifting signals
- [ ] Both rule sets share the same emit interface as the urgency/authority rules from #24

---

## [ ] Issue #26 — `rule_score` aggregator + `rule_reasons[]` output

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #20, #22, #23, #25

### What to build

A `RuleEngine.score(artifacts: dict) -> dict` function that:
1. Runs all Phase 1 rule modules (url_checker, unicode_detector, pattern_matcher, category_extractor) against the `artifacts{}` bundle
2. Collects all emitted `(code, display_string)` signals
3. Computes `rule_score` in `[0, 1]` as a weighted sum of signals (each signal has a configurable weight; score is clamped to 1.0)
4. Returns `{ "rule_score": float, "rule_reasons": [{"code": str, "display": str}, ...] }`

Signal weights live in a config file, not hardcoded in logic.

### Acceptance criteria

- [ ] A message with no signals returns `rule_score=0.0` and `rule_reasons=[]`
- [ ] A message with multiple high-weight signals returns `rule_score` approaching 1.0 (clamped, never exceeds 1.0)
- [ ] `rule_reasons` contains one entry per distinct signal that fired, with both `code` and `display` fields
- [ ] Identical input always produces identical output (deterministic)
- [ ] Signal weights are read from config, not hardcoded

---

## [ ] Issue #27 — FastAPI: `POST /v1/score` Phase 1-only stub

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #26

### What to build

Wire Phase 0 + Phase 1 into a working FastAPI endpoint at `POST /v1/score`. This is a stub that returns real Phase 0 and Phase 1 outputs but does not yet run Phase 2 or Phase 3 (those fields are `null` in the response). The endpoint is the primary integration point that proves the preprocessing and rule engine work end-to-end over HTTP.

**Request body:** `{ "text": string }`  
**Response:** `{ "rule_score": float, "rule_reasons": [...], "ml_score": null, "ai_score": null, "ai_explanation": null, "final_score": float }`

`final_score` equals `rule_score` in this stub since Phase 2 and 3 are absent.

### Acceptance criteria

- [ ] `POST /v1/score` with `{ "text": "Your Canada Post package requires verification. Click: parcel-xyz.top" }` returns `rule_score > 0` and non-empty `rule_reasons`
- [ ] `POST /v1/score` with a plain benign message returns `rule_score` near 0
- [ ] `ml_score`, `ai_score`, and `ai_explanation` are `null` in the response
- [ ] `final_score` equals `rule_score`
- [ ] Endpoint requires `X-API-Key` header (via #28)
- [ ] Invalid JSON body returns 422

---

## [ ] Issue #28 — FastAPI: X-API-Key middleware on `/v1/*` routes

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** None — start anytime

### What to build

FastAPI dependency or middleware that validates the `X-API-Key` request header on all routes under `/v1/`. The expected key is read from the `INTERNAL_API_KEY` environment variable. Missing or invalid keys return HTTP 401. The `/health` endpoint (if present) is exempt.

### Acceptance criteria

- [ ] Request with correct `X-API-Key` header passes through to the route handler
- [ ] Request with missing `X-API-Key` returns HTTP 401
- [ ] Request with incorrect `X-API-Key` returns HTTP 401
- [ ] `/health` (or equivalent) is accessible without an API key
- [ ] Key is read from the environment, not hardcoded

---

## Group 4 — Phase 2: ML Classifier

---

## [ ] Issue #29 — Download + preprocess UCI SMS Spam Collection into seed corpus

**Type:** chore / HITL  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

Download the UCI SMS Spam Collection dataset (~5,574 labeled ham/spam messages) from Kaggle or the UCI ML repository. Write a preprocessing script (`scripts/seed_data.py`) that reads the raw CSV, splits messages by label, and writes two JSON files:

- `backend/data/seed_scams.json`: array of spam message strings
- `backend/data/seed_legit.json`: array of ham message strings

Load both files into the `messages` table via `POST /v1/dataset/messages` (or direct SQL for seed bootstrap).

### Acceptance criteria

- [ ] `backend/data/seed_scams.json` exists with scam messages from the UCI dataset
- [ ] `backend/data/seed_legit.json` exists with legit messages from the UCI dataset
- [ ] Combined count is approximately 5,574 messages
- [ ] Both files contain only the raw message text (no labels, no metadata)
- [ ] Messages are seeded into the `messages` table with correct `source` and `label` values

---

## [ ] Issue #30 — `features.py`: TF-IDF pipeline on Phase 0 tokens

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #18, #29

### What to build

`backend/app/core/ml/features.py` — a TF-IDF vectorization pipeline using `scikit-learn TfidfVectorizer`. The vectorizer is fit on the seed corpus tokens (from Phase 0) and serialized to disk. At runtime it transforms a new message's Phase 0 tokens into a sparse feature vector. The top weighted features (terms with highest TF-IDF scores for this document) are extracted and returned as `ml_details`.

### Acceptance criteria

- [ ] `TfidfVectorizer` fits on the seed corpus and serializes to `backend/data/models/tfidf.pkl`
- [ ] `tfidf.pkl` loads at FastAPI startup without re-training
- [ ] `transform(tokens)` returns a sparse feature vector
- [ ] Top-N weighted features are extractable from the vector (for `ml_details`)
- [ ] Fitting on the same corpus twice produces identical serialized output (deterministic)

---

## [ ] Issue #31 — `sentiment.py`: NLTK SentimentIntensityAnalyzer signal

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/ml/sentiment.py` — a `score_sentiment(text: str) -> dict` function using NLTK's `SentimentIntensityAnalyzer`. Returns the compound score (overall sentiment in `[-1, 1]`) and the pos/neu/neg breakdowns. High negativity and urgency are secondary signals that modestly boost `ml_score` but never determine it alone.

NLTK `vader_lexicon` must be downloaded if not already present.

### Acceptance criteria

- [ ] `score_sentiment("Your account is suspended! Act now!")` returns a compound score below 0 (negative/urgent)
- [ ] `score_sentiment("Your package has been delivered.")` returns a compound score near 0 or positive
- [ ] Output dict contains `compound`, `pos`, `neu`, `neg` keys, all in expected ranges
- [ ] `vader_lexicon` download is handled gracefully at startup (not at import time)

---

## [ ] Issue #32 — `classifier.py`: train + serialize Naive Bayes model

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #30, #31

### What to build

`backend/app/core/ml/classifier.py` — trains a Naive Bayes classifier on the TF-IDF features from the seed corpus, incorporates the sentiment compound score as an additional feature, and serializes the trained model to `backend/data/models/classifier.pkl`. At FastAPI startup, the model loads from disk. `MLClassifier.score(artifacts, rule_hits) -> dict` returns `ml_score` in `[0, 1]` and `ml_details` (top TF-IDF features, sentiment score).

### Acceptance criteria

- [ ] Model trains on the seed corpus and serializes to `backend/data/models/classifier.pkl`
- [ ] Classifier achieves > 90% accuracy on a held-out 20% split of the seed corpus
- [ ] Model loads from disk at FastAPI startup without re-training
- [ ] `score()` returns `{ "ml_score": float, "ml_details": { "top_features": [...], "sentiment": float } }`
- [ ] A known spam message from the seed corpus scores `ml_score > 0.5`
- [ ] A known ham message from the seed corpus scores `ml_score < 0.5`

---

## [ ] Issue #33 — Integrate Phase 2 into FastAPI pipeline

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #27, #32

### What to build

Wire `MLClassifier.score()` into the scoring pipeline after Phase 1. The classifier receives the Phase 0 `artifacts{}` plus the Phase 1 `rule_reasons[]` as additional context. Update `POST /v1/score` to include `ml_score` and `ml_details` in the response. `final_score` is now `(rule_score + ml_score) / 2` as a placeholder until the full combiner in #39.

### Acceptance criteria

- [ ] `POST /v1/score` response includes non-null `ml_score` and `ml_details`
- [ ] Phase 1 `rule_reasons` are passed to the classifier as context
- [ ] `ai_score` and `ai_explanation` remain `null` (Phase 3 not yet integrated)
- [ ] `final_score` is the average of `rule_score` and `ml_score`
- [ ] Pipeline does not re-tokenize; it reuses Phase 0 tokens from `artifacts{}`

---

## Group 5 — Phase 3: Claude AI

---

## [ ] Issue #34 — `client.py` + `prompts.py`: Anthropic SDK + structured prompt

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** None — start anytime

### What to build

`backend/app/core/ai/client.py` — initializes the Anthropic Python SDK client using `ANTHROPIC_API_KEY` from the environment. `backend/app/core/ai/prompts.py` — builds the structured prompt that is sent to Claude. The prompt always includes: the original SMS, Phase 0 artifacts (extracted URLs, brand slug, category), Phase 1 signals that fired (rule codes and display strings), and Phase 2 outputs (ml_score, top TF-IDF features, sentiment score). Claude is instructed to return a JSON object with `ai_score` (float in `[0, 1]`) and `explanation` (plain-English string grounded in the signals provided).

Claude must never be called cold with just the raw SMS — all prior phase context is mandatory in every call.

### Acceptance criteria

- [ ] `ClaudeClient` initializes without error when `ANTHROPIC_API_KEY` is set
- [ ] `build_prompt(artifacts, rule_reasons, ml_output)` returns a prompt string containing all four inputs
- [ ] Calling `ClaudeClient.score(text, artifacts, rule_reasons, ml_output)` returns `{ "ai_score": float, "explanation": str }`
- [ ] `ai_score` is in `[0, 1]`
- [ ] `explanation` references at least one concrete signal from the provided artifacts or rule reasons
- [ ] Prompt instructs Claude to ground its reasoning in the provided signals, not general knowledge

---

## [ ] Issue #35 — Integrate Phase 3 into pipeline after Phase 2

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #33, #34

### What to build

Wire `ClaudeClient.score()` into the scoring pipeline after Phase 2. Claude receives the raw SMS, Phase 0 artifacts, Phase 1 rule reasons, and Phase 2 `ml_output`. Update `POST /v1/score` to include `ai_score` and `ai_explanation` in the response. `final_score` remains a placeholder average of all three until the real combiner in #39.

### Acceptance criteria

- [ ] `POST /v1/score` response includes non-null `ai_score` and `ai_explanation`
- [ ] Claude receives all Phase 0–2 outputs in its prompt (verifiable by logging the prompt in dev)
- [ ] `ai_explanation` is a non-empty plain-English string
- [ ] `final_score` is `(rule_score + ml_score + ai_score) / 3` as a placeholder
- [ ] Pipeline is sequential: Phase 2 completes before Phase 3 is called

---

## [ ] Issue #36 — SHA-256 dedup cache: skip Phase 3 for repeated messages

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #35

### What to build

Before calling Claude, compute a SHA-256 hash of the raw SMS text. Check an in-memory dict for a cached result keyed by this hash. On a cache hit, return the cached `ai_score` and `ai_explanation` without making an API call. On a miss, call Claude and store the result. The cache lives in memory for MVP (acceptable since it's a single Railway process).

### Acceptance criteria

- [ ] Submitting the same SMS text twice results in only one Claude API call
- [ ] The second submission returns the same `ai_score` and `ai_explanation` as the first
- [ ] Different SMS texts always trigger separate Claude API calls
- [ ] Cache key is the SHA-256 hash of the raw (pre-normalization) SMS text
- [ ] Cache miss path is unchanged from #35

---

## Group 6 — Stage 5: Combiner + Full API

---

## [ ] Issue #37 — SQLAlchemy ORM models: `Message` + `Analysis`

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #11

### What to build

`backend/app/models/message.py` and `backend/app/models/analysis.py` — SQLAlchemy ORM classes mapping to the `messages` and `message_analysis` tables respectively. The `Analysis` model has a `message` relationship back to `Message`. Both models use the UUID primary key pattern. Column types and constraints must match the Alembic migrations from #10 and #11 exactly.

### Acceptance criteria

- [ ] `Message` model maps to `messages` table with all columns and correct types
- [ ] `Analysis` model maps to `message_analysis` table with all columns and correct types
- [ ] `Analysis.message` relationship resolves to the parent `Message` row
- [ ] `Message.analyses` back-reference returns all analysis rows for a message
- [ ] Both models import cleanly; no circular import errors
- [ ] A `Message` row can be created and queried via an SQLAlchemy session against the local Postgres

---

## [ ] Issue #38 — Pydantic schemas: `MessageCreate`, `ScoringResult`, `AnalysisResult`

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #37

### What to build

`backend/app/schemas/message.py` and `backend/app/schemas/analysis.py` — Pydantic v2 models describing the API request and response payloads.

- `MessageCreate`: `{ text: str }` — validated input for `POST /v1/score`
- `ScoringResult`: full response from `POST /v1/score` — includes `message_id`, `rule_score`, `rule_reasons`, `ml_score`, `ml_details`, `ai_score`, `ai_explanation`, `final_score`, `model_version`
- `AnalysisResult`: full analysis detail response for `/v1/messages/{id}/analysis/latest`
- `MessageRead`: message row with latest `final_score` for the list endpoint

### Acceptance criteria

- [ ] `MessageCreate` rejects empty or whitespace-only `text`
- [ ] `ScoringResult` serializes all phase outputs; nullable fields (`ml_score`, `ai_score`, `ai_explanation`) default to `None`
- [ ] `AnalysisResult` includes all `message_analysis` columns
- [ ] Schemas import cleanly and are referenced by the FastAPI route handlers
- [ ] TypeScript types in `frontend/src/types/api.ts` match the Pydantic schemas

---

## [ ] Issue #39 — `combiner.py`: weighted `final_score` calculation

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #26, #33, #35

### What to build

`backend/app/core/scoring/combiner.py` — `combine(rule_score, ml_score, ai_score, weights=None) -> float` that computes a weighted average of all three phase scores. Default weights start equal (`1/3` each). Weights are configurable via a config value without touching pipeline logic. Result is clamped to `[0, 1]`.

### Acceptance criteria

- [ ] `combine(0.9, 0.8, 0.7)` returns a value between 0.7 and 0.9 (equal-weighted average ≈ 0.8)
- [ ] `combine(1.0, 1.0, 1.0)` returns `1.0`
- [ ] `combine(0.0, 0.0, 0.0)` returns `0.0`
- [ ] Result is always in `[0, 1]`
- [ ] Custom weights are accepted and applied correctly
- [ ] Weights do not need to sum to 1.0 (function normalizes internally)

---

## [ ] Issue #40 — Complete `POST /v1/score`: full pipeline + persist

**Type:** feat / AFK  
**Estimate:** ~3h  
**Blocked by:** #35, #37, #38, #39

### What to build

Wire the full four-phase pipeline into `POST /v1/score` and add database persistence. After all three phases run and `final_score` is computed, write one row to `messages` (with `source="user_submitted"`, `label="unknown"`, `category` from Phase 0) and one row to `message_analysis` (all phase scores, reasons, explanations, and `model_version`). Return a `ScoringResult` that includes `message_id` so the frontend can link to the detail page.

### Acceptance criteria

- [ ] `POST /v1/score` runs Phase 0 → Phase 1 → Phase 2 → Phase 3 → Combiner in sequence
- [ ] A `messages` row is written with `source="user_submitted"` and `category` from Phase 0
- [ ] A `message_analysis` row is written with all phase scores, `rule_reasons`, `ml_details`, `ai_explanation`, and `final_score`
- [ ] Response includes `message_id` (the UUID of the persisted `messages` row)
- [ ] `model_version` is set from an environment variable or config constant
- [ ] Submitting the same message twice creates two `message_analysis` rows (re-scoring is allowed; dedup cache only skips the Claude API call, not persistence)

---

## [ ] Issue #41 — `GET /v1/messages` + `GET /v1/messages/{id}` endpoints

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #40

### What to build

Two read endpoints for the message store:

- `GET /v1/messages?source=&label=&limit=50&cursor=` — paginated list. Returns `MessageRead` objects (message row + latest `final_score`). Cursor-based pagination using `created_at` + `id`.
- `GET /v1/messages/{id}` — single message detail. Returns the full message row plus its latest `message_analysis` row.

Both require `X-API-Key`.

### Acceptance criteria

- [ ] `GET /v1/messages` returns a list of messages, newest first
- [ ] `?source=user_submitted` filters correctly
- [ ] `?limit=10` returns at most 10 results
- [ ] Cursor-based pagination returns the correct next page
- [ ] `GET /v1/messages/{id}` returns the correct message and its latest analysis
- [ ] `GET /v1/messages/{id}` for an unknown ID returns HTTP 404

---

## [ ] Issue #42 — `GET /v1/messages/{id}/analysis/latest` endpoint

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #41

### What to build

`GET /v1/messages/{id}/analysis/latest` — returns the most recent `message_analysis` row for the given message ID as an `AnalysisResult`. "Most recent" is determined by `created_at DESC`. Returns HTTP 404 if the message does not exist or has no analysis rows.

### Acceptance criteria

- [ ] Returns the `message_analysis` row with the most recent `created_at` for the given message
- [ ] Returns HTTP 404 for an unknown `message_id`
- [ ] Returns HTTP 404 for a message that exists but has no analysis rows
- [ ] Response matches the `AnalysisResult` schema including all phase fields

---

## Group 7 — Stage 6: Frontend UI

---

## [ ] Issue #43 — Next.js server-side proxy route → FastAPI `POST /v1/score`

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #40

### What to build

A Next.js App Router route handler at `POST /api/score` that forwards requests to FastAPI's `POST /v1/score`. The handler reads `FASTAPI_URL` and `INTERNAL_API_KEY` from server-side environment variables, appends the `X-API-Key` header, and proxies the request. The FastAPI URL is never exposed to the browser. Error responses from FastAPI are forwarded with their original status codes.

### Acceptance criteria

- [ ] `POST /api/score` from the browser proxies to FastAPI `POST /v1/score`
- [ ] `X-API-Key` header is added server-side and never visible in browser network requests
- [ ] `FASTAPI_URL` is a server-only env var (not prefixed with `NEXT_PUBLIC_`)
- [ ] FastAPI 4xx/5xx responses are forwarded to the browser with their original status code
- [ ] `next build` completes without warnings about exposed secrets

---

## [ ] Issue #44 — `/demo` page: SMS form + loading state

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #43

### What to build

`frontend/src/app/demo/page.tsx` — the primary user-facing page. A centered textarea for pasting the suspicious SMS, a submit button, and a loading state while the analysis is running. The form clears after a successful submission. Uses `useState` for form input, loading flag, and result — no server components on the interactive form layer.

### Acceptance criteria

- [ ] Textarea accepts multi-line SMS input
- [ ] Submit button is disabled while the request is in flight
- [ ] A loading indicator (spinner or skeleton) is visible during the request
- [ ] The form does not submit if the textarea is empty
- [ ] On success, the result is displayed (wired to #45 and #46)
- [ ] On error, a user-facing error message is shown (not a raw stack trace)

---

## [ ] Issue #45 — `/demo` page: `ScoreCard` + rule reasons display

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #44

### What to build

`ScoreCard` component rendered on `/demo` after a successful submission. Displays:

- `final_score` as a percentage with a risk label (`Low`, `Medium`, `High`, `Very High`) and a corresponding color (green / yellow / orange / red)
- A list of `rule_reasons` — each reason shown as its human-readable `display` string, not the machine `code`

### Acceptance criteria

- [ ] `final_score` of 0.85 renders as `"85%"` with `"High"` label in an orange/red color
- [ ] `final_score` of 0.1 renders as `"10%"` with `"Low"` label in a green color
- [ ] Each `rule_reason` displays its `display` string (not the `code`)
- [ ] Empty `rule_reasons` renders the reasons section as hidden or with a "no rule signals" message
- [ ] Component is accessible: score value has an appropriate ARIA label

---

## [ ] Issue #46 — `/demo` page: Claude explanation panel

**Type:** feat / AFK  
**Estimate:** ~1h  
**Blocked by:** #45

### What to build

A panel below the `ScoreCard` that displays `ai_explanation` — Claude's plain-English reasoning for the score. The panel only renders when `ai_explanation` is non-null and non-empty. Include a visual indicator that this explanation is AI-generated.

### Acceptance criteria

- [ ] `ai_explanation` text is rendered in full when present
- [ ] Panel does not render when `ai_explanation` is `null` or empty
- [ ] A label or icon makes clear the explanation is AI-generated (e.g., "AI analysis" badge)
- [ ] Long explanations are readable at standard viewport widths without horizontal scroll

---

## [ ] Issue #47 — `/history` page: submission list with `final_score`

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #41, #43

### What to build

`frontend/src/app/history/page.tsx` — a server-fetched list of user-submitted messages via `GET /v1/messages?source=user_submitted`. Each row shows the message text snippet (truncated), the `final_score` as a colored badge, and a link to the `/messages/[id]` detail page. Fetched server-side (Next.js Server Component).

### Acceptance criteria

- [ ] Page fetches from `GET /v1/messages?source=user_submitted` server-side
- [ ] Each row shows a truncated message snippet, `final_score` badge, and a link to `/messages/[id]`
- [ ] `final_score` badge uses the same color coding as the `ScoreCard` from #45
- [ ] Page renders correctly with zero submissions (empty state message)
- [ ] Page does not expose `FASTAPI_URL` or `INTERNAL_API_KEY` to the client

---

## [ ] Issue #48 — `/messages/[id]`: full analysis detail view

**Type:** feat / AFK  
**Estimate:** ~2h  
**Blocked by:** #42, #43

### What to build

`frontend/src/app/messages/[id]/page.tsx` — full analysis detail for a specific message. Fetches `GET /v1/messages/{id}/analysis/latest` server-side. Displays:

- Full original SMS text
- `ScoreCard` with `final_score`
- Rule reasons list
- `ml_score` and top TF-IDF features (from `ml_details`)
- Claude explanation panel
- `model_version` and `created_at` timestamp

Returns a Next.js 404 page for unknown IDs.

### Acceptance criteria

- [ ] Full SMS text is displayed untruncated
- [ ] All three phase outputs are present: `rule_score`/reasons, `ml_score`/details, `ai_explanation`
- [ ] `model_version` and formatted `created_at` are visible
- [ ] An unknown `id` renders the Next.js 404 page (not a blank page or error)
- [ ] Page does not expose secrets to the client

---

## Group 8 — Stage 7: Testing + Polish

---

## [ ] Issue #49 — pytest: Phase 0 unit tests

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #14–#17

### What to build

Unit tests in `backend/tests/test_preprocessing.py` for all Phase 0 modules. Test only external behavior — given an input, assert the output. Do not test internal helper calls.

**Coverage targets:**
- `normalizer`: homoglyph flattening, zero-width removal, NFKD normalization, idempotency
- `url_extractor`: URL detection, pre-normalization preservation, edge cases
- `tokenizer`: token list correctness, n-gram generation, fuzzy matching thresholds

### Acceptance criteria

- [ ] All Phase 0 functions have at least three tests each (happy path + edge cases)
- [ ] Normalizer idempotency is tested (`normalize(normalize(x)) == normalize(x)`)
- [ ] URL extractor test covers: no URLs, one URL, multiple URLs, bare domain
- [ ] Fuzzy matcher test covers: exact match, near-miss above threshold, miss below threshold
- [ ] All tests pass with `pytest backend/tests/test_preprocessing.py`

---

## [ ] Issue #50 — pytest: Phase 1 unit tests

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #19–#26

### What to build

Unit tests in `backend/tests/test_rules.py` for all Phase 1 rule modules. Each rule module is tested with inputs that should and should not trigger signals.

**Coverage targets:** `category_extractor` (brand detection, keyword fallback, unknown default), `url_checker` (allowlist, denylist, suspicious TLD, brand-domain mismatch), `unicode_detector` (homoglyphs, zero-width), `pattern_matcher` (urgency, authority, financial, channel-shifting), `rule_score` aggregator (score range, reasons format).

### Acceptance criteria

- [ ] Each rule module has tests for true positive (signal fires) and true negative (signal does not fire) cases
- [ ] `rule_score` is always in `[0, 1]` for any combination of signals
- [ ] `rule_reasons` entries each have `code` and `display` keys
- [ ] Brand detection longest-match behavior is explicitly tested
- [ ] All tests pass with `pytest backend/tests/test_rules.py`

---

## [ ] Issue #51 — pytest: Phase 2 unit tests

**Type:** test / AFK  
**Estimate:** ~1h  
**Blocked by:** #30–#32

### What to build

Unit tests in `backend/tests/test_ml.py` for Phase 2 modules. The classifier test loads the pre-trained model from disk (not re-trains) — tests should verify inference behavior, not training.

**Coverage targets:** TF-IDF vectorizer (transforms tokens to a sparse vector), sentiment scorer (compound score range, directional correctness), classifier (known spam → `ml_score > 0.5`, known ham → `ml_score < 0.5`).

### Acceptance criteria

- [ ] TF-IDF test verifies the serialized vectorizer loads and transforms tokens without error
- [ ] Sentiment test verifies compound score is in `[-1, 1]` and a clearly urgent message scores negative
- [ ] Classifier test verifies a known seed spam message scores above 0.5 and a known seed ham message scores below 0.5
- [ ] Tests use the pre-trained model files from `backend/data/models/`; no re-training in tests
- [ ] All tests pass with `pytest backend/tests/test_ml.py`

---

## [ ] Issue #52 — pytest: `POST /v1/score` integration test (real DB, no mocks)

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #40

### What to build

Integration test in `backend/tests/test_api.py` that submits a known scam SMS to `POST /v1/score` against a real test database (local Postgres via docker-compose). Verifies the full pipeline runs end-to-end and that both `messages` and `message_analysis` rows are persisted correctly. No database mocking.

### Acceptance criteria

- [ ] Test submits a known scam SMS (from the UCI seed corpus) and asserts `final_score > 0.5`
- [ ] Test submits a known ham SMS and asserts `final_score < 0.5`
- [ ] After submission, a `messages` row with `source="user_submitted"` exists in the test DB
- [ ] After submission, a `message_analysis` row linked to the message exists with all phase scores populated
- [ ] Test DB is isolated from the production DB (uses a separate `DATABASE_URL`)
- [ ] No database or Claude API mocks — the test runs the real pipeline (Phase 3 may be stubbed with a fixed response if API costs are a concern)

---

## [ ] Issue #52.5 — pytest: GET `/v1/messages` + analysis endpoint tests

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #41, #42, #52

### What to build

Integration tests in `backend/tests/test_api.py` (same file as #52) for the three GET read endpoints. Uses the same real test database fixture established in #52. No mocking.

**Coverage targets:**
- `GET /v1/messages`: returns list newest-first; `?source=` filter works; `?limit=` respected; cursor pagination returns correct next page; requires `X-API-Key`
- `GET /v1/messages/{id}`: returns correct message + latest analysis; unknown ID returns HTTP 404
- `GET /v1/messages/{id}/analysis/latest`: returns most recent analysis row by `created_at`; message with no analysis rows returns HTTP 404; unknown `message_id` returns HTTP 404

### Acceptance criteria

- [ ] `GET /v1/messages` returns messages ordered by `created_at DESC`
- [ ] `?source=user_submitted` filters out seed messages
- [ ] `?limit=2` returns at most 2 results with a cursor for the next page
- [ ] `GET /v1/messages/{id}` for a seeded message returns HTTP 200 with the correct `message_id`
- [ ] `GET /v1/messages/{id}` for an unknown UUID returns HTTP 404
- [ ] `GET /v1/messages/{id}/analysis/latest` returns the most recent analysis row (verified by `created_at`)
- [ ] `GET /v1/messages/{id}/analysis/latest` for a message with no analysis rows returns HTTP 404
- [ ] All three endpoints return HTTP 401 without `X-API-Key`
- [ ] All tests pass with `pytest backend/tests/test_api.py`

---

## [ ] Issue #53 — Playwright E2E: `/demo` submission flow

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #44, #52

### What to build

Playwright end-to-end test that exercises the `/demo` page in a real browser against a running local stack. Pastes a known scam SMS into the form, submits it, and asserts the `ScoreCard` renders with a non-zero `final_score` and at least one rule reason.

### Acceptance criteria

- [ ] Test navigates to `/demo`, fills the textarea, and clicks submit
- [ ] Loading state is visible during the request
- [ ] `ScoreCard` renders after submission with a `final_score` percentage displayed
- [ ] At least one rule reason is listed
- [ ] No JavaScript console errors during the flow
- [ ] Test runs with `npx playwright test` against the local dev stack

---

## [ ] Issue #54 — pytest: Phase 3 unit tests

**Type:** test / AFK  
**Estimate:** ~2h  
**Blocked by:** #34, #35, #36

### What to build

Unit tests in `backend/tests/test_ai.py` for all Phase 3 modules: the prompt builder, the client wrapper, and the SHA-256 dedup cache. The Anthropic SDK client is stubbed — no real API calls are made.

**Coverage targets:**
- `prompts.py`: `build_prompt()` includes all four required context blocks (SMS text, Phase 0 artifacts, Phase 1 `rule_reasons`, Phase 2 `ml_output`)
- `client.py`: `score()` returns a dict with `ai_score` in `[0, 1]` and a non-empty `explanation` string (stubbed client)
- Dedup cache (#36): submitting the same text twice results in exactly one Claude API call; the second call returns the cached result; different texts each trigger their own call; cache key is SHA-256 of the raw pre-normalization text

### Acceptance criteria

- [ ] `build_prompt` test asserts all four context blocks are present in the returned string
- [ ] `score()` test with a stubbed Anthropic client returns `{ "ai_score": float, "explanation": str }` with correct types
- [ ] Dedup cache: mock confirms call count is 1 after two identical submissions
- [ ] Dedup cache: mock confirms call count is 2 after two different submissions
- [ ] Cache key is SHA-256 of raw (pre-normalization) text — verified by submitting two texts that normalize to the same string but differ in raw form (e.g., one with a homoglyph)
- [ ] All tests pass with `pytest backend/tests/test_ai.py`
