# PageEditor

The Monaco editor container. Owns the toolbar, resizable panel layout, and the status bar. The Monaco pane is always dark regardless of page theme — it does not respond to the theme toggle.

## Contains

- `MonacoEditor` (`@monaco-editor/react`) — dynamically imported, SSR disabled
- `VideoConfigPanel` — conditional, rendered between toolbar and editor
- `EditorPreview`, `KeyboardShortcutReference`, `AIPanel` — right panel content, mode-driven
- `EditorStatusBar` — bottom bar
- `MediaLibrary` — dialog, opened from the toolbar Insert Media button

## Structure

`<div className="flex h-full min-w-0 flex-col overflow-hidden">`

1. **Editor toolbar** — `flex items-center gap-1 border-b px-3 py-1.5` — see toolbar section below
2. **`VideoConfigPanel`** — conditional on video layout
3. **`ResizablePanelGroup orientation="horizontal"`** — `flex min-h-0 flex-1 overflow-hidden`
   - **Left panel** (`defaultSize={50}`, `minSize={30}`) — Monaco in a `relative h-full overflow-hidden` container
   - **Right panel** (`defaultSize={50}`, `minSize={30}`) — hidden entirely when panel mode is Off
     - Panel header — `flex shrink-0 items-center justify-between border-b px-4 py-2`
       - Label — `text-muted-foreground text-xs font-medium uppercase tracking-wider`
       - Pause/Resume button — Preview mode only — `variant="ghost" size="sm"` with `gap-1.5`
     - Panel body — `min-h-0 flex-1 overflow-y-auto`
4. **`EditorStatusBar`** — below the resizable group

## Editor toolbar

Groups separated by `<div className="mx-1 h-4 w-px bg-border" />`. All action buttons are `variant="ghost" size="icon-sm"` wrapped in `<Tooltip>`.

| Group | Buttons |
|---|---|
| 1 — Inline format | Bold · Italic · Strikethrough · Inline Code |
| 2 — Link | Link |
| 3 — Headings | H1 · H2 · H3 |
| 4 — Block | Blockquote · Bullet List |
| 5 — MDX snippets | Dynamic — from snippet registry |
| 6 — Media | Insert Media |
| 7 — Clipboard | Copy · Paste · Download |
| 8 — Document | Format |

After `<div className="ml-auto" />` on the right:

- **Save button** — plain `<button>`, not `<Button>` — `flex items-center justify-center rounded px-2 py-1`
  - Dirty: `text-amber-600 hover:bg-amber-500/10 dark:text-amber-400`
  - Clean: `text-muted-foreground/40 hover:text-muted-foreground hover:bg-muted`
- **Divider**
- **Panel cycle button** — `variant="ghost" size="sm"` — icon + current panel mode label

## Preview panel states

The preview panel header shows a Pause/Resume button only in Preview mode. When paused, the preview is frozen at the snapshot taken at pause time and the `RefreshCw` icon turns `text-amber-500`.

## Icon usage

All icons from `lucide-react` (migration pending).

| Location | Icon | Size |
|---|---|---|
| Bold | `Bold` | `size-3.5` |
| Italic | `Italic` | `size-3.5` |
| Strikethrough | `Strikethrough` | `size-3.5` |
| Inline Code | `Code` | `size-3.5` |
| Link | `Link` | `size-3.5` |
| Heading 1 | `Heading1` | `size-3.5` |
| Heading 2 | `Heading2` | `size-3.5` |
| Heading 3 | `Heading3` | `size-3.5` |
| Blockquote | `TextQuote` | `size-3.5` |
| Bullet List | `List` | `size-3.5` |
| Insert Media | `ImagePlus` | `size-3.5` |
| Copy (idle) | `Copy` | `size-3.5` |
| Copy (success, 2s) | `Check` | `size-3.5` |
| Paste | `ClipboardPaste` | `size-3.5` |
| Download | `Download` | `size-3.5` |
| Format | `WandSparkles` | `size-3.5` |
| Save | `Save` | `size-3.5` |
| Panel cycle | `PanelRight` | `size-3.5` |
| Pause/Resume preview | `RefreshCw` | `size-3.5` |

## Rules

- The Monaco pane is always dark — `theme="wizcamp-dark"` must not be changed or made theme-responsive
- All toolbar action buttons use `size="icon-sm"` — not `size="icon"` or `size="sm"`
- The save button is a plain `<button>` with custom dirty/clean colour logic — do not replace with `<Button>`
- Copy button shows `Check` for 2 seconds after success — do not change this duration
- The right panel is absent from the DOM entirely when mode is Off — not hidden with CSS
- `MediaLibrary` is opened from the Insert Media toolbar button — it is not a separate page
