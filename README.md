# RTI ASU AIR Spark Challenge 2026

Planning space and application repository for the Research Technology Infrastructure (RTI) team participating in the 2026 [ASU AIR Spark Challenge](https://asuevents.asu.edu/event/asu-air-spark-challenge).

## Outcomes

This repository supports two linked outcomes:

1. **Challenge Application** — an innovative AI-powered application for research or research operations.
2. **aSDLC Pilot** — an instrumented, Enterprise-Informed trial of agent-centric delivery practices.

The Challenge Application owns the **Event Critical Path**. Process experiments may be deferred when they threaten a valid submission; every deviation becomes pilot evidence rather than a hidden exception. The pilot is intended to identify strengths, limitations, and a Standards Backlog. It does not claim that one hackathon proves production or enterprise readiness.

## Team

- Nathan Rollins (`ndrollin`) — Challenge Lead and Mentor
- Rajashree Pailla (`rpailla1`)
- Vinay Veeramallu (`vveeram6`)

## Event gates

| Gate                                 | Date and time                           |
| ------------------------------------ | --------------------------------------- |
| Applications and team name           | August 31, 2026                         |
| Select Primary and Fallback Concepts | September 1, 2026                       |
| Challenge launch                     | September 2, 2026, 5:00–7:30 p.m.       |
| Demo and closing ceremony            | September 4, 2026, 10:00 a.m.–1:30 p.m. |

See [the preparation plan](docs/planning/challenge-preparation-plan.md) for readiness gates and contingency rules.

## Human-Agent Pair Programming

The team extends pair programming through **Human-Agent Pair Programming**:

- **Interactive Pairing** for synchronous collaboration.
- **Delegated Pairing** for bounded asynchronous work with one accountable human partner.

Agents may investigate, draft, edit, test, and prepare branches within approved ticket scope. Humans remain accountable for merge, deployment, elevated credentials, destructive operations, risk acceptance, live-state changes, and product-scope changes. See [the aSDLC workflow](docs/asdlc/workflow.md).

## Delivery and assurance

Every ticket uses the same assurance controls, whether it is in the Standard Lane or the Nathan-approved Event-Critical Lane:

1. Satisfy the Definition of Ready and claim the issue.
2. Work on one short-lived branch and one reviewable pull request.
3. Use risk-based behavioral testing at approved seams.
4. Run the integrated `/code-review` locally and on the pull request.
5. Include mandatory PR-quality and security review, including Google Cloud/GKE checks where relevant.
6. Obtain another human's approval and resolve required findings.
7. Squash merge to `main` only after required checks pass.
8. Record session evidence and ticket-close evidence.

Review routing and finding policy are defined in [review-routing.md](docs/asdlc/review-routing.md). Evidence and retrospective requirements are defined in [evidence-and-retrospective.md](docs/asdlc/evidence-and-retrospective.md).

## Planned application architecture

The neutral scaffold supports concept selection without inventing product behavior:

```text
apps/web          React + TypeScript + Vite + ASU Unity
apps/api          Node.js + TypeScript + Fastify + OpenAPI + Pino
packages/shared   Zod schemas and shared contracts
```

The workspace uses npm workspaces, Vitest, one initial deployable container, and OpenTelemetry. Product-specific contracts will be added only after the Primary Concept is selected.

The ASU Research Computing API is OpenAI-compatible at `https://openai.rc.asu.edu/v1`. API keys are managed through Voyager and must never be committed or written to logs.

## Delivery target

The approved deployment design targets:

- Google Cloud project: `asu-ke-rto-web-svcs`
- Region: `us-west4`
- Existing GKE Standard cluster: `websvcs-gke-private-dev`
- Namespace: `rti-air-spark-dev`

Cloud Build is the authoritative CI/CD system. The PR pipeline performs deterministic install, lint, typecheck, tests, scans, container build/smoke tests, and manifest validation without deployment access. The `main` pipeline repeats those controls for the merged commit, publishes an immutable image, deploys, verifies rollout and smoke tests, and rolls back a failed rollout.

Repository configuration does **not** create triggers, IAM bindings, namespaces, secrets, DNS, certificates, or other live cloud state. Those are Human-Gated Actions requiring a separate exact proposal and explicit approval.

## Observability and data safety

The scaffold integrates OpenTelemetry with Google Cloud Logging, Trace, Error Reporting, Cloud Monitoring, and Managed Service for Prometheus. Request and response bodies are not logged; known credential fields are redacted, and request/startup/shutdown errors log only an allowlisted error type and message-free stack frames with trace correlation.

Only public, synthetic, or explicitly approved data may be used by default. Regulated, sensitive, student, health, credential, and controlled research data are out of scope. Prompts, retrieved content, uploads, model output, and tool output are treated as untrusted.

## Repository guide

- [CONTEXT.md](CONTEXT.md) — canonical domain language
- [docs/adr](docs/adr) — accepted architecture decisions
- [Challenge preparation plan](docs/planning/challenge-preparation-plan.md)
- [aSDLC workflow](docs/asdlc/workflow.md)
- [Integrated review routing](docs/asdlc/review-routing.md)
- [Evidence and retrospectives](docs/asdlc/evidence-and-retrospective.md)
- [Local delivery validation](docs/runbooks/local-delivery-validation.md)
- [Deployment rehearsal and rollback](docs/runbooks/deployment-rehearsal.md)
- [Demo artifact and offline contingency](docs/runbooks/demo-contingency.md)
- [Human-gated deployment prerequisites](docs/runbooks/human-gated-deployment-prerequisites.md)
- [Google observability runbook](docs/runbooks/observability.md)
- [.kiro/skills](.kiro/skills) — active adapted agent skills
- [docs/agent-session-logs](docs/agent-session-logs) — redacted session evidence

## Local development

The application scaffold and commands are implemented in the root `package.json`. The expected workflow is:

```bash
npm ci
npm run lint
npm run typecheck
npm test
npm run build
npm run validate:delivery
npm run dev
```

Use `.env.example` as the configuration contract and keep local secrets in ignored files. Container, manifest, and Cloud Build instructions are documented with the scaffold; none of the local commands should mutate live cloud state by default.

## Decision records

- [ADR 0001 — Prioritize the Challenge Application while piloting aSDLC](docs/adr/0001-prioritize-challenge-application-while-piloting-asdlc.md)
- [ADR 0002 — Use human-accountable pair programming](docs/adr/0002-use-human-accountable-pair-programming.md)
- [ADR 0003 — Require integrated review for every pull request](docs/adr/0003-require-integrated-review-for-every-pull-request.md)
- [ADR 0004 — Use TypeScript, Cloud Build, and the existing GKE development cluster](docs/adr/0004-use-typescript-cloud-build-and-existing-gke.md)
