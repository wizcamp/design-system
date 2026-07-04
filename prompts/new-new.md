
**Role:** Automation Engineer.

**Objective:** Extract color tokens and their hex codes from a Figma design file, converting them to OKLCH, and formatting them as a markdown table.

Using the Figma MCP - call the `get_variable_defs` tool for the following design: https://www.figma.com/design/0QoJnYRxO36C5snGqt79VD/06242026-LUMA?node-id=21275-9&m=dev.

Run the provided Python code to generate the markdown table. DO NOT implement your own algorithm.  Use the provided code adjusting the `color_defs` variable only.

Include conversion errors in the table

Using the Filesystem MCP server, write the markdown to `/Users/bobleeswagger/workspace/wizcamp/design-system/guidelines/colors.md`

## Markdown table format

```markdown
| Variable Name | Light Hex | Light OKLCH | Dark Hex | Dark OKLCH |
| :--- | :--- | :--- | :--- | :--- |
| accent | #f59e0b | oklch(0.7686 0.1647 70.0804) | #4e4090 | oklch(0.4291 0.1270 287.8648) |
```

## Example color definitions from `get_variable_defs`
```json
{"colors/accent-light":"#f59e0b","colors/accent-dark":"#4e4090","colors/accent-foreground-light":"#000000","colors/accent-foreground-dark":"#ffffff","colors/background-light":"#f7f9f3","colors/background-dark":"#14111f","colors/border-light":"#2d30291f","colors/border-dark":"#dce4d21f","colors/card-light":"#ffffff","colors/card-dark":"#3d3070","colors/card-foreground-light":"#2d3029","colors/card-foreground-dark":"#eef3e8","colors/destructive-light":"#e11d48","colors/destructive-dark":"#fb4d6d","colors/destructive-foreground-light":"#fff1f2","colors/destructive-foreground-dark":"#ffe4e8","colors/foreground-light":"#341e63","colors/foreground-dark":"#eef3e8","colors/input-light":"#737373","colors/input-dark":"#ffffff","colors/muted-light":"#f0f0f0","colors/muted-dark":"#2e2250","colors/muted-foreground-light":"#6b7269","colors/muted-foreground-dark":"#b8c4b4","colors/popover-light":"#e5ebe0","colors/popover-dark":"#3d3070","colors/popover-foreground-light":"#000000","colors/popover-foreground-dark":"#ffffff","colors/primary-light":"#6318e1","colors/primary-dark":"#b588ff","colors/primary-foreground-light":"#ffffff","colors/primary-foreground-dark":"#000000","colors/ring-light":"#a5b4fc","colors/ring-dark":"#818cf8","colors/secondary-light":"#f59e0b","colors/secondary-dark":"#1f0d45","colors/secondary-foreground-light":"#6b7269","colors/secondary-foreground-dark":"#b8c4b4","colors/chart-1-light":"#711cff","colors/chart-1-dark":"#8740ff","colors/chart-2-light":"#01e7e4","colors/chart-2-dark":"#26ebe9","colors/chart-3-light":"#014ce4","colors/chart-3-dark":"#2666e9","colors/chart-4-light":"#aa45ff","colors/chart-4-dark":"#711cff","colors/chart-5-light":"#3c0e88","colors/chart-5-dark":"#6318e1","colors/sidebar-light":"#e1e7d9","colors/sidebar-dark":"#231c3d","colors/sidebar-foreground-light":"#2d3029","colors/sidebar-foreground-dark":"#ffffff","colors/sidebar-primary-light":"#6674d6","colors/sidebar-primary-dark":"#96a0ea","colors/sidebar-primary-foreground-light":"#ffffff","colors/sidebar-primary-foreground-dark":"#ffffff","colors/sidebar-accent-light":"#6b7269","colors/sidebar-accent-dark":"#372d65","colors/sidebar-accent-foreground-light":"#ffffff","colors/sidebar-accent-foreground-dark":"#eef3e8","colors/sidebar-border-light":"#c8d0c0","colors/sidebar-border-dark":"#2e244f","colors/sidebar-ring-light":"#96a0ea","colors/sidebar-ring-dark":"#6674d6"}
```

