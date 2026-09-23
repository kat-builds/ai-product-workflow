# Create PRD — Core Rules

Use these rules for every `$create-prd` run.

## Output boundary

- The canonical output is `docs/project/PRD.md`.
- The PRD defines product requirements, scope, user-visible behavior, flows, constraints, copy, risks, and acceptance outcomes.
- Do not put implementation steps, task packages, commands, migrations, deployment instructions, commits, or business-code changes into the PRD.
- Before a valid Task handoff, repository inspection is read-only except for `docs/project/PRD.md`.
- Default to an incremental update when a PRD already exists. Preserve still-valid requirement IDs, decisions, and user-customized copy unless the user explicitly requests a rebuild or replacement.
- Write the PRD as UTF-8 without BOM.

## Product decision authority

Use this order for product decisions:

1. latest explicit user decision
2. confirmed upstream requirement that has not been overridden
3. existing PRD decision still in force
4. verified repository fact
5. design, playbook, module, template, or other reference material

`AGENTS.md` and project playbooks are process constraints, not product-scope sources.

A repository capability, route, provider, dependency, template feature, design, or reference document may prove an `Existing Baseline`, feasibility constraint, or reuse option. Its existence never makes it `Current Scope` by itself.

## Scope classification

Classify each important item once:

- `Current Scope` — explicitly being implemented or changed now
- `Existing Baseline` — already exists and is reused, preserved, hidden, redirected, noindexed, or intentionally untouched
- `Confirmed Next Phase` — explicitly committed for a later phase
- `Possible Later` — possible future work, not committed
- `Non-Goals` — explicitly excluded from the current work

Record superseded upstream requirements under `Explicitly Overridden`.

Do not promote `Existing Baseline`, `Confirmed Next Phase`, `Possible Later`, template capabilities, Coming Soon UI, or installed providers into `Current Scope` without a current requirement.

`Possible Later` never activates current infrastructure. `Confirmed Next Phase` may justify a future-impact note but does not create a current requirement or current infrastructure decision.

## Stable requirements

- Every `Current Scope` item that implementation or verification must trace needs a stable ID.
- Preserve IDs across incremental PRD updates when the requirement is still the same.
- Never reuse a retired ID for unrelated behavior.
- Describe observable product behavior and acceptance outcomes rather than implementation instructions.
- Infrastructure decisions marked `Reuse`, `Configure`, or `Extend` must cite the relevant `Current Scope` ID. Otherwise state `No Current Scope trigger` and use `Defer`, `Not required`, or `Blocked` as appropriate.

## Repository inspection

Inspect only what is needed to verify the requested scope, current behavior, terminology, routes, configuration shape, and reusable capabilities.

Do not bulk-load unrelated project references and then infer scope from whatever exists in the repository.

Check a path exists before citing it. If a reference document is missing, use verified repository facts instead. Missing documentation is a blocker only when the missing fact itself prevents a reliable product decision.

## PRD content discipline

- Default PRD language is Chinese unless project instructions say otherwise.
- User-facing site copy remains in the product's configured language and i18n system.
- Preserve user-customized labels, placeholders, pricing copy, and UI copy unless the requested requirement changes them.
- Include environment-variable names and purposes only; never include secret values, credentials, tokens, private URLs, or connection strings.
- Use `assets/prd-template.md` as the structural template and remove instructions, examples, placeholders, and untriggered conditional subsections from the finished PRD.
- Do not keep fake or speculative IDs merely to fill a template section.

## Validation

Run:

`python3 <skill-directory>/scripts/validate_prd.py docs/project/PRD.md`

Fix validation errors. Review warnings and fix those that reflect real defects.

Then review the final diff for:

- scope fidelity
- stable-ID preservation
- source fidelity
- contradictions
- accidental secrets
- output-boundary violations

The validator is the source of truth for mechanical document checks already encoded in the script; do not duplicate those checks as prose rules unless a model judgment is still required.
