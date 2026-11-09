# Prism — Project Overview

## Goal
Prism detects scam SMS messages and returns a **scam likelihood (%)** with explainable reasons.

Core design: a **four-phase sequential intelligence pipeline**:
- **Phase 0**: Preprocessing & extraction (normalization, URL extraction, tokenization, brand/category classification)
- **Phase 1**: Deterministic rule engine (scores Phase 0 artifacts against known signal patterns)
- **Phase 2**: NLTK-trained ML classifier (TF-IDF features, Naive Bayes, sentiment scoring)
- **Phase 3**: Claude AI API (receives all Phase 0–2 artifacts → contributes `ai_score` + human-readable explanation)

Each phase enriches the context passed to the next. The final score is a weighted combination of all three.

The system stores:
- Seed **100% scam** messages (UCI SMS Spam Collection + others)
- Seed **legit (ham)** messages
- **User-submitted** messages
- Per-run **analysis outputs** (scores + explanations)

---

## System-level MVC

Treat the whole system as one MVC in a monorepo:
- **Model**: Supabase Postgres (`messages`, `message_analysis`)
- **Controller**: FastAPI in `/backend` (authoritative scoring + persistence)
- **View**: Next.js in `/frontend` (submission, history, detail, admin surfaces)

### Responsibility mapping
- **View (Next.js)**: Presents `/demo`, `/history`, `/messages/[id]`, and admin surfaces. Never talks to Postgres directly — calls FastAPI endpoints only.
- **Controller (FastAPI)**: Runs all three pipeline phases, combines scores, persists `messages` and `message_analysis`, exposes REST API (`/v1/score`, `/v1/messages`, admin routes).
- **Model (Supabase Postgres)**: Stores all SMS (`messages`) and scoring history (`message_analysis`). FastAPI is the only service with DB credentials. `pgvector` extension enabled for v2 RAG pipeline.

---

## Architecture

### Components
- **Next.js in `/frontend` (View/UI)**
  - App Router pages and routes
  - Form UX and score visualization
  - Server-side proxy to FastAPI (avoids CORS, hides backend URL)
- **FastAPI in `/backend` (Controller/Scoring API)**
  - Three-phase scoring pipeline
  - Score combination into a single probability output
  - Database reads/writes
  - Dataset management endpoints (seed data)
- **Supabase Postgres (Model)**
  - `messages` + `message_analysis` as durable source of truth
  - `pgvector` extension ready for v2 RAG pipeline

### Deployment
| Service | Platform |
|---|---|
| Next.js frontend | Vercel |
| FastAPI backend | Railway |
| Postgres database | Supabase |

### Why this split
- Next.js excels at building and presenting the product.
- Python/FastAPI is the right environment for ML workflows and NLP tooling.
- FastAPI as the authority keeps scoring logic consistent and reproducible.
- Monorepo structure simplifies development while maintaining clear separation of concerns.

---

## Scoring Pipeline

### Inputs
- SMS `text` (primary)
- Optional metadata (future): locale, timestamp, sender

### Phase 0 — Preprocessing & Extraction (FastAPI)
Purpose: normalize the raw SMS and extract structured artifacts consumed by all downstream phases.

#### Steps:
1. **URL Extraction** — pull all URLs from raw text before normalization distorts them
2. **Normalization** — lowercase conversion, punctuation stripping, Unicode NFKD normalization, homoglyph and zero-width character flattening (`unidecode`, `unicodedata`)
3. **Tokenization, N-grams & Fuzzy Matching** — split into word tokens; generate bi-gram and tri-gram sequences for phrase detection; apply fuzzy matching (edit-distance) to catch near-miss brand names and keyword variants that exact matching would miss
4. **Brand & Category Extraction** — match tokens against `brand_variants.json` aliases (exact spaced, then exact joined, then fuzzy fallback ≥85 for aliases 6+ chars); check link domains against each brand's `domains`, also in `brand_variants.json`; fall back to keyword density scoring against `category_keywords.json` (#20, not yet implemented)

Phase 0 outputs (the `artifacts{}` bundle passed to all subsequent phases):
- `extracted_urls[]`
- `normalized_text`
- `tokens[]`, `ngrams[]`
- `brand_slug` (or `null`), `text_brand_slug`, `url_brand_slug`
- `category` (`delivery | banking | government | ... | unknown`)
- `brand_match_type` (`url | exact | fuzzy | None`), `brand_confidence`

