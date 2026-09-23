# Core Design System rules

Use these rules for every `$ui-design-system` run.

## Separate the sources of truth

Keep document roles explicit:

- **PRD** — user-facing product behavior, scope, business rules, data semantics.
- **DESIGN_SYSTEM.md** — reusable visual language, component roles, responsive behavior, interaction-system rules.
- **AGENTS.md** — operational instruction that tells AI when it must read and obey the Design System.
- **Implementation code** — evidence of current implementation, not automatic design authority.

Do not put feature scope into the Design System. Do not put reusable CSS/component geometry into the PRD unless it is itself a user-observable product requirement.

## Prefer ownership over duplication

Every recurring UI role should have one canonical owner where practical.

Examples:
- one primary-button pattern;
- one status severity mapping;
- one major-modal shell;
- one dense-row boundary rule;
- one shared spacing/token source.

When multiple implementations exist, identify which is canonical and which are drift or explicit exceptions. Do not normalize by copying the most common local CSS if the common code is inconsistent or legacy.

## Semantic tokens first

Prefer semantic roles over raw visual values in component guidance.

Good:
- primary / secondary / destructive;
- foreground / muted / warning / success;
- compact / default / major-action control size.

Avoid making screen-specific utility strings the conceptual source of truth.

The project Design System may record resolved token names and values, but implementation should reuse existing semantic tokens/primitives before introducing new literals.

## Reference implementation, not copy dependency

A project may name a current component or screen as the visual reference implementation for a pattern.

Write:
> Edit Recipe is the current reference implementation of the shared major-modal shell.

Do not write:
> Every modal must copy Edit Recipe markup.

The goal is shared ownership, not hidden cross-feature coupling.

## Responsive design transforms information

Mobile is not desktop squeezed into a narrower width.

A good project Design System should define:
- hierarchy changes;
- progressive disclosure;
- label/metadata reduction;
- content-height behavior;
- stacking;
- safe areas;
- scroll ownership;
- touch-target policy.

Do not prescribe arbitrary mobile changes that are unsupported by the product or current confirmed design.

## One logical object should read as one visual object

When a row/card represents one domain object, its name, status, quantity, metadata, and actions should visually read as belonging together unless the project intentionally separates them.

Avoid:
- details appearing outside their owner boundary;
- competing outer borders;
- repeated labels that obscure hierarchy;
- independent cards for metadata that is semantically subordinate to the same item.

## Action hierarchy must reflect consequence

Define how the project distinguishes:
- primary completion;
- secondary/progress save;
- destructive/reset;
- overflow/low-frequency;
- disabled/unavailable;
- confirmation-required actions.

Destructive or irreversible actions should not gain visual prominence merely because they share a footer with the primary action.

## Status colors represent severity, not implementation detail

Projects should map status semantics deliberately.

Do not make normal states look like errors or warnings because of implementation facts such as "local rather than cloud".

A typical project may distinguish:
- neutral/informational;
- success;
- warning/attention;
- destructive/conflict.

The exact colors belong to the project.

## Interaction ownership is part of design

For layered UI, define who owns:
- scroll;
- focus;
- dismissal;
- Escape;
- outside interaction;
- sticky regions;
- viewport anchoring after expand/collapse.

The topmost active modal/confirmation should not accidentally dismiss its parent unless the product explicitly intends that behavior.

## Compact controls and touch actions are different roles

Do not force one global height onto every control.

A project may intentionally have:
- dense inline data-entry controls;
- normal desktop controls;
- larger mobile primary/close/menu actions.

The Design System should define these roles and their target sizes. Do not infer that a compact desktop token is automatically appropriate for every mobile action.

## Preserve stable viewport context

Disclosure, expand/collapse, sorting, save, and inline editing should avoid unexpected viewport jumps when the user's current visual context can be preserved.

Document this as a reusable interaction rule only when it applies broadly or has been explicitly confirmed.

## Exceptions must be named

A deliberate exception should state:
- what differs;
- why;
- where it applies;
- what shared rules still apply.

An undocumented exception is drift, not a second design system.
