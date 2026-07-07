# Icon Discovery

All icons are imported from `@tabler/icons-react`. Do NOT import icons from any other library.

```tsx
import { IconPlus, IconTrash, IconSearch } from '@tabler/icons-react'
```

All Tabler icons accept: `size` (default 24), `color` (default `"currentColor"`), `stroke` (default 2), `className`.

IMPORTANT: Do NOT guess icon names. Verify every icon exists in this catalog before importing.

## Wizcamp standard icons

Icons used across the application, sorted by frequency of use.

| Import name | Context |
|---|---|
| `IconCheck` | confirmation, checkmarks |
| `IconTrash` | delete actions |
| `IconEye` | impersonate, publish, view |
| `IconDots` | overflow menu trigger |
| `IconPlus` | add/create actions |
| `IconChevronRight` | navigation, breadcrumbs |
| `IconChevronLeft` | navigation, back |
| `IconChevronDown` | dropdowns, collapsibles |
| `IconVideo` | video source indicator |
| `IconRotate2` | reactivate/reinstate |
| `IconPlayerPlay` | video player |
| `IconLogout` | sign out |
| `IconLock` | lock unit |
| `IconFileText` | doc page type |
| `IconCopy` | copy to clipboard |
| `IconX` | close/dismiss |
| `IconSend` | resend invitation |
| `IconSearch` | search inputs |
| `IconCircleCheck` | conclude/complete, success states |
| `IconPencil` | edit actions |
| `IconLoader2` | loading spinner (use with `animate-spin`) |
| `IconGripVertical` | drag handle |
| `IconExternalLink` | open in new tab |
| `IconArrowRight` | navigation links |
| `IconArrowLeft` | back navigation |
| `IconAlertCircle` | error states |
| `IconEyeOff` | unpublish |
| `IconRefresh` | sync/refresh |
| `IconLayoutGrid` | grid view toggle |
| `IconBrandGithub` | OAuth provider |
| `IconCalendar` | dates, date pickers |
| `IconBook2` | learning content |
| `IconBan` | suspend student |
| `IconAlertTriangle` | warnings |
| `IconUsers` | students/people |
| `IconUpload` | file upload |
| `IconSparkles` | AI/highlights |
| `IconSettings` | configuration |
| `IconInfoCircle` | info tooltips |
| `IconBell` | notifications |
| `IconChartBar` | engagement/progress |
| `IconDownload` | file downloads |
| `IconBulb` | tips/hints |
| `IconSchool` | education |
| `IconLayoutDashboard` | dashboard nav |
| `IconLink` | URL links |
| `IconMovie` | video/media |
| `IconLockOpen` | unlock unit |
| `IconArrowUp` | sort ascending |
| `IconArrowDown` | sort descending |
| `IconArrowsUpDown` | sort toggle |
| `IconChevronUp` | collapse/expand |
| `IconCircleX` | error/cancel |
| `IconPlayerPlayFilled` | play button (filled) |
| `IconPhotoPlus` | insert image |
| `IconPhotoOff` | missing image |

## Fallback: verifying unlisted icons

If the icon you need is not in this catalog:
1. Check https://tabler.io/icons — search by keyword
2. Tabler import names are `Icon` + PascalCase of the icon name (e.g. `icon-arrow-up` → `IconArrowUp`)
3. If the icon doesn't exist, pick a different one from this catalog and verify
