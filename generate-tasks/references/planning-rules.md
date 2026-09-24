# Planning, dependency, conflict, and ordering rules

Read this file when generating or updating runnable task plans.

## Split by independently verifiable outcomes

Create the fewest parent packages that produce coherent, independently acceptable results. Four to eight parent packages is a common shape, not a target.

Each runnable parent should have:

- one clear result
- stable PRD source IDs
- an explicit boundary / non-goals
- direct dependencies only
- real affected files or an honest TBD
- focused verification references
- the correct acceptance method
- any human prerequisite or real-integration state

Do not create separate parent tasks for subtasks that must be implemented and verified together. Do not hide Confirmation or Blocked work inside implementation subtasks.

## Dependency graph

A dependency exists only when one task needs an output, decision, contract, migration, configuration, or state produced by another task.

Task number, document order, phase label, or working in the same feature area does not itself create a dependency.

Build the direct dependency graph before choosing execution order. Keep local blockers local; do not serialize unrelated work.

`tasks.md` stores the canonical direct dependencies. `task-prompt.md` derives its current execution sequence from those dependencies and current task states.

## Critical path and recommended order

Task IDs are stable references, not sequence numbers.

For unfinished parents:

1. Exclude `✅ Approved` tasks unless they have been explicitly reopened.
2. Respect all unfinished direct dependencies.
3. Prefer runnable tasks that unblock the critical path or multiple downstream tasks.
4. Then consider expected duration, risk, integration cost, and conflict surface.
5. Put Confirmation Tasks, Blocked Tasks, human prerequisites, and external dependencies immediately before the work they actually block.
6. Never assume a user action, credential, provider state, or external blocker is already resolved.

If every unfinished parent is blocked, order them by expected unlock value and make the first blocker explicit rather than pretending a task is runnable.

## Conflict analysis

Conflict is a scheduling constraint, not another name for dependency.

Mark two unfinished parent tasks as conflicting when concurrent implementation would create a meaningful risk of incompatible writes, stale contracts, or unsafe integration. Strong signals include:

- direct overlap in files both tasks are expected to modify
- schema, migrations, seeds, or fixtures
- auth, authorization, ownership, or session contracts
- payment, credits, webhook, entitlement, or billing state
- package/dependency and lockfile changes
- shared config, env, or deployment files
- shared types, interfaces, API contracts, registries, or generated clients
- routes, layouts, navigation, middleware, or global styles
- shared localization/content namespaces or messages
- shared core modules or cross-cutting utilities

Being in the same directory is not enough.

The `Conflicts` snapshot in `task-prompt.md`:

- contains only current unfinished parent Task IDs
- never contains the task itself
- never contains completed tasks
- is symmetric: if A conflicts with B, B must list A
- does not automatically repeat dependencies as conflicts

Run `scripts/validate_task_conflicts.py` after generation/update.

## Single-Agent vs Multi-Agent

Default to the simpler execution model unless parallel work has a clear time-to-correct-completion benefit.

Consider:

- runnable independent tasks
- critical-path benefit
- file/contract conflict surface
- branch/worktree startup and coordination cost
- review, merge, and integration cost
- machine/browser/build/test resource contention
- stale-context and rework risk

Do not use Multi-Agent merely because multiple tasks exist, and do not split coherent work just to create parallel workers.

If Multi-Agent has clear net benefit, read `multi-agent-execution-rules.md` completely and follow it. Otherwise keep a normal linear `task-prompt.md` sequence and do not emit Worker/batch/branch placeholders.

Generating a Multi-Agent plan does not itself launch Workers, Subagents, branches, worktrees, merges, or commits.

## `task-prompt.md` derivation

The exact structure comes from `assets/task-prompt-template.md` and the validator. Semantically:

- the title uses the confirmed user-facing project name; if absent, use a verified primary domain; do not guess from package or directory names
- `## Completed` contains only Approved parent IDs in real completion order
- `## Unfinished` contains every unfinished parent in the same order as the Task sections
- mark the current critical-path item(s) with the required `❗` notation from the template/validator
- each unfinished Task shows concise dependency and current conflict IDs
- each Task explanation uses concrete product language and explains `Now`, `This task`, and `After`
- explanations must not expose internal task/test/gate IDs, file paths, or vague engineering filler to the user
- each Single-Agent execution Prompt should stay short and point back to the canonical parent rather than restating its full contract

For Single-Agent execution, one session handles one runnable parent at a time. When the user actually sends a Task Prompt or replies with the project's defined start signal, that authorizes the commit instruction contained in that Prompt; task generation itself does not authorize a commit.

After a task state changes, regenerate the derived completed/unfinished summaries, critical-path markers, dependency/conflict snapshot, and recommended order.
