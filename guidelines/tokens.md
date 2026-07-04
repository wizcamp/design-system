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
| accent | #711cff | oklch(0.5239 0.2850 288.3272) | #4e4090 | oklch(0.4291 0.1270 287.8648) |
| accent-foreground | #000000 | oklch(0 0 0) | #ffffff | oklch(1.0000 0 0) |
| background | #f7f9f3 | oklch(0.9789 0.0082 121.6273) | #14111f | oklch(0.1887 0.0283 293.3346) |
| border | #2d3029 | oklch(0.3037 0.0130 126.1273) | #dce4d2 | oklch(0.9078 0.0256 126.5689) |
| card | #ffffff | oklch(1.0000 0 0) | #3d3070 | oklch(0.3592 0.1063 289.2818) |
| card-foreground | #2d3029 | oklch(0.3037 0.0130 126.1273) | #eef3e8 | oklch(0.9573 0.0155 126.8214) |
| chart-1 | #711cff | oklch(0.5239 0.2850 288.3272) | #8740ff | oklch(0.5741 0.2599 293.3024) |
| chart-2 | #01e7e4 | oklch(0.8392 0.1436 193.0922) | #26ebe9 | oklch(0.8528 0.1410 193.7031) |
| chart-3 | #014ce4 | oklch(0.4916 0.2375 262.6080) | #2666e9 | oklch(0.5506 0.2090 262.3216) |
| chart-4 | #aa45ff | oklch(0.6172 0.2593 304.4246) | #711cff | oklch(0.5239 0.2850 288.3272) |
| chart-5 | #3c0e88 | oklch(0.3349 0.1759 289.8483) | #6318e1 | oklch(0.4771 0.2590 288.3583) |
| destructive | #e11d48 | oklch(0.5858 0.2220 17.5846) | #fb4d6d | oklch(0.6721 0.2093 14.3131) |
| destructive-foreground | #fff1f2 | oklch(0.9694 0.0152 12.4217) | #ffe4e8 | oklch(0.9419 0.0301 7.5182) |
| foreground | #341e63 | oklch(0.3070 0.1154 293.0169) | #eef3e8 | oklch(0.9573 0.0155 126.8214) |
| input | #737373 | oklch(0.5555 0 0) | #ffffff | oklch(1.0000 0 0) |
| muted | #f0f0f0 | oklch(0.9551 0 0) | #2e2250 | oklch(0.2921 0.0811 292.6961) |
| muted-foreground | #6b7269 | oklch(0.5433 0.0161 138.7230) | #b8c4b4 | oklch(0.8065 0.0257 137.8181) |
| popover | #e5ebe0 | oklch(0.9325 0.0160 130.4249) | #3d3070 | oklch(0.3592 0.1063 289.2818) |
| popover-foreground | #000000 | oklch(0 0 0) | #ffffff | oklch(1.0000 0 0) |
| primary | #6318e1 | oklch(0.4771 0.2590 288.3583) | #b588ff | oklch(0.7192 0.1717 299.5252) |
| primary-foreground | #ffffff | oklch(1.0000 0 0) | #000000 | oklch(0 0 0) |
| ring | #a5b4fc | oklch(0.7853 0.1041 274.7134) | #818cf8 | oklch(0.6801 0.1583 276.9349) |
| secondary | #f59e0b | oklch(0.7686 0.1647 70.0804) | #1f0d45 | oklch(0.2271 0.0977 291.2928) |
| secondary-foreground | #6b7269 | oklch(0.5433 0.0161 138.7230) | #b8c4b4 | oklch(0.8065 0.0257 137.8181) |
| sidebar | #e1e7d9 | oklch(0.9195 0.0198 125.8334) | #231c3d | oklch(0.2532 0.0608 291.1828) |
| sidebar-accent | #6b7269 | oklch(0.5433 0.0161 138.7230) | #372d65 | oklch(0.3392 0.0948 288.5050) |
| sidebar-accent-foreground | #ffffff | oklch(1.0000 0 0) | #eef3e8 | oklch(0.9573 0.0155 126.8214) |
| sidebar-border | #c8d0c0 | oklch(0.8469 0.0235 128.7729) | #2e244f | oklch(0.2955 0.0760 291.7821) |
| sidebar-foreground | #2d3029 | oklch(0.3037 0.0130 126.1273) | #ffffff | oklch(1.0000 0 0) |
| sidebar-primary | #6674d6 | oklch(0.5948 0.1490 274.8277) | #96a0ea | oklch(0.7267 0.1080 277.4551) |
| sidebar-primary-foreground | #ffffff | oklch(1.0000 0 0) | #ffffff | oklch(1.0000 0 0) |
| sidebar-ring | #96a0ea | oklch(0.7267 0.1080 277.4551) | #6674d6 | oklch(0.5948 0.1490 274.8277) |

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