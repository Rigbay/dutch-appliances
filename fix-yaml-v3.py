#!/usr/bin/env python3
"""
Comprehensive frontmatter fixer:
1. Normalize pros/cons/related/affiliateLinks list indentation to 2 spaces
2. Quote any list items containing colons (except URLs)
3. Quote unquoted description/title fields containing colons
4. Add missing 'draft: false' fields
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
    new_fm_lines = []
    in_list_section = None  # 'pros', 'cons', 'related', 'affiliateLinks', or None
    changed = False
    
    i = 0
    while i < len(fm_lines):
        line = fm_lines[i]
        stripped = line.strip()
        
        # Detect entering/exiting list sections
        list_match = re.match(r'^(pros|cons|related|affiliateLinks):', stripped)
        if list_match:
            new_fm_lines.append(line)
            in_list_section = list_match.group(1)
            i += 1
            continue
        
        # Exit list section when hitting another top-level key
        if in_list_section and re.match(r'^[a-z]', stripped) and not stripped.startswith("- "):
            if ":" in stripped and not stripped.startswith("#"):
                in_list_section = None
        
        if in_list_section and stripped.startswith("- "):
            val = stripped[2:]
            # Quote non-URL items containing colons
            if ":" in val and not val.startswith(("http://", "https://")):
                if not (val.startswith("'") or val.startswith('"')):
                    val = f"'{val}'"
            
            new_fm_lines.append(f"  - {val}")
            if line != f"  - {val}":
                changed = True
        elif stripped == "" and in_list_section:
            new_fm_lines.append("")
        elif in_list_section and not stripped:
            new_fm_lines.append("")
        else:
            # Not in list section - check description/title for unquoted colons
            desc_match = re.match(r'^(description|title):\s*(.+)$', stripped)
            if desc_match and not stripped.startswith("#"):
                key = desc_match.group(1)
                val = desc_match.group(2).strip()
                if ":" in val and not (val.startswith("'") or val.startswith('"')):
                    new_fm_lines.append(f"{key}: '{val}'")
                    changed = True
                    i += 1
                    continue
            
            new_fm_lines.append(line)
        
        if in_list_section and not stripped.startswith("- ") and stripped != "":
            # Check if this is a new top-level key
            if ":" in stripped:
                in_list_section = None
        
        i += 1
    
    # Add draft: false if missing
    has_draft = any(re.match(r'^draft:', l.strip()) for l in new_fm_lines)
    if not has_draft:
        # Find the last line before closing --- (related section end or second-to-last)
        for j in range(len(new_fm_lines) - 1, -1, -1):
            if new_fm_lines[j].strip():
                new_fm_lines.insert(j + 1, "draft: false")
                break
        changed = True
    
    if changed:
        fixed += 1
        new_fm = "\n".join(new_fm_lines)
        new_content = parts[0] + "---" + new_fm + "---" + body
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"Fixed {fixed} files")
