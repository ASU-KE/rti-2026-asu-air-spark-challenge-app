# 0001 — Scope and anchor scenario

Status: Accepted
Date: 2026 (hackathon planning)

## Context

The requirements describe an ambitious "flexible framework" for multi-agent social
experiments, while the README states the hackathon scope is deliberately constrained and
should "prove the core research workflow rather than attempt to build a complete
general-purpose simulation platform." An open-ended framework and a 48-hour prototype pull in
opposite directions, and nearly every downstream decision depends on which one we are
building.

The abstract goal ("problems of social collective action under differential information")
also does not, by itself, determine a data model, an end-state test, or an output shape. A
concrete scenario is needed to anchor the design.

## Decision

1. **Build a constrained prototype, framework-shaped.** Design the domain model and module
   seams as if for the full framework, but scope the *build* to a single end-to-end vertical
   slice: configure → run → observe → export. Breadth (arbitrary multi-scale configurability)
   is deliberately limited; the prototype may be fleshed out as time allows.
2. **Anchor scenario: opinion dynamics / consensus under unequal information.** Agents hold a
   quantified Stance on a proposition and update it over Rounds while their access to peers
   (Network Edges) and to background information (Context Shells) is deliberately unequal.

## Consequences

- The scenario gives a natural time-series dataset (Stance per Agent per Round) and an
  obvious, testable end-state (convergence or max rounds) for the Orchestrator.
- It exercises all three differentiation axes (Role, Persona, network-structural access).
- The framework-shaped seams keep future breadth reachable without betting the hackathon on
  it.
- Anything not needed to demonstrate this one workflow is out of scope for the prototype.

## Alternatives considered

- **Public-goods / cooperation game**, **coordination game**, **information-cascade
  deliberation** — all viable collective-action scenarios; opinion dynamics was chosen for the
  cleanest measurable convergence signal and demo legibility.
- **Full general framework** — rejected for the 48-hour window per the README's stated scope
  discipline.
