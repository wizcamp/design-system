#!/usr/bin/env python3
"""
Figma Design Token ETL Pipeline

Extracts color tokens from a Figma design file table, converts them to OKLCH,
and updates design system documentation and CSS files.

Usage:
    python scripts/sync-figma-tokens.py

Environment:
    FIGMA_TOKEN: Personal access token from Figma account settings
"""

import os
import sys
import json
import re
import math
import requests
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv

# ==========================================
# CONFIGURATION
# ==========================================

FIGMA_FILE_ID = "0QoJnYRxO36C5snGqt79VD"
BASE_COLORS_NODE_ID = "21275-9"

# File paths relative to script location
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
MONOREPO_ROOT = REPO_ROOT.parent.parent

load_dotenv(REPO_ROOT / ".env.local")

TOKENS_MD_PATH = REPO_ROOT / "guidelines" / "tokens.md"
COLORS_MD_PATH = REPO_ROOT / "guidelines" / "colors.md"
#GLOBALS_CSS_PATH = REPO_ROOT / "styles" / "globals.css"
GLOBALS_CSS_PATH = MONOREPO_ROOT / "wizcamp-lms" / "app" / "globals.css"

# API Configuration
FIGMA_API_BASE = "https://api.figma.com/v1"

# ==========================================
# COLOR CONVERSION (DO NOT MODIFY)
# ==========================================

def parse_color(input_str: str) -> Tuple[float, float, float]:
    """Parse hex color to RGB (0-1 range)."""
    input_str = input_str.strip()
    if input_str.startswith('#'):
        hex_str = input_str[1:]
        if len(hex_str) == 3:
            hex_str = ''.join([c*2 for c in hex_str])
        if len(hex_str) == 6:
            return tuple(int(hex_str[i:i+2], 16) / 255 for i in (0, 2, 4))
    raise ValueError(f"Cannot parse color: {input_str}")

