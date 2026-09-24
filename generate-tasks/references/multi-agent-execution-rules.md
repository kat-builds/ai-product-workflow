# Multi-Agent Execution Rules

Updated: 2026-08-21

> Goal: reduce time-to-correct-completion without sacrificing correctness or increasing avoidable coordination risk. This file defines how `docs/project/task-prompt.md` may represent parallel batches, a Main Manager, Worker prompts, and handoff. Canonical `docs/project/tasks.md` always defines the task contract and must not store runtime scheduling details.

## Contents

1. Scope and enablement
2. Dependencies, critical path, and batches
3. Conflict surface analysis
4. Main Manager and Worker isolation
5. `task-prompt.md` structure
6. Worker prompt contract
7. Reasoning level and resources
8. Ownership, merge, and stale context
9. User involvement
10. Self-check

## 0. Terms and document boundaries

- **Worker**: an independent coding-agent worker/session started from `task-prompt.md`. Each Worker uses one unique non-`main` branch and, when supported or needed, an isolated worktree or equivalent workspace. A Worker handles one parent Task Package at a time.
- **Main Manager**: the only Integration Owner. It owns `main`, review, merge decisions, integration validation, canonical task status, and subsequent scheduling.
- **Subagent**: an agent created and managed inside one parent-agent session. It is not the same as an independent Worker and the two concepts must not be mixed.

Document roles:

- `tasks.md`: canonical task source of truth. It must not contain an Execution Plan, Worker assignment, branch/worktree metadata, launch/handoff prompts, or Stop Conditions.
- `task-prompt.md`: current execution snapshot. It may contain batches, a Main Manager kickoff prompt, Worker metadata, and copyable prompts for unfinished tasks. It must not redefine the task contract.

Generating a Multi-Agent plan does not itself start Workers/Subagents, create branches/worktrees, merge, or commit.

## 1. Scope and enablement

Decide whether Multi-Agent execution is worthwhile only after parent-task boundaries, the direct dependency graph, and conflict surfaces are known. Optimize for faster correct completion, not for the largest Worker count.

Consider:

- runnable independent tasks;
- critical-path benefit and expected duration;
- file/module/interface/schema/business-semantic conflict surface;
- session startup, context loading, branch/worktree, coordination, review, merge, and integration cost;
- CPU, RAM, disk/I/O, browser, build, test, typecheck, dev-server, and other shared-resource contention;
- stale-context and rework risk.

Generate Main Manager / Worker / batch content only when the expected parallel time benefit clearly exceeds these costs and the write boundaries can be isolated safely. Otherwise use the normal Single-Agent linear task sequence and do not emit empty Worker or batch scaffolding.

## 2. Dependencies, critical path, and batches

A Task may enter a batch only when:

1. its direct dependencies are `✅ Approved`, or the Main Manager has verified from repository evidence that the required contract is already locked;
2. no unresolved product decision, human prerequisite, or external blocker prevents the work;
3. its write boundary can be isolated safely from other tasks in the same batch;
4. shared resources are sufficient and concurrency is unlikely to make total time worse;
5. the expected time saving exceeds startup, coordination, merge, and validation cost.

Scheduling priority:

1. unblock real prerequisites first;
2. keep the critical path moving;
3. start safe independent work in parallel only when there is clear benefit;
4. when otherwise equal, prefer work that is longer or unlocks more downstream tasks;
5. keep local blockers local.

Task ID is not execution order. Tasks in the same batch may be displayed in a stable order, but display order must not be described as a dependency.

Do not split a coherent parent merely to create more Workers. Waiting/Blocked tasks keep their own `## Task X.X` section at the expected unlock position, but the prompt must state the unlock condition and must not imply that the task is runnable now.

## 3. Conflict Surface Analysis

Check each planned task for overlap in:

