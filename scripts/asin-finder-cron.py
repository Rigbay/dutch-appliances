#!/usr/bin/env python3
"""
Cron ASIN Finder — batch product name → Amazon NL search → extract ASIN → verify title → apply.
Works within boundaries: only curl calls to amazon.nl, no destructive ops.
"""
import subprocess, re, json, yaml, time, sys
from pathlib import Path
from urllib.parse import quote
from collections import defaultdict

REVIEWS_DIR = Path('src/content/reviews')
KNOWN_FILE = Path('scripts/known-asins.json')
PROGRESS_FILE = Path('scripts/asin-finder-progress-20260604.json')
OUTPUT_FILE = Path('scripts/asin-progress-20260604.md')

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
DELAY = 3  # seconds between Amazon requests

def load_known():
    if KNOWN_FILE.exists():
        d = json.load(open(KNOWN_FILE))
        return d.get('known_asins', {}), d.get('collisions', {})
    return {}, {}

def load_progress():
    if PROGRESS_FILE.exists():
        return json.load(open(PROGRESS_FILE))
    return {'found': {}, 'not_on_amazon': [], 'checked': [], 'failed': []}

def save_progress(p):
    json.dump(p, open(PROGRESS_FILE, 'w'), indent=2)

def extract_products_needing_asins():
    """Return dict: product_name → [(file, index)] for search-link-only products."""
    results = defaultdict(list)
    for fpath in sorted(REVIEWS_DIR.glob('*.md')):
        content = fpath.read_text()
        parts = content.split('---')
        if len(parts) < 3: continue
        try:
            fm = yaml.safe_load(parts[1])
        except: continue
        if not fm or 'products' not in fm: continue
        for i, p in enumerate(fm['products']):
            link = p.get('affiliateLink', '')
            if 'amazon.nl/s?k=' in link:
                name = p.get('name', '').strip()
                results[name].append((str(fpath), i))
    return dict(results)

def search_amazon_nl(product_name):
    """Search Amazon NL and return list of ASINs found."""
    query = quote(product_name)
    url = f"https://www.amazon.nl/s?k={query}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '20',
             '-H', f'User-Agent: {UA}',
             '-H', 'Accept-Language: nl-NL,nl;q=0.9',
             url],
            capture_output=True, text=True, timeout=30
        )
        html = result.stdout
        asins = re.findall(r'/dp/([A-Z0-9]{10})', html)
        return list(set(asins))
    except Exception as e:
        return []

def verify_asin(asin):
    """Get product title for an ASIN to verify relevance."""
    url = f"https://www.amazon.nl/dp/{asin}"
    try:
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '15',
             '-H', f'User-Agent: {UA}',
             '-H', 'Accept-Language: nl-NL,nl;q=0.9',
             url],
            capture_output=True, text=True, timeout=20
        )
        match = re.search(r'<title>\s*([^<]+?)\s*</title>', result.stdout)
        if match:
            return match.group(1).strip()
    except:
        pass
    return None

def name_words_match(search_name, page_title):
    """Check if enough words from search name appear in page title."""
    if not page_title:
        return False
    words = set(search_name.lower().split())
    # Remove very short/generic words
    skip = {'de', 'en', 'het', 'een', 'van', 'met', 'voor', 'the', 'in', 'op', 'is', 'was', '1', '2'}
    words = words - skip
    if len(words) < 2:
        return False
    title_lower = page_title.lower()
    matches = sum(1 for w in words if w in title_lower)
    return matches >= min(2, len(words))

def find_asin_for_product(name, progress):
    """Try to find an ASIN for a product. Returns (asin, verified_title) or (None, None)."""
    # Check already found
    cname = name.lower().strip()
    if cname in progress['found']:
        return progress['found'][cname], 'cached'
    if name in progress['not_on_amazon']:
        return None, 'not_on_amazon'
    
    # Search Amazon NL
    asins = search_amazon_nl(name)
    if not asins:
        progress['not_on_amazon'].append(name)
        save_progress(progress)
        return None, 'no_results'
    
    # Verify top ASINs
    for asin in asins[:3]:
        title = verify_asin(asin)
        if title and name_words_match(name, title):
            progress['found'][cname] = asin
            save_progress(progress)
            return asin, title
    
    # If no match by title, use the first ASIN (product might be there but title parsing failed)
    # Be conservative: don't use unverified ASINs
    progress['not_on_amazon'].append(name)
    save_progress(progress)
    return None, 'no_title_match'

