# Implementation Tasks

Last updated: YYYY-MM-DD
Document language: en

> Document role: This file is the canonical task source of truth for the current project. It defines task scope, requirements, dependencies, status, and acceptance. Product requirements and business rules come from `docs/project/PRD.md`; the copyable execution prompts live in `docs/project/task-prompt.md`. If the two task documents disagree, this file wins and `task-prompt.md` must be regenerated.

> Task status: ⬜ Pending · 🔵 In progress · 🟡 Ready for review · ✅ Approved · ⛔ Blocked

## Scope Freeze

### In Scope

- `FR-001` — ...

### Existing Baseline

- `PAGE-001` — how the existing capability is preserved, reused, hidden, or intentionally left untouched.

### Out of Scope

- ...

### Follow-up / Later

#### Confirmed Next Phase

- ...

#### Possible Later

- ...

#### Out-of-scope findings discovered during execution

- ...

## Traceability & Reuse

### Requirement Traceability

| PRD ID | Requirement Summary | Task Package | Coverage | Status |
|---|---|---|---|---|
| `FR-001` | ... | `1.0` | ... | Planned |
| `FR-002` | ... | `2.0` | ... | Planned |
| `FR-003` | ... | `3.0` | ... | Planned |

### Component Reuse Summary

| Section / Component | Decision | Existing Source | Target | Allowed Changes | Must Not Change |
|---|---|---|---|---|---|
| ... | Reuse / Adapt / New / Hide / Do not touch | ... | ... | ... | ... |

## Dependencies & Blockers

### Task Dependency Graph

| Task Package | Direct Dependencies | Unlocks | Start Condition |
|---|---|---|---|
| `1.0` | `None` | `2.0` | PRD and repository facts are sufficient |
| `2.0` | `1.0` | `None` | `1.0` ✅ Approved; required human prerequisite is provided before real provider verification |
| `3.0` | `None` | `None` | PRD and repository facts are sufficient; task number does not create a dependency on `1.0` |

### External Dependencies & Blockers

| Capability | PRD IDs | Decision | Provider / Dependency | Required Config | Impact if Missing |
|---|---|---|---|---|---|
| ... | `FR-002` | Reuse / Configure / Defer | ... | `VARIABLE_NAME` | ... |

<!-- Include the following structure only when a real blocker exists. -->

### BLOCKED-001: Title

- Status: `⛔ Blocked`
- Affected PRD IDs: `FR-001`
- User Intervention: `🔴 P1 User Decision Required`
- Blocker Source: ...
- Reason: ...
- Unlock Condition: ...
- Allowed Before Unlock: ...
- Do Not Do: ...

## Relevant Files

### Core files to change

- `path` — operation and boundary.

### May be involved

- `path` — trigger condition.

### New files

- `path` — purpose, or explicitly write `TBD — verify actual file path in repo before implementation.`

## Task Packages

<!-- Human prerequisites, prerequisite state, and real integration use the exact scalar enums defined by the validator. Parent tasks must not contain execution prompts, Stop Conditions, or Worker launch information. -->

### [ ] 1.0 Complete an objectively verifiable result

- Task Type: `Formal Task Package`
- Status: `⬜ Pending`
- Acceptance: `AI verification`
- Human Prerequisite: `None`
- Prerequisite Status: `Not required`
- Real Integration: `Not required`
- Source: `FR-001`
- Goal: ...
- Boundary / Non-goals: ...
- Dependencies: `None`
- Subtasks:
  - 1.1 ...
  - 1.2 ...
- Files:
  - `path` — ...
- AI Verification: `T-001`, `T-002`

### [ ] 2.0 Complete a result that needs a human prerequisite but can still be objectively verified by AI

- Task Type: `Formal Task Package`
- Status: `⬜ Pending`
- Acceptance: `AI verification`
- Human Prerequisite: `Required`
- Prerequisite Status: `Pending`
- User Intervention: `🔴 P1 User Action Required`
- User Steps:
  1. Open the confirmed provider test-mode configuration entry.
  2. Complete the required authorization or configuration using the names in this task. Do not record secret values in the document.
  3. Confirm that the test environment can use the configuration.
