# ProgressBar / DripProgressBar

`ProgressBar` is the base horizontal progress primitive. `DripProgressBar` is a thin wrapper that pre-applies the drip CSS variable classes — use it in any drip-release context instead of passing `indicatorClassName` / `trackClassName` manually.

## Structure

`<div className="relative w-full rounded-full bg-muted overflow-hidden {height}">` — `role="progressbar"`

- Height: `h-1.5` (`size="sm"`, unit breakdown rows) or `h-2` (`size="md"`, default, student rows)

Layers (back to front):

1. **Muted base track** — the outer `bg-muted` div itself — always full width
2. **Gray arc** (conditional — only when `trackValue` is set) — `absolute inset-y-0 left-0 rounded-full {trackClassName}` — width = `trackValue%` — represents the unlocked/available region
3. **Indicator arc** — `absolute inset-y-0 left-0 rounded-full transition-all duration-500 {indicatorClassName}` — width = `(value / 100) × trackValue%` in two-layer mode, or `value%` in single-layer mode

See [index.md](index.md) for the two-layer math.

## Props — ProgressBar

| Prop | Type | Default | Notes |
|---|---|---|---|
| `value` | `number` | required | Visited percentage 0–100 — drives the indicator layer |
| `trackValue` | `number` | — | Unlocked percentage 0–100. When provided, enables two-layer mode. |
| `size` | `'sm' \| 'md'` | `'md'` | `sm` = `h-1.5` (unit rows), `md` = `h-2` (student rows) |
| `indicatorClassName` | `string` | `bg-success` | Override the fill layer color |
| `trackClassName` | `string` | `bg-muted-foreground/30` | Override the intermediate track layer color |

## Props — DripProgressBar

Same as `ProgressBar` except:
- `trackValue` is required
- `indicatorClassName` defaults to `bg-progress-drip-indicator`
- `trackClassName` defaults to `bg-progress-drip-track`

## Rules

- Always use `DripProgressBar` in drip-release contexts — never pass `bg-progress-drip-indicator` manually to `ProgressBar`
- `LessonNavBar` owns its own `ProgressBar` instance — do not render a separate bar alongside it
- Do not use `indicatorClassName` to apply arbitrary colors — only progress CSS variable classes or `bg-success` / `bg-primary`
