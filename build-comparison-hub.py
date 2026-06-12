#!/usr/bin/env python3
"""Extract metadata from comparison articles and generate an Astro comparison hub page."""
import os, re, yaml, json

REVIEWS_DIR = "src/content/reviews"
OUT_PATH = "src/pages/vergelijken.astro"

# Category display names
CAT_LABELS = {
    "keuken": "Keukenapparaten",
    "schoonmaken": "Schoonmaken & Stofzuigen",
    "huishoudelijk": "Huishoudelijk & Wassen",
    "tuin": "Tuin & Buiten",
    "overig": "Overige Apparaten",
}

def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath) as f:
        content = f.read()
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except Exception:
        return None

def extract_verdict(filepath):
    """Extract a short verdict from the first few paragraphs after frontmatter."""
    with open(filepath) as f:
        content = f.read()
    parts = re.split(r'^---$', content, flags=re.MULTILINE)
    if len(parts) < 3:
        return ""
    body = '---'.join(parts[2:])
    # Find verdict/conclusie section or first meaningful paragraph
    # Try verdict/conclusie pattern first
    m = re.search(r'(?:Verdict|Conclusie|Samenvatting|Ons oordeel|Kortom|Bottom line)[:\s]*[\n\r]+(.+?)(?:\n\n|\n#|\n\*\*)', body, re.DOTALL | re.IGNORECASE)
    if m:
        verdict = re.sub(r'\*\*|__', '', m.group(1).strip())
        if len(verdict) > 15:
            return verdict[:200]
    # Fallback: first substantial paragraph after intro
    paragraphs = [p.strip() for p in body.split('\n\n') if len(p.strip()) > 60 and not p.startswith('#')]
    for p in paragraphs[:5]:
        cleaned = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', p)
        cleaned = re.sub(r'\*\*|__|#', '', cleaned).strip()
        if len(cleaned) > 40:
            return cleaned[:180]
    return ""

def main():
    comp_files = []
    for fname in os.listdir(REVIEWS_DIR):
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(REVIEWS_DIR, fname)
        fm = parse_frontmatter(fpath)
        if not fm:
            continue
        slug = fm.get('slug', fname.replace('.md', ''))
        title = fm.get('title', '')
        category = fm.get('category', 'overig')
        rating = fm.get('rating', 0)
        # Only include comparison articles (vs in slug or title)
        if 'vs' not in slug.lower():
            continue
        verdict = extract_verdict(fpath)
        comp_files.append({
            'slug': slug,
            'title': title,
            'category': category,
            'rating': rating,
            'verdict': verdict,
            'priceRange': fm.get('priceRange', ''),
            'featuredProduct': fm.get('featuredProduct', ''),
        })

    # Group by category
    grouped = {}
    for c in comp_files:
        cat = c['category']
        if cat not in grouped:
            grouped[cat] = []
        grouped[cat].append(c)

    # Sort groups by size
    sorted_groups = sorted(grouped.items(), key=lambda x: -len(x[1]))

    print(f"Found {len(comp_files)} comparison articles across {len(grouped)} categories")
    for cat, articles in sorted_groups:
        print(f"  {cat}: {len(articles)} articles")
    
    # Save JSON for the Astro page to read
    os.makedirs("src/data", exist_ok=True)
    with open("src/data/comparisons.json", "w") as f:
        json.dump({"groups": [[cat, articles] for cat, articles in sorted_groups], "total": len(comp_files)}, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved src/data/comparisons.json with {len(comp_files)} articles in {len(grouped)} groups")

if __name__ == '__main__':
    main()
