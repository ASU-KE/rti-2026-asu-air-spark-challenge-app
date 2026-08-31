# Reviewer Agent Configs

The pipeline needs three agents, one per stage role. Create them once per environment; the skill assumes they exist.

## Why agents rather than the stage `model` field

The `subagent` tool exposes a stage-level `model` field, but it does not change the backing model. Verified behavior:

| Agent config | Stage `model` | Model that actually ran |
|--------------|---------------|-------------------------|
| `"model": "claude-opus-4.6"` | `gpt-5.6-sol` | `claude-opus-4.6` (agent wins) |
| `"model": "claude-opus-4.6"` | `deepseek-3.2` | `claude-opus-4.6` (agent wins) |
| `"model": null` | `gpt-5.6-sol` | global `chat.defaultModel` |

The agent named in `role` determines the model. A pipeline that varies only `model` runs every stage on the same model, which silently defeats the entire point of adversarial review — the failure is invisible unless you check the attribution lines.

## Creating the agents

```
kiro-cli agent create code-reviewer-a
kiro-cli agent create code-reviewer-b
kiro-cli agent create code-review-synthesizer
```

Then set each config's `model` field (`kiro-cli agent edit <name>`) using the templates below. Resolve the identifiers against `kiro-cli chat --list-models` first — the values here are illustrative and go stale as new versions ship.

## `code-reviewer-a`

Reviewer A and its cross-validation pass. Anthropic family, latest Opus.

```json
{
  "name": "code-reviewer-a",
  "description": "Reviewer A for adversarial code review. Anthropic family.",
  "prompt": "You are an independent code reviewer. Review only what you are asked to review. Cite file:line for every finding. Do not coordinate with other reviewers.",
  "model": "claude-opus-5",
  "tools": ["*"],
  "allowedTools": ["@builtin", "fs_read", "fs_list"],
  "mcpServers": {},
  "resources": [],
  "useLegacyMcpJson": true
}
```

## `code-reviewer-b`

Reviewer B and its cross-validation pass. Must be a **different provider** than `code-reviewer-a`. Preference order: OpenAI → DeepSeek → GLM.

```json
{
  "name": "code-reviewer-b",
  "description": "Reviewer B for adversarial code review. Non-Anthropic family.",
  "prompt": "You are an independent code reviewer. Review only what you are asked to review. Cite file:line for every finding. Do not coordinate with other reviewers.",
  "model": "gpt-5.6-sol",
  "tools": ["*"],
  "allowedTools": ["@builtin", "fs_read", "fs_list"],
  "mcpServers": {},
  "resources": [],
  "useLegacyMcpJson": true
}
```

## `code-review-synthesizer`

Phase 3 only. Reconciliation is structural, so a cheaper Sonnet-class model is correct here — it does not need to match Reviewer A's version.

```json
{
  "name": "code-review-synthesizer",
  "description": "Synthesizer for adversarial code review. Reconciles two cross-validated reviews.",
  "prompt": "You reconcile completed reviews. Never add new findings. Preserve severity tiers, file:line citations, and code suggestions verbatim from the source reviews.",
  "model": "claude-sonnet-5",
  "tools": ["*"],
  "allowedTools": ["@builtin", "fs_read", "fs_list"],
  "mcpServers": {},
  "resources": [],
  "useLegacyMcpJson": true
}
```

## Tool grants

The reviewer agents need read access to the repository and whatever integration provides PR diffs and comments (a GitHub or GitLab MCP server, or the CLI). Grant read-only tools where possible: reviewers read and report, they do not modify the repo. Posting the review is the calling session's job, not a reviewer stage's.

Keep the grants minimal. Broad grants inherited from a general-purpose agent give reviewer stages access to unrelated systems for no benefit.

## Verifying the roster took effect

Check the pinned `model` in each agent config before running the pipeline, and confirm `kiro-cli agent list` resolves the names the pipeline uses. Do not verify by reading the attribution lines afterward: models routinely misidentify their own version, because the version being served postdates their training data. Observed behavior with these configs:

| Agent | Pinned model | Self-reported |
|-------|--------------|---------------|
| `code-reviewer-a` | `claude-opus-5` | "Claude Opus 4.5" — wrong version, correct provider |
| `code-reviewer-b` | `gpt-5.6-sol` | "OpenAI trained me; gpt-5.6-sol" — accurate |
| `code-review-synthesizer` | `claude-sonnet-5` | "Anthropic; claude-sonnet-5" — accurate |

Provider is reliable in a self-report; version is not. That is why the calling session interpolates the configured identifiers into the prompts rather than asking each stage to describe itself.

Never post a review produced by two instances of the same provider as adversarial output.
