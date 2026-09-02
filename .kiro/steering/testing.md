---
inclusion: auto
name: testing
description: Test coverage bar and test stack. Use when writing tests, choosing test types, or judging whether coverage is enough.
---

# Testing Requirements

The red → green loop, what a good test is, and where seams go live in the `tdd` skill. This steering owns the two things that skill defers here: the coverage bar and the test stack. It does not restate the loop.

## Coverage bar

Coverage is judged qualitatively at confirmed **seams** — the public boundaries you test at — not as a global line or branch percentage. Confirm the seams with the user before writing tests, then hold this floor across every confirmed seam:

- The happy path is exercised.
- Error paths and failure modes are exercised.
- Boundary conditions are exercised — empty inputs, invalid values, and limits.

The floor is a bar across the confirmed seams, not a mandate to test every internal or hit a number. Choose which seams and test types matter by the risk of the feature, so effort lands on critical paths and complex logic.

## Test stack

This project targets a Python/FastAPI backend and a React/TypeScript frontend deployed to Google Cloud GKE. Select test types by feature risk across three seam levels:

- **Unit** — functions, utilities, and components in isolation. Backend: `pytest`. Frontend: React Testing Library on the project's configured runner.
- **Integration / contract** — FastAPI endpoints, database access, and the contracts between backend and frontend. Backend: `pytest` against the app and a test database.
- **End-to-end** — critical user journeys through the UI, with Playwright.

Resolve the exact test command per the `tdd` skill (read `package.json` scripts and project config); do not assume `npm test`.

## Troubleshooting failures

1. Check test isolation — each test builds its own state and passes in any order.
2. Verify mocks match the real boundary they stand in for.
3. Fix the implementation; change a test only when it encodes the wrong behavior.
