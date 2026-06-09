#!/usr/bin/env python3
"""
YAML frontmatter fixer v4: Wrap ALL pros/cons list items in single quotes.
Multi-line items get joined before quoting. URLs stay unquoted.
This is the most reliable approach — YAML single-quoted scalars can't wrap.
"""
import os, re

REVIEWS = "src/content/reviews"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

fixed = 0

for fname in sorted(os.listdir(REVIEWS)):
    if not fname.endswith(".md"):
        continue
    filepath = os.path.join(REVIEWS, fname)
    with open(filepath) as f:
        content = f.read()
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        continue
    
    fm = parts[1]
    body = parts[2]
    fm_lines = fm.split("\n")
    new_lines = []
    in_section = None
    buf = ""  # buffer for multi-line list items
    changed = False
    buf_started = False
    
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        stripped = line.strip()
        
        # Detect section headers
        if re.match(r'^(pros|cons|related|affiliateLinks):', stripped):
            new_lines.append(line)
            in_section = stripped.split(":")[0]
            buf_started = False
            i += 1
            continue
        
        # Exit section
        if in_section and re.match(r'^[a-z]', stripped) and ":" in stripped and not stripped.startswith("- "):
            if buf_started:
                # Flush buffer as quoted item
                val = buf.strip()
                if ":" in val and not val.startswith(("http://", "https://")):
                    new_lines.append(f"  - '{val}'")
                else:
                    new_lines.append(f"  - '{val}'")
                buf = ""
                buf_started = False
            in_section = None
        
        if in_section in ("pros", "cons"):
            # Handle list items
            if stripped.startswith("- "):
                # Flush previous buffer
                if buf_started:
                    val = buf.strip()
                    new_lines.append(f"  - '{val}'")
                    buf = ""
                    buf_started = False
                # Start new buffer
                buf = stripped[2:]
                buf_started = True
            elif buf_started and stripped and not stripped.startswith("- "):
                # Continuation line
                buf += " " + stripped
            elif buf_started and not stripped:
                # Empty line - flush buffer
                val = buf.strip()
                new_lines.append(f"  - '{val}'")
                new_lines.append("")
                buf = ""
                buf_started = False
            else:
                new_lines.append(line)
        elif in_section in ("related", "affiliateLinks"):
            if stripped.startswith("- "):
                val = stripped[2:]
                if ":" in val and not val.startswith(("http://", "https://")):
                    val = f"'{val}'"
                new_lines.append(f"  - {val}")
            else:
                new_lines.append(line)
        else:
            # Fix unquoted description/title
            m = re.match(r'^(description|title):\s*(.+)$', stripped)
            if m:
                key = m.group(1)
                val = m.group(2).strip()
                if ":" in val and not (val.startswith("'") or val.startswith('"')):
                    new_lines.append(f"{key}: '{val}'")
                    changed = True
                    i += 1
                    continue
            new_lines.append(line)
        
        i += 1
    
    # Flush final buffer
    if buf_started and buf:
        val = buf.strip()
        new_lines.append(f"  - '{val}'")
    
    # Add draft: false if missing
    has_draft = any(re.match(r'^draft:', l.strip()) for l in new_lines)
    if not has_draft:
        for j in range(len(new_lines) - 1, -1, -1):
            if new_lines[j].strip():
                new_lines.insert(j + 1, "draft: false")
                break
    
    new_fm = "\n".join(new_lines)
    if new_fm != fm:
        changed = True
    
    if changed:
        fixed += 1
        new_content = parts[0] + "---" + new_fm + "---" + body
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"Fixed {fixed} files")

# Now verify with Python YAML parser
import yaml
errors = 0
for fname in sorted(os.listdir(REVIEWS)):
    if not fname.endswith(".md"):
        continue
    filepath = os.path.join(REVIEWS, fname)
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        continue
    try:
        yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"  STILL BROKEN: {fname}: {e}")
        errors += 1

if errors == 0:
    print("ALL FRONTMATTER VALID!")
else:
    print(f"{errors} files still broken")
