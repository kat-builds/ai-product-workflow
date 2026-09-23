# AI Product Workflow Skills

A skill-first workflow for turning confirmed product requirements into implementation-ready, design-consistent plans with Codex.

This repository packages the workflow as three reusable Skills. The workflow rules, templates, references, and validators live inside each Skill instead of standalone files under `docs/`.

## Included Skills

| Skill | Purpose | Target-project output |
| --- | --- | --- |
| `$create-prd` | Create, update, or audit the canonical product requirements document from confirmed requirements and repository facts | `docs/project/PRD.md` |
| `$generate-tasks` | Convert the PRD into traceable implementation tasks and a user-facing execution prompt | `docs/project/tasks.md` and `docs/project/task-prompt.md` |
| `$ui-design-system` | Initialize, update, preflight, or audit a project's canonical Design System and reusable AI UI guardrails | `docs/project/design/DESIGN_SYSTEM.md` (and, on request, a UI-enforcement snippet in the project's `AGENTS.md`) |

The output files remain project documentation. Only the reusable workflow instructions live as Skills.

## How the Skills relate

`$create-prd` and `$generate-tasks` form the sequential product-to-plan pipeline: confirmed requirements become a validated PRD, and the validated PRD becomes traceable implementation tasks.

`$ui-design-system` is complementary rather than sequential. It owns a separate document — the project's Design System — and can be run independently at any point: to establish UI rules for a new project, to preflight a planned UI task against existing rules before `$generate-tasks` plans it, or to audit implementation drift after the fact. `$create-prd` and `$generate-tasks` treat an existing Design System as reference material that constrains presentation and reuse; they never redefine it, and `$ui-design-system` never redefines product scope or task acceptance criteria.

## Workflow

```text
Confirmed requirements and repository facts
                    ↓
               $create-prd
                    ↓
         docs/project/PRD.md
                    ↓
             $generate-tasks  ←──── $ui-design-system
                    ↓          (Design System constrains UI tasks;
 docs/project/tasks.md +        can also run standalone to
    task-prompt.md               initialize/audit UI rules)
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
├── ui-design-system/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   └── scripts/
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

Independently of that pipeline, initialize or audit the project's UI rules at any time:

```text
$ui-design-system Initialize (or audit) the project's Design System from its current theme, tokens, and shared UI primitives.
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
* Treat a project's Design System as the owner of recurring visual and interaction rules, and the PRD as the owner of product behavior; neither Skill silently overrides the other.

## License

This project is licensed under the Apache License 2.0. See `LICENSE` for details.
