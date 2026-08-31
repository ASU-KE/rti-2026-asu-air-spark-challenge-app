# Human-Agent Pair Programming workflow

## Purpose

This workflow operationalizes the Enterprise-Informed aSDLC Pilot while keeping a named human accountable for every agent-assisted change. GitHub Issues is the system of record, and each change moves through one visible ticket, branch, pull request, review, and evidence chain.

## Roles and authority

The **Human Partner** owns intent, authorization, decisions, and outcome. The **Agent Partner** performs bounded work and reports evidence. In Interactive Pairing they collaborate synchronously; in Delegated Pairing the agent works asynchronously within an approved ticket and returns a structured handoff.

Authority levels:

1. **Autonomous Work** — read-only investigation, approved research, drafting, and non-mutating validation.
2. **Ticket-Authorized Work** — edit, test, create a short-lived branch, commit, and open or update a pull request within an assigned ready ticket.
3. **Human-Gated Action** — merge, deploy, elevated credentials, destructive operations, live-state changes, risk acceptance, and product-scope changes.

A stop-work concern involving security, privacy, compliance, or Responsible AI supersedes schedule pressure.

## Lanes

- **Standard Lane** uses full specification, agreed testing seams, normal ticket sizing, and complete documentation.
- **Event-Critical Lane** is approved by Nathan when ceremony or scope must shrink to protect submission.

Both lanes use identical implementation, testing, integrated review, PR review, security review, human approval, traceability, and merge controls. Lane changes alter ceremony and priority—not assurance.

## Definition of Ready

A ticket is `ready-for-agent` only when it states:

- User or operational outcome and acceptance criteria.
- Accountable human and delivery lane.
- Scope boundaries and out-of-scope items.
- Dependencies and blocking edges.
- Affected interfaces and approved behavioral testing seam.
- Data classification and security/Responsible AI considerations.
- Validation commands or observable completion evidence.
- Deployment, migration, and rollback implications when applicable.

## Claim and branch

1. Assign the accountable human.
2. Add a claim comment containing pairing mode, agent/model, session identifier, and planned branch.
3. Confirm no other active owner exists.
4. Create one short-lived branch named `<type>/<issue-number>-<short-slug>` from current `main`.
5. Keep the issue updated when the lane, scope, blocker, or owner changes.

## Delivery loop

1. **Orient:** read the issue, `CONTEXT.md`, applicable ADRs, and affected interfaces. Restate uncertainty before coding.
2. **Plan a tracer bullet:** choose the smallest independently demonstrable vertical behavior.
3. **Agree the seam:** identify the public interface where behavior will be observed. Product behavior changes use red → green TDD at that seam.
4. **Implement:** make one coherent change, preserve the Event Critical Path, and keep secrets and sensitive data outside the repository and logs.
5. **Validate continuously:** run targeted tests and typechecks; run the complete affected suite before review.
6. **Preflight review:** invoke `/code-review` against a fixed point. The integrated workflow always includes Standards, Spec, PR quality/risk, security, provider layers, independent cross-model review, cross-validation, and synthesis.
7. **Open/update the PR:** link the issue; include scope, evidence, risks, observability, rollback, deviations, and Session Evidence Records.
8. **PR gate:** run the same integrated review on the pull request and obtain one approval from another human. The author may not self-approve.
9. **Resolve findings:** fix Blocker/Critical/High findings; fix Medium findings or record an accepted linked follow-up; Low findings are nonblocking. Adjudicate disputed blocking findings.
10. **Merge:** after required checks, approvals, current-branch confirmation, and resolved conversations, a human squash-merges to `main`.
11. **Close:** add ticket-close evidence and update linked follow-ups, the Standards Backlog, and applicable docs.

## Definition of Done

A ticket is done when:

- Acceptance criteria are demonstrated through public interfaces.
- Required unit, integration, contract, E2E, regression, security, and failure-path tests pass according to risk.
- Lint, typecheck, build, scans, and relevant manifest/container checks pass.
- Integrated review disposition satisfies finding policy.
- Another human approved the pull request.
- Documentation, OpenAPI/contracts, operational notes, observability, and rollback guidance are current.
- Session evidence and ticket-close evidence are linked.
- Deferred work is represented by accepted linked issues.
- The merged commit is traceable to the issue and PR.

## Handoff format

A Delegated Pairing handoff records:

- Issue, branch, commit or working-tree state, and accountable human.
- Completed behavior and remaining acceptance criteria.
- Files/interfaces changed.
- Commands run and exact results.
- Review findings and disposition.
- Risks, blockers, assumptions, and deviations.
- Recommended next action and any required Human-Gated Action.

## Collision and recovery

Only one active owner may modify a ticket. When overlapping interfaces are unavoidable, create explicit blocking edges and sequence the changes. Agents never rewrite another partner's uncommitted work, bypass hooks, force-push, or silently broaden scope. Failed delegated work returns a handoff that preserves diagnostics and leaves the repository recoverable.
