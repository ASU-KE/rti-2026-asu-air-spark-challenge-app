import { NavLink, Outlet } from "react-router-dom";
import { NAV_SCREENS } from "../navigation";
import "./AppShell.css";

/**
 * The application shell: an ASU Unity themed brand header (banner landmark), an
 * app-level primary navigation, and the routed screen content (main landmark).
 *
 * The header is styled to the ASU Unity Design System brand (maroon/gold, ASU
 * wordmark) with local markup rather than the `@asu/component-header-footer`
 * package. That package's published bundle (v1.5.0) inlines its own copy of
 * React and crashes with React error #527 when rendered inside a React 19 app;
 * see `AsuHeaderMount.tsx` for the swap-in seam to adopt it once upstream
 * externalizes React.
 *
 * The primary navigation is rendered as first-class React Router `NavLink`s:
 * a labelled `navigation` landmark of real `link`s, keyboard-navigable, with
 * `aria-current` on the active screen, wired directly to client-side routing.
 */
export function AppShell() {
  return (
    <>
      <a className="skip-link" href="#main-content">
        Skip to main content
      </a>

      <header className="app-banner">
        <a className="app-banner__brand" href="https://www.asu.edu">
          <span className="app-banner__wordmark">
            Arizona State University
          </span>
        </a>
        <p className="app-banner__title">AIRgents of Change</p>
      </header>

      <nav aria-label="Primary" className="primary-nav">
        <ul className="primary-nav__list">
          {NAV_SCREENS.map((screen) => (
            <li key={screen.path} className="primary-nav__item">
              <NavLink
                to={screen.path}
                end={screen.path === "/"}
                className={({ isActive }) =>
                  isActive
                    ? "primary-nav__link primary-nav__link--active"
                    : "primary-nav__link"
                }
              >
                {screen.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <main id="main-content" className="app-main">
        <Outlet />
      </main>
    </>
  );
}
