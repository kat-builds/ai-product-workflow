# <Product or Feature Name> Product Requirements Document (PRD)

> Document role: This file defines current product scope, functional logic, interaction flows, business rules, page/entry structure, and acceptance outcomes. Visual implementation follows the project's confirmed Design System, shared components, and UI conventions when applicable.

> Language: Use the language selected by the applicable project instructions or the user's current request. User-facing copy follows the product's actual language and localization/content system; do not assume English, i18n, or a specific framework.

- Last updated: YYYY-MM-DD
- Document language: en
- Status: Draft / Confirmed / Partially Blocked
- Product decision priority: latest explicit user decision > confirmed upstream requirement not overridden > existing PRD decision still in force > verified repository fact > design/playbook/template reference
- Output boundary: this document defines product requirements only; do not include implementation tasks, commands, migrations, deployment steps, or commit instructions

## 1. Introduction & Goals

### Product Overview

<What the product is and what this PRD covers.>

### User Problem & Target User

- User problem: <specific problem>
- Target user: <specific audience>
- Core value: <observable value>

### Current Goals & Success Criteria

- `NFR-001` — <measurable goal or acceptance outcome>

### Adopted Assumptions

- <Only record non-blocking assumptions that matter. Write "None" when there are none.>

## 2. Domain, Audience & SEO

- Domain: <domain or TBD>
- Target region: <region>
- Site language: <language>
- Primary audience: <audience>
- SEO handling: <current relevant strategy; if not applicable, say why briefly>

## 3. Project Type & Scope

### Project Type

- Type: <Simple frontend tool / Content site / API tool / AI tool / Account product / Paid product>
- PRD depth: <why specialist sections are or are not needed>

### Current Scope

- `FR-001` — <capability being implemented or changed now; define it formally below>

### Existing Baseline

- `PAGE-001` — <existing capability and its Reuse / Preserve / Hide / Redirect / Noindex / Do not touch / Delete handling>

### Confirmed Next Phase

- <Explicitly committed later work and any future impact. Write "None" when absent. Do not create current requirements or activate infrastructure from this section.>

### Possible Later

- <Possible future work that is not committed. Write "None" when absent.>

### Explicitly Overridden

- <Earlier requirement superseded by the latest decision and the replacement decision. Write "None" when absent.>

### Infrastructure Decisions

| Capability | Decision | Scope basis | Notes |
|---|---|---|---|
| Database | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID or No Current Scope trigger> | <notes> |
| Auth | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID or No Current Scope trigger> | <notes> |
| Storage | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID or No Current Scope trigger> | <notes> |
| Payment | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID or No Current Scope trigger> | <notes> |
| Analytics | <Reuse / Configure / Extend / Defer / Not required / Blocked> | <Current Scope ID or No Current Scope trigger> | <notes> |

Only `Reuse / Configure / Extend` activates a capability for Current Scope, and its Scope basis must cite Current Scope IDs. Reference docs, templates, Existing Baseline, Confirmed Next Phase, or Possible Later do not activate current infrastructure by themselves.

## 4. User Scenarios

### Scenario 1: <Name>

- User: <role>
- Trigger: <when this starts>
- Goal: <what the user wants to achieve>
- Expected result: <observable outcome>

## 5. Page Structure

### `PAGE-001` — <Page or Entry Name>

- Route: `/example`
- Page role: <responsibility>
- Handling: New / Reuse / Adapt / Hide / Preserve / Do not touch / Redirect / Noindex / Delete
- Section order: <order>
- Key states: initial / empty / loading / error / success
- Primary CTA: <actual user-facing copy or COPY ID>
- Navigation / footer handling: <explicit decision>

## 6. Interaction Flows

### `FLOW-001` — <Complete Flow Name>

1. The user enters from <entry>.
2. The user performs <action>.
3. The system shows <immediate feedback>.
4. On success, the system shows <result> and allows <next step>.
5. On failure, enter `ERR-001` and allow the user to <recover or retry>.

## 7. Functional Requirements

### `FR-001` — <Single Testable Requirement Title>

- Trigger: <user action or condition>
- System behavior: <behavior and business rules>
- User-visible result: <what the user sees>
- Boundaries: <what is excluded or limited>
- Acceptance criteria: <directly testable outcome>

## 8. API, Data, Auth, Storage & Payment

