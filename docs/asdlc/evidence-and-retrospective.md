# Evidence and retrospective standard

## Session Evidence Records

Create one redacted Markdown record for every agent session under `docs/agent-session-logs/`:

```text
YYYYMMDDTHHMMSSZ.<ASURITE>.<agent-model>.<short-title>.md
```

Use UTC, lowercase filesystem-safe tokens, and a short hyphenated title. Example:

```text
20260902T231500Z.ndrollin.gpt-5-6-sol.health-endpoint.md
```

A Session Evidence Record contains:

```markdown
# <Session title>

- Issue: #<number>
- Pull request: #<number or N/A>
- Accountable human: <name and ASURITE>
- Agent/model: <agent and exact model when available>
- Pairing mode: Interactive Pairing | Delegated Pairing
- Delivery lane: Standard Lane | Event-Critical Lane
- Started: <UTC timestamp>
- Ended: <UTC timestamp>

## Authorized scope

<ticket boundary and Human-Gated Actions excluded>

## Outcome

<observable result and acceptance criteria status>

## Changes

<interfaces/files changed; no raw transcript>

## Validation

<commands/checks and exact outcomes>

## Review

<review stages, findings, disposition, and confidence degradation>

## Human interventions

<decisions, corrections, approvals, and estimated effort>

## Failures and recovery

<failed attempts, diagnostics, and recovery>

## Deviations and follow-up

<process deviations, accepted risk, linked issues, Standards Backlog items>
```

## Redaction rules

Evidence records contain summaries and references, not chat transcripts. Exclude:

- API keys, tokens, credentials, cookies, and private keys.
- Sensitive prompts, model responses, uploads, student/health/research records, or controlled data.
- Unnecessary personal information.
- Secret values copied from logs or command output.
- Internal service endpoints or identifiers that are not approved for repository disclosure.

Replace sensitive material with a category such as `[REDACTED: API key]` and preserve only the minimum diagnostic fact.

## Ticket-close evidence

Before closing a ticket, add a concise issue comment with:

- Delivered behavior and acceptance-criteria result.
- Pull request and merged commit.
- Validation and integrated-review links.
- Session Evidence Record links.
- Deviations, accepted risk, or linked follow-ups.
- Demonstration or operational evidence where applicable.

## Pilot measures

The pilot records evidence sufficient to compare human-agent delivery without claiming causal certainty from a single event:

- Human and agent elapsed effort.
- Time from ready claim to pull request and merge.
- Validation failures before and after review.
- Findings by source, severity, validity, and disposition.
- Human interventions and scope corrections.
- Rework, rollback, and escaped-defect events.
- Process deviations and their Event Critical Path rationale.
- Documentation/operational completeness at ticket close.

Never optimize work to improve a metric at the expense of product safety or submission.

## Retrospective cadence

### Ticket closure

Record one short note: what accelerated delivery, what created rework, what assurance caught, and what should change next time.

### Post-submission debrief

Immediately after submission, capture timeline, unresolved risks, demo readiness, and evidence that may be lost during final preparation.

### Post-ceremony retrospective

After the closing ceremony, discuss application outcome, team collaboration, Human-Agent Pair Programming, integrated review, platform reliability, and presentation feedback.

### Full pilot evaluation

Within three business days, publish an evaluation that:

1. Separates observed facts from interpretation.
2. Compares planned and actual workflow.
3. Identifies which practices were effective, ineffective, or untested.
4. Records security, reliability, Responsible AI, and technical-debt outcomes.
5. Proposes Standards Backlog items with owner, evidence, priority, and next validation step.
6. Recommends whether each practice should be adopted, revised, tested again, or rejected.

## Standards Backlog

A Standards Backlog item is evidence-backed follow-up work, not a hidden exception. Each item includes the observed gap, affected standard or workflow, impact, evidence links, proposed experiment or remediation, accountable owner, and target date. Later RTO review decides whether pilot practices become engineering standards.
