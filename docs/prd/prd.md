# Prism Product Requirements Document (PRD)

## 1. Goals and Background Context

### 1.1 Goals
- Provide fast scam analysis that returns a risk score and explanation for SMS text or phone call inputs.
- Empower users to take safe next steps with clear suggested actions based on the scan results.
- Expand the shared scam intelligence database through community reporting of new incidents.
- Maintain a trustworthy experience that protects user data while integrating with third-party AI services.

### 1.2 Background Context
The Prism project addresses the increasing volume of SMS and phone-call scams targeting broad consumer groups, including vulnerable populations. Today, individuals lack an accessible way to evaluate suspicious communications, creating uncertainty and risk. Prism combines predefined detection rules, AI-powered classification, and an evolving database of known scam keywords and numbers to deliver accurate, explainable results in under three seconds. By allowing users to submit new scam reports, the system continually expands its coverage and offers the broader community a reliable first line of defense.

### 1.3 Change Log
| Date       | Version | Description               | Author |
|------------|---------|---------------------------|--------|
| 2025-09-23 | v0.1    | Initial PRD draft created | PM     |

## 2. Requirements

### 2.1 Functional Requirements
1. **FR1:** The system must accept either an SMS text body or phone number input and run a scam analysis workflow on each submission.
2. **FR2:** The system must return a numerical risk score with an accompanying plain-language explanation for every analyzed input.
3. **FR3:** The system must surface recommended user actions (e.g., block, ignore, report) tailored to the analysis outcome.
4. **FR4:** The system must allow users to report suspected scams, storing the message/number in the shared database for future detection.
5. **FR5:** The system must cross-check submissions against a maintained database of known scam keywords and phone numbers.
6. **FR6:** The system must integrate with at least one external AI API to enrich scam detection beyond static rules.

### 2.2 Non-Functional Requirements
1. **NFR1:** Each analysis request must complete in under three seconds to maintain a responsive user experience.
2. **NFR2:** The platform must scale to handle high concurrent usage and an expanding scam-report database with minimal performance degradation.
3. **NFR3:** All user-submitted data and third-party API interactions must be secured in transit and at rest, complying with privacy best practices.
4. **NFR4:** The user interface must be intuitive and accessible for non-technical and vulnerable users while supporting power users.
5. **NFR5:** The codebase must be modular and well-documented so the development team can iterate quickly on new detections or integrations.

## 3. User Interface Design Goals

### 3.1 Overall UX Vision
Deliver a reassuring, low-friction experience that lets users quickly paste a suspicious SMS or enter a phone number, receive an instantly understandable risk score, and gain confidence in the recommended next steps. The interface should feel trustworthy, transparent, and safe for vulnerable audiences.

### 3.2 Key Interaction Paradigms
- Single-field submission widgets for SMS text and phone numbers with inline guidance.
- Immediate analysis feedback with expandable detail for power users.
- Guided reporting workflow that encourages users to contribute new scam data without feeling overwhelmed.

### 3.3 Core Screens and Views
- Submission Home (text/number input, quick results, suggested actions).
- Detailed Analysis View (expanded explanation, AI reasoning, database matches).
- Report Scam Flow (step-by-step wizard to contribute new scams).
- Knowledge Base / Safety Tips (educational resources referenced from results).
- Account & Preferences (optional profile for frequent contributors — assumption).

### 3.4 Accessibility (WCAG AA)
Plan for WCAG AA compliance, including high-contrast color pairs, keyboard navigability, and screen-reader-friendly descriptions for risk scores and status indicators.

### 3.5 Branding
Assume a modern, calm aesthetic emphasizing trust: muted blues/greens, clear typography, and iconography that conveys safety. Brand assets are not yet defined—flagging as a dependency for future design work.

### 3.6 Target Device and Platforms
Primary focus is a responsive web experience optimized for desktop, tablet, and mobile browsers. Native mobile apps can be considered later based on adoption trends.

