#!/usr/bin/env python3
"""Apply manually verified ASINs from web_search results to KiesKeuken articles."""
import yaml, re, json
from pathlib import Path

REVIEWS_DIR = Path('src/content/reviews')

# Manually verified ASINs from today's web_search results:
NEW_ASINS = {
    'roborock s8 maxv ultra': 'B0CRV7F37B',
    'dreame l20 ultra': 'B0CC236CLT',
}

def apply():
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
            name = p.get('name', '').strip().lower()
            for key, asin in NEW_ASINS.items():
                if key in name:
                    p['affiliateLink'] = f"https://www.amazon.nl/dp/{asin}?tag=kieskeukennl-21"
                    modified = True
                    applied += 1
                    print(f"  ✓ {fpath.name}: {p.get('name','')} → {asin}")
                    break
        
        if modified:
            new_fm = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{new_fm}---{parts[2]}"
            fpath.write_text(new_content)
            files_modified.add(str(fpath))
    
    return applied, files_modified

if __name__ == '__main__':
    n, files = apply()
    print(f"\nApplied {n} replacements across {len(files)} files")
    for f in sorted(files):
        print(f"  {f}")
