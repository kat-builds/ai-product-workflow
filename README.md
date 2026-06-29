# AI Product Workflow

A documentation-first workflow for turning product ideas into implementation-ready engineering tasks with AI assistance.

This repository documents a structured process I use to move from a vague product idea to a clear specification, UI brief, development PRD, implementation task list, and final consistency review.

It is designed for small web tools, content-driven products, AI-assisted utilities, and lightweight SaaS-style experiments.

---

## Why This Exists

AI can help generate product documents and development tasks, but without a clear workflow it often:

* expands scope too early
* invents features that were never requested
* assumes login, dashboard, payment, or database requirements too soon
* creates tasks that do not match the PRD
* copies UI design output without checking product intent
* skips verification and edge cases

This workflow is designed to keep AI-assisted product development grounded, traceable, and implementation-ready.

---

## Workflow

```text
Product Idea
     ↓
Requirement Discovery
     ↓
SPEC / Design Brief
     ↓
UI Exploration
     ↓
UX Interaction Specification
     ↓
Development PRD
     ↓
SEO / Keyword Strategy
     ↓
Implementation Tasks
     ↓
Implementation Review
     ↓
Ready for Development
```

---

## Workflow Stages

| Stage                        | Purpose                                                                      | Output                      |
| ---------------------------- | ---------------------------------------------------------------------------- | --------------------------- |
| Requirement Discovery        | Clarify the idea, user problem, MVP scope, and product direction             | SPEC / Design Brief         |
| UI Exploration               | Use the SPEC to explore layout, structure, and visual hierarchy              | UI draft / design reference |
| UX Interaction Specification | Define tool behavior, states, buttons, errors, and edge cases                | UX PRD                      |
| Development PRD              | Convert the brief and design materials into an implementation-ready PRD      | `docs/PRD.md`               |
| SEO / Keyword Strategy       | Decide whether keywords belong on the homepage, inner pages, or blog content | Keyword strategy            |
| Implementation Tasks         | Break the PRD into executable engineering tasks                              | `docs/tasks.md`             |
| Implementation Review        | Check whether the PRD and tasks are consistent before development            | Review notes                |

---

## Repository Structure

```text
.
├── README.md
├── LICENSE
│
└── docs/
    ├── create-prd.md
    └── generate-task.md
```

### `docs/create-prd.md`

Defines how to generate an implementation-ready PRD from earlier product notes, design references, and confirmed project scope.

It focuses on:

* scope control
* product requirements
* user flow
* UI states
* error handling
* copy requirements
* component reuse
* infrastructure assumptions
* verification criteria

### `docs/generate-task.md`

Defines how to convert a PRD into a structured implementation task list.

It focuses on:

* PRD traceability
* task sequencing
* component reuse
* verification steps
* avoiding invented scripts or APIs
* separating current scope from later work
* preventing unnecessary SaaS complexity

---

## Core Principles

* Documentation comes before implementation.
* AI should clarify ambiguity, not invent product direction.
* Current scope must be separated from future ideas.
* Tasks must be traceable to PRD requirements.
* Existing infrastructure must be verified before new infrastructure is proposed.
* UI design output is a reference, not the source of truth.
* Verification should be defined before development starts.
* Do not add login, dashboard, payment, database, API, or history features unless they are required by the confirmed scope.

---

## Intended Use

This workflow is useful for:

* small web tools
* SEO-driven utility sites
* AI-assisted product experiments
* lightweight SaaS prototypes
* product documentation workflows
* AI-assisted development planning

It is not intended for large enterprise product planning, high-compliance systems, or projects where requirements must be approved through formal product management processes.

---

## Example Use Case

A typical workflow might look like this:

```text
Idea:
Build an online DOCX to Markdown converter.

Step 1:
Clarify the product idea and generate a SPEC / Design Brief.

Step 2:
Use the SPEC to create a UI draft.

Step 3:
Document tool-area interactions, states, and edge cases.

Step 4:
Generate a development-ready PRD.

Step 5:
Generate implementation tasks from the PRD.

Step 6:
Review PRD and tasks for consistency before development.
```

---

## What This Project Demonstrates

This project demonstrates:

* AI-assisted product planning
* technical documentation design
* requirement clarification
* PRD structure
* task breakdown
* scope control
* implementation review
* practical workflow design for solo builders and small product teams

---

## Future Improvements

Possible future improvements include:

* adding complete example projects
* adding SPEC / PRD / tasks samples
* adding workflow diagrams
* adding review checklists
* adding English and Chinese documentation versions
* adding reusable templates for different project types

---

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.
