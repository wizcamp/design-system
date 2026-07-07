# Surfaces

> Stub — expand as patterns are established.

## Principles

- Every content region must sit on a visible surface. Content should never appear to float unstyled on the page.
- Adjacent layers must have sufficient visual contrast. Use background color steps as the primary separation tool — borders are the exception, not the rule.
- Do not nest visible containers more than 3 levels deep.

## Rules

- Use the correct background token for each layer. Consult `tokens.md` for the surface token hierarchy.
- Do not add shadows to static cards or panels — shadows are reserved for floating overlays (dropdowns, modals, tooltips).
- Each scrollable region scrolls independently — do not let one region's overflow affect another.
