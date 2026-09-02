# Spec — AIRgents of Change (Prototype)

- **Status:** ready-for-agent (not yet split into work tickets)
- **Source discovery:** `docs/session-transcripts/2026-09-02T175136-0400.ndrollin.Kiro.AIRgents-of-Change-Discovery.md`
- **Glossary:** `CONTEXT.md` — this spec uses those canonical terms.
- **Decisions of record:** `docs/adr/0001`–`0006`.
- **Deployment:** GCP candidates in `docs/planning/gcp-service-mapping.md`; infrastructure deferred to a separate session.

> Scope note: this is the **constrained, framework-shaped prototype** (ADR-0001). The domain
> model and module seams are designed as if for the full framework, but the built surface is a
> single vertical slice: configure → run → observe → export. Breadth beyond that is out of
> scope for the prototype and may be fleshed out as time allows.

---

## Problem Statement

A researcher studying social collective action needs to run controlled experiments in which
LLM-driven Agents hold and revise positions on a proposition while their access to peers and
to background information is deliberately unequal. Today there is no tool that lets them
configure such a society, run it reproducibly, watch it unfold, and export the results.
Doing this by hand — wiring prompts, tracking who-can-see-what, sequencing turns, staying
within an LLM provider's rate limits, and collecting per-turn data — is slow, error-prone,
and not reproducible.

## Solution

A full-stack application ("AIRgents of Change") that lets a researcher, through a dashboard,
define an **Experiment** (Agents with **Roles** and **Personas**, a **Network** of directed
**Edges**, **Context Shells** of gated information, a proposition, and **Orchestrator**
settings), execute one or more reproducible **Runs**, observe each **Run** live as it
advances through **Rounds**, and view and export the resulting **Dataset**.

The anchor scenario is **opinion dynamics / consensus under unequal information** (ADR-0001):
each Round, every Agent observes what it is permitted to see, optionally sends a **Message**,
and updates its **Stance** (a numeric position + confidence + rationale). A deterministic
**Orchestrator** ends the Run on **Convergence** or at a maximum Round count. Agent reasoning
is powered by the ASU Research Computing OpenAI-compatible gateway (LiteLLM-backed), accessed
through a single shared, rate-limited **ProviderClient**.

## User Stories

### Experiment configuration

1. As a researcher, I want to create an Experiment, so that I can define a reusable study
   design.
2. As a researcher, I want to name and describe an Experiment, so that I can find and
   recognize it later.
3. As a researcher, I want to state the proposition Agents hold a Stance on, so that the
   study has a clear subject.
4. As a researcher, I want to create Roles (goal + task instructions), so that I can define
   what Agents are trying to achieve.
5. As a researcher, I want to create Personas (behavioral styles), so that I can vary how
   Agents pursue their goals independently of the goal itself.
6. As a researcher, I want to instantiate Agents and assign each a Role and a Persona, so
   that each Agent is a distinct Role × Persona participant.
7. As a researcher, I want to set each Agent's initial Stance, so that a Run starts from a
   defined position distribution.
8. As a researcher, I want to define Context Shells holding background information, so that
   information can be unevenly distributed.
9. As a researcher, I want to assign Shells to Agents, so that different Agents begin with
   different knowledge.
10. As a researcher, I want to choose a Network Preset (e.g. `no-connections`, `pair-couple`,
    `small-world`), so that I can start from a common topology.
11. As a researcher, I want to set Network density where a Preset supports it, so that I can
    tune connectivity.
12. As a researcher, I want to apply Override layers at network-wide, Role-group, and
    individual scales, so that I can customize peer visibility at multiple scales.
13. As a researcher, I want Edges to be directed, so that I can express asymmetric access
    (A sees B without B seeing A).
14. As a researcher, I want to select a default Model for the Experiment, so that Agents are
    powered by a chosen LLM.
15. As a researcher, I want to override the Model per Role, so that I can compare cohorts
    running on different LLMs.
16. As a researcher, I want to configure the update order (`synchronous`, `sequential`,
    `random`), so that I can study synchronous vs. asynchronous updating.
