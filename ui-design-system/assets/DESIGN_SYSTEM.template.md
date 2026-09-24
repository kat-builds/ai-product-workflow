# {{PROJECT_NAME}} — Design System

Last updated: YYYY-MM-DD
Document language: en

> This document is the canonical source of truth for recurring visual and interaction-system decisions. Product behavior and business rules remain in the PRD. Repository code is implementation evidence; isolated legacy styles do not override this document.

## 1. Authority & Scope

### Source-of-truth roles

- **PRD:** {{PRD_PATH_OR_RULE}}
- **Design System:** this document
- **AI/project operating rules:** {{PROJECT_INSTRUCTION_PATH_OR_NONE}}
- **Theme/token source:** {{TOKEN_SOURCE}}
- **Shared UI primitive source:** {{SHARED_UI_SOURCE}}

### Canonical reference implementations

| UI role | Reference implementation | What it establishes |
|---|---|---|
| {{ROLE}} | {{PATH_OR_COMPONENT}} | {{RULE}} |

### Explicit exceptions

| Surface | Exception | Reason | Shared rules that still apply |
|---|---|---|---|
| {{SURFACE_OR_NONE}} | {{EXCEPTION}} | {{REASON}} | {{RULES}} |

## 2. Design Profile

- **Visual character:** {{CHARACTER}}
- **Density:** {{DENSITY}}
- **Shape language:** {{SHAPE}}
- **Hierarchy:** {{HIERARCHY}}
- **Motion philosophy:** {{MOTION_OR_NONE}}

## 3. Foundations

### 3.1 Color semantics

| Semantic role | Token / source | Use | Must not mean |
|---|---|---|---|
| Background | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Foreground | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Primary | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Secondary | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Muted / informational | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Success | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Warning / attention | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |
| Destructive / conflict | {{TOKEN}} | {{USE}} | {{ANTI_USE}} |

### 3.2 Typography

| Role | Token / classes | Usage |
|---|---|---|
| Page title | {{VALUE}} | {{USAGE}} |
| Section title | {{VALUE}} | {{USAGE}} |
| Body | {{VALUE}} | {{USAGE}} |
| Label | {{VALUE}} | {{USAGE}} |
| Metadata / helper | {{VALUE}} | {{USAGE}} |

### 3.3 Spacing & density

Define the project's spacing rhythm and when compact vs normal density applies.

- **Compact:** {{VALUE_AND_USE}}
- **Default:** {{VALUE_AND_USE}}
- **Section:** {{VALUE_AND_USE}}

### 3.4 Borders, radius & elevation

- **Border ownership:** {{RULE}}
- **Border width/style:** {{VALUE}}
- **Radius:** {{VALUE}}
- **Shadow/elevation:** {{VALUE}}
- **One logical object = one visual boundary:** {{PROJECT_RULE}}

### 3.5 Control sizing & touch targets

| Role | Size policy | Typical use |
|---|---|---|
| Dense inline control | {{VALUE}} | {{USE}} |
| Default control | {{VALUE}} | {{USE}} |
| Mobile major action | {{VALUE}} | {{USE}} |
| Mobile close / important menu | {{VALUE}} | {{USE}} |

Do not assume dense desktop geometry is appropriate for major mobile actions.

## 4. Layout & Responsive System

### 4.1 Containers & breakpoints

- **Container ownership:** {{RULE}}
- **Breakpoints:** {{VALUES_OR_SOURCE}}
- **Page padding:** {{RULE}}

### 4.2 Responsive transformation

Define how hierarchy changes rather than merely shrinking desktop UI.

- **Desktop:** {{RULE}}
- **Tablet / medium:** {{RULE}}
- **Mobile:** {{RULE}}
- **Progressive disclosure:** {{RULE}}
- **Metadata limits / overflow:** {{RULE}}

### 4.3 Content height & whitespace

- Natural content height vs equal-height behavior: {{RULE}}
- When stretching is allowed: {{RULE}}

### 4.4 Scroll ownership

- Page scroll owner: {{RULE}}
- Modal/drawer scroll owner: {{RULE}}
- Sticky header/footer behavior: {{RULE}}
- Bottom clearance / safe-area behavior: {{RULE}}

## 5. Component Patterns

### 5.1 Buttons & actions

Define:
- primary;
- secondary;
- destructive;
- low-frequency/overflow;
- icon-only;
- disabled/loading.

Rules:
{{BUTTON_RULES}}