- database schema, migrations, seeds, and fixtures;
- auth, authorization, ownership, and session contracts;
- payment, credits, webhook, entitlement, and billing state;
- package/dependency and lockfile changes;
- shared config, environment, and deployment files;
- shared types, interfaces, API contracts, registries, and generated clients;
- routes, layouts, navigation, middleware, and global styles;
- design tokens and shared UI primitives;
- localization/content namespaces and shared messages;
- shared core modules, central registries, and cross-cutting utilities;
- any actual file expected to be edited by more than one task.

Give every high-conflict surface one owner. Other Workers must treat it as read-only/prohibited and use a clear coordination point. If boundaries cannot be isolated reliably, reduce concurrency, assign the work to one Worker, or serialize it. Separate worktrees do not solve semantic, interface, or integration conflicts by themselves.

## 4. Main Manager and Worker isolation

### 4.1 Main Manager

The unique Main Manager / Integration Owner:

- maintains the dependency graph and critical path;
- decides Worker scheduling from real repository/Git state;
- owns `main`, merge timing/order, and cross-task conflict resolution;
- reviews Worker diffs, boundaries, and validation evidence;
- runs necessary integration/final validation;
- after merge, updates canonical `tasks.md` state and regenerates `task-prompt.md`.

The Main Manager should focus on integration rather than taking ordinary implementation work that can safely remain with a Worker.

### 4.2 Worker

Each Worker:

- uses a unique non-`main` branch from the latest confirmed `main`; use an isolated worktree or equivalent workspace when supported or required;
- handles only its assigned Task Package and allowed files/modules;
- does not operate on, switch to, modify, merge, or push `main`;
- does not integrate another Worker branch;
- does not modify `docs/project/tasks.md` or `docs/project/task-prompt.md`;
- stops and reports to the Main Manager if a dependency assumption fails, a boundary must be crossed, or a shared contract conflicts;
- creates its own task-scoped commit and complete Completion Report, but does not merge.

## 5. `task-prompt.md` structure

Document order:

1. H1 with the confirmed project name or domain plus the document-role note;
2. `## Completed` when Approved parents exist, in real completion order;
3. `## Unfinished` when unfinished parents exist, matching the Task section order and marking current critical-path tasks with `❗`;
4. one complete Main Manager Kickoff `text` prompt;
5. every unfinished `## Task X.X — <title>` section in batch order.

Do not output `Next task`, `Execution mode`, rationale text, or top-level usage instructions. When no unfinished parents remain, omit the kickoff and all Task sections.

A Task may include short scheduling metadata before its plain-language explanation:

```md
- Dependencies: None
Execution batch: `Batch 1` — may run in parallel with Task 3.0
Worker: `Worker A`
Branch: `task/1-0-...`
Allowed Files / Modules: `path/a`, `path/b`
Focused Validation: `T-001`
```

Add `Do Not Touch` only for a real high-conflict exception. Do not repeat the default reasoning level. This metadata is a current scheduling snapshot and must not be copied into `tasks.md`.

The Main Manager Kickoff Prompt must require the manager to:

- read canonical `tasks.md` and derived `task-prompt.md`;
- verify `main`, working tree, dependencies, resources, batches, branches, and boundaries from actual repository/Git state rather than trusting planning text as fact;
- report which independent Worker sessions/workspaces should be started now, without creating Workers, branches, worktrees, or beginning implementation;
- later review/merge using branch, commit, diff, logs, and validation evidence;
- after merge, update `tasks.md` and regenerate `task-prompt.md` before returning the next runnable prompts.

## 6. Worker prompt contract

Every unfinished parent keeps this shape:

````md
## Task X.X — <title>

- Dependencies: None, or only Task / blocker IDs

- Now: <real user-facing problem>
- This task: <what this task changes>
- After: <visible result>

**Prompt for coding agent**

```text
<complete Worker prompt>
```
````

In addition to the normal parent-task contract, a Worker prompt must include:

