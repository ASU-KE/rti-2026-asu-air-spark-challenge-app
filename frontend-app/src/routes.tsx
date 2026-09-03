import type { ReactElement } from "react";
import { Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { NAV_SCREENS } from "./navigation";
import { ExperimentBuilderPage } from "./pages/ExperimentBuilderPage";
import { NetworkOverviewPage } from "./pages/NetworkOverviewPage";
import { RunMonitorPage } from "./pages/RunMonitorPage";
import { DatasetManagerPage } from "./pages/DatasetManagerPage";

/**
 * Maps each screen's route path to its page element. Keyed by the same paths
 * as {@link NAV_SCREENS}, so the navigation and the route table are generated
 * from one source and cannot drift: a screen added to `NAV_SCREENS` without a
 * matching entry here fails the type check below.
 */
const SCREEN_ELEMENTS: Record<(typeof NAV_SCREENS)[number]["path"], ReactElement> =
  {
    "/": <ExperimentBuilderPage />,
    "/network": <NetworkOverviewPage />,
    "/runs": <RunMonitorPage />,
    "/datasets": <DatasetManagerPage />,
  };

/**
 * The app's route tree. `AppShell` is the layout route; each screen renders
 * into its `<Outlet />`. Using the component `<Routes>` API (rather than a
 * data router) keeps client-side navigation on React Router's in-memory path,
 * which is what both the browser (main.tsx) and the tests drive.
 */
export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<AppShell />}>
        {NAV_SCREENS.map((screen) =>
          screen.path === "/" ? (
            <Route key={screen.path} index element={SCREEN_ELEMENTS[screen.path]} />
          ) : (
            <Route
              key={screen.path}
              path={screen.path.replace(/^\//, "")}
              element={SCREEN_ELEMENTS[screen.path]}
            />
          ),
        )}
      </Route>
    </Routes>
  );
}
