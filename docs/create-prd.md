# PRD Generation Guidelines

Last updated: June 23, 2026

> **Objective:** Turn an initial product request into a clear, implementation-ready Product Requirements Document (PRD) that a junior developer can execute with confidence.

## 1. Core Concepts

### Definitions

| Term | Definition |
| --- | --- |
| **High-risk capability** | Any capability that requires additional product, security, or operational constraints, including third-party or AI APIs, webhooks, authentication, authorization, databases, storage, file uploads, user-owned data, history, payments, credits, quotas, and analytics. |
| **Upstream specification** | Any source document supplied by the user, such as an `idea2spec` output, design brief, `prdv0`, draft PRD, or design notes. |
| **P0 question** | A blocking question that affects Current Scope, infrastructure, payments, authentication, data, information architecture, or a core interaction. It must be resolved before the PRD is generated. |
| **P1 question** | A non-blocking question with a defensible default. State the proposed assumption before generating the PRD. |
| **P2 question** | A question that does not affect implementation of the Current Scope. Record it under `Open Questions`. |

### Scope terminology

Use these terms consistently throughout the repository:

| Term | Meaning |
| --- | --- |
| `Current Scope` | Work explicitly included in this PRD. |
| `Existing Baseline` | Functionality that already exists in the repository, is already live, or was completed in an earlier phase and is not new work in this PRD. |
| `Confirmed Next Phase` | Functionality the user has committed to implementing next. It is not part of the current implementation, but may inform infrastructure decisions. |
| `Possible Later` | Uncommitted future work. It must not affect the Current Scope or infrastructure decisions. |
| `Non-Goals` | Work explicitly excluded from this PRD. |

`Current Scope` is the canonical scope label. Do not use alternatives such as `Current V1`, `V1 Scope`, or `Current Version`. Labels such as V1, V2, and Phase 2 may identify releases, but they do not determine scope.

When work from a `Confirmed Next Phase` begins, create or update the PRD and promote that work into a new `Current Scope`. Move completed functionality into `Existing Baseline`. Never promote future work implicitly.

## 2. Workflow

### Step 1: Analyze the request

Complete the following analysis before asking questions.

#### Classify the project

| Project type | Typical characteristics |
| --- | --- |
| Client-side utility | No backend, persistent storage, or accounts |
| API-powered utility | Uses a third-party API and a lightweight backend |
| AI generation product | Calls an AI API and exposes generation results or status |
| Monetized product | Includes payments, subscriptions, credits, quotas, or paid access |
| Content-led product | Primarily publishes content and may also include tools or accounts |

The classification determines how much detail the PRD needs. Keep simple projects lightweight. Expand the relevant requirements when the product uses APIs, data, authentication, storage, payments, entitlements, or analytics. Record the result under `Project Type & Scope Depth`.

#### Map upstream specifications

If an upstream specification exists, normalize it before drafting the PRD.

| Upstream label or intent | PRD destination |
| --- | --- |
| Current work | `Current Scope`, `Functional Requirements`, and `Interaction Flows` |
| Existing functionality | `Existing Baseline`; use only to decide what to reuse, preserve, hide, or leave untouched |
| `Confirmed Next Phase` | Preserve only when the source explicitly commits to it or the user confirms it |
| `Possible Later` | `Possible Later / Future`; do not create implementation or infrastructure requirements |
| Explicit exclusion | `Non-Goals`; do not generate features, pages, components, or tasks |
| `Need Decision` | `Open Questions`; elevate to P0 if it affects scope, infrastructure, payments, authentication, data, page structure, or core interactions |
| `Copy Guidance for STITCH` | Design-stage guidance only; final copy is governed by `UI Copy, Error Messages & i18n Mapping` unless explicitly approved |
| `Design Notes for STITCH` | The relevant part of `Design-to-Implementation Plan` |
| `Do Not Include in UI` | `Design Authority Rules`, `Risks & Decisions`, or `Non-Goals`, depending on intent |

Enforce these boundaries:

