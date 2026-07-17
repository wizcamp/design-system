# AdminPageContent

> **Removed.** `AdminPageContent` no longer exists as a component.

The content area wrapper was removed when the admin layout was streamlined. Page content now renders directly as children of the `<main>` element in `AdminLayout`.

## Current pattern

Page-level padding and layout classes are applied directly on the page's outermost element:

```tsx
// Example admin page
export default function CohortsPage() {
  return (
    <div className="p-4 sm:p-6 space-y-6">
      {/* page content */}
    </div>
  );
}
```

The `<main>` in `AdminLayout` carries `min-h-0 flex-1 overflow-auto` — do not add another overflow wrapper inside it.

## Rules

- Do not re-introduce `AdminPageContent` — apply padding directly on the page's outermost element
- Page-specific layout classes (`space-y-6`, `flex`, `grid`, `max-w-2xl`) go on the outermost page element
- Loading skeletons render inside the page's outermost element, not around it
