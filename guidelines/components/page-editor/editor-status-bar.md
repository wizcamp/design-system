# EditorStatusBar

The bottom status bar of the page editor. A single `text-xs` row showing validate state, save state, save mode, panel mode, word count, and cursor position.

## Structure

`<div className="bg-muted/40 flex shrink-0 items-center gap-3 border-t px-4 py-1 text-xs">`

Left to right:

1. **Validate toggle** — `<button>` — icon + label — clicking toggles syntax validation on/off
   - Validating: `<Loader2 className="size-3 animate-spin" />`
   - On + valid: `<CheckCheck className="size-3 text-emerald-500" />`
   - On + invalid: `<CheckCheck className="size-3 text-destructive" />` + truncated error `max-w-48`
   - Off: `<EyeOff className="size-3" />` — full row at `text-muted-foreground/40`
2. **·** separator — `text-muted-foreground/30`
3. **Save state** — one of:
   - `Conflict` — `text-destructive font-medium`
   - `Save failed` — `text-destructive font-medium` — full error in `title`
   - `Saving…` — `text-muted-foreground` + `<Loader2 className="size-3 animate-spin" />`
   - `Unsaved` — `text-amber-600 dark:text-amber-400` + `size-1.5 rounded-full bg-amber-500` dot
   - `Saved` — `text-muted-foreground`
4. **·** separator
5. **Save mode** — `<button>` — `text-muted-foreground hover:text-foreground` — clicking cycles through Live · Auto · Manual
6. **·** separator
7. **Panel mode** — `<span className="text-muted-foreground">` — current right panel label
8. **`flex-1` spacer**
9. **Word count** — `text-muted-foreground/60` — `{n} word(s)`
10. **·** separator
11. **Cursor position** — `text-muted-foreground/60` — `Ln {n}, Col {n}`

## Rules

- Save state priority (highest first): Conflict → Save failed → Saving → Unsaved → Saved
- Validate toggle opacity drops to `/40` when off — it is never hidden entirely
- Word count and cursor position are always right-aligned via the `flex-1` spacer
