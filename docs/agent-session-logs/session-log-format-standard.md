# Agent session evidence format

Create one redacted Markdown Session Evidence Record for every agent session in this directory.

## Filename

```text
YYYYMMDDTHHMMSSZ.<ASURITE>.<agent-model>.<short-title>.md
```

Use UTC and lowercase filesystem-safe tokens. Example:

```text
20260902T231500Z.ndrollin.gpt-5-6-sol.health-endpoint.md
```

## Required content

Each record identifies the issue and pull request, accountable human, agent/model, Pairing Mode, Delivery Lane, UTC start/end, authorized scope, outcome, changed interfaces, validation results, review findings/disposition, human interventions, failures/recovery, and deviations/follow-up.

Records summarize evidence; they do not contain raw chat transcripts. Never include credentials, secrets, sensitive prompts or model responses, uploads, regulated or controlled data, or unnecessary personal information. Use category redactions such as `[REDACTED: API key]` when a diagnostic fact must be retained.

The complete template, measurement guidance, ticket-close evidence, and retrospective cadence are defined in [the evidence and retrospective standard](../asdlc/evidence-and-retrospective.md).
