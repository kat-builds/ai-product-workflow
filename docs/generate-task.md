# Implementation Task Generation Guidelines

Last updated: June 23, 2026

> **Objective:** Convert `docs/PRD.md` into a scoped, traceable, and verifiable implementation plan at `docs/tasks.md` without inventing requirements or starting implementation.

## 1. Core Concepts

### Task document

`docs/tasks.md` is the execution contract between the PRD and implementation. It defines scope boundaries, requirement traceability, component reuse, file ownership, task sequencing, verification, and handoff prompts.

It is not a second PRD. It may clarify how confirmed requirements will be implemented, but it must not introduce product behavior, business rules, routes, providers, copy, or infrastructure that the PRD does not authorize.

### PRD reference IDs

Every formal parent task must reference at least one PRD requirement ID, such as `FR-001`, `UX-002`, `API-001`, `DATA-001`, `PAY-001`, `SEC-001`, `SEO-001`, or `AN-001`.

If the PRD contains testable requirements without IDs, mark the task plan `Needs review` and request a PRD update. Do not create substitute IDs in `tasks.md`. A `BLOCKED-###` identifier tracks an implementation blocker; it never replaces a PRD ID.

### Scope terms

Use the same terminology as the PRD:

| Term | Task-plan treatment |
| --- | --- |
| `Current Scope` | Generate formal implementation tasks. |
| `Existing Baseline` | Generate only the work required to reuse, preserve, hide, remove from navigation, or leave untouched. |
| `Confirmed Next Phase` | Record under `Follow-up / Later`; do not generate executable tasks. It may justify limited infrastructure preparation only when the PRD explicitly requires it. |
| `Possible Later` | Record under `Follow-up / Later`; it must not affect current tasks or infrastructure. |
| `Non-Goals` | Record under `Out of Scope`; generate no implementation tasks. |

### Task categories

| Category | Purpose |
| --- | --- |
| **Formal parent task** | An executable, independently verifiable unit of Current Scope work. |
| **Subtask** | A numbered detail within a parent task. It is not independently assigned, checked off, or committed. |
| **Blocked Task** | A non-executable record of missing information, access, tooling, or a product decision. |
| **Confirmation Task** | A decision request that can be resolved without implementation. Use sparingly and keep it outside the formal task sequence. |
| **Follow-up / Later** | Non-executable future work or out-of-scope findings. |
| **Final Verification** | Repository-level checks required before the implementation is considered complete. |

### Verification

Verification must be evidence-based. Use commands and test methods that actually exist in the repository. Distinguish:

- **AI self-checks:** deterministic checks the coding agent can run and report, such as linting, type checking, targeted tests, route checks, or state assertions.
- **Manual tests:** experiential checks that require a person, such as visual quality, mobile feel, usability, readability, and end-to-end product judgment.

## 2. Inputs and Preflight Checks

### 2.1 PRD readiness

Read `docs/PRD.md` in full. It is usable only when it provides enough information to identify:

- Current Scope and Non-Goals;
- the Existing Baseline and treatment of template functionality;
- testable requirements and stable PRD IDs;
- core user journeys and acceptance criteria;
- applicable responsive and UI states;
- triggered API, data, authentication, storage, payment, analytics, security, privacy, and SEO requirements; and
- unresolved questions with blocking status.

Do not generate formal tasks for a capability when a blocking question controls its scope, provider, business behavior, data boundary, payment model, authentication model, information architecture, or user promise. Create a Blocked Task with an explicit unblock condition instead.

Non-blocking questions may remain in the plan, but the affected task must state the assumption and avoid irreversible decisions.

Ask clarification questions only when the answer cannot be recovered from the PRD or repository and a safe assumption is not available. Do not ask the user to make routine low-level engineering decisions.

### 2.2 Repository preflight

Inspect the repository before naming files, components, dependencies, or commands. At minimum, check:

- `AGENTS.md` and any nested instruction files;
- `package.json` and lockfiles;
- application routes and entry points;
- shared UI and feature components;
- design tokens and styling conventions;
- i18n configuration and locale resources;
- API routes, server actions, services, and provider adapters;
- schema, migrations, storage, and authentication code;
- test configuration and existing test patterns;
- deployment, environment, and platform configuration;
- `docs/design/`, SEO references, and other files cited by the PRD; and
- existing `docs/tasks.md`, if present.

Use fast, read-only discovery first (`rg --files`, `rg`, and focused file reads). Do not run builds, migrations, generators, installers, deployment commands, or other state-changing operations while generating the task document.

