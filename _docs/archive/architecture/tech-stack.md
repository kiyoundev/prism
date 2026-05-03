# Prism Technology Stack Overview

## 1. Frontend
- **Framework:** Next.js 15 (App Router, Server Components where appropriate)
- **Language:** TypeScript 5 for shared types across UI and API routes
- **UI Library:** UntitledUI with Tailwind CSS 4 token integration
- **State Management:** Zustand 5 with slice-based stores at `apps/web/store/`
- **Data Fetching:** Next.js `fetch`, SWR/React Query helpers via services layer
- **Testing:** Jest 30 + React Testing Library, Storybook 9 for visual verification

## 2. Backend (Serverless API)
- **Runtime:** Next.js API Routes deployed as Netlify Functions
- **Language:** TypeScript (shared models from `packages/shared/types`)
- **Rule Engine:** Custom keyword/number matcher backed by JSON store, migrating to Supabase tables
- **AI Integration:** External AI provider adapter with prompt versioning and latency logging
- **Validation:** Zod schemas for request/response payloads

## 3. Persistence & Data
- **MVP Storage:** JSON files under `data/` for submissions, reports, knowledge content
- **Planned Migration:** Supabase Postgres (tables for submissions, reports, moderation, knowledge)
- **Object Storage:** Netlify assets initially → Supabase Storage for evidence/uploads later
- **Caching:** Netlify Edge caching for static/knowledge pages; in-memory memoization for rule lists

## 4. Infrastructure & DevOps
- **Hosting:** Netlify (CDN/Edge, serverless functions, environment management)
- **CI/CD:** Netlify deploy previews + GitHub Actions for tests/lint/storybook
- **IaC:** `netlify.toml`, Supabase CLI migrations, future Terraform optional
- **Monitoring:** Netlify Analytics for MVP → Supabase Observability and custom dashboards
- **Logging:** Netlify function logs, structured JSON log helpers, Supabase log drains post-migration

## 5. Tooling & Developer Experience
- **Build Tool/Bundler:** Turbopack (Next.js default)
- **Linting & Formatting:** ESLint 9, Prettier 3, eslint-config-next + a11y rules
- **Storybook:** v9 integration for component documentation and a11y checks
- **Playwright:** 1.48 E2E flows covering analysis, reporting, moderation
- **AI Workflows:** BMAD agent system (`.bmad-core/`) to orchestrate PM, UX, Architect, Dev roles

## 6. Security & Compliance Baseline
- **Auth (MVP):** Environment-token protected moderator routes; eventual Supabase Auth/RLS
- **Secrets:** Netlify environment variables, Supabase secret manager after migration
- **Policies:** CSP headers, rate limiting, input sanitization, audit logging

## 7. Accessibility & Performance Targets
- **Accessibility:** WCAG 2.1 AA requirements embedded in component standards
- **Performance:** <3s analysis response end-to-end, <2.5s FCP on 3G, dynamic imports for heavy panels
- **Monitoring:** Web Vitals reporting via `reportWebVitals`, Netlify analytics dashboards
