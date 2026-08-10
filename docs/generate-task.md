# Rules: Generate an Implementation Task Document (`tasks.md`)

Last updated: 2026-06-29

> One-sentence objective: Convert confirmed requirements with stable IDs in `docs/PRD.md` into a traceable, verifiable `docs/tasks.md` executed in verification stages. Every parent task package must pass AI self-checks and receive user approval before the next stage begins.

## I. Responsibilities and Boundaries

`docs/tasks.md` explains how to complete the work in stages, including scope freeze, requirement traceability, reuse boundaries, dependencies, affected files, task packages, verification, and execution prompts.

When generating or updating tasks:

- Write only `docs/tasks.md`; do not modify application code, configuration, the PRD, or other documentation.
- Read-only repository inspection using `rg`, `ls`, `sed`, and file reads is allowed.
- Do not install dependencies, start services, build, run database migrations, call providers, or deploy.
- Requirements and business rules come from `docs/PRD.md`. Repository inspection determines how to implement them, not what to implement.
- Design materials guide layout and visual direction only; they must not introduce functionality, states, entry points, or copy unconfirmed by the PRD.
- Do not modify user-customized UI copy, labels, or placeholders unless explicitly required by the PRD.
- Do not expose or demonstrate real API keys, secrets, tokens, OAuth secrets, webhook secrets, or database URLs.

If the user asks to “plan the tasks” or “generate tasks,” the current turn generates or updates only the task document and does not execute its tasks.

## II. Standard Classification Rules

### 2.1 Scope and Task Destination

| PRD category or status | Destination in tasks.md | Executable |
|---|---|---|
| Unblocked `Current Scope` | Formal parent task package | Yes |
| `Existing Baseline` requiring reuse, hiding, preservation, redirect, noindex, or closeout | Formal parent task package or task boundary | Yes, but not as new functionality |
| `Confirmed Next Phase` | `Follow-up / Later` | No, unless a new PRD promotes it to Current Scope |
| `Possible Later` | `Follow-up / Later` | No |
| `Non-Goals` | `Out of Scope` | No |
| `Blocking: Yes` or `⛔ Blocked` | `Blocked Task` | No |
| `Blocking: No` | Note or `Follow-up / Later` | Does not block other tasks |
| New requirement without a PRD ID | `Follow-up / Later` or require a PRD update first | No |

This table is the sole complete definition of scope treatment. Later sections apply it directly without repeating or expanding it.

### 2.2 Task Types

- **Formal Task Package:** A parent task that can be fully implemented, verified by AI, and submitted for user acceptance.
- **Confirmation Task:** Produces only an approach, affected-file list, configuration list, or unblock condition; it does not modify real business implementation.
- **Blocked Task:** Records the source, affected PRD IDs, permitted preliminary work, and unblock condition; it contains no real integration steps.
- **Follow-up / Later:** Work not executed now; it has no checkbox or execution prompt.

Every formal or confirmation parent task package must reference at least one PRD ID. A Blocked ID cannot replace a PRD ID.

### 2.3 Parent Task Status

Parent task packages are the unit of execution and verification. Their fixed lifecycle is:

```text
Pending → In progress → Ready for review → Approved
```

- `Pending`: Not started; title uses `[ ]`.
- `In progress`: All child items within the parent are being completed.
- `Ready for review`: AI verification has passed; stop and wait for user confirmation.
- `Approved`: The user has confirmed the task; only then change the title to `[x]`.

Child items describe required coverage inside the parent package. They have no checkbox and are not independently executed, committed, or given prompts.

## III. Five-Step Generation Workflow

### Step 1: Read the PRD and Check Usability and Blockers

Read `docs/PRD.md` and extract:

- `Current Scope`, `Existing Baseline`, `Confirmed Next Phase`, `Possible Later`, and `Non-Goals`;
- page, flow, functionality, copy, error, and non-functional requirement IDs;
- API, Data, Auth, Storage, Payment, Analytics, and external providers;
- design and technical constraints; and
- Open Questions, `Blocking`, and `⛔ Blocked` states.

Minimum usability requirements:

- Current Scope is not empty.
- Core flows and page scope can be determined.
- Every Current Scope item requiring implementation or verification has a stable PRD ID.
- Critical payment, authentication, data, and core-provider boundaries are not presented as confirmed when they remain unknown.

