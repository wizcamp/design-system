# LoginForm

The OAuth sign-in card for the portal login surface. Renders a centered card with the Wizcamp wordmark, an optional error banner, two OAuth provider buttons, and an enroll footer link.

## Structure

Outer wrapper — `<div className="md:bg-card flex w-full flex-col md:max-w-[400px] md:rounded-xl md:border md:shadow-md">`

1. **Card body** — `<div className="flex flex-col items-center gap-6 p-8">`

   a. **Identity block** — `flex flex-col items-center gap-2 text-center`
      - Wordmark — `<div className="mb-2 text-3xl font-bold tracking-tight">⚡ Wizcamp</div>`
      - Heading — `<h1 className="text-2xl font-semibold md:text-[28px]">Sign in to your portal</h1>`
      - Subtext — `<p className="text-muted-foreground text-sm">Use the same account you signed up with.</p>`

   b. **Error banner** (conditional — shown when `error` query param is present)
      - `<div className="border-destructive/50 bg-destructive/10 text-destructive w-full rounded-md border px-4 py-3 text-sm">`
      - Error codes → display strings:
        | Code | Message |
        |---|---|
        | `not_registered` | No portal account found for this email. Check your invitation email or contact james@wizcamp.io. |
        | `account_suspended` | Your account has been suspended. Contact james@wizcamp.io for assistance. |
        | `oauth_failed` | Sign-in failed. Please try again. |
        | `access_denied` | Access denied. Contact james@wizcamp.io if you believe this is an error. |
        | _(fallback)_ | Something went wrong. Please try again. |

   c. **OAuth button group** — `<div className="flex w-full flex-col gap-3">`
      - Google button — `<Button variant="outline" className="w-full gap-2">` + `<GoogleIcon />` + "Continue with Google"
      - GitHub button — `<Button variant="outline" className="w-full gap-2">` + `<GitHubIcon />` + "Continue with GitHub"
      - Dev login section (conditional — `IS_LOCAL` only, remove before production):
        - Divider — `relative my-1` with centered `<span className="bg-card text-muted-foreground px-2">local dev only</span>`
        - `<Button variant="secondary" className="w-full">Dev Login (Admin)</Button>`

2. **Card footer** — `<div className="border-t px-8 py-4 text-center">`
   - `<p className="text-muted-foreground text-xs">Don't have an account? <a href="https://wizcamp.io" ...>Enroll at wizcamp.io</a></p>`
   - Link classes: `hover:text-foreground underline underline-offset-4`

## Page-level wrapper (LoginPage)

`LoginPage` wraps `LoginForm` in a `<Suspense>` and renders the footer copyright below it:

```
<div className="bg-card md:bg-muted flex min-h-svh flex-col items-center md:justify-center md:gap-6 md:px-4 md:py-6">
  <Suspense fallback={...}>
    <LoginForm />
    <footer className="mt-auto flex w-full items-center justify-center gap-4 py-6 md:mt-0">
      <p className="text-muted-foreground text-xs">© {year} Wizcamp</p>
    </footer>
  </Suspense>
</div>
```

The `Suspense` fallback renders an invisible `<div className="w-full max-w-sm" />` placeholder and an `invisible` copyright line to prevent layout shift while `useSearchParams()` resolves.

## Icons

Both icons are inline SVG components defined in the same file — not imported from an icon library.

| Component | Size | Fill |
|---|---|---|
| `GoogleIcon` | `size-4 shrink-0` | Multi-color paths (`#4285F4`, `#34A853`, `#FBBC05`, `#EA4335`) |
| `GitHubIcon` | `size-4 shrink-0` | `fill="currentColor"` — inherits text color |

## Props

`LoginForm` takes no props. All data is sourced from `useSearchParams()`.

| Hook / source | Provides |
|---|---|
| `useSearchParams()` | `error` (error code string), `returnTo` (redirect path after OAuth) |
| `NEXT_PUBLIC_API_URL` | OAuth initiation base URL |
| `NEXT_PUBLIC_API_URL_INTERNAL` | Presence indicates local dev — enables dev login button |

## OAuth flow

`initiateOAuth(provider)` constructs a URL to `{OAUTH_BASE}/lms/auth/oauth/initiate` with `provider` and optional `returnTo` params, then sets `window.location.href`. `returnTo` is validated with `isSafeRedirectPath` before being appended.

## Rules

- `LoginForm` is `'use client'` — it calls `useSearchParams()`
- Always wrap `LoginForm` in `<Suspense>` at the page level — `useSearchParams()` requires it under the App Router
- The dev login button must never appear in production — it is gated on `IS_LOCAL` (`!!NEXT_PUBLIC_API_URL_INTERNAL`)
- OAuth buttons are always `variant="outline"` — never change the variant
- The footer enroll link always points to `https://wizcamp.io` — never an internal route
- The copyright footer is rendered by `LoginPage`, not by `LoginForm` — do not move it inside the card
