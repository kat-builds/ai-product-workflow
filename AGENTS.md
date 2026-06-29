# Repository Guidelines

> [!IMPORTANT]
> **Customize this file before using the workflow in another repository.**
>
> The project-specific rules below describe an example Next.js SaaS codebase. They are not universal defaults. If your repository uses a different framework, runtime, package manager, directory structure, database, authentication system, payment provider, deployment platform, or test runner, replace the corresponding guidance with rules verified against your repository.
>
> Before assigning implementation work to an AI coding agent:
>
> 1. Inspect the actual repository structure and identify application code, shared components, tests, scripts, static assets, documentation, and configuration.
> 2. Read the package manifest, lockfiles, CI configuration, and existing contributor documentation.
> 3. Replace the example architecture notes with the frameworks, services, and infrastructure that the project actually uses.
> 4. List only build, development, formatting, test, migration, and deployment commands that exist in the repository.
> 5. Document the project's real naming, formatting, module-boundary, i18n, security, and testing conventions.
> 6. Remove rules for capabilities the project does not use. Do not assume authentication, payments, databases, storage, analytics, AI providers, or cloud deployment merely because they appear in this example.
> 7. Keep repository instructions aligned with `docs/PRD.md` and `docs/tasks.md`; project-specific implementation rules must not expand the confirmed `Current Scope`.
>
> At minimum, review and customize these sections:
>
> - `Project Structure & Module Organization`
> - `Current Architecture Notes`
> - `Build, Test, and Development Commands`
> - `Coding Style & Naming Conventions`
> - `Testing Guidelines`
> - `Commit & Pull Request Guidelines`
> - `Configuration & Secrets`
>
> If a detail cannot be verified from the repository, write `TBD` and explain how it should be confirmed instead of inventing a rule or command.

## Project Structure & Module Organization
Routes and server actions live in `src/app` (locale-aware pages in `[locale]`). Reusable UI sits in `src/components`—libraries like `ui/`, `magicui/`, `tailark/`, plus domain folders. Shared logic and AI workflows belong in `src/lib` and `src/ai`, while Drizzle schemas and migrations stay in `src/db`. Place transactional emails in `src/mail`, analytics providers in `src/analytics`, static assets in `public/`, operational scripts in `scripts/`, and marketing/docs content in `content/`.

## Current Architecture Notes
The app uses Next.js App Router with `next-intl`; public routes live under `(marketing)`, authenticated routes under `(protected)`, and API routes under `src/app/api`. Better Auth uses Drizzle/PostgreSQL and currently exposes credential login in product config; Google provider support remains wired in auth config but GitHub login is disabled. Payments use the provider pattern in `src/payment` and can switch between Stripe and Creem via `NEXT_PUBLIC_PAYMENT_PROVIDER`. Mail and newsletter integrations use Resend, storage uses S3-compatible storage through `s3mini`, and Cloudflare deployment runs through OpenNext, Wrangler, and Hyperdrive.

## Build, Test, and Development Commands
Install dependencies with `pnpm install` and run `pnpm dev` for the local Next.js server. Use `pnpm build` to produce the optimized bundle and `pnpm start` to serve it. `pnpm lint` triggers Biome checks, while `pnpm format` applies consistent formatting. Database work flows through Drizzle: `pnpm db:generate` emits SQL from the schema, `pnpm db:migrate` applies local changes, and `pnpm db:push` syncs to remote instances. Support tooling includes `pnpm email` for the email previewer and utility scripts such as `pnpm list-users` or `pnpm fix-payments`. E2E support uses `pnpm e2e`, `pnpm e2e:ui`, and `pnpm e2e:install`.

## Coding Style & Naming Conventions
Biome (`biome.json`) enforces two-space indentation, single quotes, ES5 trailing commas, and required semicolons. Module filenames favour kebab-case (`dashboard-sidebar.tsx`), hooks use the `use-` prefix (`use-session.ts`), and utilities default to named exports. Tailwind utilities live in `src/styles`; extend tokens there instead of scattering magic values. Keep server-only code in files marked with `"use server"` and avoid pulling client hooks into those modules.

Do not change UI copy, labels, or placeholder text that the user has already customized unless explicitly instructed.

## Testing Guidelines
Automated tests are not wired into package scripts, so validate changes with `pnpm dev`, linting, and focused manual QA around auth, billing, and AI flows. When adding a runner, colocate specs with the feature using `.test.ts(x)` or `.spec.ts(x)` suffixes and document the command in your PR. Update `src/db/migrations` with fixtures whenever data changes are needed for reviewers.

E2E tests are configured through `playwright.config.ts`, with specs under `tests/e2e/specs/` and the catalog in `tests/e2e/TEST-CATALOG.md`. E2E runs against a dedicated local Next.js server on port `3100` using `.next-e2e`, sets `NEXT_PUBLIC_DEMO_WEBSITE=true` and `NEXT_PUBLIC_E2E_TEST_MODE=true`, and uses `/api/e2e/users` for `e2e-*@example.test` accounts. Run targeted specs while developing, for example `pnpm e2e -- tests/e2e/specs/auth.spec.ts`; run broader E2E checks before releases or auth/protected-route/shared-layout changes.

For UI/content-focused tasks (UI tweaks, copy updates, page structure/layout updates, and dashboard/blog/landing page work), do not run `pnpm build` by default. Suggest `pnpm build` as an optional final check and run it only if the user explicitly asks.

## Commit & Pull Request Guidelines
Use Conventional Commit style.

- New feature → `feat:`
- UI / visual change only → `ui:`
- Bug fix → `fix:`
- Documentation only → `docs:`

Keep commits small and focused. Reference issue IDs in the body when relevant. Update `env.example` whenever environment variables change.

PRs must include: short summary, testing notes (commands + results), screenshots for UI changes, and notes for docs/config updates. Highlight breaking changes early.

After each completed task with file changes, provide 1 suggested commit message in a fenced code block (copyable). Do not commit unless explicitly requested.

- When generating or updating task execution prompts, follow `docs/generate-task.md` exactly.
- A commit instruction inside a generated prompt applies to the future execution of that prompt; it does not authorize committing during the current documentation-editing task.
- Do not remove or weaken generated commit instructions merely because the current task does not authorize an immediate commit.

## Configuration & Secrets
Copy `env.example` to `.env` before running commands. Store production credentials with your deployment provider and never commit secrets. Use scoped API keys for `opennextjs-cloudflare` or `wrangler`, rotate keys tied to providers in `src/ai`, and remove temporary debugging logs before merging.

## Global Encoding Rules

- This rule is global for the whole repository, not only changelog files.
- Always write text files with UTF-8 encoding.
- In PowerShell, always specify encoding explicitly when writing files:
  - `Set-Content -Encoding utf8`
  - `Out-File -Encoding utf8`
- Do not run nested shell pipelines that execute another `powershell -Command` block for Chinese/multilingual content generation.
- After writing any Chinese or multilingual content, verify file output:
  - `Get-Content <file> | Select-Object -First 50`
  - Confirm there is no garbled text (`??`, mojibake, broken symbols).

## Question Format Requirements

- Number every question (`1, 2, 3...`).
- Give 2-4 options per question (`A/B/C/D`).
- For each question, include:
  - `Recommended: X`
  - `Reason: <one short sentence>`
- Start with answer instructions:
  - `Reply with letters in order, e.g. ACB = 1A 2C 3B.`
  - If fewer letters are provided, use recommended options for the rest (unless user says otherwise).
- Also accept explicit form: `1A, 2C, 3B`.