## Conversion code
```python
import json
import re
import math

# Color definitions from the `get_variable_defs` Figma tool
color_defs = '{}' 

# --- Functions provided by the user ---
def parse_color(input_str):
    input_str = input_str.strip()
    if input_str.startswith('#'):
        hex_str = input_str[1:]
        if len(hex_str) == 3:
            hex_str = ''.join([c*2 for c in hex_str])
        if len(hex_str) == 6:
            return tuple(int(hex_str[i:i+2], 16) / 255 for i in (0, 2, 4))
    m = re.match(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*\,\s*(\d+)\s*\)', input_str)
    if m:
        return tuple(int(x) / 255 for x in m.groups())
    raise ValueError(f"Cannot parse color: {input_str}")

def rgb_to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def oklab_to_oklch(L, a, b):
    c = math.sqrt(a * a + b * b)
    h = math.degrees(math.atan2(b, a)) % 360 if c > 1e-10 else 0
    return L, c, h

def rgb_to_oklch(r, g, b):
    r, g, b = rgb_to_linear(r), rgb_to_linear(g), rgb_to_linear(b)
    L = (0.412221469470763 * r + 0.5363325372617348 * g + 0.0514459932675022 * b) ** (1/3)
    M = (0.2119034958178252 * r + 0.6806995506452344 * g + 0.1073969535369406 * b) ** (1/3)
    S = (0.0883024591900564 * r + 0.2817188391361215 * g + 0.6299787016738222 * b) ** (1/3)
    l = 0.210454268309314 * L + 0.7936177747023054 * M - 0.0040720430116193 * S
    a = 1.9779985324311684 * L - 2.4285922420485799 * M + 0.450593709617411 * S
    b = 0.0259040424655478 * L + 0.7827717124575296 * M - 0.8086757549230774 * S
    return oklab_to_oklch(l, a, b)

def format_number(num):
    if abs(num) < 1e-10:
        return "0"
    if abs(num - round(num)) < 1e-10:
        return f"{round(num):.4f}"
    return f"{num:.4f}"

# --- Processing Logic ---

# 1. Group tokens by base name and variant (light/dark, foreground/background)
variables = {}
for key, hex_code in color_defs.items():
    if key.startswith("colors/"):
        # Extract the variable name from the key
        parts = key.split('/')
        base_name_with_variant = parts[1]
        
        # Use the full base name (e.g., 'accent-light', 'muted-foreground-light')
        # The requirement says "variable names minus the 'color/' prefix"
        # which means we should group 'accent-light' and 'accent-dark' under 'accent'
        # For simplicity and fidelity to the prompt's example, we'll create a grouping key.
        
        name_parts = base_name_with_variant.split('-')
        
        if len(name_parts) > 1 and name_parts[-1] in ('light', 'dark'):
            base_name = '-'.join(name_parts[:-1])
            variant = name_parts[-1]
            
            if base_name not in variables:
                variables[base_name] = {}
            
            variables[base_name][variant] = hex_code

# 2. Collect all unique variable names
all_variables = list(variables.keys())

conversion_results = []

# 3. Process each variable
for var_name in all_variables:
    # Check for pairs of light/dark variants
    light_hex = variables[var_name].get('light')
    dark_hex = variables[var_name].get('dark')
    
    # If a pair is found, process them
    if light_hex and dark_hex:
        
        # Function to run conversion for a single hex code
        def convert_hex(hex_code):
            try:
                # Execute the provided conversion logic
                r, g, b = parse_color(hex_code)
                l, c, h = rgb_to_oklch(r, g, b)
                return f"oklch({format_number(l)} {format_number(c)} {format_number(h)})"
            except Exception:
                return "Conversion Error"

        light_oklch = convert_hex(light_hex)
        dark_oklch = convert_hex(dark_hex)

        conversion_results.append({
            "Variable Name": var_name,
            "Light Hex": light_hex,
            "Light OKLCH": light_oklch,
            "Dark Hex": dark_hex,
            "Dark OKLCH": dark_oklch
        })

# 4. Sort results by Variable Name
conversion_results.sort(key=lambda x: x["Variable Name"])

# 5. Generate the markdown table
markdown_table = "| Variable Name | Light Hex | Light OKLCH | Dark Hex | Dark OKLCH |\n"
markdown_table += "| :--- | :--- | :--- | :--- | :--- |\n"

for result in conversion_results:
    markdown_table += f"| {result['Variable Name']} | {result['Light Hex']} | {result['Light OKLCH']} | {result['Dark Hex']} | {result['Dark OKLCH']} |\n"

print(markdown_table)
```