- Never promote `Possible Later` to `Current Scope` or `Confirmed Next Phase` without explicit user confirmation.
- Repository code does not automatically make a capability part of the Current Scope.
- Template functionality cannot override `Non-Goals`.
- Do not silently drop a `Need Decision` item or present it as resolved.
- The user's latest explicit decision takes precedence over upstream material. Mark superseded material as `Explicitly Overridden`.

Summarize the mapping under `Version Scope & Infrastructure Decision`.

#### Detect high-risk requirements

Check the Current Scope for:

- third-party APIs, AI APIs, webhooks, and provider SDKs;
- authentication, accounts, roles, and permissions;
- database access, user assets, history, file storage, and cloud storage;
- payments, subscriptions, credits, quotas, and paid entitlements; and
- analytics, behavioral tracking, and conversion measurement.

Use the result to determine the depth of `API, Data, Payment & Analytics Requirements`, `Security, Privacy & Compliance`, `Error States & Edge Cases`, and `External Providers & Configuration Handoff`.

### Step 2: Ask clarification questions

Ask only when information is genuinely missing and cannot be inferred safely. Do not ask the user to make low-level architecture decisions.

- Ask P0 questions in the current round.
- State recommended assumptions for P1 questions before generating the PRD.
- Add P2 questions to `Open Questions` with `Blocking: No`.
- Combine related questions where practical, but do not conceal independent decisions.
- Treat provider, API, payment, authentication, or storage choices as P0 when they determine whether a core Current Scope feature is feasible.

Assumptions must be supported by the project type, repository structure, design context, responsive defaults, or prior user confirmation. Never invent pricing, API endpoints, provider limitations, data-retention policies, or payment models.

If mobile behavior is unspecified, apply the defaults in `Mobile & Responsive Requirements`. If authentication is confirmed in Current Scope but the sign-in methods are unspecified, default to Google OAuth and email/password and state that any disabled entry points must be enabled.

Typical clarification areas include the user problem, primary journey, exclusions, success criteria, domain and SEO keywords, release scope, APIs, data and authentication, payments and entitlements, analytics, and the treatment of template-only routes such as Pricing, Dashboard, Upgrade, Billing, or Login.

If a capability appears in a draft, template, or “Coming Soon” message but is absent from Current Scope, confirm whether it is `Confirmed Next Phase`, `Possible Later`, or `Template Only`. Ask separately when different capabilities have different release timing.

#### Question format

Number every question. Prefer two to four multiple-choice options and include both a recommendation and a short rationale. For free-text values such as a domain, price, or provider, provide a recommended default or example.

```text
Reply with letters in order, e.g. ACB = 1A 2C 3B.

1. What is the primary objective of this feature?
   A. Improve onboarding
   B. Increase retention
   C. Reduce support volume
   D. Generate revenue

   Recommended: A
   Reason: This provides the clearest basis for interaction and acceptance criteria.

2. What is the primary domain? (Free text)

   Recommended: example.com
   Reason: The domain affects SEO, metadata, and brand copy.

3. When should payments be introduced?
   A. Confirmed Next Phase — committed for the next release
   B. Possible Later — under consideration, but not committed
   C. Template Only — present in the starter, but not planned for this product

   Recommended: B
   Reason: This determines whether payment and database infrastructure should be prepared now.
```

If the user answers only some questions, do not assume the remaining answers unless they explicitly accept all recommendations. Continue asking unresolved P0 questions; apply and disclose recommended P1 assumptions.

If the requested output filename conflicts with this standard—for example, `RPD.md` instead of `PRD.md`—confirm the intended convention before writing the file.

### Step 3: Interpret the answers

Classify each requirement by the meaning of the answer, not by the original P0/P1/P2 label.

| Decision | Treatment |
| --- | --- |
| Required now | Add to `Current Scope` and `Functional Requirements` |
| Already available, with no new work | Add to `Existing Baseline` and document whether to reuse, preserve, hide, or leave untouched |
| Committed for the next phase | Add to `Confirmed Next Phase`; exclude it from current features, pages, components, and implementation |
| May be considered later | Add to `Possible Later`; do not let it influence current infrastructure |
| Explicitly excluded | Add to `Non-Goals`; generate no related feature or page |
| Still unresolved | Add to `Open Questions`; never drop it silently |