### 3.7 Primary User Flows
1. **Suspicious Content Analysis**
   - **Entry:** User lands on the home screen via direct link or saved bookmark.
   - **Steps:** Selects SMS or phone input → provides content → submits → system validates format → backend runs hybrid rules + AI analysis → results screen renders risk score, explanation, and suggested actions.
   - **Branches:**
     - Invalid input (empty, malformed number) → inline error messaging with resubmission path.
     - Analysis delay beyond three seconds → loading state with retry option and status link.
   - **Exit:** User reviews actions, optionally expands explanations, or proceeds to reporting flow.

2. **Community Reporting Flow**
   - **Entry:** User clicks "Report this scam" from results or navigation.
   - **Steps:** Guided wizard collects structured details (message, number, category, notes) → validation/sanitization → confirmation screen summarizing submission.
   - **Branches:** Missing required fields → inline prompts; user aborts mid-flow → partial data discarded with optional save reminder (future enhancement).
   - **Exit:** Success message with optional opt-in for follow-up notification; user returns to results or knowledge hub.

3. **Knowledge Hub Exploration**
   - **Entry:** User opens safety tips panel from results or navigates directly to knowledge hub.
   - **Steps:** Browse categorized articles → open detailed tip → follow cross-links to related guidance.
   - **Branches:** Article unavailable (network error) → fallback message with retry; outdated article flagged by moderation → display notice.
   - **Exit:** User returns to primary analysis flow or reports new scam with updated knowledge.

### 3.8 Edge Cases & Recovery
- Invalid or unsupported input formats trigger contextual validation messages and keep focus in the offending field.
- API or AI integration failure surfaces a non-technical error message, logs the event, and offers retry plus a link to manual safety advice.
- Users navigating away mid-report will see a warning modal to prevent accidental data loss (future enhancement flagged for Epic 3).

### 3.9 Information Architecture
- **Global Navigation:** Header links to Home (Analysis), Knowledge Hub, and Community Reporting with a persistent call-to-action button for “Check Message/Number.”
- **Results Layout:** Primary column presents risk score, explanation, and action playbooks; secondary column houses safety tips, knowledge articles, and optional reporting prompt.
- **Footer:** Includes trust badges, privacy policy, terms, and quick link to submit a new report.
- **Wizard Flow:** Reporting steps presented linearly with a progress indicator (Steps 1–4) and breadcrumb navigation for quick review before submission.

### 3.10 Key Content Requirements
- **Risk Result Banner:** Clear headline (“Potential Scam Detected” or “Low Risk”) with short subtext describing confidence and next steps.
- **Action Cards:** Short, imperative copy (e.g., “Block this number in your phone settings”) and optional tooltips explaining rationale.
- **Error States:** Plain-language messages for invalid input, rate limiting, or service outages, with suggested manual safety actions.
- **Reporting Confirmation:** Thank-you copy acknowledging contribution and setting expectation for moderation timeline.
- **Knowledge Articles:** Consistent structure with overview, warning signs, and prevention checklist formatted for readability.

## 4. Technical Assumptions

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

## 5. Epic Overview
1. **Epic 1: Prism Foundation & Core Detection** — Establish the Next.js app shell, initial scam analysis workflow (rules + AI integration), JSON-based persistence, and basic risk score presentation so users can submit inputs and get actionable results.
2. **Epic 2: Explanations, Guidance & Trust** — Enhance the results experience with richer explanatory narratives, suggested actions, accessibility improvements, and WCAG AA compliance to convert raw scores into confident user decisions.
3. **Epic 3: Community Reporting & Intelligence Growth** — Launch the user-reporting flow, moderation tooling, and Supabase migration plan that expand scam intelligence while keeping data secure and maintainable.
4. **Epic 4: Knowledge Hub & Continuous Improvement** — Deliver the safety tips knowledge base, Storybook-driven UI polish, analytics hooks, and iterative improvements informed by usage data to sustain engagement.

## 6. Epic 1 Prism Foundation & Core Detection
Establish the core Prism experience so users can submit suspected scams and receive immediate, trustworthy feedback. This epic creates the unified Next.js monolith, baseline UI, initial analysis workflow, and JSON persistence that all later work builds upon.

