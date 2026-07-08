# SettingRow

The canonical layout primitive for a single label/control pair inside a `SettingsSection`. Stacks vertically on mobile and switches to a horizontal split on `sm` and above.

## Structure

`<div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between sm:gap-4">`

1. **Label column** — `<div className="min-w-0">`
   - Label — `<p className="text-sm font-medium">` — always present
   - Description (conditional) — `<p className="text-muted-foreground mt-0.5 text-xs">` — rendered only when `description` is provided

2. **Control column** — `<div className="w-full sm:w-64 sm:shrink-0">`
   - `children` — the control element (input, select, switch, toggle, read-only value)

## Responsive behavior

| Breakpoint | Layout |
|---|---|
| `< sm` (< 640px) | Stacked — label above, control below, full width |
| `≥ sm` (≥ 640px) | Horizontal — label left (flex-1, min-w-0), control right (fixed `w-64`, `shrink-0`) |

The control column is always `w-full` on mobile and `w-64 shrink-0` on desktop. This fixed width keeps all controls visually aligned across rows.

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `label` | `string` | required | Row label — rendered as `<p>` |
| `description` | `string` | — | Optional helper text below the label |
| `children` | `ReactNode` | required | The control — input, select, switch, or read-only value |

## Control patterns

| Control type | Element |
|---|---|
| Text / secret input | `SecretField` or `InputGroup` |
| Dropdown select | `<Select>` (shadcn/ui) |
| Boolean toggle | `<Switch>` (shadcn/ui) |
| Read-only value | `<span className="font-mono text-sm">` or `<span className="text-sm">` |

## Rules

- Every label/control pair inside a `SettingsSection` must use `SettingRow` — never lay out label and control ad hoc
- Do not add margin or padding to `children` — the control column owns its own sizing
- Read-only values use `<span>` directly inside the control column — no wrapper needed
- `SettingRow` has no `'use client'` directive — it is a pure layout component
- Do not export `Props` — it is file-private
