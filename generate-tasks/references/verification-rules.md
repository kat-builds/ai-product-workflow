# Verification and acceptance rules

Read this file when defining parent acceptance, `T-*`, `G-*`, or real integration.

## Match verification to blast radius

Use the smallest verification set that gives meaningful confidence for the planned change. Applicable `AGENTS.md` rules override generic defaults.

Typical objective checks include:

- typecheck
- focused Biome/lint
- existing focused unit/integration/regression tests
- `git diff --check`
- API/database/provider test-mode assertions when the task actually touches those surfaces and the environment permits them
- route/metadata/config checks required by the project

Do not invent commands. Use scripts and tools that actually exist in the repository or are explicitly required by applicable project rules.

## UI and E2E policy

Do not automatically plan UI/component unit tests merely because a task changes UI.

Do not automatically plan agent-driven browser verification, interactive click-through testing, screenshots, or visual-inspection loops.

Do not automatically create or run E2E tests.

For UI/copy/layout work, normally plan:

- relevant existing regression/domain tests
- typecheck
- focused lint/Biome
- `git diff --check` when applicable
- manual verification of the affected screens/interactions when project rules require it

When manual UI verification is required and remains part of acceptance after objective checks, use `验收方式：AI 验证后人工复查` and a focused `G-*` gate containing only the user's remaining checks.

Only plan E2E when at least one is true:

- the user explicitly requests it
- the task itself is to create/repair E2E coverage
- applicable project/release rules explicitly require it

When repeatable E2E is required, prefer deterministic Node.js + Playwright (or the repository's existing deterministic E2E runner) over agent-driven browser interaction. Reuse existing runnable specs/scripts before creating new ones.

Never claim E2E passed unless a runnable test was actually executed successfully.

## `T-*` AI verification

Every runnable parent must reference focused `T-*` rows required by the current template/validator.

A `T-*` row should describe an objective check the executor can actually run and judge from evidence. Define each test once in the central Verification Plan and reference it from the parent rather than duplicating the command everywhere.

Rules:

- cover the normal path for the task's core behavior
- add failure, duplicate, conflict, recovery, idempotency, or security checks only when the PRD or blast radius makes them relevant
- do not test capabilities that are outside Current Scope
- do not mark planned or inferred behavior as Passed/Verified
- do not use a human gate as a substitute for objective verification the executor can perform
- do not use AI verification as a reason to access production services or weaken repository safety rules

## Human review and `G-*`

Use a `G-*` only when objective verification is complete but an unavoidable human judgment or explicit approval still remains.

Examples:

- manual UI/interaction acceptance required by project policy
- subjective visual or brand judgment
- legal/commercial/final Go/No-Go decision
- explicit approval for a destructive, irreversible, production-sensitive action

A `G-*` contains only the remaining human step. It must not repeat source-code inspection, commands, `T-*`, API calls, database queries, or other technical evidence already handled by AI verification.

The user steps should state, in ordinary language:

- where to go
- what to do
- what to observe
- what counts as pass
- what to do if it fails

If the gate fails, reopen the affected parent and invalidate only the evidence/gates that are no longer trustworthy.

## Human prerequisites are not acceptance gates

Login, CAPTCHA, 2FA, secret/environment configuration, account permission, test account/data, or one-time platform setup are prerequisites, not `G-*` review gates. Handle them under `user-action-rules.md`.

## Real integration

Use the existing `真实联调` enum from the template/validator:

- `Not required`
- `Pending`
- `Verified`

`Pending` means implementation and local/mock/static verification may be complete while the real external dependency has not been tested.

Do not treat mock tests, typecheck, build, unit tests, planned calls, or an Approved parent as evidence that real integration is Verified.

If the PRD makes real integration a parent acceptance condition, the parent cannot become Approved until the real test has actually run and evidence is recorded. If the PRD explicitly allows real integration as a later non-blocking check, keep it Pending without misrepresenting it as completed.

## Verification plan semantics

The exact table structure and enums are owned by `assets/tasks-template.md` and `scripts/validate_tasks.py`.

Before finishing, semantically confirm:

- every parent has relevant focused verification
- each referenced `T-*` exists once and points to the correct parent/stage
- acceptance mode matches whether human review is actually required
- UI work follows the project's UI/E2E policy rather than automatically creating browser tests
- real integration status reflects actual evidence requirements
- no production service is used by automated verification unless the user explicitly authorized that production operation
