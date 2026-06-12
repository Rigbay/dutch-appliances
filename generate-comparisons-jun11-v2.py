#!/usr/bin/env python3
"""Generate 5 new comparison articles using Gemini API for KiesKeuken.
Outputs to src/content/reviews/ in canonical clone /workspace/kieskeuken
"""

import os, sys, json, time

# Load env
env_path = os.path.expanduser("~/.hermes/.env")
env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

GEMINI_KEY = env.get("GEMINI_API_KEY")
if not GEMINI_KEY:
    print("FATAL: No GEMINI_API_KEY")
    sys.exit(1)

MODEL = "gemini-2.5-flash"

COMPARISONS = [
    {
        "slug": "ijsmachine-vs-diepvries-zelf-maken-2026",
        "title": "IJsmachine vs. Zelf IJs Maken in de Diepvries: Wat Is Lekkerder én Makkelijker?",
        "category": "keuken",
        "price_range": "EUR 25-300",
        "reading_time": "9 min",
        "products_keywords": [
            "Cuisinart ICE30BCE ijsmachine",
            "Magimix Gelato Expert",
            "Ninja Creami NC300",
            "Unold 48870 ijsmachine",
            "Princess IJsmachine",
            "Silikomart ijslolly vormen"
        ],
        "related": [
            "beste-ijsmachine-2026",
            "beste-keukenmachine-2026",
            "beste-blender-2026",
            "beste-gourmetstel-2026",
            "beste-bruiswaterapparaat-2026"
        ]
    },
    {
        "slug": "pizza-oven-vs-gewone-oven-2026",
        "title": "Pizza Oven vs. Gewone Oven 2026: Heb Je een Aparte Pizza Oven Nodig voor Restaurantkwaliteit?",
        "category": "keuken",
        "price_range": "EUR 80-800",
        "reading_time": "10 min",
        "products_keywords": [
            "Ooni Koda 12 pizza oven",
            "Sage the Pizzaiolo",
            "G3 Ferrari Delizia pizza oven",
            "Ariete 909 pizza oven",
            "Lidl Silvercrest pizza oven",
            "Roccbox Gozney pizza oven"
        ],
        "related": [
            "beste-pizza-oven-2026",
            "beste-oven-2026",
            "beste-airfryer-2026",
            "beste-bakplaat-2026",
            "oven-vs-magnetron-2026"
        ]
    },
    {
        "slug": "rijstkoker-vs-pan-2026",
        "title": "Rijstkoker vs. Rijst Koken in een Pan 2026: Wat Geeft Het Beste Resultaat?",
        "category": "keuken",
        "price_range": "EUR 15-250",
        "reading_time": "8 min",
        "products_keywords": [
            "Yum Asia Panda rijstkoker",
            "Cuckoo CR-0631 rijstkoker",
            "Russell Hobbs 19750 rijstkoker",
            "Reishunger digitale rijstkoker",
            "Tefal RK302E rijstkoker",
            "BK kookpan inductie"
        ],
        "related": [
            "beste-rijstkoker-2026",
            "beste-koekenpan-2026",
            "beste-pannenset-2026",
            "beste-stoomoven-2026",
            "beste-slowcooker-2026"
        ]
    },
    {
        "slug": "tuinverwarming-vs-vuurkorf-2026",
        "title": "Tuinverwarming vs. Vuurkorf 2026: Wat Verwarmt Je Terras Beter en Goedkoper?",
        "category": "tuin",
        "price_range": "EUR 30-400",
        "reading_time": "9 min",
        "products_keywords": [
            "Eurom Golden 2000 terrasverwarmer",
            "Sunred elektronische terrasverwarmer",
            "Primus Kinjia vuurkorf",
            "OutdoorChef vuurschaal",
            "Blumfeldt Heatwave terrasverwarmer",
            "Vonroc terrasverwarmer"
        ],
        "related": [
            "beste-tuinverwarming-2026",
            "beste-barbecue-2026",
            "beste-elektrische-kachel-2026",
            "gasbarbecue-vs-houtskoolbarbecue-2026",
            "beste-tuinverlichting-2026"
        ]
    },
    {
        "slug": "ontvochtiger-vs-luchtreiniger-2026",
        "title": "Ontvochtiger vs. Luchtreiniger 2026: Welke Heb Je Nodig voor een Gezond Binnenklimaat?",
        "category": "huishoudelijk",
        "price_range": "EUR 80-600",
        "reading_time": "10 min",
        "products_keywords": [
            "Philips Air Performer 8000",
            "Pro Breeze 12L ontvochtiger",
            "MeacoDry Arete One ontvochtiger",
            "Xiaomi Smart Air Purifier 4 Pro",
            "Dyson Purifier Hot+Cool Formaldehyde",
            "Eurom D-Lux ontvochtiger"
        ],
        "related": [
            "beste-ontvochtiger-2026",
            "beste-luchtreiniger-2026",
            "beste-luchtbevochtiger-2026",
            "luchtreiniger-vs-luchtbevochtiger-2026",
            "beste-airconditioner-2026"
        ]
    }
]

