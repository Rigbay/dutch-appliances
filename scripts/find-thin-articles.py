#!/usr/bin/env python3
"""Find thin articles (<300 words body)."""
import re
from pathlib import Path

reviews_dir = Path('src/content/reviews')
thin = []
for f in sorted(reviews_dir.glob('*.md')):
    content = f.read_text()
    body = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    word_count = len(body.split())
    if word_count < 300:
        slug = f.stem
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else slug
        thin.append((slug, title, word_count))

print(f'Thin articles (<300 words): {len(thin)}')
for slug, title, wc in sorted(thin, key=lambda x: x[2]):
    print(f'  {wc:4d} words — {slug}')
