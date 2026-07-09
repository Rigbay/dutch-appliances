#!/usr/bin/env python3
"""Find high-value comparison gaps."""
import os, re
from pathlib import Path

reviews_dir = Path('src/content/reviews')
all_slugs = set()
vs_slugs = set()
non_vs = []

for f in sorted(reviews_dir.glob('*.md')):
    slug = f.stem
    all_slugs.add(slug)
    if '-vs-' in slug:
        vs_slugs.add(slug)
    else:
        content = f.read_text()
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else slug
        cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
        category = cat_match.group(1) if cat_match else 'keuken'
        non_vs.append((slug, title, category))

# Extract existing pair keys
existing_pairs = set()
for vs in vs_slugs:
    base = vs.replace('-2026', '')
    parts = base.split('-vs-')
    if len(parts) == 2:
        a, b = sorted([parts[0].strip(), parts[1].strip()])
        existing_pairs.add((a, b))

# High-value pair candidates
candidates = [
    ('beste-airfryer-2026', 'beste-friteuse-2026', 'keuken'),
    ('beste-espresso-apparaat-2026', 'beste-filterkoffiemachine-2026', 'keuken'),
    ('beste-magnetron-2026', 'beste-heteluchtoven-2026', 'keuken'),
    ('beste-slowcooker-2026', 'beste-snelkookpan-2026', 'keuken'),
    ('beste-broodmachine-2026', 'beste-broodrooster-2026', 'keuken'),
    ('beste-waterkoker-2026', 'beste-fluitketel-2026', 'keuken'),
    ('beste-keukenmachine-2026', 'beste-foodprocessor-2026', 'keuken'),
    ('beste-staafmixer-2026', 'beste-blender-2026', 'keuken'),
    ('beste-tosti-ijzer-2026', 'beste-broodrooster-2026', 'keuken'),
    ('beste-ijsmachine-2026', 'beste-diepvries-2026', 'keuken'),
    ('beste-stofzuiger-2026', 'beste-robotstofzuiger-2026', 'schoonmaken'),
    ('beste-stoomreiniger-2026', 'beste-hogedrukreiniger-2026', 'schoonmaken'),
    ('beste-dweilrobot-2026', 'beste-robotstofzuiger-2026', 'schoonmaken'),
    ('beste-wasmachine-2026', 'beste-wasdroger-2026', 'huishoudelijk'),
    ('beste-airconditioner-2026', 'beste-ventilator-2026', 'huishoudelijk'),
    ('beste-luchtreiniger-2026', 'beste-luchtbevochtiger-2026', 'huishoudelijk'),
    ('beste-strijkijzer-2026', 'beste-stoomgenerator-2026', 'huishoudelijk'),
    ('beste-vaatwasser-2026', 'beste-handafwas-2026', 'huishoudelijk'),
    ('beste-grasmaaier-2026', 'beste-robotgrasmaaier-2026', 'tuin'),
    ('beste-barbecue-2026', 'beste-elektrische-grill-2026', 'tuin'),
    ('beste-heggenschaar-2026', 'beste-bosmaaier-2026', 'tuin'),
    ('beste-hogedrukreiniger-2026', 'beste-tuinslang-2026', 'tuin'),
    ('beste-kettingzaag-2026', 'beste-cirkelzaag-2026', 'tuin'),
]

gaps = []
for a_slug, b_slug, cat in candidates:
    a_key = a_slug.replace('beste-', '').replace('-2026', '')
    b_key = b_slug.replace('beste-', '').replace('-2026', '')
    pair_key = tuple(sorted([a_key, b_key]))
    
    covered = False
    for ep in existing_pairs:
        if pair_key == ep:
            covered = True
            break
        if a_key in ep and b_key in ep:
            covered = True
            break
    
    if not covered:
        a_exists = a_slug in all_slugs
        b_exists = b_slug in all_slugs
        if a_exists and b_exists:
            gaps.append((a_slug, b_slug, cat, a_key, b_key))
            print(f'GAP: {a_key} vs {b_key} [{cat}]')
        else:
            missing = []
            if not a_exists: missing.append(a_slug)
            if not b_exists: missing.append(b_slug)
            print(f'SKIP: {a_key} vs {b_key} — missing: {missing}')

print(f'\nTotal viable gaps: {len(gaps)}')
