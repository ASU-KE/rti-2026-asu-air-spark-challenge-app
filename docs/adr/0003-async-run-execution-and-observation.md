# 0003 — Asynchronous Run execution and live observation

Status: Accepted
Date: 2026 (hackathon planning)

## Context

A Run is long-running: up to 50 Agents × many Rounds × one throttled LLM call each. It cannot
complete within a single synchronous HTTP request. The Intermediate Dataset must also be
**observable live** while the Run advances. AGENTS.md marks the background-job runner and the
persistence engine as *not settled* and requires that they stay behind abstractions.

## Decision

- Model a **`RunExecutor` seam** that drives a Run's Rounds asynchronously. The API *starts* a
  Run and returns immediately; the Run advances in the background.
- For the prototype, implement the executor **in-process** (FastAPI `asyncio` background task),
  behind the seam so an external job runner can replace it later without touching callers.
- The executor appends **Round Records** to the Intermediate Dataset through the repository
  seam; that append-only log is the single source of truth.
- Clients observe progress live via **Server-Sent Events (SSE)**, with REST polling of the Run
  status as a fallback.

## Consequences

- In-process execution is sufficient for the prototype's scale (10 agents) and is
  demo-legible; the seam preserves the "not settled" promise for scaling later.
- SSE fits an append-only, unidirectional log and rides the existing async process without
  WebSocket overhead. The deployment ingress must permit response streaming.
- The concrete persistence engine remains unchosen behind the repository seam; the Round
  Record log is durable-by-append so a crash mid-Run is not fatal and live observation reads
  the same source as final export.

## Alternatives considered

- **External job runner (e.g. Cloud Tasks / Pub/Sub + workers, Celery)** — appropriate at
  scale; deferred as an ask-first decision to avoid committing to a service prematurely.
- **WebSockets** — bidirectional and heavier than needed for one-way progress streaming;
  rejected for the prototype.
- **Polling only** — simplest but laggy for live observation; kept only as a fallback.
