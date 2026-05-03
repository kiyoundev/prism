# Prism Project Brief

## Overview
Prism is a web-based assistant that analyzes suspicious SMS messages or phone numbers, returning an explainable risk score and tailored guidance within three seconds. The product blends deterministic rules with AI-driven heuristics, captures community scam reports, and curates educational content so users can act confidently against fraud.

## Problem Statement
Consumers receive escalating volumes of scam texts and robocalls yet lack a trustworthy, self-serve way to evaluate them. Existing anti-spam tools are opaque, slow to adapt, or inaccessible to vulnerable users. As a result, individuals either ignore threats (risking harm) or overreact (blocking legitimate contacts) because they lack actionable, transparent advice.

## Proposed Solution
1. Accept SMS or phone number inputs, validate format, and trigger a hybrid rules + AI analysis pipeline.
2. Return an explainable risk score with human-readable factors, suggested actions, and safety education.
3. Offer a guided community reporting flow that expands Prism’s intelligence and informs future detections.
4. Deliver a responsive, WCAG AA-aligned UI that keeps vulnerable audiences in focus.

## Target Users
- Cautious consumers who routinely receive questionable texts or calls.
- Caregivers or advocates supporting vulnerable populations (e.g., seniors).
- Community moderators and product operators who review and act on new scam submissions.

## Key Goals
- `G1` Rapidly answer “Is this message safe?” with transparent reasoning.
- `G2` Empower users to take safe next steps (block, report, ignore) without confusion.
- `G3` Grow a vetted scam intelligence database through community contributions.
- `G4` Build trust with an accessible, privacy-conscious experience.

## Success Metrics (To Be Finalized)
- Analysis completion rate (% of submissions that return a score within 3s).
- User follow-through on recommended actions (e.g., reporting scams, blocking numbers).
- Community report volume and approval rate after moderation.
- User trust indicators (CSAT/NPS, qualitative feedback).

> **TODO:** Baselines and target values remain outstanding per PRD Appendix A; capture once research is complete.

## Scope & MVP Boundaries
- **In scope:** SMS/phone analysis, AI+rules pipeline, suggested actions, reporting stub, JSON persistence, Netlify deployment.
- **Out of scope (MVP):** Native mobile apps, full Supabase migration, advanced moderation tooling, personalized accounts.

## Dependencies & Risks
- External AI provider SLAs and cost constraints.
- Privacy obligations for storing user-submitted content.
- Accessibility compliance to serve vulnerable audiences effectively.
- Supabase migration path for scale (Epic 3) and associated downtime planning.

## Next Steps
1. Finalize business KPIs, personas, and research evidence (PRD Appendix A).
2. Coordinate with UX expert for a detailed front-end spec and accessibility guidelines.
3. Reconcile architecture follow-ups once PRD and UX gaps close.
4. Prepare implementation roadmap aligned with epics and story backlog.
