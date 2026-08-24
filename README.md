# AI Product Workflow Skills

A skill-first workflow for turning confirmed product requirements into implementation-ready plans with Codex.

This repository packages the workflow as two reusable Skills. The workflow rules, templates, references, and validators now live inside each Skill instead of standalone files under `docs/`.

## Included Skills

| Skill | Purpose | Target-project output |
| --- | --- | --- |
| `$create-prd` | Create, update, or audit the canonical product requirements document from confirmed requirements and repository facts | `docs/project/PRD.md` |
| `$generate-tasks` | Convert the PRD into traceable implementation tasks and a user-facing execution prompt | `docs/project/tasks.md` and `docs/project/task-prompt.md` |

The output files remain project documentation. Only the reusable workflow instructions have moved from Markdown playbooks to Skills.

## Workflow

```text
Confirmed requirements and repository facts
                    ↓
               $create-prd
                    ↓
         docs/project/PRD.md
                    ↓
             $generate-tasks
                    ↓
 docs/project/tasks.md + task-prompt.md
                    ↓
          Ready for implementation
```

## Repository Structure

```text
.
├── create-prd/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   └── scripts/
├── generate-tasks/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── AGENTS.md
├── LICENSE
└── README.md
```

Each Skill follows the standard structure: `SKILL.md` contains its metadata and workflow instructions, while optional folders provide supporting templates, references, validation scripts, tests, and UI metadata.

## Use in Codex

Make the Skill directories available in a Codex-supported Skill location, then invoke them explicitly in the target project:

```text
$create-prd Create or update the PRD from the confirmed requirements and current repository facts.
```

After the PRD is confirmed:

```text
$generate-tasks Generate or update the implementation tasks from the current PRD.
```

Codex can discover repository Skills under `.agents/skills` and personal Skills under `$HOME/.agents/skills`. You can also install a Skill from a repository with `$skill-installer`. See the [official OpenAI Skill documentation](https://developers.openai.com/codex/skills) for current installation and discovery options.

## Core Principles

* Confirm product scope before planning implementation.
* Keep current scope separate from baseline behavior and future ideas.
* Trace implementation tasks back to stable PRD requirement IDs.
* Verify the current repository before proposing infrastructure or commands.
* Treat design output as a reference, not the source of product requirements.
* Define verification before implementation begins.
* Do not assume Auth, Payment, Database, Storage, API, or history features are enabled merely because a template contains them.

## License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.
