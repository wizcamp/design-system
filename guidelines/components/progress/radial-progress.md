# RadialProgress / DripProgressRing

`RadialProgress` is the base circular progress primitive. `DripProgressRing` is a thin wrapper that pre-applies `stroke-progress-drip-indicator` — use it in drip-release contexts instead of passing `indicatorClassName` manually.

## Structure

`<div className="relative inline-flex items-center justify-center" style="width:{size}px; height:{size}px">` — `role="progressbar"`

- Default `size` = 40px, `strokeWidth` = 4px

SVG layers (back to front, all `<circle>` elements, ring starts at 12 o'clock via `-rotate-90` on the `<svg>`):

1. **Muted base ring** — `stroke-muted`, full circumference, no dash offset — always present
2. **Gray arc** (conditional — only when `trackValue` is set) — `stroke-muted-foreground/30`, `strokeDashoffset` animates to `circumference - (trackValue / 100) × circumference` — represents the unlocked region
3. **Indicator arc** — `{indicatorClassName}` (default `stroke-success`), `strokeDashoffset` animates to `circumference - effectivePct / 100 × circumference` — `effectivePct = (value / 100) × trackValue` in two-layer mode, or `value` in single-layer mode
4. **Stat label** (conditional — only when `showValue`) — SVG `<text>` centered at `(size/2, size/2)`, counter-rotated 90° so it reads upright — `fontSize = size / 4`, `fill-foreground font-medium`

Content layers (over the SVG):

5. **Avatar slot** (conditional — only when `children` and not `showValue`) — `relative z-10 flex items-center justify-center` — content centered inside the ring

`showValue` and `children` are mutually exclusive — `showValue` takes precedence.

See [index.md](index.md) for the two-layer math.

## Props — RadialProgress

| Prop | Type | Default | Notes |
|---|---|---|---|
| `value` | `number` | required | Progress percentage 0–100 |
| `trackValue` | `number` | — | Unlocked percentage 0–100. Enables two-layer mode. |
| `size` | `number` | `40` | Diameter in px |
| `strokeWidth` | `number` | `4` | Ring stroke width in px |
| `indicatorClassName` | `string` | `stroke-success` | Override the progress arc color |
| `showValue` | `boolean` | `false` | Stat mode — renders percentage as centered SVG text |
| `children` | `ReactNode` | — | Avatar mode — content centered inside the ring |

## Props — DripProgressRing

Same as `RadialProgress` except:
- `trackValue` is required
- `indicatorClassName` defaults to `stroke-progress-drip-indicator`

## Rules

- Always use `DripProgressRing` in drip-release contexts — never pass `stroke-progress-drip-indicator` manually to `RadialProgress`
- Do not use `indicatorClassName` to apply arbitrary stroke colors — only progress CSS variable classes or `stroke-success` / `stroke-primary`
- `size` and `strokeWidth` are in px — do not pass Tailwind class strings
