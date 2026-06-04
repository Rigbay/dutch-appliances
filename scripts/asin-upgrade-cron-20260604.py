#!/usr/bin/env python3
"""
Cron-run ASIN upgrade: find ASINs for search-link products via web_search,
apply matches to KiesKeuken articles.

Strategy (Jun 4, 15:50 CEST):
- Focus on products with specific model numbers first (highest match probability)
- Skip already-known ASINs and collision ASINs
- Process top-frequency products (multi-article reuse = highest ROI)
"""

import yaml
import re
import json
import glob
import sys
from collections import Counter, defaultdict
from pathlib import Path

REVIEWS_DIR = Path('src/content/reviews')
KNOWN_ASINS_FILE = Path('scripts/known-asins.json')
OUTPUT_FILE = Path('scripts/asin-progress-20260604.md')

def load_known_asins():
    if KNOWN_ASINS_FILE.exists():
        d = json.load(open(KNOWN_ASINS_FILE))
        known = d.get('known_asins', {})
        collisions = d.get('collisions', {})
        # Flatten collisions: all products using collision ASINs
        collision_products = set()
        for asin, products in collisions.items():
            for p in products:
                collision_products.add(p.lower().strip('*'))
        return known, collision_products
    return {}, set()

def extract_search_links():
    """
    Returns: dict of product_name -> list of (article_file, yaml_product_index)
    Only returns products with amazon.nl/s?k= links (not already upgraded).
    """
    results = defaultdict(list)
    for fpath in sorted(REVIEWS_DIR.glob('*.md')):
        content = fpath.read_text()
        parts = content.split('---')
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1])
        except:
            continue
        if not fm or 'products' not in fm:
            continue
        for i, p in enumerate(fm['products']):
            link = p.get('affiliateLink', '')
            if 'amazon.nl/s?k=' in link or 'amazon.nl/s?' in link:
                name = p.get('name', '').strip()
                results[name].append((str(fpath), i))
    return dict(results)

def has_model_number(name):
    """Check if product name contains a specific model number."""
    # Pattern: letters + numbers like HD9867/90, CSG656BS7, 5KSM175
    return bool(re.search(r'[A-Z]{2,}\d+[A-Z]?\d*', name)) or \
           bool(re.search(r'\d{3,}[A-Z]*[/\-][A-Z]?\d+', name))

def clean_name(name):
    """Normalize product name for comparison."""
    return name.lower().strip().replace('**', '').strip()

def main():
    known_asins, collision_products = load_known_asins()
    search_links = extract_search_links()
    
    # Normalize known ASINs
    known_normalized = {}
    for key, asin in known_asins.items():
        known_normalized[clean_name(key)] = asin
    
    # Find products with model numbers, sorted by frequency
    model_number_products = []
    for name, refs in search_links.items():
        cname = clean_name(name)
        if has_model_number(name) and len(refs) >= 1:
            # Skip known
            if cname in known_normalized:
                continue
            # Skip collision
            if cname in collision_products:
                continue
            model_number_products.append((name, len(refs), refs))
    
    # Sort by frequency desc
    model_number_products.sort(key=lambda x: -x[1])
    
    # Output candidate list for web_search
    lines = []
    lines.append("# ASIN Upgrade — Cron Run 2026-06-04 15:50 CEST\n")
    lines.append(f"## Status\n")
    lines.append(f"- Total search links: {sum(len(v) for v in search_links.values())}")
    lines.append(f"- Unique products: {len(search_links)}")
    lines.append(f"- Products with model numbers: {len(model_number_products)}")
    lines.append(f"- Already known (skip): {len(known_normalized)}")
    lines.append(f"- Collision products (skip): {len(collision_products)}")
    lines.append(f"- Candidates for lookup: {len(model_number_products)}\n")
    
    lines.append("## Top 50 Candidates (by article frequency)\n")
    lines.append("| # | Product | Articles | Model? |")
    lines.append("|---|---------|----------|--------|")
    for idx, (name, count, refs) in enumerate(model_number_products[:50], 1):
        model_tag = "✓" if has_model_number(name) else ""
        lines.append(f"| {idx} | `{name[:80]}` | {count} | {model_tag} |")
    
    # Output as a batch file for the web_search phase
    lines.append("\n## Batch Lookup List (for web_search)\n")
    lines.append("```")
    for name, count, refs in model_number_products[:50]:
        lines.append(f"site:amazon.nl \"{name[:100]}\"")
    lines.append("```")
    
    OUTPUT_FILE.write_text('\n'.join(lines) + '\n')
    
    # Also print to stdout for immediate consumption
    print(f"Found {len(model_number_products)} products with model numbers")
    print(f"Top 10:")
    for name, count, refs in model_number_products[:10]:
        articles = [r[0].replace('src/content/reviews/', '') for r in refs]
        print(f"  [{count}x] {name[:80]} → {', '.join(articles[:3])}")

if __name__ == '__main__':
    main()
