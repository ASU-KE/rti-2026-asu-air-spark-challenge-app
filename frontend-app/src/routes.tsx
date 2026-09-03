import { Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { ExperimentBuilderPage } from "./pages/ExperimentBuilderPage";
import { NetworkOverviewPage } from "./pages/NetworkOverviewPage";
import { RunMonitorPage } from "./pages/RunMonitorPage";
import { DatasetManagerPage } from "./pages/DatasetManagerPage";

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
        <Route index element={<ExperimentBuilderPage />} />
        <Route path="network" element={<NetworkOverviewPage />} />
        <Route path="runs" element={<RunMonitorPage />} />
        <Route path="datasets" element={<DatasetManagerPage />} />
      </Route>
    </Routes>
  );
}
