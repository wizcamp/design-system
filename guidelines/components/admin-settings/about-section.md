# AboutSection

The last section on the settings page. Displays read-only environment metadata — portal version and API URL. No props, no data fetching, no interactivity.

## Structure

`<SettingsSection title="About">`

Two `SettingRow` instances:

1. `label="Portal version"` — `<span className="font-mono text-xs">0.1.0</span>`
2. `label="API URL"` — `<span className="max-w-xs truncate font-mono text-xs">{process.env.NEXT_PUBLIC_API_URL ?? '—'}</span>`

## Rules

- `AboutSection` takes no props
- `AboutSection` has no `'use client'` directive — it is a pure layout component
- The version string is hardcoded — update it manually when the version changes
- `NEXT_PUBLIC_API_URL` is read at render time — `'—'` is shown when the env var is not set
- The API URL span uses `max-w-xs truncate` to prevent overflow on long URLs
