#!/usr/bin/env python3
"""
Font Family Sync Pipeline

Extracts font family tokens from a Figma design system table, then surgically
updates app/layout.tsx (next/font/google imports + instances + className spread)
and app/globals.css (@theme inline font entries).

Usage:
    python scripts/sync-fonts.py

Environment:
    FIGMA_TOKEN: Personal access token from Figma account settings
"""

import os
import sys
import re
import requests
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

# ==========================================
# CONFIGURATION
# ==========================================

FIGMA_FILE_ID = "0QoJnYRxO36C5snGqt79VD"
FONTS_NODE_ID = "21275-33"

SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
MONOREPO_ROOT = REPO_ROOT.parent.parent

load_dotenv(REPO_ROOT / ".env.local")

LAYOUT_TSX_PATH = MONOREPO_ROOT / "wizcamp-lms" / "app" / "layout.tsx"
GLOBALS_CSS_PATH = MONOREPO_ROOT / "wizcamp-lms" / "app" / "globals.css"
FONTS_MD_PATH = REPO_ROOT / "guidelines" / "foundations" / "fonts.md"

FIGMA_API_BASE = "https://api.figma.com/v1"

BUILTIN_FONTS = {
    "Georgia", "Arial", "Times New Roman", "Courier New",
    "Verdana", "Trebuchet MS", "Impact", "Comic Sans MS",
}

BUILTIN_CSS_STACKS = {
    "Georgia":         "Georgia, serif",
    "Arial":           "Arial, sans-serif",
    "Times New Roman": '"Times New Roman", serif',
    "Courier New":     '"Courier New", monospace',
    "Verdana":         "Verdana, sans-serif",
    "Trebuchet MS":    '"Trebuchet MS", sans-serif',
    "Impact":          "Impact, sans-serif",
    "Comic Sans MS":   '"Comic Sans MS", cursive',
}

# ==========================================
# HELPERS (copied from sync-figma-tokens.py — keep in sync)
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
        var_name = get_var_name_fn(token["name"])
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

def to_camel_case(s: str) -> str:
    parts = s.replace("_", " ").split()
    return parts[0].lower() + "".join(p.capitalize() for p in parts[1:])


def transform_tokens(tokens: List[Dict]) -> List[Dict]:
    print(f"🔄 Transforming {len(tokens)} tokens...")

    google_count = 0
    builtin_count = 0

    for token in tokens:
        family = token["font_family"]
        is_builtin = family in BUILTIN_FONTS
        token["is_builtin"] = is_builtin

        if is_builtin:
            token["css_value"] = BUILTIN_CSS_STACKS.get(family, family)
            builtin_count += 1
        else:
            next_font_name = family.replace(" ", "_")
            var_name = "--font-" + family.lower().replace(" ", "-")
            js_var_name = to_camel_case(next_font_name)
            token["next_font_name"] = next_font_name
            token["var_name"] = var_name
            token["js_var_name"] = js_var_name
            token["css_value"] = f"var({var_name})"
            google_count += 1

    print(f"✅ Transform complete ({google_count} google, {builtin_count} builtin)")
    return tokens

# ==========================================
# PHASE 1: EXTRACT FROM FIGMA
# ==========================================

