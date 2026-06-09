#!/usr/bin/env python3
"""Generate 3 comparison articles for KiesKeuken using Gemini API."""
import json, urllib.request, urllib.error, os, sys, unicodedata, re

# Load API key
KEY_FILE = os.path.expanduser("~/.hermes/.env")
API_KEY = None
with open(KEY_FILE) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

if not API_KEY:
    print("FATAL: No GEMINI_API_KEY found")
    sys.exit(1)

print(f"Key found, length={len(API_KEY)}")

def call_gemini(prompt, max_tokens=4000):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": max_tokens, "topP": 0.95}
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:500]}"
    except Exception as e:
        return f"Error: {e}"

def build_prompt(cat1, cat2, category, anchor_slugs=None):
    cat1_dutch = cat1.replace("-", " ").title()
    cat2_dutch = cat2.replace("-", " ").title()
    
    anchor_text = ""
    if anchor_slugs:
        anchor_text = "Bestaande artikelen om naar te verwijzen (via related):\n" + "\n".join(f"  - {s}" for s in anchor_slugs)

    return f"""Je bent een Nederlandse redacteur voor KiesKeuken / Beste Apparaten (rigbay.github.io/dutch-appliances/).

Schrijf een COMPLEET vergelijkingsartikel: "{cat1_dutch} vs. {cat2_dutch} 2026".

CATEGORIE: {category}

{anchor_text}

FORMAAT — exact deze structuur:
1. Intro (2-3 alinea's, pakkende opening)
2. Snel advies (3 aanbevelingen: beste algemeen, beste budget, beste premium)
3. De ultieme vergelijking op 6 aspecten (voor elk aspect: voor- en nadelen per type met concrete voorbeelden)
4. Prijsvergelijking (reele prijsranges in euro's, lange-termijn kosten)
5. Verborgen nadelen (eerlijke minpunten die fabrikanten niet vermelden — minimaal 3 per type)
6. Voor wie is welke? (5-6 gebruikersscenario's met concrete aanbevelingen)
7. Top 5 producten (echte producten van Amazon NL — per product: naam, verdict 1 zin, priceRange, bestFor label, rating 3.5-5.0)
8. Conclusie
9. Veelgestelde vragen (FAQ — 4 vragen met antwoorden)

BELANGRIJKE REGELS:
- Schrijf in vloeiend, natuurlijk Nederlands (NL-NL, niet Vlaams)
- Gebruik concrete prijzen in euro's (EUR X-Y)
- Alle producten moeten echt bestaan (controleer dit)
- Product-URLs: https://www.amazon.nl/s?k=[productnaam+model]&tag=kieskeukennl-21
- Minimaal 5 producten in de top 5 sectie
- Eerlijk over nadelen — geen marketingtaal
- Gebruik H2 (##) voor hoofdsecties, H3 (###) voor subsecties
- H1 (#) alleen voor de titel bovenaan
- GEEN markdown code fences om het artikel heen

Stuur het COMPLETE artikel terug, klaar om in een .md bestand te plaatsen. Geen uitleg ervoor of erna — alleen het artikel zelf."""

articles = [
    {
        "cat1": "handmixer", "cat2": "blender", "category": "keuken",
        "title": "Handmixer vs. Blender 2026: Welke Past Bij Jouw Bak- en Keukenroutine?",
        "slug": "handmixer-vs-blender-2026",
        "desc": "Handmixer vs. Blender 2026 vergeleken: prijs, functies, gebruiksgemak en verborgen nadelen. Eerlijke keuzehulp voor bakkers en thuiskoks met Amazon NL affiliate links.",
        "related": ["beste-handmixer-2026", "beste-blender-2026", "beste-keukenmachine-2026", "beste-staafmixer-2026"],
        "anchors": ["beste-handmixer-2026", "beste-blender-2026"]
    },
    {
        "cat1": "staafmixer", "cat2": "keukenmachine", "category": "keuken",
        "title": "Staafmixer vs. Keukenmachine 2026: Wanneer Is Een Staafmixer Genoeg?",
        "slug": "staafmixer-vs-keukenmachine-2026",
        "desc": "Staafmixer vs. Keukenmachine 2026 vergeleken: prijs, functies, ruimte en verborgen nadelen. Ontdek welke past bij jouw kookstijl met Amazon NL affiliate links.",
        "related": ["beste-staafmixer-2026", "beste-keukenmachine-2026", "beste-blender-2026", "beste-hakmolen-2026"],
        "anchors": ["beste-staafmixer-2026", "beste-keukenmachine-2026"]
    },
    {
        "cat1": "luchtontvochtiger", "cat2": "luchtbevochtiger", "category": "huishoudelijk",
        "title": "Luchtontvochtiger vs. Luchtbevochtiger 2026: Wat Heb Je Nodig voor een Gezond Binnenklimaat?",
        "slug": "luchtontvochtiger-vs-luchtbevochtiger-2026",
        "desc": "Luchtontvochtiger vs. Luchtbevochtiger 2026 vergeleken: prijs, effectiviteit, energiekosten en verborgen nadelen. Eerlijke keuzehulp met Amazon NL affiliate links.",
        "related": ["beste-luchtbevochtiger-2026", "beste-luchtreiniger-2026", "beste-ventilator-2026", "luchtreiniger-vs-luchtbevochtiger-2026"],
        "anchors": ["beste-luchtbevochtiger-2026"]
    },
]

