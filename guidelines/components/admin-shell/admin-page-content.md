# AdminPageContent

The content area wrapper rendered as the second child of every admin page. Owns the canonical `p-4 sm:p-6` padding for the content region inside `SidebarInset`.

## Structure

`<main className="p-4 sm:p-6 {className}">`

- Single `<main>` element — the only `<main>` in the admin layout tree (`SidebarInset` is a `<div>`)
- `className` is merged via `cn()` — page-specific layout classes (`space-y-6`, `flex`, `grid`, `max-w-2xl`) go here, not on a child div

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `children` | `ReactNode` | required | Page content |
| `className` | `string` | — | Additional classes merged via `cn()` — use for page-specific layout like `space-y-6` or `max-w-2xl` |

## Rules

- Always the second child of the page — immediately after `AdminPageHeader`
- Never add padding inside `AdminPageContent` children to compensate for the wrapper — the wrapper owns all edge padding
- Page-specific layout classes (`space-y-6`, `flex`, `grid`, `max-w-2xl`) go on `className`, not on a wrapper div inside
- Do not nest another `AdminPageContent` inside a page
- Used for both loading and loaded states — the loading skeleton renders inside `AdminPageContent`, not around it
