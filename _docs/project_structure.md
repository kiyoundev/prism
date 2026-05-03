# Prism Project Structure (Monorepo)

```
prism/
├── README.md
├── package.json                 # Root scripts and dev dependencies
├── .gitignore
├── .env.example
├── docker-compose.yml           # Local development setup
├── 
├── frontend/                    # Next.js application
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   ├── .env.local
│   ├── 
│   ├── src/
│   │   ├── app/                 # App Router (Next.js 13+)
│   │   │   ├── demo/
│   │   │   │   └── page.tsx
│   │   │   ├── history/
│   │   │   │   └── page.tsx
│   │   │   ├── messages/
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx
│   │   │   ├── admin/
│   │   │   │   ├── datasets/
│   │   │   │   │   └── page.tsx
│   │   │   │   └── eval/
│   │   │   │       └── page.tsx
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/             # Reusable UI components
│   │   │   ├── forms/
│   │   │   └── visualizations/
│   │   ├── lib/
│   │   │   ├── api.ts          # API client functions
│   │   │   └── utils.ts        # runtime helpers
│   │   └── types/
│   │       └── api.ts          # TypeScript types for API
│   ├── public/
│   └── .next/
│
├── backend/                     # FastAPI application
│   ├── requirements.txt
│   ├── pyproject.toml           # Python project config
│   ├── .env
│   ├── alembic.ini
│   ├── 
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── config.py            # Database and app settings
│   │   ├── database.py          # Database connection
│   │   ├── 
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── message.py
│   │   │   └── analysis.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── message.py
│   │   │   └── analysis.py
│   │   ├── 
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── scoring.py
│   │   │   │   │   ├── messages.py
│   │   │   │   │   └── dataset.py
│   │   │   │   └── api.py
│   │   │   └── deps.py         # Dependencies
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── rules/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── url_checker.py
│   │   │   │   ├── pattern_matcher.py
│   │   │   │   ├── keyword_detector.py
│   │   │   │   ├── unicode_detector.py
│   │   │   │   └── config/            # JSON/YAML assets (brand variants, category keywords, risk lists)
│   │   │   ├── ml/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── embeddings.py
│   │   │   │   ├── similarity.py
│   │   │   │   └── classifier.py
│   │   │   └── scoring/
│   │   │       ├── __init__.py
│   │   │       ├── pipeline.py
│   │   │       └── combiner.py
│   │   ├── 
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── text_processing.py
│   ├── 
│   ├── alembic/                 # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_rules.py
│   │   ├── test_ml.py
│   │   └── test_api.py
│   └── data/                    # Seed data and models
│       ├── seed_scams.json
│       ├── seed_legit.json
│       └── models/
│
├── docs/                        # Documentation
│   ├── overview_v1.md
│   ├── api.md
│   └── deployment.md
│
└── scripts/                     # Utility scripts
    ├── setup.sh
    ├── seed_data.py
    └── deploy.sh
```

## Key Points:
- **Monorepo**: Single repository with clear frontend/backend separation
- **Root package.json**: Contains scripts to run both services (`npm run dev:frontend`, `npm run dev:backend`)
- **Shared types**: TypeScript types in `frontend/src/types/` match Pydantic schemas in `backend/schemas/`
- **Environment files**: Separate `.env` files for each service
- **Database migrations**: Alembic manages Postgres schema changes
- **Testing**: Separate test suites for each component
- **Data storage**: Seed data and ML models in `backend/data/`



- models/: SQLAlchemy ORM classes mapping directly to tables (message.py, analysis.py).
- schemas/: Pydantic models that describe payloads (e.g., MessageCreate, MessageRead, AnalysisResult)Routers depend on schemas; repositories/services depend on models.


- v1/api.py creates an APIRouter and includes endpoint routers (scoring.py, messages.py, dataset.py).
endpoints/*.py files define actual routes (e.g., router.post("/score")).
- deps.py holds reusable dependencies (auth, DB session injector) that endpoint modules import.
- main.py pulls in from app.api.v1.api import api_router and calls app.include_router(api_router, prefix="/api/v1"), so each endpoint file contributes to the final HTTP surface without cluttering main.py.