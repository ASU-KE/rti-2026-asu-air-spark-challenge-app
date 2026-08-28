---
name: write-asu-themed-document
description: 'Author or re-theme a self-contained, single-file HTML planning/proposal document (and its site index) to ASU official web design standards (the ASU Unity Design System). Produces static HTML with inline CSS/JS, no build step, suitable for publishing to GitHub Pages.'
license: MIT
metadata:
  author: KE Research Technology Office
  version: '1.0.0'
  compatibility: 'Harness-agnostic. Plain markdown instructions with no tool-specific syntax — usable by any coding agent that can read/write files, run shell commands, and (ideally) preview HTML in a browser.'
---

# ASU-Themed Document Writer

You produce internal planning documents, project proposals, and status pages as **self-contained, single-file HTML** — inline `<style>`, inline `<script>`, no build step, no external CSS/JS/font dependencies — themed to ASU's official web design standards (the **ASU Unity Design System**, "UDS"). These documents are typically published as static sites (e.g., GitHub Pages) and are frequently interactive (filterable boards, tabs, expandable detail popovers) rather than flat prose.

## When to use this skill

- Writing a new internal proposal, planning board, dashboard mock, or status page that needs to look like an official ASU web property.
- Re-theming an existing plain/unbranded HTML document to match ASU brand.
- Adding a new page to an existing ASU-branded documentation site so it matches the site's landing page.

## Source of truth — check live before trusting memory

Design tokens change slowly but you should still verify against the canonical source rather than relying purely on the tables below, which are a point-in-time extraction.

1. **Preferred:** the public component library repo — `https://github.com/ASU/asu-unity-stack`. Clone or fetch it (shallow clone is enough) and read:
   - `packages/unity-bootstrap-theme/src/scss/_custom-asu-variables.scss` — the base color/font/spacing tokens
   - `packages/unity-bootstrap-theme/src/scss/variables/_colors.scss` and `_typography.scss` — how tokens compose into semantic roles (links, body text, etc.)
   - `packages/unity-bootstrap-theme/src/scss/extends/_global-header.scss` and `_globalfooter.scss` — canonical header/footer component CSS
   - `packages/component-header-footer/examples/global-header-footer.html` — canonical header/footer markup
2. **Fallback:** the public brand guide at `https://brandguide.asu.edu`. This is a _design reference for humans_, not shippable CSS — cross-check anything derived from it against the component repo above before treating it as final if the repo is reachable.
3. **Last resort:** the token tables in this document, extracted directly from `_custom-asu-variables.scss`. If neither source above is reachable, use these, but flag to the user that live verification wasn't possible.

Do not invent brand colors, gradients, or component shapes that aren't attested in one of the above. If a first pass turns out to diverge from the canonical component CSS (e.g. a masthead style that "feels right" but doesn't match `_global-header.scss`), that is a defect to correct, not a stylistic choice to defend.

## Design tokens

### Color

| Token             | Hex                    | Use                                                                                                                                                 |
| ----------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `maroon`          | `#8c1d40`              | Primary brand color — links, accents, active states                                                                                                 |
| `darkmaroon`      | `#440e22`              | Visited-link state for maroon links                                                                                                                 |
| `gold`            | `#ffc627`              | Secondary brand color — underlines, fills on dark backgrounds, small accents                                                                        |
| `darkgold`        | `#7f6227`              | Gold-family **text** on light backgrounds. Raw gold fails contrast as text on white/light gray — never use `#ffc627` for text on a light background |
| `asu-gray-1`      | `#191919`              | Base font color / near-black                                                                                                                        |
| `asu-gray-2`      | `#484848`              | Secondary text                                                                                                                                      |
| `asu-gray-3`      | `#747474`              | Muted text                                                                                                                                          |
| `asu-gray-4`      | `#bfbfbf`              | Disabled / low-emphasis                                                                                                                             |
| `asu-gray-5`      | `#d0d0d0`              | Borders, dividers (also the canonical header bottom-border color)                                                                                   |
| `asu-gray-6`      | `#e8e8e8`              | Light surfaces, utility-strip background                                                                                                            |
| `asu-gray-7`      | `#fafafa`              | Page background                                                                                                                                     |
| `alerts-error`    | `#cc2f2f`              | Error state                                                                                                                                         |
| `alerts-warning`  | `#ff7f32` (ASU Orange) | Warning state                                                                                                                                       |
| `alerts-success`  | `#78be20` (ASU Green)  | Success state                                                                                                                                       |
| `alerts-info`     | `#00a3e0` (ASU Blue)   | Informational state                                                                                                                                 |
| `divider-darker`  | `#1e1e1e`              | Footer background                                                                                                                                   |
| `divider-lighter` | `#393939`              | Footer divider/border                                                                                                                               |
| `bluefocus`       | `#00baff`              | Accessibility focus ring — `box-shadow: 0 0 8px #00baff` on `:focus`                                                                                |

