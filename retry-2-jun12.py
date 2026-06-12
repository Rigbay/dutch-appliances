#!/usr/bin/env python3
"""Retry 2 failed articles."""
import json, urllib.request, os
from pathlib import Path

SITE_ROOT = Path("/workspace/kieskeuken")
REVIEWS_DIR = SITE_ROOT / "src/content/reviews"

# Read API key from env file
env_path = os.path.expanduser("~/.hermes/.env")
API_KEY = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("GEMINI_API_KEY=***            API_KEY=line.s...=", 1)[1]
            break

if not API_KEY:
    print("ERROR: Could not find GEMINI_API_KEY")
    exit(1)

PROMPT = """Je bent een Nederlandse consumentenjournalist die eerlijke, praktische vergelijkingsartikelen schrijft voor een Nederlandstalige website over huishoudelijke apparaten.

Schrijf een compleet vergelijkingsartikel in het Nederlands: {topic_nl}

CATEGORIE: {category}
DOELGROEP: {audience}

STRUCTUUR (volg exact):

1. Inleiding — 2-3 alinea's: waarom deze vergelijking relevant is in 2026, de kernvraag, beste keuze met argumenten.

2. Snel advies — 3 bullets: "Kies {product_a} als je...", "Kies {product_b} als je...", concrete situaties + voordelen.

3. Wat is het verschil? — 3-4 alinea's over de fundamentele verschillen in werking, resultaat, kosten, onderhoud.

4. Vergelijkingstabel — Markdown-tabel met 5-7 rijen, kolommen: Aspect | {product_a_short} | {product_b_short} | Winnaar.

5. Beste keuze per situatie — 4 secties: Beste voor kleine ruimte, Beste voor gezinnen, Beste voor budget, Beste voor gemak. Per sectie: concrete productaanbeveling met prijsrange.

6. Waar op letten bij aankoop? — 3-4 alinea's over verborgen eigenschappen (schoonmaak, garantie, formaat, verbruik, accessoires).

7. Conclusie — 1-2 alinea's: echte afweging, wie kiest beter voor alternatief.

Schrijf levendig, concreet, Nederlands. Prijzen in euro's. Minimaal 1000 woorden. Eerlijk over minpunten van beide opties.

Stuur ALLEEN geldige JSON terug — GEEN markdown code fences, GEEN extra tekst. Het JSON-object moet deze velden hebben:
{{
  "body_markdown": "VOLLEDIGE artikeltekst in Markdown, beginnend bij ## Inleiding",
  "featuredProduct": "Naam beste product",
  "priceRange": "EUR X-Y",
  "pros": ["pro 1", "pro 2", "pro 3"],
  "cons": ["con 1", "con 2", "con 3"],
  "readingTime": "X min",
  "products": [
    {{
      "name": "Volledige productnaam + model",
      "verdict": "1 zin waarom deze keuze",
      "priceRange": "EUR X-Y",
      "bestFor": "Gebruiksscenario",
      "rating": 4.0
    }}
  ]
}}

BELANGRIJK: ALLE dubbele aanhalingstekens in de body_markdown moeten escaped zijn (\\"). Gebruik GEEN echte line breaks in de JSON — gebruik \\n voor nieuwe regels in de markdown. Gebruik GEEN tabs of andere control characters in de JSON string."""

SPECS = [
    {
        "slug": "kettingzaag-vs-handzaag-2026",
        "topic_nl": "kettingzaag versus handzaag — welk zaaggereedschap voor jouw klus?",
        "category": "tuin",
        "audience": "Nederlandse klussers en tuinbezitters die bomen snoeien, hout zagen of brandhout maken — van incidenteel gebruik tot regelmatig onderhoud",
        "product_a": "kettingzaag",
        "product_b": "handzaag",
        "product_a_short": "Kettingzaag",
        "product_b_short": "Handzaag",
        "product_ideas": "Stihl MS 170, Husqvarna 120 Mark II, Makita UC4051A, Bosch AKE 35, Bahco 396-LAP, Fiskars Xtract SW31, Silky Gomtaro"
    },
    {
        "slug": "waterontharder-vs-ontkalker-2026",
        "topic_nl": "waterontharder versus ontkalker — wat is de beste oplossing tegen kalk in huis?",
        "category": "huishoudelijk",
        "audience": "Nederlandse huishoudens in regio's met hard water die kalkaanslag in apparaten, op kranen en in de badkamer willen voorkomen — van huurders tot huiseigenaren",
        "product_a": "waterontharder",
        "product_b": "ontkalker",
        "product_a_short": "Waterontharder",
        "product_b_short": "Ontkalker",
        "product_ideas": "AquaCell waterontharder, BWT AQA Perla, Waterboss 900, Amfa4000 antikalksysteem, BWT AQA Drink, AquaTru magnetische ontkalker, Calgon tabletten"
    }
]