### Step 4: Generate the PRD

Write the final document to `docs/PRD.md` in GitHub-flavored Markdown. Include only confirmed requirements, disclosed assumptions, and unresolved questions—not the clarification dialogue itself.

Place this note below the title:

> **Document purpose:** This PRD defines what the product must do and how it must behave, including functional logic, interaction flows, business rules, information architecture, and acceptance criteria. Visual references live in `docs/design/`; implementation must follow the repository's design tokens, component system, and i18n conventions.

Place this language policy immediately after it:

> **Language policy:** This document is written in English. User-facing copy must be loaded from i18n resources and must not be hard-coded in business components. Code identifiers, routes, field names, and internal terminology must also use English.

### Step 5: Review and save

Run the `PRD Self-Check`, resolve every failed item, and then save the document. A failed check may not be skipped.

## 3. Required PRD Structure

### Document depth

Match detail to product complexity. Expand sections only when APIs, payments, authentication, storage, uploads, complex state transitions, or template customization require it. Do not pad the document with repetitive `Not applicable` entries.

For a required section that does not apply, write `Not applicable` and one sentence explaining why. For `API, Data, Payment & Analytics Requirements`, write a single `Not applicable` line when the entire section is irrelevant; when only some capabilities apply, include only the relevant subsections.

Missing repository, design, SEO, or engineering context must not stop PRD generation. Briefly identify what is unavailable and add only decisions that materially affect the product or implementation to `Open Questions`.

Use the following top-level order unless this guide explicitly allows omission:

1. `Introduction / Overview`
2. `Domain & Primary Keywords / SEO References`
3. `Goals & Acceptance Criteria`
4. `User Scenarios`
5. `Project Type & Scope Depth`
6. `Version Scope & Infrastructure Decision`
7. `Glossary`
8. `Design Reference`
9. `Page Structure & Information Architecture`
10. `Mobile & Responsive Requirements`
11. `Functional Requirements`
12. `Interaction Flows`
13. `API, Data, Payment & Analytics Requirements`
14. `Security, Privacy & Compliance`
15. `UI Copy, Error Messages & i18n Mapping`
16. `Error States & Edge Cases`
17. `Design-to-Implementation Plan`
18. `Technical Considerations`
19. `External Providers & Configuration Handoff`
20. `Success Metrics / Tracking Plan`
21. `Open Questions`
22. `Non-Goals`
23. `Implementation Notes & Constraints`

### Requirement IDs and traceability

Assign stable IDs to testable requirements:

- `FR-###` — functional requirements
- `UX-###` — interaction and responsive behavior
- `API-###` — provider and API behavior
- `DATA-###` — persistence, ownership, and retention
- `PAY-###` — payments, credits, quotas, and entitlements
- `SEC-###` — security, privacy, and compliance
- `SEO-###` — metadata, indexing, canonical URLs, and structured data
- `AN-###` — analytics and success measurement

IDs must be unique and stable. Acceptance criteria and downstream tasks must reference them. Do not assign IDs to speculative future work.

### Scope and infrastructure decision

Include a compact matrix that distinguishes `Current Scope`, `Existing Baseline`, `Confirmed Next Phase`, `Possible Later`, and `Non-Goals`. For each infrastructure capability—API, database, authentication, storage, payments, and analytics—state one of:

- `Required now`
- `Prepare now for Confirmed Next Phase`
- `Reuse Existing Baseline`
- `Not required`
- `TBD — blocking decision required`

Infrastructure preparation is justified only by Current Scope or an explicitly Confirmed Next Phase. Template code and Possible Later ideas are not sufficient justification.

### Functional and interaction requirements

For each core capability, define inputs, outputs, validation, state transitions, business rules, failure behavior, and acceptance criteria. Describe complete user journeys from entry point to result, including recovery paths.

