---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

TDD is mandatory. Build every change test-first with the `/tdd` skill: agree the seams with the user, then drive each one through the red → green loop. No production code is written before a real, failing red at the seam it implements. "No test framework yet" is not an exemption — set one up first.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Ship each slice through the delivery pipeline in the `git-workflow` skill: atomic commits across the red → green loop, then `/code-review` and — when the slice touches auth, secrets, input, or data — `/security-review`, and finally one small, readable PR per slice targeting `main`. Never a monolithic PR.
