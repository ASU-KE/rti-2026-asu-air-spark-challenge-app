---
name: adversarial-code-review
description: Review a PR with two reviewers from different model families that cross-validate each other's findings before synthesis. Use when a change touches authentication, secrets, provider throttling, data integrity, or cross-service contracts, or when a review needs higher confidence than the mandatory /code-review gate provides.
---

## When to Activate

Use this skill as an opt-in escalation for high-risk slices (authentication, secrets, provider throttling, data integrity, cross-service contracts). It composes ON TOP of the mandatory `/code-review` gate — it never replaces it.

Two reviewers from different model families produce independent reviews, then cross-validate each other's findings, then a cheap model synthesizes the result. Different families catch different blind spots; cross-validation forces each model to explicitly confirm or challenge the other's findings, which produces higher-confidence output than simple reconciliation.

Relationship to sibling skills:

- `/code-review` — the mandatory gate for every slice. This skill composes ON TOP of it for high-risk changes.
- `pr-review` — fast pass for non-blocking feedback. Use when you need a quick opinion.
- `security-review` — deep audit for auth, secrets, and networking. Use when the change is security-heavy; compose with this skill if risk is extreme.

Cross-validation roughly doubles reviewer-tier invocations (each reviewer model runs twice) and adds a serial validation layer before synthesis. That is the cost of higher-confidence findings.

## When to Skip

Single-model review is acceptable only in these cases:

