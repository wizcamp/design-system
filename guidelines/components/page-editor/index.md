# Page Editor Subsystem

The full-screen MDX authoring environment for admin content editors. Breaks the standard admin shell layout — it occupies the full viewport height and does not use `AdminPageContent`.

## Hierarchy

```
PageEditPage                       ← route page — loading/error guard
  └── PageEditorShell              ← same file — full-viewport layout root
        ├── AdminPageHeader        ← breadcrumbs only
        ├── Identity Strip         ← back link · editable title · slug · status chip
        ├── Configuration Strip    ← layout toggle · video source type buttons
        ├── PageEditor             ← components/admin/PageEditor.tsx — fills remaining height
        │     ├── Editor Toolbar   ← format groups · clipboard · save · panel cycle
        │     ├── VideoConfigPanel ← components/admin/VideoConfigPanel.tsx — conditional
        │     ├── Monaco (left)    ← resizable — always dark, theme-invariant
        │     └── Right Panel      ← resizable — Preview | Reference | AI | off
        ├── EditorStatusBar        ← components/admin/EditorStatusBar.tsx
        └── AdminToolbar           ← components/admin/AdminToolbar.tsx — fixed floating pill
```

## Components

| Component | File | Role |
|---|---|---|
| `PageEditor` | [page-editor.md](page-editor.md) | Monaco container + toolbar + resizable panel layout |
| `VideoConfigPanel` | [video-config-panel.md](video-config-panel.md) | Conditional video source configuration strip |
| `EditorStatusBar` | [editor-status-bar.md](editor-status-bar.md) | Bottom bar — validate · save state · mode · cursor |
| `AdminToolbar` | [admin-toolbar.md](admin-toolbar.md) | Fixed floating pill — publish toggle · preview · save indicator |
| `ConflictResolutionModal` | [conflict-resolution-modal.md](conflict-resolution-modal.md) | Non-dismissable conflict dialog with diff view |
| `AIPanel` | [ai-panel.md](ai-panel.md) | Right-panel AI chat thread |

## Layout contract

`PageEditorShell` does not use `AdminPageContent`. The root is `flex h-dvh flex-col overflow-hidden` — the editor fills all remaining height below the header and two configuration strips via `min-h-0 flex-1 overflow-hidden`. `AdminToolbar` is fixed-positioned and floats above the layout.

## Right panel modes

| Mode | Content |
|---|---|
| Preview | Live MDX render — updates on save or on every keystroke in Live save mode |
| Reference | Keyboard shortcut table |
| AI | AI chat thread — requires API key configured in admin settings |
| Off | Panel hidden — Monaco takes full width |

## Rules

- `AdminPageHeader` is always the first child — breadcrumbs only, no CTAs
- `AdminToolbar` is always rendered at the shell level, never inside `PageEditor`
- `ConflictResolutionModal` is non-dismissable — it must be resolved before editing continues
- Do not add `AdminPageContent` — this subsystem owns its own full-viewport layout