Note: the `_colors.scss` grayscale numbering (`gray-1`..`gray-7`) is **inverted from the brand-guideline numbering** for backwards-compatibility reasons in the source repo (their `1` = brand guideline `7`, lightest). Always key off the hex value or the `asu-gray-N` brand-guideline name in the table above, not a bare "gray-N" reference pulled from unfamiliar code, to avoid silently swapping light and dark.

Secondary/categorical palette (ASU Blue `#00a3e0`, Orange `#ff7f32`, Turquoise, Pink, Green, Crimson) is available for chart/tag categorization — darken any of these ~10-15% if you need them as small text/badge backgrounds with white text, to hold contrast.

### Typography

```css
font-family:
  Arial, Helvetica, 'Nimbus Sans L', 'Liberation Sans', FreeSans, sans-serif;
```

This is the literal canonical stack (`$uds-font-family-base`). Do not add `system-ui`, `-apple-system`, `"Segoe UI"`, or a display font on top of it — the canonical stack is deliberately a plain, widely-available sans-serif chain.

Font weights: normal `400`, bold `700` (note: `<b>`/`<strong>` must be forced to `700` — Bootstrap's reset otherwise pushes them to `900`).

## Canonical component patterns

These are the three structural bands of an ASU UDS page. Get these right first — they're the most visible signal of "is this actually ASU-branded" and the easiest place to invent something plausible-but-wrong.

### 1. Masthead / utility strip (`#wrapper-header-top`)

A thin bar **above** the main nav. Light gray, not colored:

```css
.masthead {
  background: #e8e8e8;
} /* asu-gray-6 */
.masthead .wordmark {
  color: #8c1d40;
} /* maroon */
.masthead .wordmark .accent {
  color: #7f6227;
} /* darkgold, NOT raw gold */
.masthead .site-label {
  color: #484848;
}
```

### 2. Main nav (`#wrapper-header-main`)

.topnav {
  background: #ffffff;
  border-bottom: 1px solid #d0d0d0; /* asu-gray-5 */
}
.navlinks button {
  color: #484848;
  border-bottom: 3px solid transparent; /* reserve space for the indicator */
}
.navlinks button:hover {
  color: #8c1d40;
  border-bottom-color: #d0d0d0;
}
.navlinks button.active {
  color: #8c1d40;
  border-bottom-color: #ffc627;
} /* gold underline */
```

### 3. Footer (`#wrapper-footer-columns`)

Dark, with a subtler dark divider — **no gold border anywhere on the footer**:

```css
footer {
  background: #1e1e1e;
  border-top: 1px solid #393939;
  color: #e8e8e8;
}
footer a {
  color: #e8e8e8;
  text-decoration: none;
}
footer a:hover {
  color: #ffc627;
  text-decoration: underline;
}
```

### Links (body content)

```css
a {
  color: #8c1d40;
} /* maroon */
a:visited {
  color: #440e22;
} /* darkmaroon */
```

## Page architecture

Match the pattern of a small ASU-KE documentation site:

- `index.html` — a landing page listing published documents (title, masthead, a `ul.doc-list` of cards linking to each document, footer).
- One HTML file per document (e.g. `proposals/<slug>.html`), each **fully self-contained**: its own `<style>` block defining a `:root` of CSS custom properties for every token above (don't repeat literal hex values through the stylesheet — define once, reference via `var(--token)`), its own inline `<script>` if the page is interactive.
- No shared CSS/JS file, no CDN, no build step. Every page must render correctly opened as a plain file or served as a static asset with zero other files present besides what it itself links to (images/assets under the same relative path).
- Domain-specific literal colors that come from an external system of record (e.g. Azure DevOps lifecycle-state colors, a status taxonomy defined elsewhere) should stay as **documented literals**, not get folded into the brand palette — leave a comment noting where they come from and do not remap them when you retheme the rest of the page.

## Workflow

1. **Gather the content.** Get the document's structure and content from the user or existing source (existing unbranded HTML, a spec, notes). Don't invent factual content.
2. **Confirm/refresh design tokens** using the Source of Truth section above.
3. **Scaffold the `:root` token block** as CSS custom properties, then build the masthead → main nav → hero/content sections → footer using the canonical patterns above.
4. **Build content sections** with the brand palette applied consistently — categorical colors for tags/badges, maroon/gold for structural accents, grayscale for text hierarchy.
5. **If the page has interactive elements** (filters, tabs, expandable detail popovers, drag targets, live-updating widgets) that could be mistaken for a static screenshot: add a short highlight note near the top of the page stating it's a live/clickable preview, and make sure every interactive control has visible affordance — a "click for details" style hint, a hover state, or an obvious tab/button shape. Don't rely on `cursor: pointer` alone; a first-time viewer skimming a screenshot won't see it. Keep hint wording _consistent_ across equivalent controls (e.g. every column header that opens a popover should use the same "click for…" phrasing).
6. **Verify visually.** Render the page in a browser (local file preview or a dev server) and check every section, not just the first screen: masthead, nav active/hover states, hero, each content section, interactive controls actually work, footer. Check the browser console for errors.
7. **Check contrast** on every text-on-color combination you introduced, especially gold-on-light (use `darkgold`, not raw `gold`) and any text placed on a newly-changed background.
8. **Check for stray literals.** If you introduced or changed a CSS custom property that's meant to replace an old palette, `grep` for the old literal color values (hex/rgba) elsewhere in the same file — hardcoded values don't pick up a `:root` change and are the most common way a retheme looks "half-done."
9. **If publishing to GitHub Pages behind org/SSO restriction:** a user report of "missing styling" on the live site is very often an authentication artifact, not a code defect — the screenshot may have been taken from an unauthenticated view that GitHub redirected to a sign-in page. Before debugging CSS, verify: the deployed build matches the latest commit, the committed file bytes match the local file byte-for-byte, and there are no console errors — then ask whether the viewer was signed in to the org on GitHub.
10. **Commit** using Conventional Commits if the user asks for a commit (`feat:` for new themed pages, `fix:` for correcting a divergence from canonical patterns).

## Common mistakes to avoid

These are real divergences that required a second pass to catch — check for them explicitly rather than assuming a first draft is correct:

- Rendering the masthead/nav as a **solid maroon bar with a gold border**. Canonical is white/light with a gold-underline indicator, not a filled color band.
- Using **raw gold (`#ffc627`) as text color** on any light/white background — always substitute `darkgold` (`#7f6227`).
- Giving the **footer a gold top border**. Canonical footer border is the dark divider gray (`#393939`), never gold.
- Nav "active" state rendered as a **filled pill** instead of a gold underline.
- Leaving **hardcoded `rgba()`/hex literals** from a prior palette in place after introducing CSS variables for the new one — they silently don't update.
- Adding **extra font-family fallbacks** (`system-ui`, `-apple-system`, `"Segoe UI"`) on top of the canonical stack.
- Interactive controls that look identical to plain static UI (no hint text, no visibly different hover/active state) — a viewer has no way to discover they can click.

## Verification checklist

- [ ] Design tokens confirmed against the live `asu-unity-stack` repo (or brand guide fallback), not just recalled from memory.
- [ ] Masthead is light/white with the gray-6 utility strip above a white main nav — not a solid maroon band.
- [ ] Nav active/hover indicator is a gold underline.
- [ ] Footer is `#1e1e1e` / `#393939` divider, no gold border.
- [ ] No raw gold used as text color on a light background anywhere.
- [ ] All reused colors are CSS custom properties, not repeated literals — checked with a grep for stray old-palette values.
- [ ] Font stack matches the canonical `$uds-font-family-base` exactly.
- [ ] Domain-specific literal colors from an external system of record are preserved unchanged and documented as such.
- [ ] Page renders correctly in a browser preview end-to-end (every section, no console errors).
- [ ] Every interactive control is discoverable — hint text or clear affordance, not just `cursor: pointer`.
- [ ] If publishing behind GitHub org/SSO-restricted Pages, deployment build and byte-identity were checked before treating a "missing styling" report as a code bug.
- [ ] Commit message follows Conventional Commits, if a commit was requested.
