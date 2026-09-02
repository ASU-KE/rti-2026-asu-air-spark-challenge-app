# 0005 — Markdown at the LLM boundary, JSON internally

Status: Accepted
Date: 2026 (hackathon planning)

## Context

Each Round an Agent must return a structured Stance (a numeric position, a confidence, and a
free-text rationale). The provider exposes a range of open/instruction-tuned models (Qwen,
Gemma, Minimax, Llama, Kimi, of varying sizes), and support for provider-side "JSON mode" or
function-calling on the LiteLLM gateway is **unverified**. Small and open models produce
well-formed nested JSON unreliably, but follow a labeled Markdown template consistently. A
malformed response must not derail a Run.

## Decision

- The **model-facing format is a labeled Markdown template** (e.g. `## Stance` / `##
  Confidence` / `## Rationale` sections), which is parsed into the canonical Stance schema
  (Pydantic).
- **JSON remains the internal representation** used by the API, the Datasets, and storage.
  Markdown exists only at the LLM boundary.
- Parsing failures are handled by **one repair retry** (re-prompt including the parse error);
  if it still fails, the Agent's prior Stance is **carried forward**, the Round Record is
  flagged (e.g. `unparsed`), and the Run continues.
- The parsing/formatting sits behind the `ProviderClient` so provider-side structured-output
  features can be adopted later if `/v1/models` shows support.

## Consequences

- Markedly more reliable structured extraction across the heterogeneous model set, including
  small models.
- Transcripts and prompts are more human-legible for the demo.
- A Run is resilient to occasional malformed responses rather than crashing.
- Slightly non-standard versus defaulting to JSON mode, and requires a maintained Markdown
  parser.

## Alternatives considered

- **Raw JSON with schema + repair retry** — the initial approach; kept as the fallback shape
  but rejected as the primary boundary format because open models break nested JSON too often.
- **Provider JSON mode / function-calling** — cannot be relied on; gateway support unverified.
