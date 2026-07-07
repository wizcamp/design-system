# AdminPageHeader

The top bar rendered as the first child of every admin page. Contains the `SidebarTrigger` and breadcrumb navigation. Height is always `h-16` with a `border-b`.

Consumes `useSidebar()` from `SidebarProvider` via `SidebarTrigger` — must always be rendered inside the admin shell.

## Structure

`<header className="flex h-16 items-center gap-2 border-b px-4">`

1. **SidebarTrigger** — `className="-ml-1"` — toggles the sidebar; always present

2. **Desktop breadcrumb** — `hidden lg:flex min-w-0 flex-1 items-center`
   - shadcn/ui `<Breadcrumb>` with `<BreadcrumbList>` — `className="min-w-0"`
   - Each crumb: `<BreadcrumbItem>` containing either `<BreadcrumbLink>` (if `href`) or `<BreadcrumbPage>` (last item)
   - `<BreadcrumbSeparator />` between each pair

3. **Mobile layout** — `flex lg:hidden min-w-0 flex-1 items-center gap-2`
   - Back chevron (conditional — only when `depth > 1` and `parent.href` exists):
     `<Link>` — `hover:bg-muted flex min-h-[44px] min-w-[44px] shrink-0 items-center justify-center rounded-md`
     — `<ChevronLeft className="h-5 w-5" />`
   - Current page label — `flex-1 truncate text-sm font-medium`
   - Depth popover (conditional — only when `depth > 1`):
     `<PopoverTrigger>` — `hover:bg-muted flex min-h-[44px] min-w-[44px] shrink-0 items-center justify-center gap-1 rounded-md text-sm`
     — `<ChevronDown className="h-4 w-4 transition-transform" />` (rotates 180° when open) + depth count `text-xs font-medium`
     - `<PopoverContent align="end" className="w-64 p-2">` — lists all crumbs with `↳` indent for nested items; linked crumbs close the popover on click

## Props

| Prop | Type | Notes |
|---|---|---|
| `breadcrumbs` | `{ label: string; href?: string }[]` | Ordered list of crumbs. Last item is always the current page (no `href`). |

## Rules

- Always the first child of the page — before `AdminPageContent`
- Never nest inside `AdminPageContent`
- The last breadcrumb must never have an `href` — it is the current page
- Do not add CTAs, buttons, or filters to `AdminPageHeader` — those belong inside `AdminPageContent`
