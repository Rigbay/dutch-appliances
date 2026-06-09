#!/usr/bin/env python3
"""Fix all YAML frontmatter issues that break Astro builds."""
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
    
    fm_lines = parts[1].split("\n")
    in_list = False
    changed = False
    
    for i, line in enumerate(fm_lines):
        stripped = line.strip()
        
        # Fix unquoted description values with colons
        desc_match = re.match(r'^description:\s*(.+)$', stripped)
        if desc_match:
            val = desc_match.group(1).strip()
            if ":" in val and not (val.startswith("'") or val.startswith('"')):
                fm_lines[i] = f"description: '{val}'"
                changed = True
                continue
        
        # Track list context
        if re.match(r'^(pros|cons|related|affiliateLinks):', stripped):
            in_list = True
            continue
        elif in_list and re.match(r'^\w[\w-]*:', stripped):
            in_list = False
            continue
        elif in_list and stripped == "":
            continue
        
        if in_list and stripped.startswith("- ") and ":" in stripped:
            val = stripped[2:]
            if val.startswith(("http://", "https://")):
                continue
            if val.startswith("'") or val.startswith('"'):
                continue
            fm_lines[i] = f"  - '{val}'"
            changed = True
    
    if changed:
        fixed += 1
        new_fm = "\n".join(fm_lines)
        new_content = parts[0] + "---" + new_fm + "---" + parts[2]
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"Fixed {fixed} files")
