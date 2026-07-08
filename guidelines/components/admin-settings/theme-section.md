# ThemeSection

Lets the user choose their preferred color scheme. Renders a horizontal radio group with three options: Light, Dark, and System. Applies the selection immediately via `next-themes` and persists it via the settings mutation.

## Structure

`<SettingsSection title="Theme" description="Choose your preferred color scheme.">`

- `<RadioGroup value={currentTheme ?? 'system'} onValueChange={...} className="flex gap-4">`
  - Three items — each `<div className="flex items-center gap-2">`:
    - `<RadioGroupItem value={value} id={`theme-${value}`} disabled={mutation.isPending} />`
    - `<Label htmlFor={`theme-${value}`}>{label}</Label>`

| Value | Label |
|---|---|
| `light` | `Light` |
| `dark` | `Dark` |
| `system` | `System` |

## Behavior

On selection change:
1. `setTheme(value)` — applies the theme immediately via `next-themes`
2. `mutation.mutate({ theme: value })` — persists to the backend

All radio items are `disabled` while `mutation.isPending` is `true` to prevent double-submission.

## Props

| Prop | Type | Notes |
|---|---|---|
| `currentTheme` | `Theme \| undefined` | Current persisted theme — falls back to `'system'` when undefined |
| `mutation` | `{ mutate: (patch: { theme: Theme }) => void; isPending: boolean }` | The settings mutation instance — passed from the page |

`Theme` is `NonNullable<UserSettings['theme']>` — the three string literals `'light'`, `'dark'`, `'system'`.

## Rules

- `ThemeSection` is `'use client'` — it calls `useTheme()`
- The mutation instance is passed as a prop from the page — `ThemeSection` does not call `useUpdateAdminSettingsMutation()` itself
- The three options are defined as a `const` array at module scope — do not inline them in JSX
- `currentTheme` defaults to `'system'` when undefined — the radio group always has a selected value
- Do not export `Props` — it is file-private
