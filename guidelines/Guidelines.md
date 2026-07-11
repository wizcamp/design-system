# Wizcamp Design System — Guidelines

## Product character

Wizcamp is an edtech platform for teenagers (ages 13–17) learning to code.

- **Tone**: Energetic and encouraging — not corporate, not childish
- **Density**: Purposeful whitespace; content-forward without feeling cramped
- **Surface strategy**: Layered backgrounds create hierarchy. Surface color is the primary separation tool — borders are for content elements and interactive controls, not layout region separation.
- **Color**: Brand color is used for primary actions, active states, and small accents. Never use brand color as a large background fill.
- **Elevation**: Shadows are reserved for floating overlays (dropdowns, modals, tooltips) only — not cards or panels

## Reading order

**MUST READ before writing any code:**
1. This file (`Guidelines.md`) — product character, rules, and workflows
2. `setup.md` — tech stack, dependencies, and configuration
3. `foundations/` — colors, fonts, typography, custom spacing, utility class reference, and prose system

**Read on-demand:**
- `composition/` — read when building page layouts or combining components
- `components/{name}.md` or `components/{name}/` — read BEFORE using that component or subsystem

## Workflows

### Before using a component
1. Check `components/catalog.md` for the component catalog
2. For standalone components: read `components/{name}.md`
3. For subsystems: read `components/{name}/index.md` first, then the file for the specific component
4. Follow all rules, valid props, and usage notes in that file
5. Do NOT write code using a component until you have read its guidelines file

### Before using an icon
1. Check `icon-discovery.md` for available icons
2. Do NOT guess icon names — verify the icon exists first
3. If an icon doesn’t exist, pick a different one and verify

### When building a layout
1. Read `composition/layouts.md` for page structure patterns
2. Read `composition/surfaces.md` for layering and background class rules
3. Use Tailwind spacing utilities — never hardcode pixel values

## Hard rules

- Never hardcode a hex value — always use a Tailwind utility class from `globals.css`
- Never hardcode a pixel value for spacing — always use a Tailwind spacing utility
- Always use shadcn/ui primitives over raw HTML elements — `Button` not `<button>`, `Avatar` not `<img>` in a circle
- Whenever possible, avoid inline SVGs for icons — prefer a named import from the icon library (see `icon-discovery.md`)
- Consult `foundations/typography.md` for text styles — do not set font size, weight, or line height ad hoc
- Surface color defines layout hierarchy, not borders — do not add borders between layout regions
- Each logical section gets its own container — never combine unrelated content in one block
- Complexity is revealed progressively — hide secondary controls behind expand, hover, or click
