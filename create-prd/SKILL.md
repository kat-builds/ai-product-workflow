---
name: create-prd
description: Create, update, or audit the canonical docs/project/PRD.md. Use when defining or reconciling product requirements and scope; do not implement product changes.
---

# Create PRD

Create or update `docs/project/PRD.md` without starting implementation.

## Boundary

This Skill owns PRD work only.

Before a valid Task handoff, modify only `docs/project/PRD.md`. Do not implement business code, tests, migrations, configuration, dependencies, builds, deployments, production resources, or external provider changes.

A validated PRD may hand off to the `generate-tasks` Skill only when `references/handoff.md` permits it. Let `generate-tasks` own its derived Task documents and rules.

## Workflow

1. Follow the applicable project/agent instructions and the user's current request.
2. Read every input the user explicitly referenced.
3. If `docs/project/PRD.md` exists, read it and default to an incremental update unless the user explicitly requests a rebuild.
4. Read `references/core-rules.md`.
5. Inspect only the repository facts and project documents needed to verify the requested scope.
6. Read the applicable sections of `references/conditional-rules.md` only when the confirmed scope or a genuine unresolved product decision triggers them.
7. Resolve blocking product decisions before drafting; use safe defaults for non-blocking implementation details.
8. Read `assets/prd-template.md` as the canonical English structure. Apply the selected locale rules from the Output language section when assembling the document. Remove instructions, examples, placeholders, and untriggered conditional subsections from the final PRD.
9. Create or update `docs/project/PRD.md` as UTF-8 without BOM.
10. Run `python3 <skill-directory>/scripts/validate_prd.py docs/project/PRD.md` and fix real defects.
11. Review the final diff for scope fidelity, ID stability, source fidelity, contradictions, secrets, and output-boundary compliance.
12. If Task synchronization may be appropriate, read `references/handoff.md`. Continue with the `generate-tasks` Skill only when that handoff rule permits it; otherwise stop after the validated PRD.

## Output language

Skill source documents and canonical assets are written in English.

Choose the generated PRD language in this order:

1. the user's explicit language request
2. applicable project instructions
3. an existing PRD's `Document language` value during incremental updates
4. the current conversation language
5. English as the fallback

Use `locales/<language>.json` when that locale exists so validator-sensitive headings and labels stay consistent. If a requested locale does not exist, keep validator-sensitive structural labels in English and write the narrative content in the requested language.

Do not change an existing PRD's language during an incremental update unless the user or project instructions explicitly require it.

## Source discipline

Product decisions follow this order:

1. latest explicit user decision
2. confirmed upstream requirement
3. existing PRD decision still in force
4. verified repository fact
5. design, template, playbook, module, or other reference material

Repository capabilities and reference documents may constrain implementation or describe an `Existing Baseline`. Their existence does not make them `Current Scope`.

Do not infer new product scope from installed modules, templates, routes, providers, dependencies, or design references.

## Questions

Do not ask merely because a detail is unspecified.

Ask only when an unresolved product decision would materially change scope, core flows, page structure, payment, auth, data, privacy, or provider feasibility. When that occurs, use the blocking-question rules in `references/conditional-rules.md`.

## Finish

Report:

- what changed in the PRD
- important scope decisions or blockers
- validation result
- whether Task synchronization ran or was intentionally deferred

Do not claim implementation, deployment, or commits occurred when they did not.
