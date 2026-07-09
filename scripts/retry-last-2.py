#!/usr/bin/env python3
"""Retry the last 2 failed comparison articles with longer backoff."""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

REVIEWS_DIR = Path("/workspace/kieskeuken/src/content/reviews")
AMAZON_TAG = "kieskeukennl-21"
TODAY = "2026-07-08"

api_key = None
env_path = Path.home() / ".hermes" / ".env"
for line in env_path.read_text().splitlines():
    if line.startswith("GEMINI_API_KEY="):
        api_key = line.split("=", 1)[1].strip().strip("'\"")
        break

topics = [
    {
        "slug": "airfryer-vs-slowcooker-2026",
        "title": "Airfryer vs. Slowcooker 2026: Snel Krokant of Langzaam Smaakvol — Welke Past bij Jou?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Airfryer vs Slowcooker 2026.

Context: Juli 2026. Twee populaire keukenapparaten met totaal verschillende kookfilosofieen: de airfryer (hete lucht, snel, krokant, friet/snacks) en de slowcooker (lage temperatuur, urenlang, stoofvlees/soepen).

STRUCTUUR:
1. Inleiding (2-3 alinea's)
2. Snel advies — wie kiest wat
3. Hoe werkt het?
4. Vergelijkingstabel — 6 producten: Product | Type | Capaciteit | Vermogen | Prijs | Score
5. Diepere vergelijking: gerechten, energieverbruik, kooktijd, schoonmaak
6. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Philips Airfryer XXL, Ninja Foodi Max Dual Zone, Crock-Pot Slowcooker, Instant Pot Duo, Princess Aerofryer XXL, Russell Hobbs Slowcooker
- Minimaal 1500 woorden
- Prijzen in euro's""",
        "product_names": ["Philips Airfryer XXL HD9650/90", "Ninja Foodi Max Dual Zone AF400EU", "Crock-Pot Slowcooker 4.7L", "Instant Pot Duo 7-in-1", "Princess Aerofryer XXL 182065", "Russell Hobbs Slowcooker 3.5L"],
        "product_links": [f"https://www.amazon.nl/dp/B07VHKMGFX?tag={AMAZON_TAG}", f"https://www.amazon.nl/dp/B09B1XGZ4H?tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Crock-Pot+slowcooker+4.7L&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Instant+Pot+Duo+7-in-1&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Princess+Aerofryer+XXL+182065&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Russell+Hobbs+slowcooker+3.5L&tag={AMAZON_TAG}"],
        "related": ["beste-airfryer-2026", "beste-slowcooker-2026", "airfryer-vs-friteuse-2026", "slowcooker-vs-snelkookpan-2026"]
    },
    {
        "slug": "stofzuiger-vs-bezem-2026",
        "title": "Stofzuiger vs. Bezem 2026: Wanneer is een Bezem Beter dan een Stofzuiger?",
        "category": "schoonmaken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Stofzuiger vs Bezem 2026.

Context: Juli 2026. Wanneer volstaat een goede bezem en wanneer heb je echt een stofzuiger nodig? Voor kleine appartementen, studentenkamers, snelle schoonmaakbeurten en harde vloeren.

STRUCTUUR:
1. Inleiding (2-3 alinea's)
2. Snel advies — wie kiest wat
3. Wanneer een bezem beter is
4. Wanneer een stofzuiger beter is
5. Vergelijkingstabel — 6 producten: Product | Type | Geschikt voor | Prijs | Score
6. Hybride oplossingen — steelstofzuiger, kruimeldief
7. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Leifheit Vloerwisser Set, Philips PowerPro Compact, Dyson V8, Brabantia Bezemset, Karcher WD3, Swiffer Dweilsysteem
- Minimaal 1500 woorden
- Prijzen in euro's""",
        "product_names": ["Leifheit Vloerwisser Set", "Philips PowerPro Compact FC9332/09", "Dyson V8 Absolute", "Brabantia Bezemset", "Karcher WD3 Nat/Droog", "Swiffer Dweilsysteem"],
        "product_links": [f"https://www.amazon.nl/s?k=Leifheit+vloerwisser+set&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Philips+PowerPro+Compact+FC9332&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Dyson+V8+Absolute&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Brabantia+bezemset&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Karcher+WD3&tag={AMAZON_TAG}", f"https://www.amazon.nl/s?k=Swiffer+dweilsysteem&tag={AMAZON_TAG}"],
        "related": ["beste-stofzuiger-2026", "beste-steelstofzuiger-2026", "stofzuiger-vs-steelstofzuiger-2026", "robotstofzuiger-vs-stofzuiger-2026"]
    }
]

def call_gemini(prompt_text, api_key, retries=5):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    body = {"contents": [{"parts": [{"text": prompt_text}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as resp:
                data = json.loads(resp.read())
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text.startswith("```"):
                    lines = text.split("\n")
                    lines = lines[1:]
                    if lines and lines[-1].strip() == "```":
                        lines = lines[:-1]
                    text = "\n".join(lines)
                return text
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < retries - 1:
                wait = (attempt + 1) * 20
                print(f"503, retry in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise
        except Exception:
            if attempt < retries - 1:
                wait = (attempt + 1) * 10
                print(f"err, retry in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise

def build_article(topic, body_md):
    title, slug, category, related = topic["title"], topic["slug"], topic["category"], topic["related"]
    desc_slug = slug.replace("-vs-", " vs ").replace("-2026", "").replace("-", " ")
    lines = ["---", f'title: "{title}"', f'slug: "{slug}"', f'description: "Vergelijk {desc_slug} in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21)."', f'category: "{category}"', "rating: 4.5", 'priceRange: "EUR 15-1500"', "pros:", '  - "Eerlijke vergelijking met concrete voor- en nadelen per type"', '  - "Actuele prijzen en modellen voor 2026"', '  - "Helder advies voor elke woonsituatie en budget"', "cons:", '  - "Prijzen kunnen wijzigen afhankelijk van aanbiedingen"', '  - "Niet elk model is getest in dagelijks gebruik"', '  - "Sommige specificaties zijn afhankelijk van woningtype"', "affiliateLinks:"]
    for link in topic["product_links"][:5]:
        lines.append(f'  - "{link}"')
    lines += [f"date: {TODAY}", "modelYear: 2026", f'featuredProduct: "{topic["product_names"][0]}"', 'readingTime: "10 min"', "products:"]
    for i, name in enumerate(topic["product_names"]):
        lines += [f'  - name: "{name}"', f'    verdict: "Vergelijkingsproduct — zie tabel voor volledige specificaties."', f'    priceRange: "EUR 15-1500"', f'    bestFor: "Vergelijking {desc_slug}"', f'    rating: 4.5', f'    affiliateLink: "{topic["product_links"][i]}"']
    lines.append("related:")
    for r in related:
        lines.append(f'  - "{r}"')
    lines += ["draft: false", "---", "", body_md]
    return "\n".join(lines) + "\n"

for topic in topics:
    slug = topic["slug"]
    out_path = REVIEWS_DIR / f"{slug}.md"
    if out_path.exists():
        print(f"SKIP {slug} — already exists")
        continue
    print(f"GENERATING {slug}...", end=" ", flush=True)
    t0 = time.time()
    try:
        body_md = call_gemini(topic["prompt"], api_key)
        article = build_article(topic, body_md)
        REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
        out_path.write_text(article)
        print(f"OK ({time.time()-t0:.1f}s, ~{len(body_md)} chars)")
        time.sleep(5)
    except Exception as e:
        print(f"FAILED: {e}")
print("DONE")
