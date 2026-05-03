# 4. Technical Assumptions

- **Repository Structure:** Monorepo — All front-end and back-end code will live inside the existing Next.js project to simplify coordination and shared configuration.
- **Service Architecture:** Monolith (Next.js App + API Routes) — The application will use Next.js API routes for backend logic, deploying the entire solution as a unified service.
- **Testing Requirements:** Unit + Integration — Primary focus on Jest-based unit tests with targeted integration coverage across API routes and front-end interactions.
- **Additional Technical Assumptions and Requests:**
  - Front-end Stack: Next.js (React) with TypeScript for type-safe UI development.
  - UI Library: UntitledUI as the primary design system and component baseline.
  - State Management: Zustand for application state where React context is insufficient.
  - UI Testing & Review: Storybook for component isolation, visual review, and potential snapshot tests.
  - Backend: Next.js API routes for server-side logic.
  - Data Layer: Start with a JSON-file persistence layer during MVP; plan migration path to Supabase as data volume and auth needs grow.
  - Testing Tooling: Jest with React Testing Library for component and integration tests.
  - Deployment Platform: Netlify for hosting, leveraging its Next.js support, preview deploys, and environment-variable management for AI keys.
