# Prism — System Architecture

## 1. Overview

Prism is a monorepo containing two services and one managed database:

| Service | Technology | Platform |
|---|---|---|
| Frontend | Next.js 15 (App Router) | Vercel |
| Backend | FastAPI (Python) | Railway |
| Database | Postgres + pgvector | Supabase |

The frontend never touches the database directly. All scoring logic, ML inference, and persistence live exclusively in FastAPI.

---

## 2. Component Diagram

```
┌─────────────────────────────────────────────────────┐
│                    User (Browser)                    │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS
┌────────────────────────▼────────────────────────────┐
│              Next.js Frontend (Vercel)               │
│  /demo   /history   /messages/[id]   /admin/*        │
│                                                      │
│  Server-side proxy route → FastAPI                   │
└────────────────────────┬────────────────────────────┘
                         │ HTTP (internal)
┌────────────────────────▼────────────────────────────┐
│              FastAPI Backend (Railway)               │
│                                                      │
│  POST /v1/score                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │  Phase 0: Preprocessing & Extraction         │   │
│  │  → normalized text, tokens, URLs,            │   │
│  │    brand slug, category, artifacts{}         │   │
│  └────────────────────┬─────────────────────────┘   │
│                       │ (artifacts flow down)        │
│  ┌────────────────────▼─────────────────────────┐   │
│  │  Phase 1: Rule Engine                        │   │
│  │  → rule_score, rule_reasons[]                │   │
│  └────────────────────┬─────────────────────────┘   │
│                       │ (all context flows down)     │
│  ┌────────────────────▼─────────────────────────┐   │
│  │  Phase 2: ML Classifier (NLTK + TF-IDF)      │   │
│  │  → ml_score, sentiment, TF-IDF weights       │   │
│  └────────────────────┬─────────────────────────┘   │
│                       │ (all context flows down)     │
│  ┌────────────────────▼─────────────────────────┐   │
│  │  Phase 3: Claude AI API                      │   │
│  │  → ai_score, plain-English explanation       │   │
│  └────────────────────┬─────────────────────────┘   │
│                       │                              │
│  ┌────────────────────▼─────────────────────────┐   │
│  │  Combiner: final_score                       │   │
│  │  weighted(rule_score, ml_score, ai_score)    │   │
│  └────────────────────┬─────────────────────────┘   │
│                       │                              │
│  Persist → messages + message_analysis               │
└───────────────────────┬─────────────────────────────┘
                        │ SQLAlchemy / psycopg2
┌───────────────────────▼─────────────────────────────┐
│              Supabase Postgres                       │
│  messages          message_analysis                  │
│  (pgvector ready for v2 RAG)                         │
└─────────────────────────────────────────────────────┘
```

---

## 3. API Boundary Diagram

Prism has two API layers. The browser calls the Next.js API routes on the same Vercel origin. Those route handlers run on the server, attach the private internal API key, and forward the request to FastAPI on Railway. FastAPI owns scoring, persistence, and all database access.

```
┌──────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                                                              │
│  User submits SMS from /demo                                 │
│                                                              │
│  fetch('/api/score', {                                       │
│    method: 'POST',                                           │
│    body: { text: '...' }                                     │
│  })                                                          │
│                                                              │
│  Browser can see: /api/score                                 │
│  Browser cannot see: INTERNAL_API_KEY, DATABASE_URL          │
└──────────────────────────────┬───────────────────────────────┘
                               │ Same-origin HTTPS
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                  Next.js Frontend (Vercel)                   │
│                                                              │
│  Route handler: POST /api/score                              │
│                                                              │
│  Reads server-only env vars:                                 │
│  - FASTAPI_URL                                               │
│  - INTERNAL_API_KEY                                          │
│                                                              │
│  Forwards request to FastAPI:                                │
│                                                              │
│  POST ${FASTAPI_URL}/v1/score                                │
│  X-API-Key: ${INTERNAL_API_KEY}                              │
│  Body: { text: '...' }                                       │
│                                                              │
│  Returns FastAPI response back to browser                    │
└──────────────────────────────┬───────────────────────────────┘
                               │ Server-to-server HTTPS
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Railway)                 │
│                                                              │
│  Endpoint: POST /v1/score                                    │
│                                                              │
│  Validates:                                                  │
│  - X-API-Key matches INTERNAL_API_KEY                        │
│                                                              │
│  Reads server-only env vars:                                 │
│  - DATABASE_URL                                              │
│  - ANTHROPIC_API_KEY                                         │
│  - INTERNAL_API_KEY                                          │
│                                                              │
│  Runs scoring pipeline:                                      │
│  Phase 0 → Phase 1 → Phase 2 → Phase 3 → Combiner            │
│                                                              │
│  Calls Claude with ANTHROPIC_API_KEY                         │
│  Persists results through DATABASE_URL                       │
└──────────────────────────────┬───────────────────────────────┘
                               │ SQL over pooled connection
                               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Supabase Postgres                         │
│                                                              │
│  DATABASE_URL uses transaction pooler, port 6543             │
│                                                              │
│  Tables:                                                     │
│  - messages                                                  │
│  - message_analysis                                          │
│                                                              │
│  pgvector enabled for future RAG retrieval                   │
└──────────────────────────────────────────────────────────────┘
```

