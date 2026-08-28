---
name: security-review
description: Perform a focused security audit on PRs touching IAM policies, networking, security groups, authentication, or secrets. Use when a security review is explicitly requested, or when changes involve permissions, network exposure, or credential handling.
---

## When to Activate

This skill goes deeper than the security section in pr-review. Use it when:
- A PR modifies IAM policies, roles, or permission boundaries
- Security groups or network ACLs are added/modified
- Authentication or authorization logic changes
- Secrets, credentials, or API keys may be exposed
- A reviewer explicitly requests a security-focused review

## Before Asking the User

Search for answers in official documentation first:
- AWS IAM docs for policy evaluation logic
- Terraform provider docs for resource behavior
- Repo's existing IAM patterns for established conventions
- AWS security best practices for the relevant service

## Review Process

### 1. Run Secrets Detection

Run gitleaks against the PR diff:

```
scripts/scan-secrets.sh
```

This scans the current branch diff for leaked secrets, API keys, tokens, and credentials.

### 2. IAM Policy Analysis

For every IAM policy in the diff:

- **Actions:** Are they scoped to specific actions or using `*`?
- **Resources:** Are they scoped to specific ARNs or using `*`?
- **Conditions:** Are there conditions restricting when the policy applies?
- **Effect:** Any explicit Denys that might be overridden elsewhere?
- **Trust policies:** Who/what can assume this role? Is the principal scoped tightly?

See `references/iam-anti-patterns.md` for common over-permissive patterns and their fixes.

### 3. Network Exposure Check

For security group and network changes:

- Is `0.0.0.0/0` used on any ingress rule? Flag immediately.
- Are ports scoped to what the service actually needs?
- Are CIDR ranges appropriate for the environment?
- Are egress rules unnecessarily broad?

See `references/sg-baseline.md` for acceptable ports/CIDRs per environment.

### 4. Secrets & Credential Handling

- Are secrets fetched at runtime (Vault, SSM, Secrets Manager) or hardcoded?
- Are sensitive Terraform outputs marked `sensitive = true`?
- Are credentials passed via environment variables rather than command-line arguments?
- Are secret paths explicitly enumerated rather than wildcarded?
- Is access logging enabled on storage containing sensitive data?

### 5. Blast Radius Assessment

- What's the worst case if this policy is exploited?
- Can this role pivot to other accounts or services?
- Is there a break-glass procedure if this needs to be revoked quickly?

## Response Format

```
## Security Review

**Scope:** [IAM / Networking / Auth / Secrets / Mixed]
**Risk Level:** [low / medium / high / critical]
**Blast Radius:** [single service / account-wide / cross-account]

### 🔴 Security Blockers
- [specific findings with remediation]

### 🟡 Security Warnings
- [items that increase risk but aren't immediately exploitable]

### 🟢 Hardening Suggestions
- [defense-in-depth improvements]

### ✅ Security Positives
- [good practices observed]

### Least-Privilege Recommendation
[Suggest a scoped-down policy using assets/iam-policy-template.json as a starting point]
```

## Principles

- Assume breach: review as if an attacker will find any weakness
- Least privilege is the default — burden of proof is on the permission, not the restriction
- Temporary permissions become permanent — flag anything "we'll scope down later"
- Network exposure is harder to undo than IAM — treat SG changes with extra scrutiny
