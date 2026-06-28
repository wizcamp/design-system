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

## Another Section