- Worker, Task Package, branch, direct dependencies, allowed files/modules, and focused validation;
- `Do Not Touch` only when needed;
- reasoning level only when the execution environment supports it and this task needs a non-default level;
- confirmation of the isolated branch/workspace and instructions to read applicable project/agent instructions, the canonical parent task, and only the necessary PRD context;
- instruction to verify already-correct implementation rather than rewriting it;
- instruction to handle only the assigned Task, avoid `main`, and leave both task documents untouched;
- instruction to stop and report to the Main Manager if the boundary or dependency assumption becomes invalid;
- instruction to create a repository-compliant commit whose subject begins with the Task ID, without merging;
- a Completion Report containing Worker, Task, branch, commit hash, changed files/diff, dependency assumptions, boundary, validation commands/results, risks/blockers, and recommended canonical status.

A Worker never synchronizes `task-prompt.md`; the Main Manager does that after merge.

For a Waiting/Blocked task, the prompt must check the unlock condition first. If it is still unresolved, report the blocker without creating a branch, implementing, or committing.

## 7. Reasoning level and resources

Record a reasoning/effort level only when the execution environment actually supports one.

- Main Manager: prefer `High`.
- Worker default: `Medium`.
- `Low`: mechanical, low-risk, tightly bounded, easy-to-verify work only.
- `High`: complex or high-risk work, critical-path work, cross-module changes, auth, payment, migration, debugging, or integration.
- When uncertain, use `Medium`. Do not name a specific model.

Workers run focused validation. The Main Manager rate-limits full builds, full suites, Playwright/browser/E2E work, and large integration tests so Workers do not fight over browser, port, CPU, memory, or other shared resources.

## 8. Ownership, merge, and stale context

Once a Worker has materially started a Task, keep that Task with the same Worker unless it is blocked, failing to converge, based on an invalid assumption, made stale by a newer `main`, or clearly cheaper to replan than continue.

Before merging, the Main Manager must:

1. review the diff, commit, and changed files;
2. verify Task boundary, allowed files, Do Not Touch, and dependency assumptions;
3. review validation evidence;
4. add targeted review/validation when risk requires it;
5. choose merge timing/order from in-flight branches, shared files, dependencies, and critical path;
6. run appropriate integration validation after merge, then update both task documents.

Do not mechanically require every branch to rebase, and do not merge merely because a Worker finished.

## 9. User involvement

- Parent prerequisites, `G-*` gates, Confirmation Tasks, Blocked Tasks, and User Action Guides remain canonical in `tasks.md`.
- `task-prompt.md` only explains how a blocker affects execution order; it does not duplicate the full user-action procedure.
- `P1` blocks the current or near-term critical path, `P2` is required later, and `P3` does not block the main path.
- Never record a real secret, credential, or verification code.

## 10. Self-Check

1. Parallelism has a real dependency/conflict/resource basis; no Task was split merely to increase Worker count.
2. Every batch contains only runnable or explicitly contract-locked work; Waiting/Blocked tasks have real unlock conditions.
3. There is one Main Manager, one merge gate, and clear branch/workspace/file ownership.
4. `tasks.md` contains no Execution Plan, Worker metadata, Prompt, or Stop Condition.
5. `task-prompt.md` project name/domain, completion order, unfinished summary, critical-path markers, batches, parent tasks, and dependencies match canonical state.
6. Every Task keeps short dependency metadata, a concrete plain-language explanation, and one copyable prompt without duplicating the full PRD/Task Package.
7. Every Worker prompt names one Task/branch, boundary, focused validation, `main` prohibition, commit requirement, and Completion Report; Workers do not modify the task documents.
8. The Main Manager kickoff is complete and copyable and makes clear that the user or supported execution environment starts independent Worker sessions; this Skill does not launch Workers/Subagents itself.
9. Reasoning levels and heavy validation respect available resources; no specific model is required.
10. Genuine user blockers are modeled once in `tasks.md`; `task-prompt.md` only references them and never exposes secrets.
