# Typography

Wizcamp uses two font families:
- **Inter** — all general UI text
- **Plus Jakarta Sans** — LMS heading text. Registered as two variants:
  - `font-lms-heading` — SemiBold (600) for hero and card headings
  - `font-lms-header-secondary` — Bold (700) for section-level headings in cards

Never set `font-size` directly. Always use the classes below.

## Type scale

| Class | Size | Weight | Line height | Font | Use for |
|---|---|---|---|---|---|
| `.wiz-hero` | 32px | 600 | 1.2 | Plus Jakarta Sans | Profile name, hero headings in banners |
| `.wiz-display` | 28px | 700 | 1.2 | Inter | Page-level display headings |
| `.wiz-heading` | 20px | 700 | 1.3 | Plus Jakarta Sans | Section headings, card titles |
| `.wiz-subheading` | 16px | 600 | 1.4 | Inter | Sub-section labels |
| `.wiz-body` | 14px | 400 | 1.5 | Inter | Default body text |
| `.wiz-label` | 13px | 500 | 1.4 | Inter | Form labels, UI labels, button text |
| `.wiz-caption` | 12px | 400 | 1.4 | Inter | Metadata, timestamps, helper text |
| `.wiz-caption-bold` | 12px | 600 | 1.4 | Inter | Badges, status labels |

## Rules

- Headings: use `--text-primary`
- Body and labels: use `--text-primary` or `--text-secondary`
- Captions and metadata: use `--text-muted`
- Reduce visual hierarchy through size class, not opacity