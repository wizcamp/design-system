# Prose (MDX Content)

The prose system controls typography and spacing for instructor-authored MDX lesson content. It is built on a custom `.prose` class in `globals.css` — not Tailwind Typography (`@tailwindcss/typography`).

---

## The Two Classes

| Class | What it does |
|---|---|
| `prose` | Enters the prose context. Applies typography, spacing, and color to all standard HTML elements inside it. |
| `not-prose` | Exits the prose context. All prose rules are suppressed for this element and all its descendants. |

The selector pattern used in `globals.css` is `:where(el):not(:where(.not-prose, .not-prose *))` — this drops element specificity to zero so Tailwind utilities always win, and makes `not-prose` a genuine full escape with no per-element reset rules required.

---

## Prose CSS Variables

Defined in `:root`. No `.dark` overrides needed — all reference shadcn variables that adapt automatically.

| Variable | Value | Role |
|---|---|---|
| `--prose-body` | distinct per mode | Body text color |
| `--prose-heading` | `var(--foreground)` | Heading color |
| `--prose-muted` | `var(--muted-foreground)` | Blockquote, figcaption, secondary text |
| `--prose-border` | `var(--border)` | Blockquote left border, table borders, `<hr>` |
| `--prose-code-bg` | `var(--muted)` | Inline code pill background |

---

## Prose Defaults

Applied to the `.prose` container itself (not element-scoped):

- `color: var(--prose-body)`
- `max-width: none` — prose never constrains its own width; the layout wrapper does
- `line-height: 1.8`
- `font-size: 1.0625rem`
- First child: `margin-top: 0`; last child: `margin-bottom: 0`

---

## The Split Component Pattern

Every custom MDX component (Callout, Quiz, Steps, etc.) is split into two parts:

**Structural outer element** — always gets `not-prose` as the first class. The component's chrome (border, background, padding, header strip) must escape prose entirely. Outer spacing (`my-6` or `my-8`) is set explicitly on this element — never inherited from prose.

**Content slot div** — any div that renders instructor-authored markdown children gets `prose` to re-enter the prose context inside the `not-prose` boundary. The `:where()/:not()` selector pattern means a nested `.prose` inside a `.not-prose` creates a new prose scope automatically.

```tsx
{/* Structural outer — seals chrome */}
<div role="note" className={cn('not-prose my-6 rounded-lg border p-4', v.bgClass)}>
  {/* Title row — structural, no prose styles needed */}
  <div className="flex items-center gap-2">...</div>
  {/* Content slot — re-enters prose */}
  <div className={cn('prose [&>*:first-child]:mt-0 [&>*:last-child]:mb-0', ...)}>
    {children}
  </div>
</div>
```

The `[&>*:first-child]:mt-0 [&>*:last-child]:mb-0` edge-clamp on content slot divs prevents prose paragraph margins from accumulating against the component's own padding.

---

## `<figure>` vs `<div>` Convention

| Wrapper | When to use |
|---|---|
| `<figure>` + `<figcaption>` | Static or passively embedded artifact with an optional caption — images, iframes, embeds |
| `<div role="...">` | Interactive UI shell — video players, quizzes, checklists, glossaries |

`<figure>` is safe inside `not-prose` — the `:where()/:not()` guard means `.prose figure` rules never fire inside a `not-prose` container. Reset browser default margins with `my-0` or the component's own outer spacing.

---

## `@layer components` Exception

`@layer components` in `globals.css` is acceptable only for always-dark, theme-invariant component chrome that cannot be expressed with shadcn utility classes. `CodeBlock` and `Terminal` are the only current examples — their `--code-*` variables are hardcoded hex values that do not respond to `.dark`. Every other MDX component uses pure Tailwind utility classes only.

---

## Rendering Surfaces

Both the student learn page and admin editor preview use `className="prose max-w-none"` — no modifier classes needed. The `:where()/:not()` selector pattern and the component split handle everything.

---

## Current Component Split State

| Component | `not-prose` on | `prose` content slot |
|---|---|---|
| Callout | outer `<div>` | body content div |
| Quiz | outer `<div>` | question div, explanation div |
| Steps | outer `<ol>` | each step body content div |
| Checklist | outer `<div>` | deferred to production styling pass |
| Glossary | outer `<div>` | none — no instructor prose slot |
| CodeBlock | outer `<div>` | none — `@layer components` exception |
| Terminal | outer `<div>` | none — `@layer components` exception |

---

## Checklist for New MDX Components

1. Put `not-prose` as the first class on the outermost structural element's className
2. Set explicit `my-6` or `my-8` on the outer element — never rely on prose for outer spacing
3. Put `prose` as the first class on any div that renders instructor-authored markdown children
4. Add `[&>*:first-child]:mt-0 [&>*:last-child]:mb-0` to each `prose` content slot div
5. Use `<figure>` + `<figcaption>` for static/embedded artifacts; use `<div role="...">` for interactive UI shells
6. If the component needs always-dark theme-invariant chrome, follow the CodeBlock/Terminal `@layer components` pattern — justify this explicitly; it is not the default