### API boundary rules

- Browser code calls only same-origin Next.js routes like `/api/score`.
- Browser code never receives `INTERNAL_API_KEY`, `DATABASE_URL`, or `ANTHROPIC_API_KEY`.
- Next.js route handlers can read `FASTAPI_URL` and `INTERNAL_API_KEY` because they run server-side.
- FastAPI validates protected `/v1/*` requests using the `X-API-Key` header.
- FastAPI is the only service that connects to Supabase or calls Anthropic.
- Supabase is never accessed directly from the browser or frontend client components.

---

## 4. Scoring Pipeline — Sequential Data Flow

The pipeline is **sequential, not parallel**. Each phase enriches the context passed to the next.

### Phase 0 — Preprocessing & Extraction
- Input: raw SMS text
- Extracts all URLs before normalization
- Normalizes: lowercase, punctuation stripping, Unicode NFKD, homoglyph and zero-width character flattening
- Tokenizes text; generates bi-gram and tri-gram sequences; applies fuzzy matching (edit-distance) for near-miss brand/keyword detection
- Extracts brand slug and category (brand-first via `brand_variants.json`, keyword fallback, URL domain check via `allowed_domains.json`)
- Output: `artifacts{}` — extracted URLs, normalized text, tokens, n-grams, brand slug, category

### Phase 1 — Rule Engine
- Input: Phase 0 `artifacts{}`
- Scores deterministic rule signals against extracted artifacts (see `docs/rule_engine.md` for full signal list)
- Output: `rule_score [0,1]`, `rule_reasons[]`

### Phase 2 — ML Classifier
- Input: Phase 0 artifacts + Phase 1 rule hits
- TF-IDF weighting (`scikit-learn TfidfVectorizer`) on Phase 0 tokens
- NLTK sentiment scoring (urgency/negativity as secondary signal)
- Naive Bayes classifier (baseline), trained on UCI SMS Spam Collection; logistic regression is compared against it on the same split and adopted only if it wins (see `overview.md`, Stage 3 — Model selection)
- Output: `ml_score [0,1]`, `ml_details{}`

### Phase 3 — Claude AI API
- Input: raw SMS + Phase 0 artifacts + Phase 1 rule hits + Phase 2 outputs
- Sends a structured prompt — Claude is not called with raw SMS cold; it receives all detected signals as context
- **Grounding principle**: Claude is intentionally constrained to reason within the context we provide. It never scores a message in isolation or draws on general knowledge alone — every signal in its prompt is a concrete artifact extracted by Phases 0–2. In v2, RAG-retrieved examples from our confirmed scam corpus extend this boundary further, anchoring Claude's reasoning to patterns we curate and control.
- Contributes `ai_score` as one weighted input to the combiner; produces the human-readable explanation
- Output: `ai_score [0,1]`, `explanation` (plain English, grounded in actual detected artifacts)
- Provider: Claude (Anthropic)

### Combiner
```python
final_score = weighted_combiner(rule_score, ml_score, ai_score)
```
Weights start equal; tune after evaluation data accumulates.

---

## 5. Frontend Architecture

### Pages
| Route | Purpose |
|---|---|
| `/demo` | SMS submission form + score result |
| `/history` | List of past submissions with `final_score` |
| `/messages/[id]` | Full analysis detail (all three phase outputs) |
| `/admin/datasets` | Seed data management (optional) |
| `/admin/eval` | Metrics dashboard (optional) |

### Key decisions
- **No client-side state management (no Zustand).** All data lives in the database; Next.js Server Components fetch on demand. The only client state on `/demo` is `useState` for form input, loading, and result.
- **shadcn/ui** (Radix UI primitives) provides accessible components out of the box — WCAG AA keyboard navigation and ARIA semantics built in.
- **Server-side proxy route** in Next.js forwards requests to FastAPI. The backend URL is never exposed to the browser.

### Tech stack
- Next.js 15 (App Router, Server Components)
- TypeScript
- TailwindCSS
- shadcn/ui + Lucide React

---

## 6. Backend Architecture

### Directory layout (FastAPI)
```
backend/app/
├── main.py                  # App entry point, CORS, router inclusion
├── core/
│   ├── preprocessing/       # Phase 0: shared extraction layer
│   │   ├── normalizer.py    # Lowercase, punctuation, unicode/homoglyph flattening
│   │   ├── url_extractor.py
│   │   ├── tokenizer.py     # Tokenization, n-grams, fuzzy matching
│   │   └── extractor.py     # Brand/category detection entry point
│   ├── rules/               # Phase 1: rule engine
│   │   ├── category_extractor.py
│   │   ├── url_checker.py
│   │   └── config/          # JSON config files (brand_variants, category_keywords, allowed_domains)
│   ├── ml/                  # Phase 2: NLTK classifier + TF-IDF
│   │   └── classifier.py
│   └── scoring/             # Pipeline orchestration + combiner
│       ├── pipeline.py      # Runs Phase 0 → 1 → 2 → 3 sequentially
│       └── combiner.py
├── api/v1/endpoints/        # Route handlers
│   ├── scoring.py           # POST /v1/score
│   ├── messages.py          # GET /v1/messages
│   └── dataset.py           # Admin dataset endpoints
├── models/                  # SQLAlchemy ORM classes
└── schemas/                 # Pydantic request/response models
```

