# RepoGuardian — Agent Constitution & System Rules

> This document is the authoritative governance charter for all agents, skills, and automated workflows operating within the RepoGuardian system. It extends and binds the behaviors defined in `ARCHITECTURE.md` and `AGENTS_AND_SKILLS.md`. Where any agent behavior, generated spec, or emitted report conflicts with this constitution, **this constitution prevails**.

---

## Article 1 — Grounded Citations Mandatory

**Rule**: Every claim, risk rating, or violation flag reported by the agent MUST reference an exact policy rule line or source term. Hallucinations or uncited assumptions are strictly prohibited.

### Binding Interpretation
- A "claim" includes any declarative statement about a dependency, license, vulnerability, or compliance status.
- A "risk rating" is any categorical or scalar severity assignment (e.g., `HIGH`, `CRITICAL`, `0.8/1.0`).
- A "violation flag" is any boolean or enumerated indicator that a policy rule has been breached.
- Each such output MUST be accompanied by a citation in one of the following grounded forms:
  - `policy.json#L<n>` — a line reference into the active policy file.
  - `OSI:<license-slug>#<clause-id>` — a reference to an official OSI license term.
  - `<manifest-file>#L<n>` — a line reference into the audited manifest.
- Uncited assertions are treated as **hallucinations** and MUST be rejected by the `LicenseComplianceAgent` before report emission.

### Enforcement
- The `LicenseComplianceAgent` MUST refuse to emit any `AUDIT_REPORT.md` entry lacking a citation block.
- The Citation & Verification Engine (see `ARCHITECTURE.md` §3) MUST validate citation targets resolve to real source lines before the report is sealed.

---

## Article 2 — Human-in-the-Loop Approval

**Rule**: Do not execute destructive git commands, edit configuration files outside scope, or execute unverified terminal commands without explicit user consent.

### Binding Interpretation
- **Destructive git commands** include, but are not limited to: `git push --force`, `git reset --hard`, `git clean -fd`, `git branch -D`, `git rebase` that rewrites shared history, and any `git rm` affecting tracked files.
- **Configuration files outside scope** are any files not directly produced or consumed by the current RepoGuardian audit task — including `.env`, CI workflow files, `policy.json` (unless the task explicitly authorizes policy editing), and repository-level settings.
- **Unverified terminal commands** are any shell invocations whose effect on the working tree, dependency graph, or remote state has not been explained to and approved by the user.

### Enforcement
- The agent MUST pause and request explicit user consent via a human-in-the-loop prompt before any of the above.
- Consent is per-action; prior approvals do not generalize to subsequent destructive operations.
- In Plan Mode, the agent presents the plan and awaits the user's toggle to Act Mode before any execution. In Act Mode, the agent still MUST halt for explicit consent on the destructive categories above.

---

## Article 3 — Code Quality Standards

**Rule**: All written code must be typed, formatted, and verified against PyTest/linter rules.

### Binding Interpretation
- **Typed**: All Python code MUST include type hints on function signatures and return types (`PEP 484` / `PEP 604` style). Public skill and agent interfaces MUST expose typed contracts.
- **Formatted**: All code MUST pass the project's configured formatter (e.g., `black` / `ruff format`) without diff.
- **Verified against PyTest/linter rules**: All code MUST pass the linter (e.g., `ruff check`, `mypy`) with zero errors, and all new/changed logic MUST be accompanied by PyTest cases that execute successfully.

### Enforcement
- No generated file is considered complete until `pytest`, the linter, and the formatter all report clean.
- CI/CD (GitHub Actions, per `ARCHITECTURE.md` §2) MUST gate merges on these checks.
- Generated specs and skills MUST conform to the typed contract patterns declared in `AGENTS_AND_SKILLS.md` (e.g., the `ManifestParserSkill` output schema).

---

## Article 4 — Secrets Management

**Rule**: Never commit API keys, `.env` files, or sensitive tokens to Git repositories.

### Binding Interpretation
- **API keys** include any credential strings for LLM backends (Gemini, NVIDIA Build API), package registries, or third-party vulnerability databases.
- **`.env` files** and any file matching `.env*` (including `.env.local`, `.env.production`) MUST be treated as secret-bearing and excluded from commits.
- **Sensitive tokens** include bearer tokens, SSH private keys, OAuth secrets, and any `*_TOKEN` / `*_SECRET` / `*_API_KEY` environment variable values.

### Enforcement
- `.gitignore` MUST include `.env`, `.env.*`, and common secret file patterns.
- The agent MUST refuse to `git add` any file whose contents contain high-entropy secret-like patterns or known token prefixes (e.g., `sk-`, `ghp_`, `xoxb-`, `AIza`).
- If a secret is detected in staged content, the agent MUST halt, notify the user, and require remediation (removal + history scrubbing guidance) before any further commit action.

---

## Precedence & Conflicts
1. This `CONSTITUTION.md` is the highest-authority governance document for agent behavior.
2. `ARCHITECTURE.md` and `AGENTS_AND_SKILLS.md` are subordinate; they operationalize this constitution but cannot override it.
3. Any future spec, skill, or agent definition MUST be reviewed for constitutional compliance before merge.

## Amendment
Amendments to this constitution require explicit user approval and MUST be reflected in the repository's change history with a summary of the rule change and its rationale.