# SettingsSection

The card shell that wraps every settings section. Provides a consistent `bg-card` rounded border card with a title, optional description, and a loading skeleton state.

## Structure

`<section className="bg-card rounded-lg border p-6">`

1. **Title** — `<h2 className="text-sm font-semibold">` — always present
2. **Description** (conditional) — `<p className="text-muted-foreground mt-1 text-sm">` — rendered only when `description` is provided
3. **Body** — `<div className="mt-4 space-y-4">`
   - **Loading state** — two `<Skeleton className="h-10 w-full" />` stacked with `space-y-4`
   - **Loaded state** — `children`

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `title` | `string` | required | Section heading — rendered as `<h2>` |
| `description` | `string` | — | Optional subtitle below the title |
| `isLoading` | `boolean` | `false` | When `true`, replaces children with two skeleton rows |
| `children` | `ReactNode` | required | Section content — `SettingRow` instances, custom layouts |

## Loading skeleton

When `isLoading` is `true`, two full-width `h-10` skeletons are shown. This is a generic placeholder — sections with known row counts do not customize the skeleton count.

## Rules

- Every settings section must be wrapped in `SettingsSection` — never render a bare card
- `isLoading` should be `true` only while the section's data is being fetched — not while a mutation is pending
- Do not add padding inside `children` to compensate for the card padding — `p-6` on the card owns all edge spacing
- `space-y-4` on the body div is the canonical row gap — do not override it with a wrapper div
- `SettingsSection` is `'use client'` because it imports `Skeleton` — do not remove the directive
