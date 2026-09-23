# AGENTS.md enforcement

The Design System becomes reliably reusable only when project operating instructions make AI read it before relevant UI work.

## Install principle

Keep the `AGENTS.md` block short.

Do not paste the entire Design System into `AGENTS.md`. That creates duplication and future contradictions.

`AGENTS.md` should:
- point to the canonical Design System path;
- define when it must be read;
- state its authority over recurring visual/UI-system decisions;
- require reuse before new patterns;
- require deliberate resolution when a task conflicts with the Design System;
- require a final consistency check.

Use `assets/AGENTS.design-system-snippet.md` as the base.

## Scope the trigger

The agent does not need to load the Design System for every backend-only edit.

Require it for work touching:
- UI components;
- layout or responsive behavior;
- styling/theme/tokens;
- forms and controls;
- cards/rows/tables/lists;
- dialogs/modals/drawers/popovers/menus;
- navigation;
- loading/empty/error/status presentation;
- interaction behavior such as focus, scrolling, disclosure, dismissal, or touch targets.

## Precedence

The recommended project contract is:

- PRD owns product behavior and scope.
- Design System owns recurring visual and interaction-system rules.
- AGENTS.md owns the workflow requirement to consult those documents.
- Latest explicit user instruction may change either source of truth, but the relevant document should be updated deliberately rather than silently diverging.

## Conflict handling

When implementation requirements conflict with the Design System:

1. determine whether the conflict is product behavior or visual-system behavior;
2. do not work around the rule with local CSS simply to finish the task;
3. if the new behavior is a deliberate reusable design decision, update the Design System first or in the design-documentation pass authorized by the task;
4. if it is a true one-off exception, document the exception and its boundary;
5. then implement against the updated/confirmed rule.

## Existing repositories

When installing enforcement into a mature project:
- locate the nearest applicable `AGENTS.md`;
- preserve unrelated instructions;
- avoid duplicating an existing UI/design section;
- adapt the canonical Design System path;
- do not add implementation-specific style values to AGENTS.md.

## New repositories

Install the guardrail early, immediately after or alongside the initial Design System. This prevents later agents from establishing competing patterns before the project has a visual source of truth.
