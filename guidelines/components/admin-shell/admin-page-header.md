# AdminHeader

The top bar rendered as the first child of `SidebarInset` in `AdminLayout`. Contains the `SidebarTrigger`, breadcrumb navigation, and `AccountPanel`. Height is always `h-16` with a `border-b`.

Renamed from `AdminPageHeader`. No longer accepts props — breadcrumbs are derived internally.

## Breadcrumb strategy

Breadcrumbs are assembled from two sources:

1. **Static prefix** — derived from the current pathname by matching against `ADMIN_CRUMB` entries in `lib/admin-routes.ts`. The first `ADMIN_CRUMB` entry whose `href` matches the start of the pathname becomes the leading crumb.
2. **Dynamic tail** — provided by page client components via `useSetBreadcrumbs()` from `BreadcrumbProvider`. Pages push their dynamic crumbs (e.g. cohort name, student name) into context on mount and clear them on unmount.

`AdminHeader` reads `useBreadcrumbContext()` for the dynamic tail and calls `deriveStaticPrefix(pathname)` (file-private) for the static prefix. The two are concatenated: `[...staticPrefix, ...dynamicTail]`.

## Structure

`<header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">`

1. **SidebarTrigger** — `className="-ml-1"` — always present

2. **Desktop breadcrumb** — `hidden lg:flex min-w-0 flex-1 items-center`
   - shadcn/ui `<Breadcrumb>` with `<BreadcrumbList className="min-w-0">`
   - Each crumb: `<BreadcrumbItem>` containing `<BreadcrumbLink render={<Link href={...} />}>` (if `href`) or `<BreadcrumbPage>` (last item)
   - `<BreadcrumbSeparator />` between each pair

3. **Mobile layout** — `flex lg:hidden min-w-0 flex-1 items-center gap-2`
   - Back chevron (conditional — only when `breadcrumbs.length > 1` and `parent.href` exists):
     `<Link>` — `hover:bg-muted flex min-h-[44px] min-w-[44px] shrink-0 items-center justify-center rounded-md`
     — `<Icon icon={ChevronLeft} size={20} />`
   - Current page label — `flex-1 truncate text-sm font-medium`
   - Note: the mobile depth popover from the original design was not implemented — mobile shows back chevron + current label only

4. **AccountPanel** — `<AccountPanel />` — always visible, right-aligned

## Props

None. `AdminHeader` derives all data internally from `usePathname()` and `useBreadcrumbContext()`.

## How pages set breadcrumbs

Page client components call `useSetBreadcrumbs(tail: Crumb[])` from `breadcrumb-provider.tsx`. Pass only the dynamic tail — the static section prefix is added automatically.

```tsx
// Example: cohort detail page
useSetBreadcrumbs([{ label: cohort.cohortName }]);

// Example: page editor (nested)
useSetBreadcrumbs([
  { label: cohort.cohortName, href: `/admin/cohorts/${cohortSlug}` },
  { label: page.title },
]);
```

The last crumb must never have an `href` — it is the current page.

## Rules

- Always the first child of `SidebarInset` — rendered in `AdminLayout`, not in page components
- Never nest inside page content
- Do not add CTAs, buttons, or filters to `AdminHeader` — those belong on the page
- The last breadcrumb must never have an `href`
- Pages set their dynamic breadcrumb tail via `useSetBreadcrumbs()` — never pass breadcrumbs as props to `AdminHeader`
