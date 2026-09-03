---
name: react-patterns
description: React 18/19 component and hook authoring — hooks discipline, server/client boundaries, Suspense and error boundaries, form actions, state and data-fetching decisions, accessible composition, and migrating legacy class or effect-heavy components. Use when writing or reviewing React components.
metadata:
  origin: ECC
---

# React Patterns

## Core Principles

### 1. Render is a Pure Function of Props and State

Derive during render; never store derived state in `useEffect` — it adds a render cycle, can desync, and obscures the data flow.

```tsx
// Good: derive during render
function Cart({ items }: { items: CartItem[] }) {
  const total = items.reduce((sum, i) => sum + i.price * i.qty, 0);
  return <span>{formatMoney(total)}</span>;
}

// Bad: derived state stored separately
function Cart({ items }: { items: CartItem[] }) {
  const [total, setTotal] = useState(0);
  useEffect(() => {
    setTotal(items.reduce((sum, i) => sum + i.price * i.qty, 0));
  }, [items]);
  return <span>{formatMoney(total)}</span>;
}
```

### 2. Side Effects Outside Render

Effects, mutations, network calls, and subscriptions live in event handlers or `useEffect` — never in the render body.

### 3. Composition Over Inheritance

React has no inheritance model for components. Compose with `children`, render props, or component props.

## Hooks Discipline

Core hooks rules:

- Top-level only, never conditional
- Cleanup every subscription, interval, listener
- Functional updater (`setX(prev => prev + 1)`) when new state depends on old
- Default position: do not memoize — add `useMemo`/`useCallback` only when a profiler or a dependency chain proves it matters
- Extract a custom hook only when the same hook sequence appears in 2+ components

## State Location Decision Tree

```
Used by one component?
  -> useState inside it

Used by parent + a few descendants?
  -> lift to nearest common ancestor

Used across distant branches AND low-frequency reads (theme, auth, locale)?
  -> React Context

High-frequency updates shared across the tree?
  -> external store (Zustand, Jotai, Redux Toolkit)

Derived from a server?
  -> server-state library (TanStack Query, SWR)
```

Most pages do not need context or a global store. Resist abstraction until duplicated lifting becomes painful.

## Suspense + Error Boundaries

```tsx
<ErrorBoundary fallback={<ErrorView />}>
  <Suspense fallback={<UserSkeleton />}>
    <UserDetail id={id} />
  </Suspense>
</ErrorBoundary>
```

- Place Suspense boundaries close to the data, not at the route root — progressively reveal content
- Error Boundary remains a class API; use `react-error-boundary` for a hook-friendly wrapper
- A boundary catches errors thrown during render, lifecycle, and constructors of its children — NOT in event handlers or async code

## Forms

### React 19 form actions (preferred for new code)

```tsx
import { useActionState } from "react";

const initial = { error: null as string | null };

async function updateUserAction(_prev: typeof initial, formData: FormData) {
  const parsed = UserSchema.safeParse(Object.fromEntries(formData));
  if (!parsed.success) return { error: "Invalid input" };
  const res = await api.updateUser(parsed.data);
  return { error: res.ok ? null : "Update failed" };
}

export function UserForm() {
  const [state, formAction, pending] = useActionState(updateUserAction, initial);
  return (
    <form action={formAction}>
      <input name="name" required />
      <button type="submit" disabled={pending}>Save</button>
      {state.error && <p role="alert">{state.error}</p>}
    </form>
  );
}
```

### Controlled inputs

Use controlled when the value drives other UI, formats on every keystroke, or implements real-time validation.

### Complex forms

For multi-step forms, dynamic field arrays, or cross-field validation, use a library (React Hook Form, TanStack Form). Hand-rolled form state past trivial complexity is a maintenance trap.

## Data Fetching Decision Matrix

| Need | Tool |
|---|---|
| Client-side cache + mutations + invalidation | TanStack Query |
| Lightweight client cache + revalidation | SWR |
| Real-time subscriptions | Server-Sent Events, WebSockets, or the lib's subscription API |
| One-off fire-and-forget | `fetch()` in an event handler |

Reach for a tool above for application data; `useEffect` + `fetch` brings race conditions, no cache, no retry, and no Suspense integration.

## Composition Recipes

### Slot via `children`

```tsx
<Layout>
  <Header />
  <Main>{content}</Main>
</Layout>
```

### Named slots

```tsx
<Page header={<Nav />} sidebar={<Filters />}>
  <Results />
</Page>
```

### Compound components (shared state via Context)

```tsx
<Tabs defaultValue="profile">
  <Tabs.List>
    <Tabs.Trigger value="profile">Profile</Tabs.Trigger>
    <Tabs.Trigger value="settings">Settings</Tabs.Trigger>
  </Tabs.List>
  <Tabs.Panel value="profile"><Profile /></Tabs.Panel>
  <Tabs.Panel value="settings"><Settings /></Tabs.Panel>
</Tabs>
```

### Render prop / function-as-child

Useful when the parent needs to pass parameters to the rendered output:

```tsx
<DataLoader id={id}>
  {({ data, isLoading }) => isLoading ? <Spinner /> : <UserCard user={data} />}
</DataLoader>
```

Modern alternative: a hook (`useData(id)`) returning the same shape — usually cleaner.

## Performance

### When `React.memo` Actually Helps

Wrap a component in `React.memo` only when all three hold — if any fails, skip it, since `React.memo` adds an equality check on every render that is pure overhead when props differ on most renders:

1. It re-renders frequently
2. Its props are usually the same between renders
3. Its render is measurably expensive

### Avoiding Render Cascades

- Lift state down rather than up where possible
- Split context: one context per concern, so a change to `themeContext` does not re-render auth consumers
- Use `useSyncExternalStore` for external state libraries — required for safe concurrent rendering

### Lists

- Provide stable `key` props (database id, not array index)
- Virtualize long lists with `@tanstack/react-virtual` or `react-window` once visible item count exceeds ~50 with non-trivial rows

## Accessibility-First Composition

- Render semantic HTML (`<button>`, `<a>`, `<nav>`, `<main>`) before reaching for `role` attributes
- Every interactive element must be reachable by keyboard
- Form inputs need labels — `<label htmlFor>`, or `aria-label` when labeled only by an icon
- Manage focus on route changes and modal open/close
- Run `axe` in component tests (see [skills/react-testing](../react-testing/SKILL.md))
- [skills/accessibility/SKILL.md](../accessibility/SKILL.md) covers WCAG criteria and pattern libraries

## Scope

Router-agnostic: the patterns here work with React Router and TanStack Router. Router-specific concerns layer on top of React core and follow the router's own docs.

- **React Native** — platform patterns differ enough to warrant a separate `react-native-patterns` skill (not present yet)

## Related

- Worked examples: [EXAMPLES.md](EXAMPLES.md) — debounced-search hook, `useOptimistic`, context splitting
- Skills: [react-performance](../react-performance/SKILL.md) for the performance ruleset, [frontend-patterns](../frontend-patterns/SKILL.md) for the UI cookbook (forms, animation, state wiring), [accessibility](../accessibility/SKILL.md)
- Agents: `react-reviewer` for code review, `react-build-resolver` for build/bundler errors
- Commands: `/react-review`, `/react-build`, `/react-test`
