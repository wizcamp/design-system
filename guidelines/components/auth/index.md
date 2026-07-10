# Auth Subsystem

The pre-authentication surfaces for the portal. Two routes — login and join — share a common `AuthLayout` shell and a card-centered visual language. No nav, no sidebar. Public-facing only.

## Hierarchy

```
AuthLayout                               ← app/(auth)/layout.tsx
  ├── LoginPage                          ← app/(auth)/login/page.tsx (RSC)
  │     └── LoginForm                   ← app/(auth)/login/login-form.tsx ('use client')
  └── JoinPage                           ← app/(auth)/join/page.tsx (RSC)
        └── JoinClient                  ← app/(auth)/join/join-client.tsx ('use client')
```

## Components

| Component | File | Role |
|---|---|---|
| `AuthLayout` | [auth-layout.md](auth-layout.md) | Full-height muted background shell — mounted once for all `(auth)` routes |
| `LoginForm` | [login-form.md](login-form.md) | OAuth sign-in card — Google + GitHub buttons, error banner, enroll footer |
| `JoinClient` | [join-client.md](join-client.md) | Magic-link onboarding card — four render branches driven by token validation state |

## Shell contract

`AuthLayout` is a Next.js route layout — it is not imported by page components. It mounts automatically for all routes under `app/(auth)/`. Both pages receive the `bg-muted flex min-h-svh flex-col` shell for free.

Each page RSC acts as a thin guard:
- `LoginPage` — redirects authenticated sessions to `/admin` or `/dashboard` before rendering `LoginForm`
- `JoinPage` — redirects to `/login` when neither `token` nor `error` is present; passes both as props to `JoinClient`

## Responsive behavior

Both cards use the same mobile-first breakpoint pattern:

| Viewport | Background | Card | Card width |
|---|---|---|---|
| Mobile (`< md`) | `bg-card` (full bleed) | No border, no shadow, no radius | `w-full` |
| Desktop (`≥ md`) | `bg-muted` | `rounded-xl border shadow-md bg-card` | `max-w-[400px]` / `max-w-[440px]` |

On mobile the card fills the viewport — the muted background is never visible. On desktop the card floats centered over the muted background.

## Shared visual primitives

- **Wordmark** — `⚡ Wizcamp` — `text-3xl font-bold tracking-tight` — present in every render branch of both surfaces
- **OAuth buttons** — `Button variant="outline" className="w-full gap-2"` — always stacked vertically with `gap-3`
- **Provider icons** — inline SVG, `size-4 shrink-0` — `GoogleIcon` (multi-color paths) and `GitHubIcon` (`fill="currentColor"`)
- **Error banner** — `border-destructive/50 bg-destructive/10 text-destructive rounded-md border px-4 py-3 text-sm`
- **Help link** — `<a href="mailto:...">` — `hover:text-foreground underline underline-offset-4`

## Rules

- Never add navigation, a sidebar, or a header bar to any `(auth)` route
- The wordmark is always the first visual element in every card branch — do not remove or reorder it
- OAuth buttons are always `variant="outline"` — never `variant="default"` or `variant="ghost"`
- Error banners use the destructive token set — never a custom color
- `JoinClient` is the canonical component; `page.client.tsx` is a legacy duplicate — do not add new logic to `page.client.tsx`
