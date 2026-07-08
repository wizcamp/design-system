# SecretField

A masked credential input with reveal, copy, and save actions. Used for API keys and other sensitive string values. Manages its own draft/reveal/saved state internally.

## Structure

`<div className="space-y-2">`

1. **Label** — `<Label className="text-sm font-medium">` — always present
2. **Description** (conditional) — `<p className="text-muted-foreground text-xs">` — rendered only when `description` is provided
3. **Input row** — `<div className="flex items-center gap-2">`
   - **InputGroup** — `className="flex-1"`
     - Lock addon (conditional — when `isProtected`) — `<InputGroupAddon align="inline-start">` — `<Lock className="size-4 text-muted-foreground" />`
     - **InputGroupInput** — `type={revealed ? 'text' : 'password'}` — `className="font-mono text-sm"`
     - **Inline-end addon** — `<InputGroupAddon align="inline-end">`
       - Reveal/hide toggle — `<InputGroupButton>` — `<Eye className="size-3.5" />` / `<EyeOff className="size-3.5" />`
       - Copy button (conditional — when `value` exists) — `<InputGroupButton>` — `<Copy className="size-3.5" />`
   - **Save button** (conditional — when not `isProtected`) — `<Button size="sm">` — label cycles: `'Save'` → `'…'` (saving) → `<Check className="size-4" />` (saved, 2 s) → `'Save'`

## Display logic

| State | Input value shown |
|---|---|
| No saved value | Empty, `placeholder` shown |
| Saved value, not revealed, not dirty | Masked: first 4 chars + `•` × (length − 8) + last 4 chars |
| Saved value, revealed, not dirty | Full plaintext value |
| Draft in progress | Draft string (unmasked) |

The input switches to draft mode on focus (when not `isProtected`) — the full saved value is pre-filled into the draft so the user can edit from the existing value.

## Save flow

1. User types a new value → `draft` becomes non-empty → Save button enables
2. User clicks Save → `onSave(draft.trim())` called → button shows `'…'`
3. On settled (parent calls `onSettled`) → button shows `<Check>` for 2 s → resets to `'Save'`, draft cleared

## Protected mode

When `isProtected` is `true`:
- Lock icon appears in the inline-start addon
- Input is `disabled`
- Save button is not rendered
- The field is display-only — the value can be revealed and copied but not changed

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `label` | `string` | required | Field label |
| `description` | `string` | — | Helper text below the label |
| `value` | `string` | — | Current saved value |
| `onSave` | `(value: string) => void` | — | Called with trimmed draft on save |
| `isSaving` | `boolean` | `false` | Disables save button and shows `'…'` |
| `isProtected` | `boolean` | `false` | Renders in read-only protected mode |
| `placeholder` | `string` | — | Shown when no value exists (e.g. `'sk-or-...'`) |

## Icon usage

| Location | Icon | Size |
|---|---|---|
| Protected lock | `Lock` (lucide-react) | `size-4` |
| Reveal toggle (hidden) | `Eye` (lucide-react) | `size-3.5` |
| Reveal toggle (shown) | `EyeOff` (lucide-react) | `size-3.5` |
| Copy button | `Copy` (lucide-react) | `size-3.5` |
| Save confirmed | `Check` (lucide-react) | `size-4` |

## Rules

- `SecretField` is the only permitted pattern for masked credential inputs — do not use a plain `<Input type="password">`
- Never pass the raw value into a visible `<span>` — always use the masking logic
- The save button must be disabled when `draft` is empty, `isSaving` is `true`, or `draft.trim()` is empty
- `SecretField` is `'use client'` — it owns `draft`, `revealed`, and `saved` state
- Do not export `Props` — it is file-private
