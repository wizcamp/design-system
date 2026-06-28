# Project Setup

## Tech stack

- **Framework**: React 18, Next.js (App Router)
- **Styling**: Tailwind CSS v4 with shadcn/ui token conventions
- **Component primitives**: shadcn/ui
- **Icons**: `@tabler/icons-react` — named imports only

## Tailwind v4 notes

Tailwind v4 uses a CSS-first config. There is no `tailwind.config.js`.
All theme customization lives in the global CSS file via `@theme inline`.
Do not generate a `tailwind.config.js` or `tailwind.config.ts` file.
Do not use `@apply` — write utility classes directly in JSX.

## shadcn/ui component usage

Prefer shadcn/ui primitives over raw HTML elements:
- `Button` over `<button>`
- `Separator` over `<hr>`
- `Avatar`, `AvatarImage`, `AvatarFallback` over a raw `<img>` in a circle
- `Card`, `CardContent`, `CardHeader` for card containers

Do not use shadcn/ui components for layout — use Tailwind flex/grid
utilities for layout and spacing.

## Icon imports

Always import icons like this:

```tsx
import { IconLogout, IconBrandGithub } from '@tabler/icons-react'
```

Never use inline SVGs. Never import from `lucide-react`.

## Token usage

All color, spacing, and radius tokens are documented in `tokens.md`.
Read that file before applying any visual styling.