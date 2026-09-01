---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents, then cross-validates each axis against the other before aggregating findings with confidence stratification. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards**: does the code conform to this repo's documented coding standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context. Each sub-agent then cross-validates the other's findings before the calling session aggregates results with confidence stratification.

The issue tracker should have been provided to you. If `docs/agents/issue-tracker.md` is missing, tell the user to run `/setup-matt-pocock-skills`.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, `main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside two parallel sub-agents.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is. If they say there isn't one, the **Spec** sub-agent will skip and report "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Phase 1 — Independent review (parallel)

Spawn both sub-agents simultaneously. Each reviews only its own axis. Neither is given the other axis's materials, and each is told explicitly not to coordinate.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant: (a) every place the diff violates a documented standard — cite the standard (file + rule) and use severity **Must fix** or **Should fix**; (b) any baseline smell you spot — name it, quote the hunk, and use severity **Should fix** or **Nice to have**. Documented-standard breaches can be hard violations; baseline smells are always judgement calls; a documented repo standard overrides the baseline. Skip anything tooling enforces. Under 400 words. Do not coordinate with or reference any other reviewer — produce your axis independently."

**Spec sub-agent prompt** should include:

- The diff command and commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing or partial — severity **Must fix**; (b) behaviour in the diff that wasn't asked for (scope creep) — severity **Should fix**; (c) requirements that look implemented but where the implementation looks wrong — severity **Must fix**. Quote the spec line for each finding. Under 400 words. Do not coordinate with or reference any other reviewer — produce your axis independently."

If the spec is missing, skip the Spec sub-agent and note this in the final report. Also skip Phase 2 cross-validation for that axis.

### 5. Phase 2 — Cross-axis validation (parallel)

After both Phase 1 outputs are collected, spawn both sub-agents again simultaneously — each validating the *other* axis's findings. Pass both Phase 1 outputs to each sub-agent verbatim. The sub-agents may re-read the diff to test a finding.

**The five validation outcomes** apply to every finding the other sub-agent raised:

- **Agree** — only if the finding can be independently verified from the diff and code alone, using only the materials provided to this reviewer. State the specific code evidence. A reviewer must never mark a finding Agree unless the evidence required to independently validate that finding is available in its provided context.
- **Disagree** — the finding is incorrect, overstated, or based on a misreading of the code. Cite the specific file:line evidence.
- **Missed** — a finding of the other axis's type that is independently observable from this reviewer's own provided materials. The finding must be raisable without any materials outside what this reviewer was given in Phase 1. A Standards reviewer may flag a code-observable behavioral issue the Spec reviewer missed; it may not claim a missing requirement without the spec. A Spec reviewer may flag an obvious code quality issue apparent from the diff; it may not claim a missed documented-standard violation without the standards docs.
- **Retract** — a finding from this reviewer's own Phase 1 output that the other reviewer's evidence reveals to be wrong.
- **Context insufficient to validate** — the finding turns on materials not provided to this reviewer (spec content, acceptance criteria, documented standards, or smell definitions). Name the finding and state what material is missing. Do not agree or disagree without evidence.

**Standards sub-agent cross-validation prompt** should be constructed by the calling session as follows, with `<<standards_phase1_output>>` and `<<spec_phase1_output>>` replaced by the verbatim Phase 1 outputs before the prompt is sent:

```
You are the Standards reviewer performing cross-axis validation.

Standards Phase 1 output:
<<standards_phase1_output>>

Spec Phase 1 output:
<<spec_phase1_output>>

Apply the following five validation outcomes to every finding in the Spec Phase 1 output:

- Agree — only if the finding can be independently verified from the diff and code alone, using only the materials provided to you (the diff, commit list, standards docs, and smell baseline). State the specific code evidence. You must never mark a finding Agree unless the evidence required to independently validate it is available in your provided context.
- Disagree — the finding is incorrect, overstated, or based on a misreading of the code. Cite the specific file:line evidence.
- Missed — a finding of the Spec axis type that is independently observable from your own provided materials. The finding must be raisable without any materials outside what you were given. You may flag a code-observable behavioral issue the Spec reviewer missed; you may not claim a missing requirement without the spec.
- Retract — a finding from your own Standards Phase 1 output that the Spec reviewer's evidence reveals to be wrong.
- Context insufficient to validate — the finding turns on spec content, acceptance criteria, or requirement text not provided to you. Name the finding and state what material is missing. Do not agree or disagree without evidence.

You do not have access to the originating spec or issue. For any Spec finding that requires spec content to evaluate — especially missing-requirement findings — you must mark it Context insufficient to validate rather than agreeing or disagreeing without evidence.

For your own Standards Phase 1 findings, note any you now wish to Retract in light of the Spec reviewer's output. Do not add new findings — only validate or challenge existing ones. Be concise but address every finding.
```

**Spec sub-agent cross-validation prompt** should be constructed by the calling session as follows, with `<<standards_phase1_output>>` and `<<spec_phase1_output>>` replaced by the verbatim Phase 1 outputs before the prompt is sent:

```
You are the Spec reviewer performing cross-axis validation.

