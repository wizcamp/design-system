# Surfaces

## Principles

- Every content region must sit on a visible surface. Content should never appear to float unstyled on the page.
- Adjacent layers must have sufficient visual contrast. Use background color steps as the primary separation tool — borders are the exception, not the rule.
- Do not nest visible containers more than 3 levels deep.

## The Four-Layer System

Four background layers are defined in `globals.css`, each a distinct value in both light and dark mode. Layer depth maps directly to visual elevation.

| Layer | Class | Role | Examples |
|---|---|---|---|
| Canvas | `bg-background` | Page root, outermost shell | `<body>`, page wrappers, route layouts |
| Recessed | `bg-sidebar` / `bg-muted` | Sidebar, filter bars, recessed panels | Admin sidebar, filter toolbars, tab bars |
| Raised | `bg-card` | Cards, drawers, sheet panels | Content cards, form drawers, detail panels |
| Floating | `bg-popover` | Dropdowns, tooltips, popovers | DropdownMenu, Tooltip, Popover |

`bg-sidebar` and `bg-muted` are both recessed-layer classes but serve different contexts: `bg-sidebar` is for the navigation sidebar specifically; `bg-muted` is for recessed UI regions within the content area (filter bars, empty states, secondary panels).

## Rules

- Use the correct background class for each layer. Consult `foundations/utilities.md` for the full list.
- Do not skip layers — a card (`bg-card`) should sit on canvas or recessed, not directly inside another card.
- Do not add shadows to static cards or panels — shadows are reserved for floating overlays (dropdowns, modals, tooltips).
- Borders separate content elements and interactive controls, not layout regions. Do not add a border between a sidebar and a content area — the background color difference is the separator.
- Each scrollable region scrolls independently — do not let one region's overflow affect another.

See `foundations/prose.md` for the prose surface system.

See `components/code-block.md` for the always-dark code block surface exception.
