---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

1. Claim the ticket and cut the branch: assign it to yourself (`gh issue edit <n> --add-assignee @me`; skip if working from local ticket files), then cut `feature/<issue>-<slug>` from `main`.

TDD is mandatory. Build every change test-first with the `/tdd` skill: agree the seams with the user, then drive each one through the red → green loop. No production code is written before a real, failing red at the seam it implements. "No test framework yet" is not an exemption — set one up first.

2. Follow the commit story: make atomic commits that track the red → green loop — `test:` once red is confirmed, `feat:`/`fix:` once green, optional `refactor:` after green (it counts against the cap). Make one logical change per commit; never fold a refactor into a feature commit.

3. When the slice is green and complete, check the diff against `main` — it must be ≤300 lines (code + tests). If it is bigger, do NOT open the PR: stop, report, and split the ticket back through `/to-tickets`. Because every commit is atomic and stands green on its own, any green prefix is a valid split point: the first PR takes the commits up to the last point at or under the cap, and the remainder becomes the next ticket.

4. Run typechecking regularly, single test files regularly, and the full test suite once at the end.

5. Ship each slice through the delivery pipeline in the `git-workflow` skill: `/code-review` always; `/security-review` when the slice touches auth, secrets, input boundaries, or data access (skip only when none apply, and say so); CI green before requesting human review; one small, readable PR per slice targeting `main` that links and closes the ticket; never a monolithic PR.
