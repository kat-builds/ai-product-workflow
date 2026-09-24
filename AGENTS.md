# Repository Guidelines

## Purpose & Repository Boundaries

This repository packages reusable AI product-workflow Skills. It contains no application code.

Each top-level directory is one Skill:

- `create-prd/` — create, update, or audit a target project's `docs/project/PRD.md`.
- `generate-tasks/` — derive `docs/project/tasks.md` and `docs/project/task-prompt.md` from a validated PRD.
- `ui-design-system/` — initialize, update, preflight, or audit a target project's `docs/project/design/DESIGN_SYSTEM.md`, and optionally install a minimal Design System guardrail into the applicable project/agent instruction file.

A Skill may contain:

- `SKILL.md` — metadata, boundaries, and workflow instructions.
- `agents/` — optional agent metadata or interface configuration.
- `assets/` — canonical templates and reusable snippets.
- `references/` — detailed rules loaded when relevant.
- `locales/` — translated structural labels used by generated documents and validators.
- `scripts/` — standard-library validator scripts.
- `tests/` — validator unit tests where present.

This `AGENTS.md` governs maintenance of this repository only. It must not become a hidden runtime dependency of the published Skills.

If a rule is required for a Skill to work correctly in another project, put the general version of that rule inside the Skill itself (`SKILL.md`, `references/`, `assets/`, or validator logic), not only in this repository-level file.

## Target-Project Independence

Do not assume that a target project uses Next.js, pnpm, npm, Bun, Tailwind, Drizzle, Stripe, Cloudflare, Vercel, i18n, or any other specific stack.

The Skills must derive project-specific facts from the target repository and its applicable project/agent instructions.

Template capabilities do not automatically become product scope. The presence of auth, payment, storage, AI, database, analytics, or other modules in a starter template does not mean the target product uses them.

Do not move maintainer-specific working preferences into the public Skill contract unless they are genuinely required for all users.

## Source Language & Generated Document Language

Skill source documentation is maintained in English:

- `SKILL.md`
- `references/*.md`
- `assets/*.md`
- `agents/*.yaml`

Translated structural labels belong under `locales/`.

Generated project documents are not English-only. They may follow the language requested by the user or defined by the target project.

Keep one validator implementation per document type. Do not create separate language-specific validator scripts or duplicate core validation logic by language.

When changing validator-sensitive headings or fields:

1. update the canonical English structure;
2. update every supported locale mapping;
3. update normalization or validation logic when needed;
4. keep locale key sets aligned;
5. test English plus at least one translated document.

## Build, Test & Validation

This repository has no application build step.

Validation commands:

- `python3 create-prd/scripts/validate_prd.py <path-to-PRD.md>`
- `python3 generate-tasks/scripts/validate_tasks.py <tasks.md> [task-prompt.md]`
- `python3 generate-tasks/scripts/validate_task_conflicts.py <task-prompt.md>`
- `python3 ui-design-system/scripts/validate_design_system.py <path-to-DESIGN_SYSTEM.md>`

Run the `generate-tasks` unit tests from that Skill directory:

```bash
cd generate-tasks
python3 -m unittest discover -s tests
```

After changing a template, locale mapping, or validator:

- exercise the affected validator with a resolved scratch/example document rather than an untouched placeholder template;
- verify the current English structure;
- verify supported translated structure where applicable;
- confirm locale files remain structurally aligned;
- confirm no generated or scratch artifacts were accidentally committed.

There are no application E2E or UI tests in this repository.

## Coding Style & Naming

Keep validator scripts compatible with Python 3.9+ and standard-library only so they can run in target projects without extra dependencies.

Follow the existing naming conventions:

- Skill directories: kebab-case.
- Skill entry file: `SKILL.md`.
- Python scripts/tests: lower_snake_case.
- Locale files: language code such as `en.json`, `zh.json`.

Keep reusable rules generic. Prefer project inspection over hard-coded package managers, frameworks, providers, paths, breakpoints, languages, or agent products.

Preserve user-customized product copy when a Skill is operating on a target project unless the task explicitly requires changing it.

## Syncing Skill Directories

When syncing these Skills from another maintained source, treat only these directories as Skill sync targets:

- `create-prd/`
- `generate-tasks/`
- `ui-design-system/`

Do not overwrite repository-owned files such as `README.md`, `AGENTS.md`, or `LICENSE` as part of a Skill-directory sync unless the current task explicitly requires those files to change.

After syncing:

1. review `git diff`;
2. confirm only intended Skill files changed;
3. run the relevant validators and unit tests;
4. review user-facing README examples separately when the Skill contract changed.

## Git, Commit & Pull Request Workflow

Use a non-`main` working branch for meaningful changes.

Before merging:

1. review the complete diff;
2. run the relevant validation/tests;
3. summarize behavior or contract changes;
4. call out any breaking template or validator changes;
5. obtain explicit user approval to merge.

When approved, prefer a squash merge to `main`, then remove the working branch when practical.

Use Conventional Commit style where it fits:

- new behavior → `feat:`
- bug fix → `fix:`
- documentation-only change → `docs:`
- maintenance/tooling → `chore:`

Commit subjects should be specific enough to serve as a useful project-history index. Avoid vague subjects such as `update`, `fix`, `changes`, or `misc`.

For non-trivial commits, include a short body describing the important behavior change and why it was needed.

PRs should include:

- a short summary;
- validation/test commands and results;
- notes for Skill-contract, template, locale, or validator changes;
- breaking-change notes when applicable.

A commit instruction inside a generated task prompt authorizes the future execution workflow described by that prompt; it does not authorize unrelated commits or merges while maintaining this repository.

## Configuration, Secrets & Encoding

This repository should contain no application secrets or environment-specific credentials.

Never place real secrets, credentials, tokens, connection strings, private keys, or verification codes in Skill examples, templates, tests, PRDs, task documents, or logs.

Write text files as UTF-8 and check multilingual fixtures or locale files for mojibake after editing them.
