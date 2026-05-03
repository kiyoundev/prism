# Prism Repository Source Tree

```
.
├── apps/
│   └── web/
│       ├── app/                 # Next.js App Router entrypoints and routes (UI + API)
│       ├── components/          # Shared UI components consumed by feature folders
│       ├── features/            # Feature modules (analysis, reporting, knowledge)
│       ├── lib/
│       │   ├── services/        # Client-side services for API interactions
│       │   ├── repositories/    # Data access abstractions (JSON ➜ Supabase)
│       │   └── utils/           # Cross-cutting helpers (formatters, logging)
│       ├── store/               # Zustand stores and selectors
│       └── styles/              # Tailwind and UntitledUI theme extensions
├── packages/
│   ├── shared/
│   │   ├── types/               # TypeScript interfaces shared across UI/API
│   │   └── utils/               # Reusable logic (parsers, formatters)
│   └── workflows/               # AI agent prompt helpers and workflow scripts
├── configs/
│   ├── eslint/                  # ESLint config and overrides
│   ├── jest/                    # Jest configuration and setup files
│   ├── storybook/               # Storybook main/preview configs
│   └── tailwind/                # Tailwind configuration & tokens
├── infrastructure/
│   ├── netlify/                 # `netlify.toml`, build/deploy config, edge functions
│   └── supabase/                # SQL migrations, RLS policies, seeding scripts
├── data/
│   ├── submissions/             # JSON persistence for analysis results (MVP)
│   └── reports/                 # JSON store for community reports (MVP)
├── docs/
│   ├── architecture.md          # System architecture reference
│   ├── architecture/            # Architecture supporting docs (standards, tree, stack)
│   ├── epics/                   # Epic-level documentation and story breakdowns
│   ├── front-end-spec.md        # UX front-end specification
│   ├── prd/                     # Sharded Product Requirements Document
│   └── project-brief.md         # PM executive summary
├── scripts/                     # Maintenance scripts (lint, data migrations, automations)
├── .ai/                         # AI agent debug logs and metadata
└── .bmad-core/                  # BMAD method assets (agents, checklists, workflows)
```

## Notes
- Feature folders under `apps/web/features/` encapsulate UI, hooks, and test files per story.
- Migration from JSON to Supabase moves data from `data/` into managed Postgres tables.
- Keep CI/CD configuration (`.github/workflows/`) co-located once initialized.


# Recommended Directory Layout

- **`src/app/`**
  Page routes and layouts (`page.tsx`, `layout.tsx`, etc.).
  Example: `src/app/known-scams/page.tsx` renders `/known-scams`.
  Nested folders (e.g., `src/app/admin/reports/page.tsx`) produce nested routes (`/admin/reports`).

- **`src/packages/shared/utils/`**
  Reusable helpers such as `supabase/server.ts`, hashing utilities, and other cross-cutting logic.

- **`data/`**
  Curated JSON, attachments, and other seed/test fixtures.
  Example: `data/known-scams/` for ground-truth SMS samples separate from live Supabase data.

- **`supabase/`**
  CLI-generated migrations, seed scripts, and RLS policies.

- **`configs/`**
  Tool configuration (ESLint, Jest, Storybook, Tailwind, etc.).

- **`docs/`**
  Documentation, including architecture references such as this source-tree guide.