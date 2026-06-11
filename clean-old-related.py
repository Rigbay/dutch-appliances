#!/usr/bin/env python3
"""Remove older related-sections that predate the new cross-linking script.
Keeps only '## Gerelateerde koopgidsen' — the newest, properly formatted section."""

import os, re

REVIEWS = 'src/content/reviews'

# Patterns to remove (these are older, lower-quality sections)
OLD_SECTIONS = [
    # Matches "## Gerelateerde artikelen" and its content up to next ## or end
    r'\n\n## Gerelateerde artikelen\n.*?(?=\n\n##|\n---\n|\Z)',
    # Matches "## 📚 Lees ook" and its content
    r'\n\n## 📚 Lees ook\n.*?(?=\n\n##|\n---\n|\Z)',
    # Matches "## Vergelijk ook" and its content
    r'\n\n## Vergelijk ook\n.*?(?=\n\n##|\n---\n|\Z)',
]

count = 0
removed_sections = 0

for f in sorted(os.listdir(REVIEWS)):
    if not f.endswith('.md'): continue
    path = f'{REVIEWS}/{f}'
    with open(path) as fh:
        content = fh.read()
    
    original = content
    for pattern in OLD_SECTIONS:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # Also remove old inline "onze [...] gids" patterns that clutter body text
    # These are from previous linking scripts and are noisy
    # Pattern: "onze [beste X gids](/slug/)" repeated
    # We keep the new Gerelateerde koopgidsen section instead
    
    if content != original:
        removed = len(re.findall(r'\n\n## (?:Gerelateerde artikelen|📚 Lees ook|Vergelijk ook)', original))
        removed_sections += removed
        with open(path, 'w') as fh:
            fh.write(content)
        count += 1

print(f'Cleaned {count} files, removed {removed_sections} old sections')

# Also remove trailing blank lines before --- at end
count2 = 0
for f in sorted(os.listdir(REVIEWS)):
    if not f.endswith('.md'): continue
    path = f'{REVIEWS}/{f}'
    with open(path) as fh:
        content = fh.read()
    
    # Ensure no more than 1 blank line before final ---
    original = content
    content = re.sub(r'\n{3,}---\s*$', r'\n\n---\n', content)
    # Clean up multiple consecutive blank lines in body
    content = re.sub(r'\n{4,}', r'\n\n\n', content)
    
    if content != original:
        with open(path, 'w') as fh:
            fh.write(content)
        count2 += 1

print(f'Blank-line cleanup: {count2} files')
