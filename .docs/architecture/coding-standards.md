# Prism Coding Standards

## 1. Core Principles
- Frontend is TypeScript (Next.js). Backend is Python (FastAPI). Keep concerns strictly separated — no business logic in the frontend.
- Use shadcn/ui primitives and project-defined components before authoring custom markup.
- Keep logic isolated: presentational components stay pure, pipeline logic lives in FastAPI services.
- Make all asynchronous operations resilient with explicit error handling and structured logs.
- Treat accessibility and performance requirements as part of definition of done.

## 2. Frontend File & Naming Conventions
- Components: `PascalCase` (e.g., `ScoreCard.tsx`)
- Hooks: `useCamelCase` (e.g., `useScoreSubmission.ts`)
- API routes (proxy): `src/app/api/<resource>/route.ts`
- Tests colocated with code as `*.test.ts(x)`
- TypeScript types under `src/types/` with suffix `*.ts`
- Never call `fetch` directly inside components — use typed wrappers in `src/lib/api.ts`

## 3. Backend File & Naming Conventions
- Endpoint files: `backend/app/api/v1/endpoints/<resource>.py`
- Pydantic schemas: `backend/app/schemas/<resource>.py` — one file per domain object
- SQLAlchemy models: `backend/app/models/<resource>.py`
- Pipeline logic: `backend/app/core/scoring/pipeline.py` orchestrates Phase 1 → 2 → 3
- Config files (brand_variants, category_keywords, allowed_domains): `backend/app/core/rules/config/` — loaded at startup, never written at runtime
- Python style: black formatting, ruff linting, type hints on all function signatures

## 4. UI Implementation Rules
- Use shadcn/ui components; extend with Tailwind utilities — do not hard-code color hex values
- Provide semantic HTML, labels, and `aria-*` attributes; include focus management for dynamic views
- Use `next/dynamic` for optional heavy panels and suspense fallbacks
- Surface errors with human-friendly copy and optional retry actions

## 5. Pipeline Rules (Backend)
- Phases run sequentially: Phase 0 → Phase 1 → Phase 2 → Phase 3. Never invoke them in parallel.
- Each phase receives all artifacts from upstream phases as input.
- Phase 3 (Claude) must never be called with raw SMS text alone — always pass Phase 0–2 artifacts.
- Rule config (brand_variants.json, etc.) is the source of truth for MVP. Do not create Supabase tables for rule definitions until an admin UI exists.

## 6. Data & Services
- Frontend calls FastAPI exclusively through the server-side proxy route (`src/app/api/score/route.ts`). The FastAPI URL is never exposed to the browser.
- FastAPI is the only service with Supabase credentials. Frontend never touches the DB.
- All services accept explicit parameter objects rather than positional arguments.
- Log key pipeline events (rule hits, ML score, Claude response latency) with structured metadata.

## 7. Testing Expectations
- Python: pytest for unit and integration tests. Test each pipeline phase independently with fixture inputs.
- Frontend: Jest + React Testing Library for component logic; keyboard navigation for accessibility coverage.
- E2E: Playwright covering the `/demo` submission flow end-to-end.

## 8. Documentation & Reviews
- Update `docs/architecture.md` or `docs/overview.md` when introducing new integrations or data flows.
- Note open TODOs in code with `# TODO(prism-xyz):` (Python) or `// TODO(prism-xyz):` (TS) and track in backlog.
- Pull requests link to the relevant implementation stage from `docs/overview.md` roadmap.
