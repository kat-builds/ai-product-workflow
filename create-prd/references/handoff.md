# Create PRD — Task Handoff

Read this file only after `docs/project/PRD.md` has been updated and validated successfully.

## Purpose

`docs/project/PRD.md` defines product requirements. `docs/project/tasks.md` and `docs/project/task-prompt.md` are derived execution plans and must not redefine the PRD.

After PRD validation, decide whether `$generate-tasks` can safely synchronize the Task documents in the same turn.

## Continue to `$generate-tasks` when

Same-turn Task synchronization is appropriate when all of the following are true:

- the applicable requirements are clear and stable
- no product decision still requires user confirmation
- the affected implementation surface can be determined reliably
- the change is sufficiently bounded to derive implementation tasks without guessing
- the PRD itself does not require manual review before planning

A local correction, clarification, or bounded extension of already-understood requirements can normally continue when these conditions are satisfied.

Do not use requirement count as a hard threshold. Judge requirement readiness, change impact, dependencies, and unresolved decisions.

## Stop before Task synchronization when

Stop after the validated PRD if any of these apply:

- unresolved product decisions remain
- requirements conflict or are still unstable
- the change spans interconnected flows whose task boundaries cannot yet be determined reliably
- a major architecture, core data model, plan, entitlement, or permission boundary is being redesigned
- the PRD explicitly needs human review before planning
- the correct implementation requirements still depend on speculation or missing facts

Report the blocker plainly; do not manufacture Tasks to make the workflow look complete.

## Handoff boundary

If the handoff is allowed:

1. Load and follow `$generate-tasks`.
2. Let that Skill own Task format, dependency/conflict analysis, validation, and Task document updates.
3. Do not copy `$generate-tasks` rules into this Skill.
4. Do not implement product code, tests, migrations, configuration, dependencies, deployment, or production changes as part of the PRD handoff.

A valid handoff may update only the Task documents allowed by `$generate-tasks`, in addition to the already validated PRD.

If the handoff is not allowed, stop after reporting the validated PRD and the reason Task synchronization must wait.
