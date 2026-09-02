---
name: accessibility
description: >
  Design, implement, and audit accessible TypeScript React UI to WCAG 2.2 Level
  AA. Use when building an accessible component, auditing a change for keyboard,
  contrast, or screen-reader support, or choosing semantic HTML and ARIA roles
  in JSX/TSX.
metadata:
  origin: ECC
---

# Accessibility (WCAG 2.2)

Deliver React interfaces that assistive technology (screen readers, switch controls, keyboard navigation) can operate, by implementing WCAG 2.2 success criteria in JSX/TSX.

## Core Concepts

- **POUR Principles**: the foundation of WCAG — Perceivable, Operable, Understandable, Robust.
- **Semantic Mapping**: reach for the native HTML element (`<button>`, `<a>`, `<label>`) before a custom `role`, so accessibility is built in.
- **Accessibility Tree**: the representation of the UI that assistive technology actually reads.
- **Focus Management**: control the order and visibility of the keyboard/screen-reader cursor.
- **Labeling & Hints**: supply context through `<label>`, `aria-label`, and `aria-describedby`.

## How It Works

### Step 1: Identify the Component Role

Determine the functional purpose (button, link, tab). Use the most semantic HTML element available before resorting to a custom `role`.

### Step 2: Define Perceivable Attributes

- Meet text contrast of **4.5:1** (normal) or **3:1** (large/UI).
- Add text alternatives for non-text content (images, icons) via `alt` or `aria-label`.
- Reflow responsively up to 400% zoom without loss of function.

### Step 3: Implement Operable Controls

- Meet a minimum target size of **24x24 CSS px** (SC 2.5.8).
- Make every interactive element keyboard-reachable with a visible focus indicator (SC 2.4.11).
- Provide single-pointer alternatives for dragging movements.

### Step 4: Ensure Understandable Logic

- Keep navigation patterns consistent.
- Give descriptive error messages with correction suggestions (SC 3.3.3).
- Apply Redundant Entry (SC 3.3.7) so users are never asked for the same data twice.

### Step 5: Verify Robust Compatibility

- Expose correct `Name, Role, Value` patterns.
- Announce dynamic status through `aria-live` regions.

## HTML & ARIA Mapping

Reach for the semantic HTML element first; add the ARIA attribute only when JSX needs to fill a gap the element leaves.

| Feature            | Semantic HTML          | ARIA attribute (JSX)          |
| :----------------- | :--------------------- | :---------------------------- |
| **Primary Label**  | `<label htmlFor>`      | `aria-label`                  |
| **Secondary Hint** | —                      | `aria-describedby`            |
| **Action Role**    | `<button>`             | `role="button"` (last resort) |
| **Live Updates**   | —                      | `aria-live="polite"`          |

## Examples

### Accessible Search

```tsx
function ProductSearch() {
  return (
    <form role="search">
      <label htmlFor="search-input" className="sr-only">
        Search products
      </label>
      <input type="search" id="search-input" placeholder="Search..." />
      <button type="submit" aria-label="Submit search">
        <svg aria-hidden="true">...</svg>
      </button>
    </form>
  );
}
```

### Accessible Icon Button

```tsx
function DeleteButton({ onDelete }: { onDelete: () => void }) {
  return (
    <button
      type="button"
      onClick={onDelete}
      aria-label="Delete item"
      aria-describedby="delete-hint"
    >
      <svg aria-hidden="true">...</svg>
      <span id="delete-hint" className="sr-only">
        Permanently removes this item from your list
      </span>
    </button>
  );
}
```

### Accessible Toggle

```tsx
function NotificationToggle({
  enabled,
  onToggle,
}: {
  enabled: boolean;
  onToggle: () => void;
}) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={enabled}
      aria-label="Enable notifications"
      onClick={onToggle}
    >
      {enabled ? "On" : "Off"}
    </button>
  );
}
```

## Common Pitfalls

Lead with the correct behavior; each pitfall below teaches a trap the steps above don't spell out.

- **Operable controls, not click-only containers**: a `<div>` or `<span>` with an `onClick` needs an explicit `role` and keyboard handler to be reachable — reach for `<button>` instead.
- **Signal status with text or an icon, not color alone**: a red border communicates nothing to users who can't perceive the color.
- **Trap focus in modals and release it cleanly on close**: focus stays contained while open and returns to the trigger, escapable via `Escape` or an explicit close button (SC 2.1.2).
- **Write alt text as the content itself**: skip "Image of…" / "Picture of…" — the screen reader already announces the "Image" role.

## Best Practices Checklist

Sign off only when every box is checked for the change under review.

- [ ] Interactive elements meet the **24x24 CSS px** target size.
- [ ] Focus indicators are clearly visible and high-contrast.
- [ ] Modals contain focus while open and release it on close (`Escape` key or close button).
- [ ] Dropdowns and menus restore focus to the trigger element on close.
- [ ] Forms provide text-based error suggestions.
- [ ] Icon-only buttons have a descriptive text label.
- [ ] Content reflows properly when text is scaled.

## References

- [WCAG 2.2 Guidelines](https://www.w3.org/TR/WCAG22/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/TR/wai-aria-practices/)
- [MDN ARIA Reference](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA)

## Related Skills

- `frontend-patterns`
