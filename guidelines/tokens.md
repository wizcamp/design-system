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

