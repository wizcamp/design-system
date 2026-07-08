# Admin Settings Subsystem

The settings page for the admin portal. Composed of a shared structural shell (`SettingsSection`, `SettingRow`) and six content sections rendered in a fixed vertical stack.

## Hierarchy

```
AdminSettingsPage                        ← app/(authenticated)/(admin)/admin/settings/page.tsx
  ├── AdminPageHeader                    ← breadcrumbs: [{ label: 'Settings' }]
  └── AdminPageContent                   ← className="max-w-2xl space-y-6"
        ├── IdentitySection              ← components/settings/identity-section.tsx
        ├── AICreditsSection             ← components/settings/ai-credits-section.tsx
        ├── AIPreferencesSection         ← components/settings/ai-preferences-section.tsx
        ├── EditorPreferencesSection     ← components/settings/editor-preferences-section.tsx
        ├── ThemeSection                 ← components/settings/theme-section.tsx
        └── AboutSection                 ← components/settings/about-section.tsx
```

Every section is wrapped in `SettingsSection`, which provides the card shell. Rows within a section use `SettingRow` for the label/control layout. `SecretField` is a standalone input primitive used inside `AICreditsSection`.

## Components

| Component | File | Role |
|---|---|---|
| `SettingsSection` | [settings-section.md](settings-section.md) | Card shell — title, optional description, loading skeleton |
| `SettingRow` | [setting-row.md](setting-row.md) | Responsive label + control row |
| `SecretField` | [secret-field.md](secret-field.md) | Masked input with reveal, copy, and save actions |
| `IdentitySection` | [identity-section.md](identity-section.md) | Avatar, name, OAuth provider badge, sign-out |
| `AICreditsSection` | [ai-credits-section.md](ai-credits-section.md) | API key entry + credit balance display |
| `AIPreferencesSection` | [ai-preferences-section.md](ai-preferences-section.md) | Model picker + system prompt textarea |
| `EditorPreferencesSection` | [editor-preferences-section.md](editor-preferences-section.md) | Save mode select + validate-on-type toggle |
| `ThemeSection` | [theme-section.md](theme-section.md) | Light / Dark / System radio group |
| `AboutSection` | [about-section.md](about-section.md) | Read-only portal version and API URL |

## Page layout

`AdminPageContent` receives `className="max-w-2xl space-y-6"` — the settings page is a single centered column, never a grid. All sections stack vertically with `space-y-6` gap.

## Section ordering

The section order is fixed and must not be changed:

1. Identity
2. AI Credits
3. AI Preferences
4. Editor Preferences
5. Theme
6. About

## Rules

- Every section must be wrapped in `SettingsSection` — never render a bare card or `<section>` directly
- Every label/control pair inside a section must use `SettingRow` — never lay out label and control ad hoc
- `SecretField` is the only permitted pattern for masked credential inputs — do not use a plain `<Input type="password">`
- Do not add sections outside the six defined above without a corresponding design decision
- The page is `'use client'` because it owns `savingField` state and passes callbacks to sections — this is the only place that state lives
- Sections do not own mutation instances — they receive `updateSettings` / `mutation` as props from the page
- `EditorPreferencesSection` is the only section that sources its own data via `useEditorSettings()` — all other sections receive data as props
