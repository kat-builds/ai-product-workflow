# Promoting UI decisions into the Design System

Use these rules when deciding whether a recent UI fix or design decision belongs in the project Design System.

## Promote when at least one strong condition is true

A rule is a good Design System candidate when:

1. the user explicitly states that it should apply broadly or become the standard;
2. it affects a shared primitive, token, shell, layout system, or interaction owner;
3. the same problem/pattern appears on two or more meaningful surfaces;
4. it prevents recurring accessibility, touch, focus, scroll, destructive-action, or dismissal defects;
5. future components would otherwise be likely to reinvent the same decision;
6. a named reference implementation has become the approved model for a reusable role.

## Usually keep local

Do not promote automatically when the change is:

- one screen's unique business layout;
- a one-off copy adjustment;
- a content-specific width or spacing tweak;
- a temporary workaround;
- a browser/library bug patch with no reusable design meaning;
- an implementation detail already fully expressed by an existing token/primitive;
- a preference inferred from one screenshot without confirmation.

## Convert incidents into reusable rules

Do not document the incident itself.

Bad:
> Quick Stock's three-dot menu overlapped the X on September 23.

Better:
> Major modal secondary/overflow actions must not compete with the canonical Close region; place them in a separate action region when needed.

Bad:
> Shopping categories had a large blank box.

Better:
> Mobile category/list containers default to natural content height; desktop equal-height rules must not leak into mobile without an explicit alignment reason.

## Promotion test

Before adding a rule, answer:

- **Role:** What reusable UI role does this govern?
- **Owner:** Which token/primitive/pattern owns it?
- **Scope:** Where should it apply?
- **Exception:** When should it not apply?
- **Evidence:** Is this explicitly confirmed or supported by repeated/shared project evidence?

If these cannot be answered, keep the change local.

## Update style

When the Design System already contains a nearby rule:
- strengthen or clarify that rule instead of adding a duplicate section;
- preserve project terminology;
- keep examples subordinate to the rule;
- name a canonical reference implementation when that reduces ambiguity.

Avoid chronological changelog prose in the normative Design System. Git history already records chronology.
