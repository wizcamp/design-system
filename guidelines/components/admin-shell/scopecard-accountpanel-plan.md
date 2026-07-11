# ScopeCard & AccountPanel — implementation plan

Both components wrap existing primitives from `components/ui/sidebar.tsx`. Neither should reimplement styling, active-state, or collapse behavior that the primitives already own — that's the core lesson from the current `CohortContextGroup`/`UserNavFooter` code, which hand-rolled all three.

**AccountPanel scope note:** per requirement, only variants where the account holder's name and email remain visible at rest (no hover/click required) are included. That disqualifies the trigger→Sheet pattern (email replaced by "View account") and the compact single-line pattern (email dropped entirely). Three variants qualify — A, B, C below — presented as real alternatives, not a single forced answer.

---

## 1. ScopeCard

### Purpose
Generic "active scope" indicator. Replaces `CohortContextGroup`. Decoupled from the `Cohort` domain type — the caller resolves which entity is active and passes primitive props.

### Prop shape

```ts
type ScopeCardProps = {
  href: string;
  icon: LucideIcon;
  eyebrow: string;   // e.g. campName
  label: string;     // e.g. cohortName, falls back to slug
  isActive?: boolean; // default true — card only renders when a scope is active
};
```

### Resolver (lives in `AdminSidebar`, not in the component)

```ts
function resolveActiveScope(pathname: string, cohorts: Cohort[]): ScopeCardProps | null {
  const match = pathname.match(/^\/admin\/cohorts\/([^/]+)/);
  if (!match) return null;
  const slug = match[1];
  const cohort = cohorts.find(c => c.cohortSlug === slug);
  return {
    href: `/admin/cohorts/${slug}`,
    icon: Calendar,
    eyebrow: cohort?.campName ?? '…',
    label: cohort?.cohortName ?? slug,
  };
}
```

Adding a second scope-bearing entity later (Students, Enrollments) means adding a branch to this resolver, not touching `ScopeCard`.

### Next.js implementation

```tsx
// components/admin/scope-card.tsx
'use client';

import Link from 'next/link';
import type { LucideIcon } from 'lucide-react';
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarGroupContent,
  SidebarMenuButton,
} from '@/components/ui/sidebar';

type ScopeCardProps = {
  href: string;
  icon: LucideIcon;
  eyebrow: string;
  label: string;
  isActive?: boolean;
};

export function ScopeCard({ href, icon: Icon, eyebrow, label, isActive = true }: ScopeCardProps) {
  return (
    <SidebarGroup data-slot="scope-card">
      <SidebarGroupLabel>Current context</SidebarGroupLabel>
      <SidebarGroupContent>
        <SidebarMenuButton
          isActive={isActive}
          render={<Link href={href} />}
          tooltip={label}
          size="lg"
          className="bg-primary/10 text-primary h-auto py-2.5"
        >
          <Icon className="size-4 shrink-0" />
          <div className="min-w-0 flex-1 text-left">
            <p className="text-muted-foreground text-xs">{eyebrow}</p>
            <p className="truncate text-sm font-medium">{label}</p>
          </div>
        </SidebarMenuButton>
      </SidebarGroupContent>
    </SidebarGroup>
  );
}
```

Built entirely from `SidebarGroup` / `SidebarGroupLabel` / `SidebarMenuButton` — icon-mode collapse and the hover tooltip come free from `SidebarMenuButton`, no bespoke CSS needed.

### Figma frame naming

Two Figma pages matter here: a **Primitives** page (already presumably holding the shadcn/base-ui `Sidebar` component set — `Sidebar/Group`, `Sidebar/MenuButton`, etc.) and a **Compositions** (or **Patterns**) page where `ScopeCard` lives as an assembled instance of those primitives, not a detached redraw.

```
Compositions
└── Sidebar / Scope Card                     [component, main]
    ├── Sidebar / Scope Card / Default        [variant: state=active]
    ├── Sidebar / Scope Card / Collapsed      [variant: state=icon-only]
    └── Sidebar / Scope Card / Loading        [variant: state=loading — eyebrow="…"]
```

Inside `Sidebar / Scope Card / Default`:

```
Sidebar / Scope Card / Default
├── Sidebar / Group Label            → instance of Primitives/Sidebar/GroupLabel, text override "Current context"
└── Sidebar / Menu Button            → instance of Primitives/Sidebar/MenuButton, size=lg, active=true
    ├── Icon                         → instance of Icon/Calendar (swappable component property)
    └── Label Group
        ├── Eyebrow                  → text layer, bound to a text property "eyebrow"
        └── Label                    → text layer, bound to a text property "label"
```

