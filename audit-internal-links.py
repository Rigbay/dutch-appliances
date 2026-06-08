#!/usr/bin/env python3
"""Audit internal linking density: count how many times each article is linked from other articles."""
import os
import re
from collections import defaultdict

REVIEWS_DIR = "src/content/reviews"

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

# Build slug → title map
slug_to_title = {}
for fname in os.listdir(REVIEWS_DIR):
    if not fname.endswith(".md"):
        continue
    slug = fname.replace(".md", "")
    with open(os.path.join(REVIEWS_DIR, fname)) as f:
        content = f.read()
    # Extract title from frontmatter
    m = re.search(r"title:\s*'?([^'\n]+)'?", content)
    title = m.group(1).strip() if m else slug
    slug_to_title[slug] = title

# Count incoming links per slug
incoming = defaultdict(int)
linking = defaultdict(list)  # slug → list of slugs that link to it

for fname in os.listdir(REVIEWS_DIR):
    if not fname.endswith(".md"):
        continue
    source_slug = fname.replace(".md", "")
    with open(os.path.join(REVIEWS_DIR, fname)) as f:
        content = f.read()

    # Find all slug references in the content
    for target_slug in slug_to_title:
        if target_slug == source_slug:
            continue
        if target_slug in content:
            incoming[target_slug] += 1
            linking[target_slug].append(source_slug)

# Also count related: frontmatter entries
for fname in os.listdir(REVIEWS_DIR):
    if not fname.endswith(".md"):
        continue
    source_slug = fname.replace(".md", "")
    with open(os.path.join(REVIEWS_DIR, fname)) as f:
        content = f.read()
    # Extract related slugs from frontmatter
    fm_match = re.search(r"^---$(.*?)^---$", content, re.MULTILINE | re.DOTALL)
    if not fm_match:
        continue
    fm = fm_match.group(1)
    rel_match = re.search(r"^related:(.*?)(?:^\w+:|\Z)", fm, re.MULTILINE | re.DOTALL)
    if not rel_match:
        continue
    for line in rel_match.group(1).split("\n"):
        m = re.match(r"\s*-\s*(\S+)", line)
        if m:
            target = m.group(1)
            if target in slug_to_title and target != source_slug:
                incoming[target] += 1
                linking[target].append(source_slug)

# Categorize
orphans = []    # 0 incoming
thin = []       # 1-2 incoming
healthy = []    # 3+ incoming

for slug, count in sorted(incoming.items(), key=lambda x: x[1]):
    if count == 0:
        orphans.append(slug)
    elif count <= 2:
        thin.append(slug)
    else:
        healthy.append(slug)

print(f"=== Internal Linking Audit ===")
print(f"Total articles: {len(slug_to_title)}")
print(f"Orphans (0 incoming): {len(orphans)}")
print(f"Thin (1-2 incoming): {len(thin)}")
print(f"Healthy (3+ incoming): {len(healthy)}")
print()

if orphans:
    print("=== ORPHANS (0 incoming links) ===")
    for s in orphans:
        title = slug_to_title.get(s, s)
        # Truncate title for readability
        short = title[:80] + "…" if len(title) > 80 else title
        print(f"  {s}")
        print(f"    {short}")

if thin:
    print(f"\n=== THIN ({len(thin)} articles with 1-2 incoming) ===")
    for s in thin:
        title = slug_to_title.get(s, s)
        short = title[:80] + "…" if len(title) > 80 else title
        sources = linking.get(s, [])
        print(f"  {s} ({incoming[s]} incoming: {', '.join(sources[:3])})")
        print(f"    {short}")

# Show distribution
print(f"\n=== Distribution ===")
buckets = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, "6-10": 0, "11+": 0}
for slug, count in incoming.items():
    if count == 0:
        buckets[0] += 1
    elif count == 1:
        buckets[1] += 1
    elif count == 2:
        buckets[2] += 1
    elif count == 3:
        buckets[3] += 1
    elif count == 4:
        buckets[4] += 1
    elif count == 5:
        buckets[5] += 1
    elif 6 <= count <= 10:
        buckets["6-10"] += 1
    else:
        buckets["11+"] += 1

for k in [0, 1, 2, 3, 4, 5, "6-10", "11+"]:
    label = str(k)
    bar = "█" * buckets[k]
    print(f"  {label:>5}: {buckets[k]:3d} {bar}")
