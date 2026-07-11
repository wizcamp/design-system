#!/usr/bin/env python3
"""
Custom Spacing Sync Pipeline

Extracts semantic spacing tokens from two Figma design system tables (Desktop
and Mobile), merges them into a unified token set, and updates:
  - guidelines/foundations/custom-spacing.md
  - wizcamp-lms/app/globals.css  (@theme inline block)

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

# Suffixes stripped before token registration — axis is applied at the utility level.
STRIP_SUFFIXES = ["-x", "-y"]

# ==========================================
# HELPERS (copied from sync-fonts.py — keep in sync)
# ==========================================

def walk_tree(node: Dict):
    """Recursively yield all nodes in the tree."""
    yield node
    for child in node.get("children", []):
        yield from walk_tree(child)


def update_css_block(lines, block_regex, get_var_name_fn, get_new_line_fn, tokens):
    """Surgically update a CSS block."""
    start_idx = -1
    end_idx = -1

    for i, line in enumerate(lines):
        if re.search(block_regex, line):
            start_idx = i
            break

    if start_idx == -1:
        print(f"⚠️  Warning: Could not find block matching {block_regex}")
        return lines

    brace_count = 0
    for i in range(start_idx, len(lines)):
        brace_count += lines[i].count("{")
        brace_count -= lines[i].count("}")
        if brace_count == 0 and "{" in "".join(lines[start_idx : i + 1]):
            end_idx = i
            break

    if end_idx == -1:
        print(f"⚠️  Warning: Could not find closing brace for {block_regex}")
        return lines

    block_lines = lines[start_idx : end_idx + 1]

    for token in tokens:
        var_name = get_var_name_fn(token["css_name"])
        line_pattern = re.compile(r"^\s*" + re.escape(var_name) + r"\s*:")
        new_line = get_new_line_fn(token)

        match_indices = [j for j, bline in enumerate(block_lines) if line_pattern.match(bline)]

        if match_indices:
            block_lines[match_indices[0]] = new_line
            for idx in reversed(match_indices[1:]):
                block_lines.pop(idx)
        else:
            for j in range(len(block_lines) - 1, -1, -1):
                if "}" in block_lines[j]:
                    block_lines.insert(j, new_line)
                    break

    return lines[:start_idx] + block_lines + lines[end_idx + 1 :]

# ==========================================
# TRANSFORM HELPERS
# ==========================================

def px_to_rem(px: int) -> str:
    """Convert integer pixel value to rem string (base 16px)."""
    rem = px / 16
    # Format: drop trailing zeros but keep up to 4 decimal places
    formatted = f"{rem:.4f}".rstrip("0").rstrip(".")
    return f"{formatted}rem"


def strip_axis_suffix(name: str) -> str:
    """Strip -x or -y axis suffixes from a token name."""
    for suffix in STRIP_SUFFIXES:
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return name

# ==========================================
# PHASE 1: EXTRACT FROM FIGMA
# ==========================================

def extract_table(api_token: str, node_id: str, label: str) -> Dict[str, int]:
    """
    Extract token name → pixel value pairs from a Figma spacing table node.

    Returns a dict keyed by the raw Figma token name (before suffix stripping).
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

        # Column 1: token name (TEXT node)
        token_name: Optional[str] = None
        for node in walk_tree(cells[0]):
            if node.get("type") == "TEXT":
                token_name = node.get("characters", "").strip()
                break

        # Column 2: pixel value as string (TEXT node)
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
    mobile = extract_table(api_token, MOBILE_NODE_ID, "Mobile")
    return desktop, mobile

# ==========================================
# PHASE 2: TRANSFORM
# ==========================================