Implementation notes for the Figma file:
- Use **component properties** (not hardcoded copies) for `icon`, `eyebrow`, `label`, and a boolean `active` — this mirrors the TS prop shape 1:1, so a designer picking properties in the inspector matches the props a developer sets in JSX.
- The `Collapsed` variant should show only the `Icon` instance at 32×32, matching the `group-data-[collapsible=icon]` behavior in code — don't let Figma and code drift on what collapse looks like.
- Nest `Sidebar / Scope Card` as a child of the `Sidebar / Content` frame in any full-sidebar composition, matching the DOM order (`SidebarContent > ScopeCard`).

---

## 2. AccountPanel — three qualifying variants

All three keep name and email visible at rest. Pick one to ship first; the others are documented as fallback options if constraints change (e.g. panel needs to support >2 actions later).

### Shared prop shape

```ts
type AccountIdentity = {
  name: string;
  email: string;
  avatarUrl?: string;
};

type AccountPanelProps = {
  identity: AccountIdentity;
  themeMutation: UseMutationResult<AdminSettings, unknown, ThemeUpdateInput>;
  onSignOut: () => void;
};
```

Keeping `identity` as its own object (rather than spreading `name`/`email`/`avatarUrl` as top-level props) is what makes `AccountIdentity` reusable outside the sidebar footer later — e.g. in a settings page header — without prop duplication.

---

### Variant A — stacked rows (recommended default)

Identity row full-width for readable truncation; action rail on a second row, indented to align under the name column. No new primitive dependency.

**Next.js**

```tsx
// components/admin/account-panel.tsx
'use client';

function AccountIdentityRow({ name, email, avatarUrl }: AccountIdentity) {
  const initials = getInitials(name);
  return (
    <div data-slot="account-identity" className="flex items-center gap-3">
      <Avatar className="size-8 shrink-0">
        <AvatarImage src={avatarUrl} />
        <AvatarFallback className="text-xs">{initials}</AvatarFallback>
      </Avatar>
      <div className="min-w-0 flex-1 group-data-[collapsible=icon]:hidden">
        <p className="truncate text-sm leading-tight font-medium">{name}</p>
        <p className="text-muted-foreground truncate text-xs">{email}</p>
      </div>
    </div>
  );
}

function AccountActionRail({ children }: { children: React.ReactNode }) {
  return (
    <div
      data-slot="account-action-rail"
      className="ml-11 flex items-center justify-between group-data-[collapsible=icon]:hidden"
    >
      {children}
    </div>
  );
}

export function AccountPanel({ identity, themeMutation, onSignOut }: AccountPanelProps) {
  return (
    <div data-slot="account-panel" className="flex flex-col gap-2 rounded-lg px-2 py-2">
      <AccountIdentityRow {...identity} />
      <AccountActionRail>
        <ThemeToggle mutation={themeMutation} />
        <Button
          size="icon"
          variant="ghost"
          className="text-muted-foreground hover:text-foreground size-8 shrink-0"
          onClick={onSignOut}
          aria-label="Sign out"
        >
          <LogOut className="size-4" />
        </Button>
      </AccountActionRail>
    </div>
  );
}
```

**Figma**

```
Sidebar / Account Panel                        [component, main]
├── Sidebar / Account Panel / Default            [variant: state=default]
├── Sidebar / Account Panel / Collapsed           [variant: state=icon-only — avatar only]
└── Sidebar / Account Panel / Default
    ├── Account Identity                          → own component (see below), instanced
    └── Account Action Rail
        ├── Theme Segmented Control                → instance of Primitives/SegmentedControl (light/dark/system)
        └── Sign Out Button                        → instance of Primitives/Sidebar/MenuAction, icon=logout
```

`Account Identity` should be its **own top-level Figma component**, not nested-only inside `Account Panel` — this mirrors `AccountIdentityRow` being independently reusable in code:

```
Sidebar / Account Identity                      [component, main]
├── Avatar                                       → instance of Primitives/Avatar
└── Label Group
    ├── Name                                     → text property "name"
    └── Email                                    → text property "email"
```

---

### Variant B — trigger row that opens a menu (theme + sign-out live inside)

Identity row itself stays fully visible and unmodified — the menu is *additive*, not a replacement for the identity display, which is why this qualifies (unlike the disqualified Sheet variant, nothing about the resting state changes).

**Next.js**

