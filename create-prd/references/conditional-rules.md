# Create PRD — Conditional Rules

Read only the sections triggered by the current PRD scope or a genuine unresolved product decision.

## Blocking product questions

Use this section only when an unresolved decision would materially change `Current Scope`, a core flow, page structure, payment, auth, data, privacy, or provider feasibility.

- Ask at most three blocking questions per round.
- Prefer safe defaults for non-blocking details instead of asking.
- Do not ask the user to choose ordinary implementation details that can be derived from the repository.
- Keep P1 assumptions explicit in the PRD when they matter.
- Keep P2 issues non-blocking in `Open Questions`.
- Never invent prices, real API endpoints, legal commitments, third-party limits, or sensitive-data policies to avoid asking a genuinely blocking question.

When a blocking multiple-choice question is needed, use 2–4 mutually exclusive options and include a recommendation plus one concise reason. Accept compact replies such as `ACB` or `1A, 2C, 3B`. If the user says to use the recommendations, continue without reconfirming.

For every genuinely unresolved `Open Questions` item in the PRD, include:

- three mutually exclusive current options: `A`, `B`, `C`
- `Recommended: X`
- one concise `Reason`
- `Blocking: 🔴Yes` or `Blocking: No`
- `Temporary assumption`, using `None` or `无` when no assumption is adopted

Do not apply this unresolved-question schema to items already marked resolved.

## Conditional repository references

Read project references only after the applicable scope has been established.

### UI and design

Read UI pattern playbooks or design references only when:

- `Current Scope` changes layout, components, navigation, responsive behavior, or interaction patterns; or
- the user explicitly referenced a design; or
- a confirmed baseline UI decision needs verification.

Use them to constrain presentation, state ownership, design tokens, and reuse. Do not infer new pages, routes, features, states, copy, auth, or monetization from a design or template.

### Payment and entitlement

Read payment-flow or payment-module documents only when `Current Scope` includes payment, pricing, checkout, subscription, credits, quota, billing, or entitlement, or when a `Confirmed Next Phase` item needs a future-impact note.

Read provider-specific documentation only after that provider is confirmed for the applicable phase. An installed provider does not mean it is selected or active.

### AI, API, auth, data, storage, email, analytics, SEO, legal, deployment

Read these references only when the confirmed scope triggers the subject or an explicitly named `Existing Baseline` must be verified.

For AI image generation, reference images, generation history, image storage, model routing, or credits, read `docs/playbooks/ai-image-architecture.md` only if it exists and the scope actually triggers that topic. Use it to identify existing contracts and reuse boundaries, not to create scope.

## Infrastructure depth

Expand infrastructure requirements only when `Current Scope` actually needs them.

Typical triggers include:

- third-party API, provider SDK, or webhook
- authentication, authorization, database, user assets, or history
- file upload, local processing, object storage, or cloud results
- payment, subscriptions, credits, quota, or entitlement
- analytics, conversion tracking, SEO indexing, privacy, or legal obligations

For simple projects, explicitly mark unneeded infrastructure as `Not required` instead of inventing architecture.

## Domain-specific completeness

When a triggered domain matters to the product behavior, specify observable requirements for the relevant cases, such as:

- API/provider: input/output contract, timeout/failure behavior, limits, server boundary
- Auth/data: ownership, permissions, lifecycle, refresh/recovery, deletion
- Storage: what is stored, where, lifecycle, failure behavior
- Payment: product mapping, checkout return, webhook authority, idempotency, entitlement, recovery
- Analytics: event trigger, necessary non-sensitive properties, privacy boundary, success metric
- SEO: indexability, canonical/metadata implications, sitemap/robots behavior when relevant
- UI: responsive behavior, empty/loading/error/success states, interaction ownership

Do not expand a domain merely because the template contains a section for it.
