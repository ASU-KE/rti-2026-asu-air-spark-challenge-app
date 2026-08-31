# ASU AIR Spark Challenge Project

This repository supports our entry in the [ASU AIR Spark Challenge](https://asuevents.asu.edu/event/asu-air-spark-challenge), a 48-hour hackathon focused on using the ASU AI Research Acceleration Platform to prototype applications that address real-world problems.

Our leading application concept is a flexible framework for running computational experiments with networked, persona-based LLM social agents. In parallel, we will use the project to demonstrate and document an agentic Software Development Lifecycle (aSDLC) suitable for high-quality, enterprise and mission-critical software development.

> **Project status:** Early planning and concept development. The application scope, team name, and implementation details remain subject to agreement by the full team.

## Team name

### AIRgents of Change *(leading candidate)*

**AIRgents of Change** combines three ideas at the center of the project:

- **AIR** — the ASU AI Research Acceleration Platform powering the challenge.
- **Agents** — the autonomous, persona-based LLM participants in the proposed application.
- **Agents of change** — a team using collaborative AI research and engineering to explore meaningful real-world questions.

This is the current leading candidate, not yet the team's final approved name.

## Application concept

The proposed application is a configurable environment for creating artificial societies of LLM-driven agents and studying how their individual personas, goals, information, and relationships shape group behavior.

Through a dashboard, a researcher or experiment designer could:

- Define persona groups such as collaborators, instigators, pacifists, or antagonists.
- Give each persona custom instructions, goals, behavioral tendencies, and contextual information.
- Instantiate agents and assign them to personas and groups.
- Organize agents into a network that governs who can interact or share information.
- Control context visibility so different agents or groups operate with different—and intentionally limited—knowledge.
- Run repeatable scenarios and observe individual decisions, social influence, cooperation, conflict, and emergent collective behavior.

This framework could support experiments into questions such as:

- How does incomplete or unevenly distributed information affect group decisions?
- Under what conditions do agents cooperate, polarize, or converge on a shared outcome?
- How do different persona mixes and network structures influence collective behavior?
- Can particular interventions encourage constructive cooperation in multi-agent systems?

The concept is being developed in [GitHub Issue #3: Flexible Framework to Run Computational Experiments with Networked Persona-Based LLM Social Agents](https://github.com/ASU-KE/rti-2026-asu-air-spark-challenge-app/issues/3).

## Primary goal: Deliver a compelling challenge prototype

Our primary goal is to build and demonstrate a focused, credible prototype on the ASU AI Research Acceleration Platform. The prototype should make it easy to configure a small artificial society, run an experiment, and communicate the resulting interactions and emergent behavior.

The final hackathon scope will be deliberately constrained. We want to prove the core research workflow rather than attempt to build a complete general-purpose simulation platform within 48 hours.

A successful challenge prototype will:

1. Address a clear research or real-world question.
2. Demonstrate configurable, persona-based LLM agents interacting in a network.
3. Show the effect of goals, personas, or unequal context on agent behavior.
4. Produce results that can be inspected and explained in a live demonstration.
5. Establish a foundation that could support richer experiments after the challenge.

## Secondary goal: Demonstrate an agentic SDLC

A second—and very important—goal is to use this project as a practical test of an enterprise-ready **agentic Software Development Lifecycle (aSDLC)**. We want to evaluate how human developers and coding agents can work as accountable engineering partners while meeting the quality expectations of ASU Research Technology Office mission-critical applications.

The intended lifecycle adapts ideas from [Matt Pocock's agent skills](https://github.com/mattpocock/skills), the [ASU Enterprise Technology agent skills library](https://github.com/ASU/ddt-agent-skills-library), and emerging agent-harness practices. Its working flow is:

```text
Discovery and rigorous questioning
  → Technical specification
  → Small, dependency-aware feature tickets
  → Test-driven implementation
  → Agentic and adversarial code review
  → Pull-request review and approval
  → Integration into staging
```

### Practices we intend to exercise

- **Specification before implementation:** Establish clear requirements, architecture, constraints, and measurable success criteria.
- **Feature-based slices:** Divide work into small, independently reviewable tickets that multiple developer-agent partnerships can execute without collisions.
- **Developer-Agent Pair Programming Partnership (PPP):** Define a model in which people provide intent, judgment, and accountability while agents contribute analysis, implementation, validation, and review.
- **Test-driven development:** Use a red/green workflow and select unit, integration, contract, and end-to-end tests according to the risk of each feature.
- **Reproducible local development:** Provide the services, seed data, migrations, observability, API specifications, and sandboxing needed to validate changes reliably.
- **Independent review:** Apply code-review, pull-request-review, security-review, and adversarial-review practices against predeclared acceptance criteria.
- **Controlled integration:** Develop each work item on a feature branch, require a pull request, and integrate reviewed work through a staging branch.
- **Multi-agent coordination:** Explore ticket claims, dependency tracking, branch synchronization, and other controls that allow several developers and agents to contribute safely in parallel.

### aSDLC outputs

Beyond the application itself, we intend to produce:

- Documentation of the workflow we actually followed.
- A candid record of lessons learned, including what worked and what did not.
- Recommendations for effective developer-agent collaboration.
- A draft set of RTO Agentic SDLC Standards for further evaluation and refinement.

The current workflow notes are in [`docs/planning/goal-design-agent-sdlc-worfklow.md`](docs/planning/goal-design-agent-sdlc-worfklow.md).

## What success looks like

By the end of the challenge, we aim to have both:

1. **A working multi-agent research prototype** that demonstrates the value of configurable personas, networked interactions, and controlled context; and
2. **Evidence from a real delivery cycle** showing where an agentic SDLC improves—or complicates—software quality, development speed, coordination, traceability, and human oversight.

The application is the challenge deliverable. The process used to create it is also an experiment.