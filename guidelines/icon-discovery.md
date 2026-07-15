# Icon Discovery

All icons are imported from `@/lib/icons` (a Lucide re-export shim). Do NOT import icons from
`lucide-react` or `@tabler/icons-react` directly.

```tsx
import { Search, Trash2, Plus } from '@/lib/icons';
```

All Lucide icons accept: `size` (number, default 24), `strokeWidth` (number, default 2),
`color` (default `"currentColor"`), `className`.

IMPORTANT: Do NOT guess icon names. Verify every icon exists in this catalog before importing.

## Usage patterns

### Standard UI (admin, portal, settings)

Always use the `<Icon>` wrapper. It enforces `strokeWidth={1.75}`, `shrink-0`, and numeric `size`.

```tsx
import { Icon } from '@/components/ui/icon';
import { Search, Trash2 } from '@/lib/icons';

<Icon icon={Search} size={16} />
<Icon icon={Trash2} size={16} className="text-destructive" />
```

Size mapping from Tailwind classes:
| Tailwind | `size` prop |
|---|---|
| `size-3` | `size={12}` |
| `size-3.5` | `size={14}` |
| `size-4` | `size={16}` |
| `size-5` | `size={20}` |
| `size-6` | `size={24}` |

### MDX components

Raw icon JSX with `className="size-*"` is correct inside `components/mdx/`. The `<Icon>` wrapper
is not wired up in prose rendering contexts.

```tsx
import { Info } from '@/lib/icons';

<Info className="size-4 text-blue-500" />
```

### Brand icons (multi-color SVGs)

OAuth provider logos and other brand marks that require exact multi-color fills live in
`components/ui/brand-icons.tsx`. Do NOT route these through `<Icon>` — brand colors are not
`currentColor`.

```tsx
import { GoogleBrandIcon } from '@/components/ui/brand-icons';

<GoogleBrandIcon className="size-4" />
```

### Never

- Do not import icons directly from `lucide-react` or `@tabler/icons-react` — always use `@/lib/icons`
- Do not use raw icon JSX with `className="size-*"` outside `components/mdx/` and `components/ui/`
- Do not pass brand SVGs through `<Icon>` wrapper

---

## Wizcamp standard icons

Icons used across the application, sorted by frequency of use.

| Import name | Context |
|---|---|
| `Check` | confirmation, checkmarks |
| `Trash2` | delete actions |
| `Eye` | impersonate, publish, view |
| `MoreHorizontal` | overflow menu trigger |
| `Plus` | add/create actions |
| `ChevronRight` | navigation, breadcrumbs |
| `ChevronLeft` | navigation, back |
| `ChevronDown` | dropdowns, collapsibles |
| `Video` | video source indicator |
| `RotateCcw` | reactivate/reinstate, rewind |
| `RotateCw` | skip forward |
| `Play` | video player |
| `Pause` | video player |
| `LogOut` | sign out |
| `Lock` | lock unit |
| `FileText` | doc page type |
| `Copy` | copy to clipboard |
| `X` | close/dismiss |
| `Send` | resend invitation |
| `Search` | search inputs |
| `CircleCheck` | conclude/complete, success states |
| `Pencil` | edit actions |
| `GripVertical` | drag handle |
| `ExternalLink` | open in new tab |
| `ArrowRight` | navigation links |
| `ArrowLeft` | back navigation |
| `AlertCircle` | error states |
| `EyeOff` | unpublish |
| `RefreshCcw` | sync/refresh |
| `LayoutGrid` | grid view toggle |
| `Github` | OAuth provider (monochrome) |
| `Calendar` | dates, date pickers |
| `CalendarDays` | date ranges |
| `BookOpen` | learning content |
| `Ban` | suspend student |
| `AlertTriangle` | warnings |
| `Users` | students/people |
| `Upload` | file upload |
| `Sparkles` | AI/highlights |
| `Settings` | configuration |
| `Info` | info tooltips |
| `Bell` | notifications |
| `BarChart3` | engagement/progress |
| `Download` | file downloads |
| `Lightbulb` | tips/hints |
| `School` | education |
| `LayoutDashboard` | dashboard nav |
| `Link` | URL links |
| `Film` | video/media |
| `LockOpen` | unlock unit |
| `ChevronUp` | collapse/expand |
| `CircleX` | error/cancel |
| `PictureInPicture2` | picture-in-picture |
| `Maximize` | fullscreen enter |
| `Minimize` | fullscreen exit |
| `Volume2` | volume on |
| `VolumeX` | volume muted |
| `Zap` | speed/time-saved |
| `SwatchBook` | color swatch |
| `Palette` | color picker |
| `Ruler` | measure |
| `PanelRightOpen` | right panel toggle |
| `Globe` | external site |
| `Key` | API key / password |
| `Chrome` | Google OAuth (monochrome fallback) |
| `ArrowUpDown` | sort toggle |
| `CheckCheck` | double-check / validated |
| `LayoutSidebarRight` | sidebar toggle alias |

## Fallback: verifying unlisted icons

If the icon you need is not in this catalog:
1. Check https://lucide.dev/icons — search by keyword
2. Lucide import names are PascalCase of the icon name (e.g. `arrow-up` → `ArrowUp`)
3. Verify the name exists in `lib/icons.ts` before using it
4. If the icon doesn't exist in the shim, add it to `lib/icons.ts` as a named re-export from `lucide-react`
