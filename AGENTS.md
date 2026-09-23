# Repository Guidelines
未经批准，禁止开 Subagent

## Project Structure & Module Organization
This repository packages reusable Skills only; it contains no application code. Each top-level directory is one Skill:

- `create-prd/` — create, update, or audit a target project's `docs/project/PRD.md`.
- `generate-tasks/` — derive `docs/project/tasks.md` and `docs/project/task-prompt.md` from a validated PRD.
- `ui-design-system/` — initialize, update, preflight, or audit a target project's `docs/project/design/DESIGN_SYSTEM.md`, and optionally install the UI-enforcement snippet into that project's `AGENTS.md`.

Each Skill follows the same internal layout: `SKILL.md` (metadata and workflow instructions), plus optional `agents/` (Codex agent interface config), `assets/` (templates), `references/` (detailed rules loaded conditionally), `scripts/` (validators), and `tests/` (validator unit tests, where present).

## Current Architecture Notes
This repo has no runtime, `package.json`, or build pipeline of its own. The Skills here are consumed by a separate target project (for example via Codex Skill discovery under that project's `.agents/skills`), where they read and write that project's own `docs/project/` files. Do not assume this repository uses Next.js, pnpm, Drizzle, Stripe, or any other target-project stack — that context belongs to whichever project imports these Skills, not to this repository.

## Build, Test, and Development Commands
There is no build step. Validation lives inside each Skill:

- `python3 create-prd/scripts/validate_prd.py <path-to-PRD.md>`
- `python3 generate-tasks/scripts/validate_tasks.py <tasks.md> [task-prompt.md]`
- `python3 generate-tasks/scripts/validate_task_conflicts.py <task-prompt.md>`
- `python3 ui-design-system/scripts/validate_design_system.py <path-to-DESIGN_SYSTEM.md>`

`generate-tasks` also ships unit tests. Run them from inside that directory, since the tests import `scripts` as a local package:

```bash
cd generate-tasks && python3 -m pytest tests/
```

## Coding Style & Naming Conventions
Skill content is Markdown (`SKILL.md`, `references/*.md`, `assets/*.md`) plus Python 3.9+-compatible validator scripts. Keep validator scripts standard-library only so they run in any target project without extra installs. Follow the existing naming pattern: kebab-case Skill directory names, `SKILL.md` in all caps, lower-snake-case script and test filenames.

Do not change UI copy, labels, or placeholder text that the user has already customized unless explicitly instructed.

## Testing Guidelines
- Run `python3 -m pytest tests/` from inside `generate-tasks/` after any change to `generate-tasks/scripts/` or its templates.
- Run each Skill's validator script against its own template or asset (or a scratch example file) after changing template structure, to confirm the validator still parses it.
- There are no E2E or UI tests in this repository.

## Commit & Pull Request Guidelines
Use Conventional Commit style.

- New feature → `feat:`
- UI / visual change only → `ui:`
- Bug fix → `fix:`
- Documentation only → `docs:`

Keep commits small and focused. Reference issue IDs in the body when relevant.

Treat every commit message as a future search index for debugging and project history. Write in plain, specific language that explains both what changed and why it changed. A reader should be able to understand the affected behavior without opening the diff.

- Do not use vague subjects such as `update`, `fix`, `changes`, or `misc`.
- Prefer concrete descriptions such as `docs: tighten create-prd blocking-question rules`.
- For non-trivial commits, add a body describing the important behavior changes and the reason for them.
- When the user asks the AI to commit, the AI must compose this descriptive subject and body automatically instead of asking the user to write them.

PRs must include: short summary, testing notes (commands + results), and notes for any Skill-contract or template changes. Highlight breaking changes (for example, changes that alter a canonical template's structure or a validator's pass/fail rules) early.

After each completed task with file changes, provide 1 suggested commit message in a fenced code block (copyable). Do not commit unless explicitly requested.

- When generating or updating implementation tasks or task execution prompts, use `$generate-tasks` and follow its current Skill instructions exactly.
- A commit instruction inside a generated prompt applies to the future execution of that prompt; it does not authorize committing during the current documentation-editing task.
- Do not remove or weaken generated commit instructions merely because the current task does not authorize an immediate commit.

## Configuration & Secrets
This repository holds no application secrets or environment configuration of its own. The Skills instruct target projects to never record real secrets, credentials, tokens, connection strings, or verification codes inside PRD or task documents — see each Skill's `references/core-rules.md` for the enforced rule and each validator's secret-detection checks.

## Global Encoding Rules

- This rule is global for the whole repository, not only changelog files.
- Always write text files with UTF-8 encoding.
- In PowerShell, always specify encoding explicitly when writing files:
  - `Set-Content -Encoding utf8`
  - `Out-File -Encoding utf8`
- Do not run nested shell pipelines that execute another `powershell -Command` block for Chinese/multilingual content generation.
- After writing any Chinese or multilingual content, verify file output:
  - `Get-Content <file> | Select-Object -First 50`
  - Confirm there is no garbled text (`??`, mojibake, broken symbols).

## Question Format Requirements

- Number every question (`1, 2, 3...`).
- Give 2-4 options per question (`A/B/C/D`).
- For each question, include:
  - `Recommended: X`
  - `Reason: <one short sentence>`
- Start with answer instructions:
  - `Reply with letters in order, e.g. ACB = 1A 2C 3B.`
  - If fewer letters are provided, use recommended options for the rest (unless user says otherwise).
- Also accept explicit form: `1A, 2C, 3B`.
