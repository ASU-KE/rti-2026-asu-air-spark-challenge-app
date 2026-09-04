
I need to create a 5-minute HTML presentation for our hackathon project on the feature/presentation branch.
Before doing anything, read the README, lessons-learned folder, docs/planning/scenario-experiment-design.md, context.md/domain glossary, relevant ADRs (Architecture Decision Records), and any existing presentation or HTML files. Use the ASU Unity Stack and write-asu-themed-document skill for the design.
The presentation should tell a simple story: the problem → what we built → multi-agent architecture → experiment/jury scenario → what worked and failed → lessons learned → what we'd improve next.
A few important requirements:
This is only a 5-minute presentation, so keep it concise and visual.
Use the Jury Scenario as the main example and follow the terminology/capitalization in context.md.
“Values” means Social Values such as Violent Crimes, Mercy of the People, etc., based only on the repo.
Confidence is on a 0–1 scale where supported by the docs.
Expand every acronym on first use, e.g. ASDLC (Agentic Software Development Lifecycle) and ADR (Architecture Decision Record).
Do not mention Kiro. Mention the actual model names/versions where documented.
Explain that orchestration had limited model options and required both vision and reasoning capabilities.
We did not complete the full run because the available models were very slow. Frame this as a hackathon time/latency limitation, not proof that the research approach failed.
Show how the Validator checks work before anything reaches a human, including failed work being resubmitted/reassigned by the Orchestrator and validated again.
Briefly cover security, latency, queuing/tickets, and relevant architecture decisions.
We are not publishing research results; this is a prototype/research exploration.
Use the lessons-learned files heavily, especially unexpected agent behavior, orchestration failures, and what we changed because of them.
Make it look like a professional PPT-style presentation in HTML: clear title/subtitle hierarchy, ASU colors, diagrams/cards instead of walls of text.
Do not create or modify anything yet. First give me:
The files you used
A suggested 5-minute story
A 6–8 slide outline
The strongest lessons learned to include
Anything I asked for that isn't supported by the repo
Once I approve the outline, we'll create the HTML.