Treatment rules:

- If overall scope cannot be determined, do not generate a complete formal task plan; require the PRD to be corrected first.
- A local blocker blocks only related tasks; other unblocked Current Scope work may still generate tasks.
- If only a file path or component source is unknown, use `TBD`; do not block the requirement itself.
- If a gap changes product scope or business rules, do not decide it in tasks. Generate a Blocked/Confirmation Task or require a PRD update.
- When a question is necessary, follow the repository `AGENTS.md` format for numbering, options, Recommended, and Reason.

### Step 2: Scan Repository Context

Inspect only content relevant to the current PRD:

- `AGENTS.md`, `package.json` scripts, and repository execution rules;
- pages, routes, layouts, navigation, and footer;
- relevant components, shared UI, styles, and design tokens;
- i18n files, namespaces, and existing keys;
- site configuration, content system, metadata, sitemap, robots, and redirects when affected;
- API, database, auth, storage, payment, analytics, mail, and related directories only when triggered by the PRD;
- `env.example`, deployment configuration, and external-service usage points;
- design files, screenshots, or reference code specified by the PRD; and
- `docs/ui-patterns.md` when user feedback, states, or interaction patterns are involved.

Prioritize actual equivalent paths in the current repository, for example:

- `src/app/[locale]/*`, `src/app/api/*`;
- `src/components/*`, `src/styles/*`;
- `src/lib/*`, `src/ai/*`, `src/db/*`;
- `src/payment/*`, `src/analytics/*`, `src/mail/*`;
- `messages/*.json`, `content/*`, `src/config/*`;
- `src/app/sitemap.ts`, `src/app/robots.ts`, and metadata helpers; and
- Cloudflare, OpenNext, Wrangler, and deployment scripts that actually exist.

Rules:

- When a path is absent, find its actual equivalent; do not invent one.
- When it cannot be confirmed, write `TBD — verify actual file path in repo before implementation.`
- For reusable content, record source, target, allowed changes, and prohibited changes.
- Template capabilities do not enter Current Scope merely because they exist.
- Before adding a component, confirm that no existing component can be reused or modified within explicit boundaries.
- Verification commands may come only from `AGENTS.md`, `package.json`, or actual repository tooling.

### Step 3: Freeze Scope and Determine Dependencies

Generate:

- `In Scope`: Pages, functionality, copy, configuration, and verification included now, each referencing a PRD ID.
- `Existing Baseline`: Capabilities only reused, preserved, hidden, left untouched, or closed out.
- `Out of Scope`: Non-Goals and other explicitly excluded current content.
- `Follow-up / Later`: Confirmed Next Phase, Possible Later, and out-of-scope findings discovered during execution.

Also determine:

- whether API, database, auth, storage, payment, upload, analytics, and SEO/Legal are triggered;
- whether providers and environment variables are known, and whether missing configuration blocks all implementation, only real integration, or does not affect local UI/mock work;
- dependency order and shared high-conflict files; and
- whether new-site initialization, schema/migration, external-service configuration, or deployment prerequisites are required.

Generate new-site initialization only when explicitly required by the PRD and based on scripts and parameters that actually exist. Do not generate it merely because the template contains Cloudflare, Hyperdrive, or database configuration.

### Step 4: Decompose Parent Task Packages by Verification Stage

Use four to eight parent task packages in typical cases, but follow natural verification stages rather than forcing a count. Common stages include:

- foundational structure or shared contracts;
- core UI and page states;
- API, data, or provider integration;
- high-risk Auth, Payment, or Storage work; and
- integration, SEO/Legal, and pre-release closeout.

Rules:

- A parent task package must complete its child items continuously and produce one clear user acceptance point.
- UI and real API work may be separate stages so UI can be accepted first, but do not claim real integration is complete.
- Separate a Confirmation Task from implementation that depends on its result.
- Do not hide blocked work inside a formal parent's child items.
- Every parent states objective, boundaries, dependencies, files, AI verification, and user-acceptance test IDs.
- Do not begin the next parent task until the user approves the current one.
- If user acceptance fails, continue fixing the current parent; do not create a new stage to evade the issue.

Generate a parallel plan only when the user explicitly requests multiple AI agents. Default execution is single-threaded.

