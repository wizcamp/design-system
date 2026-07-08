# VideoConfigPanel

A configuration strip rendered between the editor toolbar and the Monaco pane. Only visible when the page layout is set to Video. Returns nothing for Doc layout pages.

## Structure

`<div className="shrink-0 space-y-3 border-b px-4 py-3">`

Content is conditional on the active video source type:

| Source type | Controls |
|---|---|
| External URL | URL input (`max-w-sm`) + Duration input |
| Hosted — no video | "Select or Upload Video" outline button |
| Hosted — video selected | Poster card + Change button + remove button |
| Loom | Loom URL input (`max-w-sm`) + inline validation error + Duration input |
| YouTube | YouTube URL input (`max-w-sm`) + inline validation error + Duration input |

Speed selector is shown for Hosted and External only — not for Loom or YouTube.

Incomplete source warning — `text-muted-foreground text-xs` — shown below controls when the video source is not yet in a publishable state.

## Hosted video card

`<div className="flex items-center gap-3 rounded-lg border px-3 py-2">`

- Poster thumbnail — `size-12 shrink-0 rounded object-cover` — shown when a poster URL is available; fallback is a `bg-muted` square with `<Video className="size-5 text-muted-foreground" />`
- Title — `truncate text-sm font-medium`
- Duration — `text-muted-foreground text-xs`
- Change — `variant="ghost" size="sm"`
- Remove — plain `<button>` — `shrink-0 rounded p-1 hover:bg-muted` — `<X className="size-4 text-muted-foreground" />`

## Input sizing

| Field | Width | Notes |
|---|---|---|
| URL / Loom / YouTube | `h-8 w-full max-w-sm` | |
| Duration | `h-8 w-20 font-mono` | |
| Speed | `h-8 w-28` | `<Select>` |

## Validation errors

Loom and YouTube inputs show an inline error below the input — `text-destructive mt-1 text-xs` — when the entered value cannot be parsed as a valid video ID or URL.

## Rules

- Returns `null` when layout is not Video — do not render a wrapper div when hidden
- Duration input is always `font-mono`
- Speed selector is absent for Loom and YouTube — those players control playback speed natively
- Removing a hosted video clears both the selected video and resets the source to an empty hosted state