```tsx
export function AccountPanel({ identity, themeMutation, onSignOut }: AccountPanelProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger
        render={
          <SidebarMenuButton size="lg" tooltip={identity.name} className="h-auto py-2">
            <AccountIdentityRow {...identity} />
            <i className="ti ti-selector" aria-hidden />
          </SidebarMenuButton>
        }
      />
      <DropdownMenuContent side="top" align="start" className="w-56">
        <DropdownMenuLabel className="text-xs text-muted-foreground">Theme</DropdownMenuLabel>
        <ThemeToggle mutation={themeMutation} />
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={onSignOut} className="text-destructive">
          <LogOut className="size-4" /> Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

⚠️ Confirm `@/components/ui/dropdown-menu` exists in the library before committing to this path — not verified in this plan.

**Figma**

```
Sidebar / Account Panel — Menu Variant           [component, main]
├── Trigger                                       [variant: state=closed | open]
│   └── Sidebar / Account Identity                → instance, same component as Variant A
│       └── Chevron (Selector)                    → instance of Icon/Selector
└── Menu / Account Actions                        → separate component, absolutely positioned
    ├── Menu / Theme Row
    │   └── Theme Segmented Control                → instance of Primitives/SegmentedControl
    ├── Menu / Divider                             → instance of Primitives/Menu/Separator
    └── Menu / Sign Out Item                        → instance of Primitives/Menu/Item, danger=true
```

Model the open/closed states as **interactive component variants** (`state=closed`/`state=open`) with a prototype connection between them, so the Figma file itself demonstrates the interaction rather than requiring a second static frame elsewhere in the file.

---

### Variant C — hover-reveal action rail

Identity is permanently visible; only the *action icons* fade in on hover/focus. Qualifies because name/email are never hidden — only the actions are conditionally shown, which is the inverse of the disqualified variants.

Note: at 216px width this variant cannot fit a 3-way theme segmented control next to two lines of identity text — it only has room for a single cycling icon (light↔dark), which drops the `'system'` state as a distinct visible option. Flag this against the sprint's decision to sync `'system'` as a first-class value before choosing this variant.

**Next.js**

```tsx
export function AccountPanel({ identity, themeMutation, onSignOut }: AccountPanelProps) {
  return (
    <div
      data-slot="account-panel"
      className="group/account flex items-center gap-2.5 rounded-lg px-2 py-2"
    >
      <AccountIdentityRow {...identity} />
      <div
        data-slot="account-action-rail"
        className="flex shrink-0 gap-0.5 opacity-0 transition-opacity group-hover/account:opacity-100 group-focus-within/account:opacity-100"
      >
        <ThemeCycleButton mutation={themeMutation} />
        <Button size="icon" variant="ghost" className="size-6" onClick={onSignOut} aria-label="Sign out">
          <LogOut className="size-3.5" />
        </Button>
      </div>
    </div>
  );
}
```

Requires a `focus-within` fallback (included above) so the actions are reachable via keyboard/touch, not just mouse hover — hover-only affordances with no fallback fail accessibility review.

**Figma**

```
Sidebar / Account Panel — Hover Variant          [component, main]
├── Sidebar / Account Panel — Hover Variant / Idle       [variant: state=idle, actions opacity=0]
└── Sidebar / Account Panel — Hover Variant / Hovered    [variant: state=hovered, actions opacity=100]
    ├── Sidebar / Account Identity                        → instance, same shared component
    └── Action Rail (compact)
        ├── Theme Cycle Button                             → instance of Primitives/Sidebar/MenuAction, icon=sun/moon toggle only
        └── Sign Out Button                                 → instance of Primitives/Sidebar/MenuAction, icon=logout
```

---

## Cross-cutting notes

- **Shared `Sidebar / Account Identity` component**: build it once, instance it into all three `AccountPanel` variants (and into Variant B's trigger). Don't let three teams draw three slightly-different avatar+name+email blocks.
- **`data-slot` convention**: every new wrapper (`account-panel`, `account-identity`, `account-action-rail`) should carry a `data-slot` attribute, matching the convention every primitive in `sidebar.tsx` already uses. This keeps the DOM introspectable the same way `[data-slot="sidebar-footer"]` already is, and gives CSS targeting parity with the existing collapse/state selectors (`group-data-[collapsible=icon]:*`).
- **Icon-collapse state**: for all three AccountPanel variants, collapsed mode should show the avatar alone with a tooltip carrying the full name — consistent with `SidebarMenuButton`'s existing icon-only + tooltip pattern, not a new fallback behavior invented per-variant.
- **Settings duplication check**: `AdminSidebar` already has a top-level `SidebarMenuItem` linking to `/admin/settings` directly above the footer. None of the three variants above add a second settings entry point — confirm that's still correct before shipping, since B's menu would be a natural place to accidentally re-add it.
