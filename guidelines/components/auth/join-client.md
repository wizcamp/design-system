# JoinClient

The magic-link onboarding card. Validates a `token` query param against the API on mount and renders one of four branches based on the result. Used for first-time student account activation and returning-student re-entry via invitation link.

## Structure

Outer page wrapper — `<div className="bg-card md:bg-muted flex min-h-svh flex-col items-center md:justify-center md:gap-6 md:px-4 md:py-6">`

Card shell — `<div className="md:bg-card flex w-full flex-col md:max-w-[440px] md:rounded-xl md:border md:shadow-md">`

All four branches render inside the card shell. Each branch uses `<div className="flex flex-col items-center gap-4 p-8 [text-center]">` as its root.

---

### Branch 1 — `error` prop present (OAuth callback error or URL-injected error)

`flex flex-col items-center gap-4 p-8 text-center`

1. Wordmark — `<div className="mb-2 text-3xl font-bold tracking-tight">⚡ Wizcamp</div>`
2. Error banner — `border-destructive/50 bg-destructive/10 text-destructive rounded-md border px-4 py-4 text-sm`
   | Code | Message |
   |---|---|
   | `not_registered` | No portal account found for this email. Check your invitation email or contact james@wizcamp.io. |
   | `account_suspended` | Your account has been suspended. Contact james@wizcamp.io for assistance. |
   | `token_used` | This magic link has already been used. Please contact your camp administrator for a new one. |
   | `oauth_failed` | Sign-in failed. Please try again. |
   | _(fallback)_ | Something went wrong. Please try again. |
3. Help link — `<p className="text-muted-foreground text-sm">Need help? <a href="mailto:james@wizcamp.io" ...>Contact james@wizcamp.io</a></p>`

---

### Branch 2 — `status: 'loading'` (token present, API call in flight)

`flex flex-col items-center gap-4 p-8` (no `text-center`)

1. Wordmark — `text-3xl font-bold tracking-tight`
2. Title skeleton — `<div className="bg-muted h-5 w-48 animate-pulse rounded" />`
3. Subtitle skeleton — `<div className="bg-muted h-4 w-64 animate-pulse rounded" />`
4. Button skeleton 1 — `<div className="bg-muted mt-4 h-10 w-full animate-pulse rounded" />`
5. Button skeleton 2 — `<div className="bg-muted h-10 w-full animate-pulse rounded" />`

---

### Branch 3 — `status: 'valid'` (token validated, student identity resolved)

`flex flex-col items-center gap-6 p-8`

1. **Identity block** — `flex flex-col items-center gap-2 text-center`
   - Wordmark — `mb-2 text-3xl font-bold tracking-tight`
   - Heading — `<h1 className="text-2xl font-semibold md:text-[28px]">`
     - Returning: `"Welcome back!"`
     - New: `"Welcome to {campName}!"`
   - Subtext — `text-muted-foreground text-sm`
     - Returning: `"Sign in to continue {campName} — {cohortName}."`
     - New: `"You're all set for {cohortName}. Sign in to get started."`

2. **OAuth button group** — `flex w-full flex-col gap-3`
   - Google button — `<Button variant="outline" className="w-full gap-2" disabled={oauthPending}>` + `<GoogleIcon />`
   - GitHub button — `<Button variant="outline" className="w-full gap-2" disabled={oauthPending}>` + `<GitHubIcon />`

3. **Account hint** — `<p className="text-muted-foreground text-xs">Use the same account you registered with.</p>`

---

### Branch 4 — `status: 'used'` or `status: 'invalid'` (token expired, already used, or missing)

`flex flex-col items-center gap-4 p-8 text-center`

1. Wordmark — `mb-2 text-3xl font-bold tracking-tight`
2. Error banner — `border-destructive/50 bg-destructive/10 text-destructive rounded-md border px-4 py-4 text-sm`
   - `used`: "This link has already been used. Please contact your camp administrator for a new link."
   - `invalid`: "This link is invalid. Please check your email or contact support."
3. Help link — same pattern as Branch 1

---

## State machine

```
ValidateState =
  | { status: 'loading' }                          ← initial when token present
  | { status: 'valid'; data: MagicLinkValidation } ← API returned 200
  | { status: 'used' }                             ← API returned 409
  | { status: 'invalid' }                          ← API error or no token
```

Initial state is `'loading'` when `token` is present; `'invalid'` when it is absent.

`oauthPending: boolean` — set to `true` on first OAuth button click; disables both buttons to prevent double-submission.

## Icons

Same inline SVG components as `LoginForm` — `GoogleIcon` and `GitHubIcon`, both `size-4 shrink-0`.

## Props

| Prop | Type | Notes |
|---|---|---|
| `token` | `string \| undefined` | Magic link token from URL query param |
| `error` | `string \| undefined` | Error code from URL query param — when present, skips token validation and renders Branch 1 |

## Data

| Source | Provides |
|---|---|
| `apiGet('/lms/auth/magic-link/validate?token=...')` | `MagicLinkValidation` — `{ campName, cohortName, returning }` |
| `NEXT_PUBLIC_API_URL` | OAuth initiation base URL |

## File notes

`join-client.tsx` is the canonical implementation. `page.client.tsx` is a legacy duplicate with identical logic — do not add new features to `page.client.tsx`. Both files currently coexist; `page.client.tsx` should be removed in a future cleanup.

## Rules

- `JoinClient` is `'use client'` — it uses `useState` and `useEffect`
- The `error` prop takes priority — when present, skip all token validation and render Branch 1 immediately
- Both OAuth buttons must be `disabled={oauthPending}` — never allow a second OAuth redirect while one is in flight
- The loading skeleton must match the approximate height of Branch 3 to prevent layout shift
- Error banner padding is `py-4` (not `py-3` as in `LoginForm`) — do not normalize without a design decision
- Never render the dev login button in `JoinClient` — it belongs only in `LoginForm`
