# AdminToolbar

A fixed floating pill rendered at the page shell level, always above the editor. Provides publish/draft toggle, student preview navigation, and save state indicators.

## Structure

`<div className="bg-background/95 supports-[backdrop-filter]:bg-background/80 fixed z-50 flex items-center gap-2 rounded-full border px-4 py-2 shadow-lg backdrop-blur {position}">`

## Positioning

| `side` | Classes | Used by |
|---|---|---|
| `'bottom-center'` | `bottom-5 left-1/2 -translate-x-1/2` | Page editor |
| `'bottom-right'` | `bottom-6 right-6` | Other admin pages |

## Contents (left to right)

1. **Student view button** (conditional — only when `previewHref` is set)
   - `variant="ghost" size="sm"` — `gap-1.5`
   - Colour: `text-amber-600 hover:bg-amber-500/10 hover:text-amber-700 dark:text-amber-400`
   - Icon: `<Eye className="size-3.5" />` — replaced by `<Loader2 className="size-3.5 animate-spin" />` while saving before navigate
   - Label: `"Student view"` — `hidden sm:inline text-xs` — replaced by `"Saving…"` while flushing
2. **Open in new tab button** (conditional — only when `previewHref` is set)
   - `variant="ghost" size="sm"` — same amber colour
   - Icon: `<ExternalLink className="size-3.5" />`
3. **Status toggle button** — `variant="ghost" size="sm" className="text-xs"`
   - Label: `"Mark as Published"` (when draft) or `"Mark as Draft"` (when published)
4. **Saving spinner** (conditional) — `<Loader2 className="text-muted-foreground size-3.5 animate-spin" />`
5. **Unsaved dot** (conditional — dirty and not saving) — `size-2 shrink-0 rounded-full bg-amber-500`
6. **Conflict label** (conditional) — `text-destructive text-xs font-medium` — `"Conflict"`
7. **Save error label** (conditional) — `text-destructive text-xs font-medium` — `"Save failed"` — full error in `title`

## Icon usage

| Location | Icon | Size |
|---|---|---|
| Student view (idle) | `Eye` | `size-3.5` |
| Student view (saving) | `Loader2` | `size-3.5` |
| Open in new tab | `ExternalLink` | `size-3.5` |
| Saving spinner | `Loader2` | `size-3.5` |

## Rules

- Always rendered at the shell level — never inside `PageEditor`
- Student view and new tab buttons are absent from the DOM when `previewHref` is not set — not disabled
- The unsaved dot and saving spinner are mutually exclusive — dot only shows when not saving
- `side="bottom-center"` is the correct value for the page editor