**Post-MVP (Jev):** an optional step can add Jev's category, brand and urgency/threat probabilities to `artifacts{}` under a `jev` key, alongside the keyword-based fields (issue #58, behind a config flag, after the #56 go/no-go). See `architecture.md`, section 9.

---

### Phase 1 — Deterministic Rule Engine (FastAPI)
Inputs: Phase 0 `artifacts{}` bundle.
Purpose: high-precision detection and explainability.

Outputs are passed to Phase 2 and Phase 3 as additional context.

#### Rule signals:
1. **URL Analysis** — typosquatting, suspicious TLDs, shorteners, IP address links, brand-domain mismatch
2. **Text Obfuscation** — homoglyphs (Cyrillic substitution), inserted noise, mathematical alphanumerics
3. **Social Engineering** — urgency ("account suspended"), authority impersonation (CRA, police), scarcity/reward
4. **Sender Metadata** — email-to-SMS from free domains, country code mismatch
5. **Formatting & Style** — emoji abuse, excessive punctuation, all-caps, visual spacing tricks
6. **Channel Shifting** — "contact us on WhatsApp/Telegram/Signal"
7. **Financial Structuring** — gift cards, crypto, Bitcoin, specific dollar amounts
8. **Phone Number Extraction** — mismatched callback numbers

#### Category extraction:
- **Brand-based** (primary): match normalized tokens against `brand_variants.json` → resolves category definitively (e.g., "Canada Post" → `delivery`)
- **Keyword-based** (fallback): score against `category_keywords.json` n-gram phrases; highest density wins above threshold
- **Default**: `unknown` — prevents category-specific strict rules from firing on generic messages

Phase 1 outputs:
- `rule_score` in `[0, 1]`
- `rule_reasons[]` (machine-readable codes + display strings)
- Extracted artifacts: detected URLs, brand slug, category, flags

Config files (`brand_variants.json`, `category_keywords.json`) live in `backend/app/core/rules/config/` and load at FastAPI startup. No DB tables required for rule definitions until an admin UI is needed.

### Phase 2 — ML Classifier (FastAPI)
Inputs: Phase 0 `artifacts{}` (normalized text, tokens, n-grams) + Phase 1 rule hits.

Approach: **NLTK-based trained classifier** on labeled scam datasets.
- Receives normalized tokens and n-grams from Phase 0 (no re-tokenization)
- **TF-IDF weighting** (`scikit-learn TfidfVectorizer`) — weights keywords by frequency in message vs. corpus; down-weights common words, up-weights rare scam-specific terms
- **Naive Bayes classifier** (baseline) → Logistic Regression (upgrade) trained on labeled corpora
- **Sentiment scoring** (`NLTK SentimentIntensityAnalyzer`) — urgency and negativity/threat level as a secondary signal; boosts confidence modestly but never decides alone