def extract_figma_fonts(api_token: str) -> List[Dict]:
    url = f"{FIGMA_API_BASE}/files/{FIGMA_FILE_ID}/nodes?ids={FONTS_NODE_ID}"
    headers = {"X-Figma-Token": api_token}

    print(f"📡 Fetching node {FONTS_NODE_ID} from Figma...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    node_key = FONTS_NODE_ID.replace("-", ":")
    table_node = data["nodes"][node_key]["document"]

    results = []

    for child in table_node.get("children", []):
        if child.get("type") != "FRAME":
            continue
        if child.get("name") == "Table Header":
            continue
        if not child.get("name", "").startswith("Table Row"):
            continue

        cells = child.get("children", [])
        if len(cells) < 3:
            continue

        token_name = None
        for node in walk_tree(cells[0]):
            if node.get("type") == "TEXT":
                token_name = node.get("characters", "").strip()
                break

        # cells[1] = Value (CSS token value), cells[2] = Used for, cells[3] = Sample
        token_value = None
        for node in walk_tree(cells[1]):
            if node.get("type") == "TEXT":
                token_value = node.get("characters", "").strip()
                break

        used_for = None
        for node in walk_tree(cells[2]):
            if node.get("type") == "TEXT":
                used_for = node.get("characters", "").strip()
                break

        font_family = None
        for node in walk_tree(cells[3]):
            if node.get("type") == "TEXT":
                style = node.get("style", {})
                font_family = style.get("fontFamily", "").strip()
                break

        if token_name and font_family:
            kind = "builtin" if font_family in BUILTIN_FONTS else "google"
            results.append({
                "name": token_name,
                "token_value": token_value or "",
                "used_for": used_for or "",
                "font_family": font_family,
            })
            print(f"  ✓ {token_name}: {font_family} ({kind})")
        else:
            print(f"  ⚠️  Skipped row — missing token name or font family")

    print(f"✅ Extracted {len(results)} font tokens")
    return results

# ==========================================
# PHASE 3: WRITE fonts.md
# ==========================================

def write_fonts_md(tokens: List[Dict]) -> None:
    """Write font tokens table to fonts.md."""
    print(f"📝 Writing {FONTS_MD_PATH}...")

    lines = [
        "# Fonts",
        "",
        "Auto-generated by `sync-fonts.py`. Do not edit manually.",
        "",
        "| Style Name | Value | Used For |",
        "| :--- | :--- | :--- |",
    ]

    for token in tokens:
        lines.append(f"| {token['name']} | {token['token_value']} | {token['used_for']} |")

    FONTS_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    FONTS_MD_PATH.write_text("\n".join(lines) + "\n")
    print(f"✅ Wrote fonts.md ({len(tokens)} tokens)")


# ==========================================
# PHASE 4a: UPDATE layout.tsx
# ==========================================

# Matches any `const Foo = Bar({ ... });` block (font instances only — PascalCase callee)
FONT_INSTANCE_RE = re.compile(
    r"^const (\w+)\s*=\s*([A-Z]\w+)\(\{[\s\S]*?\}\);",
    re.MULTILINE,
)


def update_layout_tsx(tokens: List[Dict]) -> None:
    print(f"📝 Updating {LAYOUT_TSX_PATH}...")

    if not LAYOUT_TSX_PATH.exists():
        print(f"❌ Error: {LAYOUT_TSX_PATH} does not exist")
        sys.exit(1)

    content = LAYOUT_TSX_PATH.read_text()

    google_tokens = [t for t in tokens if not t["is_builtin"]]

    # Deduplicate by font_family for import + instance generation
    seen_families: Dict[str, Dict] = {}
    unique_google = []
    for t in google_tokens:
        if t["font_family"] not in seen_families:
            seen_families[t["font_family"]] = t
            unique_google.append(t)

    unique_google_sorted = sorted(unique_google, key=lambda t: t["next_font_name"])
    active_js_vars = {t["js_var_name"] for t in unique_google_sorted}

    instance_template = (
        "const {js_var} = {next_font_name}({{\n"
        "  variable: '{var_name}',\n"
        "  subsets: ['latin'],\n"
        "}});"
    )

    # ── 3a-1: Import line ────────────────────────────────────────────────────
    import_names = ", ".join(t["next_font_name"] for t in unique_google_sorted)
    new_import = f"import {{ {import_names} }} from 'next/font/google';"

    content = re.sub(
        r"^import\s*\{[^}]*\}\s*from\s*'next/font/google'.*$",
        new_import,
        content,
        flags=re.MULTILINE,
    )

    # ── 3a-2: Upsert active font instances ───────────────────────────────────
    for t in unique_google_sorted:
        new_block = instance_template.format(
            js_var=t["js_var_name"],
            next_font_name=t["next_font_name"],
            var_name=t["var_name"],
        )
        existing = re.compile(
            r"const " + re.escape(t["js_var_name"]) + r"\s*=\s*\w+\(\{[\s\S]*?\}\);",
            re.MULTILINE,
        )
        if existing.search(content):
            content = existing.sub(new_block, content)
        else:
            content = content.replace(
                "export const metadata",
                new_block + "\n\nexport const metadata",
                1,
            )

    # ── 3a-3: Comment out stale font instances ───────────────────────────────
    def comment_if_stale(match: re.Match) -> str:
        js_var = match.group(1)
        if js_var in active_js_vars:
            return match.group(0)
        stale_count[0] += 1
        print(f"  ⚠️  Commenting out stale font instance: {js_var}")
        return "\n".join("// " + line for line in match.group(0).split("\n"))

    stale_count = [0]
    content = FONT_INSTANCE_RE.sub(comment_if_stale, content)

    # ── 3a-4: className spread on <html> ─────────────────────────────────────
    variable_refs = " ".join(f"${{{t['js_var_name']}.variable}}" for t in unique_google_sorted)

    def rebuild_classname(match: re.Match) -> str:
        existing = match.group(1)
        stripped = re.sub(r"\$\{[a-zA-Z]+\.variable\}\s*", "", existing).strip()
        return f"className={{`{variable_refs} {stripped}`}}"

    content = re.sub(r"className=\{`([^`]*)`\}", rebuild_classname, content)

    LAYOUT_TSX_PATH.write_text(content)
    print(f"✅ Updated layout.tsx ({len(unique_google)} active, {stale_count[0]} commented out)")


# ==========================================
# PHASE 4b: UPDATE globals.css
# ==========================================

def update_globals_css(tokens: List[Dict]) -> None:
    print(f"📝 Updating {GLOBALS_CSS_PATH}...")

    if not GLOBALS_CSS_PATH.exists():
        print(f"❌ Error: {GLOBALS_CSS_PATH} does not exist")
        sys.exit(1)

    content = GLOBALS_CSS_PATH.read_text()
    lines = content.split("\n")

    lines = update_css_block(
        lines=lines,
        block_regex=r"^@theme\s+inline\s*\{",
        get_var_name_fn=lambda name: f"--{name}",
        get_new_line_fn=lambda t: f"  --{t['name']}: {t['css_value']};",
        tokens=tokens,
    )

    GLOBALS_CSS_PATH.write_text("\n".join(lines))
    print(f"✅ Updated globals.css ({len(tokens)} font tokens)")


# ==========================================
# MAIN
# ==========================================

def main():
    print("🚀 Starting Font Sync Pipeline\n")

    api_token = os.getenv("FIGMA_TOKEN")
    if not api_token:
        print("❌ Error: FIGMA_TOKEN environment variable not set")
        print("   Create a .env.local file with: FIGMA_TOKEN=your_token_here")
        sys.exit(1)

    try:
        tokens = extract_figma_fonts(api_token)
        tokens = transform_tokens(tokens)
        write_fonts_md(tokens)
        update_layout_tsx(tokens)
        update_globals_css(tokens)

        print("\n✨ Font sync completed successfully!")

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