17. As a researcher, I want to configure the Memory window, so that I can vary how much
    history an Agent's reasoning includes.
18. As a researcher, I want to configure the Orchestrator termination settings (convergence
    threshold, consecutive-Round count, and maximum Rounds), so that I control when a Run
    ends.
19. As a researcher, I want to validate an Experiment before running it, so that
    misconfigurations are caught early with clear messages.
20. As a researcher, I want to edit and duplicate Experiments, so that I can iterate on a
    design.

### Running

21. As a researcher, I want to start a Run from an Experiment, so that I can execute the
    study.
22. As a researcher, I want the Run to start immediately and execute in the background, so
    that a long Run does not block the interface.
23. As a researcher, I want each Run to record its Seed, so that a Run is reproducible given
    the same Experiment, Seed, and Model set.
24. As a researcher, I want to set or reuse a Seed, so that I can repeat a specific Run.
25. As a researcher, I want to run the same Experiment multiple times, so that I can study
    variability across Runs.
26. As a researcher, I want to see a Run's status (pending, running, converged, max-rounds,
    failed), so that I know where it stands.
27. As a researcher, I want to stop a running Run, so that I can abort a study that is not
    useful.
28. As a researcher, I want the system to respect the provider's rate limits, so that Runs do
    not abuse the shared LLM gateway.
29. As a researcher, I want a Run to survive occasional malformed LLM output, so that one bad
    response does not end the study.

### Observation

30. As a researcher, I want to watch a Run advance Round by Round live, so that I can see
    behavior emerge.
31. As a researcher, I want to see each Agent's Stance per Round, so that I can track opinion
    trajectories.
32. As a researcher, I want to see Agents' rationales and Messages, so that I understand the
    qualitative story behind Stance changes.
33. As a researcher, I want a live convergence indicator, so that I can see how close the
    group is to consensus.
34. As a researcher, I want a Round Record flagged when an Agent's response could not be
    parsed, so that I can spot data quality issues.
35. As a researcher, I want a network visualization, so that I can see the topology of peer
    access at a glance.
36. As a researcher, I want nodes colored by Role-group and badged by Persona, so that I can
    identify groups visually.
37. As a researcher, I want to toggle between "peer access" (Edges) and "information access"
    (Shell membership) views, so that I can inspect each access mechanism separately.
38. As a researcher, I want the visualization to reflect the current Stance distribution, so
    that I can see polarization or convergence spatially.

### Data and export

39. As a researcher, I want to define and manage the Seed (initial) Dataset — proposition,
    Shell contents, and initial Stances — so that a Run has a defined starting point.
40. As a researcher, I want to map background information into Shells easily, so that setting
    up unequal information is not tedious.
41. As a researcher, I want the Intermediate Dataset (per-Round log of Stances and Messages)
    to be observable, so that I can inspect a Run in progress.
42. As a researcher, I want to view the Final (result) Dataset — full per-Round time series
    plus a summary — so that I can analyze the outcome.
43. As a researcher, I want the summary to report whether and when the Run converged, the
    final spread, and breakdowns by Role and Persona, so that I can interpret results
    quickly.
44. As a researcher, I want to export the Final Dataset as JSON, so that I have a complete,
    faithful record.
45. As a researcher, I want to export the per-Round Stance table as CSV, so that I can
    analyze it in standard tools.

### Access, security, and operation

46. As a researcher, I want the application restricted to asu.edu SSO, so that only
    authorized users can reach it.
47. As a researcher, I want the backend to reject requests without a valid identity, so that
    the API is protected even behind the edge proxy.
48. As an operator, I want the provider API key kept server-side only, so that it is never
    exposed to the browser.
49. As an operator, I want clear server-side logs of Run progress and provider retry/`429`
    behavior, so that I can diagnose issues.
50. As a researcher, I want clear, user-friendly error messages when something fails, so that
    I can correct configuration or retry.

## Implementation Decisions

### Domain and engine (ADR-0002)

- The engine advances a Run in discrete **Rounds**. Update order is configurable
  (`synchronous` default, `sequential`, `random`).
