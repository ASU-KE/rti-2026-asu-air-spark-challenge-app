/**
 * Ambient types for `@asu/component-header-footer`.
 *
 * The published package (v1.5.0) ships an empty `main.d.ts`, so we declare the
 * subset the app relies on. Only the UMD entry's imperative initializer is
 * used, and only by the (currently dormant) `AsuHeaderMount` swap-in seam —
 * see that file for why the package is not rendered directly. Widen this
 * declaration as more of the API is adopted.
 */
declare module "@asu/component-header-footer/dist/asuHeaderFooter.umd.js" {
  export function initGlobalHeader(config: {
    targetSelector: string;
    props: Record<string, unknown>;
  }): void;

  export function initASUFooter(config: {
    targetSelector: string;
    props: Record<string, unknown>;
  }): void;
}
