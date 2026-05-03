# Prism Technology Stack

## Frontend (Vercel)
| Concern | Technology |
|---|---|
| Framework | Next.js 15 (App Router) |
| Language | TypeScript 5 |
| Styling | TailwindCSS |
| Components | shadcn/ui (Radix UI primitives — WCAG AA accessible) |
| Icons | Lucide React |
| State | React `useState` only — no client-side store needed |
| Testing | Jest + React Testing Library |

## Backend (Railway)
| Concern | Technology |
|---|---|
| Framework | FastAPI |
| Language | Python 3.12 |
| Server | Uvicorn |
| Validation | Pydantic v2 |
| ORM | SQLAlchemy 2 |
| Migrations | Alembic |
| DB driver | psycopg2-binary |

## ML / NLP
| Concern | Technology |
|---|---|
| Tokenization / lemmatization | NLTK |
| Classifier | Naive Bayes (baseline) → Logistic Regression |
| Feature weighting | TF-IDF (`scikit-learn TfidfVectorizer`) |
| Feature extraction | scikit-learn |
| Fuzzy matching | rapidfuzz (edit-distance for near-miss brand/keyword detection) |
| Sentiment | NLTK SentimentIntensityAnalyzer |
| URL parsing | tldextract |
| Unicode normalization | unicodedata + unidecode |
| Embeddings (v2) | sentence-transformers |

## AI
| Concern | Technology |
|---|---|
| Phase 3 scoring + explanation | Claude API (Anthropic) — pending final confirmation |
| SDK | anthropic Python SDK |

## Database (Supabase)
| Concern | Technology |
|---|---|
| Engine | PostgreSQL |
| Hosting | Supabase (managed) |
| Vector search | pgvector extension (enabled from start, active in v2) |

## Infrastructure
| Concern | Technology |
|---|---|
| Frontend deploy | Vercel |
| Backend deploy | Railway |
| DB hosting | Supabase |
| CI/CD | GitHub Actions |
| Secrets | Vercel env vars (frontend), Railway env vars (backend) |

## Developer Tooling
| Concern | Technology |
|---|---|
| Python formatting | black + ruff |
| Python testing | pytest |
| Pre-commit hooks | pre-commit |
| JS/TS linting | ESLint + eslint-config-next |
