# Context: AIRgents of Change

A researcher-facing harness for running computational experiments with networked,
persona-based LLM agents. The anchor scenario is **opinion dynamics / consensus under
unequal information**: agents hold positions on a proposition and update them over time
while their access to peers and to background information is deliberately unequal.

This file is a glossary of the project's ubiquitous language. It contains no
implementation detail. When code, issues, tests, or specs name a concept below, they use
the term as defined here and avoid the listed synonyms.

## Glossary

### Agent
A single LLM-driven participant in the simulation. An Agent is fully described by its
**Role**, its **Persona**, its position in the **Network**, and the **Context Shells** it
holds. Agents observe, optionally communicate, and update their **Stance** each **Round**.

### Role
An Agent's *goal and task instructions* — what it is trying to achieve (e.g. "advocate for
the proposition", "seek the truth", "maximize group agreement"). A Role is about
**objective**, never about behavioral style.
- Avoid using "role" loosely to mean persona, network position, or job title.

### Persona
An Agent's *behavioral style or disposition*, independent of its goal (e.g. "stubborn",
"agreeable", "contrarian", "high-openness"). Two Agents with the same Role but different
Personas pursue the same objective in different ways.
- Role and Persona are orthogonal: an Agent is a Role × Persona × Network position.

### Stance
The position an Agent holds on the proposition at a given **Round**. A Stance is quantified
(a numeric position with an associated confidence) and accompanied by a short free-text
rationale. Consensus and convergence are measured on the quantified position; the rationale
carries the qualitative story.
- Avoid "opinion" or "belief" as separate terms; the canonical term is Stance.

### Round
One discrete time step (a "tick") of the simulation. In a Round, Agents observe what they
are permitted to see, optionally communicate, and update their Stance. Rounds are the
engine's backbone; continuous/real-time behavior is out of scope.

### Update order
How Agents' Stance updates are sequenced within a Round: all-at-once (**synchronous** — every
Agent reads the prior Round's state and writes simultaneously), one-at-a-time in fixed order
(**sequential**), or one-at-a-time in shuffled order (**random**). Synchronous is the default.

### Memory window
How many prior Rounds an Agent's reasoning includes when it observes and updates. It is
configurable and small by default; the window size is itself a research variable.

### Model
The LLM that produces an Agent's responses, chosen from those the provider exposes (e.g.
Qwen, Gemma, Minimax, Llama, Kimi, in various sizes). An Experiment sets a default Model,
optionally overridden per Role; the resolved Model set is recorded on each Run for
reproducibility. All Model calls share one provider rate limit regardless of which Model is
selected.

### Network
The directed graph of peer visibility among Agents. An **Edge** from A to B means A can see
B's Stance and/or messages. Direction matters: access can be asymmetric. The Network is
generated from a **Preset** and refined by **Override layers**.
- "Network" refers to peer visibility only, never to shared-document access (that is a Shell).

### Edge
A directed connection in the Network granting one Agent visibility of another's Stance and
messages.

### Preset
A named generator that produces a starting Network topology and density (e.g.
`no-connections`, `pair-couple`, `small-world`).

### Override layer
An adjustment applied on top of a Preset to customize the Network at a given scale. Layers
apply in precedence order: **network-wide → role-group → individual**.

### Context Shell (Shell)
A layer of shared background information gated by access. A Shell governs *document/context
visibility*, distinct from the Network's peer visibility. Unequal information is expressed
by assigning Agents different Shells. An Agent's total knowledge is the union of the Shells
it holds and what its inbound Edges expose.
- "Access layer" is a synonym; the canonical term is Context Shell.

### Experiment
The *design* of a study: the Agents (with their Roles, Personas, Network, and Shells), the
proposition, and the Orchestrator settings. An Experiment is a reusable template. One
Experiment produces many **Runs**.
- Avoid using "experiment" to mean a single execution — that is a Run.

### Run
One *execution* of an Experiment. A Run advances through Rounds until the Orchestrator
terminates it, producing one result **Dataset**. A Run records a **Seed** so that, given the
same Experiment, Seed, and model, it is reproducible.

### Seed
The random seed captured by a Run that fixes all stochastic choices (e.g. update order,
Preset generation), making a Run reproducible.

### Message
Content one Agent communicates to peers it shares an Edge with during a Round. Distinct from
a Stance: a Message is what an Agent *says*, a Stance is the position it *holds*.

### Convergence
The condition where the spread of Agents' Stances falls below a threshold for a sustained
number of Rounds. Convergence (or reaching the maximum Round count) is what ends a Run.

### Orchestrator
The component that monitors a Run and decides when it terminates. For the prototype it is a
**deterministic monitor** evaluating a termination predicate — Convergence *or* maximum
Rounds reached. The predicate is pluggable so an LLM-driven Orchestrator can replace it
later.

### Dataset
The data of a Run, in three stages:
- **Initial (seed) Dataset** — the proposition, the background information mapped into
  Context Shells, and each Agent's starting Stance.
- **Intermediate Dataset** — an append-only, observable per-Round log of every Agent's
  Stance and Messages. The single source of truth for a Run.
- **Final (result) Dataset** — the complete per-Round time series plus a summary (whether and
  when it converged, final spread, breakdowns by Role and Persona), derived from the
  Intermediate Dataset and exportable.
