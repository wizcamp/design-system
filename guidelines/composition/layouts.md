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