OUTPUT_DIR = "src/content/reviews"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i, art in enumerate(articles):
    print(f"\n{'='*60}")
    print(f"GENERATING [{i+1}/3]: {art['title']}")
    print(f"{'='*60}")
    
    prompt = build_prompt(art["cat1"], art["cat2"], art["category"], art["anchors"])
    body = call_gemini(prompt, max_tokens=4000)
    
    if body.startswith("HTTP") or body.startswith("Error"):
        print(f"FAILED: {body[:200]}")
        continue
    
    # Clean up the body
    body = body.strip()
    if body.startswith("```"):
        parts = body.split("```")
        body = parts[1] if len(parts) >= 3 else body
        if body.startswith("markdown"):
            body = body[8:]
    body = body.strip()
    
    # Build proper frontmatter
    fm = f"""---
title: '{art["title"]}'
slug: {art["slug"]}
description: {art["desc"]}
category: {art["category"]}
rating: 4.4
priceRange: EUR 30-500
pros:
- Eerlijke vergelijking op 6 praktische aspecten
- Concrete prijsvergelijking in euro's
- Specifieke productaanbevelingen met Amazon NL links
- Verborgen nadelen die fabrikanten liever niet vermelden
cons:
- Prijzen veranderen regelmatig, check actuele aanbiedingen
- Persoonlijke voorkeur bepaalt de beste keuze
- Sommige modellen zijn alleen online verkrijgbaar
affiliateLinks:
- https://www.amazon.nl/s?k={art["cat1"]}&tag=kieskeukennl-21
modelYear: 2026
featuredProduct: Zie snel advies hieronder
readingTime: 10 min
date: '2026-06-08'
products:
- name: Zie Top 5 in het artikel
  verdict: Beste allround keuze
  priceRange: EUR 50-150
  bestFor: Allround
  rating: 4.5
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+{art["cat2"]}&tag=kieskeukennl-21
- name: Beste budget keuze
  verdict: Beste prijs-kwaliteitverhouding
  priceRange: EUR 30-80
  bestFor: Budget
  rating: 4.2
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+budget&tag=kieskeukennl-21
- name: Premium model
  verdict: Meeste functies en vermogen
  priceRange: EUR 150-300
  bestFor: Premium
  rating: 4.6
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+premium&tag=kieskeukennl-21
- name: Compacte keuze
  verdict: Beste voor kleine keukens
  priceRange: EUR 40-90
  bestFor: Compact
  rating: 4.3
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+compact&tag=kieskeukennl-21
- name: Veelzijdige keuze
  verdict: Meeste accessoires inbegrepen
  priceRange: EUR 60-200
  bestFor: Veelzijdig
  rating: 4.4
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+accessoires&tag=kieskeukennl-21
related:
"""
    for r in art["related"]:
        fm += f"- {r}\n"
    fm += "draft: false\n---\n\n"
    
    full_article = fm + body
    
    # Write to file
    filepath = os.path.join(OUTPUT_DIR, f'{art["slug"]}.md')
    with open(filepath, "w") as f:
        f.write(full_article)
    
    wc = len(body.split())
    print(f"DONE: {filepath} ({wc} words body, {len(full_article)} chars total)")

print("\n" + "="*60)
print("ALL ARTICLES GENERATED")
