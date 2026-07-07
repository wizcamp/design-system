# Utility Classes

This project uses two layers of Tailwind utility classes for color, typography, radius, and shadow. Both layers are defined as CSS custom properties in `globals.css` and promoted to utility classes via `@theme inline`.

1. **shadcn/ui semantic classes** — the default. Use these everywhere a shadcn equivalent exists. They handle light/dark mode automatically.
2. **Wizcamp custom classes** — additive. Use only when no shadcn semantic class covers the intent.

Priority order:
1. shadcn/ui semantic class (`bg-card`, `text-muted-foreground`)
2. Wizcamp custom class (`bg-surface-canvas`, `bg-action-green`)
3. Nothing else — never `bg-[var(--anything)]`, never a hardcoded hex value

---

## Radius Scale

All radius values are multiples of `--radius` (10px base). Use the utility class — never hardcode `rounded-[10px]`.

| Class | Value |
|---|---|
| `rounded-sm` | 6px |
| `rounded-md` | 8px |
| `rounded-lg` | 10px |
| `rounded-xl` | 14px |
| `rounded-2xl` | 18px |
| `rounded-3xl` | 22px |
| `rounded-4xl` | 26px |

---

## Sidebar-Aware Breakpoints

The admin layout has a ~256px sidebar. Standard Tailwind breakpoints fire on total viewport width, not available content width. Two custom breakpoints account for the sidebar offset:

| Prefix | Viewport | Effective content width | Use for |
|---|---|---|---|
| `sidebar-sm:` | 700px | ~444px | Heading row (title + CTA button) |
| `sidebar-md:` | 796px | ~540px | Filter/sort row (StatusFilterBar + Select) |

Use `sidebar-sm:` and `sidebar-md:` on layout-sensitive wrappers in admin list pages. `sm:` is still acceptable for non-layout concerns like outer padding (`p-4 sm:p-6`).

```tsx
{/* Heading row */}
<div className="flex flex-col gap-3 sidebar-sm:flex-row sidebar-sm:items-center sidebar-sm:justify-between">
  <Button className="w-full sidebar-sm:w-auto">Create</Button>
</div>

{/* Filter/sort row */}
<div className="flex flex-col gap-3 sidebar-md:flex-row sidebar-md:items-center">
  <StatusFilterBar />
  <SelectTrigger className="w-full sidebar-md:w-56" />
</div>
```

---

## Semantic Status Colors

Four status colors beyond `destructive`. Each has a foreground pair.

| Class | Use |
|---|---|
| `text-success` / `bg-success` | Positive outcomes, active states |
| `text-info` / `bg-info` | Informational, neutral notices |
| `text-warning` / `bg-warning` | Caution, degraded states |
| `text-caution` / `bg-caution` | Soft warnings, approaching limits |
| `text-purple` / `bg-purple` | Accent, secondary brand moments |
