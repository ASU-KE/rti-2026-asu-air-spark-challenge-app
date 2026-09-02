---
inclusion: auto
name: git-workflow
description: Git workflow guidelines for conventional commits and pull request process
---

# Git Workflow with Conventional Commits

## Overview

Create standardized, semantic git commits and Pull Requests using the Conventional Commits specification. Analyze the actual diff to determine appropriate type, scope, and message.

## Conventional Commit Format

```
<type>[optional scope]: <description>

[required body]

[optional footer(s)]
```

### Commit Types

| Type       | Purpose                        |
| ---------- | ------------------------------ |
| `feat`     | New feature                    |
| `fix`      | Bug fix                        |
| `docs`     | Documentation only             |
| `style`    | Formatting/style (no logic)    |
| `refactor` | Code refactor (no feature/fix) |
| `perf`     | Performance improvement        |
| `test`     | Add/update tests               |
| `build`    | Build system/dependencies      |
| `ci`       | CI/config changes              |
| `chore`    | Maintenance/misc               |
| `revert`   | Revert commit                  |

### Breaking Changes

```
# Exclamation mark after type/scope
feat!: remove deprecated endpoint

# BREAKING CHANGE footer
feat: allow config to extend other configs

BREAKING CHANGE: `extends` key behavior changed
```

## Generate Commit Message

Analyze the diff to determine:

- **Type**: What kind of change is this?
- **Scope**: What area/module is affected?
- **Description**: One-line summary of what changed (present tense, imperative mood, <72 chars)
- **Coauthor Trailer**: One co-author for the agent

### When to add co-authors

Add `Co-authored-by` trailers when the AI agent materially authored or modified the committed change. Skip for trivial one-liners the user wrote.

### Resolve agent

1. Identify the agent: `Claude Code`, `Codex`, `Kiro`, or `OpenCode` (whichever is running this skill).
2. Resolve emails from the registry below. **Do not guess an email.** If the agent or model is not listed, ask the user explicitly.

### Registry

Agents:

| Agent       | Email                 |
| ----------- | --------------------- |
| Claude Code | noreply@anthropic.com |
| Codex       | noreply@openai.com    |
| Kiro        | noreply@kiro.dev      |
| OpenCode    | support@open-code.ai  |

### Generator

```
Co-authored-by: Kiro <noreply@kiro.dev>
```

Append it after one blank line at the end of the commit message.

## Pull Request Workflow

When creating PRs:

1. Analyze full commit history (not just latest commit)
2. Use `git diff [base-branch]...HEAD` to see all changes
3. Draft comprehensive PR summary
4. Include test plan with TODOs
5. Push with `-u` flag if new branch

> For the full development process (planning, TDD, code review) before git operations,
> see the development workflow rule.

## Best Practices

- One logical change per commit
- Present tense: "add" not "added"
- Imperative mood: "fix bug" not "fixes bug"
- Reference issues: `Closes #123`, `Refs #456`
- Keep description under 72 characters

## Git Safety Protocol

- NEVER update git config
- NEVER run destructive commands (--force, hard reset) without explicit request
- NEVER skip hooks (--no-verify) unless user asks
- NEVER force push to main/master
- If commit fails due to hooks, fix and create NEW commit (don't amend)