def build_tokens(desktop: Dict[str, int], mobile: Dict[str, int]) -> List[Dict]:
    """
    Merge Desktop and Mobile tables into a unified token list.

    - Strip -x / -y axis suffixes from token names.
    - Deduplicate: if two raw names collapse to the same base name, the first
      encountered wins (Desktop table order is authoritative).
    - Desktop value is used as the canonical CSS value registered in @theme inline.
    """
    print("🔄 Building unified token list...")

    seen: Dict[str, bool] = {}
    tokens: List[Dict] = []

    for raw_name, desktop_px in desktop.items():
        base_name = strip_axis_suffix(raw_name)

        if base_name in seen:
            print(f"  ⚠️  Duplicate after suffix strip: '{raw_name}' → '{base_name}' (skipped)")
            continue
        seen[base_name] = True

        mobile_px = mobile.get(raw_name)

        tokens.append({
            "raw_name": raw_name,
            "base_name": base_name,
            "css_name": f"spacing-{base_name}",
            "desktop_px": desktop_px,
            "desktop_rem": px_to_rem(desktop_px),
            "mobile_px": mobile_px,
            "mobile_rem": px_to_rem(mobile_px) if mobile_px is not None else None,
        })
        mobile_display = f"{mobile_px}px → {px_to_rem(mobile_px)}" if mobile_px is not None else "—"
        print(f"  ✓ {base_name}: desktop={desktop_px}px → {px_to_rem(desktop_px)}, mobile={mobile_display}")

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
        "| Token | CSS variable | Desktop (px → rem) | Mobile (px → rem) |",
        "| :--- | :--- | :--- | :--- |",
    ]

    for t in tokens:
        mobile_col = (
            f"{t['mobile_px']}px → {t['mobile_rem']}"
            if t["mobile_px"] is not None
            else "—"
        )
        lines.append(
            f"| `{t['base_name']}` | `--{t['css_name']}` "
            f"| {t['desktop_px']}px → {t['desktop_rem']} "
            f"| {mobile_col} |"
        )

    SPACING_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPACING_MD_PATH.write_text("\n".join(lines) + "\n")
    print(f"✅ Wrote custom-spacing.md ({len(tokens)} tokens)")

# Sentinel comment that brackets the mobile override block in globals.css.
_MOBILE_BLOCK_START = "/* ─── Custom spacing — mobile overrides"
_MOBILE_BLOCK_END_MARKER = "/* end custom spacing mobile overrides */"


# ==========================================
# PHASE 4: UPDATE globals.css
# ==========================================

def _build_mobile_override_block(tokens: List[Dict]) -> str:
    """Render the @media mobile override block for tokens where desktop ≠ mobile."""
    differing = [t for t in tokens if t["mobile_rem"] is not None and t["mobile_rem"] != t["desktop_rem"]]
    if not differing:
        return ""

    inner = "\n".join(f"    --{t['css_name']}: {t['mobile_rem']};" for t in differing)
    return (
        "/* ─── Custom spacing — mobile overrides ──────────────────────────────────────────\n"
        "   Tailwind v4 resolves --spacing-* utilities via var() at render time, so\n"
        "   overriding the custom properties on :root inside a @media block is\n"
        "   sufficient — no extra utility classes needed in markup. @theme cannot be\n"
        "   nested inside @media in Tailwind v4. Threshold matches Tailwind's built-in\n"
        "   `sm` breakpoint (640px) — the same point the codebase already uses for\n"
        "   gutter changes (sm:px-6, sm:px-8). Only tokens that differ between Desktop\n"
        "   and Mobile are listed. */\n"
        "@media (max-width: 639px) {\n"
        "  :root {\n"
        f"{inner}\n"
        "  }\n"
        "}\n"
        f"{_MOBILE_BLOCK_END_MARKER}"
    )


def update_globals_css(tokens: List[Dict]) -> None:
    print(f"📝 Updating {GLOBALS_CSS_PATH}...")

    if not GLOBALS_CSS_PATH.exists():
        print(f"❌ Error: {GLOBALS_CSS_PATH} does not exist")
        sys.exit(1)

    content = GLOBALS_CSS_PATH.read_text()
    lines = content.split("\n")

    # 1. Upsert desktop values into @theme inline
    lines = update_css_block(
        lines=lines,
        block_regex=r"^@theme\s+inline\s*\{",
        get_var_name_fn=lambda css_name: f"--{css_name}",
        get_new_line_fn=lambda t: f"  --{t['css_name']}: {t['desktop_rem']};",
        tokens=tokens,
    )

    # 2. Replace existing mobile override block, or insert one after @theme inline
    new_block = _build_mobile_override_block(tokens)
    joined = "\n".join(lines)

    # Remove any existing block (between sentinel comment and end marker)
    existing_pattern = re.compile(
        r"\n/\* ─── Custom spacing — mobile overrides.*?" + re.escape(_MOBILE_BLOCK_END_MARKER),
        re.DOTALL,
    )
    joined = existing_pattern.sub("", joined)

    if new_block:
        # Insert after the closing brace of @theme inline
        joined = re.sub(
            r"(^@theme\s+inline\s*\{[^}]*\})",
            lambda m: m.group(0) + "\n\n" + new_block,
            joined,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )

    GLOBALS_CSS_PATH.write_text(joined)
    mobile_count = len([t for t in tokens if t["mobile_rem"] is not None and t["mobile_rem"] != t["desktop_rem"]])
    print(f"✅ Updated globals.css ({len(tokens)} desktop tokens, {mobile_count} mobile overrides)")

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
