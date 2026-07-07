# AdminSidebar

The primary navigation shell for the admin portal. Renders a full-height sidebar with contextual cohort context, main nav, dev tools, external links, and a user identity footer.

## Contains

- `Sidebar` primitives (`SidebarHeader`, `SidebarContent`, `SidebarFooter`, `SidebarMenu`, `SidebarMenuItem`, `SidebarMenuButton`, `SidebarSeparator`) — shadcn/ui, no separate doc
- `Avatar` — shadcn/ui primitive, no separate doc
- `ThemeToggle` — custom component, see `components/theme-toggle.md` when available

## Structure

1. **Header** — `border-b px-4 py-4`
   - Title — "Wizcamp Admin" — `text-base font-bold leading-tight text-foreground`
   - Subtitle — "Camp Manager" — `text-xs text-muted-foreground mt-0.5`

2. **Contextual nav** (conditional — shown only inside a cohort deep-view)
   - Section label — "Current Context" — `text-xs font-medium text-muted-foreground mb-2 px-3`
   - Cohort link — `flex items-center gap-3 rounded-lg px-3 py-2.5 bg-primary/10 text-primary`
     - Icon — `<Calendar size={16} />` — `size-4 shrink-0`
     - Camp name — `text-xs text-muted-foreground`
     - Cohort name — `text-sm font-medium truncate`
   - `<SidebarSeparator />` below

3. **Main Navigation** — section label + `<SidebarMenu>`
   - Items: Cohorts, Meetings, Enrollments, Students
   - Each: `<SidebarMenuButton>` with `isActive` + icon (`size-4`) + label
   - Active state handled by shadcn/ui `SidebarMenuButton`

4. **Dev Tools** — section label + `<SidebarMenu>` (remove before production)
   - Items: Code Theme, Icon Comparison

5. **External Tools** — section label + `<SidebarMenu>`
   - Items: Square Developer, Zoom, wizcamp.io, GitHub
   - Each opens in a new tab via `<a target="_blank" rel="noreferrer">`

6. **Footer** — `border-t px-3 py-3`
   - Settings nav item — `<SidebarMenuButton>` linking to `/admin/settings`
   - User row — `flex items-center gap-3 rounded-lg px-2 py-2`
     - `<Avatar>` — `size-8` with image + initials fallback (`text-xs`)
     - Name — `text-sm font-medium leading-tight truncate`
     - Email — `text-xs text-muted-foreground truncate`
     - `<ThemeToggle>` — receives `useUpdateAdminSettingsMutation()`
     - Sign-out button — `<Button size="icon" variant="ghost">` — `size-8 text-muted-foreground hover:text-foreground`

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

`AdminSidebar` takes no props. All data is sourced internally.

| Hook | Provides |
|---|---|
| `useAuth()` | `user`, `signOut` |
| `useAdminCohortsQuery()` | cohort list for contextual nav |
| `useUpdateAdminSettingsMutation()` | passed to `ThemeToggle` |

## Variants

None. Single variant only.

## Rules

- Mount once in the admin layout — never inside a page component
- Nav items are defined in `navItems`, `devItems`, and `externalItems` arrays at the top of the file — do not add items inline in JSX
- All nav icons use `size-4` — do not change this
- The user footer always includes `ThemeToggle` and sign-out — do not remove either
- Dev Tools section must be removed before production
- Do not add a border or shadow to the sidebar itself — surface color provides the separation
