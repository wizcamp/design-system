# Wizcamp Design System — Guidelines

You are building UI for Wizcamp, an edtech platform for teenagers (ages 13–17).
The tech stack is React, Tailwind v4, and shadcn/ui.
Icons come exclusively from `@tabler/icons-react` via named imports. Never use inline SVGs or lucide-react.

## When to read other files

- Before writing any code at all → read `setup.md`
- Before using ANY color, background, or text color → read `tokens.md`
- Before setting ANY font size, weight, or line height → read `typography.md`
- Before using ANY spacing value → read `tokens.md` (spacing section)
- Before building a compact identity card → read `components/profile-card.md`
- Before building a profile/banner view → read `components/profile-banner.md`
- Before building a settings/form card → read `components/ai-credits.md`

## Hard rules

- Never hardcode a hex value. Always use a CSS custom property or Tailwind token from `tokens.md`.
- Never use Tailwind default size classes (`text-sm`, `text-base`, `text-lg`). Use only the type scale in `typography.md`.
- Never use lucide-react. Use @tabler/icons-react only.
- Surface color defines layout hierarchy — do not add borders between layout regions unless they are interactive elements.
- All spacing must use the 4px base scale tokens defined in `tokens.md`.