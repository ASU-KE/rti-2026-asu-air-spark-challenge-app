# Integrated review routing

## One entry point

Every pull request and every delivery lane invokes `/code-review`. This is the sole review workflow entry point; `/pr-review`, `/security-review`, and adversarial reviewers are bounded components of that workflow rather than alternative gates.

Review happens twice:

1. **Local pre-PR preflight** against a fixed commit, branch, tag, or merge base.
2. **Pull-request merge gate** against the exact PR diff and originating issue/specification.

Documentation-only changes use the same routing. Reviewers may mark a lens not applicable only with a written rationale.

## Review graph

```text
fixed diff + issue/spec + repository standards
                    |
     +--------------+---------------+
     |              |               |
 Standards       Spec fit      PR quality/risk
     |              |               |
     +--------------+---------------+
                    |
       universal security review
                    |
   required provider and AI layers
                    |
   independent reviewer A + reviewer B
                    |
      reciprocal cross-validation
                    |
       synthesis and deduplication
                    |
     adjudication when necessary
                    |
       one merge recommendation
```

## Required lenses

### Standards

Compare the change with `AGENTS.md`, `CONTEXT.md`, applicable ADRs, repository conventions, and generated-code or infrastructure standards. Identify unapproved vocabulary or architectural divergence.

### Specification

Trace every requirement and acceptance criterion to implementation and observable evidence. Look for missing behavior, accidental extra scope, contract drift, and undocumented deferrals.

### PR quality and risk

Assess purpose, cohesion, maintainability, test sensitivity, failure behavior, backward compatibility, supply-chain trust, deployment impact, observability, and rollback. The review must inspect what should have changed but did not—not only modified lines.

### Security

`/security-review` is mandatory. Its universal layer covers secrets, authentication/authorization, input/output boundaries, injection, dependency and CI trust, privacy, logging, and misuse cases.

Apply additional layers when relevant:

- **AI application:** prompt injection, untrusted model/tool output, data leakage, model abuse, cost/rate limits, provenance, and human oversight.
- **Google Cloud/GKE:** least-privilege IAM and Workload Identity, Cloud Build trust boundaries, Artifact Registry/image provenance, Kubernetes RBAC, namespace isolation, NetworkPolicy, ingress, security contexts, secrets, telemetry exposure, and rollout/rollback.
- Other providers only when the change actually touches them.

### Independent adversarial review

Two reviewers from different model families independently reconstruct behavior and produce evidence-backed findings. Each reviewer then challenges the other's findings for validity, severity, duplicates, and missed risks. If independent providers are unavailable, the workflow reports degraded confidence rather than pretending independence.

## Evidence standard

A blocking finding includes:

- Severity and affected requirement or risk.
- File and line/range or absent-change location.
- Reproduction or reasoning path.
- User, operational, or security impact.
- Smallest safe remediation or decision needed.

Speculation without a falsifiable path is a question, not a blocking finding.

## Finding policy

| Severity | Disposition before merge                                                   |
| -------- | -------------------------------------------------------------------------- |
| Blocker  | Fix; merge prohibited                                                      |
| Critical | Fix; merge prohibited                                                      |
| High     | Fix; merge prohibited                                                      |
| Medium   | Fix or obtain explicit human risk acceptance with a linked follow-up issue |
| Low      | Nonblocking; may become follow-up work                                     |
| N/A      | Written rationale required                                                 |

Security, privacy, compliance, and Responsible AI stop-work concerns remain blocking until resolved or adjudicated by an authorized human.

## Synthesis

The synthesizer:

1. Deduplicates findings without erasing independent corroboration.
2. Reconciles severity using demonstrated impact.
3. Separates required fixes, accepted follow-ups, questions, and positive evidence.
4. Identifies review degradation or incomplete evidence.
5. Produces one recommendation: **merge**, **merge after required fixes**, or **do not merge**.
6. Attributes reviewer model/provider and review stage.

## Adjudication

A disputed blocking finding is assigned to a human who did not author the disputed change when possible. The adjudicator reviews the requirement, evidence, risk, and proposed disposition. The decision and rationale are recorded in the pull request; silent dismissal is not permitted.

## Completion criterion

Integrated review is complete only when every required lens ran or has a justified N/A, every finding has a disposition, independent-review confidence is stated, all merge-blocking findings are resolved, and the synthesized recommendation is linked in the pull request.
