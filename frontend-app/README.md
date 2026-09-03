# AIRgents of Change — frontend

React 19 + TypeScript + Vite dashboard for configuring Experiments, running
them, observing Runs, and exporting Datasets. See `../CONTEXT.md` for the domain
glossary and `../docs/planning/spec-airgents-of-change-prototype.md` for the spec.

## Prerequisites

- [Bun](https://bun.sh) (package manager and script runner)
- A GitHub token with `read:packages` for the **ASU organization**, exported as
  `GITHUB_TOKEN`. The ASU Unity Design System packages are published to GitHub
  Packages, not npmjs, and `.npmrc` reads the token from that variable:

  ```sh
  export GITHUB_TOKEN=ghp_your_token_here
  bun install
  ```

  Without it, `bun install` fails with `403 permission_denied: read_package`.

## Commands

```sh
bun run dev        # start the dev server (proxies /api to the backend on :8000)
bun run typecheck  # tsc project references, no emit
bun run lint       # eslint
bun run test       # vitest (jsdom + React Testing Library + MSW)
bun run build      # typecheck then production build
```

## Two constraints worth knowing

### React is pinned to an exact version on purpose

`package.json` pins `react` and `react-dom` to **exactly** `19.2.6` — no caret.

`@asu/component-header-footer` declares React as a peer dependency but its
published bundle *inlines* react-dom 19.2.6. React 19 requires `react` and
`react-dom` to report the identical version, so any other version throws
[React error #527](https://react.dev/errors/527) ("Incompatible React versions")
the moment the header is imported.

**Do not widen these ranges**, and do not let automated dependency updates bump
them, until upstream publishes a build that externalizes React. If the ASU
package changes the version it inlines, this pin has to move in lockstep.

### The header dominates the bundle

The same inlining means the header ships its own React and FontAwesome, which is
most of the ~290 kB gzipped production bundle. Code-splitting the shell is a
known follow-up.

## Layout

```
src/
  api/          typed client over the standard response envelope
  components/   AppShell (ASU Unity header + main landmark)
  pages/        one placeholder per screen
  test/         vitest setup and MSW handlers
  navigation.ts single source of truth for screens; routes are derived from it
  routes.tsx    route tree
```

`navigation.ts` and `routes.tsx` are tied together by type: adding a screen to
`NAV_SCREENS` without a matching route element is a compile error.
