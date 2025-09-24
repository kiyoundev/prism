# Prism Coding Standards

## 1. Core Principles
- Use **TypeScript** across front-end and back-end for shared types and safer modifications.
- Favor **UntitledUI** primitives and project-defined components before authoring custom markup.
- Keep logic isolated: presentational components stay pure, business rules live in services/repositories.
- Make all asynchronous operations resilient with explicit error handling and logs.
- Treat accessibility and performance requirements as part of definition of done.

## 2. File & Naming Conventions
- Components: `PascalCase` (e.g., `RiskScoreCard.tsx`).
- Hooks: `useCamelCase` (e.g., `useAnalyzeSubmission.ts`).
- Zustand stores: `something.store.ts` exposing `useSomethingStore` hook.
- API routes: `app/api/<resource>/route.ts` with HTTP method handlers.
- Tests colocated with code as `*.test.ts(x)`; Storybook stories in `*.stories.tsx`.
- Shared types under `packages/shared` with suffix `*.types.ts`.

## 3. UI Implementation Rules
- Import Tailwind tokens via UntitledUI theme; do not hard-code color hex values.
- Honor responsiveness breakpoints from `docs/front-end-spec.md §8` via Tailwind utilities or helpers.
- Provide semantic HTML, labels, and `aria-*` attributes; include focus management for dynamic views.
- Use `next/dynamic` for optional heavy panels (e.g., knowledge tips) and suspense fallbacks.
- Surface errors with human-friendly copy and optional retry actions.

## 4. Data & Services
- Use fetch wrappers/services under `apps/web/lib/services/` to call APIs; never call `fetch` directly inside components.
- Repositories transform raw persistence results into typed domain models before returning to services.
- All services should accept explicit parameter objects rather than positional arguments.
- Log key events (analysis request, rule hits, AI failures) with structured metadata.

## 5. Testing Expectations
- Component logic: unit test with React Testing Library; simulate keyboard navigation for accessibility coverage.
- Service/repository logic: Jest unit tests verifying rule combinations, error cases, and Supabase adapters.
- E2E flows: Playwright specs covering submission, reporting wizard, and moderation happy paths.
- Add Storybook stories for each UI component variant referenced in the UX specification.

## 6. Documentation & Reviews
- Update `docs/architecture.md` or ADRs when introducing new integrations or data flows.
- Note open TODOs or assumptions in code with `// TODO(prism-xyz)` and track in backlog.
- Ensure pull requests link to relevant user story and include test evidence.
