#!/usr/bin/env python3
"""
Custom Spacing Sync Pipeline

Extracts semantic spacing tokens from two Figma design system tables (Desktop
and Mobile), merges them into a unified token set, and updates:
  - guidelines/foundations/custom-spacing.md
  - wizcamp-lms/app/globals.css  (:root CSS custom properties + @utility blocks)

The pipeline writes two sentinel-bracketed blocks into globals.css:

  1. /* ─── Custom spacing tokens  …  /* end custom spacing tokens */
     A :root block declaring --token-name CSS custom properties.
     Mobile-first: base values are mobile, @media (width >= 40rem) overrides
     to desktop values when they differ. Aligns with Tailwind v4's sm breakpoint.

  2. /* ─── Custom spacing utilities  …  /* end custom spacing utilities */
     One-liner @utility blocks — each applies a single CSS property via var().
     No media queries here; all responsive logic lives in the :root block.

Usage:
    python scripts/sync-spacing.py

Environment:
    FIGMA_TOKEN: Personal access token from Figma account settings
"""

import os
import sys
import re
import requests
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

# ==========================================
# CONFIGURATION
# ==========================================

FIGMA_FILE_ID = "0QoJnYRxO36C5snGqt79VD"
DESKTOP_NODE_ID = "31881-4"
MOBILE_NODE_ID = "21330-26900"

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
MONOREPO_ROOT = REPO_ROOT.parent.parent

load_dotenv(REPO_ROOT / ".env.local")

SPACING_MD_PATH = REPO_ROOT / "guidelines" / "foundations" / "custom-spacing.md"
GLOBALS_CSS_PATH = MONOREPO_ROOT / "wizcamp-lms" / "app" / "globals.css"

FIGMA_API_BASE = "https://api.figma.com/v1"

# Sentinel pairs that bracket each generated block in globals.css.
_TOKEN_BLOCK_START   = "/* ─── Custom spacing tokens"
_TOKEN_BLOCK_END     = "/* end custom spacing tokens */"
_UTILITY_BLOCK_START = "/* ─── Custom spacing utilities"
_UTILITY_BLOCK_END   = "/* end custom spacing utilities */"

# ==========================================
# HELPERS (copied from sync-fonts.py — keep in sync)
# ==========================================

def walk_tree(node: Dict):
    """Recursively yield all nodes in the tree."""
    yield node
    for child in node.get("children", []):
        yield from walk_tree(child)


# ==========================================
# TRANSFORM HELPERS
# ==========================================

def px_to_rem(px: int) -> str:
    """Convert integer pixel value to rem string (base 16px)."""
    rem = px / 16
    formatted = f"{rem:.4f}".rstrip("0").rstrip(".")
    return f"{formatted}rem"


# ==========================================
# PHASE 1: EXTRACT FROM FIGMA
# ==========================================

