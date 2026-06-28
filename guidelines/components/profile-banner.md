# ProfileBanner

A full-width profile card with a colored banner header, overlapping avatar,
user details, and a sign-out action. Used on account/settings pages for a
richer identity presentation than the compact ProfileCard.

## Structure

1. Card container — `<Card />` — `bg-card rounded-3xl overflow-hidden`
2. Banner background — `div` — `bg-surface-raised-dark h-40 w-full`
3. Avatar — `size-30 rounded-full`, positioned to overlap the banner bottom
   by 80px, 40px from the left edge (`-mt-20 ml-10`)
4. Info section — `flex flex-col gap-4 px-10 pb-8`
   - User name — `.wiz-hero` (32px, Plus Jakarta Sans SemiBold) + `text-foreground`
   - Contact row — `flex gap-3 items-center`
     - Email — `.wiz-body` (14px) + `font-medium` + `text-muted-foreground`
     - Connection badge — `<Badge variant="outline">` pill (`rounded-full`)
       with Tabler icon (12px) + label (`.wiz-caption` + `font-medium`)
   - Bio/status text — `.wiz-body` + `text-foreground`
5. Sign-out button — positioned **bottom-right** inside the card, above the
   banner area — `<Button variant="outline" size="sm">` pill shape
   (`rounded-full`) with "Log Out" text + `<IconLogout size={14} />`

## Icon usage

- Connection badge: `<IconBrandGithub size={12} />` from `@tabler/icons-react`
- Sign-out button: `<IconLogout size={14} />` from `@tabler/icons-react`

## Props

| Prop | Type | Required | Description |
|---|---|---|---|
| `name` | string | yes | Full display name |
| `email` | string | yes | Email address |
| `avatarSrc` | string | yes | Avatar image URL |
| `avatarAlt` | string | yes | Alt text for avatar |
| `bio` | string | no | Short bio/status line. Omit to hide. |
| `badgeLabel` | string | no | e.g. "Github". Omit to hide badge. |
| `badgeIcon` | ReactNode | no | Icon for badge, e.g. `<IconBrandGithub size={12} />` |
| `onSignOut` | () => void | yes | Callback for sign-out button |

## Variants

None at this stage. Single variant only.

## Rules

- Card: `<Card />` — `bg-card rounded-3xl overflow-hidden`
- Banner: `bg-surface-raised-dark h-40 w-full` — no border, no shadow
- Avatar: `size-30 rounded-full object-cover` — shadcn `<Avatar>` component,
  no box shadow, no border ring. Positioned with `-mt-20 ml-10` to overlap
  the banner by 80px
- Name: `.wiz-hero` + `text-foreground` — uses `font-lms-heading` (Plus Jakarta
  Sans SemiBold). **Note:** Plus Jakarta Sans must be installed and registered
  as `font-lms-heading` in the project before building this component.
- Email: `.wiz-body` + `font-medium` + `text-muted-foreground`
- Badge: `<Badge variant="outline">` — pill shape with icon + label. Uses
  shadcn/ui Badge component with outline variant
- Bio text: `.wiz-body` + `text-foreground`
- Sign-out button: `<Button variant="outline" size="sm">` — pill shape
  (`rounded-full`). Text uses `.wiz-caption` + `font-medium`. Icon uses
  `<IconLogout size={14} className="ml-1" />`
- Info section padding: `px-10 pb-8`, internal gap `gap-4`
- Contact row: email and badge sit in a horizontal `flex gap-3 items-center` row
- Do NOT use `lucide-react` — all icons from `@tabler/icons-react` only
- Do NOT add a `<Separator />` — the design uses surface color for hierarchy
- Do NOT add a section label — no "Account" or similar heading above the card