---
author: Nathan Rollins
date-created: 2026-08-26
status: superseded
superseded-by: docs/asdlc/workflow.md
---

# Goal: Explore an Enterprise-Informed Agent Software Development Lifecycle (aSDLC)

> Historical planning input. The accepted terminology, scope, and workflow are defined in `CONTEXT.md`, the accepted ADRs, and `docs/asdlc/workflow.md`.

The primary goal for this project is to test an agent-centric software development lifecycle (aSDLC) that can hold up to the demands and quality requirements for RTO mission-critical applications.

Start with [Matt Pocock's skills](https://github.com/mattpocock/skills) and SDLC:

- `/grill-with-docs`
- `/to-spec`
- `/to-tickets` with `/tdd`
- `/code-review`

Adapt and improve that baseline SDLC with ET's skills: [ASU/ddt-agent-skills-library](https://github.com/ASU/ddt-agent-skills-library)

- `/adversarial-code-review`
- `/pr-review`
- `/security-review`

## Goals:

- Produce documentation on the workflow
- Lessons Learned, what worked, what didn't
- Publish draft RTO Agentic SDLC Standards document

## Requirements:

- Clear and well-defined Technical Specification
- Work items/tickets queue must support multiple developers & agents
  - How do we manage task assignment/claims, avoid work collisions
  - Coordinate work item dependencies across dev/agent partnerships
- Human-Agent Pair Programming model
  - Document a possible Human-Agent Pair Programming framework

## Work breakdown into Feature-based Slices

- Make sure each slice/ticket is not too large (need definition of too big)
  - 700 lines?
  - Would need to be context-dependent. But need clear definition for agent steering
  - TODO: lookup how industry leaders have defnined this
- Each feature/slice is built into its own Feature Branch
  - Name schema: `feature/[ASURITE]-[Issue Number]-[Issue title]`

## Test Driven Development

- Each work item must follow TDD (Red/Green) workflow
  - **TODO:** steering needed to determine what tests/kinds of tests needed.j
- What kind of tests and coverage?
  - Is a generic 100% instruction sufficient?
  - Class/object and service modules interfaces fully tested
  - E2E full coverage
  - Allow agent recommendations

### Testing Framework:

- We need a reliable local development environment that has all required services
  - Database
    - Migrations
    - Seed database for tests
  - Logging/Monitoring
  - OpenAPI specs: documentation and tests
  - Sandboxed (Docker sbx)

## Agentic Code Review

- Pre-specified success criteria, validation tests
- Adversarial code reviews
  - [adversarial-code-review](https://github.com/ASU/ddt-agent-skills-library/tree/main/skills/adversarial-code-review)
  - [pr-review](https://github.com/ASU/ddt-agent-skills-library/tree/main/skills/pr-review)
  - [security-review](https://github.com/ASU/ddt-agent-skills-library/tree/main/skills/security-review)
- TODO: Compare mattpocock/code-review with ddt-skill

- PR required at the end of each work item (not just at the end of the development cycle)
  - After the Code Review
  - TODO: Enable GitHub Copilot PR Review
- Item PRs should merge into a `staging` branch, maybe `feature/[featurename]-[workitem]`
- Branch schema

Workflow diagram:

- TDD -> Code Review -> PR -> PR Review/Approval -> merge into `staging` branch
  - After PR creation and before PR merge: merge `staging` in; bring up-to-date
  - Can we automate branch syncs during new PR create and before PR merge?
