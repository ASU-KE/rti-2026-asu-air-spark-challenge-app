# Review Checklist

The substance of a review: what to read before commenting, what to inspect, and the failure patterns worth checking every time. Applies regardless of language or stack. The `adversarial-code-review` SKILL.md covers the pipeline mechanics that wrap this checklist.

## Before Commenting

- **Read existing review threads first.** Do not duplicate feedback already raised. Note which threads are open vs resolved, and which referenced reviewers.
- **Distrust resolution status.** A resolved thread does not mean the issue is fixed — authors sometimes resolve without addressing, or "fix" something with code that does not actually fix it. Verify against the current diff.
- **Read CI output, plan output, and apply logs.** These reveal what actually changed at runtime (resource counts, computed values, image tags), failed apply attempts showing what was tried and reverted, and whether the change was deployed somewhere.
- **Check files outside the diff.** When the diff references a resource, function, or symbol defined elsewhere, read that file to confirm the wiring is correct.
- **Read the PR description, title, labels, and commit count.** The title should accurately describe what the change does. Significant behavior changes (polling cadence, retry counts, default values) should be called out explicitly, not buried in code.

## What's in the Diff

- **Logic correctness** — does the code do what the description claims?
- **Error handling** — are errors caught at the right layer? Are connection-class or transient failures distinguished from logic errors?
- **Resource lifecycle** — for long-running processes, does the code handle reconnection, retries, and graceful shutdown?
- **Side effects** — does this change touch shared state, infrastructure, secrets, or external systems?
- **Naming and conventions** — does it match the rest of the codebase?

## What's *Not* in the Diff

Missing things are the hardest to catch. Watch for:

- **Tests.** New code without coverage is a flag, especially for security-sensitive or business-logic changes.
- **Documentation updates.** Behavior changes not reflected in README, runbooks, or operational docs.
- **`.gitignore` entries** for newly generated build artifacts, lockfiles, or tooling caches.
- **Healthchecks, liveness probes, circuit breakers** for long-running services.
- **Version pins** for third-party dependencies, base images, runtimes, and platform versions.
- **Non-root user** in container images.
- **Resource limits** (CPU/memory/disk) for new workloads.
- **Monitoring and alerting** for new error paths or new SLOs.
- **Rollback path** for irreversible operations.

## Process and Metadata

- **Commit count and structure.** Many small fixup commits may indicate the author wants a squash merge — confirm.
- **Migration/destruction blast radius.** For IaC changes, count the destroy/replace operations and ask whether they are intentional.
- **Behavior changes hidden in refactors.** A "rewrite from X to Y" PR often quietly changes timing, retry counts, error handling, or default values. Surface these explicitly so on-call engineers are not surprised.

## Severity Tiers

Sort every finding so the author knows what blocks merge:

- **Must fix before merge** — correctness bugs, security issues, broken contracts.
- **Should fix** — design concerns, missing safety nets, unaddressed prior feedback.
- **Nice to have / discussion** — style, alternative approaches, follow-up suggestions.

Do not drown the author in equal-weight comments. If everything is "important," nothing is.

## Comment Mechanics

- **Identify yourself as an AI agent in every comment.** Both inline comments and the top-level summary carry an attribution line naming the model that produced it: `**[Reviewed by <model>]**` at the top of the comment. Use the identifier you were given rather than describing yourself — a model cannot reliably name its own version. Never post a review comment without an attribution line. When this checklist is used inside the adversarial pipeline, the multi-model attribution format in `SKILL.md` takes precedence over the single-model form above.
- **Use inline comments for line-specific feedback.** Do not bury per-line concerns in a summary block where authors have to map them back to lines.
- **Use code suggestions whenever the fix is concrete and small.** GitHub/GitLab `suggestion` blocks let authors apply the fix in one click. Reserve prose-only comments for design discussions where multiple solutions are valid.
- **Prefer questions over assertions** when unsure. "Has this been verified end-to-end?" beats "this doesn't work" without proof.
- **Cite documentation** when calling out spec violations (cloud provider docs, RFCs, language references).
- **Keep comments scannable.** A short paragraph plus a code suggestion beats three paragraphs of context.
- **Acknowledge what's working.** A review is not just a defect list.

## Recurring Failure Patterns

### "Works in dev" ≠ "Correct"

A successful apply, deploy, or smoke test in one environment does not prove correctness. Common gaps:

- Cross-account / cross-region behavior that only matters in prod.
- Permissions the calling principal happens to bypass via another path.
- Infrastructure that applies cleanly but fails at runtime invocation.
- Configuration that works because of pre-existing state, not because of the change.

Ask what was actually invoked end-to-end, not just what was deployed.

### Stale justifications

