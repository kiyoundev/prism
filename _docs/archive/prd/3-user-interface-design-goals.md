# 3. User Interface Design Goals

## 3.1 Overall UX Vision
Deliver a reassuring, low-friction experience that lets users quickly paste a suspicious SMS or enter a phone number, receive an instantly understandable risk score, and gain confidence in the recommended next steps. The interface should feel trustworthy, transparent, and safe for vulnerable audiences.

## 3.2 Key Interaction Paradigms
- Single-field submission widgets for SMS text and phone numbers with inline guidance.
- Immediate analysis feedback with expandable detail for power users.
- Guided reporting workflow that encourages users to contribute new scam data without feeling overwhelmed.

## 3.3 Core Screens and Views
- Submission Home (text/number input, quick results, suggested actions).
- Detailed Analysis View (expanded explanation, AI reasoning, database matches).
- Report Scam Flow (step-by-step wizard to contribute new scams).
- Knowledge Base / Safety Tips (educational resources referenced from results).
- Account & Preferences (optional profile for frequent contributors — assumption).

## 3.4 Accessibility (WCAG AA)
Plan for WCAG AA compliance, including high-contrast color pairs, keyboard navigability, and screen-reader-friendly descriptions for risk scores and status indicators.

## 3.5 Branding
Assume a modern, calm aesthetic emphasizing trust: muted blues/greens, clear typography, and iconography that conveys safety. Brand assets are not yet defined—flagging as a dependency for future design work.

## 3.6 Target Device and Platforms
Primary focus is a responsive web experience optimized for desktop, tablet, and mobile browsers. Native mobile apps can be considered later based on adoption trends.

## 3.7 Primary User Flows
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

## 3.8 Edge Cases & Recovery
- Invalid or unsupported input formats trigger contextual validation messages and keep focus in the offending field.
- API or AI integration failure surfaces a non-technical error message, logs the event, and offers retry plus a link to manual safety advice.
- Users navigating away mid-report will see a warning modal to prevent accidental data loss (future enhancement flagged for Epic 3).

## 3.9 Information Architecture
- **Global Navigation:** Header links to Home (Analysis), Knowledge Hub, and Community Reporting with a persistent call-to-action button for “Check Message/Number.”
- **Results Layout:** Primary column presents risk score, explanation, and action playbooks; secondary column houses safety tips, knowledge articles, and optional reporting prompt.
- **Footer:** Includes trust badges, privacy policy, terms, and quick link to submit a new report.
- **Wizard Flow:** Reporting steps presented linearly with a progress indicator (Steps 1–4) and breadcrumb navigation for quick review before submission.

## 3.10 Key Content Requirements
- **Risk Result Banner:** Clear headline (“Potential Scam Detected” or “Low Risk”) with short subtext describing confidence and next steps.
- **Action Cards:** Short, imperative copy (e.g., “Block this number in your phone settings”) and optional tooltips explaining rationale.
- **Error States:** Plain-language messages for invalid input, rate limiting, or service outages, with suggested manual safety actions.
- **Reporting Confirmation:** Thank-you copy acknowledging contribution and setting expectation for moderation timeline.
- **Knowledge Articles:** Consistent structure with overview, warning signs, and prevention checklist formatted for readability.