Only list a file path, script, component, environment variable, provider, or command when repository evidence supports it. Otherwise use `TBD` and state how it will be resolved.

Follow repository-specific placement rules. Prefer existing components and established module boundaries. If a new component is required and the repository mandates a component-creation workflow or skill, record that dependency explicitly.

### 2.3 Missing context

Missing design, SEO, repository, or provider context does not automatically block the entire plan. Mark the affected item as one of:

- `TBD — non-blocking`: implementation can proceed within a reversible boundary;
- `Needs review`: the source document should be corrected before execution; or
- `⛔ Blocked`: implementation cannot proceed safely.

Never invent missing context to make the plan appear complete.

### 2.4 Existing task document

When `docs/tasks.md` already exists, update it in place:

- preserve completed parent-task numbers and status;
- do not renumber existing tasks;
- append new parent tasks to the relevant phase or section;
- update traceability and scope summaries when the PRD changes;
- retain useful verification evidence; and
- move newly excluded work to `Follow-up / Later` instead of deleting history without explanation.

If the existing plan conflicts materially with the current PRD, mark the conflict and rebuild the affected section from the PRD. The latest confirmed PRD is authoritative.

## 3. Workflow

### Step 1: Read and classify the PRD

Build an internal inventory of:

- every Current Scope requirement ID;
- Existing Baseline items that need handling;
- Confirmed Next Phase and Possible Later items;
- Non-Goals;
- applicable UI states and responsive requirements;
- external providers and environment configuration;
- acceptance criteria; and
- blocking and non-blocking open questions.

Detect high-risk capabilities explicitly. Repository code or starter-template features do not trigger work unless the PRD does.

### Step 2: Resolve blocking boundaries

For each open question, determine whether work can proceed without fabricating a requirement or creating rework with material cost. If not, create a Blocked Task containing:

- the blocker;
- affected PRD IDs and tasks;
- why it blocks implementation;
- the required decision, input, access, or tool;
- the owner; and
- a precise unblock condition.

Do not include implementation steps inside a Blocked Task.

### Step 3: Scan the repository

Map PRD requirements to real routes, modules, components, locale files, tests, configuration, and scripts. Record whether each relevant component should be reused, modified within a defined boundary, newly created, hidden, or left untouched.

### Step 4: Freeze scope

Write `Scope Freeze` before decomposing tasks. It must clearly distinguish:

- `In Scope`;
- `Existing Baseline` treatment;
- `Out of Scope`; and
- `Follow-up / Later`, split into `Confirmed Next Phase` and `Possible Later`.

If scope cannot be frozen because the PRD is contradictory or incomplete, stop formal decomposition and create the appropriate review or blocker record.

### Step 5: Build the component reuse summary

For every UI area in scope, identify the existing component and source path when available, its planned treatment, the allowed modification boundary, and the related PRD IDs. New components require a concrete reason why reuse or bounded modification is insufficient.

Design references may guide visual hierarchy and layout, but they cannot create requirements, copy, routes, states, or interactions absent from the PRD.

### Step 6: Plan risk, configuration, sequencing, and ownership

For each triggered high-risk capability, record:

- the PRD source;
- provider or source of truth;
- server/client boundary;
- environment variables and who supplies them;
- security and privacy constraints;
- prerequisite tasks;
- failure and recovery behavior; and
- required verification.

Create a two-agent parallel plan only when work can be divided by clear file ownership and integration boundaries. Shared files, routing assembly, schemas, global configuration, and final QA belong in an explicit integration pass. If safe ownership boundaries do not exist, use a single-threaded plan.

### Step 7: Decompose work and map tests

Split work by independently verifiable outcomes, not by arbitrary file count. A parent task should usually deliver one coherent capability or integration boundary.

Each parent task must include:

- PRD references;
- objective and deliverable;
- dependencies;
- scope boundary and explicit exclusions;
- numbered subtasks;
- affected files;
- completion criteria; and
- verification method and expected evidence.

Avoid tasks so broad that they cannot be reviewed safely or so small that they create coordination overhead. Keep tightly coupled UI states, copy, responsive behavior, and tests with the capability they validate.

Create at least one happy-path test for every core journey and one failure-path test for every triggered high-risk capability. Cover applicable UI states and relevant 320 px, 768 px, and 1024 px breakpoints. Do not create tests for out-of-scope capabilities.

### Step 8: Assemble `docs/tasks.md`

