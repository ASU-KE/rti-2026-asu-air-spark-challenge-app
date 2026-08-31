# Challenge preparation plan

## Objective

Prepare the team, application platform, and Human-Agent Pair Programming workflow before the ASU AIR Spark Challenge while protecting the Event Critical Path. The Challenge Application is the primary outcome; the aSDLC Pilot supplies evidence without becoming a prerequisite for submission.

The native GitHub hierarchy is rooted at [#12](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/12), with Event Preparation [#13](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/13), Concept Selection [#14](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/14), Challenge Application [#15](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/15), aSDLC Pilot [#16](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/16), and Presentation [#17](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/17) as workstream children. Workflow rehearsal [#18](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/18) remains `needs-info` until a named accountable human with ASURITE accepts it. GitHub Project inspection/creation is deferred because the current token lacks `read:project` and `project`; existing Project v2 timeline evidence makes duplicate creation unsafe.

## Fixed gates

| Date                                | Required outcome                                                           | Evidence                                                              |
| ----------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| August 31, 2026                     | All individual applications submitted; team name selected                  | Issues `#5`–`#8` and `#10` closed or updated with completion evidence |
| September 1, 2026                   | Primary and Fallback Concepts selected; scaffold and credentials rehearsed | Concept scorecard, decision comment, readiness checklist              |
| September 2, 2026 before 5:00 p.m.  | Team, tools, and demo skeleton ready                                       | Rehearsal ticket complete                                             |
| September 3, 2026 before 11:59 p.m. | Valid submission uploaded                                                  | Submission receipt and immutable release reference                    |
| September 4, 2026 before 10:00 a.m. | Demo path rehearsed and fallback available                                 | Demo checklist and presenter confirmation                             |
| Within three business days          | Full aSDLC Pilot evaluation complete                                       | Retrospective and Standards Backlog updates                           |

## Workstreams

### Event Preparation

- Confirm each member's application and challenge access.
- Select a team name by August 31.
- Confirm Presenter before the demo.
- Verify access to GitHub, Kiro CLI, the ASU AIR/Research Computing API, Google Cloud, Cloud Build, Artifact Registry, and the existing development cluster.
- Complete one end-to-end workflow rehearsal without making unapproved live changes.
- Prepare communication, timekeeping, and handoff channels.

### Concept Selection

Score issues `#2`, `#3`, and `#4` on a common 1–5 scale:

| Criterion                           | Weight |
| ----------------------------------- | -----: |
| User/research value                 |    25% |
| Feasibility in the event window     |    25% |
| ASU AIR platform fit                |    15% |
| Demo clarity                        |    15% |
| Innovation                          |    10% |
| Security/data/operational risk      |     5% |
| Team capability and reusable assets |     5% |

On September 1, record the score, assumptions, key risks, and team decision for both a Primary Concept and a Fallback Concept. If the Primary Concept lacks a demonstrable end-to-end slice four hacking hours after launch, the team explicitly chooses to narrow scope, switch to the Fallback Concept, or continue with a written rationale.

### Challenge Application

Before launch:

- Establish a neutral TypeScript web/API/shared-contract vertical slice.
- Verify deterministic install, lint, typecheck, test, build, and container smoke commands.
- Render Kubernetes manifests and enforce the repository policy baseline locally.
- Integrate health/readiness endpoints, structured logs, traces, metrics, and error reporting.
- Confirm safe data defaults and API-key handling.
- Prepare demo seed data, failure messaging, and a fallback demo path.

During the event:

- Deliver the smallest end-to-end behavior first.
- Keep `main` releasable.
- Use one ticket, branch, and pull request per demonstrable behavior.
- Reassess scope at each milestone and move deferrals to linked issues.
- Preserve a known-good immutable image and demo artifact.

### aSDLC Pilot

- Run Human-Agent Pair Programming for every agent-assisted ticket.
- Apply identical assurance controls to Standard and Event-Critical lanes.
- Record one redacted Session Evidence Record per agent session.
- Record agent/human effort, interventions, validation, review findings, deviations, and outcome.
- Capture process gaps in a Standards Backlog instead of blocking the Event Critical Path when safe.

### Presentation

- Write a three-part narrative: problem, demonstrated application, evidence-backed delivery lessons.
- Keep claims bounded to observed pilot evidence.
- Rehearse the happy path, recovery path, offline fallback, and time limit.
- Assign demo operation, narration, timekeeping, and question ownership.
- Preserve screenshots or a short recording in case the live environment is unavailable.

## Readiness checklist

A challenge-ready state requires:

- [ ] Applications and team name complete.
- [ ] Primary and Fallback Concepts recorded.
- [ ] Team roles and Presenter confirmed.
- [ ] Local scaffold passes the full validation suite.
- [ ] PR and `main` Cloud Build definitions validate.
- [ ] No PR build identity has deployment or runtime-secret access.
- [ ] Deployment proposal identifies exact service accounts, scopes, target namespace, images, secrets, DNS/TLS, and rollback behavior.
- [ ] Human approval is recorded before any live cloud mutation.
- [ ] Health, readiness, smoke, logging, trace, metric, and alert paths are understood.
- [ ] Demo data is public, synthetic, or explicitly approved.
- [ ] Rehearsal ticket has been executed and reviewed.
- [ ] Submission and demo fallback procedures are available.

## Risk controls

| Risk                                  | Control                                                             | Trigger for action                                      |
| ------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------- |
| Product scope is too large            | Vertical tracer bullets and explicit deferrals                      | No end-to-end slice after four hacking hours            |
| Agent output is incorrect or unsafe   | Accountable human, behavioral tests, integrated review              | Any unresolved Blocker/Critical/High finding            |
| Cloud pipeline blocks delivery        | Deterministic local commands and documented manual artifact path    | Required Cloud Build check is unavailable near deadline |
| Live deployment fails                 | Immutable image, rollout verification, smoke test, bounded rollback | Rollout or smoke verification fails                     |
| External API fails or is rate-limited | Timeouts, retries, cost/rate limits, graceful failure, demo fixture | Repeated API failures threaten the demo                 |
| Sensitive data reaches prompts/logs   | Approved-data-only default and redaction                            | Any suspected disclosure pauses affected work           |
| Process overhead threatens submission | Event-Critical Lane reduces ceremony, not assurance                 | Nathan approves lane change and deferrals are linked    |

## Completion

Preparation is complete when every readiness item is either satisfied or has a named accountable human, an explicit mitigation, and a deadline that protects the Event Critical Path.
