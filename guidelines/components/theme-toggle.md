# ThemeToggle

A ghost icon button that opens a dropdown for selecting light, dark, or system theme. Persists the selection to the server via a settings mutation, with debounce and optimistic rollback on failure.

## Contains

- `DropdownMenu` primitives (`DropdownMenuTrigger`, `DropdownMenuContent`, `DropdownMenuItem`) — shadcn/ui, no separate doc
- `Button` — shadcn/ui primitive, no separate doc

## Structure

1. **Trigger** — ghost icon button, `size-8`
   - Icon reflects current theme: `Sun` (light), `Moon` (dark), `Monitor` (system)
   - `text-muted-foreground` at rest, `text-foreground` on hover
   - `aria-label` describes current theme including resolved system value

2. **Dropdown** — `align="end"`, three items
   - Light — `Sun` icon + label + `Check` when active
   - Dark — `Moon` icon + label + `Check` when active
   - System — `Monitor` icon + label + `Check` when active

3. **Hydration skeleton** — renders a static `Sun` button until mounted; prevents SSR mismatch

## Icon usage

**Current (lucide-react — migration pending):**

| Location | Import | Size |
|---|---|---|
| Light option / skeleton | `Sun` | `size-5` (trigger), `size-4` (menu item) |
| Dark option | `Moon` | `size-5` (trigger), `size-4` (menu item) |
| System option | `Monitor` | `size-5` (trigger), `size-4` (menu item) |
| Active checkmark | `Check` | `size-4` |

**Target (@tabler/icons-react):**

| Location | Import | Size |
|---|---|---|
| Light option / skeleton | `IconSun` | `size-5` (trigger), `size-4` (menu item) |
| Dark option | `IconMoon` | `size-5` (trigger), `size-4` (menu item) |
| System option | `IconDeviceDesktop` | `size-5` (trigger), `size-4` (menu item) |
| Active checkmark | `IconCheck` | `size-4` |

## Props

| Prop | Type | Required | Notes |
|---|---|---|---|
| `mutation` | `ReturnType<typeof useUpdateStudentSettingsMutation> \| ReturnType<typeof useUpdateAdminSettingsMutation>` | Yes | Pass the appropriate mutation for the current portal context |

## Variants

None. Single variant only.

## Rules

- Always pass the correct mutation for the portal context — student pages use `useUpdateStudentSettingsMutation`, admin pages use `useUpdateAdminSettingsMutation`
- Never call `setTheme` directly outside this component — always go through `ThemeToggle`
- The 400ms debounce is intentional — do not remove it
- Do not render more than one `ThemeToggle` per page