- **Observation model:** in Round *N* an Agent observes, from its inbound Edges, in-neighbors'
  **Stance and Messages as of Round *N−1***, plus the Context Shells it holds and its own
  Memory window; it then emits its new Stance (*N*) and an optional Message (*N*). Messages are
  seen one Round later, never same-Round.
- **Stance** is a numeric position, a confidence, and a free-text rationale. **Convergence**
  is measured on the numeric position: spread below a configured threshold for a configured
  number of consecutive Rounds.
- **Memory window** (how many prior Rounds inform reasoning) is configurable and small by
  default.

### Model and provider (ADR-0004)

- An Experiment sets a default **Model**, optionally overridden per **Role**; the resolved
  Model set is recorded on each Run for reproducibility.
- All Agent LLM calls route through a single shared **`ProviderClient`** that wraps the ASU RC
  LiteLLM gateway. It enforces one configurable, global rate limit (bounded async queue +
  token-bucket throttle) and handles `429` with exponential backoff + jitter, honoring
  `Retry-After`. The throttle is global across all Models and Runs; per-Model rate controls
  are out of scope.
- Available Models are discovered from the gateway's `/v1/models` and offered for selection.

### LLM I/O format (ADR-0005)

- The **model-facing format is a labeled Markdown template** parsed into the canonical Stance
  schema; JSON is the internal/stored/API representation.
- Parsing failures get **one repair retry** (re-prompt with the parse error); if still failing,
  the Agent's prior Stance is **carried forward**, the Round Record is flagged (e.g.
  `unparsed`), and the Run continues.
- Markdown formatting/parsing lives behind the `ProviderClient` so provider-side
  structured-output features can be adopted later if the gateway supports them.

### Execution and observation (ADR-0003)

- A Run executes behind a **`RunExecutor`** seam; the prototype implementation is an
  in-process asyncio background task. Starting a Run returns immediately.
- The executor appends **Round Records** to the Intermediate Dataset through the repository
  seam; that append-only log is the single source of truth, and the Final Dataset is derived
  from it.
- Live observation is delivered via **Server-Sent Events**; REST polling of Run status is the
  fallback.

### Orchestrator

- The **Orchestrator** is a deterministic monitor evaluating a pluggable termination
  predicate: `converged(threshold, consecutive_rounds) OR round ≥ max_rounds`. An LLM-driven
  Orchestrator is out of scope.

### Persistence (ADR-0003 / AGENTS.md)

- All storage sits behind a **`Repository`** interface (`findAll/findById/create/update/
  delete`) covering **Experiments** and **Runs** (including their Datasets). The concrete
  engine is unchosen and deferred; selecting it is an explicit ask-first decision.
- The Intermediate Dataset is durable-by-append through the repository so a crash mid-Run is
  not fatal and live observation reads the same source as the export.

### API surface (ADR uses the AGENTS.md standard response envelope)

- REST resources: **Experiments** (CRUD); **Runs** as a sub-resource of an Experiment
  (start, get status, get/stream Dataset, stop); read-only **presets** and **models** helper
  endpoints (the latter proxying `/v1/models`).
- Responses use the standard envelope (success indicator, data payload, error message,
  pagination metadata where applicable). Input is validated at the boundary with
  schema-based validation; validation failures return clear, user-friendly messages.
- Live Round Records stream over an SSE endpoint on the Run resource.

### Authentication (ADR-0006)

- The application is fronted by **Cloudflare Access restricted to asu.edu SSO**. The FastAPI
  backend **independently validates the signed Access JWT** (signature via the edge JWKS,
  audience, asu.edu identity claim) on every request via an injected auth dependency (defense
  in depth).
- Authorization for the prototype is "any authenticated asu.edu principal"; the principal is
  captured through the auth seam for future per-user ownership. The provider API key is
  server-side only.
- Cloudflare / GKE / Terraform specifics are deferred to a separate infrastructure session.

### Frontend