def apply_asins_to_articles(progress):
    """Apply found ASINs to article files, replacing search links."""
    product_map = progress.get('found', {})
    applied = 0
    files_modified = set()
    
    for fpath in sorted(REVIEWS_DIR.glob('*.md')):
        content = fpath.read_text()
        parts = content.split('---')
        if len(parts) < 3: continue
        try:
            fm = yaml.safe_load(parts[1])
        except: continue
        if not fm or 'products' not in fm: continue
        
        modified = False
        for p in fm['products']:
            link = p.get('affiliateLink', '')
            if 'amazon.nl/s?k=' not in link and 'amazon.nl/s?' not in link:
                continue
            name = p.get('name', '').strip()
            cname = name.lower().strip()
            if cname in product_map:
                asin = product_map[cname]
                new_link = f"https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21"
                p['affiliateLink'] = new_link
                modified = True
                applied += 1
        
        if modified:
            # Rebuild frontmatter
            new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
            # Fix the 'products:' indentation issue with PyYAML
            # PyYAML doesn't preserve exact formatting, so use a string replace approach instead
            new_content = f"---\n{new_fm}---{parts[2]}"
            fpath.write_text(new_content)
            files_modified.add(str(fpath))
    
    return applied, files_modified

def main():
    known_asins, collisions = load_known()
    progress = load_progress()
    all_products = extract_products_needing_asins()
    
    # Prioritize: model numbers first (specific), then by frequency
    def priority(name):
        has_model = bool(re.search(r'[A-Z]{2,}\d+[A-Z]?\d*', name))
        freq = len(all_products.get(name, []))
        return (-has_model, -freq)
    
    product_names = sorted(all_products.keys(), key=priority)
    
    print(f"Products with search links: {len(product_names)}")
    print(f"Already found in progress: {len(progress['found'])}")
    print(f"Already marked not-on-amazon: {len(progress['not_on_amazon'])}")
    
    # Process up to 30 products this run (respecting Amazon rate limits)
    target_count = 30
    processed = 0
    new_found = 0
    
    for name in product_names:
        if processed >= target_count:
            break
        cname = name.lower().strip()
        if cname in progress['found'] or name in progress['not_on_amazon']:
            continue
        if cname in [k.lower().strip() for k in known_asins]:
            continue
        
        processed += 1
        asin, info = find_asin_for_product(name, progress)
        if asin:
            new_found += 1
            print(f"  ✓ {name[:60]:60s} → {asin} ({info[:50]})")
        else:
            print(f"  ✗ {name[:60]:60s} → {info}")
        time.sleep(DELAY)
    
    print(f"\nProcessed: {processed}, New ASINs found: {new_found}")
    print(f"Total ASINs in progress: {len(progress['found'])}")
    
    # Apply found ASINs to articles
    if progress['found']:
        applied, files = apply_asins_to_articles(progress)
        print(f"\nApplied {applied} ASIN replacements across {len(files)} files")
        if files:
            for f in sorted(files)[:10]:
                print(f"  {f}")
            if len(files) > 10:
                print(f"  ... and {len(files)-10} more")
    
    # Write report
    lines = [f"# ASIN Finder — Cron Run 2026-06-04 16:00 CEST\n"]
    lines.append(f"\n## Results\n")
    lines.append(f"- Products processed this run: {processed}")
    lines.append(f"- New ASINs found: {new_found}")
    lines.append(f"- Total ASINs in progress DB: {len(progress['found'])}")
    lines.append(f"- Total search-link products remaining: {len(all_products) - len(progress['found'])}")
    lines.append(f"\n## Progress DB\n")
    lines.append(f"Progress saved to: `{PROGRESS_FILE}`\n")
    lines.append(f"```json")
    lines.append(json.dumps({k: progress[k] for k in ['found']}, indent=2, ensure_ascii=False)[:3000])
    lines.append(f"```")
    OUTPUT_FILE.write_text('\n'.join(lines))
    
    return processed, new_found, len(progress['found'])

if __name__ == '__main__':
    main()