Training data: a multi-source seed corpus (see [Seed & Reference Datasets](#seed--reference-datasets)). Scam examples come mainly from the NCSU gateway dataset, Smishtank and the Reddit OCR corpus; UCI SMS Spam Collection supplies ham and generic spam vocabulary. Every row carries its origin dataset so the classifier can be validated per source. Additional Canadian/international datasets are added as text-level data becomes available (CAFC, FTC feeds currently lack raw message text).

Phase 2 outputs:
- `ml_score` in `[0, 1]`
- `ml_details` (TF-IDF feature weights, category confidence, sentiment signal)

**Post-MVP (Jev):** Jev (TypeSafe AI) is evaluated as a third Phase 2 candidate against Naive Bayes and logistic regression, using the same protocol (issue #59). If it passes the upgrade criterion it can replace or supplement `ml_score` behind a config flag, with the local model as fallback. A triage gate (issue #60) may also use a confident classification to skip Phase 3. All Jev work depends on the #56 spike (privacy terms, zero-shot accuracy, injection test). See `architecture.md`, section 9.

### Phase 3 — Claude AI API (FastAPI)
Inputs: raw SMS + Phase 0 artifacts + Phase 1 rule hits + Phase 2 outputs.

Phase 3 is **not a cold call** to the AI. Claude is intentionally constrained to reason within the context we provide — it never scores a message in isolation or draws on general knowledge alone. Every signal in its prompt is a concrete artifact extracted by Phases 0–2. In v2, RAG-retrieved examples from our confirmed scam corpus extend this boundary further.

Claude receives a structured prompt containing:
- The original SMS
- Phase 0 artifacts: extracted URLs, brand slug, category
- Phase 1 rule signals that fired (e.g., brand-domain mismatch, suspicious TLD, urgency patterns)
- Phase 2 outputs: `ml_score`, TF-IDF feature evidence, sentiment score
- Retrieved examples from RAG store (v2 — not MVP)

Claude produces:
- `ai_score` in `[0, 1]` — independent scoring contribution fed into the combiner
- `explanation` — human-readable plain-English reasoning grounded in the specific signals detected across all phases

Provider: **Claude (Anthropic)**.

### Combining into a final score
All three scores combine into `final_score`:

```
final_score = weighted_combiner(rule_score, ml_score, ai_score)
```

Weights are tunable. Rule engine carries highest precision; Claude carries highest contextual recall. Baseline starts equal-weighted; tune once evaluation data exists.

Optional overrides (future):
- Clamp `final_score` upward for extremely high-confidence rule hits
- Probability calibration once sufficient labeled data accumulates

---

## Data Model (Supabase Postgres)

### Core tables
See `docs/database.md` for full schema with column types and indexes.

- **`messages`** — every SMS that enters Prism. `source`: `seed_scam | seed_legit | user_submitted`. `label`: `scam | legit | unknown`.
- **`message_analysis`** — one row per scoring run. Stores `rule_score`, `rule_reasons`, `ml_score`, `ml_details`, `ai_score`, `ai_explanation`, `final_score`, `model_version`.

Config (`brand_seeds`, `category_keywords`) lives in backend JSON files for MVP. Migrates to Supabase admin tables when an admin UI is needed.

### Embeddings (v2)
- `pgvector` extension enabled on Supabase from the start
- Embeddings stored in `message_embeddings` table (supports versioning/re-embedding)
- Powers RAG retrieval for Phase 3 context

---

## API Surface (FastAPI)

### Public scoring
- `POST /v1/score` — input: `{ text: string }` → scores via all three phases, persists message + analysis, returns full result

### Message browsing
- `GET /v1/messages?source=&label=&limit=&cursor=`
- `GET /v1/messages/{id}`
- `GET /v1/messages/{id}/analysis/latest`

### Dataset management (admin)
- `POST /v1/dataset/messages` — add seed scam/legit
- `PATCH /v1/dataset/messages/{id}` — update label/metadata
- `POST /v1/dataset/reindex` — recompute embeddings (v2)

### Evaluation (future)
- `POST /v1/eval/run`
- `GET /v1/eval/latest`

---

## Next.js Pages (View)

- `/demo` — submit SMS, render score + explanations
- `/history` — list of user-submitted messages and their latest `final_score`
- `/messages/[id]` — message detail, full analysis payload
- `/admin/datasets` (optional) — seed scam/legit management
- `/admin/eval` (optional) — metrics dashboard

---

## Request Flow

1. User submits SMS in Next.js.
2. Next.js calls FastAPI `POST /v1/score` via server-side proxy route.
3. FastAPI runs Phase 1 (rules) → Phase 2 (ML, receives Phase 1 context) → Phase 3 (Claude, receives Phase 1+2 context).
4. FastAPI combines scores → writes `messages` + `message_analysis`.
5. Next.js renders `final_score` + `ai_explanation` + rule reasons.

---

## Libraries and Frameworks

### Frontend (Next.js)
- **Next.js 15** — React framework, App Router
- **TypeScript** — type safety
- **TailwindCSS** — styling
- **shadcn/ui** — accessible component library (built on Radix UI primitives, WCAG AA)
- **Lucide React** — icons

### Backend (FastAPI)
- **FastAPI** — Python web framework
- **Uvicorn** — ASGI server
- **Pydantic** — data validation and serialization
- **SQLAlchemy** — ORM for Postgres
- **Alembic** — database migrations
- **psycopg2-binary** — Postgres driver

### ML/NLP Libraries
- **NLTK** — tokenization, lemmatization, sentiment, Naive Bayes classifier
- **scikit-learn** — TF-IDF vectorization (`TfidfVectorizer`), logistic regression, feature extraction, evaluation utilities
- **rapidfuzz** — fuzzy string matching for near-miss brand/keyword detection
- **numpy/pandas** — data manipulation
- **tldextract** — URL domain parsing (public suffix list)
- **unicodedata / unidecode** — Unicode normalization and homoglyph flattening
- **regex** — pattern matching

### AI
- **Anthropic Python SDK** — Claude API integration for Phase 3

### Database
- **Supabase Postgres** — primary data store
- **pgvector** — vector similarity search (v2 RAG pipeline)

### Development Tools
- **pytest** — testing framework
- **black/ruff** — code formatting and linting
- **pre-commit** — git hooks

---

## Privacy & Data Retention (Pre-launch TODOs)
- **Raw text storage**: User-submitted SMS is stored as-is in `messages.text` for MVP. This may contain PII (phone numbers, names).
- **Pre-launch**: Define a data retention policy (e.g. auto-delete user-submitted messages after 90 days) and evaluate PII stripping before any public launch.
- **Seed data**: Seed scam/legit messages are not user-submitted and are retained indefinitely.

## Seed & Reference Datasets

### Training sources (evaluated 2026-09-29)

No public dataset of raw Canadian scam SMS was found. The best public sources of raw scam text, and how each is used:

| Source | Content | Licence | Role in Prism |
|---|---|---|---|
| **NCSU "On SMS Phishing Tactics and Infrastructure"** ([wspr-ncsu/sms-phishing](https://github.com/wspr-ncsu/sms-phishing)) | About 159k lines of raw phishing SMS collected from public SMS gateways, confirmed by VirusTotal/APWG. Fields: message, destination number, timestamp. Scam only. | MIT | Primary scam source. |
| **Smishtank** ([smishtank.com/dataset](https://smishtank.com/dataset)) | 1,090 validated submissions with sender, body, brand, URLs, VirusTotal and WHOIS data. US-leaning. Text comes from screenshots run through OCR, so expect some noise. | CC BY-NC-SA 4.0 (non-commercial, share-alike) | High-quality scam source. Check licence terms before any commercial or public release. |
| **UCI SMS Spam Collection** | About 5.5k UK/Singapore SMS from around 2010: 4.8k ham, about 750 spam. | Research use | Only sizable public ham source. Also gives generic spam vocabulary and a neutral tone baseline for sentiment. |
| **Reddit mobile-scam corpus** ([mms-characterization](https://github.com/mobile-scam-analysis/mms-characterization), paper arXiv 2605.16656) | 7 zipped CSVs (about 83 MB) of OCR text from screenshots posted to Reddit. US-style scams (IRS, DMV, E-ZPass tolls, USPS) and conversational scams (wrong-number, romance); few Canadian brands. Columns include `Extracted Text`, `timestamp`, `cluster`. Only part 1 (about 20.5k rows) was inspected. | No licence in repo (all rights reserved by default); user-generated Reddit content | Supplementary scam source. Noisy: OCR includes phone status bars and app UI text, and many rows are not scam or not SMS, so a scam filter is required. Use `Extracted Text` (the "Semantically Cleaned" column strips too much). Internal use only; do not redistribute. |

Not used: the Mendeley 5,971-message SMS Phishing Dataset (and its HuggingFace mirrors), because its ham and spam come from UCI and would leak between train and test; ScamShield (India-focused, English/Hindi/Hinglish); `all-scam-spam` (43 languages, mixed email and SMS).

**NCSU data caveats.** Mixed geography (UK, Austria and US numbers) and heavy gambling spam. Filter to `+1` destination numbers, drop gambling promotions, and deduplicate near-identical campaign messages before training.

**Known gap: legitimate transactional SMS.** No public source provides real US/Canadian legitimate notifications (carrier notices, bank alerts, 2FA codes, appointment reminders). Sources to fill it: consented, PII-scrubbed messages from friends and family; template-based synthetic ham built from real brand formats and the `brand_variants.json` domains. UCI ham (casual chat) is only a weak substitute.

### Rules for training on this mix

The scam sources are transactional and link-heavy, while UCI ham is casual chat with no links. Trained naively, the classifier learns dataset style ("has a URL, looks formal, so scam") instead of scam behavior, and real legitimate notices get flagged.

1. Tag every row with its origin dataset in addition to `source` and `label`.
2. Validate leave-one-source-out (for example, train without Smishtank and test on it). A sharp drop means the model learned dataset style.
3. Include transactional ham (see the gap above) so URLs and formal tone are not a scam-only signal.
4. Consider masking URLs to a `<URL>` token in Phase 2 features. Phase 1 already scores URLs, so Phase 2 does not need them.
5. Keep UCI's weight modest and report metrics per source.
6. Judge the model on a frozen, hand-labeled Canadian-style held-out set (see architecture review, gap 4), not on a random split of the training corpus.

### Other reference sources

- **Canadian Anti-Fraud Centre (CAFC)** — monthly intelligence bulletins. Currently lacks raw text-level data; monitor for future access.
- **FTC Consumer Sentinel Network** — Sentinel exports tagged as *Text Message Scam*. Monitor for text-level data.
- **UK NCSC 7726 Program** — curated smishing templates from carrier-forwarded reports.
- **NUS SMS Spam Corpus v0.1** — operator-verified complaints.

---

## Roadmap

### v1 (MVP) — Implementation Stages

#### Stage 1: Core Infrastructure
- Monorepo structure with `/frontend` (Next.js) and `/backend` (FastAPI) ✅
- FastAPI project with basic structure and essential dependencies ✅
- Configure PostgreSQL core tables (`messages`, `message_analysis`) via Supabase + Alembic
- CORS setup and API health check endpoint
- Next.js project with TypeScript, TailwindCSS, shadcn/ui

#### Stage 2: Preprocessing & Rule Engine (Phase 0 + Phase 1)
- Phase 0: URL extraction, normalization (lowercase, punctuation, homoglyph flattening), tokenization, n-grams, fuzzy matching
- Category extraction pipeline: brand detection + keyword scoring ✅ (in progress)
- URL analysis: allowlist/denylist, suspicious TLD, brand-domain mismatch ✅ (in progress)
- Additional rule signals: homoglyph detection, urgency patterns, financial structuring
- Rule scoring and `rule_reasons[]` generation
- Rule engine endpoints in FastAPI

#### Stage 3: ML Classifier (Phase 2)
- Build the multi-source seed corpus (NCSU, Smishtank, Reddit OCR, UCI, transactional ham) and a frozen Canadian-style held-out evaluation set
- NLTK feature pipeline: tokenize → lemmatize → n-grams → sentiment
- Train and evaluate classifier (Naive Bayes baseline, logistic regression upgrade) — see **Model selection** below
- Integrate classifier into FastAPI scoring pipeline (receives Phase 1 context)
- Store `ml_score` and `ml_details` in `message_analysis`

**Model selection (Naive Bayes vs. logistic regression)**

Naive Bayes is built first as the baseline: cheap, fast to train, and sets the score logistic regression must beat. Logistic regression is not assumed to win; it replaces Naive Bayes only if the comparison below supports it.

- **Why logistic regression may win:** Naive Bayes treats every feature as independent evidence, so correlated features (e.g. overlapping Phase 1 rule hits, co-occurring words like "verify"/"account"/"suspended") are double-counted and `ml_score` tends toward overconfident 0/1 values. Logistic regression fits all weights jointly and usually yields better-calibrated probabilities. `ml_score` feeds the weighted combiner, so score quality matters more than headline accuracy.
- **Comparison method:** train both models on the same data, using identical TF-IDF + sentiment + Phase 1 features and a fixed random seed. The data is the multi-source corpus (NCSU, Smishtank, Reddit OCR, UCI, transactional ham; see Seed & Reference Datasets), split stratified by label **and** origin dataset. Evaluate three ways: (1) the random split, as a sanity check only; (2) **leave-one-source-out**, training without one scam dataset and testing on it, with results reported per source; (3) the frozen Canadian-style held-out set (`eval_holdout.json`), which is never used for training or vectorizer fitting. Decide between models on (2) and (3), not (1).
- **Metrics:** report precision, recall, and F1 for the scam class, plus a confusion matrix, per origin dataset and on the held-out set. Do **not** rely on accuracy alone: class balance depends on how the corpus is mixed (NCSU is scam-only and large, UCI is about 87% ham), so a trivial classifier can score well on any single split. Report the false-positive rate on transactional ham (legitimate messages with URLs and brand names) separately. Check calibration (reliability curve or Brier score) on the held-out set.
- **Error costs (FP vs. FN):** a false negative (real scam scored as safe) is the costly error: the user may act on it, and the app targets vulnerable users. A false positive (legitimate message scored as scam) is cheaper per message but erodes trust if frequent. Scam-class recall is therefore weighted above precision. Phase 1 rules and Phase 3 (Claude) can still catch a Phase 2 false negative, since `ml_score` is only one combiner input.
- **Error inspection:** for each model, read the actual false-positive and false-negative messages, not just the counts, to see what wording each model misses or over-flags.
- **Threshold comparison:** compare models at the default 0.5 cutoff, then at a lower cutoff chosen to raise scam-class recall. Report FP and FN counts at each, since the cutoff trades one error for the other.
- **Reuse for Jev (post-MVP):** the same split, confusion matrix, FP/FN inspection and threshold protocol should be used to evaluate a Jev triage gate against Phase 2, so all candidates are compared on identical terms.
- **Upgrade criterion:** switch to logistic regression if it improves scam-class recall or F1 without a meaningful precision drop, or if it is clearly better calibrated at similar F1. If results are within noise, keep Naive Bayes for simplicity.
- **Known limits:** no public corpus contains Canadian scam text at scale, and UCI is small, dated, and UK/Singapore-based. The scam sources are US-leaning, and transactional ham is partly synthetic, so results may not transfer to current Canadian smishing. Treat metrics as a relative comparison between models, not an absolute quality guarantee. Phase 3 (Claude) covers wording the corpus never saw.
- **Deferred:** formal probability calibration (e.g. Platt scaling) and combiner weight tuning stay post-MVP until real evaluation data exists.

#### Stage 4: Claude AI Integration (Phase 3)
- Anthropic SDK integration
- Structured prompt template: Phase 1 signals + Phase 2 score → Claude
- Claude returns `ai_score` (numeric) + `explanation` (text)
- Integrate into sequential pipeline after Phase 2

#### Stage 5: Score Combiner & Full API
- Implement `final_score` combiner (`rule_score`, `ml_score`, `ai_score`)
- Complete `POST /v1/score` endpoint with full three-phase pipeline
- Message and analysis persistence
- Message browsing endpoints (`/v1/messages`)

#### Stage 6: Frontend UI
- `/demo` page with SMS submission form and score visualization
- Explanation display (rule reasons + Claude explanation text)
- `/history` page for message list
- `/messages/[id]` detail page
- Next.js server proxy route to FastAPI

#### Stage 7: Testing & Polish
- Unit tests for rule engine and ML pipeline
- Integration tests for full API flow
- UI testing and responsive design
- Performance optimization and error handling

### MVP hardening (architecture review follow-ups)
Tracked in `issues.md` Group 10 (#61–#69): ADRs for the combiner, Phase 3 failure handling and skip gate; positive-evidence rules; prompt-injection hardening; Phase 3 degraded mode with a "skipped" state; a rule-floor combiner with verdict bands; a rule-only Phase 3 skip gate; a persistent dedup cache; per-IP rate limiting; and the optional `sender` decision. These belong before the public demo.

### Post-MVP — Jev classification and triage
Tracked in `issues.md` Group 9 (#55–#60): a swappable Jev client, a go/no-go spike on the Canadian held-out set, pre-labeling for annotation, Phase 0 category/brand/tone classification, Phase 2 comparison, and a Phase 3 triage gate with a "Phase 3 skipped" state.

### v2 — RAG Pipeline + Self-improving Loop
RAG closes the gap between Phase 3's structured prompt context and Claude's general training knowledge. By injecting confirmed scam examples from our own corpus into the Phase 3 prompt, Claude reasons against patterns we curate and verify — not patterns from its training data. This anchors scoring and explanations to real-world scam behavior we control.

- `pgvector` embeddings store for confirmed scam corpus
- RAG retrieval at Phase 3: embed incoming SMS → retrieve top-K similar known scams → inject into Claude prompt as domain context
- **Self-training loop (v2, post-MVP)**: user-submitted messages scoring `ai_score > 0.85` are queued for admin review; approved entries retrain Phase 2 and grow the RAG store. Uses `ai_score` as pseudo-label (not `final_score`) to avoid circular signal corruption — the ML score must not influence the label it is later trained on.
- **Confidence-gated auto-approval (v3)**: entries scoring `ai_score > 0.97` bypass the moderation queue and are auto-approved — false positive rate is negligible at this threshold. All auto-approved entries are logged for audit.
- Community reporting flow: user submits new scam reports → moderation pipeline → approved entries added to RAG store + training corpus
- Evaluation dashboard (precision/recall, confusion matrix)
- Probability calibration once sufficient labeled data accumulates

### v3 — Admin & Operations
- Admin UI for seed data management (replaces JSON config files with Supabase tables)
- Model/version management + reindex workflows
- Score distribution monitoring (drift detection)
- Tactic classifier for richer explanation labels (urgency/threat/authority/reward)
