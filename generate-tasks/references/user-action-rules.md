# User action, decision, and approval rules

Read this file only when a planned task requires user involvement outside ordinary implementation.

## Distinguish three concepts

### Human prerequisite

Use when the executor can still complete and objectively verify the task, but the user must first provide an execution condition.

Typical examples:

- account login
- CAPTCHA, verification code, or 2FA
- terminal/browser/tool permission
- enabling an API or integration
- configuring a named secret/environment variable
- providing a test account, test data, or test environment
- completing one-time account/platform setup

Use the existing parent fields and enums from the template/validator. A prerequisite does not change the task's acceptance method by itself.

### User Decision

Use when the user must choose between materially different product, business, provider, architecture, or implementation directions and the answer cannot be safely inferred from the PRD.

If the decision changes product scope or business rules, the PRD must be updated first. Do not hide it as a prerequisite.

A decision that blocks multiple tasks should have one canonical Confirmation/Blocked Task rather than being duplicated in each parent.

### User Approval

Use when the action is destructive, high-impact, irreversible, hard to roll back, production-sensitive, or otherwise requires explicit consent.

General account access does not imply approval for real charges, production deletion, production release, or other irreversible actions.

## Human review after AI verification

If a final decision or approval is required only after all objective work is complete, model it through the applicable `G-*` human-review gate under `verification-rules.md`, not as an execution prerequisite.

Do not represent the same Action/Decision/Approval simultaneously as a parent prerequisite, Blocked Task, `G-*`, and task-prompt explanation. Keep one canonical source and reference it where needed.

## Request timing

Request user involvement only when it is actually needed.

Before asking the user:

- verify that the action is still required
- complete any safe work that does not depend on it
- state the exact unlock condition
- do not ask for information already available in the repository or current task context

Never ask the user to paste secrets into task documents or chat when a platform secret store or secure local configuration is the correct channel.

## User Action Guides

Reusable platform instructions may live under:

`references/user-actions/<name>.md`

After task generation/update, inventory only the User Actions/Decisions/Approvals introduced or changed in this run:

- `Not needed`: a short instruction in `tasks.md` is sufficient
- `Available`: an accurate reusable guide already exists; reference it instead of duplicating generic platform steps
- `Missing`: a reusable guide would help but does not exist

Do not invent a guide path.

If a guide is Missing, keep enough project-specific steps in `tasks.md` for the task to remain understandable, then ask once after validation whether the user wants a reusable central guide created. Do not create or update a central guide without explicit approval.

Central guides contain only stable cross-project platform procedures. Project-specific names, domains, environment-variable names, task IDs, and current state stay in `tasks.md`.

Do not prewrite steps that depend on future implementation details that do not exist yet.

## Priority and safety

Use the existing `🔴 P1/P2/P3` labels required by the template/validator. Choose priority based on actual blocking/risk impact rather than mechanically assigning P1 to every user action.

Never place real API keys, passwords, tokens, database URLs, verification codes, private keys, OAuth secrets, webhook secrets, or test-account credentials in `tasks.md`, `task-prompt.md`, or reusable guides.