Keep only the subsections actually triggered by Current Scope. For simple projects, state that specialist capabilities are `Not required` instead of retaining unused placeholders.

### API / Provider (when applicable)

- `API-001` — <purpose, input, output, failure/timeout/limit behavior, server boundary, variable names>

### Data / Auth / Storage (when applicable)

- `DATA-001` — <accounts, permissions, stored data, owner, lifecycle, refresh/recovery, deletion, and failure handling>

### Payment / Entitlement (when applicable)

- `PAY-001` — <mode, product mapping, checkout return, webhook authority, idempotency, entitlement, and recovery>

### Analytics (when applicable)

- Event: `<event_name>`
- Trigger: <condition>
- Properties: <necessary non-sensitive properties>
- Privacy boundary: <what is not collected>
- Success metric: <how success is measured>

## 9. Mobile & Responsive

### Breakpoints

<Use the project's existing breakpoints / viewport policy. If none exists, record only representative viewports the product actually needs to support and verify. For non-UI products, write "Not applicable — <reason>".>

### Rules

- No page-level horizontal scrolling.
- Wide tables, charts, code blocks, tabs, or lists scroll only inside their owning component when needed.
- Input areas may shrink, but key buttons, units, and actions must remain operable.
- Narrow-screen navigation and toolbars use an explicit wrap, stack, or horizontal-scroll strategy.

### Mobile acceptance criteria

1. <At the narrowest representative supported viewport, the core flow remains usable with no page-level horizontal scrolling.>
2. <At a representative phone viewport, primary inputs, CTA, states, and results do not overlap, clip, or move out of the operable area.>
3. <At a representative medium/tablet viewport, the transformed layout keeps the correct section order, information hierarchy, and key actions.>

For non-UI products, write: `Not applicable — <reason>`.

## 10. Error States, Security & Privacy

### Error States

#### `ERR-001` — <Error Name>

- Trigger: <error condition>
- User message: <user-facing copy in the product's actual language, or COPY ID>
- System behavior: <system handling>
- Retry: <whether/how to retry>
- Next step: <what the user can do next>

### Security & Privacy

- Data storage: <what is or is not stored>
- Third-party transfer: <what is or is not sent>
- Logging: do not log full user inputs/results, credentials, or sensitive personal data.
- Secrets: record environment-variable names and purposes only; values belong in server-side secret storage.
- Legal update: <whether Privacy / Terms / Cookie / disclosure updates are required and why>

## 11. UI Copy & Localization

| ID | Context | User-facing copy | Localization / key (if applicable) | Decision |
|---|---|---|---|---|
| `COPY-001` | Primary CTA | `<actual product copy>` | `<existing key or Not used>` | Reuse / New / Preserve |

Preserve user-customized copy, labels, placeholders, pricing copy, and marketing copy unless the PRD explicitly changes them.

## 12. Design & Technical Constraints

### Design priority

1. Product behavior, states, and business rules defined by this PRD.
2. Current project component system, design tokens, and global styles.
3. Screenshots, design exports, or reference code for layout and visual proportion.

### Applicable project references

List only references that were actually read and are triggered by classified scope. The existence of a document does not create Current Scope.

| Reference | Why applicable | Allowed effect | Scope effect |
|---|---|---|---|
| `<verified/path.md>` | <triggering Current Scope / Confirmed Next Phase / explicit baseline decision> | <constraint or reuse boundary> | Does not create Current Scope |

### Reuse and ownership

- <page sections, component responsibilities, state ownership, and Reuse / Adapt / New / Do not touch decisions>

### Product-relevant technical constraints

- <verified framework/runtime, localization approach, server/client boundary, or deployment constraint; do not include implementation commands or unverified paths>

## 13. Non-Goals

- <explicit exclusion> — Reason: <out of scope / later phase / explicitly excluded by the user>.

## 14. Open Questions

### OQ-001 — <Unresolved Question; if none exist, write "None" and remove this example>

- Question: <question>
- Impact area: <scope, page, payment, data, etc.>
- Options:
  - A: <current reasonable option A>
  - B: <current reasonable option B>
  - C: <current reasonable option C>
- Recommended: <A / B / C>
- Reason: <one concise reason>
- Blocking: 🔴Yes / No
- Current implementation impact: <current impact>
- Owner: <owner>
- Needed by: <stage or date>
- Temporary assumption: <adopted temporary assumption, or None>
