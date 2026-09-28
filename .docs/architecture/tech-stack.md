# Prism Technology Stack

## Frontend (Vercel)
| Concern | Technology | Version |
|---|---|---|
| Framework | Next.js (App Router) | 16.1.1 |
| Language | TypeScript | 5.6.2 |
| Runtime | React | 19.2.3 |
| Styling | TailwindCSS | 3.4.14 |
| Components | shadcn/ui (Radix UI primitives — WCAG AA accessible) | installed via CLI |
| Icons | Lucide React | installed via CLI |
| State | React `useState` only — no client-side store needed | — |
| Testing | Jest | 29.7.0 |

## Backend (Railway)
| Concern | Technology | Version |
|---|---|---|
| Language | Python | 3.12.8 (`backend/runtime.txt`) |
| Framework | FastAPI | 0.115.4 |
| Server | Uvicorn | 0.32.0 |
| Validation | Pydantic | 2.7.4 |
| ORM | SQLAlchemy | 2.0.24 |
| Migrations | Alembic | 1.13.3 |
| DB driver | psycopg2-binary | 2.9.9 |
| Env vars | python-dotenv | 1.0.1 |

## ML / NLP
| Concern | Technology | Version |
|---|---|---|
| Tokenization / sentiment | NLTK | 3.9.1 |
| Classifier | Naive Bayes (`scikit-learn`) | 1.5.2 |
| Feature weighting | TF-IDF (`scikit-learn TfidfVectorizer`) | 1.5.2 |
| Fuzzy matching | rapidfuzz | 3.9.7 |
| URL parsing | tldextract | 5.1.2 |
| Unicode / homoglyph flattening | unidecode | 1.3.8 |
| Numerics | numpy | 1.26.4 |
| Embeddings (v2) | sentence-transformers | TBD |

## AI
| Concern | Technology | Version |
|---|---|---|
| Phase 3 scoring + explanation | Claude API (Anthropic) | — |
| SDK | anthropic Python SDK | 0.34.2 |

## Database (Supabase)
| Concern | Technology | Version |
|---|---|---|
| Engine | PostgreSQL | managed by Supabase |
| Vector search | pgvector | enabled from start, active in v2 |

## Infrastructure
| Concern | Technology |
|---|---|
| Frontend deploy | Vercel |
| Backend deploy | Railway |
| DB hosting | Supabase |
| CI/CD | GitHub Actions |
| Secrets | Vercel env vars (frontend), Railway env vars (backend) |

## Developer Tooling
| Concern | Technology | Version |
|---|---|---|
| Python linting + formatting | Ruff | latest (global install) |
| Python testing | pytest | latest |
| JS/TS linting + formatting | ESLint + Prettier | 8.57.1 |
| Run both services locally | concurrently (root `package.json`) | 9.2.1 |

## Local Dev Notes
- **Python**: must use 3.12 locally to match Railway (`runtime.txt`). Create a venv: `python3.12 -m venv backend/venv`
- **Node**: Next.js 16 requires Node 18.18+. Run `node --version` to verify.
- **Both services**: `npm run dev` from repo root starts frontend + backend via `concurrently`