**Epic Goal**
Launch a fully deployable Prism MVP that ingests SMS text or phone inputs, analyzes them via the hybrid rules+AI workflow, and returns an intelligible risk score with suggested next steps—all backed by JSON-based storage.

### 6.1 Story 1.1 MVP Shell & Submission Flow
**As a** cautious consumer  
**I want** a secure Prism web app with clear input fields for SMS text or phone numbers  
**So that** I can quickly submit suspicious content for analysis without friction.

**Acceptance Criteria**
1. `FR1` — Landing page renders in Next.js, offering separate inputs for SMS body and phone number with validation for empty/invalid submissions.
2. `FR2` — Submission triggers a client-side request to an API route that returns a stubbed risk score payload (e.g., medium risk with placeholder explanation).
3. `FR3` — UI displays the returned score and explanation in an accessible format (WCAG AA color contrast; screen-reader labels).
4. `FR5` — JSON persistence layer (local file) records each submission with timestamp and input type for future analysis.

### 6.2 Story 1.2 Hybrid Analysis Pipeline (Rules + AI)
**As a** worried user  
**I want** Prism to evaluate suspicious inputs against known patterns and AI heuristics  
**So that** I receive a trustworthy risk score grounded in both rules and intelligent analysis.

**Acceptance Criteria**
1. `FR6` — Backend integrates with a configurable AI API client (mocked via environment variables) to classify risk based on input content.
2. `FR5` — Keyword/number rule engine matches submissions against the JSON database, capturing rule hits alongside AI responses.
3. `FR2` — API route merges rule hits and AI output into a single risk score (0–100) plus human-readable explanation.
4. `NFR1` — Pipeline responds within three seconds under normal load; include logging to surface slow requests.

### 6.3 Story 1.3 Actionable Recommendations & JSON Persistence Enhancements
**As someone** evaluating scammers  
**I want** clear guidance on what to do about a suspicious message  
**So that** I can take safe next steps without second-guessing.

**Acceptance Criteria**
1. `FR3` — API route maps risk tiers (low/medium/high) to tailored suggested actions (e.g., “block number,” “delete message,” “report to carrier”).
2. `FR5` — JSON data store captures the calculated risk score, explanation, and suggested actions for each submission.
3. `FR2` — UI displays suggested actions alongside the score, with expandable detail for the reasoning that led to them.
4. `NFR4` — Recommended actions are accessible (semantic markup, focus order, responsive layout) per UI design goals.

### 6.4 Story 1.4 Community-Friendly Reporting Stub
**As a** privacy-conscious user  
**I want** the ability to flag suspicious messages for community tracking  
**So that** Prism’s intelligence can grow even before the full reporting workflow ships.

**Acceptance Criteria**
1. `FR4` — UI includes a “Report this scam” affordance that opens a modal/wizard requesting minimal extra context.
2. `FR4` — API route appends reported data to JSON storage with a “pending review” flag.
3. `FR5` — Storage schema differentiates between analyzed submissions and user-reported incidents for later moderation.
4. `NFR3` — Submission sanitization removes personally identifiable information beyond the provided message/number; document assumptions in code comments.

## 7. Epic 2 Explanations, Guidance & Trust
Deepen Prism’s credibility by turning raw risk scores into empathetic, accessible guidance that users can trust. This epic builds on the core analysis pipeline to humanize explanations, embed safety education, and deliver WCAG-compliant UI refinements.

**Epic Goal**
Transform Prism’s MVP into a confidence-building assistant that explains scam risks clearly, recommends next steps, and reinforces trust through accessibility, transparency, and targeted education.

### 7.1 Story 2.1 Narrative Risk Explanations & Transparency
**As a** skeptical user  
**I want** to understand why Prism labeled my message as risky  
**So that** I can trust the recommendation and take appropriate action.

