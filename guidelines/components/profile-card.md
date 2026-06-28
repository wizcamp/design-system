```markdown
# ProfileCard

A compact account identity card. Used on account/settings pages to display
the signed-in user's identity and provide a sign-out action.

## Structure

1. Section label ("Account") — `text-xs font-semibold text-muted-foreground`
2. Avatar — `size-16 rounded-full` (64px circle, no shadow, no ring)
3. User name — `text-sm font-semibold text-foreground`
4. Email address — `text-xs text-muted-foreground`
5. Connection status row — Tabler icon + `text-xs text-muted-foreground`
6. Horizontal separator — `<Separator />` from shadcn/ui
7. Sign-out button — `<Button variant="ghost" size="sm">` with left-aligned Tabler icon

## Icon usage

- Connection status: `<IconBrandGithub size={12} />` from `@tabler/icons-react`
- Sign-out button: `<IconLogout size={16} />` from `@tabler/icons-react`

## Props

| Prop | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Full display name |
| `email` | string | yes | Email address |
| `avatarSrc` | string | yes | Avatar image URL |
| `avatarAlt` | string | yes | Alt text for avatar |
| `connectionLabel` | string | no | e.g. "Connected via GitHub". Omit to hide row. |
| `onSignOut` | () => void | yes | Callback for sign-out button |

## Variants

None at this stage. Single variant only.

## Rules

- Card: `<Card />` — `bg-card rounded-lg border border-border p-6`
- Avatar: `size-16 rounded-full object-cover` — no box shadow, no border ring
- Name + email + connection status stack vertically with `gap-0.5`
- Avatar and text block sit in a `flex items-center gap-4` row
- Separator: `<Separator />` — do not use a div with a border or an `<hr>`
- Sign-out button: `<Button variant="primary" size="sm">`
- Icon in button: `<IconLogout size={16} className="mr-2" />`
- Do NOT use `lucide-react` — all icons from `@tabler/icons-react` only
```