# Logo Brief Checklist

Use this checklist to identify missing requirements before designing.

## Product Context

Prefer these sources in order:

1. `docs/project/PRD.md`, when present;
2. explicit user instructions;
3. current product/config copy;
4. other reliable repository documentation.

Extract:

- product/brand name or domain;
- what the product does;
- target users;
- product positioning cues that are actually documented.

Do not invent missing brand strategy.

## Visual Context

Read `docs/project/design/DESIGN_SYSTEM.md` when present.

Inspect:

- current brand/logo assets;
- actual theme/token source of truth;
- light and dark token values;
- shared UI shape language;
- typography and visual density;
- whether the product is mostly square, rounded, angular, circular, soft, sharp, monoline, solid, or mixed;
- any documented exceptions.

Do not assume the logo should copy component radius or shape literally. Use the Design System as context, not as a forced logo template.

## Required Inputs

- Brand/product name or domain
- Product category / core use case
- Asset usage scope
- Required outputs or current asset inventory
- Color source: project tokens, explicit palette, or both
- Whether a wordmark is required
- Any explicit geometry or motif direction
- Any prohibited motifs, styles, or brand references

## Existing Asset Audit

Inspect and record:

- logo configuration;
- metadata icon declarations;
- favicon files and links;
- Apple Touch icons;
- PWA/maskable icons;
- manifest icon entries;
- OG/Twitter image paths;
- theme-specific logo usage;
- current source file ownership.

Record each required path, format, pixel dimension, theme variant, and purpose before creating files.

Check whether:

- an old asset uses stale colors;
- current config references missing files;
- multiple paths accidentally represent the same role;
- the project has both light/dark themes but only one usable logo;
- existing assets conflict with the current Design System or explicit user direction.

## Strongly Recommended Inputs

- Visual keywords, if the user has them
- Preferred or prohibited geometry
- Whether the mark should be icon-only, wordmark, or both
- Desired brand mood
- Delivery paths when the repository does not already define them

## Ambiguity Report Format

When a blocker exists, report:

1. Missing item
2. Why it blocks a correct result
3. Proposed fallback if the user wants immediate execution

## Common Blockers

- Product/brand name is undecided
- Requested format conflicts with actual platform usage
- Color requirement references a token that does not exist
- The visible brand color differs from the declared token owner
- Required asset dimensions cannot be determined
- PRD/product context is too incomplete to choose a meaningful motif
- Existing brand direction conflicts with the latest explicit user instruction