**Acceptance Criteria**
1. `FR2` — API augments risk payloads with structured factors (rule hits, AI indicators) and exposes them to the UI.
2. `FR3` — UI renders a human-readable explanation that references the specific signals contributing to the score.
3. `NFR4` — Explanations support screen readers with semantic markup and ARIA labels describing confidence levels.
4. `NFR1` — Added reasoning does not push response time above three seconds; log slow cases.

### 7.2 Story 2.2 Suggested Action Playbooks
**As a** cautious consumer  
**I want** tailored advice for each risk level  
**So that** I know exactly what to do and why.

**Acceptance Criteria**
1. `FR3` — Define reusable action playbooks for low, medium, high risk, including rationale and optional follow-up tips.
2. `FR3` — UI surfaces the action list alongside the explanation with icons and plain-language guidance.
3. `NFR4` — Action layouts respond gracefully on mobile, tablet, desktop with focus order tested via keyboard navigation.
4. `NFR3` — Document in code comments how sensitive data is masked before showing examples/actions.

### 7.3 Story 2.3 Accessibility & WCAG AA Enhancements
**As a** user with accessibility needs  
**I want** Prism to be easy to read, navigate, and operate  
**So that** I can rely on it without assistance.

**Acceptance Criteria**
1. `NFR4` — Audit color palette against WCAG AA; adjust contrast tokens (muted blue/green) and document choices.
2. `NFR4` — Ensure all controls (inputs, buttons, modals) are fully operable via keyboard and announce their state changes.
3. `NFR4` — Add skip-to-content link, form field descriptions, and aria-live regions for asynchronous results.
4. `FR2` — Verify automated accessibility tests (Storybook a11y add-on or equivalent) cover risk result components.

### 7.4 Story 2.4 Safety Education & Knowledge Hooks
**As someone** who wants to avoid future scams  
**I want** relevant safety tips when I get a result  
**So that** I learn how to recognize similar threats.

**Acceptance Criteria**
1. `FR3` — Introduce a dynamic “Safety Tips” panel that maps risk tiers and scam categories to educational content.
2. `FR2` — Tips pull from a JSON-driven knowledge base that is versioned and editable for later expansion.
3. `NFR2` — Lazy-load or cache tips to avoid slowing down the primary analysis response.
4. `NFR4` — Tips include clear headings, bullet lists, and optional links with accessible descriptions.

## 8. Epic 3 Community Reporting & Intelligence Growth
Channel community contributions into Prism’s knowledge base while preparing the platform for scalable data handling. This epic introduces the full reporting workflow, moderation controls, and the initial Supabase migration path so user submissions genuinely strengthen scam detection.

**Epic Goal**
Enable high-quality community reporting with secure data storage that transitions from JSON persistence toward Supabase, ensuring reports enhance detection accuracy without sacrificing performance or privacy.

### 8.1 Story 3.1 Reporting Wizard & Data Capture
**As a** vigilant community member  
**I want** a guided reporting experience  
**So that** I can share scam details without worrying about format or sensitive information.

**Acceptance Criteria**
1. `FR4` — Multi-step wizard collects structured details (message text, phone number, scam category, optional notes) with validation and inline masking guidance.
2. `NFR4` — Wizard is responsive (mobile/desktop) and screen-reader friendly, including progress indicators and descriptive labels.
3. `FR5` — Submitted reports append to the JSON data store with schema separating reports vs. analyzed submissions.
4. `NFR3` — Input sanitation strips personal info (e.g., email addresses) before persisting, with notes in code comments.

### 8.2 Story 3.2 Moderation Dashboard & Review Workflow
**As a** product owner/moderator  
**I want** tools to review and approve community reports  
**So that** the intelligence database stays accurate and trustworthy.

**Acceptance Criteria**
1. `FR5` — Build an admin-only Next.js route showing pending reports with search/filter capabilities.
2. `FR5` — Moderation actions (approve, flag, discard) update the JSON data store with audit timestamps.
3. `NFR3` — Protect the admin route with basic authentication guard (e.g., environment-configured token) before merging into Supabase auth later.
4. `NFR2` — Document performance considerations (e.g., pagination) to keep moderation views responsive as dataset grows.

