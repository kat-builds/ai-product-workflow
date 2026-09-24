# <Project name or domain> — Task Execution Prompts

Last updated: YYYY-MM-DD
Document language: en

> This file is only for copying prompts; canonical task definitions live in `docs/project/tasks.md`.

<!-- Prefer the confirmed user-facing project name. If no project name is confirmed, use the verified primary domain. Replace the placeholder; do not guess from package or directory names. -->

<!-- If Approved parents exist, output Completed plus one line of Task IDs in real completion order, appending newly completed tasks at the end. Omit the section when none exist. -->

## Completed

1.0

<!-- If unfinished parents exist, output Unfinished plus one line of Task IDs in the same order as the Task sections below. Prefix current critical-path IDs with ❗. Omit the section when all parents are complete. -->

## Unfinished

❗2.0, 3.0

<!-- Generate Task sections only for unfinished parents. Order them by recommended real execution sequence, not by Task ID. Single-Agent uses a linear sequence. Multi-Agent may add Execution batch and Worker metadata under the Task title. Conflicts lists only current unfinished parent Task IDs that cannot safely run in parallel and must be symmetric. -->

## Task 2.0 — Complete a result that needs a human prerequisite but can still be objectively verified

- Dependencies: None
- Conflicts: 3.0

- Now: the user cannot yet complete this operation from the page or see a clear result after submitting it.
- This task: the coding agent will connect the input, submission, success result, and failure feedback.
- After: the user can complete the operation; success shows a result, and failure clearly explains what happened.

**Prompt for coding agent**

```text
Execute Task 2.0 in docs/project/tasks.md. Read the complete parent task and inspect the current implementation first. Implement and verify only that task. When finished, update docs/project/tasks.md and docs/project/task-prompt.md, then create a commit whose subject starts with 2.0.
```

## Task 3.0 — Complete a result that still needs user judgment

- Dependencies: 2.0
- Conflicts: 2.0

- Now: the page is not yet connected to the confirmed external service, so the user cannot receive a real result.
- This task: the coding agent will connect that service and identify any login or authorization step only when it is actually needed.
- After: using the page returns a real result from the external service instead of test data.

**Prompt for coding agent**

```text
Execute Task 3.0 in docs/project/tasks.md. Read the complete parent task and inspect the current implementation first. Implement and verify only that task. When finished, update docs/project/tasks.md and docs/project/task-prompt.md, then create a commit whose subject starts with 3.0.
```

<!-- Replace every example above with the current product's real page, user action, problem, and visible result. Use `Conflicts: None` when there is no conflict. If a parent is already Ready for review, assist only with the corresponding G-* review and status closeout instead of reimplementing it. When all parents are complete, omit all Task sections. -->
