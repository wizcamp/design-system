# Admin Shell Subsystem

The structural shell that wraps every admin page. Understanding the full hierarchy is required before building or modifying any admin page.

## Hierarchy

```
AdminLayout                          ← app/(authenticated)/(admin)/layout.tsx
  └── AdminUserProvider              ← components/admin/admin-user-provider.tsx — injects AuthUser, handles 401
        └── BreadcrumbProvider       ← components/admin/breadcrumb-provider.tsx — dynamic breadcrumb tail
              └── SidebarProvider    ← shadcn/ui — manages expand/collapse state + CSS vars
                    ├── AdminSidebar ← components/admin/AdminSidebar.tsx
                    └── SidebarInset ← shadcn/ui — flex column, h-dvh, overflow-hidden
                          ├── AdminHeader   ← components/admin/AdminHeader.tsx — sticky top bar
                          └── <main>        ← inline in layout — min-h-0 flex-1 overflow-auto
                                └── ConfirmProvider  ← components/providers/confirm-provider.tsx
                                      └── {page children}
```

## Components

| Component | File | Role |
|---|---|---|
| `AdminUserProvider` | [admin-user-provider.md](../providers/admin-user-provider.md) | RSC-to-client user bridge; 401 handler; theme sync |
| `BreadcrumbProvider` | [breadcrumb-provider.md](../providers/breadcrumb-provider.md) | Dynamic breadcrumb tail context |
| `AdminSidebar` | [admin-sidebar.md](admin-sidebar.md) | Full-height nav sidebar — mounted once in `AdminLayout` |
| `AdminHeader` | [admin-header.md](admin-header.md) | `h-16` top bar with `SidebarTrigger`, breadcrumbs, and `AccountPanel` |
| `AccountPanel` | [account-panel.md](account-panel.md) | Thin adapter in the header — delegates to `AccountMenu` |

## Shell contract

`AdminLayout` is a Next.js route layout — it is not imported by page components. It mounts automatically for all routes under `app/(authenticated)/(admin)/`. Every admin page receives the shell for free.

There is no `AdminPageContent` wrapper component. Pages render their content directly as children of the layout's `<main>`. Page-level padding (`p-4 sm:p-6`) and layout classes (`space-y-6`, `max-w-2xl`, etc.) are applied directly on the page's outermost element.

`SidebarProvider` (shadcn/ui) provides:
- Expand/collapse state persisted to a cookie (`sidebar_state`)
- `--sidebar-width` and `--sidebar-width-icon` CSS custom properties consumed by `Sidebar` and `SidebarInset`
- `useSidebar()` hook — consumed by `SidebarTrigger` inside `AdminHeader`
- Keyboard shortcut `⌘B` / `Ctrl+B` to toggle the sidebar

`SidebarInset` (shadcn/ui) is a flex column with `h-dvh overflow-hidden`. The `<main>` inside it carries `min-h-0 flex-1 overflow-auto` — this is the scrollable content region. Do not add another overflow wrapper inside it.

## Rules

- Never mount `AdminSidebar` inside a page component — it belongs in `AdminLayout` only
- Page content renders directly as children of `<main>` — there is no `AdminPageContent` wrapper
- `SidebarProvider`, `SidebarInset`, and all `Sidebar*` primitives are shadcn/ui — do not document or modify them directly
- `AdminUserProvider` and `BreadcrumbProvider` are layout-level providers — never mount them inside a page component
