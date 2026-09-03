/**
 * The four top-level screens of the app. This single list is the source of
 * truth for both the primary navigation (AppShell) and the route table
 * (routes.tsx), so the two can never drift apart.
 */
export interface NavScreen {
  readonly path: string;
  readonly label: string;
}

export const NAV_SCREENS: readonly NavScreen[] = [
  { path: "/", label: "Experiment Builder" },
  { path: "/network", label: "Network Overview" },
  { path: "/runs", label: "Run Monitor" },
  { path: "/datasets", label: "Dataset Manager" },
] as const;
