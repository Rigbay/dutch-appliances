#!/usr/bin/env python3
"""Generate missing articles via Gemini with robust JSON sanitization."""
import json
import urllib.request
import os
import sys
from pathlib import Path

SITE_ROOT = Path("/workspace/kieskeuken")
REVIEWS_DIR = SITE_ROOT / "src/content/reviews"

# Read API key
with open("/workspace/.agent-runtime/.env") as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.strip().split("=", 1)[1]
            break

PROMPT = """Je bent een Nederlandse consumentenjournalist die eerlijke, praktische koopgidsen schrijft voor een Nederlandstalige website over huishoudelijke apparaten. 

Schrijf een complete koopgids in het Nederlands over: {topic_nl}

CATEGORIE: {category}
DOELGROEP: {audience}
PRODUCTIDEEËN: {product_ideas}

STRUCTUUR (volg exact):

1. Inleiding — 2-3 alinea's: waarom dit apparaat relevant is in 2026, praktische vragen, beste keuze met argumenten.

2. Snel advies — 3 bullets: "Kies X als je...", productnaam + situatie + voordeel.

3. Beste keuze per budget — 4 secties (Beste koop, Beste prestaties, Beste budget, Beste voor kleine ruimte). Per sectie: productnaam, prijsrange, voor wie, voor-/nadelen.

4. Waar op letten? — 3-4 alinea's over verborgen eigenschappen (schoonmaak, garantie, formaat, verbruik).

5. Vergelijkingstabel — Markdown-tabel met 5-7 producten, kolommen: Product | Inhoud/capaciteit | Vermogen | Prijs | Beste voor | Score.

6. Conclusie — 1-2 alinea's: echte afweging, wie kiest beter voor ander model.

Schrijf levendig, concreet, Nederlands. Prijzen in euro's. Minimaal 1200 woorden. Eerlijk over minpunten.

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
      "name": "Volledige productnaam",
      "verdict": "1 zin waarom deze keuze",
      "priceRange": "EUR X-Y",
      "bestFor": "Gebruiksscenario",
      "rating": 4.0
    }}
  ]
}}

BELANGRIJK: ALLE dubbele aanhalingstekens in de body_markdown moeten escaped zijn (\\"). Gebruik GEEN echte line breaks in de JSON — gebruik \\n voor nieuwe regels in de markdown."""

SPECS = [
    {
        "slug": "beste-bruiswaterapparaat-2026",
        "topic_nl": "de beste bruiswaterapparaten en soda makers voor thuis — vers bruiswater zonder plastic flessen",
        "category": "keuken",
        "audience": "Nederlandse huishoudens die frisdrank en bruiswater willen maken zonder plastic afval — van gezinnen tot sporters en bewuste consumenten",
        "product_ideas": "SodaStream Terra, SodaStream Art, Aarke Carbonator III, Brita Soda, Philips Soda Maker, Mysoda Woody, DrinkMate"
    },
    {
        "slug": "beste-elektrische-deken-2026",
        "topic_nl": "de beste elektrische dekens en warmtedekens voor een warme nacht in de Nederlandse winter",
        "category": "huishoudelijk",
        "audience": "Nederlandse huishoudens die de energierekening willen verlagen door gericht te verwarmen — ouderen, koukleumen en comfortzoekers",
        "product_ideas": "Inventum EK1000W, Dreamland Intelliheat, Beurer HD150, Stoov Big Hug, Medisana HDW, Silentnight Comfort, Klarstein Thermo"
    }
]

def clean_json(text):
    """Aggressively clean Gemini output to valid JSON."""
    text = text.strip()
    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    
    # Find JSON boundaries
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start:end+1]
    
    # Remove ASCII control characters except \n, \t
    cleaned = []
    for ch in text:
        if ord(ch) < 32 and ch not in ('\n', '\t', '\r'):
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
    today = "2026-06-05"
    lines = ["---"]
    lines.append(f'title: "{spec["topic_nl"][:100]}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'description: "Vergelijk de beste {slug.replace("beste-","").replace("-2026","").replace("-"," ")} van 2026. Koopgids met prijsvergelijking, tips en Amazon NL links."')
    lines.append(f'category: "{spec["category"]}"')
    
    rating = max(p.get("rating", 4.0) for p in data.get("products", [{}])) if data.get("products") else 4.0
    lines.append(f"rating: {rating}")
    lines.append(f'priceRange: "{data.get("priceRange", "EUR 50-200")}"')
    
    lines.append("pros:")
    for p in data.get("pros", ["Praktisch advies", "Duidelijke vergelijking", "Nederlandstalig"]):
        lines.append(f'  - "{p}"')
    
    lines.append("cons:")
    for c in data.get("cons", ["Prijzen variëren per winkel", "Persoonlijke voorkeur speelt rol"]):
        lines.append(f'  - "{c}"')
    
    # Build Amazon NL search links from product names
    lines.append("affiliateLinks:")
    for p in data.get("products", []):
        name = p.get("name", "").replace(" ", "+").lower()
        lines.append(f'  - "https://www.amazon.nl/s?k={name}&tag=kieskeukennl-21"')
    
    lines.append(f"date: {today}")
    lines.append(f"modelYear: 2026")
    lines.append(f'featuredProduct: "{data.get("featuredProduct", "")}"')
    lines.append(f'readingTime: "{data.get("readingTime", "8 min")}"')
    
    lines.append("products:")
    for p in data.get("products", []):
        name = p.get("name", "").replace(" ", "+").lower()
        lines.append(f'  - name: "{p.get("name","")}"')
        lines.append(f'    verdict: "{p.get("verdict","")}"')
        lines.append(f'    priceRange: "{p.get("priceRange","")}"')
        lines.append(f'    bestFor: "{p.get("bestFor","")}"')
        lines.append(f'    rating: {p.get("rating",4.0)}')
        lines.append(f'    affiliateLink: "https://www.amazon.nl/s?k={name}&tag=kieskeukennl-21"')
    
    # Related slugs
    related = [f"beste-{s}" for s in ["airfryer-2026", "waterkoker-2026", "koelkast-2026"]]
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
    
    if out_path.exists():
        print(f"SKIP {slug} — already exists")
        continue
    
    print(f"GENERATING {slug}...", end=" ", flush=True)
    prompt = PROMPT.format(**spec)
    
    try:
        raw = call_gemini(prompt)
        cleaned = clean_json(raw)
        data = json.loads(cleaned)
        article = build_md(spec, data, slug)
        out_path.write_text(article)
        print(f"OK ({len(article)} bytes)")
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {e}")
        # Try to save raw for debugging
        Path(f"/tmp/{slug}-raw.txt").write_text(raw)
        print(f"  Raw saved to /tmp/{slug}-raw.txt")
    except Exception as e:
        print(f"FAILED: {e}")