Use the structure in Section 5. Generate only the document; do not execute tasks or commands embedded in it.

### Step 9: Review and save

Fix local editorial issues in place: terminology, numbering, missing references, formatting, duplicate coverage, and incomplete verification details.

Return to the relevant earlier step when the issue changes scope, contradicts the PRD, invents product behavior, misclassifies future work, or invalidates file ownership or task sequencing.

Run the `Tasks Self-Check` and save only after all applicable checks pass.

## 4. Task Authoring Rules

### Scope boundaries

A task may implement only Current Scope or explicitly required Existing Baseline cleanup. `Confirmed Next Phase`, `Possible Later`, `Non-Goals`, and newly discovered ideas must not appear as executable subtasks.

Every parent task must include a `Boundary / Exclusions` field. State what is deliberately not included, especially adjacent template capabilities such as authentication, Dashboard, Billing, Pricing, payments, storage, analytics, or admin features.

### i18n

User-facing final copy must use the repository's i18n system. Tasks must reference approved PRD copy and existing key conventions. Do not rewrite user-approved copy, hard-code strings in business components, or invent locale file paths.

### Design implementation

Use this authority order:

1. PRD for product scope, behavior, copy, and acceptance criteria;
2. repository instructions and architecture for implementation constraints;
3. existing design tokens and components for UI construction; and
4. design references for visual direction.

When sources conflict, do not silently choose. Mark the conflict as `Needs review` or blocked according to impact.

### Follow-up work

Record future work as plain, non-checkbox text:

```markdown
## Follow-up / Later

### Confirmed Next Phase

- Item — source and reason it is deferred.

### Possible Later

- Item — source and decision still required.

### Out-of-scope findings

- Item — discovered during planning; PRD update required before promotion.
```

Follow-up items do not receive formal task numbers, implementation steps, file lists, or execution prompts.

## 5. Required `tasks.md` Structure

Use GitHub-flavored Markdown and save the document at `docs/tasks.md`.

```markdown
# Tasks

> Source of truth: `docs/PRD.md`
> Status: Draft | Ready | Needs review | Blocked
```

Use the following section order.

### 5.1 Scope Freeze

```markdown
## 1. Scope Freeze

### In Scope
- Requirement or capability (`FR-001`, `UX-001`)

### Existing Baseline
- Existing capability — reuse / preserve / hide / leave untouched

### Out of Scope
- Explicit exclusion and PRD source

### Follow-up / Later
#### Confirmed Next Phase
- Non-executable item

#### Possible Later
- Non-executable item
```

Do not use vague statements such as “everything in the PRD.” Make the boundary auditable.

### 5.2 PRD Traceability Matrix

| PRD ID | Requirement summary | Scope class | Parent task | Verification | Status |
| --- | --- | --- | --- | --- | --- |
| `FR-001` | Example requirement | Current Scope | `1.0` | Targeted test and manual test 1 | Planned |

Include every Current Scope ID and every Existing Baseline ID that requires action. A requirement may map to multiple tasks, but ownership must be clear. Future and excluded items may appear for visibility but must have no formal task assignment.

### 5.3 Component Reuse Summary

| UI area | Existing component / path | Treatment | Modification boundary | PRD IDs |
| --- | --- | --- | --- | --- |
| Example form | `TBD` | Reuse / modify / create / hide / untouched | Exact allowed change | `FR-001`, `UX-001` |

If the work has no UI or component impact, write `Not applicable` and explain why.

### 5.4 High-Risk Capability Precheck

| Capability | Triggered | PRD IDs | Source of truth / provider | Key constraints | Task or blocker |
| --- | --- | --- | --- | --- | --- |
| API | Yes / No | `API-001` | Provider or `TBD` | Server-only secret, timeout, errors | `2.0` / `BLOCKED-001` |

Cover API/AI, authentication, database, storage/uploads, payments/credits, analytics, security/privacy, and SEO infrastructure. For untriggered capabilities, use `No — not in Current Scope`; do not create speculative setup tasks.

### 5.5 Relevant Files

Group evidence-backed paths under:

- `Core changes` — files that are expected to change;
- `Potential changes` — files that may change after a stated decision; and
- `New files` — files that are justified by a requirement and repository conventions.

For each path, state its role and related task. Use `TBD` rather than inventing a path.

### 5.6 External Providers & Configuration Handoff

| Provider / configuration | Purpose | Required values | Owner | Storage / exposure boundary | Blocking |
| --- | --- | --- | --- | --- | --- |