### 5.2 Inputs, selects & dense data controls

{{FORM_RULES}}

### 5.3 Cards, rows & item boundaries

{{CARD_ROW_RULES}}

### 5.4 Lists & tables

{{LIST_TABLE_RULES}}

### 5.5 Section headers / grouping

{{SECTION_RULES}}

### 5.6 Major modal / dialog shell

Define the canonical Header → Body → Footer hierarchy.

- **Reference implementation:** {{REFERENCE}}
- **Header:** {{RULE}}
- **Secondary/overflow actions:** {{RULE}}
- **Body:** {{RULE}}
- **Footer:** {{RULE}}
- **Mobile presentation:** {{RULE}}
- **Desktop presentation:** {{RULE}}

### 5.7 Drawer / popover / menu

{{LAYERED_UI_RULES}}

### 5.8 Navigation

{{NAV_RULES}}

### 5.9 Status, feedback & notifications

| State | Visual severity | Pattern |
|---|---|---|
| Normal / informational | {{VALUE}} | {{PATTERN}} |
| Success | {{VALUE}} | {{PATTERN}} |
| Warning / attention | {{VALUE}} | {{PATTERN}} |
| Conflict / destructive | {{VALUE}} | {{PATTERN}} |

## 6. Interaction Rules

### 6.1 Decision-surface information economy

{{DECISION_SURFACE_RULE}}

### 6.2 Progressive disclosure

{{DISCLOSURE_RULE}}

### 6.3 Viewport stability

{{VIEWPORT_RULE}}

### 6.4 Focus, Escape & layered dismissal

{{FOCUS_DISMISSAL_RULE}}

### 6.5 Confirmation & destructive actions

{{CONFIRMATION_RULE}}

## 7. UI Copy & Labeling

- Label casing: {{RULE}}
- Helper/error copy: {{RULE}}
- Repeated labels on mobile: {{RULE}}
- i18n ownership: {{RULE}}

## 8. Reuse & Component Ownership

| Role | Canonical owner | Reuse rule | Do not create |
|---|---|---|---|
| {{ROLE}} | {{COMPONENT_TOKEN_PATH}} | {{RULE}} | {{PARALLEL_PATTERN}} |

Before adding screen-specific styles, confirm that no existing shared token, primitive, or canonical component owns the same role.

## 9. Accessibility & Input Modality

- Keyboard: {{RULE}}
- Focus visibility: {{RULE}}
- Contrast: {{RULE}}
- Touch targets: {{RULE}}
- Reduced motion: {{RULE_OR_NONE}}
- Screen-reader labeling: {{RULE}}

## 10. Do / Don't

### Do

- {{DO_RULE}}

### Don't

- {{DONT_RULE}}

## 11. Documented Exceptions

| ID | Surface | Rule overridden | Reason | Boundary / expiry |
|---|---|---|---|---|
| {{EXCEPTION_ID_OR_NONE}} | {{SURFACE}} | {{RULE}} | {{REASON}} | {{BOUNDARY}} |

## 12. Governance

### When a new rule belongs here

Promote a UI decision when it is explicitly global, affects a shared primitive/system, repeats across meaningful surfaces, prevents recurring interaction/accessibility defects, or becomes the approved reference for a reusable role.

Do not promote one-off content/layout tweaks without reusable meaning.

### Change process

1. Identify the reusable role and current owner.
2. Confirm whether the change is global, local, or an exception.
3. Update this document before or alongside the authorized design-documentation pass.
4. Implement by extending shared ownership rather than adding a parallel local system.
5. Audit affected surfaces for drift.

## 13. Design Audit Checklist

- [ ] Semantic tokens are reused; no unnecessary raw color/style literals.
- [ ] Typography follows the documented hierarchy.
- [ ] One logical object reads as one visual boundary.
- [ ] Primary/secondary/destructive hierarchy matches consequence.
- [ ] Responsive UI transforms hierarchy instead of squeezing desktop structure.
- [ ] Mobile touch policy is respected for major actions.
- [ ] Status colors match severity.
- [ ] Shared modal/layer patterns have one owner.
- [ ] Sticky regions do not obscure meaningful content/actions.
- [ ] Scroll/focus/Escape/outside-dismissal ownership is unambiguous.
- [ ] Expand/collapse/save/sort avoids unnecessary viewport jumps.
- [ ] Exceptions are documented rather than silently forked.
- [ ] New styles do not duplicate an existing shared role.
