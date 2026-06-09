#!/usr/bin/env python3
"""Fix ALL YAML frontmatter using Python's yaml library for guaranteed correctness."""
import os, yaml, re

REVIEWS = "src/content/reviews"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

fixed = 0
errors = []

for fname in sorted(os.listdir(REVIEWS)):
    if not fname.endswith(".md"):
        continue
    filepath = os.path.join(REVIEWS, fname)
    with open(filepath) as f:
        content = f.read()
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        continue
    
    fm_text = parts[1]
    body = parts[2]
    
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError:
        # YAML is broken - we need raw text fixes
        errors.append(fname)
        continue
    
    if data is None:
        continue
    
    # Ensure draft is present
    if 'draft' not in data:
        data['draft'] = False
    
    # Quote description/title with colons if needed
    for field in ('description', 'title'):
        val = data.get(field, '')
        if isinstance(val, str) and ":" in val:
            # yaml.dump will handle quoting automatically when needed
            pass
    
    # Re-emit valid YAML
    new_fm = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)
    new_fm = new_fm.rstrip()
    
    if new_fm != fm_text:
        fixed += 1
        new_content = parts[0] + "---" + new_fm + "---" + body
        with open(filepath, "w") as f:
            f.write(new_content)

print(f"Round-trip fixed: {fixed}")
print(f"Hard-broken YAML (need manual): {len(errors)}")
for e in errors:
    print(f"  {e}")

# Now handle the hard-broken ones
if errors:
    print("\n--- Fixing hard-broken files ---")
    for fname in errors:
        filepath = os.path.join(REVIEWS, fname)
        with open(filepath) as f:
            content = f.read()
        
        parts = content.split("---", 2)
        fm_text = parts[1]
        body = parts[2]
        lines = fm_text.split("\n")
        
        # Strategy: join all multi-line list items
        new_lines = []
        in_list = False
        buf = ""
        
        for line in lines:
            stripped = line.strip()
            
            if re.match(r'^(pros|cons):', stripped):
                in_list = True
                new_lines.append(line)
                continue
            elif in_list and re.match(r'^[a-z]', stripped) and ":" in stripped and not stripped.startswith("-"):
                if buf:
                    new_lines.append(f"  - '{buf.strip()}'")
                    buf = ""
                new_lines.append(line)
                in_list = False
                continue
            elif in_list and not stripped:
                if buf:
                    new_lines.append(f"  - '{buf.strip()}'")
                    buf = ""
                new_lines.append("")
                continue
            elif in_list and stripped.startswith("- "):
                if buf:
                    new_lines.append(f"  - '{buf.strip()}'")
                    buf = ""
                buf = stripped[2:]
            elif in_list and buf:
                buf += " " + stripped
            else:
                new_lines.append(line)
        
        if buf:
            new_lines.append(f"  - '{buf.strip()}'")
        
        new_fm = "\n".join(new_lines)
        
        # Try parsing
        try:
            yaml.safe_load(new_fm)
            new_content = parts[0] + "---" + new_fm + "---" + body
            with open(filepath, "w") as f:
                f.write(new_content)
            print(f"  FIXED: {fname}")
        except yaml.YAMLError as e:
            print(f"  STILL BROKEN: {fname}: {e}")

# Final validation
print("\n--- Final validation ---")
broken = 0
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
    except yaml.YAMLError:
        broken += 1
        if broken <= 10:
            print(f"  BROKEN: {fname}")

if broken == 0:
    print("ALL FRONTMATTER VALID!")
else:
    print(f"{broken} files still broken")