KIRO RESPONSE:
Implementation evidence
  
  - The FastAPI scaffold and tests from origin/archive/27-backend-scaffold, including the response envelope, /health, validation handling,
  server-side provider key configuration, and their tests.
  
  Design guidance
  
  - The project-local write-asu-themed-document skill, mirrored under .opencode/skills/write-asu-themed-document/SKILL.md
  
  Suggested five-minute story
  
  Open with a concrete question rather than the technology:
  
  │ “How can we study whether artificial societies reach consensus when their goals, personalities, relationships, and information are deliberately
  unequal?”
  
  Then tell the story in this order:
  
  1. The problem: Researchers need a controlled, observable way to study collective behavior among Large Language Model (LLM) Agents.
  2. The example: A six-member Jury must reach a Guilty or Not Guilty verdict while attorneys introduce evidence and jurors communicate only through
  a ring Network.
  3. What we built: A framework-shaped prototype consisting of a detailed domain/specification corpus, an interactive configure → run → observe →
  export mock prototype, and a test-first FastAPI foundation. Be explicit that these pieces were not fully integrated.
  4. How it works: Experiments produce Runs; Runs advance through discrete Rounds; Agents update Stances using permitted Network and Context Shell
  information; a shared provider queue protects the model gateway; the deterministic Orchestrator ends the Run.
  5. How work was controlled: Small claimed tickets, test-driven development, Standards and Spec review, security review where applicable,
  continuous integration, then human review.
  6. What happened: Model latency and orchestration reliability consumed the hackathon window. The full model-backed Run was not completed. This is
  a time-and-latency limitation, not evidence against the research approach.
  7. What we learned and would change: Isolate concurrent work, validate ticket adherence, benchmark models before assigning orchestration duties,
  improve durable execution and queue observability, and run a smaller end-to-end tracer earlier.
  
  The opening and closing should both say: “Prototype and research exploration—not published research findings.”
  
  Recommended seven-slide outline
  
  ┌───────────┬──────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────────────────────┐
  │ Time      │ Slide                                │ Content and visual                                                                        │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0:00–0:20 │ 1. AIRgents of Change                │ One-sentence promise: a configurable artificial society for studying consensus under      │
  │           │                                      │ unequal information. Add a visible Prototype / research exploration badge. Minimal title  │
  │           │                                      │ slide using Arizona State University (ASU) Unity Design System styling.                   │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 0:20–1:00 │ 2. The problem, made concrete        │ Introduce the Jury Scenario: six juror Agents in a ring, two Defense and two Prosecution  │
  │           │                                      │ Agents, evidence delivered to all jurors, peer communication limited to neighbors. Use a  │
  │           │                                      │ large ring-network diagram. Show Stance + confidence (0–1) + rationale; avoid presenting  │
  │           │                                      │ simulated outcomes.                                                                       │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1:00–1:40 │ 3. What we actually built            │ Three artifact cards: Designed—glossary, specification, five Architecture Decision        │
  │           │                                      │ Records (ADRs); Prototyped—interactive configure → run → observe → export mock;           │
  │           │                                      │ Implemented—test-first FastAPI foundation with response envelope, validation, health      │
  │           │                                      │ endpoint, and server-side secret handling. Label the parts as separate and not fully      │
  │           │                                      │ integrated.                                                                               │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1:40–2:35 │ 4. Multi-agent architecture          │ Horizontal architecture diagram: Researcher → Experiment → asynchronous RunExecutor →     │
  │           │                                      │ shared ProviderClient queue/throttle → Agent Network and discrete Rounds → append-only    │
  │           │                                      │ Intermediate Dataset → deterministic Orchestrator → Server-Sent Events (SSE)              │
  │           │                                      │ monitor/export. Side callouts: Security: provider key stays server-side; input validation │
  │           │                                      │ at boundaries. Latency: bounded global queue, token-bucket throttle, 429 backoff and      │
  │           │                                      │ jitter.                                                                                   │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2:35–3:20 │ 5. Nothing reaches a human unchecked │ Use the documented process: claimed GitHub ticket → one branch → test-driven development  │
  │           │                                      │ (TDD) → Standards review + Spec review → security review when applicable → continuous     │
  │           │                                      │ integration (CI) → human pull-request review. A failed check loops back to implementation │
  │           │                                      │ and is validated again. Do not currently label this automated loop “Validator             │
  │           │                                      │ reassignment by the Orchestrator” unless additional evidence is supplied.                 │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3:20–4:20 │ 6. What worked—and what broke        │ Two-column visual. Worked: scope discipline, canonical vocabulary, test-first scaffold,   │
  │           │                                      │ readable mock, explicit provider resilience decisions. Limited us: slow available models, │
  │           │                                      │ incomplete full Run, orchestration selecting or executing the wrong work, and             │
  │           │                                      │ concurrent-work collisions. Frame latency as a hackathon constraint. Show documented      │
  │           │                                      │ model identifiers only with an evidence qualifier.                                        │
  ├───────────┼──────────────────────────────────────┼───────────────────────────────────────────────────────────────────────────────────────────┤
  │ 4:20–5:00 │ 7. Lessons and next experiment       │ Four concise improvements: benchmark vision-and-reasoning-capable models first; isolate   │
  │           │                                      │ every worker in its own clone/worktree; enforce ticket/branch checks before work starts   │
  │           │                                      │ and after validation; replace in-process execution with a durable worker queue and        │
  │           │                                      │ instrument latency/queue depth. Close with: “The prototype tested both an artificial      │
  │           │                                      │ society and an Agentic Software Development Lifecycle (ASDLC). The next step is a         │
  │           │                                      │ smaller, instrumented, end-to-end Run—not a research-results claim.”                      │
  └───────────┴──────────────────────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────┘
  
  Presentation design direction
  
  Use a self-contained HyperText Markup Language (HTML) deck with:
  
  - 16:9, one viewport per slide, keyboard navigation and fullscreen support.
  - Canonical ASU maroon, gold, grayscale, typography, light masthead, and dark footer.
  - One dominant diagram or card composition per slide.
  - No more than roughly 35–45 visible words on most slides.
  - A small source footer, but no walls of citations.
  - Clear visual status labels: Designed, Prototype, Implemented, and Not completed.
  - No fabricated charts. If a trajectory illustration is retained, label it prominently as illustrative mock data—not experimental results.
  
  Strongest lessons to include
  
  Strongly supported by repository sources
  
  1. Constrain the build, preserve the framework seams. ADR-0001 deliberately limits the hackathon to one configure → run → observe → export slice
  while retaining extension points.
  2. Determinism matters for research legibility. Discrete Rounds, prior-Round observation, Seeds, configurable update order, and bounded Memory
  windows make Runs more reproducible and understandable.
  3. Long-running model work cannot live inside one request. ADR-0003 separates asynchronous execution from observation and uses an append-only
  Dataset as the source of truth.
  4. Provider limits must shape architecture. ADR-0004 calls for one bounded global queue, configurable concurrency, token-bucket throttling, and
  429 retry handling because gateway limits are unpublished.
  5. Heterogeneous models require defensive interfaces. ADR-0005 uses labeled Markdown at the model boundary, one repair attempt, then carry-forward
  plus an unparsed flag rather than losing the entire Run.
  6. Security scope should be honest. The prototype is local-only and has no authentication, but the provider key remains server-side and external
  input is validated.
  7. Small tickets are a coordination control. The documented Agentic Software Development Lifecycle requires claim-first tickets, one branch per
  slice, TDD, review gates, green CI, and a human-approved pull request.
  8. The prototype pieces must not be mistaken for an integrated product. The interactive mock, backend scaffold, scenario document, and
  presentation live across different branches or historical refs.
  
  Valuable but only provisionally documented
  
  The current presentation records these as team-reported lessons, but its own citation says they still need confirmation:
  
  - Qwen 3 (27B) produced strong output but was very slow.
  - Qwen 3 VL 32B Thinking reportedly received a frontend ticket but produced backend work and hallucinated a branch name.
  - Parallel workflows reportedly collided in a shared repository.
  - The reported responses were separate clones per Agent thread, explicit ticket-adherence checks, a faster orchestration Model, and reduced scope.
  
  These are excellent presentation material if the team confirms the wording and model identifiers.
  
  Requested content not supported by the repo
  
  1. Exact Social Value labels. I found general examples—crime, libertarianism, and mercy—and the Jury prototype reduces Value to A or B. I did not
  find “Violent Crimes” or “Mercy of the People.” Value or Social Value is also not defined in CONTEXT.md.
  2. Validator as a named component. The repo documents Standards review, Spec review, security review, CI, and human approval. It does not define a
  capitalized Validator role.
  3. Automatic resubmission or reassignment by the Orchestrator. In the domain glossary, the Orchestrator only terminates a Run on Convergence or
  maximum Rounds. It is not documented as assigning development tickets or reassigning failed work.
  4. Limited orchestration Model choices requiring both vision and reasoning. This appears in your briefing but not in the repository files I could
  inspect.
  5. The incomplete Run and latency explanation. Your requested framing is clear and should be used. The existing deck also reports slow models, but
  there are no committed Run records, timings, logs, or benchmark results corroborating it.
  6. Confirmed actual Model versions. The existing deck names Qwen 3 (27B) and Qwen 3 VL 32B Thinking, but labels them team-reported and “to be
  confirmed.” The mock prototype lists qwen2.5-72b-instruct, llama-3.3-70b, gemma-2-27b, and kimi-k2; those menu options are not evidence that those
  Models actually ran.
  7. Substantive lessons-learned files. docs/lessons/lessons-learned.md currently contains only “agent speed” and “agent permissions / global.” The
  steering-level lessons file concerns installer and hook behavior, not the reported orchestration incidents.
  8. A consistent Stance scale. The Jury design uses a 0–1 Guilty/Not Guilty scale, while the historical mock uses −1 to +1. CONTEXT.md requires a
  numeric Stance but does not select a scale. Confidence is supportable as 0–1 in the Jury design.
  9. Published research findings. No completed model-backed Dataset or research result exists in the inspected sources. The existing visual
  prototype explicitly uses a mock JavaScript simulation.
  
  I also could not inspect live GitHub issue comments because the GitHub command-line client is unavailable in this environment. The support
  assessment above is therefore based on the locally available branch and Git refs.


