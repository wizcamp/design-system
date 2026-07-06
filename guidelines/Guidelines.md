# Wizcamp Design System — Guidelines

You are building UI for Wizcamp, an edtech platform for teenagers (ages 13–17).
The tech stack is React, Tailwind v4, and shadcn/ui.
Icons come exclusively from `@tabler/icons-react` via named imports. Never use inline SVGs or lucide-react.

## Reading order

**MUST READ before writing any code:**
1. This file (`Guidelines.md`) — product character, rules, and workflows
2. `setup.md` — providers, CSS imports, build configuration
3. `tokens.md` — when to use which Tailwind tokens
4. `colors.md` - color tokens
5. `typography.md` - font families, scale, rules, etc.
<!-- 6. `components/overview.md` — full component catalog with alternative names (still to be created) -->

**Read on-demand**
- `components/{name}.md` — read BEFORE using that component

## Workflows
### Before using a component
<!-- 1. Check `components/overview.md` for the component catalog -->
2. Read `components/{name}.md` for the specific component
3. Follow all rules, valid props, and usage notes in the guidelines file
4. Do NOT write code using a component until you have read its guidelines file



## Hard rules

- Never hardcode a hex value. Always use a CSS custom property or token from Tailwind 
todo How to determine text styles
- Never use lucide-react. Use @tabler/icons-react only.