- **Trivial mechanical changes** — typos, doc-only edits, single-line config tweaks, dependency bumps with no behavior change.
- **Explicit user opt-out** — "simple review", "quick review", "single model is fine".
- **Re-review after feedback** — verify the deltas against the prior review rather than running a fresh adversarial pass.
- **No second model family available** — a second Anthropic model is never a substitute (see [Prerequisites](#prerequisites) step 3).

Anything else runs adversarial, including PRs that look small but touch infrastructure, security, IAM, data handling, or cross-service contracts. If unsure whether a PR qualifies as trivial, run adversarial.

## Review Substance

The pipeline below is mechanism. The substance of what to inspect — reading prior threads and CI output, what to look for in the diff, what to look for that is *missing* from the diff, and the recurring failure patterns worth checking every time — lives in [references/review-checklist.md](references/review-checklist.md).

**The calling session reads that file and interpolates its contents into the reviewer prompts as `<<checklist>>`.** Do not tell a reviewer stage to read the path itself: stages inherit the calling session's working directory, not the skill directory, so a relative path usually does not resolve and the reviewer proceeds without the criteria — silently, since the prompt still names the severity tiers. Where `SKILL.md` and the checklist overlap (attribution formats in particular), `SKILL.md` wins.

## Prerequisites

This skill requires two models from DIFFERENT provider/model families to be reachable in the opencode model catalog (reviewer A from one family, reviewer B from another). Before starting:

1. Consult the opencode model catalog for the session to identify available models.
2. Verify both reviewer models are reachable and can be invoked.
3. Confirm reviewer A and reviewer B are from **different providers**. Two same-provider models are a second opinion, not adversarial review — not an acceptable degrade under any circumstance.

The pipeline references three named agents by `role` (configured in the environment; see [references/reviewer-agents.md](references/reviewer-agents.md)):

| Agent | Purpose | Model family |
|-------|---------|--------------|
| `code-reviewer-a` | Reviewer A and its cross-validation pass | Current Claude Opus (Anthropic) |
| `code-reviewer-b` | Reviewer B and its cross-validation pass | Strongest available non-Anthropic model |
| `code-review-synthesizer` | Phase 3 synthesis | Sonnet-class Claude |

If no second model family is reachable, adversarial review is not possible in this environment. Fall back to single-model review and disclose that adversarial review was unavailable.

## Model Roster

Standing pipeline:

- **Reviewer A** — current Claude Opus (Anthropic family; high-capability reasoning).
- **Reviewer B** — strongest available non-Anthropic model. Preference order: OpenAI GPT-5.6 Sol → DeepSeek → GLM.
- **Synthesizer** — a Sonnet-class Claude (fast and cheap; synthesis is structural, not generative).

**Resolve models against the live catalog before spawning — do not trust the identifiers in this document.** Consult the opencode model catalog and take the newest version in each family. As of 2026-07 that resolves to `claude-opus-5` (Reviewer A), `gpt-5.6-sol` (Reviewer B), and `claude-sonnet-5` (synthesizer), with `deepseek-3.2` and `glm-5` as Reviewer B fallbacks. If credit cost matters more than review depth on a given PR, `gpt-5.6-terra` (roughly half the rate of Sol) or `deepseek-3.2` are acceptable Reviewer B substitutions — note the substitution in the summary.

**Review and cross-validation stages must use the latest available version in each reviewer family** (the strongest models do the original judgment and the challenge). A family's validation stage uses the same version as that family's review stage. **The synthesizer does not need the latest version** — any available Sonnet-class model works, since its job is structural reconciliation rather than original review.

Record/pin the selected model IDs in the corresponding agent's config (see `references/reviewer-agents.md`), not in the pipeline JSON. The `subagent` tool's stage-level `model` field is ignored; `role` is the only lever that changes the backing model.

**Attribution strings come from the agent configs, never from the model's self-report.** A model cannot reliably name its own version, because the version it is serving usually postdates its training data — a stage pinned to `claude-opus-5` self-reported "Claude Opus 4.5" and asserted that no Opus 5 exists. Read the pinned `model` from each agent config before Phase 1 and interpolate those identifiers into the prompts as `<<model_a>>`, `<<model_b>>`, and `<<model_synth>>`, exactly like prior-stage outputs. Reviewer prompts instruct the model to emit the supplied string verbatim rather than describing itself.

**Post the identifier verbatim** — `claude-opus-5`, not "Claude Opus 5". Prettifying the string reintroduces the guessing this rule exists to remove, and an exact identifier lets a reader map a comment back to a config.

**The two reviewer slots must come from two different providers — never two models from the same provider/family.** Two same-provider models are a second opinion, not adversarial review, and are not an acceptable degrade under any circumstance. If the preferred Reviewer B is unavailable, walk down the preference order and update `code-reviewer-b`'s pinned model. If no non-Anthropic reviewer family is reachable at all, adversarial review is not possible in this environment — do not substitute a second Anthropic model. Fall back to [single-model review](#single-model-fallback) and disclose that adversarial review was unavailable. The synthesizer being Claude is fine because it is not contributing original review judgment, it is reconciling the cross-validated reviews.

Verify provider diversity against the two agent configs before spawning, not against the attribution lines afterward — self-reports cannot distinguish a misrouted stage from a model that simply misidentifies itself. If both agents resolve to the same provider, the run is invalid: fix the configs and re-run rather than posting the result.

This skill consults the opencode model catalog, verifies agent configurations, and pins model IDs (see `references/reviewer-agents.md`); everything else runs through agent tools. Keep it that way — no shell scripts, no absolute paths, no platform-specific tooling — so the skill works on Linux, macOS, and Windows alike.

## Pipeline

Five stages across three phases: Review (×2), Cross-validate (×2), Synthesize (×1).

Two placeholder conventions appear in the JSON below, and they are filled in by different parties:

- `{task}` is substituted by the `subagent` tool from the stage set's top-level `task` field. Use it in every phase so each stage knows which PR it is working on.
- `<<...>>` placeholders are substituted by **the calling session** before the stage is spawned — prior-stage outputs (`<<reviewer_a output>>`), the checklist (`<<checklist>>`), and the model identifiers (`<<model_a>>`, `<<model_b>>`, `<<model_synth>>`) read from the agent configs.

**Do not rely on implicit propagation of stage outputs.** Nothing flows between stages on its own. The calling session collects each stage's output and interpolates it verbatim into the `prompt_template` of every downstream stage before spawning that stage. A prompt that still contains a literal `<<...>>` or a literal `<REPO>#<PR-NUMBER>` when it reaches a model is a bug: that stage cannot fetch the diff and will reason only about the text it was handed.

1. **Phase 1 — Review (parallel).** Spawn both reviewer stages. Collect `reviewer_a` and `reviewer_b` outputs.
2. **Phase 2 — Cross-validate (parallel).** Spawn both validate stages, interpolating both review outputs into each validate prompt. Collect `validate_a` and `validate_b` outputs.
3. **Phase 3 — Synthesize.** Spawn the synthesizer, interpolating all four prior outputs plus the three model identifiers. Collect the final review, then adjudicate any disputed items.

### Phase 1 — Review

```json
{
  "task": "Adversarial code review of <REPO>#<PR-NUMBER>",
  "mode": "blocking",
  "stages": [
    {
      "name": "reviewer_a",
      "role": "code-reviewer-a",
      "prompt_template": "Perform an independent code review of {task}.\n\nApply this review guidance:\n\n<<checklist>>\n\nProduce your review with severity tiers (Must fix / Should fix / Nice to have), file:line citations for every item, and code suggestions where the fix is concrete. Begin your output with the attribution line **[Reviewed by <<model_a>>]** exactly as given — do not substitute your own understanding of which model you are. Do not coordinate with or reference any other reviewer — review independently."
    },
    {
      "name": "reviewer_b",
      "role": "code-reviewer-b",
      "prompt_template": "Perform an independent code review of {task}.\n\nApply this review guidance:\n\n<<checklist>>\n\nProduce your review with severity tiers (Must fix / Should fix / Nice to have), file:line citations for every item, and code suggestions where the fix is concrete. Begin your output with the attribution line **[Reviewed by <<model_b>>]** exactly as given — do not substitute your own understanding of which model you are. Do not coordinate with or reference any other reviewer — review independently."
    }
  ]
}
```

### Phase 2 — Cross-validate

Replace `<<reviewer_a output>>` and `<<reviewer_b output>>` with the verbatim Phase 1 outputs before spawning. Each validator may re-read the diff to test a finding, so `{task}` must resolve here too:

```json
{
  "task": "Cross-validation for <REPO>#<PR-NUMBER>",
  "mode": "blocking",
  "stages": [
    {
      "name": "validate_a",
       "role": "code-reviewer-a",
       "prompt_template": "Two independent code reviews of {task} were produced.\n\nReview from Reviewer A:\n<<reviewer_a output>>\n\nReview from Reviewer B:\n<<reviewer_b output>>\n\nYou are Reviewer A. Cross-validate Reviewer B's findings:\n1. **Agree** — which of Reviewer B's findings do you confirm as valid? Briefly state why.\n2. **Disagree** — which of Reviewer B's findings are incorrect, overstated, or based on a misreading? Cite the code or docs that support your position.\n3. **Missed** — valid issues Reviewer B caught that you missed.\n4. **Retract** — items from your own review you now believe are wrong after seeing Reviewer B's perspective.\n\nBe specific. Cite file:line references. Read the diff again where a finding turns on what the code actually does. Do not add new findings — only validate or challenge existing ones."
    },
    {
      "name": "validate_b",
       "role": "code-reviewer-b",
       "prompt_template": "Two independent code reviews of {task} were produced.\n\nReview from Reviewer A:\n<<reviewer_a output>>\n\nReview from Reviewer B:\n<<reviewer_b output>>\n\nYou are Reviewer B. Cross-validate Reviewer A's findings:\n1. **Agree** — which of Reviewer A's findings do you confirm as valid? Briefly state why.\n2. **Disagree** — which of Reviewer A's findings are incorrect, overstated, or based on a misreading? Cite the code or docs that support your position.\n3. **Missed** — valid issues Reviewer A caught that you missed.\n4. **Retract** — items from your own review you now believe are wrong after seeing Reviewer A's perspective.\n\nBe specific. Cite file:line references. Read the diff again where a finding turns on what the code actually does. Do not add new findings — only validate or challenge existing ones."
    }
  ]
}
```

### Phase 3 — Synthesize

Interpolate all four prior outputs plus the three model identifiers:

```json
{
  "task": "Synthesis for <REPO>#<PR-NUMBER>",
  "mode": "blocking",
  "stages": [
    {
      "name": "synthesizer",
      "role": "code-review-synthesizer",
      "prompt_template": "Two independent reviewers reviewed {task}, then cross-validated each other's work. The four outputs:\n\nReviewer A original review:\n<<reviewer_a output>>\n\nReviewer B original review:\n<<reviewer_b output>>\n\nReviewer A's validation of Reviewer B's review:\n<<validate_a output>>\n\nReviewer B's validation of Reviewer A's review:\n<<validate_b output>>\n\nProduce the final consolidated review:\n\n1. **Confirmed by both (independent)** — items both reviewers raised in their original reviews, before seeing each other. Highest confidence.\n2. **Confirmed by cross-validation** — items one reviewer raised originally that the other explicitly agreed with during validation. High confidence, but the agreement was prompted rather than independent.\n3. **Disputed** — items where cross-validation produced disagreement. Present both positions with cited evidence and label each **NEEDS ADJUDICATION**. Do NOT render a final judgment — the calling session adjudicates these.\n4. **Retracted** — items either reviewer withdrew during cross-validation. Note briefly for transparency; these are not actionable feedback.\n\nPreserve severity tiers (Must fix / Should fix / Nice to have), file:line citations, and code suggestions verbatim from the source reviews. Do not add new findings — reconcile only. If you cannot fit every input, say so explicitly at the top of your output and name which inputs you could not process in full — never drop findings silently. Begin with: **[Reviewed by <<model_a>> + <<model_b>>, cross-validated, synthesized by <<model_synth>>]**"
    }
  ]
}
```

**Watch the input size.** Phase 3 is the only stage that carries four full reviews at once, and it runs on the cheapest model in the pipeline. On a large PR the prompt can exceed the synthesizer's context, and the dangerous outcome is not an error — it is a confident-looking review that silently reconciles only the portion that fit. Estimate the combined size before spawning. If it is close to the limit, split the work rather than truncating: run one synthesis pass per severity tier (Must fix first) and concatenate the results, or drop the retracted section from the input since it is not actionable feedback. The prompt also asks the synthesizer to declare incomplete processing, but treat that as a backstop, not the primary control.

### Adjudication

After synthesis, every **NEEDS ADJUDICATION** item is resolved with cited evidence before posting. The synthesizer is intentionally a cheap structural model and does not resolve disputes — adjudication is the one piece of original review judgment left, so it belongs on the strongest model available.

Normally that is the calling session, which adjudicates directly. If the calling session is running on a weaker model than the reviewers, do not adjudicate in place: spawn one more stage on `code-reviewer-a` with the disputed items, both positions, and the diff, and have it decide. Note in the summary that adjudication ran as a separate stage, since that stage shares a model family with Reviewer A and is therefore not a neutral arbiter of a dispute Reviewer A raised.

Disputed items are promoted to the higher severity tier unless the adjudicator finds compelling evidence to downgrade.

## Failure Handling

**A reviewer stage fails at runtime** (as opposed to regional unavailability, which the fallback roster handles): retry it once. On a second failure, proceed with the single surviving review and label the final output single-source rather than blocking the review entirely.

**Both reviews succeed but cross-validation cannot complete** (a reviewer model becomes unavailable for Phase 2, or only one validation pass returns): retry the missing validation pass once, then degrade to direct synthesis of the two independent reviews. In this degraded mode:

- Only **Confirmed by both (independent)** applies as the high-confidence tier. **Confirmed by cross-validation** and **Retracted** do not apply, since no prompted agreement or retraction occurred.
- Items raised by only one reviewer are presented as single-reviewer findings — neither promoted by confirmation nor removed by retraction.
- Conflicting findings cannot be resolved via cross-validation, so the calling session adjudicates them directly, the same as **NEEDS ADJUDICATION** items.
- If exactly one validation pass completed, use it: annotate items in that direction as cross-validated and treat the missing direction as un-validated.
- Disclose the degrade in the top-level summary and drop `cross-validated` from the attribution tag (e.g. `**[Reviewed by claude-opus-5 + gpt-5.6-sol, synthesized by claude-sonnet-5]**` — note: cross-validation unavailable).

Two independent cross-family reviews still outrank a single-model review, so this degrade is preferred over falling back to single-model when both reviews exist.

## Posting the Review

Post the synthesized-and-adjudicated output as a single GitHub/GitLab review. Every attribution line uses the configured model identifiers verbatim; the examples below use the roster current as of 2026-07:

- **Top-level summary** uses the full attribution, e.g. `**[Reviewed by claude-opus-5 + gpt-5.6-sol, cross-validated, synthesized by claude-sonnet-5]**`. Lead with the merge decision in tier-ordered sections (Must fix / Should fix / Nice to have), reference the inline comments rather than restating them, note process concerns that do not fit on any line, and acknowledge what is working.
- **Inline comments** carry the attribution of whichever reviewer(s) originally raised the point — Reviewer A, Reviewer B, or both (for items both raised independently) — plus a one-line synthesis note, e.g. `(synthesis: claude-sonnet-5)` at the end of the attribution line.
- **Cross-validation-confirmed items** use the joint attribution with a parenthetical note — e.g. `**[Reviewed by claude-opus-5 + gpt-5.6-sol]** (confirmed in cross-validation)` — distinguishing them from items both reviewers raised independently.
- **Retracted items** are not posted as inline comments. They appear only in the summary, for transparency.
- **Disputed items** are posted with both positions noted and the calling session's adjudication.
- The calling session may add its own pass over the diff if it sees something both reviewers missed; those comments use the calling session's own attribution and are clearly marked as not part of the adversarial pair.

Never post a review comment without an AI attribution line. Comment mechanics — inline vs summary, code suggestions, citing docs — are covered in [references/review-checklist.md](references/review-checklist.md).

## Single-Model Fallback

When skipping adversarial review, perform a normal single-pass review on the calling session's own model. Apply the same checklist — severity tiers, file:line citations, code suggestions where concrete — and attribute every comment with `**[Reviewed by <identifier>]**`, where `<identifier>` is the calling session's configured model taken from its agent config or `--model`, not the model's own guess about itself (e.g. `**[Reviewed by claude-opus-5]**`). The multi-model attribution format does not apply when only one model reviewed the PR.

Prefer the strongest model available for this path: a single reviewer has no counterweight, so its blind spots go straight into the review.

When the fallback is due to no second model family being available (rather than a trivial PR or explicit opt-out), state that explicitly in the top-level summary — e.g. "Adversarial review was unavailable: no non-Anthropic reviewer model was reachable in this environment. This is a single-model review." — so the absence of cross-family review is visible to the author.
