# AuthLayout

The root layout for all pre-authentication routes. Provides a full-height muted background column that both `LoginPage` and `JoinPage` render inside.

## Structure

`<div className="bg-muted flex min-h-svh flex-col">`

- Single `<div>` wrapper — no header, no footer, no nav
- `min-h-svh` — fills the full small-viewport height (avoids the iOS address-bar gap)
- `flex-col` — children stack vertically; each page controls its own internal centering

## Props

| Prop | Type | Notes |
|---|---|---|
| `children` | `ReactNode` | Required — the page RSC renders here |

## Rules

- Mount once as a Next.js route layout — never import or render directly in a page component
- Do not add padding, a header, or any chrome to `AuthLayout` — pages own their own layout
- `bg-muted` is the desktop background; individual pages override it to `bg-card` on mobile via their own outermost div
- Do not add `'use client'` — this is a server component
