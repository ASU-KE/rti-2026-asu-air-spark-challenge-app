# 0002 — Simulation engine: discrete rounds

Status: Accepted
Date: 2026 (hackathon planning)

## Context

The requirements call for "some sort of time-control or sequencing system" supporting both
synchronous and asynchronous decisions and communications. Opinion-dynamics models are
conventionally simulated as discrete time steps, and we need semantics that are deterministic,
reproducible, and legible in a live demo — while remaining flexible enough to become a
research variable.

## Decision

- The engine advances in **discrete Rounds** (ticks). Continuous / real-time behavior is out
  of scope.
- **Update order** within a Round is configurable: `synchronous` (default — every Agent reads
  the prior Round's state and writes simultaneously), `sequential` (fixed order), or `random`
  (shuffled order).
- **Observation model**: in Round *N* an Agent observes, from its inbound Edges, those peers'
  Stance and Messages **as of Round *N−1***, plus the Context Shells it holds and its own
  Memory window. It then emits its new Stance (*N*) and an optional Message (*N*). Messages are
  therefore seen one Round later, never same-Round.
- **Memory window**: how many prior Rounds an Agent's reasoning includes is configurable and
  small by default; the window size is itself a research variable.

## Consequences

- Synchronous, prior-Round observation makes a Run deterministic and race-free given a fixed
  Seed and Model, satisfying reproducibility.
- A small default Memory window bounds token cost predictably, which matters under the
  provider's unpublished rate limits and at 50+ agents.
- Async behavior is a configuration value (`update order`), not a re-architecture.

## Alternatives considered

- **Event-driven / real-time async** — more faithful to some social processes but
  non-deterministic, harder to reproduce and demo, and heavier to build; rejected for the
  prototype.
- **Full-history memory** — most faithful but blows the context window and token budget at
  scale; rejected in favor of a configurable window (summarized memory deferred).
