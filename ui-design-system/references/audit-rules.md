# Design System preflight and audit rules

Use this file for Preflight and Audit modes.

## Preflight

Before implementation, identify only the rules relevant to the proposed UI task.

Return a compact constraint set covering, as applicable:

- canonical primitive/reference implementation;
- token/typography/shape rules;
- responsive transformation;
- action hierarchy;
- state/severity mapping;
- visual boundary ownership;
- scroll/focus/dismissal ownership;
- touch-target roles;
- explicit exceptions.

Flag any requested change that would create a second pattern for an already-owned role.

Do not turn Preflight into an implementation plan unless the user asks for one.

## Audit evidence

Inspect representative evidence rather than every JSX class in the repository by default.

Prioritize:
1. shared primitives and token definitions;
2. canonical reference implementations named by the Design System;
3. surfaces changed by the current task;
4. repeated UI structures;
5. suspicious local overrides.

## Audit classification

Classify findings as:

- **Compliant** — follows the canonical role/pattern.
- **Drift** — contradicts an existing Design System rule.
- **Missing shared ownership** — multiple local implementations exist but the Design System has no clear owner.
- **Documented exception** — differs intentionally and matches a recorded exception.
- **Candidate rule** — implementation reveals a reusable decision not yet documented.
- **Stale rule** — Design System conflicts with a newer explicit user decision.

## Audit dimensions

Check only dimensions relevant to the project:

- semantic colors and status severity;
- typography hierarchy;
- spacing/density;
- border/radius/shadow shape language;
- button/action hierarchy;
- form/input geometry;
- card/row visual ownership;
- tables/lists and mobile transformations;
- modal/drawer/popover/menu shell consistency;
- sticky header/footer behavior;
- scroll ownership;
- focus and layered dismissal;
- progressive disclosure;
- viewport stability after expand/collapse/save/sort;
- touch-target policy;
- disabled/loading/error/success states;
- duplicated screen-specific CSS that should be shared.

## Severity

Use practical severity, not aesthetic drama:

- **High** — interaction safety/accessibility issue, destructive-action ambiguity, layered-dismissal problem, content/action becomes unreachable, or a shared primitive violates the canonical system across many screens.
- **Medium** — clear cross-surface inconsistency, duplicated pattern ownership, status hierarchy mismatch, responsive structure drift.
- **Low** — local cosmetic inconsistency that does not impair comprehension or action.

## Audit output

Prefer a short table:

| Severity | Surface | Rule | Finding | Recommended owner |
|---|---|---|---|---|

Then summarize:
- what is already consistent;
- what should be fixed locally;
- what should be promoted into the Design System;
- what should remain an exception.

Audit mode is read-only unless the user explicitly asks to apply fixes.
