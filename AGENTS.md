# Agent Instructions

## Core Principles

1. **Agent-First** — Delegate to specialized agents for domain tasks
2. **Test-Driven** — Write tests before implementation; cover confirmed seams qualitatively, not to a percentage
3. **Security-First** — Never compromise on security; validate all inputs
4. **Immutability** — Always create new objects, never mutate existing ones
5. **Plan Before Execute** — Plan complex features before writing code

## Issue tracker

Issues are tracked in GitHub Issues for this repository. See `docs/agents/issue-tracker.md`.

## Triage labels

Triage uses five canonical skill labels. See `docs/agents/triage-labels.md`.

## Domain docs

This repository uses a single-context domain documentation layout. See `docs/agents/domain.md`.

## Available Agents

| Agent                | Purpose                           | When to Use                       |
| -------------------- | --------------------------------- | --------------------------------- |
| planner              | Implementation planning           | Complex features, refactoring     |
| architect            | System design and scalability     | Architectural decisions           |
| tdd-guide            | Test-driven development           | New features, bug fixes           |
| code-reviewer        | Code quality and maintainability  | After writing/modifying code      |
| security-reviewer    | Vulnerability detection           | Before commits, sensitive code    |
| build-error-resolver | Fix build/type errors             | When build fails                  |
| e2e-runner           | End-to-end Playwright testing     | Critical user flows               |
| doc-updater          | Documentation and codemaps        | Updating docs                     |
| docs-lookup          | Documentation lookup via Context7 | API/docs questions                |
| database-reviewer    | PostgreSQL specialist             | Schema design, query optimization |
| python-reviewer      | Python code review                | Python projects                   |
| typescript-reviewer  | TypeScript/JavaScript code review | TypeScript/JavaScript projects    |

## Agent Orchestration

Use agents proactively without user prompt:

- Complex feature requests → **planner**
- Code just written/modified → **code-reviewer**
- Bug fix or new feature → **tdd-guide**
- Architectural decision → **architect**
- Security-sensitive code → **security-reviewer**

Use parallel execution for independent operations — launch multiple agents simultaneously.

## Security Guidelines

**Before ANY commit:**

- No hardcoded secrets (API keys, passwords, tokens)
- All user inputs validated
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitized HTML)
- CSRF protection enabled
- Authentication/authorization verified
- Rate limiting on all endpoints
- Error messages don't leak sensitive data

**Secret management:** NEVER hardcode secrets. Use environment variables or a secret manager. Validate required secrets at startup. Rotate any exposed secrets immediately.

**If security issue found:** STOP → use security-reviewer agent → fix CRITICAL issues → rotate exposed secrets → review codebase for similar issues.

## Coding Style

**Immutability (CRITICAL):** Always create new objects, never mutate. Return new copies with changes applied.

**File organization:** Many small files over few large ones. 200-400 lines typical, 800 max. Organize by feature/domain, not by type. High cohesion, low coupling.

**Error handling:** Handle errors at every level. Provide user-friendly messages in UI code. Log detailed context server-side. Never silently swallow errors.

**Input validation:** Validate all user input at system boundaries. Use schema-based validation. Fail fast with clear messages. Never trust external data.

**Code quality checklist:**

- Functions small (<50 lines), files focused (<800 lines)
- No deep nesting (>4 levels)
- Proper error handling, no hardcoded values
- Readable, well-named identifiers

## Testing Requirements

**Coverage bar:** Judged qualitatively at confirmed seams, not as a percentage. Across every confirmed seam, exercise the happy path, error and failure modes, and boundary conditions. See the `testing` steering and the `tdd` skill.

Test types, selected by feature risk:

1. **Unit** — functions, utilities, components (`pytest`; React Testing Library)
2. **Integration / contract** — FastAPI endpoints, database access, backend↔frontend contracts (`pytest`)
3. **E2E** — critical user journeys (Playwright)

**TDD loop (mandatory):** Write the failing test first (RED), implement to pass it (GREEN), then refactor. See the `tdd` skill.

Troubleshoot failures: check test isolation → verify mocks → fix implementation (change a test only when it encodes the wrong behavior).

## Development Workflow

1. **Plan** — Use planner agent, identify dependencies and risks, break into phases
2. **TDD** — Use tdd-guide agent, write tests first, implement, refactor
3. **Review** — Use code-reviewer agent immediately, address CRITICAL/HIGH issues
4. **Capture knowledge in the right place**
   - Personal debugging notes, preferences, and temporary context → auto memory
   - Team/project knowledge (architecture decisions, API changes, runbooks) → the project's existing docs structure
   - If the current task already produces the relevant docs or code comments, do not duplicate the same information elsewhere
   - If there is no obvious project doc location, ask before creating a new top-level file
5. **Commit** — Conventional commits format, comprehensive PR summaries

## Workflow Surface Policy

- `skills/` is the canonical workflow surface.
- New workflow contributions should land in `skills/` first.
- `commands/` is a legacy slash-entry compatibility surface and should only be added or updated when a shim is still required for migration or cross-harness parity.

## Git Workflow

**Commit format:** `<type>: <description>` — Types: feat, fix, refactor, docs, test, chore, perf, ci

**PR workflow:** Analyze full commit history → draft comprehensive summary → include test plan → push with `-u` flag.

## Architecture Patterns

**API response format:** Consistent envelope with success indicator, data payload, error message, and pagination metadata.

**Repository pattern:** Encapsulate data access behind standard interface (findAll, findById, create, update, delete). Business logic depends on abstract interface, not storage mechanism.

**Skeleton projects:** Search for battle-tested templates, evaluate with parallel agents (security, extensibility, relevance), clone best match, iterate within proven structure.

## Performance

**Context management:** Avoid last 20% of context window for large refactoring and multi-file features. Lower-sensitivity tasks (single edits, docs, simple fixes) tolerate higher utilization.

**Build troubleshooting:** Use build-error-resolver agent → analyze errors → fix incrementally → verify after each fix.

## Project Structure

```
agents/          — Specialized subagents
skills/          — Workflow skills and domain knowledge
steering/        — Steering rules
```

## Success Metrics

- All tests pass; every confirmed seam is covered
- No security vulnerabilities
- Code is readable and maintainable
- Performance is acceptable
- User requirements are met
