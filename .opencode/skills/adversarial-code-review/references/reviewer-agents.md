# Reviewer Agent Roster

The adversarial pipeline references three agents by `role`. Configure them once per environment; the pipeline assumes they exist. Each agent pins its own model — the `subagent` stage-level `model` field is ignored, so the agent named in `role` is the only lever that sets the backing model. A pipeline that varies only the stage `model` runs every stage on the same model and silently defeats adversarial review.

## The three agents

### `code-reviewer-a`

Reviewer A and its cross-validation pass. Anthropic family — the current Claude Opus. Pin the exact model ID in the agent's config.

### `code-reviewer-b`

Reviewer B and its cross-validation pass. Must resolve to a **different provider** than `code-reviewer-a`. Preference order: OpenAI → DeepSeek → GLM. Pin the exact model ID in the agent's config.

### `code-review-synthesizer`

Phase 3 synthesis only. Reconciliation is structural, so a cheaper Sonnet-class Claude is correct here; it does not need to match Reviewer A's version and may share a provider with Reviewer A.

## Selecting the models

1. Consult the opencode model catalog for the session; take the newest version in each family.
2. Set `code-reviewer-a` to the current Claude Opus and `code-reviewer-b` to the strongest reachable non-Anthropic model (walk the preference order if the first choice is unavailable).
3. Record the exact model IDs pinned in each agent's config, and report them verbatim in the review post (the `code-reviewer-a`, `code-reviewer-b`, and `code-review-synthesizer` identifiers) so a reader can map each comment back to a config.

## Verify before running

- Confirm all three agents exist and each pins a live model identifier from the catalog.
- Confirm `code-reviewer-a` and `code-reviewer-b` resolve to **different providers**. Two same-provider models are a second opinion, not adversarial review, and are never an acceptable degrade.
- Verify provider diversity against the agent configs, not the models' self-reports: a model cannot reliably name its own version, so read the pinned `model` from each config rather than asking the stage to describe itself.
- If no non-Anthropic reviewer family is reachable, adversarial review is not possible here — use the single-model fallback and disclose it.
