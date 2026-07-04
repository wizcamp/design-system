**Role:** Automation Engineer.

**Objective:** Extract design tokens from `tokens.md` and surgically inject them into `globals.css` by executing a Python script directly in your environment.

**Instructions:**
1. **DO NOT** attempt to save this script to a file. 
2. Execute the provided Python code directly using your Python interpreter/tooling. 
3. Ensure the file paths in the `TOKENS_FILE` and `CSS_FILE` variables match the target files in your workspace before executing.
4. Report the console output back to confirm the CSS file was successfully updated.

### Execute this Python Code:

```python
import os
import re

# ==========================================
# CONFIGURATION - VERIFY PATHS BEFORE RUNNING
# ==========================================
TOKENS_FILE = "/Users/bobleeswagger/workspace/wizcamp/design-system/guidelines/tokens.md"
CSS_FILE = "/Users/bobleeswagger/workspace/wizcamp-lms/app/globals.css"

def parse_tokens(filepath):
    """Extracts Variable Name, Light OKLCH, and Dark OKLCH from the markdown table."""
    if not os.path.exists(filepath):
        print(f"❌ Error: Tokens file not found at {filepath}")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if "### Base Colors" not in content:
        print("❌ Error: '### Base Colors' section not found in tokens.md")
        return []
    
    section = content.split("### Base Colors")[1].split("###")[0]
    
    tokens = []
    for line in section.strip().split('\n'):
        if line.strip().startswith('|') and not line.strip().startswith('| :---'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6 and parts[1].lower() != "variable name":
                tokens.append({
                    'name': parts[1],
                    'light': parts[3], 
                    'dark': parts[5]   
                })
                
    print(f"✅ Extracted {len(tokens)} tokens from tokens.md")
    return tokens

def update_css_block(lines, block_regex, get_var_name_fn, get_new_line_fn, tokens):
    """Surgically replaces lines using Regex to prevent double/duplicate entries."""
    start_idx = -1
    end_idx = -1
    
    # 1. Find block boundaries
    for i, line in enumerate(lines):
        if re.search(block_regex, line):
            start_idx = i
            break
            
    if start_idx == -1:
        print(f"⚠️ Warning: Could not find block matching {block_regex}")
        return lines

    brace_count = 0
    for i in range(start_idx, len(lines)):
        brace_count += lines[i].count('{')
        brace_count -= lines[i].count('}')
        if brace_count == 0 and '{' in ''.join(lines[start_idx:i+1]):
            end_idx = i
            break
            
    if end_idx == -1:
        print(f"⚠️ Warning: Could not find closing brace for {block_regex}")
        return lines

    block_lines = lines[start_idx:end_idx+1]
    
    # 2. Process each token
    for token in tokens:
        var_name = get_var_name_fn(token['name'])
        # Regex matches e.g. "  --accent:" or "  --accent :" regardless of whitespace
        line_pattern = re.compile(r'^\s*' + re.escape(var_name) + r'\s*:')
        new_line = get_new_line_fn(token)
        
        # Find all occurrences of this variable in the block
        match_indices = [j for j, bline in enumerate(block_lines) if line_pattern.match(bline)]
        
        if match_indices:
            # Overwrite the first occurrence
            block_lines[match_indices[0]] = new_line
            # Actively delete any duplicate/double lines further down in the section
            for idx in reversed(match_indices[1:]):
                block_lines.pop(idx)
        else:
            # Insert cleanly before the closing brace
            for j in range(len(block_lines)-1, -1, -1):
                if '}' in block_lines[j]:
                    block_lines.insert(j, new_line)
                    break

    return lines[:start_idx] + block_lines + lines[end_idx+1:]

def process_css(tokens):
    if not os.path.exists(CSS_FILE):
        print(f"❌ Error: CSS file not found at {CSS_FILE}")
        return

    with open(CSS_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    original_line_count = len(lines)

    # 1. Update :root { ... }
    lines = update_css_block(
        lines=lines,
        block_regex=r'^:root\s*\{',
        get_var_name_fn=lambda name: f"--{name}",
        get_new_line_fn=lambda t: f"  --{t['name']}: {t['light']};",
        tokens=tokens
    )

    # 2. Update .dark { ... }
    lines = update_css_block(
        lines=lines,
        block_regex=r'^\.dark\s*\{',
        get_var_name_fn=lambda name: f"--{name}",
        get_new_line_fn=lambda t: f"  --{t['name']}: {t['dark']};",
        tokens=tokens
    )

    # 3. Update @theme inline { ... } (Strictly Maps to var())
    lines = update_css_block(
        lines=lines,
        block_regex=r'^@theme\s+inline\s*\{',
        get_var_name_fn=lambda name: f"--color-{name}",
        get_new_line_fn=lambda t: f"  --color-{t['name']}: var(--{t['name']});",
        tokens=tokens
    )

    with open(CSS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    print(f"✅ Successfully updated {CSS_FILE} (Lines: {original_line_count} -> {len(lines)})")

# Execute the process
extracted_tokens = parse_tokens(TOKENS_FILE)
if extracted_tokens:
    process_css(extracted_tokens)