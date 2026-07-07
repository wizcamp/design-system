# Component Catalog

> Add an entry here whenever a new component guidelines file is created.

Each entry links to its guidelines file. Read the guidelines file before using any component or subsystem.

## Standalone components

| Component | File | Notes |
|---|---|---|
| CodeBlock | [code-block.md](code-block.md) | Syntax-highlighted code and terminal output — always dark, theme-invariant |
| ThemeToggle | [theme-toggle.md](theme-toggle.md) | Light/dark mode toggle — accepts a settings mutation prop |

## Subsystems

Tightly coupled component families. Read the subsystem `index.md` first, then the file for the specific component.

| Subsystem | Index | Components |
|---|---|---|
| Admin Shell | [admin-shell/index.md](admin-shell/index.md) | `AdminSidebar` → [admin-sidebar.md](admin-shell/admin-sidebar.md); `AdminPageHeader` → [admin-page-header.md](admin-shell/admin-page-header.md); `AdminPageContent` → [admin-page-content.md](admin-shell/admin-page-content.md) |
| Progress | [progress/index.md](progress/index.md) | `ProgressBar`, `DripProgressBar` → [progress-bar.md](progress/progress-bar.md); `RadialProgress`, `DripProgressRing` → [radial-progress.md](progress/radial-progress.md); `LessonNavBar` → [lesson-nav-bar.md](progress/lesson-nav-bar.md) |