Include only providers and configuration triggered by the PRD. Use variable names found in the repository or explicitly specified by the PRD. Never include real credentials or credential-like examples.

### 5.7 Technical Constraints & Dependencies

List repository rules, runtime constraints, ordering dependencies, migrations, shared-module boundaries, and integration risks. Separate confirmed constraints from assumptions and TBDs.

### 5.8 Open Questions & Blocked Tasks

Preserve PRD blocking status. Use this format for blockers:

```markdown
### ⛔ BLOCKED-001: Confirm the checkout provider and webhook contract

- **Affected PRD IDs:** `PAY-001`, `SEC-002`
- **Blocks:** Parent task `3.0`
- **Reason:** The payment flow and source of truth cannot be implemented safely without this decision.
- **Required input:** Confirmed provider, product model, and webhook ownership.
- **Owner:** Product owner
- **Unblock condition:** PRD updated with the confirmed decision.
```

Do not disguise a blocker as an ordinary implementation task.

### 5.9 Phase Gates

Define gates only where later work depends on verified outcomes. Each gate must state prerequisites, checks, expected evidence, and which tasks it unlocks. Avoid ceremonial gates that add no risk control.

### 5.10 Two-Agent Parallel Plan

Include this section only when parallel execution is safe. Provide:

- a short schedule by round;
- an ownership table with writable and prohibited files for each agent;
- shared-file integration ownership;
- prerequisite and handoff points; and
- a final integration and QA task.

No file may have simultaneous owners. If file boundaries overlap materially, omit the parallel plan and use single-threaded execution.

### 5.11 Formal Parent Tasks

Use this exact heading pattern:

```markdown
### [ ] 1.0 Implement a specific, outcome-oriented capability

- **PRD references:** `FR-001`, `UX-001`
- **Objective:** Concrete outcome delivered by this task.
- **Dependencies:** None / task IDs / blocker IDs.
- **Boundary / Exclusions:** What this task may and may not change.
- **Subtasks:**
  - **1.1** First implementation step.
  - **1.2** Required state, responsive, copy, or integration work.
- **Affected files:** Evidence-backed paths or `TBD` with a resolution method.
- **Completion criteria:**
  - The observable, testable outcome.
  - The relevant failure and responsive behavior.
- **Verification:** Command or method, expected result, and required evidence.
- **Self-check:** Confirm PRD IDs, scope boundary, component reuse, files, and verification are consistent.
```

Parent tasks use sequential `1.0`, `2.0`, `3.0` numbering. Completed titles use `[x]`. Subtasks use `1.1`, `1.2`, and so on, but do not use checkboxes, receive separate commits, or receive separate execution prompts.

Start titles with a specific verb. Do not use vague completion criteria such as “works correctly,” “looks good,” or “improve error handling.” Prefer observable criteria, for example:

- Uploading a non-`.docx` file displays the copy mapped to `Tool.errors.unsupportedFile`.
- The page has no page-level horizontal overflow at 320 px.
- No payment, authentication, history, or cloud-storage logic is introduced.

Blocked Tasks use `BLOCKED-001` numbering. Follow-up items do not consume formal task numbers. During incremental updates, append numbers; never insert or reorder existing parent-task IDs.

### 5.12 Manual Test Plan

Keep manual and AI-executable checks separate. Manual tests appear first. Use one continuous sequence across both tables.

```markdown
## 12. Manual Test Plan

### Manual Tests

| # | Scenario | Page / entry point | Steps | Test data | Expected result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Primary journey | `/` | Complete the primary flow | Valid input | Result is readable and the next action is available | Not tested |

### AI Self-Checks

| # | Scenario | Page / entry point | Steps | Test data | Expected result | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | Empty input | `/` | Submit without input | Empty | Validation appears and no invalid request is sent | Not tested |
```

Omit only the empty subsection. If neither type applies, write `Not applicable — this plan requires no manual tests or AI self-checks.`

Every core journey needs a happy-path case. Every triggered high-risk capability needs a failure case. UI work must cover all applicable states and relevant breakpoints. Result-oriented tools must test at least one confirmed result action.

Execution prompts may reference only Manual Test numbers in the red manual-test reminder. AI self-checks are performed and reported by the implementer.

### 5.13 Final Verification

Use checkboxes and record the method, expected result, and evidence:

```markdown
- [ ] Verification item
  - Method: `repository-supported command or review procedure`
  - Expected result: Observable pass condition
  - Evidence: To be completed during implementation
```