### 8.3 Story 3.3 Supabase Schema & Migration Plan
**As a** technical lead  
**I want** a clear plan for moving from JSON persistence to Supabase  
**So that** we can scale storage and analytics without disrupting users.

**Acceptance Criteria**
1. `FR5` — Define Supabase schema (tables for submissions, reports, moderation actions) with column types and indexes reflecting current JSON structure.
2. `NFR2` — Provide a migration checklist covering data export/import, environment setup, and fallback strategy for downtime.
3. `NFR3` — Specify access controls (service roles, row-level policies) required to preserve user privacy.
4. `FR6` — Document how AI integration keys and logs will be stored securely in Supabase, including environment variable mapping.

### 8.4 Story 3.4 Integrated Intelligence Feedback Loop
**As a** curious contributor  
**I want** to see how my report helps the community  
**So that** I feel rewarded for participating.

**Acceptance Criteria**
1. `FR5` — Approved reports update the detection pipeline (e.g., keywords, phone numbers) with timestamps for when they become active.
2. `FR2` — Risk explanations highlight when a new report influenced the analysis (e.g., “Community report from 2 days ago flagged this number”).
3. `FR3` — UI sends an optional success confirmation (email/stubbed notification) summarizing how the report will be used.
4. `NFR1` — Pipeline maintains sub-three-second response times even with expanded datasets; add caching or batching as needed.

## 9. Epic 4 Knowledge Hub & Continuous Improvement
Deliver sustained value by turning Prism into a learning destination with polished UI, analytics insights, and ongoing quality refinement.

**Epic Goal**
Launch user-facing knowledge resources, Storybook-driven UI governance, and analytics loops that keep the experience evolving in response to real-world usage.

### 9.1 Story 4.1 Knowledge Base & Resource Hub
**As a** security-conscious user  
**I want** a curated knowledge hub with scam-prevention guides  
**So that** I can educate myself beyond a single analysis result.

**Acceptance Criteria**
1. `FR3` — Create a static-content knowledge hub accessible from the main UI, linking category-specific tips and prevention guides.
2. `NFR2` — Render knowledge pages statically via Next.js (ISR/SSG) to ensure fast load times and SEO benefits.
3. `NFR4` — Ensure all knowledge content follows accessibility standards (headings, alt text, common keyboard navigation).
4. `FR5` — Sync knowledge articles with the JSON data layer so they can be surfaced contextually inside the core app experience.

### 9.2 Story 4.2 Storybook Governance & Visual Consistency
**As a** UI reviewer or designer  
**I want** Storybook stories and automated visual checks  
**So that** the UntitledUI implementation stays consistent as we iterate.

**Acceptance Criteria**
1. `FR3` — Document all primary UI components (inputs, risk cards, modals, tips) in Storybook with controls and usage notes.
2. `NFR4` — Integrate Storybook accessibility and interaction testing add-ons to catch regressions early.
3. `NFR5` — Set up Storybook snapshot or visual diff tests in CI (stubbed if necessary) to detect unintended styling changes.
4. `FR2` — Annotate stories with links back to corresponding functional requirements for traceability.

### 9.3 Story 4.3 Analytics & Feedback Instrumentation
**As a** product manager  
**I want** telemetry on user actions and outcomes  
**So that** we can prioritize improvements based on actual behavior.

**Acceptance Criteria**
1. `FR2` — Instrument key events (submission, tip expansion, report start/completion) with anonymized analytics hooks.
2. `NFR3` — Document privacy considerations and ensure personally identifiable information is never logged.
3. `NFR2` — Configure batching/debouncing so analytics calls do not degrade UI performance.
4. `FR3` — Provide a lightweight dashboard or query scripts to summarize conversion metrics (analysis completion rate, report submissions, knowledge hub visits).

### 9.4 Story 4.4 Continuous Improvement Toolkit
**As a** cross-functional team member  
**I want** an evolving feedback loop driven by metrics and user interviews  
**So that** Prism benefits from ongoing iteration informed by both numbers and anecdotes.

