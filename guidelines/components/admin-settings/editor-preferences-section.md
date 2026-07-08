# EditorPreferencesSection

Configures page editor behavior. Contains a save mode select and a validate-on-type toggle. The only settings section that sources its own data — it calls `useEditorSettings()` internally rather than receiving data as props.

## Structure

`<SettingsSection title="Editor Preferences" description="Configure how the page editor behaves." isLoading={isLoading}>`

1. **Save mode row** — `<SettingRow label="Save mode" description="Control when your work is saved to the server.">`
   - `<Select value={autoSave} onValueChange={...}>`
     - `<SelectTrigger className="w-64">` — displays the current mode label
     - `<SelectContent>` — three `<SelectItem>` options:

| Value | Label |
|---|---|
| `live` | `Live — saves on every keystroke` |
| `auto` | `Auto — saves after a pause` |
| `manual` | `Manual — save with ⌘S` |

2. **Validate on type row** — `<SettingRow label="Validate on type" description="Show inline validation errors while typing in the editor.">`
   - `<Switch checked={validateOnType} onCheckedChange={...} />`

## Data source

`useEditorSettings()` provides:

| Value | Type | Notes |
|---|---|---|
| `autoSave` | `'live' \| 'auto' \| 'manual'` | Current save mode |
| `validateOnType` | `boolean` | Current validate-on-type setting |
| `isLoading` | `boolean` | Passed to `SettingsSection` |
| `update` | `(patch) => void` | Persists a setting change |

## Rules

- `EditorPreferencesSection` takes no props — all data comes from `useEditorSettings()`
- `EditorPreferencesSection` is `'use client'` — it calls a hook
- The `SelectTrigger` uses `className="w-64"` to match the `SettingRow` control column width — do not change this
- The three save mode options are defined as a `const` array at module scope — do not inline them in JSX
- Do not add a save button — changes are persisted immediately via `update()`
