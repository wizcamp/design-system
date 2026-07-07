# Progress Subsystem

A tightly coupled set of components that display student progress across the portal. All share the same two-layer math and the same CSS variables.

## Components

| Component | File | Role |
|---|---|---|
| `ProgressBar` | [progress-bar.md](progress-bar.md) | Horizontal bar — base primitive |
| `DripProgressBar` | [progress-bar.md](progress-bar.md) | Thin wrapper applying drip CSS variable classes |
| `RadialProgress` | [radial-progress.md](radial-progress.md) | Circular ring — base primitive |
| `DripProgressRing` | [radial-progress.md](radial-progress.md) | Thin wrapper applying drip CSS variable classes |
| `LessonNavBar` | [lesson-nav-bar.md](lesson-nav-bar.md) | Portal nav bar — consumes `ProgressBar` with lesson indicator class |

## Two-layer math

All progress components share the same proportional model when `trackValue` is provided:

- **Track arc** spans `trackValue`% — the unlocked / drip-released region
- **Indicator arc** fills `(value / 100) × trackValue`% — visited pages within the unlocked region

This keeps the indicator visually proportionate to the unlocked portion rather than the full bar. When `trackValue` is omitted the indicator fills `value`% of the full width (single-layer mode).

## CSS Variables

Defined in `:root`. Do not use these variables outside the progress subsystem.

| Variable | Utility class | Role |
|---|---|---|
| `--progress-drip-indicator` | `bg-progress-drip-indicator` / `stroke-progress-drip-indicator` | Drip fill (maps to `success`) |
| `--progress-drip-track` | `bg-progress-drip-track` | Drip track |
| `--progress-lesson-indicator` | `bg-progress-lesson-indicator` | Lesson fill (maps to `primary`) |
| `--progress-track-visited` | `bg-progress-track-visited` | Visited step marker |
| `--progress-track-current` | `bg-progress-track-current` | Current step marker |
| `--progress-track-available` | `bg-progress-track-available` | Available (unlocked) step |
| `--progress-track-locked` | `bg-progress-track-locked` | Locked step |

## When to use which

| Context | Component |
|---|---|
| Cohort card / admin student row with drip release | `DripProgressBar` (two-layer) |
| Per-unit breakdown row (unit already unlocked) | `ProgressBar` single-layer, `size="sm"` |
| Cohort card avatar ring with drip release | `DripProgressRing` |
| Stat widget (percentage centered in ring) | `RadialProgress` with `showValue` |
| Lesson page bottom nav | `LessonNavBar` |
