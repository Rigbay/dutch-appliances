#!/usr/bin/env python3
"""Find and fix unquoted YAML list items with colons that break Astro schema."""
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
    
    changed = False
    lines = content.split("\n")
    in_list = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Track if we're in a YAML list (pros:, cons:, related:)
        if re.match(r'^(pros|cons|related|affiliateLinks):', stripped):
            in_list = True
            continue
        elif in_list and re.match(r'^\w+:', stripped):
            in_list = False
        
        if in_list and stripped.startswith("- ") and ":" in stripped:
            # Check if it's already quoted
            val = stripped[2:]  # content after "- "
            if val.startswith("'") or val.startswith('"'):
                continue
            # Wrap in single quotes
            lines[i] = f'- \'{val}\''
            changed = True
            print(f"  FIX: {fname}:{i+1}: {stripped[:60]}...")
    
    if changed:
        fixed += 1
        with open(filepath, "w") as f:
            f.write("\n".join(lines))

print(f"\nFixed {fixed} files")