### Step 5: Assemble, Self-Check, and Save

- Generate or incrementally update `docs/tasks.md` using Chapter IV.
- Run Chapter VI Self-Check, correct all failures, and save as UTF-8 Markdown without a BOM.
- Do not execute generated tasks or commit instructions in the current turn.

## IV. `docs/tasks.md` Output Structure

The following statement must appear below the title:

> Document role: This file is the current project's staged execution checklist. Requirements and business rules come from `docs/PRD.md`; visual and implementation work follows the current project's design tokens, component system, i18n, and `AGENTS.md`. If a task conflicts with the PRD, update the PRD first, then adjust the task plan.

Generate the following sections in order. Omit untriggered conditional sections instead of mechanically writing `Not applicable`. `Execution Prompts` must be the final second-level section.

### 4.1 Scope Freeze

Always include these four subsections:

```md
## Scope Freeze

### In Scope
- `FR-001` — ...

### Existing Baseline
- `PAGE-002` — preserve / reuse / hide / leave untouched

### Out of Scope
- ...

### Follow-up / Later
#### Confirmed Next Phase
- ...
#### Possible Later
- ...
#### Out-of-scope Items Discovered During Execution
- ...
```

Empty Follow-up categories may be omitted, but they must not become formal tasks or implementation steps.

### 4.2 Traceability & Reuse

Keep two independent tables; do not combine the relationships.

Requirement traceability:

```md
| PRD ID | Requirement Summary | Task Package | Coverage | Status |
|---|---|---|---|---|
| FR-001 | ... | 1.0 | ... | Planned |
```

Rules:

- Cover all Current Scope IDs and Existing Baseline IDs requiring closeout.
- One ID may be covered by multiple tasks; one task may reference multiple IDs.
- When no code change is required, state `Covered by existing implementation`, `Verification only`, or `Documentation only`.

Generate the component-reuse table only when pages or components are involved:

```md
| Section / Component | Decision | Existing Source | Target | Allowed Changes | Must Not Change |
|---|---|---|---|---|---|
| ... | Reuse / Adapt / New / Hide / Do not touch | ... | ... | ... | ... |
```

A new component must explain why existing components cannot be reused and define its single responsibility and boundaries. When execution requires creating or cloning a component, use the configured `create-component` Skill. If that Skill is explicitly required but unavailable, report a blocker; do not bypass the rule and create the component arbitrarily.

### 4.3 Dependencies & Blockers (Conditional)

Generate when API, Data, Auth, Storage, Payment, Upload, Analytics, SEO/Legal, an external provider, or a blocker is triggered.

```md
| Capability | PRD IDs | Decision | Provider / Dependency | Required Config | Impact if Missing |
|---|---|---|---|---|---|
| Payment | PAY-001 | Configure / Reuse / Defer | ... | `VARIABLE_NAME` | ... |
```

Blocked Task format:

```md
### BLOCKED-001: Title
- Affected PRD IDs: ...
- Blocker source: ...
- Reason: ...
- Unblock condition: ...
- Allowed before unblocking: ...
- Prohibited: ...
```

Rules:

- List only environment-variable names and purposes, never real values.
- An unconfirmed provider must not generate steps for real integration, webhooks, entitlement crediting, schemas, or production configuration.
- When mock/UI work can proceed, explicitly state `mock only` and prerequisites for real integration.
- `Blocking: No` must not block unrelated tasks.

### 4.4 Relevant Files

```md
## Relevant Files

### Core Changes
- `path` — operation and scope

### Potential Changes
- `path` — trigger condition

### New Files
- `path` — purpose, or `TBD` when the path is unconfirmed
```

List only real paths found through repository inspection or explicit `TBD` entries. During incremental updates, preserve historical files that remain relevant; do not delete them silently.

### 4.5 Execution Plan (When the User Explicitly Requests Parallel Work)

Generate only when the user explicitly requests multiple AI agents in parallel and at least two parent task packages have independent write boundaries. Include:

- a short round schedule: initial sequential work, parallel stages, and final single-threaded integration;
- each AI's parent task packages, writable files, prohibited files, and deliverables;
- one owner for high-conflict files such as `messages/*.json`, routes, page entry points, global styles, schemas, migrations, environment files, and `docs/tasks.md`; and
- a single-threaded integration and verification stage after parallel work.

