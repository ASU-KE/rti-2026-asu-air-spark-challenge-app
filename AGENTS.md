# Agent Instructions

## Core Principles

1. **Agent-First** — Delegate to specialized agents for domain tasks
2. **Test-Driven** — Write tests before implementation; cover confirmed seams qualitatively, not to a percentage
3. **Security-First** — Never compromise on security; validate all inputs
4. **Immutability** — Always create new objects, never mutate existing ones
5. **Plan Before Execute** — Plan complex features before writing code

## Issue tracker

Issues are tracked in GitHub Issues for this repository. See `docs/agents/issue-tracker.md`.

## Triage labels

Triage uses five canonical skill labels. See `docs/agents/triage-labels.md`.

## Domain docs

This repository uses a single-context domain documentation layout. See `docs/agents/domain.md`.

Delivery: one slice → one branch → one ≤300-line PR to main, TDD atomic commits, review gates before human review — see the delivery pipeline in .opencode/skills/git-workflow.