def rgb_to_linear(c: float) -> float:
    """Convert sRGB to linear RGB."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def oklab_to_oklch(L: float, a: float, b: float) -> Tuple[float, float, float]:
    """Convert OKLab to OKLCH."""
    c = math.sqrt(a * a + b * b)
    h = math.degrees(math.atan2(b, a)) % 360 if c > 1e-10 else 0
    return L, c, h

def rgb_to_oklch(r: float, g: float, b: float) -> Tuple[float, float, float]:
    """Convert RGB (0-1 range) to OKLCH."""
    r, g, b = rgb_to_linear(r), rgb_to_linear(g), rgb_to_linear(b)
    L = (0.412221469470763 * r + 0.5363325372617348 * g + 0.0514459932675022 * b) ** (1/3)
    M = (0.2119034958178252 * r + 0.6806995506452344 * g + 0.1073969535369406 * b) ** (1/3)
    S = (0.0883024591900564 * r + 0.2817188391361215 * g + 0.6299787016738222 * b) ** (1/3)
    l = 0.210454268309314 * L + 0.7936177747023054 * M - 0.0040720430116193 * S
    a = 1.9779985324311684 * L - 2.4285922420485799 * M + 0.450593709617411 * S
    b = 0.0259040424655478 * L + 0.7827717124575296 * M - 0.8086757549230774 * S
    return oklab_to_oklch(l, a, b)

def format_number(num: float) -> str:
    """Format number for OKLCH output."""
    if abs(num) < 1e-10:
        return "0"
    if abs(num - round(num)) < 1e-10:
        return f"{round(num):.4f}"
    return f"{num:.4f}"

def hex_to_oklch(hex_color: str, opacity: Optional[float] = None) -> str:
    """
    Convert hex color to OKLCH string with optional opacity.
    
    Args:
        hex_color: Hex color string (e.g., "#f59e0b")
        opacity: Optional opacity value (0-1 range)
    
    Returns:
        OKLCH string (e.g., "oklch(0.7686 0.1647 70.0804)" or "oklch(0.7686 0.1647 70.0804 / 80%)")
    """
    r, g, b = parse_color(hex_color)
    l, c, h = rgb_to_oklch(r, g, b)
    
    base = f"oklch({format_number(l)} {format_number(c)} {format_number(h)})"
    
    if opacity is not None and opacity < 1.0:
        # Convert to percentage and format
        opacity_pct = round(opacity * 100)
        return f"{base} / {opacity_pct}%"
    
    return base

def rgb_obj_to_hex(color_obj: Dict) -> Tuple[str, Optional[float]]:
    """
    Convert Figma RGB object to hex string and extract opacity.
    
    Args:
        color_obj: Figma color object with r, g, b, a fields (0-1 range)
    
    Returns:
        Tuple of (hex_string, opacity) where opacity is None if fully opaque
    """
    r = int(color_obj['r'] * 255)
    g = int(color_obj['g'] * 255)
    b = int(color_obj['b'] * 255)
    a = color_obj.get('a', 1.0)
    
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    opacity = a if a < 1.0 else None
    
    return hex_color, opacity

# ==========================================
# PHASE 1: EXTRACT FROM FIGMA
# ==========================================

def walk_tree(node: Dict):
    """Recursively yield all nodes in the tree."""
    yield node
    for child in node.get('children', []):
        yield from walk_tree(child)

def extract_figma_tokens(api_token: str) -> List[Dict[str, any]]:
    """
    Extract color tokens from Figma base colors table.
    
    Returns:
        List of {name: str, light_hex: str, light_opacity: float?, dark_hex: str, dark_opacity: float?}
    """
    url = f"{FIGMA_API_BASE}/files/{FIGMA_FILE_ID}/nodes?ids={BASE_COLORS_NODE_ID}"
    headers = {"X-Figma-Token": api_token}
    
    print(f"📡 Fetching node {BASE_COLORS_NODE_ID} from Figma...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    node_key = BASE_COLORS_NODE_ID.replace('-', ':')
    table_node = data['nodes'][node_key]['document']
    
    results = []
    
    # Find all "Table Row" frames (skip header)
    for child in table_node.get('children', []):
        if child.get('type') != 'FRAME':
            continue
        if child.get('name') == 'Table Header':
            continue
        if not child.get('name', '').startswith('Table Row'):
            continue
        
        cells = child.get('children', [])
        if len(cells) < 3:
            continue
        
        # Extract variable name from first cell
        var_name = None
        for node in walk_tree(cells[0]):
            if node.get('type') == 'TEXT':
                var_name = node.get('characters', '').strip()
                break
        
        # Extract light color from second cell
        light_rgb = None
        for node in walk_tree(cells[1]):
            if node.get('type') == 'RECTANGLE' and node.get('fills'):
                light_rgb = node['fills'][0]['color']
                break
        
        # Extract dark color from third cell
        dark_rgb = None
        for node in walk_tree(cells[2]):
            if node.get('type') == 'RECTANGLE' and node.get('fills'):
                dark_rgb = node['fills'][0]['color']
                break
        
        if var_name and light_rgb and dark_rgb:
            light_hex, light_opacity = rgb_obj_to_hex(light_rgb)
            dark_hex, dark_opacity = rgb_obj_to_hex(dark_rgb)
            
            token = {
                'name': var_name,
                'light_hex': light_hex,
                'dark_hex': dark_hex
            }
            
            if light_opacity is not None:
                token['light_opacity'] = light_opacity
            if dark_opacity is not None:
                token['dark_opacity'] = dark_opacity
            
            results.append(token)
            
            # Display with opacity if present
            light_display = f"{light_hex} ({int(light_opacity*100)}%)" if light_opacity else light_hex
            dark_display = f"{dark_hex} ({int(dark_opacity*100)}%)" if dark_opacity else dark_hex
            print(f"  ✓ {var_name}: {light_display} / {dark_display}")
    
    print(f"✅ Extracted {len(results)} tokens")
    return results

# ==========================================
# PHASE 2: TRANSFORM (HEX → OKLCH)
# ==========================================

def transform_tokens(tokens: List[Dict[str, any]]) -> List[Dict[str, any]]:
    """
    Convert hex colors to OKLCH format.
    
    Returns:
        List with added light_oklch and dark_oklch fields
    """
    print(f"🔄 Converting {len(tokens)} tokens to OKLCH...")
    
    for token in tokens:
        token['light_oklch'] = hex_to_oklch(
            token['light_hex'], 
            token.get('light_opacity')
        )
        token['dark_oklch'] = hex_to_oklch(
            token['dark_hex'], 
            token.get('dark_opacity')
        )
    
    print("✅ Conversion complete")
    return tokens

# ==========================================
# PHASE 3: LOAD INTO DOCUMENTATION
# ==========================================

def update_colors_md(tokens: List[Dict[str, any]]) -> None:
    """Write Base Colors table to colors.md."""
    print(f"📝 Writing {COLORS_MD_PATH}...")
    
    lines = [
        "# Base Colors",
        "",
        "Auto-generated by `sync-figma-tokens.py`. Do not edit manually.",
        "",
        "| Variable Name | Light Hex | Light OKLCH | Dark Hex | Dark OKLCH |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for token in sorted(tokens, key=lambda t: t['name']):
        light_hex_display = token['light_hex']
        if token.get('light_opacity'):
            light_hex_display = f"{light_hex_display} @ {int(token['light_opacity'] * 100)}%"
        
        dark_hex_display = token['dark_hex']
        if token.get('dark_opacity'):
            dark_hex_display = f"{dark_hex_display} @ {int(token['dark_opacity'] * 100)}%"
        
        lines.append(
            f"| {token['name']} | {light_hex_display} | {token['light_oklch']} | "
            f"{dark_hex_display} | {token['dark_oklch']} |"
        )
    
    COLORS_MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    COLORS_MD_PATH.write_text("\n".join(lines) + "\n")
    print(f"✅ Wrote colors.md ({len(tokens)} tokens)")

def update_globals_css(tokens: List[Dict[str, any]]) -> None:
    """Update globals.css with token values."""
    print(f"📝 Updating {GLOBALS_CSS_PATH}...")
    
    if not GLOBALS_CSS_PATH.exists():
        print(f"❌ Error: {GLOBALS_CSS_PATH} does not exist")
        sys.exit(1)
    
    content = GLOBALS_CSS_PATH.read_text()
    lines = content.split('\n')
    
    def update_css_block(lines, block_regex, get_var_name_fn, get_new_line_fn, tokens):
        """Surgically update a CSS block."""
        start_idx = -1
        end_idx = -1
        
        # Find block start
        for i, line in enumerate(lines):
            if re.search(block_regex, line):
                start_idx = i
                break
        
        if start_idx == -1:
            print(f"⚠️  Warning: Could not find block matching {block_regex}")
            return lines
        
        # Find block end
        brace_count = 0
        for i in range(start_idx, len(lines)):
            brace_count += lines[i].count('{')
            brace_count -= lines[i].count('}')
            if brace_count == 0 and '{' in ''.join(lines[start_idx:i+1]):
                end_idx = i
                break
        
        if end_idx == -1:
            print(f"⚠️  Warning: Could not find closing brace for {block_regex}")
            return lines
        
        block_lines = lines[start_idx:end_idx+1]
        
        # Update each token
        for token in tokens:
            var_name = get_var_name_fn(token['name'])
            line_pattern = re.compile(r'^\s*' + re.escape(var_name) + r'\s*:')
            new_line = get_new_line_fn(token)
            
            # Find all occurrences
            match_indices = [j for j, bline in enumerate(block_lines) if line_pattern.match(bline)]
            
            if match_indices:
                # Overwrite first, delete duplicates
                block_lines[match_indices[0]] = new_line
                for idx in reversed(match_indices[1:]):
                    block_lines.pop(idx)
            else:
                # Insert before closing brace
                for j in range(len(block_lines)-1, -1, -1):
                    if '}' in block_lines[j]:
                        block_lines.insert(j, new_line)
                        break
        
        return lines[:start_idx] + block_lines + lines[end_idx+1:]
    
    # Update :root
    lines = update_css_block(
        lines=lines,
        block_regex=r'^:root\s*\{',
        get_var_name_fn=lambda name: f"--{name}",
        get_new_line_fn=lambda t: f"  --{t['name']}: {t['light_oklch']};",
        tokens=tokens
    )
    
    # Update .dark
    lines = update_css_block(
        lines=lines,
        block_regex=r'^\.dark\s*\{',
        get_var_name_fn=lambda name: f"--{name}",
        get_new_line_fn=lambda t: f"  --{t['name']}: {t['dark_oklch']};",
        tokens=tokens
    )
    
    # Update @theme inline
    lines = update_css_block(
        lines=lines,
        block_regex=r'^@theme\s+inline\s*\{',
        get_var_name_fn=lambda name: f"--color-{name}",
        get_new_line_fn=lambda t: f"  --color-{t['name']}: var(--{t['name']});",
        tokens=tokens
    )
    
    GLOBALS_CSS_PATH.write_text('\n'.join(lines))
    print(f"✅ Updated globals.css ({len(tokens)} tokens)")

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    """Run the complete ETL pipeline."""
    print("🚀 Starting Figma Design Token ETL Pipeline\n")
    
    # Load API token from environment
    api_token = os.getenv('FIGMA_TOKEN')
    if not api_token:
        print("❌ Error: FIGMA_TOKEN environment variable not set")
        print("   Create a .env.local file with: FIGMA_TOKEN=your_token_here")
        sys.exit(1)
    
    try:
        # Phase 1: Extract from Figma
        tokens = extract_figma_tokens(api_token)
        
        # Phase 2: Transform to OKLCH
        tokens = transform_tokens(tokens)
        
        # Phase 3: Load into documentation
        update_colors_md(tokens)
        update_globals_css(tokens)
        
        print("\n✨ ETL pipeline completed successfully!")
        
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
