#!/usr/bin/env python3
"""Fix KiesKeuken articles with generic top-level affiliateLinks.

Many old articles have 'affiliateLinks:' (top-level frontmatter) pointing to
generic category searches like amazon.nl/s?k=keuken. These earn nothing because
they're not product-specific.

The per-product 'affiliateLink' entries under each product[] are already correct
(product-specific search URLs). We just need to replace the top-level generic
links with each product's specific search URL.
"""
import re, yaml, sys
from pathlib import Path

REVIEWS = Path("/workspace/kieskeuken/src/content/reviews")

GENERIC_SEARCH = re.compile(
    r'amazon\.nl/s\?k=(keuken|tuin|schoonmaak|huishoudelijk|algemeen|apparaten|beste\+?(tuin|keuken|apparaten))',
    re.IGNORECASE
)

def fix_article(filepath: Path) -> bool:
    text = filepath.read_text()
    original = text
    
    # Check if there are any top-level generic links
    # (not per-product affiliateLink which are indented)
    
    # Extract frontmatter
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return False
    
    fm_text = m.group(1)
    body = text[m.end():]
    
    # Check top-level affiliateLinks for generic entries
    # YAML list items start with `- ` at column 0 (top-level)
    if not GENERIC_SEARCH.search(fm_text):
        return False
    
    # Parse full frontmatter with Python yaml
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        print(f"  {filepath.name}: yaml parse error: {e}")
        return False
    
    if not isinstance(fm, dict):
        return False
    
    # Get product-specific search URLs from per-product entries
    products = fm.get('products', [])
    if not products or not isinstance(products, list):
        print(f"  {filepath.name}: no products array to derive links from")
        return False
    
    product_links = []
    for p in products:
        if isinstance(p, dict):
            link = p.get('affiliateLink', '')
            if link and 'amazon.nl/' in link:
                product_links.append(link)
    
    if not product_links:
        print(f"  {filepath.name}: no per-product affiliateLink entries found")
        return False
    
    # Now rebuild the frontmatter YAML, replacing top-level affiliateLinks
    # First, remove the old affiliateLinks section from fm
    if 'affiliateLinks' in fm:
        del fm['affiliateLinks']
    
    # Add the new product-specific links
    fm['affiliateLinks'] = product_links[:len(product_links)]
    
    # Rebuild frontmatter
    # Use a custom representer for consistent output
    class Literal(str): pass
    
    def str_representer(dumper, data):
        for delim in ['\n', ':', '{', '}', '[', ']', ',', '?', '!', '"', "'", '@', '`', '|', '>', '*', '&', '%', '#']:
            if delim in data:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    yaml.add_representer(str, str_representer)
    
    new_fm = yaml.dump(fm, default_flow_style=False, allow_unicode=True, sort_keys=False, width=80)
    new_text = f"---\n{new_fm}---\n{body}"
    
    # Some cleanup: remove extra whitespace, ensure consistent formatting
    new_text = new_text.replace('\n\n---', '\n---')
    
    filepath.write_text(new_text)
    print(f"  ✓ {filepath.name}: replaced {len(product_links)} generic links with product-specific search URLs")
    return True

# Run
fixed = []
skipped = []
for f in sorted(REVIEWS.glob("*.md")):
    try:
        if fix_article(f):
            fixed.append(f.name)
    except Exception as e:
        skipped.append((f.name, str(e)))
        print(f"  ✗ {f.name}: ERROR: {e}")

print(f"\nFixed: {len(fixed)} articles")
for name in fixed:
    print(f"  + {name}")
if skipped:
    print(f"\nErrors: {len(skipped)}")
    for name, err in skipped[:5]:
        print(f"  ✗ {name}: {err}")

if not fixed:
    print("No articles fixed.")
else:
    print("\nNext: git add + git commit on KiesKeuken repo.")