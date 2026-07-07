# LessonNavBar

Portal component rendered at the bottom of every lesson page. Displays intra-unit progress, a "up next" preview card, and previous/next navigation buttons.

Internally uses `ProgressBar` with `indicatorClassName="bg-progress-lesson-indicator"` (violet/primary). This is the only place that class is applied — do not use it elsewhere.

## Structure

`<div className="mt-12 rounded-2xl border bg-card p-6 shadow-sm space-y-4">`

1. **Unit context row** — `flex items-center justify-between text-sm`
   - Unit title — `font-medium text-foreground truncate`
   - Lesson counter — `text-muted-foreground shrink-0 tabular-nums` — e.g. `"Week · Lesson 2 of 5"`

2. **Progress bar** — `<ProgressBar size="sm" indicatorClassName="bg-progress-lesson-indicator">` — single-layer, violet/primary fill, ambient orientation only

3. **Up-next card** (conditional — three states):
   - **Next present, unlocked** — `rounded-xl bg-muted/50 border border-border px-4 py-3`
     - Label — `text-xs text-muted-foreground mb-0.5` — `"Up next"` or `"Up next · {nextUnitTitle}"` when crossing a unit boundary
     - Title — `text-sm font-medium text-foreground truncate`
   - **Next locked** — `rounded-xl bg-muted/30 border border-border/50 px-4 py-3 flex items-center gap-2`
     - `<Lock className="size-3.5 shrink-0 text-muted-foreground" />`
     - Label — `text-xs text-muted-foreground mb-0.5` — `"Coming soon"`
     - Title — `text-sm font-medium text-muted-foreground truncate` — shows `nextUnitTitle` if available, else `next.title`
   - **Next null** — slot absent entirely

4. **Navigation row** — `flex items-center justify-between gap-3 pt-1`
   - **Previous button** (conditional):
     - Present: `<Link>` — `inline-flex items-center gap-2 h-10 rounded-full px-5 border bg-background text-foreground text-sm font-medium hover:bg-accent`
       — `<ChevronLeft className="size-4 shrink-0" />` + `"Previous"` (hidden below `sm`)
     - Absent (`prev` null): `<div aria-hidden />`
   - **Next button** (conditional — three states):
     - Unlocked: `<Link>` — `inline-flex items-center gap-2 h-10 rounded-full px-5 bg-primary text-primary-foreground text-sm font-semibold hover:bg-primary/90 shadow-sm`
       — `"Next Lesson"` + `<ChevronRight className="size-4 shrink-0" />`
     - Locked: `<span role="status">` — `inline-flex items-center gap-2 h-10 rounded-full px-5 border border-border/50 bg-background text-muted-foreground text-sm font-medium opacity-50 cursor-not-allowed`
       — `"Coming Soon"` (hidden below `sm`) + `<Lock className="size-4 shrink-0" />`
     - Absent (`next` null): `<div aria-hidden />`

## Props

| Prop | Type | Notes |
|---|---|---|
| `buildHref` | `(slug: string) => string` | Builds the full href for a page slug — handles student and admin preview routes |
| `unitLabel` | `string` | e.g. `"Week"`, `"Module"`, `"Session"` — from `cohort.unitLabel` |
| `unitTitle` | `string` | e.g. `"Week 1"` — the current unit's display title |
| `currentPageIndex` | `number` | 0-based index of the current page within the unit's published pages |
| `totalPagesInUnit` | `number` | Total published pages in the current unit |
| `prev` | `NavTarget \| null` | Previous page — `{ slug, title }` |
| `next` | `NextTarget \| null` | Next page — `{ slug, title, nextUnitTitle?, isLocked? }` |
| `onNavigate` | `() => void` | Optional — called immediately on nav button click to signal transition start |

## Rules

- Mount once per lesson page — never inside a loop or conditional that could render multiples
- Do not render a separate `ProgressBar` alongside `LessonNavBar` — it owns its own bar
- `buildHref` must handle both student (`/cohort/[slug]/learn/[page]`) and admin preview routes — pass it down from the parent shell, never construct hrefs inline
- `onNavigate` is for transition signaling only — do not use it to mutate server state
