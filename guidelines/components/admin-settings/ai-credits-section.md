# AICreditsSection

Displays the user's OpenRouter API key and live credit balance. Used on both the admin settings page and the student settings page — the `isProtected` prop switches between editable (admin) and read-only (student) modes.

## Structure

`<SettingsSection title="AI Credits" isLoading={isLoadingSettings || isLoadingCredits}>`

1. **SecretField** — always rendered
   - `label="OpenRouter API Key"`
   - `description="Copy this key into your development environment to use AI features in your projects."`
   - `placeholder="sk-or-..."`
   - `isProtected` — `false` for admin (editable), `true` for student (read-only)
   - `onSave` / `isSaving` — wired only when not protected

2. **Credit balance block** (conditional — when `credits` is truthy) — `<div className="space-y-2">`
   - Three `SettingRow` instances:
     - `label="Credits used"` — `<span className="font-mono text-sm">{credits.usage.toFixed(4)}</span>` — `'—'` when null
     - `label="Remaining"` — `<span className="font-mono text-sm">{credits.limitRemainingUsd.toFixed(4)}</span>` — `'Unlimited'` when null
     - `label="Expires"` — `<span className="text-sm">{formatCompactDay(credits.expiresAt)}</span>` — `'Never'` when null

3. **Empty state** (conditional — when `credits === null && !settings?.aiApiKey`) — `<p className="text-muted-foreground text-sm">` — `"Your AI credits haven't been set up yet. Contact your instructor."`

## Loading state

`isLoading` is `true` when either `isLoadingSettings` or `isLoadingCredits` is `true`. `SettingsSection` renders two skeleton rows in this state.

## Props

| Prop | Type | Default | Notes |
|---|---|---|---|
| `settings` | `AdminSettings \| UserSettings \| undefined` | — | Provides `aiApiKey` |
| `credits` | `AiKeyMetadata \| null \| undefined` | — | `null` = no credits configured; `undefined` = still loading |
| `isLoadingSettings` | `boolean` | `false` | |
| `isLoadingCredits` | `boolean` | `false` | |
| `isProtected` | `boolean` | `false` | `true` for student view — disables key editing |
| `onSave` | `(key: string) => void` | — | Called with the new API key value |
| `isSaving` | `boolean` | `false` | Passed to `SecretField` |

## Rules

- `AICreditsSection` is `'use client'` — it receives callbacks
- The credit balance block and the empty state are mutually exclusive — never render both
- Credit values are always formatted with `.toFixed(4)` — do not round differently
- Do not export `Props` — it is file-private
