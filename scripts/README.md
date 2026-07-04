# Figma Design Token Sync

Extracts color tokens from Figma and updates design system documentation.

## Setup

1. Install dependencies:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. Create `.env.local` with your Figma token:
   ```bash
   cp .env.example .env.local
   # Edit .env.local and add your token
   ```

3. Get your Figma Personal Access Token:
   - Go to https://www.figma.com/settings
   - Scroll to "Personal Access Tokens"
   - Click "Generate new token"
   - Copy and paste into `.env.local`

## Usage

```bash
# From the design-system repo root
python scripts/sync-figma-tokens.py
```

Or set the environment variable inline:

```bash
FIGMA_TOKEN=your_token_here python scripts/sync-figma-tokens.py
```

## What It Does

1. **Extract**: Fetches the base colors table from Figma
   - Reads variable names from TEXT nodes
   - Extracts RGB colors (with opacity) from RECTANGLE fills
   - Handles transparent colors correctly

2. **Transform**: Converts hex colors to OKLCH format
   - Preserves opacity/alpha channel
   - Outputs format: `oklch(L C H)` or `oklch(L C H / A%)`

3. **Load**: Updates design system files:
   - `guidelines/tokens.md` - Base Colors table with hex and OKLCH values
   - `styles/globals.css` - CSS custom properties in `:root`, `.dark`, and `@theme inline`

## Output Examples

### Opaque Color
```css
--accent: oklch(0.7686 0.1647 70.0804);
```

### Transparent Color
```css
--border: oklch(0.3391 0.1377 128.0499 / 12%);
```

## Adding New Frames

To sync additional Figma frames, modify `extract_figma_tokens()`:

1. Add new node ID to configuration
2. Implement extraction logic for the frame's structure
3. Add corresponding update functions for target files

## Troubleshooting

### "FIGMA_TOKEN environment variable not set"
- Create `.env.local` file in the repo root
- Add your token: `FIGMA_TOKEN=figd_xxxxx`

### "Figma API Error: 403"
- Your token may be invalid or expired
- Generate a new token at https://www.figma.com/settings

### "Error: '### Base Colors' section not found"
- Ensure `guidelines/tokens.md` exists and contains a `### Base Colors` heading
- The script will insert the table after this heading

### "Could not find block matching"
- Ensure `styles/globals.css` contains `:root {`, `.dark {`, and `@theme inline {` blocks
- Check for syntax errors in the CSS file