Do not parallelize across dependency stages or create a parallel assignment for a Blocked Task. If safe file boundaries cannot be established, omit this section and use single-threaded execution.

### 4.6 Task Packages

Parent task package format:

```md
### [ ] 1.0 Complete the Core UI

- Status: `Pending`
- Source: `PAGE-001`, `FR-001`, `ERR-001`
- Objective: Deliver an independently acceptable result.
- Boundary / Exclusions: Explicitly prohibit incidental scope expansion in this stage.
- Dependencies: A prerequisite parent task, configuration, or `None`.
- Child items:
  - 1.1 Page structure and primary actions
  - 1.2 Initial / empty / loading / error / success states
  - 1.3 i18n copy and responsive behavior
- Affected files: Real paths and operations; use `TBD` when unknown.
- AI verification: `T-002`, `T-003`
- User acceptance: `T-001`
```

Rules:

- Use consecutively numbered parent headings `### [ ] 1.0`, `2.0`, and so on; do not use `0.0`.
- Number child items `1.1`, `1.2`; do not use checkboxes.
- Use specific outcome- or action-based parent titles, not vague titles such as “handle some issues.”
- `Source` must reference PRD IDs; do not write only “refer to PRD.”
- `Boundary / Exclusions` prevents UI, API, payment, authentication, or out-of-scope content from entering the same stage.
- i18n tasks identify resource files and keys; do not hard-code final copy or rewrite user-customized copy.
- Environment/configuration changes include `env.example`. Schema changes include migration/fixture decisions according to the PRD and repository rules.
- Verification commands come from repository rules. UI/content tasks do not require `pnpm build` by default unless the user explicitly requests it.
- After completing AI verification, move the parent task to `Ready for review` and stop.
- After user approval, mark it `Approved` and `[x]`, then commit the stage according to the execution prompt.
- During incremental updates, append new parents with continued numbering; do not insert or reorder existing numbers.

### 4.7 Verification Plan

Define each test once; parent tasks reference only its ID.

```md
| ID | Stage | Scenario | Executor | Page / Entry | Steps or Command | Expected Result | Status |
|---|---|---|---|---|---|---|---|
| T-001 | 1.0 | Core UI | User | `/` | ... | ... | Not tested |
| T-002 | 1.0 | 320 px overflow | AI | `/` | ... | No page-level horizontal scrolling | Not tested |
```

Test requirements:

- At least one happy-path test for every core user journey.
- At least one critical failure test for every triggered high-risk capability.
- UI tasks cover PRD-required initial, empty, invalid, loading, error, success, and result-action states.
- Cover only relevant responsive breakpoints, including at least `320 / 768 / 1024` and no page-level horizontal scrolling.
- `Executor: AI` uses deterministic commands, E2E, or reproducible checks and must report evidence.
- `Executor: User` covers visual quality, interaction feel, real experience, or scenarios requiring human confirmation.
- Even if a parent has no dedicated User test, it must wait for user confirmation after AI self-checks before the stage ends.
- Do not generate tests for untriggered capabilities.

### 4.8 Development Rules & Task Management

Generate these concise fixed rules:

```md
## Development Rules & Task Management

- Follow the PRD, Scope Freeze, and parent-task boundaries strictly; put out-of-scope content in Follow-up / Later.
- Load final user-facing copy through i18n; do not overwrite user-customized copy.
- Prefer existing components and semantic tokens; new components follow Component Reuse Summary.
- Secrets exist only in server-side or deployment-platform secret storage, never in code, Markdown, logs, or screenshots.
- If scope, business rules, page structure, permissions, data, payments, or SEO indexing surfaces change, pause and update the PRD first, then update tasks.
- Append necessary new tasks while preserving numbering; create or update a Blocked Task when a blocker is found.
- When the current parent reaches Ready for review, stop; do not begin the next parent before user confirmation.
- After user approval, change the status to Approved and the title to [x], then execute the stage's commit instruction.
```

### 4.9 Execution Prompts

This must be the final second-level section in `docs/tasks.md`. Generate prompts only for formal parent task packages and Confirmation Tasks; do not generate them for Blocked Tasks or Follow-up work.

Single-threaded prompt:

