# Utility Classes

This project uses two layers of Tailwind utility classes for color, typography, radius, and shadow. Both layers are defined as CSS custom properties in `globals.css` and promoted to utility classes via `@theme inline`.

1. **shadcn/ui semantic classes** — the default. Use these everywhere a shadcn equivalent exists. They handle light/dark mode automatically.
2. **Wizcamp custom classes** — additive. Use only when no shadcn semantic class covers the intent.

Priority order:
1. shadcn/ui semantic class (`bg-card`, `text-muted-foreground`)
2. Wizcamp custom class (`bg-surface-canvas`, `bg-action-green`)
3. Nothing else — never `bg-[var(--anything)]`, never a hardcoded hex value

---

