---
inclusion: auto
name: development-workflow
description: Development workflow guidelines for planning, TDD, code review, and commit pipeline
---

# Development Workflow

> This rule extends the git workflow rule with the full feature development process that happens before git operations.

The Feature Implementation Workflow describes the development pipeline: planning, TDD, code review, and then committing to git.

## Feature Implementation Workflow

1. **Plan First**
   - Use **planner** agent to create implementation plan
   - Identify dependencies and risks
   - Break down into phases

2. **TDD Approach**
   - Use the **tdd-guide** agent and the `tdd` skill for the red → green loop
   - Write the failing test first (RED), implement to pass it (GREEN), then refactor
   - Meet the coverage bar in the testing rule — qualitative, across confirmed seams

3. **Code Review**
   - Use **code-reviewer** agent immediately after writing code
   - Address CRITICAL and HIGH issues
   - Fix MEDIUM issues when possible

4. **Commit & Push**
   - Detailed commit messages
   - Follow conventional commits format
   - See the git workflow rule for commit message format and PR process
