
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
