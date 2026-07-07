# Admin Shell Subsystem

The structural shell that wraps every admin page. Understanding the full hierarchy is required before building or modifying any admin page.

## Hierarchy

```
AdminLayout                          ← app/(authenticated)/(admin)/layout.tsx
  └── SidebarProvider                ← shadcn/ui — manages expand/collapse state + CSS vars
        ├── AdminSidebar             ← components/admin/AdminSidebar.tsx
        │     └── Sidebar primitives ← shadcn/ui (SidebarHeader, SidebarContent, etc.)
        └── SidebarInset             ← shadcn/ui — the scrollable main content <main>
              ├── AdminPageHeader    ← components/admin/AdminPageHeader.tsx — on every page
              └── AdminPageContent   ← components/admin/AdminPageContent.tsx — on every page
                    └── {page content}
```

## Components

| Component | File | Role |
|---|---|---|
| `AdminSidebar` | [admin-sidebar.md](admin-sidebar.md) | Full-height nav sidebar — mounted once in `AdminLayout` |
| `AdminPageHeader` | [admin-page-header.md](admin-page-header.md) | `h-16` top bar with `SidebarTrigger` + breadcrumbs — first child of every page |
| `AdminPageContent` | [admin-page-content.md](admin-page-content.md) | Content area wrapper — canonical `p-4 sm:p-6` padding — second child of every page |

## Shell contract

`AdminLayout` is a Next.js route layout — it is not imported by page components. It mounts automatically for all routes under `app/(authenticated)/(admin)/`. Every admin page receives the shell for free and must only render `AdminPageHeader` + `AdminPageContent` as its top-level children.

`SidebarProvider` (shadcn/ui) provides:
- Expand/collapse state persisted to a cookie (`sidebar_state`)
- `--sidebar-width` and `--sidebar-width-icon` CSS custom properties consumed by `Sidebar` and `SidebarInset`
- `useSidebar()` hook — consumed by `SidebarTrigger` inside `AdminPageHeader`
- Keyboard shortcut `⌘B` / `Ctrl+B` to toggle the sidebar

`SidebarInset` (shadcn/ui) is a `<div>` that holds all page content. It carries `bg-background` and `overflow-hidden` — do not add another background or overflow wrapper inside it. `AdminPageContent` is the `<main>` element — the only `<main>` in the admin layout tree.

## Rules

- Every admin page must render `<AdminPageHeader>` as its first child and `<AdminPageContent>` as its second — no exceptions
- Never render page content directly inside `SidebarInset` without `AdminPageContent`
- Never mount `AdminSidebar` inside a page component — it belongs in `AdminLayout` only
- `SidebarProvider`, `SidebarInset`, and all `Sidebar*` primitives are shadcn/ui — do not document or modify them directly
