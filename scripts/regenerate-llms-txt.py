#!/usr/bin/env python3
"""Regenerate llms.txt with accurate article counts and all articles."""
import os, re

REVIEWS_DIR = "src/content/reviews"
OUTPUT = "public/llms.txt"
BASE_URL = "https://rigbay.github.io/dutch-appliances"

# Collect all articles
articles = []
for f in sorted(os.listdir(REVIEWS_DIR)):
    if not f.endswith(".md"):
        continue
    slug = f.replace(".md", "")
    with open(os.path.join(REVIEWS_DIR, f)) as fh:
        content = fh.read()
    
    # Extract title and category
    title = ""
    category = ""
    in_fm = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            if not in_fm:
                in_fm = True
                continue
            else:
                break  # end of frontmatter
        if not in_fm:
            continue
        if stripped.startswith("title:"):
            title = stripped.split(":", 1)[1].strip().strip("'\"")
        if stripped.startswith("category:"):
            category = stripped.split(":", 1)[1].strip().strip("'\"")
        if title and category:
            break
    
    if not category:
        category = "keuken"
    
    if not title:
        title = slug.replace("-", " ").title()
    
    articles.append({
        "slug": slug,
        "title": title,
        "category": category,
        "is_vs": "-vs-" in slug,
    })

# Count
total = len(articles)
vs_count = sum(1 for a in articles if a["is_vs"])
guide_count = total - vs_count

# Group by category
cats = {"keuken": [], "schoonmaken": [], "huishoudelijk": [], "tuin": []}
for a in articles:
    cat = a["category"]
    if cat not in cats:
        cat = "keuken"
    cats[cat].append(a)

cat_labels = {
    "keuken": "Keukenapparaten",
    "schoonmaken": "Schoonmaken en Stofzuigen",
    "huishoudelijk": "Huishoudelijk",
    "tuin": "Tuin en Buiten",
}

lines = []
lines.append("# Beste Apparaten 2026")
lines.append("")
lines.append(f"Nederlandstalige koopgidsen voor huishoudelijke apparaten: airfryers, stofzuigers, koffiemachines, wasmachines, blenders, tuingereedschap en meer.")
lines.append(f"{total} artikelen ({guide_count} koopgidsen + {vs_count} vergelijkingen) met Amazon NL affiliate links (tag: kieskeukennl-21).")
lines.append("")

for cat_key in ["keuken", "schoonmaken", "huishoudelijk", "tuin"]:
    cat_articles = cats[cat_key]
    if not cat_articles:
        continue
    lines.append(f"## {cat_labels[cat_key]}")
    lines.append("")
    for a in cat_articles:
        lines.append(f"- {a['title']}: {BASE_URL}/{a['slug']}/")
    lines.append("")

# Add hub pages
lines.append("## Vergelijk en Overzicht")
lines.append("")
lines.append(f"- Alle {vs_count} apparaat-vergelijkingen: {BASE_URL}/vergelijkingen/")
lines.append(f"- Vergelijk alle apparaten in één tabel: {BASE_URL}/vergelijk/")
lines.append(f"- Top 15 apparaten van 2026: {BASE_URL}/top-15/")
lines.append(f"- Apparaat keuzehulp: {BASE_URL}/apparaat-kiezen/")
lines.append(f"- Apparaten per situatie: {BASE_URL}/apparaten-per-situatie/")
lines.append(f"- Budget apparaten onder €100: {BASE_URL}/budget/")
lines.append(f"- Apparaten onder €50: {BASE_URL}/onder-50-euro/")
lines.append(f"- Middenklasse €100-€300: {BASE_URL}/middenklasse/")
lines.append(f"- Beste merken vergeleken: {BASE_URL}/beste-merken/")
lines.append(f"- Nieuwe keuken inrichten: {BASE_URL}/nieuwe-keuken-inrichten/")
lines.append(f"- Stroomkosten per apparaat: {BASE_URL}/stroomkosten-apparaten/")
lines.append(f"- Energiezuinige apparaten: {BASE_URL}/energiezuinige-apparaten/")
lines.append(f"- Zomer apparaten 2026: {BASE_URL}/zomer-apparaten/")
lines.append(f"- Koopgids keukenapparaten: {BASE_URL}/keukenapparaten-koopgids/")
lines.append(f"- Over onze werkwijze: {BASE_URL}/over/")
lines.append("")

lines.append("## Categorieën")
lines.append("")
for cat_key in ["keuken", "schoonmaken", "huishoudelijk", "tuin"]:
    lines.append(f"- {cat_labels[cat_key]}: {BASE_URL}/categorie/{cat_key}/")
lines.append("")

lines.append("## Transparantie")
lines.append("")
lines.append("- Alle artikelen bevatten Amazon NL affiliate links (tag: kieskeukennl-21)")
lines.append("- Producten worden eerlijk vergeleken met plus- en minpunten")
lines.append("- Prijzen en beschikbaarheid kunnen wijzigen")
lines.append("- Laatste update: juli 2026")

with open(OUTPUT, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"llms.txt regenerated: {total} articles ({guide_count} guides + {vs_count} comparisons)")
print(f"Categories: keuken={len(cats['keuken'])}, schoonmaken={len(cats['schoonmaken'])}, huishoudelijk={len(cats['huishoudelijk'])}, tuin={len(cats['tuin'])}")
