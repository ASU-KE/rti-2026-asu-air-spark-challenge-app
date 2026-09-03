---
name: security-review
description: Focused security audit on PRs touching authentication, authorization, secrets, input handling, GCP IAM, or GKE networking. Use when a security review is explicitly requested, or when changes involve permissions, network exposure, or credential handling.
---

## When to Activate

This skill goes deeper than the security lens in pr-review. Use it when a PR:
- Changes authentication or authorization (FastAPI auth dependencies, JWT/session handling, React route or action guards)
- Handles secrets, credentials, or API keys
- Adds or changes GCP IAM roles, bindings, or service accounts
- Modifies GKE networking, VPC firewall rules, or Ingress/Gateway exposure
- Touches input boundaries (request bodies, query params, uploads) or database queries
- A reviewer explicitly requests a security-focused review

## Before Asking the User

Search for answers in official documentation first:
- Google Cloud IAM docs for role/binding evaluation and Workload Identity Federation
- FastAPI security docs (OAuth2, dependencies) and OWASP references for app-layer issues
- The repo's existing auth, secrets, and IAM patterns
- The GKE hardening guide for cluster and workload settings

## Review Process

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

- Are secrets fetched at runtime from Secret Manager (or injected env), never hardcoded or committed?
- Is Workload Identity Federation used for GKE workloads and external CI/CD, instead of long-lived service-account keys?
- Are required secrets validated at startup and kept out of logs and error responses?

### 5. GCP IAM Least Privilege

For every IAM role or binding in the diff:

- **Roles:** A predefined or custom role scoped to need — not a primitive `roles/owner`, `roles/editor`, or `roles/viewer`?
- **Members:** A dedicated least-privilege service account per workload — not the default compute SA or a user account?
- **Scope:** Granted at the narrowest resource (bucket, dataset, topic, secret) rather than the whole project?
- **Keys:** No exported service-account keys where Workload Identity Federation would work?
- **`iam.serviceAccountUser` / `actAs`:** Granted only where impersonation is genuinely required?

See `references/iam-anti-patterns.md` for common over-permissive patterns and their fixes.

### 6. GKE & Network Exposure

- Is anything exposed publicly that shouldn't be — a `LoadBalancer` Service or an Ingress without authentication?
- Do VPC firewall rules avoid `0.0.0.0/0` except on 443 behind a managed load balancer? SSH and database ports are never world-open.
- Are databases reachable only privately (Private Service Connect or authorized networks), never via public IP?
- Are workloads least-privileged: non-root, read-only root filesystem, dropped capabilities, and a `NetworkPolicy` in place?

See `references/network-baseline.md` for acceptable ports, sources, and per-environment rules.

### 7. Blast Radius Assessment

- What is the worst case if this route, credential, or role is abused?
- Can the identity pivot to other services or projects?
- Is there a fast revoke or rollback path — rotate the secret, remove the binding, disable the route?

## Response Format

```
## Security Review

**Scope:** [Auth / Input / Secrets / IAM / Network / Mixed]
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

### Least-Privilege Recommendation
[Suggest a scoped-down role/binding using assets/iam-binding-template.tf as a starting point]
```

## Principles

- Assume breach: review as if an attacker will find any weakness
- Least privilege is the default — burden of proof is on the permission, not the restriction
- Temporary permissions become permanent — flag anything "we'll scope down later"
- Server-side is the only trust boundary — never rely on the client (React) to enforce security
- Network exposure is harder to undo than a role change — treat firewall and Ingress changes with extra scrutiny
