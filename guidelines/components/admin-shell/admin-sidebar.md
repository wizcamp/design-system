# AdminSidebar

The primary navigation shell for the admin portal. Renders a full-height sidebar with main nav, dev tools, external links, and a settings footer link.

## Hierarchy

```
AdminLayout
  └── SidebarProvider
        ├── AdminSidebar                 ← components/admin/AdminSidebar.tsx
        │     ├── SidebarHeader          ← shadcn/ui primitive
        │     ├── SidebarContent         ← shadcn/ui primitive
        │     │     ├── SidebarGroup (Main Navigation)
        │     │     ├── SidebarGroup (Dev Tools)   ← dev only
        │     │     └── SidebarGroup (External Tools)
        │     └── SidebarFooter          ← shadcn/ui primitive
        │           └── SidebarMenu      ← Settings link
        └── SidebarInset
```

## Contains

- `Sidebar` primitives (`SidebarHeader`, `SidebarContent`, `SidebarFooter`, `SidebarGroup`, `SidebarGroupLabel`, `SidebarGroupContent`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`) — shadcn/ui, no separate doc
- `Icon` — `components/ui/icon` wrapper, enforces `strokeWidth={1.75}` and `shrink-0`
- Nav item arrays sourced from `lib/admin-routes.ts` (`navItems`) and file-local constants (`devItems`, `externalItems`)

## Structure

1. **Header** — `border-b px-4 py-4`
   - Title — "Wizcamp Admin" — `text-base font-bold leading-tight`
   - Subtitle — "Camp Manager" — `text-xs text-muted-foreground mt-0.5`

2. **Main Navigation** — `SidebarGroup > SidebarGroupLabel + SidebarGroupContent > SidebarMenu`
   - Label — "Main Navigation"
   - Items sourced from `navItems` in `lib/admin-routes.ts`: Cohorts, Meetings, Enrollments, Students
   - Each: `<SidebarMenuButton>` with `isActive` + `<Icon>` (`size={16}`) + label
   - Active check: `pathname === href || pathname.startsWith(href + '/')`
   - `render={<Link href={href} />}` — uses base-ui render prop pattern

3. **Dev Tools** — `SidebarGroup` (rendered only when `process.env.NODE_ENV !== 'production'`)
   - Label — "Dev Tools"
   - Items (file-local `devItems`): Code Theme, Icon Catalog, Spacing
   - Active check: `pathname === href` (exact match only)

4. **External Tools** — `SidebarGroup > SidebarGroupLabel + SidebarGroupContent > SidebarMenu`
   - Label — "External Tools"
   - Items (file-local `externalItems`): Square Developer, Zoom, wizcamp.io, GitHub
   - Each: `render={<a href={href} target="_blank" rel="noreferrer" />}` — no `isActive`

5. **Footer** — `border-t px-3 py-3`
   - Settings nav item — `<SidebarMenuButton>` linking to `/admin/settings`
   - Active check: `pathname.startsWith('/admin/settings')`
   - Note: Settings link is a placeholder pending `AccountPanel` migration to the sidebar footer; remove when confirmed redundant

## Nav item arrays

`navItems` lives in `lib/admin-routes.ts` — shared with `AdminHeader` for breadcrumb derivation. `devItems` and `externalItems` are file-local constants at the top of `AdminSidebar.tsx`.

## Icon usage

All icons imported from `@/lib/icons` (the lucide-react shim). Rendered via `<Icon icon={X} size={16} />`.

| Location | Icon | Size |
|---|---|---|
| Cohorts nav | `Calendar` | `size={16}` |
| Meetings nav | `CalendarDays` | `size={16}` |
| Enrollments nav | `Users` | `size={16}` |
| Students nav | `School` | `size={16}` |
| Dev — Code Theme | `Palette` | `size={16}` |
| Dev — Icon Catalog | `SwatchBook` | `size={16}` |
| Dev — Spacing | `Ruler` | `size={16}` |
| External — Square | `ExternalLink` | `size={16}` |
| External — Zoom | `Video` | `size={16}` |
| External — wizcamp.io | `Globe` | `size={16}` |
| External — GitHub | `Github` | `size={16}` |
| Settings footer | `Settings` | `size={16}` |

## Props

`AdminSidebar` takes no props. All data is sourced from `usePathname()` and the file-local item arrays.

## What was removed

- `CohortContextGroup` — file-private sub-component for cohort deep-view context. Removed; `ScopeCard` is the planned replacement (not yet built — see `scopecard-accountpanel-plan.md`).
- `UserNavFooter` — file-private sub-component for avatar, theme toggle, and sign-out. Removed; `AccountPanel` now lives in `AdminHeader` instead of the sidebar footer.
- `useAuth()`, `useAdminCohortsQuery()`, `useUpdateAdminSettingsMutation()` — all hooks removed from this component. `AdminSidebar` now only calls `usePathname()`.

## Rules

- Mount once in the admin layout — never inside a page component
- Nav items are defined in `navItems` (from `lib/admin-routes.ts`), `devItems`, and `externalItems` — do not add items inline in JSX
- All nav icons use `size={16}` via `<Icon>` — do not use raw icon JSX
- Dev Tools section is gated by `process.env.NODE_ENV !== 'production'` — do not remove the guard
- Do not add a border or shadow to the sidebar itself — surface color provides the separation
- `AdminSidebar` calls no hooks other than `usePathname()` — all data is static or derived from the pathname
