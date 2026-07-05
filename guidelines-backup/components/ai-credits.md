# AiCredits

A settings card for displaying and managing a user's AI API key.
Shows the key in a masked input field with visibility toggle and copy
actions, plus an optional notice for users whose credits are not yet
set up.

## Structure

1. Card container — `div` — `bg-card rounded-2xl border-border p-8 flex flex-col gap-6`
2. Title — "AI Credits" — `.wiz-heading` + `text-foreground`
   (uses `font-lms-header-secondary` — Plus Jakarta Sans Bold)
3. API Key group — `flex flex-col gap-2 w-full`
   - Label — "OpenRouter API Key" — `.wiz-body` + `font-semibold` + `text-foreground`
   - Description — `.wiz-label` + `text-muted-foreground`
   - Input field — `bg-surface-canvas border-border rounded-full h-[44px] px-3 py-1 relative`
     - Inner container — `relative w-full h-6`
     - Key icon — `absolute left-0 top-0` — `<IconLock size={24} />`
     - Masked value — `absolute left-[32px] top-[1.5px]`, 18px, Inter Regular,
       `tracking-[4px]`, `text-input`
     - Visibility toggle — `absolute left-[760px] top-0` — `<IconEye size={24} />`
       (right-aligned, 2 icons from right edge)
     - Copy button — `absolute left-[792px] top-0` — `<IconCopy size={24} />`
       (rightmost icon)
4. Notice box (optional) — `bg-surface-canvas border-border rounded-full h-[44px] px-3 py-1`
   - Text — `.wiz-label` + `text-input` — notice/status message

## Icon usage

- Lock: `<IconLock size={24} />` from `@tabler/icons-react`
- Eye: `<IconEye size={24} />` from `@tabler/icons-react`
- Copy: `<IconCopy size={24} />` from `@tabler/icons-react`

## Props

| Prop | Type | Required | Description |
|---|---|---|---|
| `apiKey` | string | yes | The raw API key value |
| `masked` | boolean | no | Whether to show the key masked (default `true`) |
| `onToggleVisibility` | () => void | yes | Toggles masked/visible state |
| `onCopy` | () => void | yes | Copies the key to clipboard |
| `notice` | string | no | Optional notice text below the input. Omit to hide. |

## Variants

None at this stage. Single variant only.

## Rules

- Card: `bg-card rounded-2xl border-border p-8` — uses a visible border,
  unlike the ProfileBanner which relies on surface color
- Title: `.wiz-heading` (20px, Plus Jakarta Sans Bold via `font-lms-header-secondary`)
  + `text-foreground`
- Label: `.wiz-body` (14px) + `font-semibold` + `text-foreground`
- Description: `.wiz-label` (13px) + `text-muted-foreground`
- Input field: `bg-surface-canvas border-border rounded-full h-[44px] px-3 py-1`
  — pill shape, icons and masked text are absolutely positioned inside a
  relative 24px-tall inner container
- Masked key text: 18px, Inter Regular, `tracking-[4px]`, `text-input`
- Action icons (eye, copy): 24px, `text-muted-foreground`, cursor-pointer,
  absolutely positioned at right edge of input, wrapped in `<button>` with focus ring
- Notice box: `bg-surface-canvas border-border rounded-full h-[44px] px-3 py-1`
  — same pill shape as input field
- Notice text: `.wiz-label` (13px) + `text-input`
- Do NOT use `lucide-react` — all icons from `@tabler/icons-react` only
- Do NOT reveal the full API key by default — mask with bullet characters