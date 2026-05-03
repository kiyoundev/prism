
# Prism — Project Overview (v1)

## Goal
Prism detects scam SMS messages and returns a **scam likelihood (%)** with explainable reasons.

Core design: a **two-stage intelligence pipeline**:
- **Phase 1**: deterministic rule engine (static pattern matching)
- **Phase 2**: context/semantic scoring (ML)

The system stores:
- seed **100% scam** messages
- seed **legit (ham)** messages
- **user-submitted** messages
- per-run **analysis outputs** (scores + explanations)

## System-level MVC (recommended mental model)
Treat the whole system as one MVC in a monorepo structure:
- **Model**: Postgres data + ML artifacts (embeddings/model versions)
- **Controller**: FastAPI in `/backend` (authoritative scoring + persistence)
- **View**: Next.js in `/frontend` (submission, history, details, dashboards)

### How responsibilities map today
- **View (Next.js)**: Presents `/demo`, `/history`, `/messages/[id]`, and admin surfaces. It never talks to Postgres directly; instead it calls FastAPI endpoints for scoring runs and history.
- **Controller (FastAPI)**: Runs Phase 1 rules + Phase 2 ML, combines scores, persists `messages` and `message_analysis`, and exposes REST APIs (`/v1/score`, `/v1/messages`, admin routes). SQLAlchemy/psycopg connect FastAPI to Postgres.
- **Model (Supabase Postgres + artifacts)**: Stores all SMS (`messages`) and scoring history (`message_analysis`) and eventually embeddings/models. Supabase still hosts the managed Postgres instance; FastAPI is the only service with DB credentials.

## Architecture
### Components
- **Next.js in `/frontend` (View/UI)**
  - pages/routes
  - form UX and visualization
  - optional server-side proxy to FastAPI (to avoid CORS and hide backend URL)