### Config loading
Rule engine config (`brand_variants.json`, `category_keywords.json`, `allowed_domains.json`) loads from disk at FastAPI startup. No database tables required for rule definitions until an admin UI is needed.

### Dependency chain
```
POST /v1/score
  → pipeline.run(text)
      → Preprocessor.extract(text)                              # Phase 0
      → RuleEngine.score(artifacts)                             # Phase 1
      → MLClassifier.score(artifacts, rule_hits)                # Phase 2
      → ClaudeClient.score(text, artifacts, rule_hits, ml_out)  # Phase 3
      → Combiner.combine(rule_score, ml_score, ai_score)
  → MessageRepository.save(message, analysis)
  → return ScoringResult
```

---

## 6. Database

See `docs/database.md` for full schema.

Core tables:
- **`messages`** — every SMS (seed scam, seed legit, user submitted). Source and label tracked per row.
- **`message_analysis`** — one row per scoring run. All three phase scores, reasons, and model version stored.

Supabase was chosen over plain Railway Postgres for two reasons:
1. **Supabase Studio** — table editor for manually curating seed scam data
2. **pgvector extension** — natively available, required for v2 RAG pipeline with no migration needed

---

## 7. External Integrations

| Integration | Purpose | When |
|---|---|---|
| Claude API (Anthropic) | Phase 3 scoring + explanation text | Every `/v1/score` call |
| Supabase Postgres | Persistent storage | Every request |
| pgvector | Embedding similarity search for RAG | v2 |

---

## 8. v2 RAG Pipeline (Post-MVP)

**Why RAG**: Even with Phase 0–2 artifacts in the prompt, Claude's baseline reasoning draws on general knowledge. RAG closes this gap by injecting confirmed scam examples from our own corpus — forcing Claude to reason against patterns we curate and verify, not patterns from its training data. This keeps Phase 3's scoring and explanations anchored to real-world scam behavior we control.

The RAG pipeline runs at inference time and enriches Phase 3's Claude prompt with retrieved domain context:

```
Incoming SMS
  → embed with sentence-transformers
  → pgvector similarity search against confirmed scam corpus
  → top-K similar known scams retrieved
  → injected into Phase 3 Claude prompt as context
  → Claude reasons with domain-specific examples, not just general knowledge
```

The self-training loop is **post-MVP** and runs periodically (batch, not real-time).

**Moderated queue (v2):**
1. User submits SMS → pipeline scores it → if `ai_score > 0.85`, the message is flagged and written to `messages` with `label: pending_review`
2. Admin reviews the pending queue and approves or rejects each entry
3. Approved entries are relabeled `scam`, fed into the next Phase 2 retraining batch, and added to the pgvector RAG store
4. Phase 3's `ai_score` is used as the pseudo-label — not `final_score` — to avoid a circular feedback loop where the ML score influences the final score which then becomes the ML training signal

**Confidence-gated auto-approval (v3):**
- Entries where `ai_score > 0.97` bypass the review queue and are auto-approved
- At this threshold the false positive rate is negligible, reducing admin burden at scale
- All auto-approved entries are still written to an audit log

---

## 9. Future: Jev Triage Gate (Post-MVP)

**Status: not implemented.** Original Phases 0–3 ship first; this is a later addition once the core pipeline is stable.

[Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (TypeSafe AI) is a "System-1" model: no autoregressive text generation, returns typed classifications with calibrated probability + confidence scores over a fixed, predefined answer space. ~70–500ms latency, near-zero cost per call. No natural-language rationale — numbers only.

**Where it fits**: a triage gate inserted between Phase 2 and Phase 3.

```
Phase 0 → Phase 1 → Phase 2
                       │
                       ▼
           ┌───────────────────────┐
           │  Jev Triage Gate      │
           │  Choice: scam | legit │
           │  + confidence score   │
           └───────┬───────┬───────┘
                    │       │
        high confidence   low confidence
        (either class)    / borderline
                    │       │
                    ▼       ▼
          skip Phase 3   Phase 3 (Claude)
          use Jev score  full reasoning +
          as final input explanation
```

Rationale: most submissions are not borderline — Jev can resolve the easy majority at a fraction of Claude's cost/latency, reserving the expensive Phase 3 call (and its explanation text) for cases that actually need reasoning. Confidence threshold TBD from eval data.

**Explicit non-goal**: Jev does not replace Phase 3. It cannot produce the plain-English explanation shown to users — that's structurally out of scope for a numbers-only classifier. It only gates whether Phase 3 runs.

---

## 10. Security Baseline

- FastAPI backend URL never exposed to the browser (Next.js proxy)
- All DB credentials held exclusively by Railway/FastAPI — Supabase RLS enforced
- Input sanitization on all user-submitted text before pipeline entry
- Claude API key stored as Railway environment variable
- Rate limiting on `/v1/score` to prevent abuse
