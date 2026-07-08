# AIPreferencesSection

Configures the default AI model and system prompt used across the platform. Contains a searchable model picker (combobox) and a freeform system prompt textarea with an explicit save action.

## Structure

`<SettingsSection title="AI Preferences" description="Configure the AI model and system prompt used across the platform." isLoading={isLoading}>`

1. **Model row** — `<SettingRow label="Model" description="Select the default AI model for completions.">`
   - **Combobox** — `<Popover>` + `<Command>` pattern
     - Trigger — `<PopoverTrigger type="button">` — styled via `buttonVariants({ variant: 'outline' })` + `'w-full justify-between'`
       - Label span — `text-muted-foreground` when loading, default color when loaded
       - `<ChevronsUpDown className="ml-2 size-4 shrink-0 opacity-50" />`
     - Content — `<PopoverContent align="start" className="w-[var(--anchor-width)] p-0">`
       - `<Command>` with `<CommandInput placeholder="Search models…" />`
       - `<CommandList>` → `<CommandEmpty>No model found.</CommandEmpty>` + `<CommandGroup>`
       - Each option — `<CommandItem>` — selecting calls `updateSettings({ aiModel: option.id })` and closes the popover
   - The model list always starts with `AUTO_OPTION` (`{ id: 'openrouter/auto', name: 'Auto (OpenRouter selects)' }`)
   - If the saved model is not in the fetched catalog, it is injected as `{ id: saved, name: saved }` after `AUTO_OPTION`

2. **System prompt block** — `<div className="space-y-2">`
   - Label — `<label className="text-sm font-medium">System prompt</label>`
   - Helper text — `<p className="text-muted-foreground text-xs">`
   - Textarea — `<Textarea rows={4} className="text-sm" />`
     - Value: `promptDraft` when dirty, otherwise `settings?.aiSystemPrompt ?? ''`
   - Save row — `<div className="flex justify-end">`
     - `<Button size="sm">` — disabled when prompt is not dirty or `isPending`
     - Label cycles: `'Save'` → `'…'` (pending) → `<Check className="size-4" />` (saved, 2 s) → `'Save'`

## State

| State | Type | Notes |
|---|---|---|
| `promptDraft` | `string` | Local draft — empty string means not dirty |
| `promptSaved` | `boolean` | Controls the 2 s `<Check>` flash after save |
| `open` | `boolean` | Combobox open/closed |

A prompt is dirty when `promptDraft !== ''` and `promptDraft !== (settings?.aiSystemPrompt ?? '')`.

## Props

| Prop | Type | Notes |
|---|---|---|
| `settings` | `AdminSettings \| undefined` | Provides `aiModel` and `aiSystemPrompt` |
| `isLoading` | `boolean` | Passed to `SettingsSection` |
| `updateSettings` | `(patch: Partial<AdminSettings>) => void` | Called for both model and prompt saves |
| `isPending` | `boolean` | Disables the prompt save button while a mutation is in flight |

## Icon usage

| Location | Icon | Size |
|---|---|---|
| Combobox chevron | `ChevronsUpDown` (lucide-react) | `size-4` |
| Prompt save confirmed | `Check` (lucide-react) | `size-4` |

## Rules

- `AIPreferencesSection` is `'use client'` — it owns `promptDraft`, `promptSaved`, and `open` state
- The model combobox uses `PopoverTrigger` directly (not `asChild` on a `Button`) — do not change this
- `PopoverContent` width is anchored to the trigger via `w-[var(--anchor-width)]` — do not use a fixed width
- The system prompt save button is always right-aligned — do not move it
- Do not export `Props` — it is file-private
