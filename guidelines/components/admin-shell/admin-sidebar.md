# AdminSidebar

The primary navigation shell for the admin portal. Renders a full-height sidebar with contextual cohort context, main nav, dev tools, external links, and a user identity footer.

## Hierarchy

```
AdminLayout                          ← app/(authenticated)/(admin)/layout.tsx
  └── SidebarProvider                ← shadcn/ui — manages expand/collapse state + CSS vars
        ├── AdminSidebar             ← components/admin/AdminSidebar.tsx
        │     ├── SidebarHeader      ← shadcn/ui primitive
        │     ├── SidebarContent     ← shadcn/ui primitive
        │     │     ├── CohortContextGroup   ← file-private — conditional, cohort deep-view only
        │     │     ├── SidebarGroup (Main Navigation)
        │     │     ├── SidebarGroup (Dev Tools)
        │     │     └── SidebarGroup (External Tools)
        │     └── SidebarFooter      ← shadcn/ui primitive
        │           ├── SidebarMenu  ← Settings link
        │           └── UserNavFooter ← file-private — avatar, theme toggle, sign-out
        └── SidebarInset             ← shadcn/ui — the scrollable main content <main>
              ├── AdminPageHeader    ← components/admin/AdminPageHeader.tsx — on every page
              └── AdminPageContent   ← components/admin/AdminPageContent.tsx — on every page
                    └── {page content}
```

## Contains

- `Sidebar` primitives (`SidebarHeader`, `SidebarContent`, `SidebarFooter`, `SidebarGroup`, `SidebarGroupLabel`, `SidebarGroupContent`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`) — shadcn/ui, no separate doc
- `Avatar` — shadcn/ui primitive, no separate doc
- `ThemeToggle` — custom component, see `components/theme-toggle.md`
- `CohortContextGroup` — file-private sub-component, see below
- `UserNavFooter` — file-private sub-component, see below

## Structure

1. **Header** — `border-b px-4 py-4`
   - Title — "Wizcamp Admin" — `text-base font-bold leading-tight`
   - Subtitle — "Camp Manager" — `text-xs text-muted-foreground mt-0.5`

2. **Contextual nav** — `<CohortContextGroup>` (conditional — rendered only when inside a cohort deep-view)
   - Wrapped in `SidebarGroup > SidebarGroupLabel + SidebarGroupContent`
   - Label — "Current Context"
   - Cohort link — `flex items-center gap-3 rounded-lg px-3 py-2.5 bg-primary/10 text-primary`
     - Icon — `<Calendar />` — `size-4 shrink-0`
     - Camp name — `text-xs text-muted-foreground`
     - Cohort name — `text-sm font-medium truncate`

3. **Main Navigation** — `SidebarGroup > SidebarGroupLabel + SidebarGroupContent > SidebarMenu`
   - Label — "Main Navigation"
   - Items: Cohorts, Meetings, Enrollments, Students
   - Each: `<SidebarMenuButton>` with `isActive` + icon (`size-4`) + label

4. **Dev Tools** — `SidebarGroup > SidebarGroupLabel + SidebarGroupContent > SidebarMenu` (remove before production)
   - Label — "Dev Tools"
   - Items: Code Theme, Icon Comparison

5. **External Tools** — `SidebarGroup > SidebarGroupLabel + SidebarGroupContent > SidebarMenu`
   - Label — "External Tools"
   - Items: Square Developer, Zoom, wizcamp.io, GitHub
   - Each opens in a new tab via `<a target="_blank" rel="noreferrer">`

6. **Footer** — `border-t px-3 py-3`
   - Settings nav item — `<SidebarMenuButton>` linking to `/admin/settings`
   - `<UserNavFooter>` — see below

## Local sub-components

These are file-private (unexported). They receive all data as props — no hooks inside.

### `CohortContextGroup`

| Prop | Type | Description |
|---|---|---|
| `cohortSlug` | `string` | Slug parsed from the current pathname |
| `currentCohort` | `Cohort \| undefined` | Matched cohort from the query result |

Renders a `SidebarGroup` with a single cohort context link. Rendered conditionally by `AdminSidebar` when `cohortSlug` is non-null.

### `UserNavFooter`

| Prop | Type | Description |
|---|---|---|
| `user` | `ReturnType<typeof useAuth>['user']` | Authenticated user object |
| `signOut` | `ReturnType<typeof useAuth>['signOut']` | Sign-out handler |
| `updateSettings` | `UseMutationResult` | Passed through to `ThemeToggle` |

Renders the avatar, name, email, theme toggle, and sign-out button row in the sidebar footer.

## Icon usage

**Current (lucide-react — migration pending):**

| Location | Import | Size |
|---|---|---|
| Cohorts nav | `Calendar` | `size-4` |
| Meetings nav | `CalendarDays` | `size-4` |
| Enrollments nav | `Users` | `size-4` |
| Students nav | `GraduationCap` | `size-4` |
| Dev — Code Theme | `Palette` | `size-4` |
| Dev — Icon Comparison | `SwatchBook` | `size-4` |
| External — Square | `ExternalLink` | `size-4` |
| External — Zoom | `Video` | `size-4` |
| External — wizcamp.io | `Globe` | `size-4` |
| External — GitHub | `Github` | `size-4` |
| Settings footer | `Settings` | `size-4` |
| Sign-out button | `LogOut` | `size-4` |

**Target (@tabler/icons-react):**

| Location | Import | Size |
|---|---|---|
| Cohorts nav | `IconCalendar` | `size-4` |
| Meetings nav | `IconCalendar` | `size-4` |
| Enrollments nav | `IconUsers` | `size-4` |
| Students nav | `IconSchool` | `size-4` |
| Dev — Code Theme | `IconPalette` | `size-4` |
| Dev — Icon Comparison | `IconSwatch` | `size-4` |
| External — Square | `IconExternalLink` | `size-4` |
| External — Zoom | `IconVideo` | `size-4` |
| External — wizcamp.io | `IconGlobe` | `size-4` |
| External — GitHub | `IconBrandGithub` | `size-4` |
| Settings footer | `IconSettings` | `size-4` |
| Sign-out button | `IconLogout` | `size-4` |

## Props

`AdminSidebar` takes no props. All data is sourced internally via hooks and passed down to local sub-components.

| Hook | Provides |
|---|---|
| `useAuth()` | `user`, `signOut` |
| `useAdminCohortsQuery()` | cohort list for contextual nav |
| `useUpdateAdminSettingsMutation()` | passed to `UserNavFooter` → `ThemeToggle` |

## Variants

None. Single variant only.

## Rules

- Mount once in the admin layout — never inside a page component
- Nav items are defined in `navItems`, `devItems`, and `externalItems` arrays at the top of the file — do not add items inline in JSX
- All nav icons use `size-4` — do not change this
- The user footer always includes `ThemeToggle` and sign-out — do not remove either
- Dev Tools section must be removed before production
- Do not add a border or shadow to the sidebar itself — surface color provides the separation
- `CohortContextGroup` and `UserNavFooter` are file-private — do not export them or move them to separate files
- All hooks are called in `AdminSidebar` only — local sub-components receive data as props
