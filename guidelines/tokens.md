# Design Tokens

## How to use these tokens

This project layers two token sets:

1. **shadcn/ui semantic tokens** — the default. Use these everywhere a
   shadcn equivalent exists. They handle light/dark mode automatically.
2. **Wizcamp custom tokens** — additive. Use only when no shadcn semantic
   token covers the intent. Registered in `globals.css` via `@theme inline`
   so they resolve to clean Tailwind utility classes.

Priority order:
1. shadcn/ui semantic class (`bg-card`, `text-muted-foreground`)
2. Wizcamp custom class (`bg-surface-canvas`, `bg-action-green`)
3. Nothing else — never arbitrary `bg-[var(--token)]`, never hardcoded hex

---

## shadcn/ui semantic tokens

These are the standard shadcn/ui tokens available in every file.
They resolve automatically for light and dark mode.

### Base Colors

| Variable Name | Light Hex | Light OKLCH | Dark Hex | Dark OKLCH |
| :--- | :--- | :--- | :--- | :--- |
| accent | #f59e0b | oklch(0.7686 0.1647 70.0804) | #4e4090 | oklch(0.4291 0.1270 287.8648) |
| accent-foreground | #000000 | oklch(0 0 0) | #ffffff | oklch(1 0 0) |
| background | #f7f9f3 | oklch(0.9088 0.0134 44.0897) | #14111f | oklch(0.1886 0.1068 238.4932) |
| card | #ffffff | oklch(1 0 0) | #3d3070 | oklch(0.3441 0.0728 285.8278) |
| card-foreground | #2d3029 | oklch(0.3391 0.1377 128.0499) | #eef3e8 | oklch(0.8744 0.0895 237.7888) |
| chart-1 | #711cff | oklch(0.6328 0.1945 279.0594) | #8740ff | oklch(0.6484 0.1552 277.3513) |
| chart-2 | #01e7e4 | oklch(0.8906 0.1915 166.5263) | #26ebe9 | oklch(0.7938 0.1357 164.9385) |
| chart-3 | #014ce4 | oklch(0.5536 0.1213 266.5144) | #2666e9 | oklch(0.5847 0.1207 272.5544) |
| chart-4 | #aa45ff | oklch(0.6678 0.2447 274.5355) | #711cff | oklch(0.6328 0.1945 279.0594) |
| chart-5 | #3c0e88 | oklch(0.3691 0.1303 283.8473) | #6318e1 | oklch(0.5471 0.1205 278.8427) |
| destructive | #e11d48 | None | #fb4d6d | None |
| destructive-foreground | #fff1f2 | None | #ffe4e8 | None |
| foreground | #341e63 | oklch(0.3791 0.1751 255.5259) | #eef3e8 | oklch(0.8744 0.0895 237.7888) |
| input | #737373 | oklch(0.5162 0.0467 220.8294) | #ffffff | oklch(1 0 0) |
| muted | #f0f0f0 | oklch(0.9431 0.0205 45.4545) | #2e2250 | oklch(0.3441 0.0766 280.4896) |
| muted-foreground | #6b7269 | oklch(0.5838 0.0608 130.2348) | #b8c4b4 | oklch(0.8205 0.0597 115.0453) |
| popover | #e5ebe0 | oklch(0.8874 0.0296 84.5391) | #3d3070 | oklch(0.3441 0.0728 285.8278) |
| popover-foreground | #000000 | oklch(0 0 0) | #ffffff | oklch(1 0 0) |
| primary | #6318e1 | oklch(0.5471 0.1205 278.8427) | #b588ff | oklch(0.7129 0.1252 259.3395) |
| primary-foreground | #ffffff | oklch(1 0 0) | #000000 | oklch(0 0 0) |
| ring | #a5b4fc | oklch(0.7351 0.1895 257.8262) | #818cf8 | oklch(0.6526 0.1534 264.6151) |
| secondary | #f59e0b | oklch(0.7686 0.1647 70.0804) | #1f0d45 | oklch(0.2761 0.0622 284.8512) |
| secondary-foreground | #6b7269 | oklch(0.5838 0.0608 130.2348) | #b8c4b4 | oklch(0.8205 0.0597 115.0453) |
| sidebar | #e1e7d9 | oklch(0.8999 0.0102 82.8098) | #231c3d | oklch(0.3492 0.0782 278.3263) |
| sidebar-accent | #6b7269 | oklch(0.5838 0.0608 130.2348) | #372d65 | None |
| sidebar-accent-foreground | #ffffff | oklch(1 0 0) | #eef3e8 | oklch(0.8744 0.0895 237.7888) |
| sidebar-border | #c8d0c0 | None | #2e244f | None |
| sidebar-foreground | #2d3029 | oklch(0.3391 0.1377 128.0499) | #eef3e8 | oklch(0.8744 0.0895 237.7888) |
| sidebar-primary | #6674d6 | oklch(0.5657 0.1416 257.1033) | #96a0ea | oklch(0.7716 0.1687 261.7323) |
| sidebar-primary-foreground | #ffffff | oklch(1 0 0) | #ffffff | oklch(1 0 0) |
| sidebar-ring | #96a0ea | oklch(0.7716 0.1687 261.7323) | #6674d6 | oklch(0.5657 0.1416 257.1033) |
| secondary-foreground | #6b7269 | oklch(0.5838 0.0608 130.2348) | #b8c4b4 | oklch(0.8205 0.0597 115.0453) |
| chart-1 | #711cff | oklch(0.6328 0.1945 279.0594) | #8740ff | oklch(0.6484 0.1552 277.3513) |
| chart-2 | #01e7e4 | oklch(0.8906 0.1915 166.5263) | #26ebe9 | oklch(0.7938 0.1357 164.9385) |
| chart-3 | #014ce4 | oklch(0.5536 0.1213 266.5144) | #2666e9 | oklch(0.5847 0.1207 272.5544) |
| chart-4 | #aa45ff | oklch(0.6678 0.2447 274.5355) | #711cff | oklch(0.6328 0.1945 279.0594) |
| chart-5 | #3c0e88 | oklch(0.3691 0.1303 283.8473) | #6318e1 | oklch(0.5471 0.1205 278.8427) |

