# Layouts

> Stub — expand as patterns are established.

## Principles

- Each logical section of a page gets its own container. Do not combine unrelated content in one block.
- Page headers are direct children of the route layout — not nested inside a content container.
- Surface color defines visual depth. See `composition/surfaces.md` for the layer system.

## Rules

- Use Tailwind spacing utilities for all gaps and padding — never hardcode pixel values.
- Consult `composition/surfaces.md` for the correct background class at each layer.
- Do not use layout components (flex/grid wrappers) for visual styling — keep structure and appearance separate.
- In admin list pages, use `sidebar-sm:` and `sidebar-md:` breakpoints for layout-sensitive wrappers, not `sm:`. See `foundations/utilities.md` — Sidebar-Aware Breakpoints.

## Spacing tokens

Semantic spacing tokens are defined in `foundations/custom-spacing.md` and registered in `globals.css`. Use them via Tailwind utilities — never hardcode the pixel values.

```tsx
<div className="px-container-padding">…</div>
<section className="py-section-padding">…</section>
<div className="gap-section-title-gap-md">…</div>
```

- `container-padding` — horizontal padding on the outermost page container.
- `section-padding` — vertical padding on full-width page sections.
- `section-title-gap-{sm|md|lg|xl}` — gap between a section title block and its content; scale maps to increasing visual weight of the heading.

Mobile overrides (below Tailwind `sm` / 640px) are applied automatically via a `@media` block in `globals.css`. Use the same utility class — no breakpoint prefix needed.