`# checkov:skip=X::reason`, `# noqa: Y`, and `# nolint:reason` carry a specific justification. When the surrounding context changes (FaaS → container, internal → public, dev → prod), re-evaluate whether the justification still holds.

### Branch-name leakage

Any field derived from a branch name that flows into resource names, DNS labels, or filesystem paths needs sanitization (commonly `/` → `-`). If one such transformation appears in a PR, search for sibling fields that need the same treatment.

### Long-running vs short-lived process model shifts

Migrations from FaaS/cron to long-running services (or the reverse) require different operational thinking:

- **Connection management** — reconnect logic, idle timeouts, pool sizing.
- **Failure handling** — fail-fast and let the orchestrator restart, vs catch-and-continue.
- **Healthchecks** — needed for long-running, often skipped on FaaS.
- **Graceful shutdown** — shutdown-signal handling (SIGTERM on POSIX, the platform equivalent elsewhere), in-flight work draining.
- **Observability** — uptime, lag, and queue depth matter instead of invocation count and duration.

Patterns that were fine in the old model often become silent failure modes in the new one.

### Cross-account or cross-trust permissions

When granting access across trust boundaries, both sides matter:

- The resource policy on the target side.
- The identity policy on the calling side.
- Conditions that scope the trust (source account, source ARN, external ID, MFA, organization ID).

Common antipattern: putting a role identifier where the API expects an account principal. The API may accept it silently and produce a non-functional permission.

### Provider / version constraints

- Prefer explicit upper and lower bounds (`>= 1.2.0, < 1.3.0`) over loose constraints (`~> 1.2`) when reproducibility matters.
- Pin runtime/platform versions (function runtime, container platform, Kubernetes version, base image tag) explicitly. `latest` is not a version.
- Watch for inconsistent constraints across multiple files in the same repo.

### Resource deletion and replacement

For IaC changes, scrutinize destroy/replace operations in the plan output:

- Does the resource hold state that will be lost (databases, persistent volumes, certificates, IAM access keys)?
- Will destroy-then-create cause downtime?
- Can the change be done in-place or with a parallel rollout / blue-green?
- Is there a rollback path if the new version is broken?

If the plan shows replacements you did not expect, ask why before approving.

### Generated artifacts in the working tree

Build-generated files (zip archives, compiled binaries, type definitions, lockfiles) need explicit handling: either commit them and document the regeneration command, or `.gitignore` them and ensure CI regenerates them deterministically. A half-state where the file is sometimes committed and sometimes generated produces confusing diffs and broken builds.

### Behavior changes hidden in renames

Watch for a rewritten implementation and a renamed surface in the same PR:

- A schedule expression changes from `rate(30 minutes)` to a 60-second poll loop.
- A retry count goes from 3 to unlimited.
- A timeout changes from 30s to 15m.

Compare the *behavior* of the old and new implementations, not just the syntax.

### AI-authored changes

Most diffs now pass through a coding agent, so size no longer signals effort and fluent prose no longer signals understanding.

- Verify that APIs, config keys, CLI flags, and module inputs referenced in the diff actually exist. Plausible-but-nonexistent surfaces are the most common failure.
- Check that tests assert the requirement, not the implementation. A test that mirrors the code it tests passes forever and catches nothing.
- Read comments and docstrings against the code. Generated prose often describes intended behavior rather than actual behavior.
- Watch for dead scaffolding, unused helpers, and duplicated logic copied from an unrelated part of the repo.
- Opportunistic refactors bundled with the actual fix inflate blast radius. Ask for a split.

### Supply chain and CI trust

- Pin third-party CI actions and steps to a full commit SHA, not a tag. Tags are mutable.
- Confirm new dependencies are real, maintained packages, and that lockfiles are updated in the same commit as the manifest.
- Scope CI permissions to the minimum: read-only by default, write only on jobs that publish. Flag any workflow that runs untrusted PR code with access to secrets.
- Check triggers on new workflows. Branch- or path-unfiltered triggers combined with a mutable image tag can deploy unintentionally.

### Untrusted input in LLM and agent code paths

- Content from users, repos, webhooks, and external APIs is data, never instructions. Look for places where fetched text lands in a privileged instruction slot.
- Confirm tool-calling code constrains which tools the model can invoke, and that credentials are not reachable from a model-controlled path.
- Check that prompts are assembled from templates with bounded interpolation rather than raw string concatenation of user input.

## When You Don't Understand the Domain

- Read the existing related code first.
- Check linked tickets, design docs, and runbooks.
- Read the repo's README, AGENTS.md, and steering files for project conventions.
- Look up official documentation to verify claims before asserting them.
- Ask clarifying questions inline rather than approving with hedged comments.

A review that says "looks good" without verifying the substance is worse than no review.