- TypeScript/React using the ASU Unity Design System components.
- Screens: **Experiment Builder** (Agents, Roles, Personas, Shell assignment, Network Preset +
  overrides, Model selection, engine + Orchestrator settings); **Network Overview** (directed
  graph; color by Role-group, badge by Persona; toggle between peer-access Edges and
  information-access Shell membership; reflects current Stance distribution); **Run Monitor**
  (SSE-fed Stance trajectories + convergence indicator); **Dataset Manager** (Seed mapping,
  live Intermediate observation, Final view + JSON/CSV export).

## Testing Decisions

A good test asserts **externally observable behavior**, not internals: given an Experiment and
scripted Agent responses, a Run reaches the expected end-state and produces the expected
Dataset shape and access behavior. Tests must not assert on private structures, prompt
strings, or call sequencing beyond what is observable at the seam.

- **Primary seam — the FastAPI HTTP API (backend integration tests).** Configure an
  Experiment, start a Run, observe the Dataset, and assert behavior end-to-end through the
  public API. Representative cases:
  - A Run **converges** and terminates with a `converged` status when scripted Stances draw
    together.
  - A Run terminates at **`max_rounds`** when Stances never converge.
  - The **Dataset** has the expected per-Round shape (Stance per Agent per Round; Messages;
    summary with convergence, final spread, Role/Persona breakdowns).
  - **Access restrictions hold**: an Agent's observation reflects only its inbound Edges and
    assigned Shells (and Messages are seen one Round later).
  - **Parse-failure handling**: a scripted malformed response triggers one repair retry, then
    carry-forward with the Round Record flagged `unparsed`; the Run continues.
  - **Reproducibility**: same Experiment + Seed + scripted Model yields identical Round
    Records.
  - **Auth**: requests without a valid asu.edu JWT are rejected; valid ones succeed.

- **Injected boundaries (deterministic doubles, not new seams):**
  1. A **fake `ProviderClient`** returning scripted Markdown responses per Agent per Round —
     makes engine behavior deterministic and hermetic, and exercises Markdown parsing,
     repair-retry, and carry-forward without the network. The real ProviderClient's throttle/
     backoff logic is unit-tested separately against a fake transport (assert `429` backoff and
     global rate limiting without hitting the gateway).
  2. An **in-memory `Repository`** — keeps the persistence engine deferred while giving the
     API seam real read/write behavior.

- **Frontend — React Testing Library** at the component/page boundary with the API mocked
  (MSW): assert the Builder validates and submits an Experiment, the Run Monitor renders
  streamed Round Records, and the Dataset Manager triggers JSON/CSV export. One thin
  **Playwright E2E** covers the critical flow (configure → run → observe → export) if time
  allows.

- **Prior art:** none yet — this establishes the seam conventions for the repository. Follow
  the `tdd` skill's red→green loop and the `testing` steering's coverage floor and required
  test types.

## Out of Scope

- Concrete persistence engine, external job runner, frontend hosting/CDN, and all
  Cloudflare/GKE/Terraform infrastructure (separate infrastructure/Terraform session).
- Per-Model rate controls (single shared throttle only; deferred to a later feature cycle).
- Per-Agent Model selection (per-Role override is the finest granularity in the prototype).
- LLM-driven Orchestrator (deterministic predicate only).
- Summarized/full-history Agent memory (windowed memory only).
- Real-time/continuous-time simulation (discrete Rounds only).
- Provider embeddings or any non-chat-completions capability.
- Finer-grained RBAC and per-user data isolation (principal is captured but not yet enforced
  as ownership).
- Cost modeling and pricing estimates.
- Collective-action scenarios other than opinion dynamics / consensus under unequal
  information.

## Further Notes

- Scale target: 10 Agents for the prototype with seams that keep 50+ reachable; the shared
  throttle and windowed memory are the primary levers that keep token cost and provider load
  bounded at scale.
- The framework-shaped seams (`ProviderClient`, `RunExecutor`, `Repository`, pluggable
  Orchestrator predicate, Preset generators, Override layers) are deliberate extension points;
  fleshing out breadth within them is the "as time allows" path from ADR-0001.
- This spec is intentionally not published to GitHub Issues; the issue queue is reserved for
  work tickets to be derived from this spec in a later session.