def extract_table(api_token: str, node_id: str, label: str) -> Dict[str, int]:
    """
    Extract token name → pixel value pairs from a Figma spacing table node.

    Returns a dict keyed by the raw Figma token name.
    """
    url = f"{FIGMA_API_BASE}/files/{FIGMA_FILE_ID}/nodes?ids={node_id}"
    headers = {"X-Figma-Token": api_token}

    print(f"📡 Fetching {label} node {node_id} from Figma...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    node_key = node_id.replace("-", ":")
    node_entry = data.get("nodes", {}).get(node_key)
    if not node_entry:
        print(f"❌ Node '{node_key}' returned null from Figma — the node may have moved or the token lacks access.")
        print(f"   Raw response keys: {list(data.get('nodes', {}).keys())}")
        print(f"   Raw node value: {data.get('nodes', {}).get(node_key)}")
        sys.exit(1)
    table_node = node_entry["document"]

    results: Dict[str, int] = {}

    for child in table_node.get("children", []):
        if child.get("type") != "FRAME":
            continue
        if child.get("name") == "Table Header":
            continue
        if not child.get("name", "").startswith("Table Row"):
            continue

        cells = child.get("children", [])
        if len(cells) < 2:
            continue

        token_name: Optional[str] = None
        for node in walk_tree(cells[0]):
            if node.get("type") == "TEXT":
                token_name = node.get("characters", "").strip()
                break

        px_text: Optional[str] = None
        for node in walk_tree(cells[1]):
            if node.get("type") == "TEXT":
                px_text = node.get("characters", "").strip()
                break

        if not token_name or not px_text:
            print(f"  ⚠️  Skipped row — missing name or value")
            continue

        try:
            px_value = int(px_text)
        except ValueError:
            print(f"  ⚠️  Skipped '{token_name}' — non-integer value '{px_text}'")
            continue

        results[token_name] = px_value
        print(f"  ✓ {token_name}: {px_value}px")

    print(f"✅ Extracted {len(results)} {label} tokens")
    return results


def extract_figma_spacing(api_token: str):
    desktop = extract_table(api_token, DESKTOP_NODE_ID, "Desktop")
    mobile  = extract_table(api_token, MOBILE_NODE_ID,  "Mobile")
    return desktop, mobile


# ==========================================
# PHASE 2: TRANSFORM
# ==========================================

def resolve_property(name: str) -> Optional[tuple[str, str]]:
    """
    Derive (css_property, css_var_name) from a Figma token name.

    Rules evaluated in order; first match wins.
    css_var_name mirrors the token name exactly: --container-padding-x,
    --section-padding-y, --section-title-gap-md, etc.
    Returns None if no rule matches — caller skips with a warning.

    Convention:
      - tokens ending in -x  → padding-inline
      - tokens ending in -y  → padding-block
      - tokens containing 'gap' or 'title' → gap
    """
    if name.endswith("-x"):
        return "padding-inline", f"--{name}"
    if name.endswith("-y"):
        return "padding-block", f"--{name}"
    if "title" in name or "gap" in name:
        return "gap", f"--{name}"
    return None


def build_tokens(desktop: Dict[str, int], mobile: Dict[str, int]) -> List[Dict]:
    """
    Merge Desktop and Mobile tables into a unified token list.

    Desktop table order is authoritative. Tokens not matched by resolve_property
    are skipped with a warning.
    """
    print("🔄 Building unified token list...")

    seen: Dict[str, bool] = {}
    tokens: List[Dict] = []

    for token_name, desktop_px in desktop.items():
        if token_name in seen:
            print(f"  ⚠️  Duplicate token: '{token_name}' (skipped)")
            continue
        seen[token_name] = True

        resolved = resolve_property(token_name)
        if not resolved:
            print(f"  ⚠️  Unknown token '{token_name}' — no matching rule in resolve_property, skipped")
            continue

        css_property, css_var = resolved
        mobile_px = mobile.get(token_name)

        tokens.append({
            "token_name":   token_name,
            "css_var":      css_var,        # e.g. --container-padding-x
            "css_property": css_property,   # e.g. padding-inline
            "desktop_px":   desktop_px,
            "desktop_rem":  px_to_rem(desktop_px),
            "mobile_px":    mobile_px,
            "mobile_rem":   px_to_rem(mobile_px) if mobile_px is not None else None,
        })

        mobile_display = f"{mobile_px}px → {px_to_rem(mobile_px)}" if mobile_px is not None else "—"
        print(f"  ✓ {token_name}: desktop={desktop_px}px → {px_to_rem(desktop_px)}, mobile={mobile_display}")

    print(f"✅ Built {len(tokens)} unified tokens")
    return tokens


# ==========================================
# PHASE 3: WRITE custom-spacing.md
# ==========================================

def write_spacing_md(tokens: List[Dict]) -> None:
    print(f"📝 Writing {SPACING_MD_PATH}...")

    lines = [
        "# Custom Spacing",
        "",
        "Auto-generated by `sync-spacing.py`. Do not edit manually.",
        "",
        "| Class | Desktop (px → rem) | Mobile (px → rem) |",
        "| :--- | :--- | :--- |",
    ]

    for t in tokens:
        mobile_col = (
            f"{t['mobile_px']}px → {t['mobile_rem']}"
            if t["mobile_px"] is not None
            else "—"
        )
        lines.append(
            f"| `{t['token_name']}` "
            f"| {t['desktop_px']}px → {t['desktop_rem']} "
            f"| {mobile_col} |"
        )

    SPACING_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPACING_MD_PATH.write_text("\n".join(lines) + "\n")
    print(f"✅ Wrote custom-spacing.md ({len(tokens)} tokens)")


# ==========================================
# PHASE 4: UPDATE globals.css
# ==========================================

def _build_token_block(tokens: List[Dict]) -> str:
    """
    Render the :root block declaring CSS custom properties.

    Mobile-first: base value is the mobile rem (or desktop if no mobile override).
    @media (width >= 40rem) applies the desktop value when it differs.
    Aligns with Tailwind v4's sm breakpoint (40rem = 640px at default font size).
    """
    lines = [
        "/* ─── Custom spacing tokens ─────────────────────────────────────────────────────",
        "   Auto-generated by sync-spacing.py. Do not edit manually.",
        "   Mobile-first CSS custom properties. @media (width >= 40rem) = Tailwind sm. */",
        ":root {",
    ]

    # Base values (mobile-first: use mobile_rem when available, else desktop_rem)
    for t in tokens:
        base = t["mobile_rem"] if t["mobile_rem"] is not None else t["desktop_rem"]
        lines.append(f"  {t['css_var']}: {base};")

    # Desktop overrides — only emit the @media block if any token actually differs
    overrides = [t for t in tokens if t["mobile_rem"] is not None and t["mobile_rem"] != t["desktop_rem"]]
    if overrides:
        lines.append("  @media (width >= 40rem) {")
        for t in overrides:
            lines.append(f"    {t['css_var']}: {t['desktop_rem']};")
        lines.append("  }")

    lines.append("}")
    lines.append(_TOKEN_BLOCK_END)
    return "\n".join(lines)


def _build_utility_block(tokens: List[Dict]) -> str:
    """
    Render one-liner @utility blocks — each applies a single CSS property via var().
    No media queries; all responsive logic lives in the :root token block above.
    """
    lines = [
        "/* ─── Custom spacing utilities ─────────────────────────────────────────────────",
        "   Auto-generated by sync-spacing.py. Do not edit manually.",
        "   Each utility is a single-line var() reference — responsive behaviour",
        "   is handled entirely by the CSS custom properties in the token block above. */",
    ]

    for t in tokens:
        lines.append(f"@utility {t['token_name']} {{ {t['css_property']}: var({t['css_var']}); }}")

    lines.append(_UTILITY_BLOCK_END)
    return "\n".join(lines)


def update_globals_css(tokens: List[Dict]) -> None:
    print(f"📝 Updating {GLOBALS_CSS_PATH}...")

    if not GLOBALS_CSS_PATH.exists():
        print(f"❌ Error: {GLOBALS_CSS_PATH} does not exist")
        sys.exit(1)

    content = GLOBALS_CSS_PATH.read_text()

    new_token_block   = _build_token_block(tokens)
    new_utility_block = _build_utility_block(tokens)

    token_pattern = re.compile(
        r"/\* ─── Custom spacing tokens.*?" + re.escape(_TOKEN_BLOCK_END),
        re.DOTALL,
    )
    utility_pattern = re.compile(
        r"/\* ─── Custom spacing utilities.*?" + re.escape(_UTILITY_BLOCK_END),
        re.DOTALL,
    )

    if token_pattern.search(content):
        content = token_pattern.sub(new_token_block, content)
    else:
        # First run: insert both blocks after the closing brace of @theme inline.
        # The utility block follows immediately after the token block.
        content = re.sub(
            r"(^@theme\s+inline\s*\{.*?^\})",
            lambda m: m.group(0) + "\n\n" + new_token_block + "\n\n" + new_utility_block,
            content,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        GLOBALS_CSS_PATH.write_text(content)
        override_count = len([t for t in tokens if t["mobile_rem"] is not None and t["mobile_rem"] != t["desktop_rem"]])
        print(f"✅ Inserted globals.css ({len(tokens)} tokens, {override_count} with sm overrides)")
        return

    if utility_pattern.search(content):
        content = utility_pattern.sub(new_utility_block, content)
    else:
        # Token block existed but utility block is missing — append after token block.
        content = token_pattern.sub(new_token_block + "\n\n" + new_utility_block, content)

    GLOBALS_CSS_PATH.write_text(content)
    override_count = len([t for t in tokens if t["mobile_rem"] is not None and t["mobile_rem"] != t["desktop_rem"]])
    print(f"✅ Updated globals.css ({len(tokens)} tokens, {override_count} with sm overrides)")


# ==========================================
# MAIN
# ==========================================

def main():
    print("🚀 Starting Custom Spacing Sync Pipeline\n")

    api_token = os.getenv("FIGMA_TOKEN")
    if not api_token:
        print("❌ Error: FIGMA_TOKEN environment variable not set")
        print("   Create a .env.local file with: FIGMA_TOKEN=your_token_here")
        sys.exit(1)

    try:
        desktop, mobile = extract_figma_spacing(api_token)
        tokens = build_tokens(desktop, mobile)
        write_spacing_md(tokens)
        update_globals_css(tokens)

        print("\n✨ Spacing sync completed successfully!")

    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Figma API Error: {e}")
        print(f"   Response: {e.response.text}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