- Timing: `when execution reaches provider test-mode verification`
- After: AI resumes implementation and verification from the blocked step; the user is not required for this task's acceptance.
- Real Integration: `Pending`
- Source: `FR-002`
- Goal: ...
- Boundary / Non-goals: ordinary account access does not authorize real charges, production release, production deletion, or other irreversible actions.
- Dependencies: `1.0`
- Subtasks:
  - 2.1 ...
- Files:
  - `path` — ...
- AI Verification: `T-003`

### [ ] 3.0 Complete a result that still needs human judgment

- Task Type: `Formal Task Package`
- Status: `⬜ Pending`
- Acceptance: `AI verification then human review`
- Human Prerequisite: `None`
- Prerequisite Status: `Not required`
- Real Integration: `Not required`
- Source: `FR-003`
- Goal: ...
- Boundary / Non-goals: ...
- Dependencies: `None`
- Subtasks:
  - 3.1 ...
- Files:
  - `path` — ...
- AI Verification: `T-004`
- Human Review Gate: `G-01` — before production release

<!-- Collect every parent Human Review Gate reference and define each unique G-* checkpoint exactly once. -->

### [ ] G-01 Human review — before production release

- Covered Tasks: `3.0`
- User Intervention: `🔴 P2 User Decision Required`
- Review Reason: the final experience requires a subjective user judgment that AI verification cannot replace.
- User Checks:
  1. Open the target screen after AI verification has passed.
  2. Complete the confirmed core flow once.
  3. Decide whether the overall experience matches the product goal and record any specific issue that still needs a change.
- Pass Criteria: the experience matches the confirmed goal and no subjective issue still requires a change.
- If Failed: record the concrete issue, reopen `3.0` as 🔵 In progress, fix it, rerun AI verification, then repeat this review.
- After Passing: mark `G-01` as [x], update `3.0` to ✅ Approved and [x], then continue after the status update is committed.

## Verification Plan

| ID | Stage | Scenario | Executor | Page / Entry | Steps or Command | Expected Result | Status |
|---|---|---|---|---|---|---|---|
| `T-001` | `1.0` | Type checking | AI | Repository root | Use the current repository's verified typecheck command, if one exists | Command succeeds with no applicable type errors | Not tested |
| `T-002` | `1.0` | Core user flow | AI | `/path` | Use an existing deterministic repository flow/test when available; otherwise use the project's defined verification method | State is saved and displayed correctly | Not tested |
| `T-003` | `2.0` | Provider test mode | AI | Test environment | After the human prerequisite is provided, exercise the confirmed provider test mode | Valid result is returned with no authentication error | Pending |
| `T-004` | `3.0` | Objective UI states | AI | `/path` | Check the relevant initial, loading, error, success, and responsive states using the project's verification policy | Objective states match the PRD and the page has no unintended horizontal overflow | Not tested |

## Development Rules & Task Management

* Follow the PRD, Scope Freeze, and parent-task boundary. Put out-of-scope findings in Follow-up / Later.
* User-facing copy follows the project's existing language/localization/content system. Do not add i18n merely for task planning, and do not overwrite user-customized copy.
* Reuse existing components and semantic tokens. New components follow the Component Reuse Summary.
* Do not delete existing files, routes, components, or capabilities unless the PRD or parent task explicitly requires it, and do not replace working behavior with placeholders.
* Secrets belong only in server-side or deployment-platform secret storage, never in code, Markdown, logs, or screenshots.
* Keep `Real Integration` as `Pending` until the real provider/external dependency has actually been verified.
* If final review invalidates an approved result, reopen the affected `✅ Approved` task as `🔵 In progress`, reset any invalidated `G-*` gate, and rerun only the affected verification.
* `docs/project/task-prompt.md` is a derived execution entry point. If it conflicts with this file, regenerate it from this canonical task state.
