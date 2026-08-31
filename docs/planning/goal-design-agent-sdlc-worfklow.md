---
author: Nathan Rollins
date-created: 2026-08-26
status: draft
---

# Goal: Design an Enteprise-ready agent Software Development Lifecycle (aSDLC)

The primary goal for this project is to test an agent-centric software development lifecyle (aSDLC) that can hold up to the demands and quality requirements for RTO mission-critical applications.

I am inspired by the SDLC workflow that Matt Pocock demonstrates with his skills library (https://github.com/mattpocock/skills) (also located in this project in `/.kiro/skills`):

- `/grill-with-docs`
- `/to-spec`
- `/to-tickets` with `/tdd`
- `/code-review`

We intend to adapt and improve that baseline SDLC using ASU ENterprise Technology's (ET) skills: [ASU/ddt-agent-skills-library](https://github.com/ASU/ddt-agent-skills-library). Also located in `.kiro/skills`.

- `/adversarial-code-review`
- `/pr-review`
- `/security-review`

A far more refined and advanced agent harness that we have just encountered is [aafan-m/ECC](https://github.com/affaan-m/ECC). ECC demonstrates a mature agent harness framework that exemplifies the robust SDLC I hope to demonstrate in time. It may be too much to adapt prior to the hackathon, but we are reviewing it for insights that we may test in this project.

## Goals:

- Produce documentation on the workflow
- Lessons Learned, what worked, what didn't
- Publish draft RTO Agentic SDLC Standards document

## Requirements:

- Clear and well-defined Technical Specification
- Work items/tickets queue must support multiple developers & agents
  - How do we manage task assignment/claims, avoid work collisions
  - Coordinate work item dependencies across dev/agent partnerships
- Developer-Agent model: Pair Programming Partnership (define PPP)
  - Document possible Agent-Dev PPP framework

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
