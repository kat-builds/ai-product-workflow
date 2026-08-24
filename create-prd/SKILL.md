---
name: create-prd
description: Create, update, or audit the canonical docs/project/PRD.md from confirmed user requirements, applicable project instructions, upstream specifications, design inputs, and verified repository facts. Use when Codex needs to define or reconcile product scope, preserve stable requirement IDs, separate Current Scope from baseline and future work, or validate an existing PRD before task generation. This skill writes only docs/project/PRD.md, never generates tasks or implementation changes, and never commits.
---

# Create PRD

Create or update the canonical `docs/project/PRD.md` without starting implementation.

## Enforce the output boundary

- Write only `docs/project/PRD.md`.
- Treat every repository inspection and validation step as read-only except for that one file.
- Do not create or update `docs/project/tasks.md`, task prompts, business code, tests, migrations, configuration, dependencies, or any other file.
- Do not run builds, migrations, deployments, external provider calls, or task-generation workflows.
- Do not stage or commit changes.
- If a request combines PRD work with implementation or asks for another output path, complete only the PRD portion at the canonical path and report the out-of-scope portion instead of performing it.

## Follow the required workflow

1. Read every applicable `AGENTS.md` before other project files.
2. Read the user's latest request and every explicitly referenced input.
3. Read an existing `docs/project/PRD.md` completely. Default to an incremental update and preserve applicable IDs, decisions, and customized copy unless the user explicitly requests a rebuild.
4. Read the canonical [references/prd-generation-rules.md](references/prd-generation-rules.md) completely. It is the sole shared PRD-authoring rule source.
5. Discover relevant project-specific documents by filename before opening them. Follow the conditional routing rules below; do not search for duplicate repository PRD-authoring playbooks or bulk-load unrelated references.
6. Scan only repository areas needed to verify the requested scope, current behavior, terminology, routes, configuration shape, and reusable capabilities.
7. Resolve scope classifications and any blocking P0 decisions before drafting.
8. Read [assets/prd-template.md](assets/prd-template.md) when assembling the final document. Remove all instructions, examples, placeholders, and untriggered conditional subsections from the result.
9. Create or update only `docs/project/PRD.md` as UTF-8 without BOM.
10. Run `python3 <skill-directory>/scripts/validate_prd.py docs/project/PRD.md`.
11. Fix every error. Review warnings and fix any warning that reflects a real defect.
12. Re-read the final diff for scope, ID stability, source fidelity, conditional-reference use, contradictions, secrets, and output-boundary compliance.

## Route project references conditionally

Apply these rules after scope is derived from the user and confirmed upstream requirements:

- Read a UI pattern playbook, such as `docs/playbooks/ui-patterns.md`, only when Current Scope changes user-facing layout, components, navigation, responsive behavior, or interaction patterns, or when an explicitly requested baseline UI decision requires it. Use it to constrain presentation and reuse, never to add pages, features, states, routes, or copy.
- Read payment-flow and payment-module documents only when Current Scope includes payment, pricing, checkout, subscription, credits, quota, billing, or entitlement, or when an explicit Confirmed Next Phase item needs a future-impact note. Read provider-specific documentation only after that provider is confirmed for the applicable phase.
- Read AI, API, auth, data, storage, email, newsletter, analytics, SEO, legal, deployment, or provider documents only when confirmed scope triggers that subject or when an explicitly named Existing Baseline item must be verified.
- Read design files only when the user references them or already-confirmed UI scope needs them.
- Check that a path exists before citing it. Never invent a missing reference path.

The existence, content, or installed capability described by any playbook, module document, design, route, provider, dependency, or template is evidence about constraints or `Existing Baseline` only. It is never evidence that the capability belongs in `Current Scope`. `Possible Later` never triggers current infrastructure. `Confirmed Next Phase` may justify a future-impact note but never a current requirement or active infrastructure decision.

## Apply scope and source authority

- Use this authority order for product decisions: latest explicit user decision; confirmed upstream requirement; existing PRD decision still in force; verified repository fact; design or template reference.
- Use applicable `AGENTS.md` and repository playbooks as process constraints, not as product-scope sources.
- Classify every important item exactly once as `Current Scope`, `Existing Baseline`, `Confirmed Next Phase`, `Possible Later`, or `Non-Goals`.
- Record superseded upstream requirements under `Explicitly Overridden`.
- Require a stable ID for every Current Scope item that implementation or verification must trace. Preserve IDs during incremental updates and never reuse a retired ID for different behavior.
- Require current infrastructure decisions to cite Current Scope IDs or explicitly state `No Current Scope trigger`. Do not use a reference document, template capability, Existing Baseline, Confirmed Next Phase, or Possible Later as the sole basis for active current infrastructure.
- Describe observable product behavior and acceptance outcomes. Exclude file-change lists, implementation steps, task packages, commands, commits, migrations, and deployment instructions.
- Include only environment-variable names and purposes. Never include values, credentials, tokens, private URLs, or other secrets.

## Ask only blocking product questions

Ask at most three questions per round only when a P0 uncertainty would materially change Current Scope, a core flow, pages, payment, auth, data, privacy, or provider feasibility. Use the exact numbered A/B/C/D format in the reference rules. Apply safe P1 defaults and record them; keep P2 items non-blocking in `Open Questions`.

For every genuine unresolved `Open Questions` entry, include an `Options` field with three mutually exclusive, currently reasonable choices labeled `A`, `B`, and `C`, followed by `Recommended: X` and one concise `Reason`. The recommendation must select one listed option without treating it as a confirmed decision. Use `Blocking: 🔴Yes` only for a blocking entry and `Blocking: No` otherwise. Always include `Temporary assumption`, writing `None` or `无` when no temporary assumption has been adopted. Do not apply this unresolved-question schema to entries explicitly marked `Resolved`.

## Finish narrowly

Report the PRD path, meaningful scope decisions or blockers, preserved or overridden IDs/decisions, and the validator result. Do not claim implementation, task generation, or commits occurred.
