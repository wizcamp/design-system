# Project Setup

## Tech stack

- **Framework**: React 19, Next.js 16 (App Router)
- **Styling**: Tailwind CSS v4 with shadcn/ui token conventions
- **Component primitives**: shadcn/ui
- **Icons**: `@tabler/icons-react` — named imports only

## Tailwind v4

No `tailwind.config.js`. All design tokens are declared in `globals.css` under `@theme inline`. Tailwind v4 reads those declarations and auto-generates the corresponding utility classes — `bg-*`, `text-*`, `border-*`, `ring-*`, etc. — so every semantic token defined there is immediately available as a Tailwind class. This is how shadcn/ui semantic tokens (`bg-card`, `text-muted-foreground`) and Wizcamp custom tokens (`bg-surface-canvas`, `bg-action-green`) both become usable as plain utility classes in JSX.

Do not use `@apply` — write utility classes directly in JSX.

## shadcn/ui

Prefer shadcn/ui primitives over raw HTML elements:
- `Button` over `<button>`
- `Separator` over `<hr>`
- `Avatar`, `AvatarImage`, `AvatarFallback` over a raw `<img>` in a circle
- `Card`, `CardContent`, `CardHeader` for card containers

Do not use shadcn/ui components for layout — use Tailwind flex/grid utilities.

## Icons

Always use named imports:

```tsx
import { IconLogout, IconBrandGithub } from '@tabler/icons-react'
```

For the full icon catalog and verification steps, see `icon-discovery.md`.