def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end+1]
    cleaned = []
    for ch in text:
        if ord(ch) < 32 and ch not in ('\n', '\r'):
            cleaned.append(' ')
        else:
            cleaned.append(ch)
    return ''.join(cleaned)

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 8192}
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]

def build_md(spec, data, slug):
    today = "2026-06-12"
    lines = ["---"]
    title = spec["topic_nl"]
    lines.append(f'title: "{title}"')
    lines.append(f'slug: "{slug}"')
    desc = f'Vergelijk {slug.replace("-2026","").replace("-"," ")} in 2026. Ontdek de voor- en nadelen, prijsvergelijking en welke het beste bij jouw situatie past.'
    lines.append(f'description: "{desc}"')
    lines.append(f'category: "{spec["category"]}"')
    rating = max(p.get("rating", 4.0) for p in data.get("products", [{}])) if data.get("products") else 4.0
    lines.append(f"rating: {rating}")
    lines.append(f'priceRange: "{data.get("priceRange", "EUR 50-500")}"')
    lines.append("pros:")
    for p in data.get("pros", ["Praktisch advies", "Duidelijke vergelijking", "Nederlandstalig"]):
        lines.append(f'  - "{p}"')
    lines.append("cons:")
    for c in data.get("cons", ["Prijzen varieren per winkel", "Persoonlijke voorkeur speelt rol"]):
        lines.append(f'  - "{c}"')
    lines.append("affiliateLinks:")
    for p in data.get("products", []):
        name = p.get("name", "").replace(" ", "+")
        lines.append(f'  - "https://www.amazon.nl/s?k={name}&tag=kieskeukennl-21"')
    lines.append(f"date: {today}")
    lines.append(f"modelYear: 2026")
    lines.append(f'featuredProduct: "{data.get("featuredProduct", "")}"')
    lines.append(f'readingTime: "{data.get("readingTime", "9 min")}"')
    lines.append("products:")
    for p in data.get("products", []):
        name = p.get("name", "")
        search_name = name.replace(" ", "+")
        lines.append(f'  - name: "{name}"')
        lines.append(f'    verdict: "{p.get("verdict","")}"')
        lines.append(f'    priceRange: "{p.get("priceRange","")}"')
        lines.append(f'    bestFor: "{p.get("bestFor","")}"')
        lines.append(f'    rating: {p.get("rating",4.0)}')
        lines.append(f'    affiliateLink: "https://www.amazon.nl/s?k={search_name}&tag=kieskeukennl-21"')
    related_map = {
        "tuin": ["beste-heggenschaar-2026", "beste-bosmaaier-2026", "beste-grasmaaier-2026", "beste-kettingzaag-2026"],
        "huishoudelijk": ["beste-elektrische-kachel-2026", "beste-waterontharder-2026", "beste-luchtreiniger-2026", "beste-ontvochtiger-2026"],
        "schoonmaken": ["beste-tapijtreiniger-2026", "beste-stoomreiniger-2026", "beste-stofzuiger-2026", "beste-vloerwisser-2026"],
        "keuken": ["beste-airfryer-2026", "beste-koffiemachine-2026", "beste-waterkoker-2026", "beste-magnetron-2026"]
    }
    related = related_map.get(spec["category"], related_map["keuken"])
    lines.append("related:")
    for r in related:
        lines.append(f'  - "{r}"')
    lines.append("draft: false")
    lines.append("---")
    lines.append("")
    lines.append(data.get("body_markdown", "").strip())
    return "\n".join(lines)

for spec in SPECS:
    slug = spec["slug"]
    out_path = REVIEWS_DIR / f"{slug}.md"
    print(f"GENERATING {slug}...", end=" ", flush=True)
    prompt = PROMPT.format(**spec)
    try:
        raw = call_gemini(prompt)
        cleaned = clean_json(raw)
        data = json.loads(cleaned)
        if not data.get("body_markdown") or len(data.get("body_markdown", "")) < 500:
            print(f"BODY TOO SHORT ({len(data.get('body_markdown', ''))} chars) — retrying")
            raw = call_gemini(prompt)
            cleaned = clean_json(raw)
            data = json.loads(cleaned)
        if not data.get("products") or len(data.get("products", [])) < 3:
            print(f"TOO FEW PRODUCTS ({len(data.get('products', []))}) — retrying")
            raw = call_gemini(prompt)
            cleaned = clean_json(raw)
            data = json.loads(cleaned)
        article = build_md(spec, data, slug)
        out_path.write_text(article)
        print(f"OK ({len(article)} bytes, {len(data.get('products',[]))} products)")
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {e}")
        Path(f"/tmp/{slug}-raw-v2.txt").write_text(raw)
        print(f"  Raw saved to /tmp/{slug}-raw-v2.txt")
    except Exception as e:
        print(f"FAILED: {e}")
