import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { ASUHeader } from "@asu/component-header-footer";
import type { AsuNavItem } from "@asu/component-header-footer";
import { NAV_SCREENS } from "../navigation";
import "./AppShell.css";

/**
 * The application shell: the ASU Unity Design System global header (which
 * supplies the `banner` landmark, the ASU global and site navigation, and its
 * own skip link) above the routed screen content (`main` landmark).
 *
 * The four screens are fed to the header as its `navTree`. Each item keeps its
 * real `href` so links remain shareable and open normally in a new tab, while
 * `onClick` intercepts plain activations and routes client-side instead of
 * triggering a full page load.
 */
export function AppShell() {
  const navigate = useNavigate();
  const { pathname } = useLocation();

  const navTree: AsuNavItem[] = NAV_SCREENS.map((screen, index) => ({
    id: index + 1,
    href: screen.path,
    text: screen.label,
    selected: screen.path === pathname,
    onClick: (event) => {
      // Let the browser handle modified clicks (new tab/window) natively.
      if (
        event &&
        (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey)
      ) {
        return;
      }
      event?.preventDefault();
      void navigate(screen.path);
    },
  }));

  return (
    <>
      <ASUHeader
        title="AIRgents of Change"
        parentOrg="Arizona State University"
        parentOrgUrl="https://www.asu.edu"
        loggedIn={false}
        navTree={navTree}
        breakpoint="Lg"
      />

      {/*
        The ASU header's skip link targets `#skip-to-content`, so the main
        region must carry that id for "Skip to main content" to land here.
      */}
      <main id="skip-to-content" className="app-main">
        <Outlet />
      </main>
    </>
  );
}
