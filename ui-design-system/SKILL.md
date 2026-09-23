---
name: ui-design-system
description: Initialize, update, preflight, or audit a project's canonical Design System and reusable AI UI guardrails. Use when establishing UI rules for a new project, consolidating repeated design decisions, checking UI consistency, or installing AGENTS.md enforcement; do not implement product UI.
---

# UI Design System

Create and maintain a project-specific visual source of truth so future AI UI work reuses established patterns instead of redesigning each screen independently.

## Boundary

This Skill owns design-system documentation and design-consistency analysis.

Default writable target:

- `docs/project/design/DESIGN_SYSTEM.md`

When the user explicitly asks to install or update AI enforcement, it may also update the applicable project `AGENTS.md` with the minimal guardrail block from `assets/AGENTS.design-system-snippet.md`.

Do not implement application UI, change product behavior, rewrite business logic, modify the PRD, generate implementation tasks, change dependencies, or perform unrelated refactors.

If the user asks for design-system work and implementation together, finish and validate the design-system pass first. Keep implementation as a separate step unless the user explicitly overrides that separation.

## Modes

Choose the narrowest mode that matches the request:

- **Initialize** — no canonical Design System exists; inspect the project and create one.
- **Update** — a Design System exists; add or revise only rules justified by confirmed decisions or reusable project evidence.
- **Preflight** — read-only; identify the Design System rules that constrain a proposed UI task and flag likely conflicts before coding.
- **Audit** — read-only by default; compare implementation against the Design System and report drift, missing rules, and legitimate exceptions.
- **Install enforcement** — only when explicitly requested; add the minimal `AGENTS.md` rule that makes future UI work read and obey the project Design System.

## Workflow

1. Follow the applicable `AGENTS.md` and the user's current request.
2. Locate the project's canonical Design System:
   - prefer the path named by `AGENTS.md`;
   - otherwise reuse an existing design-system document;
   - otherwise use `docs/project/design/DESIGN_SYSTEM.md`.
3. Read the product PRD only as needed to understand user-facing behavior, scope, and constraints. PRD owns product behavior; the Design System owns visual and interaction-system rules.
4. Read `references/core-rules.md`.
5. Inspect only the repository evidence needed for the requested mode:
   - theme/token sources;
   - global CSS or Tailwind/theme configuration;
   - shared UI primitives;
   - representative canonical screens/components;
   - responsive/layout utilities;
   - recent UI changes relevant to the requested decision.
6. Classify observed UI patterns as:
   - **Canonical** — explicitly confirmed or clearly owned by a shared primitive/reference implementation;
   - **Drift** — conflicts with an established rule;
   - **Legitimate exception** — intentionally different for a documented reason;
   - **Candidate pattern** — repeated or important enough to consider promoting.
7. For Initialize or Update, read `references/promotion-rules.md`. Do not promote one-off fixes into global rules.
8. For Initialize, assemble the document from `assets/DESIGN_SYSTEM.template.md`. Fill it with project facts; do not copy another project's visual values.
9. For Update, preserve valid existing rules and edit incrementally. Prefer clarifying ownership and removing contradictions over rewriting the document.
10. For Preflight or Audit, read `references/audit-rules.md`. Stay read-only unless the user explicitly requests fixes.
11. If AGENTS enforcement is requested, read `references/agent-enforcement.md` and adapt `assets/AGENTS.design-system-snippet.md` to the project's actual path.
12. Run:

    ```bash
    python3 <skill-directory>/scripts/validate_design_system.py <design-system-path>
    ```

13. Perform the semantic checks the validator cannot do:
    - user decisions outrank accidental legacy code;
    - product behavior is not being redefined as visual guidance;
    - shared roles have one canonical pattern;
    - exceptions are explicit rather than silent forks;
    - mobile/responsive rules describe transformation, not just shrinking;
    - interaction ownership covers focus, scroll, dismissal, and destructive actions where relevant.

## Authority model

Use this precedence for visual and interaction-system decisions:

1. latest explicit user design decision
2. current canonical project Design System rule
3. explicitly named reference implementation or shared primitive
4. verified project tokens/theme configuration
5. repeated current implementation pattern
6. isolated legacy/local styling

Repository prevalence alone does not make a pattern canonical.

When PRD and Design System appear to conflict:
- PRD owns **what the product does**;
- Design System owns **how recurring UI roles look and behave visually**;
- do not silently override either document; identify the conflict and update the correct source of truth deliberately.

## Project-specific, not universal

This Skill is reusable; the generated Design System is project-specific.

Do not hardcode another project's:
- colors;
- border widths;
- radius;
- shadows;
- typography;
- spacing values;
- modal appearance;
- breakpoints;
- control heights.

The reusable part is the governance and structure: define semantic tokens, canonical component roles, responsive behavior, interaction ownership, exceptions, and reuse rules.

## Finish

Report briefly:

- mode used: Initialize / Update / Preflight / Audit / Install enforcement
- Design System path
- important rules created, changed, or audited
- whether AGENTS enforcement was installed
- validator result
- unresolved design decisions or documented exceptions

Do not claim UI implementation or product behavior changed when it did not.
