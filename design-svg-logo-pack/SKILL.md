---
name: design-svg-logo-pack
description: Design and integrate original web brand asset packs from a project's real product context, visual language, theme tokens, and asset inventory. Use when users ask to create, refresh, recolor, resize, or globally integrate logos, favicons, app icons, PWA/maskable icons, or OG/social previews. Derive geometry and styling from the current project instead of imposing a fixed logo style.
---

# Design SVG Logo Pack

## Overview

Create a complete, implementation-ready brand asset pack for a product website or app.

The Skill does not impose a universal visual style. It inspects the current project first, then derives logo geometry, color, contrast, variants, file paths, and platform sizes from the product context, existing visual language, theme tokens, Design System, and real asset usage.

The goal is consistency with the product, not a fixed "AI logo" look.

## Workflow

### 1. Clarify the brief

- Read `references/logo-brief-checklist.md`.
- Ask only the minimum follow-up questions needed to unblock a correct result.
- Preserve explicit user direction for brand mood, geometry, wordmark use, or prohibited motifs.
- Do not invent brand positioning or marketing copy when the project does not support it.

### 2. Inspect project context

- Prefer `docs/project/PRD.md` when it exists.
- If there is no PRD, locate reliable product context from repository docs, config, product copy, or the current user request.
- Read `docs/project/design/DESIGN_SYSTEM.md` when it exists and use it as visual context for shape language, color ownership, contrast, and interaction/UI conventions. Do not treat it as product scope.
- Locate the project's actual theme/token source of truth and resolve aliases before choosing colors.
- Locate every current brand-asset usage point, including:
  - logo configuration;
  - metadata icons;
  - favicon links;
  - web app manifest;
  - Apple Touch icons;
  - PWA and maskable icons;
  - browser shortcuts;
  - OG images;
  - Twitter/social images.
- Build an inventory of every referenced path, format, size, theme variant, and purpose before producing files.
- Do not assume the deliverable is limited to a light logo, dark logo, and OG image.

### 3. Derive the visual direction

Use project evidence in this order:

1. explicit user direction;
2. existing brand assets that are still current;
3. the project Design System and theme tokens;
4. current product UI and shared visual patterns;
5. product context from PRD/config/copy;
6. a documented fallback only when the project has no usable visual direction.

Derive, rather than hard-code:

- overall geometry: square, rounded, circular, angular, organic, monoline, solid, or mixed;
- corner treatment;
- stroke weight;
- fill/stroke balance;
- motif complexity;
- light/dark treatment;
- icon-only vs wordmark usage.

Do not assume rounded corners, a specific radius, a specific stroke weight, or a specific brand silhouette.

When no reliable visual direction exists, choose the simplest low-complexity geometry that remains legible at favicon size, state the assumption, and keep it easy to revise.

Use one central motif with a small number of geometric primitives. Keep the mark abstract and product-related without copying a known brand silhouette. Avoid text glyph dependence inside the icon mark unless the user explicitly wants a lettermark.

### 4. Produce vector source files

- Produce the SVG variants actually required by the asset inventory and theme usage.
- Use a square source canvas for icon marks; `512x512` is the default source size when the repository does not define another canonical source.
- Use vector primitives and paths only unless the user explicitly asks for raster artwork.
- Keep structure clean: grouped layers, stable IDs where useful, no unnecessary filters.
- Include `<title>` and `<desc>` when the SVG is used as meaningful accessible content.
- Reuse one canonical geometry per intended mark variant and derive platform sizes from it to prevent drift.

### 5. Map project colors

- Prefer the project's actual brand/logo token owner when one exists.
- If the project intentionally uses `primary` / `primary-foreground` as brand colors, reuse them.
- Do not assume those tokens are always the brand colors.
- Resolve light and dark theme values separately when both themes exist.
- When explicit user brand colors conflict with current project tokens, report the mismatch and follow the latest explicit user direction unless it would create an accessibility or integration problem.
- Record the final resolved color values used for every delivered theme variant.
- When the export pipeline cannot handle CSS color functions such as `oklch(...)`, convert final delivered SVG/raster colors to a compatible format such as `#RRGGBB`.

