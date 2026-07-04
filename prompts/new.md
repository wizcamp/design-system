**Role:** Automation Engineer.

**Objective:** Extract base colors tokens and their hex codes from Figma a design file, convert them to OKLCH, and write a markdown table with the results to the design system documentation.  

Using the Figma MCP - call the `get_variable_defs` tool for the following design: https://www.figma.com/design/0QoJnYRxO36C5snGqt79VD/06242026-LUMA?node-id=21275-9&m=dev.

Build a markdown table of the following structure and output it in the chat:

```markdown
| Variable Name | Light Hex | Light OKLCH | Dark Hex | Dark OKLCH |
| :--- | :--- | :--- | :--- | :--- |
| accent | #f59e0b | oklch(0.7686 0.1647 70.0804) | #4e4090 | oklch(0.4291 0.1270 287.8648) |
```

**Methodology**

- Only consider definitions that are colors (prefixed with color)
- row format: variable names minus the 'color/' prefix, light hex code, light hex code (OKLCH), dark hex code, dark hex code (OKLCH) 
- group names by light and dark values
- include compound names in the list like 'muted-foreground', not just single-word names
- convert each hex color using the provided Python function (rgb -> OKLCH); use the script as is only adjusting for your tool, e.g., removing main method
- include (do not strip) the format_number function for the conversion code
- do not modify the Python code unless you need for tooling purposes only
- sort table ascending by Variable name
- skip conversion errors

### RGB TO OKLCH Conversion Script

Execute this Python script locally for all color processing:

```python
import sys
import re
import math

HEX = '#FFFFFF' // <- The hex code you want to convert goes here

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

r, g, b = parse_color(HEX)
l, c, h = rgb_to_oklch(r, g, b)
print(f"oklch({format_number(l)} {format_number(c)} {format_number(h)})")
```