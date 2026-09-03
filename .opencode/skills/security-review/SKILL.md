---
name: security-review
description: Focused security audit on PRs touching authentication, authorization, secrets, input handling, or data. Use when a security review is explicitly requested, or when changes involve permissions, credential handling, or data boundaries.
---

## When to Activate

This skill goes deeper than the security lens in pr-review. Use it when a PR:
- Changes authentication or authorization (FastAPI auth dependencies, JWT/session handling, React route or action guards)
- Handles secrets, credentials, or API keys

- Touches input boundaries (request bodies, query params, uploads) or database queries
- A reviewer explicitly requests a security-focused review

## Before Asking the User

Search for answers in official documentation first:
 - FastAPI security docs (OAuth2, dependencies) and OWASP Top 10 / ASVS for app-layer issues
 - The repo's existing auth and secrets patterns

## Review Process

### Cloud Deployment Scope

> ⚠️ Cloud deployment is out of scope for the prototype (see `docs/planning/application-requirements.md`). This review covers local-only execution. If cloud deployment becomes in-scope, re-derive cloud-specific checks (IAM least privilege, network exposure).

### 1. Run Secrets Detection

Run gitleaks against the PR diff:

```
scripts/scan-secrets.sh
```

This scans the current branch diff for leaked secrets, API keys, tokens, and credentials.

### 2. Authentication & Authorization

- Are protected FastAPI routes guarded by a shared auth dependency, not ad hoc per-handler checks?
- Is authorization enforced server-side? Never trust the client or React state to gate access.
- Are tokens verified for signature, expiry, and audience, and are sessions stored in `httpOnly`, `Secure` cookies rather than `localStorage`?
- Do object-level checks prevent IDOR — one user reaching another's resource by guessing an id?

### 3. Input Handling & Injection

- Is every external input validated at the boundary with a Pydantic schema (backend) or a typed schema (frontend)?
- Are database queries built with SQLAlchemy constructs or bound parameters — never f-string or `%`-formatted SQL?
- Is user-supplied HTML sanitized? Flag `dangerouslySetInnerHTML` with untrusted input.
- Are file paths and uploads validated against path traversal, with content types and sizes bounded?

### 4. Secrets & Credential Handling

- Are secrets and credentials provided via environment variables at runtime, never hardcoded in source or committed to the repo?
- Are all required credentials validated at application startup, with a clear error if missing?
- Are secrets and credentials kept out of logs, console output, and error responses?

### 5. Blast Radius Assessment

- What is the worst case if this route, credential, or data access is abused?
- Can the identity or data access pivot to other services or data stores?
- Is there a fast revoke or rollback path — disable the route, clear the cache, or terminate the session?

## Response Format

```
## Security Review

**Scope:** [Auth / Input / Secrets / Network / Mixed]
**Risk Level:** [low / medium / high / critical]
**Blast Radius:** [single service / project-wide / cross-project]

### 🔴 Security Blockers
- [specific findings with remediation]

### 🟡 Security Warnings
- [items that increase risk but aren't immediately exploitable]

### 🟢 Hardening Suggestions
- [defense-in-depth improvements]

### ✅ Security Positives
- [good practices observed]

### Hardening recommendations
- [Specific, actionable suggestions to improve security posture]
```

## Principles

- Assume breach: review as if an attacker will find any weakness
- Least privilege is the default — burden of proof is on the permission, not the restriction
- Temporary permissions become permanent — flag anything "we'll scope down later"
- Server-side is the only trust boundary — never rely on the client (React) to enforce security
- Network exposure is harder to undo than a role change — treat firewall and Ingress changes with extra scrutiny
