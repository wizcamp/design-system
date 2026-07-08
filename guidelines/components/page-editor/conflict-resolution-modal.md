# ConflictResolutionModal

A non-dismissable dialog that appears when a save returns a 409 conflict. The editor is blocked until the user resolves the conflict. Has two views: a choice view and a full-screen diff view.

## Contains

- `Dialog` primitives — shadcn/ui, no separate doc
- `DiffEditor` (`@monaco-editor/react`) — dynamically imported, SSR disabled — diff view only

## Choice view

Standard dialog dimensions. `showCloseButton={false}`.

- **Header** — title: `"Edit Conflict"` · description: explains the conflict
- **Footer** — three buttons:
  - `"See Difference"` — `variant="outline"` — opens diff view
  - `"Use Server Version"` — `variant="outline"` — first click shows a confirmation step
  - `"Keep My Version"` — `variant="default"`

**Discard confirmation step** — replaces the footer when "Use Server Version" is clicked once:

- Warning block — `bg-destructive/10 text-destructive flex items-start gap-3 rounded-lg p-3`
  - `<AlertTriangle className="mt-0.5 size-4 shrink-0" />`
  - `"Are you sure? This cannot be undone."`
- Footer: `"Go back"` (outline) + `"Yes, discard my changes"` (destructive)

## Diff view

Full-screen — `DialogContent` overrides to `top-0 left-0 h-svh max-h-svh w-full max-w-none rounded-none p-0`.

- **Header** — `shrink-0 border-b px-6 py-4` — title: `"Comparing Versions"` · description: `"Left: server version · Right: your version"`
- **DiffEditor** — `min-h-0 flex-1` — `readOnly: true`, `renderSideBySide: true`, `theme="wizcamp-dark"`, minimap disabled, word wrap on
- **Footer** — `shrink-0 border-t px-6 py-4`
  - Default: `"Back"` (outline) + `"Use Server Version"` (outline) + `"Keep My Version"` (default)
  - After clicking "Use Server Version": `"Cancel"` (outline) + `"Yes, discard my changes"` (destructive)

## Rules

- The modal is non-dismissable — clicking outside or pressing Escape does nothing
- `showCloseButton={false}` must be set — the user must make an explicit choice
- The DiffEditor uses `theme="wizcamp-dark"` — always dark, same as the main Monaco pane
- "Use Server Version" always requires a two-click confirmation — never fires on first click
