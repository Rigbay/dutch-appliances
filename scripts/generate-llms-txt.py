#!/usr/bin/env python3
"""Generate llms.txt for AI crawler discoverability."""
import os, re
from pathlib import Path
from datetime import date

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"
BASE_URL = "https://rigbay.github.io/dutch-appliances"

articles = []
for f in sorted(REVIEWS_DIR.glob('*.md')):
    content = f.read_text()
    slug = f.stem
    
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else slug
    
    desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    desc = desc_match.group(1) if desc_match else ''
    
    cat_match = re.search(r'^category:\s*(\S+)', content, re.MULTILINE)
    category = cat_match.group(1) if cat_match else 'keuken'
    
    rating_match = re.search(r'^rating:\s*([\d.]+)', content, re.MULTILINE)
    rating = float(rating_match.group(1)) if rating_match else 4.0
    
    is_vs = '-vs-' in slug
    
    articles.append({
        'slug': slug,
        'title': title,
        'description': desc,
        'category': category,
        'rating': rating,
        'is_vs': is_vs
    })

# Sort: non-vs first by rating, then vs by rating
non_vs = sorted([a for a in articles if not a['is_vs']], key=lambda x: x['rating'], reverse=True)
vs_articles = sorted([a for a in articles if a['is_vs']], key=lambda x: x['rating'], reverse=True)

today = date.today().isoformat()

lines = []
lines.append(f"# KiesKeuken — Beste Apparaten 2026")
lines.append(f"# Laatst bijgewerkt: {today}")
lines.append(f"# Totaal artikelen: {len(articles)} ({len(non_vs)} koopgidsen + {len(vs_articles)} vergelijkingen)")
lines.append(f"# Amazon NL affiliate tag: kieskeukennl-21")
lines.append(f"# Site: {BASE_URL}")
lines.append("")

lines.append("## Koopgidsen")
lines.append("")
for a in non_vs:
    lines.append(f"- [{a['title']}]({BASE_URL}/{a['slug']}/) — {a['category']} — ★{a['rating']:.1f} — {a['description'][:120]}")

lines.append("")
lines.append("## Directe Vergelijkingen")
lines.append("")
for a in vs_articles:
    lines.append(f"- [{a['title']}]({BASE_URL}/{a['slug']}/) — {a['category']} — ★{a['rating']:.1f}")

lines.append("")
lines.append("## Belangrijke Pagina's")
lines.append("")
lines.append(f"- [Alle apparaten overzicht]({BASE_URL}/alle-apparaten/)")
lines.append(f"- [Vergelijkingen hub]({BASE_URL}/vergelijkingen/)")
lines.append(f"- [Top 15 van 2026]({BASE_URL}/top-15/)")
lines.append(f"- [Budget onder €50]({BASE_URL}/onder-50-euro/)")
lines.append(f"- [Budget onder €100]({BASE_URL}/budget/)")
lines.append(f"- [Middenklasse]({BASE_URL}/middenklasse/)")
lines.append(f"- [Energiezuinige apparaten]({BASE_URL}/energiezuinige-apparaten/)")
lines.append(f"- [Stroomkosten apparaten]({BASE_URL}/stroomkosten-apparaten/)")
lines.append(f"- [Nieuwe keuken inrichten]({BASE_URL}/nieuwe-keuken-inrichten/)")
lines.append(f"- [Apparaat kiezen]({BASE_URL}/apparaat-kiezen/)")
lines.append(f"- [Beste merken]({BASE_URL}/beste-merken/)")
lines.append(f"- [Over ons]({BASE_URL}/over/)")

# Write to public/ for deployment
public_path = SITE_ROOT / "public" / "llms.txt"
public_path.write_text("\n".join(lines) + "\n")
print(f"Written: {public_path}")

# Also write to dist/ if it exists
dist_path = SITE_ROOT / "dist" / "llms.txt"
if dist_path.parent.exists():
    dist_path.write_text("\n".join(lines) + "\n")
    print(f"Written: {dist_path}")

# Also write llms-full.txt with first 500 chars of each article body
lines_full = lines[:6] + [""]
lines_full.append("## Koopgidsen (met excerpt)")
lines_full.append("")
for a in non_vs:
    fpath = REVIEWS_DIR / f"{a['slug']}.md"
    if fpath.exists():
        body = fpath.read_text()
        # Remove frontmatter
        body = re.sub(r'^---.*?---\n', '', body, flags=re.DOTALL)
        # Clean markdown
        body = re.sub(r'#+\s*', '', body)
        body = re.sub(r'\*\*', '', body)
        body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', body)
        body = re.sub(r'\n+', ' ', body).strip()
        excerpt = body[:500]
    else:
        excerpt = a['description']
    lines_full.append(f"## {a['title']}")
    lines_full.append(f"URL: {BASE_URL}/{a['slug']}/")
    lines_full.append(f"Categorie: {a['category']} | Rating: ★{a['rating']:.1f}")
    lines_full.append(f"")
    lines_full.append(excerpt)
    lines_full.append("")

full_path = SITE_ROOT / "public" / "llms-full.txt"
full_path.write_text("\n".join(lines_full) + "\n")
print(f"Written: {full_path}")

if dist_path.parent.exists():
    dist_full = SITE_ROOT / "dist" / "llms-full.txt"
    dist_full.write_text("\n".join(lines_full) + "\n")
    print(f"Written: {dist_full}")

print(f"\nDone. llms.txt: {len(non_vs)} koopgidsen + {len(vs_articles)} vergelijkingen = {len(articles)} totaal")