Interactive experiences must cover every applicable state:

`initial` → `empty` / `invalid` → `loading` → `success` / `error` → result action

Result actions may include copy, download, reset, retry, or return to input, but only when confirmed by scope. Define disabled states, duplicate submission behavior, timeout handling, and preservation or clearing of user input.

### Mobile and responsive requirements

Define behavior at 320 px, 768 px, and 1024 px where relevant. Requirements must cover content priority, stacking, navigation, touch targets, overflow, long content, tables, dialogs, and keyboard behavior. Page-level horizontal scrolling is not acceptable at supported widths.

### APIs, data, payments, and analytics

Include only triggered subsections.

For APIs, define the provider, server/client boundary, request and response contract, timeout, retry, rate limits, degraded behavior, and configuration ownership. Never expose secrets in client code, documentation examples, logs, or screenshots.

For data, define ownership, schema intent, source of truth, persistence, retention, deletion, migration, and access boundaries. Do not invent a retention policy.

For payments, define the product model, entitlement source of truth, webhook behavior, idempotency, failed-payment behavior, cancellation, refunds where applicable, and UI states. Pricing and commercial policy require explicit user confirmation.

For analytics, define event names, trigger conditions, properties, consent requirements, and the decision each event supports. Avoid collecting unnecessary personal data.

### Security, privacy, and compliance

Document trust boundaries, validation, authorization, secret handling, file constraints, data exposure, privacy disclosures, and applicable legal surfaces. Do not invent legal guarantees. Any unresolved issue that could expose user data, money, credentials, or privileged actions is blocking.

### UI copy and i18n

List approved user-facing copy and its i18n key. Include labels, helper text, empty states, validation messages, loading text, success feedback, error recovery, and result actions. Preserve copy explicitly approved by the user. Do not hard-code final strings in UI components.

### Design authority

Design references govern visual direction and layout only. They must not introduce unconfirmed features, copy, states, routes, or business rules. The PRD governs product behavior; repository design tokens and components govern implementation details.

The implementation plan must identify reusable components, components requiring bounded modification, genuinely new components, and template components that should remain hidden or untouched. Do not fabricate file paths or components that were not found in the repository; use `TBD` when evidence is unavailable.

### Open questions

For each open question, include:

- the decision required;
- `Blocking: Yes` or `Blocking: No`;
- the affected requirement IDs or sections;
- the recommended option, when a safe recommendation exists; and
- the owner or source needed to resolve it.

A blocking question must not coexist with requirements that pretend the same decision is already settled.

## 4. PRD Self-Check

Before saving `docs/PRD.md`, verify that:

1. Scope terminology is consistent and future work has not leaked into Current Scope.
2. Every upstream item is mapped, explicitly overridden, or retained as an open question.
3. The project type and document depth are appropriate.
4. Goals are measurable and acceptance criteria are testable.
5. Requirement IDs are unique, stable, and traceable.
6. Core journeys, responsive behavior, states, errors, and recovery paths are defined.
7. APIs, data, authentication, storage, payments, analytics, security, and privacy are expanded only when triggered.
8. No provider, endpoint, price, policy, path, component, environment variable, or command has been invented.
9. User-facing copy uses i18n keys and approved copy has not been rewritten.
10. Design references do not override product requirements.
11. Missing context and unresolved decisions are visible, with correct blocking status.
12. `Non-Goals` are explicit and generate no implementation requirements.
13. The PRD contains no secrets or realistic secret placeholders.
14. The file uses valid GitHub-flavored Markdown and is saved at `docs/PRD.md`.

## 5. Final Constraints

- Generate or update only `docs/PRD.md`; do not start implementation as part of this workflow.
- Do not execute state-changing commands while preparing the PRD. Read-only repository inspection is allowed.
- Do not turn assumptions into confirmed business rules.
- Do not expose API keys, secrets, tokens, OAuth credentials, webhook secrets, database URLs, or provider credentials.
- If a P0 decision remains unresolved, stop at the decision boundary and ask the user. Do not draft around it as though it were confirmed.
