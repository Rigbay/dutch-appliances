#!/usr/bin/env python3
"""
Fix same-ASIN issue in KiesKeuken articles.
Replaces duplicated ASINs with product-name-search URLs.

Usage:
  python3 scripts/fix-same-asin.py --dry-run   (preview)
  python3 scripts/fix-same-asin.py --live       (write files)
"""

import os, re, sys, json

REVIEWS_DIR = os.path.expanduser("~/kieskeuken/src/content/reviews")
TAG = "kieskeukennl-21"

def get_asin(link):
    m = re.search(r'/dp/([A-Z0-9]{10,14})', link)
    return m.group(1) if m else None

def make_search_url(product_name):
    q = product_name.strip().strip('"').strip("'")
    q = re.sub(r'[()",:;!?]', '', q)
    q = re.sub(r'\s+', '+', q)
    return f"https://www.amazon.nl/s?k={q}&tag={TAG}"

def parse_products(text):
    """Extract product names and affiliateLinks from frontmatter products array."""
    lines = text.split('\n')
    products = []
    in_products = False
    current = {}
    
    for i, line in enumerate(lines):
        raw = line  # preserve for writing back
        # Detect products section start
        if raw.startswith('products:') and not in_products:
            in_products = True
            continue
        
        if not in_products:
            continue
        
        stripped = raw.strip()
        
        # Detect end: empty line, ---, or a top-level key (no indent after products area)
        indent = len(raw) - len(raw.lstrip())
        
        if stripped == '' and indent == 0:
            in_products = False
            continue
        if stripped.startswith('---'):
            in_products = False
            continue
        if indent == 0 and stripped and not stripped.startswith('- ') and not stripped.startswith('#'):
            # Probably a new top-level key
            in_products = False
            continue
        
        if stripped.startswith('- name:'):
            if current and 'name' in current:
                products.append(current)
            current = {'name': stripped.split('- name:', 1)[1].strip().strip('"').strip("'")}
        elif 'affiliateLink:' in stripped and current:
            link = stripped.split('affiliateLink:', 1)[1].strip().strip('"').strip("'")
            current['affiliateLink'] = link
            current['asin'] = get_asin(link)
    
    # Add last product
    if current and 'name' in current:
        products.append(current)
    
    return products

def fix_article(filepath, dry_run=True):
    basename = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        text = f.read()
    
    lines = text.split('\n')
    products = parse_products(text)
    
    if not products:
        return 0
    
    # Check if same-ASIN problem
    asins = [p.get('asin') for p in products if p.get('asin')]
    unique_asins = set(asins)
    
    if len(unique_asins) > 1:
        return 0  # already correct (different ASINs)
    
    if len(unique_asins) == 0:
        return 0  # no ASINs found to fix
    
    shared_asin = list(unique_asins)[0]
    
    # Also check top-level affiliateLinks list
    top_has_bad = False
    in_aff_list = False
    in_products_block = False
    changes = []
    
    changed_lines = set()
    
    # 1. Fix per-product affiliateLinks 
    for prod in products:
        name = prod['name']
        if prod.get('asin') == shared_asin:
            new_url = make_search_url(name)
            # Find this product in the file text and replace its affiliateLink
            # We need to match name + old link -> new link
            old_link_line = None
            for i, line in enumerate(lines):
                if i in changed_lines:
                    continue
                stripped = line.strip()
                # Match: the line has affiliateLink and the old ASIN
                if 'affiliateLink:' in stripped and shared_asin in stripped:
                    # Verify this is the right product by checking above lines
                    # Check if we passed this product's - name: line
                    above = '\n'.join(lines[max(0,i-10):i])
                    if name[:20] in above:
                        old_link_line = i
                        break
            
            if old_link_line is not None:
                lines[old_link_line] = re.sub(
                    r'(affiliateLink:\s*["\']?).*',
                    f'affiliateLink: {new_url}',
                    lines[old_link_line],
                    count=1
                )
                changed_lines.add(old_link_line)
                changes.append((basename, name[:30], shared_asin, "→ search URL"))
    
    # 2. Fix top-level affiliateLinks list (list items with the shared ASIN)
    for i, line in enumerate(lines):
        if i in changed_lines:
            continue
        stripped = line.strip()
        if stripped.startswith('- ') and shared_asin in stripped:
            # Top-level list item with bad ASIN
            # Replace with a general search URL for the article category
            category = 'kieskeuken'
            for j in range(max(0,i-20), i):
                cat_match = re.search(r'category:\s*(\w+)', lines[j])
                if cat_match:
                    category = cat_match.group(1)
                    break
            new_url = make_search_url(category)
            lines[i] = f"- {new_url}"
            changed_lines.add(i)
            changes.append((basename, f"top-level #{i+1}", shared_asin, "→ category search"))
    
    if not changes:
        return 0
    
    if dry_run:
        print(f"  🔴 {basename}: {len(products)} products ({len(unique_asins)} ASIN) → {len(changes)} fixes")
        return len(changes)
    else:
        new_text = '\n'.join(lines)
        with open(filepath, 'w') as f:
            f.write(new_text)
        print(f"  ✅ {basename}: {len(changes)} fixes applied")
        return len(changes)

def main():
    dry_run = '--dry-run' in sys.argv
    live = '--live' in sys.argv
    
    if dry_run and live:
        print("ERROR: Cannot use --dry-run and --live together")
        sys.exit(1)
    
    if not dry_run and not live:
        print("Usage: fix-same-asin.py [--dry-run | --live]")
        sys.exit(1)
    
    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"KiesKeuken Same-ASIN Fix ({mode})\n")
    
    total_articles = 0
    total_changes = 0
    
    for fname in sorted(os.listdir(REVIEWS_DIR)):
        if not fname.endswith('.md'):
            continue
        path = os.path.join(REVIEWS_DIR, fname)
        n = fix_article(path, dry_run=dry_run)
        if n > 0:
            total_articles += 1
            total_changes += n
    
    print(f"\nArticles fixed: {total_articles}")
    print(f"Total changes: {total_changes}")
    if dry_run:
        print("Run with --live to apply")

if __name__ == '__main__':
    main()