Standards Phase 1 output:
<<standards_phase1_output>>

Spec Phase 1 output:
<<spec_phase1_output>>

Apply the following five validation outcomes to every finding in the Standards Phase 1 output:

- Agree — only if the finding can be independently verified from the diff and code alone, using only the materials provided to you (the diff, commit list, and spec). State the specific code evidence. You must never mark a finding Agree unless the evidence required to independently validate it is available in your provided context.
- Disagree — the finding is incorrect, overstated, or based on a misreading of the code. Cite the specific file:line evidence.
- Missed — a finding of the Standards axis type that is independently observable from your own provided materials. The finding must be raisable without any materials outside what you were given. You may flag an obvious code quality issue apparent from the diff; you may not claim a missed documented-standard violation without the standards docs.
- Retract — a finding from your own Spec Phase 1 output that the Standards reviewer's evidence reveals to be wrong.
- Context insufficient to validate — the finding turns on documented standards, coding conventions, or smell definitions not provided to you. Name the finding and state what material is missing. Do not agree or disagree without evidence.

You do not have access to the coding standards documents or smell baseline. For any Standards finding that requires those documents to evaluate, you must mark it Context insufficient to validate rather than agreeing or disagreeing without evidence.

For your own Spec Phase 1 findings, note any you now wish to Retract in light of the Standards reviewer's output. Do not add new findings — only validate or challenge existing ones. Be concise but address every finding.
```

### 6. Aggregate with confidence stratification

The calling session aggregates all four outputs. Each finding carries its axis tag [Standards] or [Spec] and its original severity tier (Must fix / Should fix / Nice to have) from Phase 1. The confidence tier is determined as follows:

**Tier 1 — Confirmed by both independently.**
Both sub-agents raised the same finding in Phase 1, before seeing each other. Highest confidence. Two findings qualify for this tier only when they identify the same underlying defect with materially equivalent diagnosis and remediation — not merely when they share the same code location, observable fact, or evidentiary basis. Findings that cite the same evidence but represent different defects, or imply different fixes, remain separate findings and proceed through normal cross-validation and confidence assignment.

**Tier 2 — Confirmed by cross-validation.**
One reviewer raised the finding in Phase 1; the other Agreed in Phase 2 with cited code evidence. High confidence. A finding where cross-validation returned *Context insufficient to validate* does not qualify for this tier — the absence of a challenge is not confirmation. Tier 2 requires a positive Agree with stated evidence.

**Tier 3 — Disputed / NEEDS ADJUDICATION.**
Cross-validation produced a Disagree with cited evidence. Present both positions. The calling session adjudicates with cited code or spec evidence before presenting the final report. Disputed findings default to the higher severity tier unless the adjudicator has explicit evidence to downgrade.

**Tier 4 — Single-reviewer, validation not possible.**
Two cases land here: (a) the cross-axis reviewer marked *Context insufficient to validate*, meaning independent validation was not possible with available materials; (b) findings not addressed in cross-validation. These retain their Phase 1 severity and are surfaced as-is. They are not elevated to Tier 2 simply because a cross-validation pass was attempted.

**Retracted** — items either reviewer withdrew in Phase 2. Listed in the summary for transparency; not posted as actionable findings.

**If the four outputs are too large to aggregate in one pass:** split by severity tier — Must fix first — and concatenate. Never truncate silently; if aggregation is incomplete, state explicitly which findings were not processed.

Present findings in tier order (Tier 1 first) within each severity level. Keep the [Standards] / [Spec] axis tags on every finding so the two axes remain distinguishable throughout.

End with a summary: total findings per axis, per confidence tier, the worst finding per axis, and any degraded or retracted items.

Do **not** pick a single worst finding across both axes: that's the reranking the axis separation exists to prevent.

## Skip conditions

Run Phase 2 cross-validation by default. Skip it — and run Phase 1 only — for:

- **Trivial mechanical changes**: typos, doc-only edits, single-line config tweaks, dependency bumps with no behavior change.
- **Explicit user opt-out**: "simple review", "quick review", "single model is fine".
- **Re-review after feedback**: verify the deltas against the prior review rather than running a fresh cross-validation pass.

## Failure modes

**A Phase 1 sub-agent fails**: retry once. On second failure, skip Phase 2 entirely (no cross-validation to do) and proceed with the single surviving review labeled single-source in the summary.

**A Phase 2 validation pass fails**: retry once. On second failure, run aggregation without that direction. Annotate which direction was un-validated. The surviving validation pass is used; items in the missing direction land at Tier 4. Two independent Phase 1 reviews without any cross-validation still outrank a single Phase 1 pass — do not fall back to single-axis review when both Phase 1 outputs exist.

## Sub-agent and model call count

| Scenario | Phase 1 calls | Phase 2 calls | Total |
|---|---|---|---|
| Full run | 2 | 2 | 4 |
| One Phase 2 pass fails | 2 | 1 | 3 |
| Both Phase 2 passes fail | 2 | 0 | 2 |
| Skip condition applies | 1 | 0 | 1 |

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other. The confidence tiers within each axis express how well-validated a finding is; they do not override the axis separation.
