/**
 * The four top-level screens of the app. This single list is the source of
 * truth for both the primary navigation (AppShell) and the route table
 * (routes.tsx): the route table is keyed by these exact `path` literals, so a
 * screen added here without a matching route element fails the type check.
 *
 * Declared `as const` (not annotated `NavScreen[]`) so `path` stays a literal
 * union rather than widening to `string` — that literal union is what enforces
 * the route/nav correspondence.
 */
export interface NavScreen {
  readonly path: string;
  readonly label: string;
}

export const NAV_SCREENS = [
  { path: "/", label: "Experiment Builder" },
  { path: "/network", label: "Network Overview" },
  { path: "/runs", label: "Run Monitor" },
  { path: "/datasets", label: "Dataset Manager" },
] as const satisfies readonly NavScreen[];
