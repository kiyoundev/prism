# Prism Repository Source Tree

```
prism/
├── README.md
├── package.json                    # Root scripts (dev:frontend, dev:backend, test)
├── pytest.ini                      # Python test config
├── .gitignore
│
├── frontend/                       # Next.js application (Vercel)
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local
│   └── src/
│       ├── app/                    # App Router routes
│       │   ├── demo/page.tsx       # SMS submission + score display
│       │   ├── history/page.tsx    # Submission history list
│       │   ├── messages/[id]/page.tsx  # Full analysis detail
│       │   ├── admin/
│       │   │   ├── datasets/page.tsx   # Seed data management (optional)
│       │   │   └── eval/page.tsx       # Metrics dashboard (optional)
│       │   ├── api/score/route.ts  # Server-side proxy → FastAPI
│       │   ├── layout.tsx
│       │   └── page.tsx            # Landing / redirect to /demo
│       ├── components/
│       │   ├── ui/                 # shadcn/ui generated components
│       │   ├── ScoreCard.tsx       # Risk score visualization
│       │   ├── ExplanationPanel.tsx
│       │   └── MessageForm.tsx
│       ├── lib/
│       │   ├── api.ts              # Typed fetch wrappers for FastAPI
│       │   └── utils.ts
│       └── types/
│           └── api.ts              # TypeScript interfaces matching Pydantic schemas
│
├── backend/                        # FastAPI application (Railway)
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── .env
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point, CORS, router mount
│   │   ├── config.py               # Settings (DB URL, API keys)
│   │   ├── database.py             # SQLAlchemy engine + session
│   │   ├── core/
│   │   │   ├── preprocessing/      # Phase 0: shared extraction layer
│   │   │   │   ├── normalizer.py   # Lowercase, punctuation, unicode/homoglyph flattening
│   │   │   │   ├── url_extractor.py
│   │   │   │   ├── tokenizer.py    # Tokenization, n-grams, fuzzy matching (rapidfuzz)
│   │   │   │   └── extractor.py    # Brand/category detection entry point
│   │   │   ├── rules/              # Phase 1: deterministic rule engine
│   │   │   │   ├── category_extractor.py
│   │   │   │   ├── url_checker.py
│   │   │   │   ├── pattern_matcher.py
│   │   │   │   ├── unicode_detector.py
│   │   │   │   └── config/         # JSON config (loaded at startup, no DB needed)
│   │   │   │       ├── brand_variants.json
│   │   │   │       ├── category_keywords.json
│   │   │   │       └── allowed_domains.json
│   │   │   ├── ml/                 # Phase 2: NLTK classifier + TF-IDF
│   │   │   │   ├── classifier.py   # Train + inference
│   │   │   │   ├── features.py     # TF-IDF vectorization + NLTK feature extraction
│   │   │   │   └── sentiment.py    # Urgency/negativity signal
│   │   │   ├── ai/                 # Phase 3: Claude API
│   │   │   │   ├── client.py       # Anthropic SDK wrapper
│   │   │   │   └── prompts.py      # Structured prompt templates
│   │   │   └── scoring/            # Pipeline orchestration
│   │   │       ├── pipeline.py     # Runs Phase 0 → 1 → 2 → 3 sequentially
│   │   │       └── combiner.py     # Weighted final_score calculation
│   │   ├── api/v1/
│   │   │   ├── api.py              # APIRouter aggregator
│   │   │   ├── deps.py             # DB session injector, auth deps
│   │   │   └── endpoints/
│   │   │       ├── scoring.py      # POST /v1/score
│   │   │       ├── messages.py     # GET /v1/messages, /v1/messages/{id}
│   │   │       └── dataset.py      # Admin seed data endpoints
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── message.py
│   │   │   └── analysis.py
│   │   └── schemas/                # Pydantic request/response schemas
│   │       ├── message.py
│   │       └── analysis.py
│   ├── alembic/                    # DB migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   │   ├── test_rules.py
│   │   ├── test_ml.py
│   │   └── test_api.py
│   └── data/
│       ├── seed_scams.json         # 100% confirmed scam examples
│       ├── seed_legit.json         # Known legitimate messages
│       ├── nltk_data/              # Auto-downloaded NLTK corpora (gitignored; fetched on first startup)
│       └── models/                 # Trained classifier artifacts (v2+)
│
├── data/
│   └── known-scams/                # Curated scam reference data
│
├── docs/                           # Documentation
│   ├── overview.md                 # Master: goals, pipeline, roadmap
│   ├── architecture.md             # System architecture + component diagram
│   ├── database.md                 # Postgres schema reference
│   ├── rule_engine.md              # Phase 1 rule engine details
│   ├── project_structure.md        # This source tree
│   ├── architecture/
│   │   ├── tech-stack.md           # Full tech stack table
│   │   ├── source-tree.md          # (this file)
│   │   ├── rule-engine.md          # Rule engine architecture
│   │   └── coding-standards.md     # Code style and conventions
│   └── archive/                    # Superseded planning docs (Sep–Dec 2025)
│
└── scripts/
    ├── json_loader.py
    ├── msg_escaper.py
    └── scams.txt
```

## Notes
- `frontend/src/app/api/score/route.ts` is a Next.js server-side proxy — the FastAPI backend URL is never sent to the browser.
- `backend/app/core/rules/config/` JSON files load at FastAPI startup. No database tables are needed for rule config until an admin UI is built.
- `backend/data/models/` stores trained Phase 2 classifier artifacts. In v2 this grows to include embedding models.
- Alembic in `backend/alembic/` manages all Supabase schema migrations — never apply DDL manually.
