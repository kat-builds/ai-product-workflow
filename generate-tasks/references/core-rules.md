# Core task-generation rules

Use these rules for every `generate-tasks` run.

## Authority and write boundary

- `docs/project/PRD.md` is the only product-scope and business-rule authority.
- Applicable project/agent instruction files define repository operation, validation, and user-interaction constraints.
- Repository code, config, scripts, tests, and deployment files establish implementation facts only; they do not create product requirements.
- Design, module, architecture, and playbook documents constrain implementation only when the PRD or applicable project rules make them relevant.
- Never infer new Current Scope from installed modules, template capabilities, routes, dependencies, providers, or reference documents.

When generating or updating tasks, modify only:

- `docs/project/tasks.md`
- `docs/project/task-prompt.md`

Do not modify the PRD, business code, tests, config, dependencies, migrations, deployment, production resources, or provider state. Do not commit during task generation.

If the user requests review/audit only, stay read-only unless they explicitly ask to fix the task documents.

When invoked from the `create-prd` Skill, use only the already validated PRD version and do not reopen product scope.

## Document roles

`docs/project/tasks.md` is the canonical task source of truth. It owns task scope, status, dependencies, acceptance, files, and verification references.

`docs/project/task-prompt.md` is derived from canonical tasks. It owns only the current recommended execution order, concise user-facing explanation, dependency/conflict snapshot, and copyable execution Prompt.

If the two documents disagree, `tasks.md` wins and `task-prompt.md` must be regenerated.

Do not place copyable execution Prompts, Worker assignments, branch/worktree details, or runtime scheduling snapshots in `tasks.md`.

## Scope mapping

Map PRD classifications as follows:

- `Current Scope` without a blocker -> Formal Task Package.
- `Existing Baseline` -> task only when the PRD requires reuse, preservation, hiding, redirect/noindex, validation, cleanup, or another explicit action.
- `Confirmed Next Phase` -> Follow-up / Later until promoted to Current Scope.
- `Possible Later` -> Follow-up / Later.
- `Non-Goals` -> Out of Scope.
- Blocking unresolved product decision -> Confirmation Task or Blocked Task.
- Non-blocking open question -> note or Follow-up / Later; do not block unrelated work.
- New idea without a stable PRD ID -> Follow-up / Later or update the PRD first.

Every Formal Task Package and Confirmation Task must trace to at least one real stable PRD ID.

## Task types

### Formal Task Package

Produces one coherent implementation result that can be independently accepted. Keep related implementation and its focused verification together.

### Confirmation Task

Produces a decision, investigation result, option analysis, configuration plan, feasibility result, or unblock condition. It must not implement production behavior. If the outcome changes product scope or business rules, update and validate the PRD before creating implementation work.

### Blocked Task

Records the blocker, affected PRD IDs, what may safely proceed, what must not proceed, and the unlock condition. Do not hide unresolved product or high-impact approval decisions inside an implementation task.

### Follow-up / Later

Records work outside Current Scope. It is not runnable and gets no execution Prompt.

## Parent task states

Use the existing template/validator state contract:

- `⬜ Pending`
- `🔵 In progress`
- `🟡 Ready for review`
- `✅ Approved`

Use `⛔ Blocked` only for a standalone Blocked Task, not as an alternative parent-state value.

For AI-only acceptance:

`⬜ Pending -> 🔵 In progress -> ✅ Approved`

For AI verification followed by required human review:

`⬜ Pending -> 🔵 In progress -> 🟡 Ready for review -> ✅ Approved`

Do not keep an Approved state when later evidence invalidates it. Reopen the affected task, reset invalidated human-review gates, and rerun only the affected validation.

## Incremental updates

If `tasks.md` already exists, update it incrementally unless the user explicitly requests a rebuild.

- Preserve valid task IDs and completed/in-progress history.
- Do not silently renumber, reorder, or rewrite unaffected historical tasks.
- Append new parent IDs after existing stable IDs.
- If a PRD change makes an old task obsolete, preserve its historical identity and record why it is no longer executable rather than reusing its ID for different work.
- Recompute `task-prompt.md` from the final canonical state every time.
- Approved parents appear only in the completed summary, not as active Prompt sections.
- Reopened parents return to the unfinished execution sequence.

## Repository evidence

Inspect only repository areas needed for the PRD scope being planned.

- Use real paths and real package scripts.
- Derive the framework, package manager, localization/content system, providers, test commands, and deployment tooling from the current repository; do not inherit those assumptions from a template, another repository, or this Skill.
- Prefer nearby implementation patterns and reusable components/utilities.
- Record a clear TBD only when a path or implementation fact genuinely cannot be verified.
- Do not invent provider setup, database work, deployment work, migrations, routes, or tests merely because the template supports them.
- Do not rewrite user-customized UI copy unless the PRD explicitly requires it.
- Never include real secrets, credentials, private URLs, verification codes, or test-account credentials in either task document.

## Output contract

The exact Markdown structure, required fields, enums, headings, and tables are defined by:

- `assets/tasks-template.md`
- `assets/task-prompt-template.md`
- `scripts/validate_tasks.py`
- `scripts/validate_task_conflicts.py`

Do not duplicate those mechanical contracts in prose. Follow the templates, then let the validators enforce structure and references.
