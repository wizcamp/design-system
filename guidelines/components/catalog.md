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
| Auth | [auth/index.md](auth/index.md) | `AuthLayout` → [auth-layout.md](auth/auth-layout.md); `LoginForm` → [login-form.md](auth/login-form.md); `JoinClient` → [join-client.md](auth/join-client.md) |
| Admin Shell | [admin-shell/index.md](admin-shell/index.md) | `AdminSidebar` → [admin-sidebar.md](admin-shell/admin-sidebar.md); `AdminPageHeader` → [admin-page-header.md](admin-shell/admin-page-header.md); `AdminPageContent` → [admin-page-content.md](admin-shell/admin-page-content.md) |
| Admin Settings | [admin-settings/index.md](admin-settings/index.md) | `SettingsSection` → [settings-section.md](admin-settings/settings-section.md); `SettingRow` → [setting-row.md](admin-settings/setting-row.md); `SecretField` → [secret-field.md](admin-settings/secret-field.md); `IdentitySection` → [identity-section.md](admin-settings/identity-section.md); `AICreditsSection` → [ai-credits-section.md](admin-settings/ai-credits-section.md); `AIPreferencesSection` → [ai-preferences-section.md](admin-settings/ai-preferences-section.md); `EditorPreferencesSection` → [editor-preferences-section.md](admin-settings/editor-preferences-section.md); `ThemeSection` → [theme-section.md](admin-settings/theme-section.md); `AboutSection` → [about-section.md](admin-settings/about-section.md) |
| Page Editor | [page-editor/index.md](page-editor/index.md) | `PageEditor` → [page-editor.md](page-editor/page-editor.md); `VideoConfigPanel` → [video-config-panel.md](page-editor/video-config-panel.md); `EditorStatusBar` → [editor-status-bar.md](page-editor/editor-status-bar.md); `AdminToolbar` → [admin-toolbar.md](page-editor/admin-toolbar.md); `ConflictResolutionModal` → [conflict-resolution-modal.md](page-editor/conflict-resolution-modal.md); `AIPanel` → [ai-panel.md](page-editor/ai-panel.md) |
| Progress | [progress/index.md](progress/index.md) | `ProgressBar`, `DripProgressBar` → [progress-bar.md](progress/progress-bar.md); `RadialProgress`, `DripProgressRing` → [radial-progress.md](progress/radial-progress.md); `LessonNavBar` → [lesson-nav-bar.md](progress/lesson-nav-bar.md) |
