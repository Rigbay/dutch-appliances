#!/usr/bin/env python3
"""Regenerate comparisons.json from actual review files."""
import json, os, re
from pathlib import Path

reviews_dir = Path('src/content/reviews')
comparisons = []

for f in sorted(reviews_dir.glob('*.md')):
    slug = f.stem
    if '-vs-' not in slug:
        continue
    
    content = f.read_text()
    
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else slug.replace('-', ' ').title()
    
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    category = cat_match.group(1) if cat_match else 'keuken'
    
    rating_match = re.search(r'^rating:\s*([\d.]+)', content, re.MULTILINE)
    rating = float(rating_match.group(1)) if rating_match else 4.0
    
    price_match = re.search(r'^priceRange:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    price_range = price_match.group(1) if price_match else '€50-500'
    
    rt_match = re.search(r'^readingTime:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    reading_time = rt_match.group(1) if rt_match else '8 min'
    
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    description = desc_match.group(1) if desc_match else f'Vergelijk {title}. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21).'
    
    comparisons.append({
        'slug': slug,
        'title': title,
        'category': category,
        'rating': rating,
        'priceRange': price_range,
        'readingTime': reading_time,
        'description': description
    })

comparisons.sort(key=lambda x: x['rating'], reverse=True)

with open('src/data/comparisons.json', 'w') as f:
    json.dump(comparisons, f, indent=2, ensure_ascii=False)

print(f'Regenerated comparisons.json with {len(comparisons)} entries')
for c in comparisons[-5:]:
    print(f'  {c["slug"]} ({c["rating"]})')
