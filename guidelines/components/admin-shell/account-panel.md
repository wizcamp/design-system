# AccountPanel

Thin adapter component that lives in `AdminHeader`. Wires up auth, settings, and sign-out logic and delegates all rendering to `AccountMenu` in `components/ui/`.

## Files

| File | Role |
|---|---|
| `components/admin/AccountPanel.tsx` | Adapter — hooks, sign-out handler, data wiring |
| `components/ui/account-menu.tsx` | Presentational — `DropdownMenu` trigger + menu content |

## AccountPanel (adapter)

No props. Sources all data internally:

| Hook / import | Provides |
|---|---|
| `useAdminUser()` | `user` (`AuthUser`) |
| `useAdminSettingsQuery()` | `settings.theme` |
| `useUpdateAdminSettingsMutation()` | passed to `useThemePersistence` |
| `useThemePersistence(updateSettings)` | `theme`, `applyTheme` |
| `useRouter()` + `useQueryClient()` | used in `handleSignOut` |

Sign-out sequence: clear `THEME_STORAGE_KEY` from `localStorage`, clear `wizcamp-theme-synced` from `sessionStorage`, call `POST /lms/auth/signout` (errors swallowed), clear TanStack Query cache, redirect to `/login`.

Passes to `AccountMenu`: `user`, `theme`, `onThemeChange={applyTheme}`, `onSignOut={handleSignOut}`, `settingsHref="/admin/settings"`.

## AccountMenu (presentational)

### Props

| Prop | Type |
|---|---|
| `user` | `{ firstName, lastName, email, avatarUrl? }` |
| `theme` | `UserTheme` |
| `onThemeChange` | `(value: UserTheme) => void` |
| `onSignOut` | `() => Promise<void>` |
| `settingsHref` | `string` |

### Structure

**Trigger** — `<button>` with `hover:bg-muted`, `min-h-[44px]` on mobile / `sm:min-h-0`:
- `Avatar` (size-8) with `AvatarImage` + `AvatarFallback` (initials, `text-xs`)
- Name + email stack — `hidden sm:block`, truncated
- `ChevronDown` icon — `hidden sm:block`, `text-muted-foreground`, `size={14}`

**Menu** — `<DropdownMenuContent align="end" className="w-64">`:
1. `DropdownMenuLabel` — name + email (full, not truncated)
2. `DropdownMenuSeparator`
3. Theme label (`text-muted-foreground text-xs font-normal`)
4. Three theme items — Light (`Sun`), Dark (`Moon`), System (`Monitor`) — active item shows `Check` icon right-aligned
5. `DropdownMenuSeparator`
6. Settings item — `render={<Link href={settingsHref} />}` with `Settings` icon
7. `DropdownMenuSeparator`
8. Sign out item — `text-destructive focus:text-destructive` with `LogOut` icon

### Icon usage

All icons from `@/lib/icons` via `<Icon>` wrapper. Menu item icons: `className="mr-2 size-4 shrink-0"`.

| Location | Icon |
|---|---|
| Trigger chevron | `ChevronDown` size={14} |
| Theme — Light | `Sun` |
| Theme — Dark | `Moon` |
| Theme — System | `Monitor` |
| Active theme check | `Check` |
| Settings item | `Settings` |
| Sign out item | `LogOut` |

## Rules

- `AccountPanel` is the only consumer of `AccountMenu` in the admin shell — do not import `AccountMenu` directly from page components
- `AccountMenu` is a generic `components/ui/` component — it has no dependency on admin-specific hooks or types
- Sign-out must always clear both storage keys and the query cache before redirecting
- The trigger must always meet the 44×44px tap target on mobile (`min-h-[44px]` + `sm:min-h-0`)
