# IdentitySection

The first section on the admin settings page. Displays the current user's avatar, name, email, and OAuth provider, with a sign-out button. Read-only — no editable fields.

## Structure

`<SettingsSection title="Account">`

1. **Identity row** — `<div className="flex items-center gap-4">`
   - **Avatar** — `<Avatar className="size-16">`
     - `<AvatarImage src={user?.avatarUrl} alt={user?.firstName} />`
     - `<AvatarFallback className="text-lg">` — two-character initials (first letter of first name + first letter of last name, uppercased); falls back to `'?'` when user is null
   - **Text block** — `<div>`
     - Full name — `<p className="font-semibold">` — `{firstName} {lastName}`
     - Email — `<p className="text-muted-foreground text-sm">`
     - OAuth badge (conditional — when `user.oauthProvider` exists) — `<p className="text-muted-foreground mt-0.5 flex items-center gap-1 text-xs">`
       - Provider icon — `<Chrome className="size-3" />` (Google) or `<Github className="size-3" />` (GitHub)
       - Label — `'Connected via Google'` or `'Connected via GitHub'`

2. **Separator** — `<Separator />`

3. **Sign-out button** — `<Button variant="outline" size="sm" onClick={onSignOut}>`
   - `<LogOut className="mr-2 size-4" />Sign out`

## Props

| Prop | Type | Notes |
|---|---|---|
| `user` | `AuthUser \| null \| undefined` | Current authenticated user — all fields rendered conditionally |
| `onSignOut` | `() => void` | Called when the sign-out button is clicked |

## Icon usage

| Location | Icon | Size |
|---|---|---|
| Google OAuth badge | `Chrome` (lucide-react) | `size-3` |
| GitHub OAuth badge | `Github` (lucide-react) | `size-3` |
| Sign-out button | `LogOut` (lucide-react) | `size-4` |

## Rules

- `IdentitySection` is read-only — do not add editable fields
- The OAuth badge is only rendered when `user.oauthProvider` is present — never show it for users without an OAuth connection
- The `Separator` always appears between the identity row and the sign-out button — do not remove it
- Avatar initials are always two characters — first letter of each name part; `'?'` when user is null
- `IdentitySection` is `'use client'` — it receives an `onSignOut` callback
- Do not export `Props` — it is file-private
