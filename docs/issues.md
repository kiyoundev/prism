# Prism — Issue Backlog

53 atomic issues sliced for solo part-time development.
Estimated total: ~78 hours → **MVP target: end of August 2026**.

All issues are AFK (no human decision gate required).

---

## Timeline

**Assumptions**: ~6 focused hours/week on Prism (working across 3–4 projects simultaneously). Weeks are calendar weeks — slow weeks and context-switching are built in.

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

> If velocity drops to ~4 hrs/week (heavier periods on other projects), push each milestone ~1–2 weeks. If a week is fully productive, pull milestones forward accordingly.

---

## Group 0 — Hotfixes

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 1 | Fix requirements.txt: uncomment unidecode (crash fix) | 30m | — |
| 2 | requirements.txt: add alembic, rapidfuzz, scikit-learn, anthropic, numpy with stage comments | 30m | #1 |
| 3 | `pyproject.toml`: configure black + ruff | 30m | — |
| 4 | pre-commit hooks: wire black + ruff | 30m | #3 |

---

## Group 1 — Infrastructure Setup

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 5 | Supabase: create project, grab `DATABASE_URL` | 30m | — |
| 6 | Railway: create project, set `DATABASE_URL`, `ANTHROPIC_API_KEY`, `INTERNAL_API_KEY` | 30m | #5 |
| 7 | Vercel: link frontend project, set `FASTAPI_URL` env var | 30m | — |
| 8 | `.env.example` files for `backend/` and `frontend/` | 30m | #5, #6, #7 |
| 9 | `docker-compose.yml` for local dev (FastAPI + Postgres) | 1h | #5 |
| 10 | Alembic init + `messages` table migration | 2h | #5 |
| 11 | `message_analysis` table migration | 1h | #10 |
| 12 | GitHub Actions CI: lint + test on PR | 1h | #3, #4 |
| 13 | Frontend: install shadcn/ui + Lucide React, base layout | 1h | — |

---

## Group 2 — Stage 2: Phase 0 Preprocessing

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 14 | `normalizer.py`: lowercase, punctuation, unicode NFKD, homoglyph flatten | 2h | — |
| 15 | `url_extractor.py`: extract URLs before normalization | 1h | — |
| 16 | `tokenizer.py`: word tokens + bi/tri-grams | 2h | — |
| 17 | `tokenizer.py`: rapidfuzz fuzzy matching for near-miss brands/keywords | 2h | #16 |
| 18 | `extractor.py`: wire Phase 0 into `artifacts{}` bundle | 1h | #14, #15, #16, #17 |

---

## Group 3 — Stage 2: Phase 1 Rule Engine

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 19 | `category_extractor.py`: complete brand detection (longest-match, multi-word) | 2h | #18 |
| 20 | `category_extractor.py`: keyword scoring + resolution logic | 2h | #19 |
| 21 | `url_checker.py`: allowlist/denylist + suspicious TLD detection | 2h | #18 |
| 22 | `url_checker.py`: brand-domain mismatch detection | 2h | #21 |
| 23 | `unicode_detector.py`: homoglyph + zero-width character detection | 2h | — |
| 24 | `pattern_matcher.py`: urgency + authority social engineering patterns | 2h | — |
| 25 | `pattern_matcher.py`: financial structuring + channel-shifting rules | 1h | #24 |
| 26 | `rule_score` aggregator + `rule_reasons[]` output | 2h | #20, #22, #23, #25 |
| 27 | FastAPI: `POST /v1/score` Phase 1-only stub | 2h | #26 |
| 28 | FastAPI: X-API-Key middleware on `/v1/*` routes | 1h | — |

---

## Group 4 — Stage 3: Phase 2 ML Classifier

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 29 | Download + preprocess UCI SMS Spam Collection into seed corpus | 2h | — |
| 30 | `features.py`: TF-IDF pipeline on Phase 0 tokens | 2h | #18, #29 |
| 31 | `sentiment.py`: NLTK SentimentIntensityAnalyzer signal | 1h | — |
| 32 | `classifier.py`: train + serialize Naive Bayes model | 2h | #30, #31 |
| 33 | Integrate Phase 2 into FastAPI pipeline (receives Phase 1 context) | 2h | #27, #32 |

---

## Group 5 — Stage 4: Phase 3 Claude AI

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 34 | `client.py` + `prompts.py`: Anthropic SDK setup + structured prompt template | 2h | — |
| 35 | Integrate Phase 3 into pipeline after Phase 2 | 2h | #33, #34 |
| 36 | SHA-256 dedup cache: skip Phase 3 for repeated messages | 1h | #35 |

---

## Group 6 — Stage 5: Combiner + Full API

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 37 | SQLAlchemy ORM models: `Message` + `Analysis` | 2h | #11 |
| 38 | Pydantic schemas: `MessageCreate`, `ScoringResult`, `AnalysisResult` | 1h | #37 |
| 39 | `combiner.py`: weighted `final_score` calculation | 1h | #26, #33, #35 |
| 40 | Complete `POST /v1/score`: full pipeline + persist message + analysis | 3h | #35, #37, #38, #39 |
| 41 | `GET /v1/messages` + `GET /v1/messages/{id}` endpoints | 2h | #40 |
| 42 | `GET /v1/messages/{id}/analysis/latest` endpoint | 1h | #41 |

---

## Group 7 — Stage 6: Frontend UI

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 43 | Next.js server-side proxy route → FastAPI `POST /v1/score` | 1h | #40 |
| 44 | `/demo` page: SMS form + loading state | 2h | #43 |
| 45 | `/demo` page: `ScoreCard` + rule reasons display | 2h | #44 |
| 46 | `/demo` page: Claude explanation panel | 1h | #45 |
| 47 | `/history` page: submission list with `final_score` | 2h | #41, #43 |
| 48 | `/messages/[id]`: full analysis detail view | 2h | #42, #43 |

---

## Group 8 — Stage 7: Testing + Polish

| # | Title | Est. | Blocked by |
|---|---|---|---|
| 49 | pytest: Phase 0 normalizer + tokenizer unit tests | 2h | #14–#17 |
| 50 | pytest: Phase 1 rule engine unit tests | 2h | #19–#26 |
| 51 | pytest: Phase 2 ML classifier unit tests | 1h | #30–#32 |
| 52 | pytest: `POST /v1/score` integration test | 2h | #40 |
| 53 | Playwright E2E: `/demo` submission flow | 2h | #44, #52 |