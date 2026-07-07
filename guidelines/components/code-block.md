# CodeBlock

> Stub — expand as component is documented.

Renders syntax-highlighted code with an optional filename, language badge, line numbers, and copy button. `Terminal` is a variant for shell output with typed line annotations (`command`, `output`, `error`, `warning`).

Both components are always dark regardless of page theme — they do not respond to the theme toggle.

## CSS Variables

Always-dark, theme-invariant. Defined in `:root` with no `.dark` overrides. Applied via the `.code-block` CSS class in `globals.css`. Do not use these variables outside `CodeBlock` and `Terminal`.

| Variable | Role |
|---|---|
| `--code-bg` | Container background (`#0d1117`) |
| `--code-header-bg` | Header bar background |
| `--code-border` | Container and header border |
| `--code-fg` | Code text foreground |
| `--code-header-fg` | Header labels and icons |
| `--code-line-highlight-bg` | Highlighted line background |
| `--code-line-highlight-border` | Highlighted line left accent |
| `--code-copy-success` | Copy button success state |