```text
Start parent task package <number>: <title>.

Strictly follow the Source, Boundary / Exclusions, Dependencies, and file scope defined for this task package in docs/tasks.md. Do not expand scope. At the start, set the status to In progress, complete all child items continuously, and perform the listed AI verification.

After AI verification passes:
- Set the status to Ready for review
- Report the changes, verification evidence, and test IDs the user must execute
- Stop and wait for user confirmation; do not begin the next parent task package even when there is no manual browser test

After user acceptance passes:
- Set the status to Approved and change the title from [ ] to [x]
- If implementation files changed, complete the required verification and commit with a message beginning with <number>
- Do not automatically begin the next parent task package

If user acceptance fails, continue fixing and re-verifying the current parent task package. Do not create a new stage to evade the issue.
```

Use a parallel prompt only when an Execution Plan exists, and additionally state the AI identifier, writable files, and prohibited files. Every parallel parent independently enters `Ready for review`; the single-threaded owner defined in the plan handles shared-file integration and final QA.

When generating the task document, write only these future execution instructions. Do not execute tasks, change status, or commit.

## V. Incremental Updates to an Existing `docs/tasks.md`

If the file exists, update incrementally by default. Rewrite it entirely only when the user explicitly requests a rebuild.

- Preserve `[x]`, `Approved`, `Ready for review`, and `In progress` states.
- Do not silently delete, rewrite, or reorder historical tasks.
- When a PRD change invalidates a task, mark it `Superseded` or move it to Follow-up and state the reason.
- Append new parent task packages at the end of the relevant stage or all formal tasks, continuing numbering.
- Insert newly triggered conditional sections in output order; do not add empty untriggered sections for formatting completeness.
- Update Traceability, Relevant Files, Verification Plan, and corresponding Execution Prompts.
- Set `Last updated` to the actual update date.

## VI. Tasks Self-Check

Before saving, verify:

1. Scope Freeze exactly matches the five PRD scope categories.
2. Every Current Scope ID and Existing Baseline ID requiring closeout appears in traceability.
3. Every formal or confirmation parent task package references at least one PRD ID.
4. New ideas without PRD IDs appear only in Follow-up or require a PRD update.
5. Blocked content contains no real implementation, provider integration, schema, or production-configuration steps.
6. A local blocker does not prevent generation of unrelated Current Scope tasks.
7. File paths, component sources, and verification commands come from repository inspection; unknowns use `TBD`.
8. The Component Reuse table agrees with parent-task files and boundaries.
9. High-risk capabilities enter dependencies, tasks, and tests only when triggered by the PRD.
10. Only environment-variable names and purposes are listed; no real secrets or sensitive values appear.
11. Parent tasks follow natural verification stages and are not split merely to reach a count or mixed with out-of-scope content.
12. Child items have no checkboxes or independent prompts and are not separate execution units.
13. Every parent includes status, source, objective, boundary, dependencies, child items, files, and test IDs.
14. Every test is defined once in Verification Plan; parent tasks reference only IDs.
15. AI and User executors are explicit, with coverage for core flows and triggered error states.
16. Every parent task uses the `Ready for review` user gate.
17. `[x]` means `Approved`, not merely that AI self-checks passed.
18. No stage-completion commit or next parent begins before user confirmation.
19. A parallel plan exists only when explicitly requested, with one owner per high-conflict file.
20. i18n, design tokens, user-customized copy, and component-reuse rules are not bypassed.
21. UI/content tasks do not require `pnpm build` by default.
22. Incremental updates do not reset status, reorder numbering, or silently delete historical tasks.
23. Execution Prompts is the final second-level output section.
24. The file contains task planning only, not execution code, build output, migrations, or deployment results.
25. The file is UTF-8 without BOM, mojibake, or garbled text.

## VII. Final Constraints

1. Generate or update only `docs/tasks.md`; do not modify business files or begin implementation.
2. Do not redefine product requirements, expand scope, or invent PRD IDs in tasks.
3. Do not output untriggered sections or irrelevant verification merely to fill the template.
4. Parent task packages are the only formal units of execution and user acceptance; child items describe coverage only.
5. Every parent task must stop after AI self-checks and wait for user confirmation.
6. Commit instructions in future execution prompts do not authorize committing during task generation.
