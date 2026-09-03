/**
 * Ambient types for `@asu/component-header-footer`.
 *
 * The published package (v1.5.0) ships an empty `main.d.ts`, so we declare the
 * surface this app uses. Prop shapes mirror the package's
 * `docs/README.props.md` (HeaderProps, NavTreeProps, Logo, Button typedefs).
 * Widen this declaration as more of the API is adopted.
 *
 * IMPORTANT — exact React pin: the package declares `react` and `react-dom` as
 * peer dependencies but its dist *inlines* react-dom (19.2.6). React 19 requires
 * `react` and `react-dom` to report the exact same version, so the app must pin
 * both to the inlined version or the header throws React error #527 at import.
 * Do not widen the react/react-dom ranges in package.json. See README.
 */
declare module "@asu/component-header-footer" {
  import type { ComponentType } from "react";

  export interface AsuLogo {
    alt: string;
    title: string;
    src: string;
    mobileSrc: string;
    brandLink?: string;
  }

  export interface AsuNavButton {
    href?: string;
    color?: "gold" | "maroon" | "light" | "dark";
    text: string;
    classes?: string;
    onClick?: () => void;
    as?: "a" | "button" | "div";
  }

  export interface AsuNavItem {
    id: number;
    href?: string;
    text?: string;
    type?: string;
    selected?: boolean;
    items?: AsuNavItem[][];
    buttons?: AsuNavButton[];
    class?: string;
    onClick?: (event?: React.MouseEvent) => void;
  }

  export interface AsuHeaderProps {
    title?: string;
    navTree?: AsuNavItem[];
    logo?: AsuLogo;
    baseUrl?: string;
    parentOrg?: string;
    parentOrgUrl?: string;
    buttons?: AsuNavButton[];
    breakpoint?: "Lg" | "Xl";
    animateTitle?: boolean;
    expandOnHover?: boolean;
    mobileNavTree?: AsuNavItem[];
    searchUrl?: string;
    site?: string;
    loggedIn?: boolean;
    userName?: string;
    isPartner?: boolean;
  }

  export interface AsuFooterProps {
    logo?: AsuLogo;
    unit?: Record<string, unknown>;
    contacts?: Record<string, unknown>;
  }

  export const ASUHeader: ComponentType<AsuHeaderProps>;
  export const ASUFooter: ComponentType<AsuFooterProps>;
}