PROMPT_TEMPLATE = """Je bent een ervaren Nederlandse content-schrijver voor KiesKeuken.nl, een affiliate-koopgids website over huishoudelijke apparaten. Schrijf een SEO-geoptimaliseerd Markdown-artikel in het Nederlands dat twee apparaten met elkaar vergelijkt.

**VERGELIJKING:** {title}
**CATEGORIE:** {category}
**PRIJSRANGE:** {price_range}
**LEESTIJD:** {reading_time}

Schrijf het artikel als Markdown met de volgende structuur:

## Snel Advies: Welk Apparaat Past Bij Jou?
[3 specifieke aanbevelingen: beste keuze met modelnaam, voordelen, en prijsindicatie]

## Beste Keuze per Budget
### Beste Koop (ca. EUR [range])
### Beste Prestaties (ca. EUR [range])
### Beste Budget (ca. EUR [range])
[Per budget-niveau: 2 producten, specifieke modelnamen, prijsrange, sterke/zwakke punten]

## Waar Op Letten?
[3-4 subsecties over de belangrijkste vergelijkingscriteria. Gebruik '### ' koppen]

## Vergelijkingstabel: [Apparaat] vs [Apparaat] 2026
[Markdown tabel met 6-8 producten, kolommen: Model | Type | Prijs | Beste voor | Rating]

## Minpunten per Apparaattype
[Eerlijke nadelen]

## FAQ
[6-8 vragen in format:
### Vraag?
Antwoord in 3-5 zinnen.]

## Conclusie
[Samenvatting wie welk apparaat moet kopen]

**REGELS:**
- Nederlands, natuurlijk, geen vertaalde Engelse zinsconstructies
- Gebruik concrete modelnamen en realistische prijzen (EUR)
- Affiliate links naar Amazon NL met tag kieskeukennl-21: format is https://www.amazon.nl/s?k=ModelNaam&tag=kieskeukennl-21
- Minimaal 800 woorden, maximaal 2000
- Gebruik **vet** voor productnamen
- Geen overdreven marketingtaal — eerlijk over nadelen
- Prijzen in euro's: EUR XX-YY
- Sluit af met een gerelateerde-artikelen sectie met 4-5 interne links
- EINDE van het artikel: alleen de Markdown, geen uitleg ervoor of erna

Producten om te gebruiken (zoek op Amazon NL, tag kieskeukennl-21):
{products_keywords}
"""

import urllib.request, urllib.error

def call_gemini(prompt, retries=3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }).encode()
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"  Attempt {attempt+1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(3)
    return None

def build_frontmatter(comp, description):
    """Build YAML frontmatter for the comparison article."""
    keywords = comp["products_keywords"]
    affiliate_links = "\n".join([f"  - https://www.amazon.nl/s?k={kw.replace(' ', '+')}&tag=kieskeukennl-21" for kw in keywords])
    related_links = "\n".join([f"  - {r}" for r in comp["related"]])
    
    fm = f"""---
title: '{comp["title"]}'
slug: {comp["slug"]}
description: "{description}"
category: {comp["category"]}
rating: 4.4
priceRange: {comp["price_range"]}
pros:
  - Eerlijke vergelijking op 6 praktische aspecten
  - Concrete prijsvergelijking inclusief gebruikskosten
  - Specifieke productaanbevelingen met Amazon NL links
  - Verborgen nadelen die fabrikanten liever niet vermelden
cons:
  - Prijzen veranderen regelmatig, check actuele aanbiedingen
  - Persoonlijke voorkeur bepaalt uiteindelijk de beste keuze
  - Sommige modellen alleen online verkrijgbaar
affiliateLinks:
{affiliate_links}
modelYear: 2026
featuredProduct: {keywords[0].split('  ')[0] if '  ' not in keywords[0] else keywords[0].split('  ')[0]}
readingTime: {comp["reading_time"]}
date: '2026-06-11'
related:
{related_links}
draft: false
faq: []"""
    return fm

def extract_description(text):
    """Extract a short description from article body."""
    # Find the first section after the title
    lines = text.strip().split('\n')
    # Skip the title line and blank lines
    for i, line in enumerate(lines):
        if line.startswith('# '):
            # Take the next paragraph
            for j in range(i+1, min(i+20, len(lines))):
                para = lines[j].strip()
                if para and not para.startswith('#') and not para.startswith('-') and not para.startswith('|'):
                    # Clean: remove markdown formatting, limit to 180 chars
                    para = para.replace('**', '').replace('*', '').strip()
                    if len(para) > 175:
                        para = para[:175].rsplit(' ', 1)[0] + '.'
                    return para[:180]
    return "Vergelijk twee populaire apparaten: prijs, gebruiksgemak, en verborgen nadelen. Eerlijke keuzehulp met Amazon NL affiliate links."

def main():
    output_dir = "/workspace/kieskeuken/src/content/reviews"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, comp in enumerate(COMPARISONS):
        slug = comp["slug"]
        filepath = os.path.join(output_dir, f"{slug}.md")
        if os.path.exists(filepath):
            print(f"[{i+1}/{len(COMPARISONS)}] SKIP {slug} — already exists")
            continue
        
        print(f"[{i+1}/{len(COMPARISONS)}] Generating: {slug}")
        prompt = PROMPT_TEMPLATE.format(
            title=comp["title"],
            category=comp["category"],
            price_range=comp["price_range"],
            reading_time=comp["reading_time"],
            products_keywords="\n".join(f"- {kw}" for kw in comp["products_keywords"])
        )
        
        text = call_gemini(prompt)
        if not text:
            print(f"  FAILED after retries")
            continue
        
        description = extract_description(text)
        fm = build_frontmatter(comp, description)
        
        full_article = fm + "\n---\n\n" + text.strip()
        
        with open(filepath, 'w') as f:
            f.write(full_article)
        
        print(f"  Wrote {len(full_article)} chars to {filepath}")
        time.sleep(2)  # Rate limit
    
    print("\nDone!")

if __name__ == "__main__":
    main()
