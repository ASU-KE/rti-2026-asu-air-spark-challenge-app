# 0004 — Single shared provider throttle over the LiteLLM gateway

Status: Accepted
Date: 2026 (hackathon planning)

## Context

Agent reasoning is powered by the ASU Research Computing OpenAI-compatible gateway
(`https://openai.rc.asu.edu/v1`), which is backed by LiteLLM. The gateway's rate limits are
**not published**; the documentation only states that exceeding the allowed rate returns a
`429` ("wait and try again"). A Run can issue many concurrent Agent calls, and multiple Runs
may execute at once. A researcher may also select different Models per Run (and per Role), and
we must use the provider responsibly.

## Decision

- Route **every** Agent LLM call through **one shared `ProviderClient`** per process that
  wraps the gateway.
- The client enforces a **single, configurable rate limit** (bounded async queue +
  token-bucket throttle) and handles `429` with **exponential backoff + jitter**, honoring
  `Retry-After` when present.
- The throttle is **global across all Models and all Runs** — Model selection does not create
  separate rate buckets. Per-Model rate controls are explicitly deferred to a later feature
  cycle.
- The actual rate and concurrency are **configuration values**, tunable to whatever the
  platform tolerates without code change.

## Consequences

- The platform sees a single, bounded outbound call budget regardless of how many Runs or
  Models are active, which is the safe posture under unpublished limits.
- Because the gateway is LiteLLM-fronted, a single throttle in front of it is sufficient;
  Model differences do not require separate client-side buckets for the prototype.
- Per-Run result isolation is unaffected; only the outbound call budget is shared.

## Alternatives considered

- **Per-Model queues / throttles** — potentially higher throughput if models have distinct
  limits, but the limits are unpublished and LiteLLM already multiplexes them; added
  complexity is not justified now. Deferred to a separate feature cycle.
- **No client-side throttle (rely on 429 alone)** — risks hammering the gateway and unfair use;
  rejected.
