---
name: generate-tasks
description: Generate, update, or audit canonical docs/project/tasks.md and its derived docs/project/task-prompt.md from a validated PRD. Use for implementation task planning and execution sequencing; do not implement product changes.
---

# Generate Tasks

Turn the validated `docs/project/PRD.md` into canonical implementation tasks and a derived execution-prompt view without implementing the work.

## Boundary

This Skill owns task planning only.

When generating or updating, modify only:

- `docs/project/tasks.md`
- `docs/project/task-prompt.md`

Do not modify the PRD, business code, tests, migrations, dependencies, configuration, deployment, production resources, or provider state. Do not commit during task generation.

If the user requests review/audit only, remain read-only unless they explicitly request fixes.

When invoked by `$create-prd`, use only the already validated PRD version and do not reopen or expand product scope.

## Workflow

1. Follow the applicable `AGENTS.md` and the user's current request.
2. Read `docs/project/PRD.md` completely. Treat its Current Scope, business rules, stable IDs, Non-Goals, and blockers as authoritative.
3. If `docs/project/tasks.md` already exists, read it and `docs/project/task-prompt.md`; default to an incremental update unless the user explicitly requests a rebuild.
4. Read `references/core-rules.md`.
5. Inspect only repository code, config, tests, scripts, and project references needed to verify implementation facts for the PRD scope.
6. Read `references/planning-rules.md`; build the parent-task dependency graph, critical path, conflict snapshot, and recommended execution order.
7. Read `references/verification-rules.md`; define focused AI verification, any required human review, and real-integration status. Follow applicable project UI/E2E policy rather than automatically planning browser or E2E testing.
8. If any task needs user action, decision, approval, login, secret/config setup, test access, or another human prerequisite, read `references/user-action-rules.md`.
9. Decide Single-Agent vs Multi-Agent only after the dependency/conflict analysis. If Multi-Agent has clear net benefit, read `references/multi-agent-execution-rules.md` completely; otherwise do not load or emit Multi-Agent details.
10. Read `assets/tasks-template.md` and `assets/task-prompt-template.md`. Build canonical `tasks.md` first, then derive `task-prompt.md` from the final task state and planning analysis.
11. Run:

    ```bash
    python3 <skill-directory>/scripts/validate_tasks.py docs/project/tasks.md docs/project/task-prompt.md
    python3 <skill-directory>/scripts/validate_task_conflicts.py docs/project/task-prompt.md
    ```

12. Fix all structural/conflict errors and review warnings that indicate real defects.
13. Perform the semantic review the validators cannot do: PRD coverage, scope fidelity, real paths/commands, sensible task boundaries, dependency/critical-path correctness, conflict meaning, verification appropriateness, and user-facing Prompt explanations.
14. If User Actions were introduced or changed, apply `references/user-action-rules.md` and report whether reusable guides are Available, Missing, or Not needed. Do not create a missing central guide without explicit user approval.

## Planning principles

- `tasks.md` is the only canonical task contract.
- `task-prompt.md` is a derived execution snapshot and must not redefine task scope or acceptance.
- Repository facts constrain implementation; they do not create requirements.
- Every runnable Formal/Confirmation parent traces to real stable PRD ID(s).
- Task IDs are stable references, not execution order.
- Dependency and conflict are different concepts.
- Prefer the fewest coherent parent tasks that produce independently verifiable results.
- Keep blockers local and preserve runnable unrelated work.
- Existing valid task history is preserved during incremental updates.
- Do not automatically add UI unit tests, agent-driven browser verification, screenshots, or E2E. Follow the project's validation policy; when E2E is explicitly required, prefer deterministic repository scripts such as Node.js + Playwright.

## Conditional project references

Read project playbooks/modules/design references only when the PRD or applicable `AGENTS.md` makes them relevant to the planned work.

Their existence may constrain reuse or implementation, but never makes a capability Current Scope.

Verify a reference path exists before relying on it. If no reliable path can be confirmed, record an honest TBD rather than inventing one.

## Output contract

The exact structures, fields, enums, tables, Prompt shape, and mechanical consistency rules are owned by:

- `assets/tasks-template.md`
- `assets/task-prompt-template.md`
- `scripts/validate_tasks.py`
- `scripts/validate_task_conflicts.py`

Use those sources instead of restating their full mechanical contract in this router.

## Finish

Report briefly:

- what changed in `tasks.md` / `task-prompt.md`
- meaningful blockers or planning decisions
- `Structural validator: PASSED/FAILED`
- `Task conflict validator: PASSED/FAILED`
- `PRD semantic review: PASSED/FAILED`
- `Prompt sequence review: PASSED/FAILED`
- `User Actions: NONE` or the relevant `Available/Missing/Not needed` items

Do not claim implementation, deployment, provider changes, E2E execution, or commits occurred when they did not.