---

## How to use these tokens

This project layers two token sets:

1. **shadcn/ui semantic tokens** — the default. Use these everywhere a
   shadcn equivalent exists. They handle light/dark mode automatically.
2. **Wizcamp custom tokens** — additive. Use only when no shadcn semantic
   token covers the intent. Registered in `globals.css` via `@theme inline`
   so they resolve to clean Tailwind utility classes.

Priority order:
1. shadcn/ui semantic class (`bg-card`, `text-muted-foreground`)
2. Wizcamp custom class (`bg-surface-canvas`, `bg-action-green`)
3. Nothing else — never arbitrary `bg-[var(--token)]`, never hardcoded hex

---

## shadcn/ui semantic tokens

These are the standard shadcn/ui tokens available in every file.
They resolve automatically for light and dark mode.

### Backgrounds

| Tailwind utility | CSS variable | Light value | Use for |
|---|---|---|---|
| `bg-background` | `--background` | `#F4F3EE` | App/page background |
| `bg-card` | `--card` | `#FFFFFF` | Card and panel surfaces |
| `bg-popover` | `--popover` | `#FFFFFF` | Dropdowns, tooltips, popovers |
| `bg-primary` | `--primary` | `#00C951` | Primary CTA button fills |
| `bg-secondary` | `--secondary` | `#EEEDE8` | Secondary button fills |
| `bg-muted` | `--muted` | `#EEEDE8` | Subtle backgrounds, hover states |
| `bg-accent` | `--accent` | `#EEEDE8` | Hover highlight on menu items |
| `bg-destructive` | `--destructive` | `#EF4444` | Destructive action fills |

### Text

| Tailwind utility | CSS variable | Light value | Use for |
|---|---|---|---|
| `text-foreground` | `--foreground` | `#1A1A2E` | Primary body text and headings |
| `text-card-foreground` | `--card-foreground` | `#1A1A2E` | Text on card surfaces |
| `text-popover-foreground` | `--popover-foreground` | `#1A1A2E` | Text in popovers |
| `text-primary-foreground` | `--primary-foreground` | `#FFFFFF` | Text on primary-filled elements |
| `text-secondary-foreground` | `--secondary-foreground` | `#1A1A2E` | Text on secondary-filled elements |
| `text-muted-foreground` | `--muted-foreground` | `#5C5C7A` | Supporting text, labels, metadata |
| `text-accent-foreground` | `--accent-foreground` | `#1A1A2E` | Text on accent backgrounds |
| `text-destructive` | `--destructive` | `#EF4444` | Destructive text and icons |

### Borders and inputs

| Tailwind utility | CSS variable | Light value | Use for |
|---|---|---|---|
| `border-border` | `--border` | `#E2E1DB` | Default borders and separators |
| `border-input` | `--input` | `#BDBDB8` | Form input borders |
| `ring-ring` | `--ring` | `#00C951` | Focus rings |