### 6. Produce the complete platform asset set

Generate the assets actually required by the discovered inventory.

For a typical web project, check whether the project needs:

- favicon sizes such as `16x16`, `32x32`, and `48x48`;
- a multi-size `.ico`;
- Apple Touch icon at `180x180`;
- PWA/Android icons at `192x192` and `512x512`;
- a separate maskable icon source with artwork inside the platform safe area;
- light/dark application logos at the configured dimensions;
- OG/Twitter preview at the dimensions required by the repository, commonly `1200x630`.

Do not create arbitrary files that the project will never reference.

For a new project with no existing asset inventory, use current web-platform conventions as the fallback set and record that these are defaults rather than project-derived requirements.

### 7. Produce OG/social assets when in scope

- Use the dimensions required by the repository; `1200x630` is the fallback when no project-specific size exists.
- Reuse the brand motif as the primary visual signal, but compose for a wide social preview rather than stretching the square icon.
- Use product/brand text only when it is reliably sourced from the project or user.
- Keep text sparse and readable after social compression.
- Avoid UI screenshots unless the user explicitly asks for screenshot-style social art.
- Prefer the existing canonical social-image path when the project already defines one.

### 8. Integrate globally when requested

- Update the repository's real logo, icon, manifest, metadata, and social-image references.
- Prefer one source of truth over per-component overrides.
- Follow the project's actual framework and metadata conventions rather than assuming Next.js, Astro, Vite, or another stack.
- Do not change unrelated UI or product behavior while integrating brand assets.

### 9. Validate

Verify:

- SVG canvas/viewBox values;
- raster pixel dimensions;
- `.ico` embedded sizes when applicable;
- maskable safe-area placement;
- configured paths actually exist;
- light/dark contrast;
- favicon legibility at `16px` and `32px`;
- full-size balance at the canonical source size;
- OG readability at reduced preview size;
- no unsupported color syntax for the target export pipeline;
- no obvious accidental resemblance to major known brand marks.

### 10. Report the result

Summarize:

- visual direction and project evidence used;
- assumptions made because the project did not define something;
- exact files created or updated;
- every delivered size and format;
- integration paths changed;
- validation performed;
- any unresolved ambiguity.

Include a concise legal boundary note when relevant: the mark is intentionally designed to avoid obvious similarity to major known marks, but this is not a trademark clearance or legal opinion.

## Default behavior

Use defaults only when the project and user do not provide an answer.

- Source location: follow the current repository's existing asset structure; for a new conventional web project, `public/` is an acceptable fallback.
- Source size: `512x512` for square icon marks when no project canonical size exists.
- Geometry: no fixed rounded, square, circular, or angular default. Derive from project context; if nothing exists, use simple low-complexity geometry and state the assumption.
- Stroke/fill style: no fixed default weight. Choose the simplest treatment that remains legible at small sizes and fits the project's visual language.
- Theme variants: create only the variants the project actually needs; if both light and dark themes require distinct asset treatment, provide both.
- Wordmark: do not invent one unless requested or already part of the current brand system.
- OG/social copy: use only sourced product/brand text.

## Quality bar

- The asset family should feel like one system across logo, favicon, app icons, and social previews.
- Variants should be recognizably the same mark unless the product explicitly requires distinct marks.
- The mark must remain readable at favicon size.
- The design should fit the current product's visual language without blindly copying UI component geometry.
- Keep path count low and source ownership clear.
- Derive raster sizes deterministically from canonical vector sources where possible.
- Avoid unnecessary visual complexity, gradients, filters, or decorative effects unless the project already uses them or the user requests them.
- Avoid obvious similarity to well-known brand marks.

## Legal boundary

Do not promise trademark registration success, global uniqueness, or legal clearance. Do not provide legal advice.

## Resources

- Brief checklist: `references/logo-brief-checklist.md`
- Legal-safe wording: `references/legal-boundary.md`
