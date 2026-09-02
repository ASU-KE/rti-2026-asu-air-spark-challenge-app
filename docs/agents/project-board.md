# Development Project board

The **AIRgents of Change — Development** GitHub Project tracks the implementation and
deployment work tickets derived from
`docs/planning/spec-airgents-of-change-prototype.md`. It is optimized for coordinating
multiple developers and their agents working tickets in parallel without colliding.

- **Project:** https://github.com/orgs/ASU-KE/projects/13 (org-owned, `ASU-KE`, private)
- **Populated by:** `/to-tickets` (one issue per vertical slice, in dependency order).
- **Not tracked here:** planning/brainstorm/administrative issues. Those live in the
  separate **Planning** project (#9) and must be left untouched.

## How coordination works

Two levers keep parallel work from colliding:

1. **Area** — every ticket names the module it touches, so two agents don't edit the same
   seam at once. The **By Area** view surfaces collisions.
2. **Dependency-aware readiness** — `/to-tickets` sets GitHub's native blocking links.
   A ticket is only **Status: Ready** (and labeled `ready-for-agent`) once its blockers
   are done; blocked work sits in **Status: Blocked** so nobody grabs it. Agents pull
   from the **Agent Queue** view, which shows only ready, unassigned, agent-grabbable
   tickets.

Readiness/routing stays on the existing triage labels (`ready-for-agent`,
`ready-for-human`, `needs-triage`, `needs-info`, `wontfix` — see `triage-labels.md`). The
Project fields below are for workflow state and sequencing.

## Fields

| Field | Type | Values |
| --- | --- | --- |
| Status | single-select | Backlog · Ready · Blocked · In Progress · In Review · Done |
| Area | single-select | Domain/Engine · ProviderClient · RunExecutor · Repository · API · Frontend · Auth · Testing · Docs · Infra |
| Priority | single-select | P0 · P1 · P2 |
| Size | single-select | XS · S · M · L |
| Iteration | iteration | *(optional; add via UI if time-boxing — see below)* |

Plus built-ins: Assignees (the developer), Labels, Linked pull requests, Parent issue,
Sub-issues progress.

### Status semantics

- **Backlog** — not yet ready to start.
- **Ready** — unblocked and `ready-for-agent` to grab.
- **Blocked** — waiting on a blocking ticket.
- **In Progress** — actively being worked by a dev/agent.
- **In Review** — PR open, awaiting review.
- **Done** — merged and verified.

## Labels

Durable classification that travels with the issue (usable in `gh issue list` queries):

- **Area:** `area:engine`, `area:provider`, `area:api`, `area:frontend`, `area:auth`,
  `area:testing`, `area:infra`, `area:docs`
- **Type:** `type:feature`, `type:refactor`, `type:prefactor`, `type:chore`

## Views (create in the web UI)

Custom Project views can't be created via the `gh` CLI or GraphQL API (Projects v2 views
are read-only in the API), so build these once in the UI. Filter strings paste directly
into the view filter bar.

1. **Board** — Layout: Board, Column field: **Status**. Primary working wall.
2. **Agent Queue** — Layout: Table. Filter: `status:Ready label:"ready-for-agent" no:assignee`.
   Sort: Priority ↑, then Size ↑. Fields: Title, Area, Priority, Size, Linked pull requests.
   The "grab the next unblocked ticket" queue for AFK agents.
3. **By Developer** — Layout: Board, Column field: **Assignees**.
4. **By Area** — Layout: Table, Group by: **Area**.
5. **Blocked** — Layout: Table, Filter: `status:Blocked`, show Parent issue.

### Optional UI toggles

- **Iteration field** — Settings → + New field → Iteration (the one field type the CLI
  can't create). Add only if time-boxing.
- **Built-in workflows** (⋯ → Workflows) — enable *Item added → Status: Backlog*,
  *Item reopened → In Progress*, *Item closed → Done*. Leave **Auto-add to project** off
  (or filter it tightly) so it never sweeps in the planning issues.

## `/to-tickets` handoff routine

`/to-tickets` creates one issue per slice in dependency order with native blocking links
and the `ready-for-agent` label. For each new issue, also:

1. Add it to the board:
   ```sh
   gh project item-add 13 --owner ASU-KE --url <issue-url>
   ```
2. Set Area / Priority / Size and Status (Ready if unblocked, else Blocked). Use the IDs
   in the reference below with `gh project item-edit`.
3. Apply the matching `area:*` and `type:*` labels on the issue.

Do **not** close or modify parent/planning issues (#1–#25 and project #9).

## Field & option IDs (for scripting)

Project ID: `PVT_kwDOBMsMkc4BiSOi` — Project number: `13` — Owner: `ASU-KE`

Re-fetch with `gh project field-list 13 --owner ASU-KE --format json` if fields change.

| Field | Field ID | Option | Option ID |
| --- | --- | --- | --- |
| Status | `PVTSSF_lADOBMsMkc4BiSOizhhK1r8` | Backlog | `f6a63f15` |
| | | Ready | `f806ce33` |
| | | Blocked | `28f35456` |
| | | In Progress | `d0750c0d` |
| | | In Review | `d0186499` |
| | | Done | `341f87bb` |
| Area | `PVTSSF_lADOBMsMkc4BiSOizhhK12I` | Domain/Engine | `6d548cb2` |
| | | ProviderClient | `292b82e5` |
| | | RunExecutor | `4b7bbd5b` |
| | | Repository | `69cedf53` |
| | | API | `88fa7902` |
| | | Frontend | `807a8b75` |
| | | Auth | `257aa1a9` |
| | | Testing | `9de8aa94` |
| | | Docs | `eb96afcc` |
| | | Infra | `c40ff0e7` |
| Priority | `PVTSSF_lADOBMsMkc4BiSOizhhK12M` | P0 | `d62030bb` |
| | | P1 | `083f631e` |
| | | P2 | `a4d80a9d` |
| Size | `PVTSSF_lADOBMsMkc4BiSOizhhK12Q` | XS | `dadee7a3` |
| | | S | `bf905204` |
| | | M | `cac996ad` |
| | | L | `33fa5346` |

### Example: set fields on a board item

`item-edit` needs the item's project-item ID (from `gh project item-list 13 --owner ASU-KE
--format json`), not the issue number:

```sh
gh project item-edit --id <ITEM_ID> --project-id PVT_kwDOBMsMkc4BiSOi \
  --field-id PVTSSF_lADOBMsMkc4BiSOizhhK1r8 --single-select-option-id f806ce33   # Status: Ready
```