### Functional

| Tailwind utility | CSS variable | Use for |
|---|---|---|
| `bg-sidebar` | `--sidebar` | Sidebar background |
| `text-sidebar-foreground` | `--sidebar-foreground` | Sidebar text |
| `bg-sidebar-accent` | `--sidebar-accent` | Sidebar hover states |
| `text-sidebar-accent-foreground` | `--sidebar-accent-foreground` | Text on sidebar hover |
| `border-sidebar-border` | `--sidebar-border` | Sidebar border |
| `ring-sidebar-ring` | `--sidebar-ring` | Sidebar focus rings |

---

## Wizcamp custom tokens

Defined in `globals.css` via `@theme inline`. These extend the shadcn
base for Wizcamp's dual-surface (marketing/LMS) architecture.

### LMS surface layers (light mode only)

The LMS uses six named surface layers that establish visual hierarchy
through background depth rather than borders.

| Tailwind utility | Value | Position in hierarchy | Use for |
|---|---|---|---|
| `bg-surface-canvas` | `#F4F3EE` | 1 — outermost | LMS page background |
| `bg-surface-sunken` | `#EFEEEA` | 2 | Recessed regions below canvas |
| `bg-surface-base` | `#FFFFFF` | 3 | Primary content cards and panels |
| `bg-surface-inset` | `#EEEDE8` | 4 | Inset sections within a card |
| `bg-surface-dim` | `#E8E7E1` | 5 | Disabled states, secondary insets |
| `bg-surface-well` | `#E2E1DB` | 6 — innermost | Deeply nested content, code blocks |

**Rule:** Never skip layers. An inset section inside a card goes
`bg-surface-base` → `bg-surface-inset`, not `bg-surface-base` → `bg-surface-dim`.

**Rule:** Do not add borders between surface layers to indicate hierarchy.
Surface color alone defines depth. Borders are for interactive elements only.

### Marketing surface layers (dark mode only)

The marketing site uses four surface layers anchored at `#22183A`.
Dark mode applies to the marketing site only — never add `dark:` variant
classes to LMS components.

| Tailwind utility | Value | Use for |
|---|---|---|
| `bg-surface-dusk` | `#22183A` | Marketing page background |
| `bg-surface-dusk-raised` | `#2C2050` | Raised cards on marketing |
| `bg-surface-dusk-inset` | `#1A1230` | Inset sections on marketing |
| `bg-surface-dusk-well` | `#130D24` | Deepest nesting on marketing |

### Wizcamp surface extensions

| Tailwind utility | Value | Use for |
|---|---|---|
| `bg-surface-raised-dark` | `#4E4090` | Profile banner backgrounds, elevated dark surfaces |

### Wizcamp action color

| Tailwind utility | Value | Use for |
|---|---|---|
| `bg-action-green` | `#00C951` | Non-shadcn elements needing the brand CTA color |
| `text-action-green` | `#00C951` | Icon or text in success/active states |

**Rule:** On shadcn `Button` components use `bg-primary` / `text-primary-foreground`.
Use `bg-action-green` only on non-shadcn elements where the semantic name
adds clarity. Never use as a background for large surface areas.

### Wizcamp text extensions

| Tailwind utility | Value | Use for |
|---|---|---|
| `text-wizcamp-muted` | `#9494A8` | Captions, timestamps, placeholder text |

---

## Spacing (4px base scale)

Tailwind v4 spacing utilities map directly — no custom tokens needed.

| Tailwind utility | Value | Use for |
|---|---|---|
| `p-1` / `gap-1` / `m-1` | 4px | Tight icon-to-label gaps |
| `p-2` / `gap-2` / `m-2` | 8px | Inline element spacing |
| `p-3` / `gap-3` / `m-3` | 12px | Compact component padding |
| `p-4` / `gap-4` / `m-4` | 16px | Default component padding |
| `p-6` / `gap-6` / `m-6` | 24px | Card padding, section gaps |
| `p-8` / `gap-8` / `m-8` | 32px | Large section padding |

Never hardcode a pixel value for spacing. Always use a Tailwind spacing
utility from this scale.

---

## Border radius

shadcn/ui exposes radius via a single `--radius` CSS variable. Tailwind
maps it to these utilities:

| Tailwind utility | Use for |
|---|---|
| `rounded-sm` | Tags, badges, small chips |
| `rounded-md` | Buttons, inputs, small cards |
| `rounded-lg` | Primary cards and panels |
| `rounded-full` | Avatars, pill badges |