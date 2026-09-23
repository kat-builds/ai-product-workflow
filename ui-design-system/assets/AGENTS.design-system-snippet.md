## UI / Design System

For any task that changes UI components, styling, layout, responsive behavior, forms/controls, navigation, status presentation, dialogs/modals/drawers/popovers/menus, or interaction behavior such as focus, scrolling, disclosure, dismissal, or touch targets:

1. Read `docs/project/design/DESIGN_SYSTEM.md` before editing code.
2. Treat it as the canonical source of truth for recurring visual and interaction-system decisions. The PRD remains authoritative for product behavior and scope.
3. Reuse existing semantic tokens, shared primitives, and canonical reference components before creating screen-specific styles or a parallel pattern.
4. Do not silently diverge from the Design System. If a requested change conflicts with it, determine whether the rule should be deliberately updated or the surface needs a documented exception before implementation.
5. Keep responsive behavior consistent with the documented hierarchy, scroll ownership, touch-target, and layered-interaction rules.
6. Before finishing, check the changed UI against the applicable Design System rules and report any intentional exception.
