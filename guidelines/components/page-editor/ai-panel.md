# AIPanel

The AI chat panel rendered in the right panel when mode is set to AI. Built on `assistant-ui` primitives. Requires an OpenRouter API key configured in admin settings — shows a gated empty state otherwise.

## Contains

- `AssistantRuntimeProvider`, `ThreadPrimitive`, `MessagePrimitive`, `ComposerPrimitive`, `ActionBarPrimitive` — `@assistant-ui/react`, no separate doc

## Structure

`<ThreadPrimitive.Root className="flex h-full flex-col">`

1. **Viewport** — `min-h-0 flex-1 overflow-y-scroll scroll-smooth px-2 pt-4`
   - **Empty state** (when thread has no messages) — `flex h-32 flex-col items-center justify-center gap-1 text-center text-sm text-muted-foreground`
     - `"Ask the AI about your lesson"` — `font-medium`
     - `"Selected text or the full document is sent as context."` — `text-xs`
   - **User message** — `mb-4 flex justify-end px-2`
     - Bubble — `bg-primary text-primary-foreground max-w-[85%] rounded-xl px-3.5 py-2 text-sm`
   - **Assistant message** — `mb-4 px-2`
     - Content — `leading-relaxed` — markdown rendered via `MarkdownText`
     - Streaming indicator — `text-muted-foreground animate-pulse text-sm` — `●` — shown only while generating with no content yet
     - Error state — `border-destructive/30 bg-destructive/10 text-destructive mt-2 rounded-md border p-2 text-xs`
     - Action bar — `text-muted-foreground mt-1.5 flex items-center gap-0.5` — hidden while running, auto-hides on non-last messages
   - **Composer** — sticky at bottom of viewport — `sticky bottom-0 pb-3 pt-2`

2. **No-key empty state** (replaces thread entirely) — `flex h-full flex-col items-center justify-center gap-3 p-6 text-center text-sm text-muted-foreground`
   - `"No OpenRouter API key configured."`
   - Link to `/admin/settings` — `text-primary text-sm underline underline-offset-2`

## Composer

`<ComposerPrimitive.Root className="border-input bg-background flex w-full flex-col rounded-xl border px-1 pt-1.5 transition-colors outline-none focus-within:border-foreground/40">`

- Textarea — `placeholder:text-muted-foreground max-h-28 min-h-[52px] resize-none bg-transparent px-3 py-2 text-sm`
- Send/Cancel row — `flex items-center justify-end px-2 pb-2`
  - Send — `bg-primary text-primary-foreground hover:bg-primary/90 flex size-7 items-center justify-center rounded-full` — `<ArrowUpIcon className="size-3.5" />`
  - Cancel (while running) — same classes — `<SquareIcon className="size-3 fill-current" />`

## Action bar buttons

All: `hover:bg-muted hover:text-foreground flex size-7 items-center justify-center rounded transition-colors`

| Button | Icon | Size | Notes |
|---|---|---|---|
| Copy | `CopyIcon` / `CheckIcon` | `size-3.5` | Swaps to check on copy |
| Reload | `RefreshCwIcon` | `size-3.5` | Regenerates last response |
| Insert at cursor | `ArrowUpFromLine` | `size-3.5` | Inserts markdown content at Monaco cursor position |

## Rules

- The no-key empty state replaces the entire panel — do not render the thread behind it
- The Insert at cursor button inserts at the current Monaco cursor position — it does not replace selected text
- Do not render `AIPanel` outside of `PageEditor` — it depends on the editor ref passed from `PageEditor`
