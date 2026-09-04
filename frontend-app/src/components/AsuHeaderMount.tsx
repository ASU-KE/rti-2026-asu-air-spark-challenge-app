import { useEffect, useRef } from "react";

interface AsuHeaderMountProps {
  title: string;
  parentOrg: string;
  parentOrgUrl: string;
}

/**
 * SWAP-IN SEAM (not currently used by {@link AppShell}).
 *
 * Mounts the real ASU Unity global header from `@asu/component-header-footer`
 * via its UMD initializer. It is intentionally *not* wired into the shell yet:
 * the published package (v1.5.0) bundles its own copy of React and throws
 * React error #527 when loaded inside this React 19 app — from both its ESM
 * and UMD entry points. The import is therefore deferred to a dynamic import
 * inside the effect so merely keeping this file never loads the broken bundle.
 *
 * Once upstream publishes a build that externalizes React, swap the themed
 * header in `AppShell` for this component and the app gets the real UDS header.
 * Tracking: the packaging bug is a follow-up filed against the ASU Unity stack.
 */
export function AsuHeaderMount({
  title,
  parentOrg,
  parentOrgUrl,
}: AsuHeaderMountProps) {
  const containerId = useRef<string>("");
  if (!containerId.current) {
    containerId.current = `asu-header-${Math.random().toString(36).slice(2)}`;
  }

  useEffect(() => {
    let cancelled = false;
    const container = document.getElementById(containerId.current);

    void import("@asu/component-header-footer/dist/asuHeaderFooter.umd.js")
      .then((mod) => {
        if (cancelled) return;
        // Clear any prior instance before re-initializing into the same node.
        if (container) container.innerHTML = "";
        mod.initGlobalHeader({
          targetSelector: `#${containerId.current}`,
          props: {
            title,
            parentOrg,
            parentOrgUrl,
            loggedIn: false,
            navTree: [],
            breakpoint: "Lg",
          },
        });
      })
      .catch((error: unknown) => {
        // Surface activation failures loudly rather than silently swallowing
        // them — this is the seam that guards the known React #527 crash.
        console.error("Failed to mount ASU Unity header", error);
      });

    return () => {
      cancelled = true;
    };
  }, [title, parentOrg, parentOrgUrl]);

  return <div id={containerId.current} />;
}