Cover only enabled pages and in-scope capabilities. Use repository scripts rather than invented commands. Depending on scope, verify:

- enabled routes and complete end-to-end journeys;
- navigation, footer, metadata, canonical URLs, sitemap, and robots behavior;
- approved i18n copy;
- responsive behavior at 320 px, 768 px, and 1024 px with no page-level horizontal overflow;
- legal, analytics, authentication, payment, storage, API, and privacy behavior when triggered; and
- result actions and error recovery.

Review Legal and About content only when changes affect user data, uploads, AI/API use, payments, authentication, privacy promises, or brand positioning. Generate Blog or content-growth work only when the PRD places it in Current Scope.

### 5.14 Development Rules & Task List Management

Include these standing rules:

- Implement strictly against `docs/PRD.md` and `Scope Freeze`.
- Reuse components according to `Component Reuse Summary`.
- Load final user-facing copy through i18n.
- Never expose secrets in code, Markdown, logs, screenshots, or a public repository.
- Use only verification commands supported by repository instructions and scripts.
- Mark a parent task `[x]` only after its completion criteria and verification pass.
- Add newly discovered required work to `docs/tasks.md` before implementation.
- Put out-of-scope findings in `Follow-up / Later` until the user confirms a PRD update.
- Record blockers as Blocked Tasks, not ordinary subtasks.

Treat any change to routes, navigation, indexed content, shared modules, schemas, global configuration, authorization, data, payments, infrastructure, task ownership, or verification strategy as a potential scope change. Pause implementation when it affects product behavior or commitments; obtain user confirmation and update the PRD before continuing.

### 5.15 Execution Prompts

This must be the final section of `docs/tasks.md`. It contains copyable prompts only; generating the task plan must not execute them.

Create a new-site initialization prompt only when the PRD explicitly requires repository initialization or template migration and the referenced setup script exists. Derive authentication, local data, production data, and storage decisions from the PRD—not from template defaults.

For each formal parent task, generate a concise execution prompt:

```text
### Single-threaded: `<short task summary>`

Start task <parent task ID>.
Use the `Boundary / Exclusions` field in docs/tasks.md as the scope limit.

When complete:
- change the parent-task title from [ ] to [x];
- if implementation files changed, run the required verification and commit with a message beginning with <parent task ID>.

🔴 Manually test item(s) <actual Manual Test number(s)>.
```

Remove the red reminder when the task has no manual test. Do not generate execution prompts for Blocked Tasks or Follow-up items.

When a complete two-agent plan exists, generate one prompt per assigned round with the exact writable and prohibited file boundaries from the ownership table. Add a separate integration prompt for shared-file assembly, routing, and final QA.

## 6. Tasks Self-Check

Before saving `docs/tasks.md`, verify that:

1. `Scope Freeze` contains only Current Scope, required Existing Baseline treatment, explicit exclusions, and non-executable follow-up work.
2. The traceability matrix covers every Current Scope ID and every Existing Baseline ID requiring action.
3. Every formal parent task references at least one PRD ID.
4. The component reuse summary defines reuse, modification, creation, hidden, and untouched boundaries where relevant.
5. Files, components, providers, environment variables, and commands come from repository evidence; unknowns use `TBD`.
6. Open questions and blockers preserve the PRD's blocking status and contain no pretend implementation.
7. User-facing copy uses i18n and approved copy remains unchanged.
8. High-risk capabilities and infrastructure are included only when triggered by the PRD.
9. Applicable interactive states, responsive behavior, error paths, and result actions have tasks and tests.
10. PRD gaps are marked `Needs review` or blocked rather than filled with invented requirements.
11. Manual tests and Final Verification cover only in-scope behavior.
12. Parallel ownership has no overlapping files and includes an integration boundary.
13. Execution Prompts is the final section and does not instruct an implementer to continue automatically into the next parent task.
14. The file contains no secrets or realistic credential examples.

Resolve every failed check before saving.

## 7. Final Constraints

- Generate or update only `docs/tasks.md`. Do not modify product code or begin implementation.
- Use read-only repository inspection while planning; do not run state-changing commands.
- Do not repair missing product requirements inside the task plan. Update the PRD or create a blocker.
- Do not rewrite approved copy; require i18n for final user-facing strings.
- Do not generate, expose, or demonstrate API keys, secrets, tokens, OAuth credentials, webhook secrets, database URLs, or provider credentials.