**Acceptance Criteria**
1. `NFR5` — Create a versioned “continuous improvement” guide in the repository outlining how telemetry, qualitative feedback, and bug reports feed the roadmap.
2. `FR2` — Implement experimentation toggles (feature flags) for future A/B tests on result explanations or tips.
3. `FR3` — Provide a structured feedback form within the app that routes to team channels (email or logging stub for MVP).
4. `NFR2` — Ensure feature flags and feedback endpoints remain performant and do not block core analysis flows.

## 10. Appendix A – PM Checklist Findings (In Progress)
- **Problem Statement – Partial:** Add quantitative impact data (e.g., industry scam statistics) and a short comparison to existing anti-spam tools to clarify differentiation.
- **Business Goals & Success Metrics – Missing:** Define 3–4 measurable objectives with baselines and timelines, such as analysis completion rate, community reporting adoption, and trust/satisfaction scores.
- **User Research & Insights – Partial:** Document lightweight personas, note available or planned research sources, and summarize competitive landscape observations to ground assumptions.
- **Security & Compliance – Partial:** Capture authentication/authorization approach, privacy/compliance obligations, API key management, and the security testing plan.
- **Reliability & Resilience – Partial:** Define availability targets, backup and restoration strategy (especially for Supabase migration), failure-recovery expectations, and operational ownership.
- **Architecture Guidance – Partial:** Summarize integration points between the monolith, AI API, and future Supabase backend; note performance safeguards (rate limits, caching) and high-risk areas needing architectural investigation.
- **Technical Decision Framework – Partial:** Document decision criteria, trade-offs, and rationale for selecting the current approach over alternatives, including non-negotiable constraints and open technical questions.

### 10.1 Checklist Category Status Snapshot
| Category | Status | Follow-up Notes |
| --- | --- | --- |
| 1. Problem Definition & Context | Fail | Add KPIs, quantitative impact, research evidence. |
| 2. MVP Scope Definition | Partial | Document scope boundaries and MVP validation plan. |
| 3. User Experience Requirements | Pass | – |
| 4. Functional Requirements | Pass | – |
| 5. Non-Functional Requirements | Partial | Expand security/compliance and reliability sections. |
| 6. Epic & Story Structure | Pass | – |
| 7. Technical Guidance | Partial | Provide integration guidance and decision framework. |
| 8. Cross-Functional Requirements | Fail | Add data, integration, and operational requirements. |
| 9. Clarity & Communication | Partial | Define stakeholder alignment and communication plan. |

### 10.2 Top Issues by Priority (from PM Checklist)
- **BLOCKERS:** Business goals & KPIs, security & compliance posture, and data/integration/operational requirements remain undocumented (`docs/prd.md:19-34`, `docs/prd.md:321-328`).
- **HIGH:** Reliability & resilience strategy, technical decision framework, and stakeholder alignment plan need dedicated sections (`docs/prd.md:321-328`).
- **MEDIUM:** Scope boundaries & MVP validation approach, user research evidence/personas, and quantified differentiation metrics should be added (`docs/prd.md:1-113`, Appendix A).
- **LOW:** Future enhancements/roadmap guidance can be fleshed out once core gaps are resolved.

## 11. Checklist Results Report
_To be completed after running the PM checklist._

## 12. Next Steps

### 12.1 UX Expert Prompt
```
You are the UX Expert reviewing the "Prism Product Requirements Document (PRD)" located at docs/prd.md.
Focus on validating the UX Design Goals and epic/story expectations related to user flows, accessibility, and trust-building.
Deliver refined UX recommendations, identify any UX risks, and outline suggested next UX tasks for designers.
```

### 12.2 Architect Prompt
```
You are the Architect analyzing the "Prism Product Requirements Document (PRD)" at docs/prd.md.
Evaluate the technical assumptions, non-functional requirements, and epic/story breakdown for architectural completeness.
Propose the initial technical architecture, highlight critical decisions, and recommend next steps to de-risk implementation.
```
