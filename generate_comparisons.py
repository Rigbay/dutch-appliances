#!/usr/bin/env python3
"""Generate 3 new comparison articles using Gemini API."""
import os, sys, json, requests

# Load API key
env_path = os.path.expanduser("~/.hermes/.env")
api_key = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("GEMINI_API_KEY=***            api_key = line.split("=", 1)[1].strip()
            break

print(f"Key found: {bool(api_key)}", file=sys.stderr)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

def safe_url(name):
    """Make a name safe for Amazon search URLs."""
    import urllib.parse
    return urllib.parse.quote(name, safe='')

ARTICLES = [
    {
        "filename": "gasbarbecue-vs-houtskoolbarbecue-2026.md",
        "topic": "Gasbarbecue vs. Houtskoolbarbecue",
        "category": "tuin",
        "priceRange": "EUR 50-2000",
        "featuredProduct": "Weber Spirit II E-310 / Kamado Joe Classic",
        "products": [
            ("Weber Spirit II E-310", "Beste gasbarbecue met 3 branders, betrouwbare ontsteking en gelijkmatige hitte.", "EUR 450-600", "Gas / Gezinnen", 4.7),
            ("Weber Go-Anywhere Gas", "Beste draagbare gasbarbecue voor camping, strand en kleine balkons.", "EUR 80-120", "Gas / Draagbaar", 4.4),
            ("Kamado Joe Classic II", "Premium keramische kamado voor authentiek houtskoolgrillen en slow cooking.", "EUR 900-1400", "Houtskool / Premium", 4.8),
            ("Weber Master-Touch GBS 57cm", "Beste houtskool bbq voor beginners en gevorderden met GBS-systeem.", "EUR 250-350", "Houtskool / Allround", 4.6),
            ("Campingaz Bistro 3", "Beste compacte gasbarbecue voor kleine tuinen en balkons.", "EUR 50-80", "Gas / Budget", 4.3),
        ],
        "related": ["beste-barbecue-2026", "barbecue-vs-elektrische-grill-2026", "beste-tuinverwarming-2026", "beste-tuinverlichting-2026", "elektrische-grasmaaier-vs-benzine-grasmaaier-2026"],
    },
    {
        "filename": "broodmachine-vs-zelf-bakken-2026.md",
        "topic": "Broodmachine vs. Zelf Brood Bakken",
        "category": "keuken",
        "priceRange": "EUR 60-500",
        "featuredProduct": "Panasonic SD-YR2550 / KitchenAid Artisan",
        "products": [
            ("Panasonic SD-YR2550", "Beste broodmachine met automatische gist- en notendispenser.", "EUR 160-220", "Broodmachine / Premium", 4.7),
            ("Philips Daily Collection HD9045", "Beste compacte broodmachine voor dagelijks vers brood.", "EUR 80-120", "Broodmachine / Budget", 4.4),
            ("Unold Backmeister Top Edition", "Complete broodmachine met glutenvrij programma en timer.", "EUR 100-150", "Broodmachine / Allround", 4.5),
            ("KitchenAid Artisan 5KSM175", "Beste keukenmachine voor handmatig deeg kneden en creatief bakken.", "EUR 350-500", "Handbakken / Keukenmachine", 4.8),
            ("Rösle Handmixer met Deeghaken", "Betaalbare handmixer met krachtige deeghaken voor handmatig bakken.", "EUR 60-90", "Handbakken / Budget", 4.3),
        ],
        "related": ["beste-broodmachine-2026", "beste-keukenmachine-2026", "beste-handmixer-2026", "beste-oven-2026", "beste-keukenweegschaal-2026", "handmixer-vs-keukenmachine-2026"],
    },
    {
        "filename": "mobiele-airco-vs-split-airco-2026.md",
        "topic": "Mobiele Airco vs. Split-Unit Airco",
        "category": "huishoudelijk",
        "priceRange": "EUR 150-2500",
        "featuredProduct": "De'Longhi Pinguino / Daikin Perfera FTXM",
        "products": [
            ("De'Longhi Pinguino PAC N90", "Beste mobiele airco met A-energielabel en fluisterstille nachtmodus.", "EUR 400-550", "Mobiel / Premium", 4.5),
            ("AEG ChillFlex Pro 9000", "Krachtige mobiele airco met warmtepompfunctie voor het hele jaar.", "EUR 500-700", "Mobiel / Allseason", 4.6),
            ("Inventum MN207C", "Beste budget mobiele airco voor kleine tot middelgrote kamers.", "EUR 200-300", "Mobiel / Budget", 4.3),
            ("Daikin Perfera FTXM25R", "Beste split-unit airco met A+++ energielabel en wifi-bediening.", "EUR 1200-1800", "Split / Premium", 4.8),
            ("Mitsubishi Electric MSZ-AP25VG", "Hoogwaardige split-unit met 3D luchtverdeling en stille werking.", "EUR 900-1400", "Split / Middenklasse", 4.7),
        ],
        "related": ["beste-airconditioner-2026", "airconditioner-vs-luchtkoeler-2026", "airconditioner-vs-ventilator-2026", "beste-ventilator-2026", "beste-luchtreiniger-2026", "beste-ontvochtiger-2026"],
    },
]

def build_frontmatter(spec):
    products_yaml = []
    for (name, verdict, pricerange, bestfor, rating) in spec["products"]:
        link = f"https://www.amazon.nl/s?k={safe_url(name)}&tag=kieskeukennl-21"
        products_yaml.append(
            f"- name: {name}\n"
            f"  verdict: {verdict}\n"
            f"  priceRange: {pricerange}\n"
            f"  bestFor: {bestfor}\n"
            f"  rating: {rating}\n"
            f"  affiliateLink: {link}"
        )
    
    related_yaml = "\n".join(f"- {r}" for r in spec["related"])
    slug = spec["filename"].replace(".md", "")
    
    return f"""---
title: '{spec["topic"]} 2026: Wat Past Bij Jouw Situatie?'
slug: {slug}
description: {spec["topic"]} in 2026 vergeleken: prijs, prestaties, gemak en verborgen nadelen. Eerlijke keuzehulp met Amazon NL links (kieskeukennl-21).
category: {spec['category']}
rating: 4.5
priceRange: {spec['priceRange']}
pros:
- Heldere vergelijking op 6 praktische aspecten met echte voor- en nadelen
- Concrete prijsvergelijking in euro's met realistische budgetopties
- Eerlijke koopadviezen per situatie (van budget tot premium)
- Specifieke productaanbevelingen met Amazon NL affiliate links
- Verborgen nadelen die fabrikanten liever niet vermelden
cons:
- Prijzen veranderen regelmatig — check altijd de actuele aanbieding
- Persoonlijke voorkeur en situatie bepalen de beste keuze
- Sommige producten zijn seizoensgebonden
affiliateLinks:
- https://www.amazon.nl/s?k={safe_url(slug.split('-vs-')[0].replace('-', '+'))}&tag=kieskeukennl-21
modelYear: 2026
featuredProduct: {spec['featuredProduct']}
readingTime: 12 min
date: '2026-06-08'
products:
{chr(10).join(products_yaml)}
related:
{related_yaml}
---"""

def generate_article(spec):
    topic = spec["topic"]
    prompt = f"""Je bent een Nederlandse SEO-schrijver voor KiesKeuken / Beste Apparaten. Schrijf een uitgebreide, behulpzame vergelijkingsgids in het Nederlands over: "{topic} voor 2026".

FORMAT VEREISTEN:
- Begin met `# {topic} 2026: [pakkende ondertitel]`
- Gebruik daarna deze exacte structuur met ## koppen:
  ## De ultieme vergelijking op 6 aspecten
  (6 subsecties: ### 1. [Aspectnaam], etc -- elk met Voor- en Nadelen voor beide opties en een Winnaar)
  ## Prijsvergelijking en terugverdientijd
  ## Verborgen nadelen die fabrikanten niet vertellen
  ## Voor wie is welke optie het beste?
  ## Onze productaanbevelingen (top 5)
  ## Veelgestelde vragen (FAQ)

STIJL:
- Eerlijk, behulpzaam, geen overdreven marketingtaal
- Nederlands op B1-niveau (toegankelijk voor iedereen)
- Gebruik bullet points (*) voor opsommingen, **vet** voor kernwoorden
- Concrete prijzen en besparingen in euro's noemen
- Minimaal 1800 woorden totaal
- Gebruik de term "wij" en "onze" (KiesKeuken / Beste Apparaten)
- Eindig met een korte paragraaf over waar lezers de producten kunnen kopen via onze Amazon NL links

BELANGRIJK: 
- Alleen Markdown, geen HTML
- Gebruik --- als sectie-scheiding (horizontale lijn)
- Geen emoji in koppen
- Schrijf geen frontmatter (--- blok) -- alleen de artikeltekst

Begin nu met het artikel."""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }
    
    resp = requests.post(URL, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"  API error {resp.status_code}: {resp.text[:300]}", file=sys.stderr)
        return None
    
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

os.chdir("/workspace/kieskeuken")
for spec in ARTICLES:
    filename = spec["filename"]
    outpath = f"src/content/reviews/{filename}"
    print(f"\n=== {filename} ===")
    
    if os.path.exists(outpath):
        print("  SKIP: exists")
        continue
    
    body = generate_article(spec)
    if not body:
        print("  FAILED")
        continue
    
    fm = build_frontmatter(spec)
    full = fm + "\n\n" + body
    
    with open(outpath, "w") as f:
        f.write(full)
    
    print(f"  OK: {len(full)} chars")

print("\nDone!")