- **FastAPI in `/backend` (Controller/Scoring API)**
  - rules + ML scoring pipelinej
  - score combination into a single probability-like output
  - database reads/**writes**
  - dataset management endpoints (seed data)
  - optional evaluation endpoints
- **Postgres (Model)**
  - messages + analyses as durable source of truth
  - optional `pgvector` for embedding similarity search

### Why this split in a monorepo
- Next.js excels at building and presenting the product.
- Python (FastAPI) is better for ML workflows and maintaining modern NLP tooling.
- FastAPI being the authority keeps scoring logic consistent and reproducible.
- Monorepo structure simplifies development while maintaining clear separation of concerns.

## Scoring Pipeline
### Inputs
- SMS `text` (primary)
- optional metadata (future): locale, timestamp, user id

### Phase 1 — Deterministic Rule Engine (FastAPI)
Purpose: high-precision detection and explainability.

#### Rule signals:
1. **URL Analysis**
   - **Typosquatting & Lookalikes:** `netflix.com` vs `netflix.com` (Cyrillic), or `purolator-delivery.com` (hyphenated lookalikes).
   - **Suspicious TLDs:** `.xyz`, `.top`, `.vip`, `.info` are rarely used by legitimate brands.
   - **Subdomain Abuse:** `cra-refund.gc.ca.hosting.com` (looks legit on left, hosted on right).
   - **URL Shorteners:** `bit.ly`, `tinyurl` used in "official" banking/gov alerts.
   - **IP Address Links:** `http://142.x.x.x` links are almost always malicious.

2. **Text Obfuscation** (Evasion)
   - **Homoglyphs:** Using Cyrillic `а` instead of Latin `a`.
   - **Inserted Noise:** `V.E.R.I.F.Y` or `A c t i o n R e q u i r e d`.
   - **Mathematical Alphanumerics:** 𝐔𝐫𝐠𝐞𝐧𝐭 instead of Urgent.

3. **Social Engineering Patterns**
   - **Urgency:** "Immediate action required", "Account suspended", "Will be deleted".
   - **Authority:** Impersonating Police, CRA, Border Services.
   - **Scarcity/Reward:** "You have a refund pending", "Claim your prize".

4. **Sender Metadata**
   - **Email-to-SMS:** "Official" alerts coming from `@gmail.com` or `@hotmail.com` addresses.
   - **Country Code Mismatch:** "CRA" alert coming from +44 (UK) or +1 (US) numbers.

5. **Formatting & Style**
   - **Emoji Usage:** "Official" alerts rarely use emojis (🚨, 💰, 🔥).
   - **Excessive Punctuation:** `Immediately!!!!` or `$$$` or `???`.
   - **All-Caps Abuse:** "YOUR ACCOUNT HAS BEEN SUSPENDED" (legit uses sentence case).
   - **Visual Spacing:** Multiple newlines to push the malicious link "below the fold".

6. **Channel Shifting**
   - **Platform references:** "Contact us on WhatsApp", "Telegram", or "Signal".
   - **Personal numbers:** "Text me back at [personal cell number]" for corporate contexts.

7. **Financial Structuring**
   - **Payment Methods:** "Gift Card", "Bitcoin", "Crypto", "Steam Card".
   - **Specific Amounts:** weirdly specific numbers like "$452.91" to feign accuracy.

8. **Phone Number Extraction**
   - **Mismatched Contacts:** Message from shortcode (legit) but asks to "Call this 1-800 number" (scam call center).



Outputs:
- `rule_score` in `[0, 1]`
- `rule_reasons[]` (machine-readable codes + display strings)
- extracted artifacts (urls/domains/flags) for UI and storage
- Brand/category cues live in backend config files (e.g., `brand_seeds`, `category_keywords`, link risk lists). Stage 1 loads these at FastAPI startup, uses them to derive the category + evidence, and only persists the results (`messages.category`, `message_analysis.rule_reasons`). No DB tables are required for the rule definitions until an admin UI is needed.

### Phase 2 — Context/ML Scoring (FastAPI)
Primary approach (fits small datasets): **embedding similarity**.

Behavior:
- embed incoming SMS
- retrieve nearest neighbors among seed scams and seed legits
- compute an `ml_score` from similarity (and optionally contrast vs legit neighbors)

Optional extension: **tactic classifier** (urgency/threat/authority/reward/etc.) to produce richer explanations.

Outputs:
- `ml_score` in `[0, 1]`
- `neighbors[]` (top matches with similarity)
- optional `tactics[]` (label + confidence)

### Combining into a single %
Recommended baseline combiner (soft-OR):
- `final_score = 1 - (1 - rule_score) * (1 - ml_score)`

Optional overrides (future):
- clamp `final_score` upward for extremely high-confidence rule hits
- probability calibration (once enough scam + legit labels exist)

## Data Model (Postgres)
### Core tables (conceptual)
- `messages`
  - stores raw text
  - `source`: seed_scam | seed_legit | user_submitted
  - `label`: scam | legit | unknown
  - timestamps

- `message_analysis`
  - one row per scoring run
  - `rule_score`, `rule_reasons` (json)
  - `ml_score`, `ml_details` (json: neighbors/tactics)
  - `final_score`
  - `model_version` / `pipeline_version`
  - timestamps

### Embeddings (optional)
- If using `pgvector`, store embeddings either:
  - on `messages` (simple), or
  - in `message_embeddings` (supports versioning/re-embedding)

## API Surface (FastAPI)
### Public scoring
- `POST /v1/score`
  - input: `{ text: string }`
  - action: score + persist message + persist analysis
  - output: `{ message_id, rule_score, rule_reasons, ml_score, ml_details, final_score, model_version }`

### Message browsing (for UI)
- `GET /v1/messages?source=&label=&limit=&cursor=`
- `GET /v1/messages/{id}`
- `GET /v1/messages/{id}/analysis/latest`

### Dataset management (admin)
- `POST /v1/dataset/messages` (add seed scam/legit)
- `PATCH /v1/dataset/messages/{id}` (update label/metadata)
- `POST /v1/dataset/reindex` (recompute embeddings)

### Evaluation (optional)
- `POST /v1/eval/run`
- `GET /v1/eval/latest`

## Next.js Pages (View)
- `/demo`: submit SMS and render score + explanations
- `/history`: list of user-submitted messages and their latest `final_score`
- `/messages/[id]`: message detail, full analysis payload
- `/admin/datasets` (optional): seed scam/legit management
- `/admin/eval` (optional): metrics dashboard

## Request Flow (typical)
1. User submits SMS in Next.js.
2. Next.js calls FastAPI `POST /v1/score` (direct with CORS, or via a Next proxy route).
3. FastAPI:
   - runs Phase 1 rules
   - runs Phase 2 context scoring
   - combines to `final_score`
   - writes `messages` + `message_analysis`
4. Next.js renders % + reasons + nearest-neighbor evidence.

## Libraries and Frameworks

### Frontend (Next.js)
- **Next.js** - React framework for the UI
- **React** - Core UI library
- **TypeScript** - Type safety (recommended)
- **TailwindCSS** - Styling framework
- **Lucide React** - Icons for UI components
- **Axios/Fetch** - API calls to FastAPI backend

### Backend (FastAPI)
- **FastAPI** - Python web framework for scoring API
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - ORM for Postgres
- **Alembic** - Database migrations
- **psycopg2-binary** - Postgres driver
- **pgvector** - Vector similarity search (optional)

### ML/NLP Libraries
- **sentence-transformers** - Text embeddings
- **scikit-learn** - ML utilities and similarity calculations
- **numpy/pandas** - Data manipulation
- **regex** - Pattern matching for rule engine
- **unicodedata** - Unicode normalization

### Database
- **PostgreSQL** - Primary data store
- **pgvector extension** - For embedding storage and similarity search

### Development Tools
- **pytest** - Testing framework
- **black/ruff** - Code formatting and linting
- **pre-commit** - Git hooks
- **Docker** - Containerization (optional for deployment)

## Seed & Reference Datasets

- **Canadian Anti-Fraud Centre (CAFC)** – monthly intelligence bulletins and the “Recent Scams” feed with confirmed SMS/phone exemplars. Requires analyst portal access for bulk exports.
- **FTC Consumer Sentinel Network** – “FTC Scam Alerts” plus Sentinel exports tagged as *Text Message Scam*, all reviewed by investigators.
- **UK NCSC 7726 Program** – curated smishing templates sourced from carrier-forwarded 7726 reports; representative samples published regularly.
- **Carrier spam honeypots (AT&T, T-Mobile, Vodafone, etc.)** – abuse/intelligence teams share confirmed smishing payloads via GSMA’s Fraud Intelligence Network and similar channels.
- **SMS Spam Collection (UCI/Kaggle)** – ~5.5k “ham”/“spam” messages with manual verification, suitable for baseline modeling.
- **NUS SMS Spam Corpus v0.1** – operator-verified complaints; each entry labeled after review.
- **Canadian Phishing Dataset (CIC-AND)** – includes SMS phishing samples extracted from real incidents with manual analysis.

## Roadmap
### v1 (MVP) - Implementation Stages

#### Stage 1: Core Infrastructure
- Set up monorepo structure with `/frontend` (Next.js) and `/backend` (FastAPI) folders [✅]
- Configure Next.js project with TypeScript and TailwindCSS in `/frontend` [✅]
- Set up FastAPI project with basic structure in `/backend` [✅]
  - Only essential dependencies installed outlined in `requirements.txt` [✅]
- Configure PostgreSQL database with core tables (`messages`, `message_analysis`)
- Implement basic API health check and CORS setup
- Set up unified package management (root `package.json` for scripts, separate `requirements.txt` for Python) [✅]

#### Stage 2: Rule Engine (Phase 1)
- Implement deterministic rule patterns:
  - Suspicious URL detection (shorteners, suspicious domains) 
  - Phone/email pattern matching
  - Unicode normalization and homoglyph detection
  - Keyword patterns for credential/OTP/social engineering
- Create rule scoring logic and reason **generation**
- Add rule engine endpoints to FastAPI

#### Stage 3: ML Similarity Scoring (Phase 2)
- Integrate sentence-transformers for text embeddings
- Implement embedding storage (pgvector or simple file-based)
- Create similarity search algorithm
- Add seed scam/legit dataset management endpoints
- Implement ML scoring pipeline

#### Stage 4: Score Combination & API
- Implement final score combination logic
- Create `/v1/score` endpoint with full **pipeline**
- Add message and analysis persistence
- Implement message browsing endpoints (`/v1/messages`)

#### Stage 5: Frontend UI
- Build `/demo` page with SMS submission form
- Create score visualization and explanation display
- Implement `/history` page for message list
- Build `/messages/[id]` detail page
- Add API integration between Next.js and FastAPI

#### Stage 6: Testing & Polish
- Add unit tests for rule engine and ML pipeline
- Integration testing for full API flow
- UI testing and responsive design fixes
- Performance optimization and error handling

### v2 (better probability + richer explanations)
- add legit dataset growth
- thresholds tuning + probability calibration
- tactic classifier
- evaluation dashboard (precision/recall, confusion matrix)

### v3 (polish)
- admin tools for labeling
- model/version management + reindex workflows
- monitoring score distribution (drift)

