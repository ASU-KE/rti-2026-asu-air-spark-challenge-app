---
inclusion: auto
name: performance
description: Agent performance guidance — model selection, context budget, and build troubleshooting. Use when picking a model tier, planning a large refactor, or when a build fails.
---

# Performance Optimization

## Model Selection

Match model strength to the task rather than defaulting to one model:

- **Fast, low-cost model** — high-frequency worker tasks: code generation, pair programming, and worker agents in a multi-agent run.
- **Strongest available model** — architecture decisions, cross-file refactors, and tasks needing the deepest reasoning.

Choose the tier by task and let the harness resolve the concrete model, so this guidance does not go stale against a version.

## Context Budget

Avoid the last 20% of the context window for:

- Large-scale refactoring
- Feature work spanning multiple files
- Debugging complex interactions

Single-file edits, independent utilities, documentation, and simple bug fixes tolerate higher utilization.

## Build Troubleshooting

When a build fails, use the **build-error-resolver** agent: read the error messages, fix incrementally, and verify after each fix.
