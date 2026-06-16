#!/usr/bin/env python3
"""Fix truncated articles + generate 2 missing ones using Ollama qwen3:14b.
Hermes cron — June 16, 2026
"""
import os, sys, json, time, subprocess

OUT_DIR = "/workspace/kieskeuken/src/content/reviews"
MODEL = "qwen3:14b"

def call_ollama(system_prompt, user_prompt):
    """Call Ollama with system + user prompt."""
    cmd = ["ollama", "run", MODEL]
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    try:
        result = subprocess.run(cmd, input=full_prompt, capture_output=True, text=True, timeout=180)
        if result.returncode != 0:
            print(f"  Ollama error: {result.stderr[:300]}")
            return None
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  Ollama timeout")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

# === FIX TRUNCATED ARTICLES ===
FIXES = [
    {
        "slug": "vaatwasser-inbouw-vs-vrijstaand-2026",
        "completion_prompt": """Het volgende artikel over inbouw vs vrijstaande vaatwasser is afgekapt mid-sentence. De tekst stopt bij: "...Een vrijstaande vaatwasser daarentegen is een compleet apparaat met een afgewerkte buiten"

Schrijf ALLEEN de ontbrekende secties:
- Maak de lopende paragraaf af (over het uiterlijk van vrijstaande vaatwassers)
- ## Vergelijkingstabel: Inbouw vs. Vrijstaande Vaatwasser (2026) — tabel met 8 rijen: Prijs, Installatie, Design, Flexibiliteit, Capaciteit, Geluidsniveau, Energieverbruik, Geschikt voor
- ## Beste Inbouw Vaatwasser Modellen van 2026 — Bosch Serie 6 (EUR 600-900), Siemens iQ500 (EUR 800-1200), Miele (EUR 1000-1500)
- ## Beste Vrijstaande Vaatwasser Modellen van 2026 — Bosch Serie 4 (EUR 450-700), AEG (EUR 500-850), Siemens vrijstaand (EUR 550-900)
- ## Wanneer Kies Je voor een Inbouw Vaatwasser? — 3-4 situaties
- ## Wanneer Kies Je voor een Vrijstaande Vaatwasser? — 3-4 situaties
- ## Kostenvergelijking op Lange Termijn — aanschaf + installatie + energie over 5 jaar
- ## Veelgemaakte Fouten bij het Kiezen — 3 fouten
- ## Conclusie — 2 paragrafen met aanbeveling per situatie
- **Affiliate disclosure**: Amazon.nl tag kieskeukennl-21

Schrijf in vlot Nederlands. Output: alleen de Markdown secties, geen frontmatter."""
    },
    {
        "slug": "slowcooker-vs-snelkookpan-2026",
        "completion_prompt": """Het volgende artikel over slowcooker vs snelkookpan is afgekapt mid-sentence. De tekst stopt bij: "...Voor wie de voorkeur geeft aan een"

Schrijf ALLEEN de ontbrekende secties:
- Maak de lopende paragraaf over de Tefal Secure 5 Neo af
- Voeg Ninja Foodi multicooker (EUR 150-250) toe als derde snelkookpan-model
- ## Wanneer Kies Je voor een Slowcooker? — 3-4 situaties (stoofschotels, meal prep, budget, etc.)
- ## Wanneer Kies Je voor een Snelkookpan? — 3-4 situaties (tijdsdruk, bonen/peulvruchten, bouillon, etc.)
- ## Kostenvergelijking op Lange Termijn — aanschaf + energie + onderhoud over 5 jaar
- ## Veelgemaakte Fouten bij het Kiezen — 3 fouten
- ## Conclusie — 2 paragrafen met aanbeveling per situatie
- **Affiliate disclosure**: Amazon.nl tag kieskeukennl-21

Schrijf in vlot Nederlands. Output: alleen de Markdown secties, geen frontmatter."""
    }
]

print("=== FIXING TRUNCATED ARTICLES (Ollama qwen3:14b) ===")
for fix in FIXES:
    path = os.path.join(OUT_DIR, f"{fix['slug']}.md")
    with open(path) as f:
        existing = f.read()
    
    print(f"\nFixing: {fix['slug']} (existing: {len(existing)} chars)")
    completion = call_ollama("Je bent een Nederlandse copywriter. Schrijf alleen de gevraagde secties in vlot, natuurlijk Nederlands. Gebruik ## voor koppen.", fix['completion_prompt'])
    
    if completion:
        completion = completion.strip()
        if completion.startswith("```"):
            lines = completion.split("\n")
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            completion = "\n".join(lines)
        
        full = existing.rstrip() + "\n\n" + completion
        with open(path, "w") as f:
            f.write(full)
        print(f"  OK: now {len(full)} chars")
    else:
        print(f"  FAILED")
    
    time.sleep(2)

# === FIX SHORT ONTVOCHTIGER ARTICLE ===
print("\n=== FIXING SHORT ONTVOCHTIGER ARTICLE ===")
path = os.path.join(OUT_DIR, "ontvochtiger-vs-luchtbevochtiger-2026.md")
with open(path) as f:
    existing = f.read()

# Check if it has all sections
missing_sections = []
if "## Vergelijkingstabel" not in existing:
    missing_sections.append("Vergelijkingstabel")
if "## Wanneer Kies Je voor" not in existing:
    missing_sections.append("Wanneer-secties")
if "## Kostenvergelijking" not in existing:
    missing_sections.append("Kostenvergelijking")
if "## Veelgemaakte Fouten" not in existing:
    missing_sections.append("Veelgemaakte Fouten")
if "## Conclusie" not in existing:
    missing_sections.append("Conclusie")

print(f"  Missing sections: {missing_sections}")

if missing_sections:
    completion_prompt = f"""Het volgende artikel over ontvochtiger vs luchtbevochtiger is te kort en mist secties. Schrijf ALLEEN de ontbrekende secties:

- ## Vergelijkingstabel: Ontvochtiger vs. Luchtbevochtiger (2026) — tabel met 8 rijen: Prijs, Functie, Geschikt voor, Energieverbruik, Onderhoud, Geluidsniveau, Levensduur, Effect op gezondheid
- ## Wanneer Kies Je voor een Ontvochtiger? — 3-4 situaties (vochtige kelder, schimmel, was drogen binnen, condens op ramen)
- ## Wanneer Kies Je voor een Luchtbevochtiger? — 3-4 situaties (droge lucht in winter, houten vloeren/meubels, droge huid/luchtwegen, babykamer)
- ## Kostenvergelijking op Lange Termijn — aanschaf + energie + filters/onderhoud over 5 jaar
- ## Veelgemaakte Fouten bij het Kiezen — 3 fouten
- ## Conclusie — 2 paragrafen met aanbeveling per situatie
- **Affiliate disclosure**: Amazon.nl tag kieskeukennl-21

Schrijf in vlot Nederlands. Output: alleen de Markdown secties, geen frontmatter."""
    
    completion = call_ollama("Je bent een Nederlandse copywriter. Schrijf alleen de gevraagde secties in vlot, natuurlijk Nederlands. Gebruik ## voor koppen.", completion_prompt)
    
    if completion:
        completion = completion.strip()
        if completion.startswith("```"):
            lines = completion.split("\n")
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            completion = "\n".join(lines)
        
        full = existing.rstrip() + "\n\n" + completion
        with open(path, "w") as f:
            f.write(full)
        print(f"  OK: now {len(full)} chars")
    else:
        print(f"  FAILED")

# === GENERATE 2 MISSING ARTICLES ===
NEW_ARTICLES = [
    {
        "slug": "airfryer-vs-stoomoven-2026",
        "title": "Airfryer vs. Stoomoven 2026: Welke Is Gezonder en Veelzijdiger?",
        "category": "keuken",
        "price_range": "EUR 70-500",
        "reading_time": "9 min",
        "products_keywords": "Philips Airfryer XXL, Ninja Airfryer Dual, Miele stoomoven, Bosch Serie 8 stoomoven, Siemens iQ700 stoomoven, Cosori Airfryer",
        "related": "beste-airfryer-2026, beste-stoomoven-2026, airfryer-vs-heteluchtoven-2026, airfryer-vs-oven-2026, slowcooker-vs-stoomoven-2026, beste-oven-2026"
    },
    {
        "slug": "hogedrukreiniger-vs-tuinslang-2026",
        "title": "Hogedrukreiniger vs. Tuinslang 2026: Wat Is de Beste Keuze voor Jouw Terras en Oprit?",
        "category": "tuin",
        "price_range": "EUR 15-500",
        "reading_time": "8 min",
        "products_keywords": "Kärcher K5 hogedrukreiniger, Nilfisk hogedrukreiniger, Gardena tuinslang set, Hozelock tuinslang, Bosch hogedrukreiniger, Kärcher K2 hogedrukreiniger",
        "related": "beste-hogedrukreiniger-2026, beste-tuinslang-2026, stoomreiniger-vs-hogedrukreiniger-2026, beste-tuingereedschap-set-2026, beste-barbecue-2026, beste-grasmaaier-2026"
    }
]

SYSTEM_PROMPT = """Je bent een Nederlandse copywriter voor KiesKeuken (BesteApparaten.nl). Je schrijft vergelijkingsartikelen voor huishoudelijke apparaten.

FORMAT: Markdown met YAML frontmatter. Het artikel moet tussen 800-1200 woorden zijn.

FRONTMATTER TEMPLATE (exact dit formaat):
---
title: '<TITLE>'
slug: '<SLUG>'
description: '<120-155 char meta description met Amazon-link koopadvies en tag kieskeukennl-21>'
category: '<CATEGORY>'
rating: 4.5
priceRange: '<PRICE_RANGE>'
pros:
- '<PRO_1>'
- '<PRO_2>'
- '<PRO_3>'
cons:
- '<CON_1>'
- '<CON_2>'
- '<CON_3>'
affiliateLinks:
- https://www.amazon.nl/s?k=<product1_search>&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=<product2_search>&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=<product3_search>&tag=kieskeukennl-21
date: 2026-06-16
modelYear: 2026
featuredProduct: '<BEST_PRODUCT_NAME>'
readingTime: '<READING_TIME>'
products:
- name: '<PRODUCT_1_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.amazon.nl/s?k=<product1_search>&tag=kieskeukennl-21
- name: '<PRODUCT_2_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.amazon.nl/s?k=<product2_search>&tag=kieskeukennl-21
- name: '<PRODUCT_3_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.amazon.nl/s?k=<product3_search>&tag=kieskeukennl-21
- name: '<PRODUCT_4_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.amazon.nl/s?k=<product4_search>&tag=kieskeukennl-21
- name: '<PRODUCT_5_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.amazon.nl/s?k=<product5_search>&tag=kieskeukennl-21
related:
- '<RELATED_1>'
- '<RELATED_2>'
- '<RELATED_3>'
- '<RELATED_4>'
- '<RELATED_5>'
- '<RELATED_6>'
faq:
- q: '<FAQ_VRAAG_1>'
  a: '<FAQ_ANTWOORD_1>'
- q: '<FAQ_VRAAG_2>'
  a: '<FAQ_ANTWOORD_2>'
- q: '<FAQ_VRAAG_3>'
  a: '<FAQ_ANTWOORD_3>'
- q: '<FAQ_VRAAG_4>'
  a: '<FAQ_ANTWOORD_4>'
- q: '<FAQ_VRAAG_5>'
  a: '<FAQ_ANTWOORD_5>'
---

BODY STRUCTUUR (volg deze exacte volgorde):

## <Product A> vs. <Product B>: Wat Is het Verschil?
[2-3 paragrafen]

## Vergelijkingstabel: <Product A> vs. <Product B> (2026)
| Aspect | <Product A> | <Product B> |
|--------|-------------|-------------|
| Prijs | EUR X-Y | EUR X-Y |
| ... | ... | ... |
(8 rijen)

## Beste <Product A> Modellen van 2026
[2-3 modellen met prijsindicatie]

## Beste <Product B> Modellen van 2026
[2-3 modellen met prijsindicatie]

## Wanneer Kies Je voor <Product A>?
[3-4 situaties]

## Wanneer Kies Je voor <Product B>?
[3-4 situaties]

## Kostenvergelijking op Lange Termijn
[aanschaf + gebruikskosten over 5 jaar]

## Veelgemaakte Fouten bij het Kiezen
[3 fouten]

## Conclusie
[2-3 paragrafen met aanbeveling per situatie]

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou.

REGELS:
- Schrijf in vlot, natuurlijk Nederlands (geen ChatGPT-clichés).
- Gebruik concrete prijzen (EUR X-Y) en echte productnamen.
- Wees eerlijk over minpunten — geen marketingtaal.
- Geen Bol.com placeholders. Alle affiliate links naar Amazon.nl met tag kieskeukennl-21.
- Houd het artikel tussen 800-1200 woorden.
- Gebruik ## voor koppen, niet #.
- Geen "Introductie" of "Inleiding" kop — start meteen met de vergelijking.
- De FAQ sectie moet 5 vragen bevatten met concrete antwoorden."""

print("\n=== GENERATING 2 MISSING ARTICLES (Ollama qwen3:14b) ===")
for i, comp in enumerate(NEW_ARTICLES):
    print(f"\n[{i+1}/2] Generating: {comp['slug']}")
    
    user_prompt = f"""Schrijf een vergelijkingsartikel voor:

TITEL: {comp['title']}
SLUG: {comp['slug']}
CATEGORIE: {comp['category']}
PRIJSRANGE: {comp['price_range']}
LEESTIJD: {comp['reading_time']}

PRODUCTEN OM TE NOEMEN: {comp['products_keywords']}

GERELATEERDE ARTIKELEN (gebruik deze exacte slugs in de 'related' lijst):
{chr(10).join('- ' + r for r in comp['related'].split(', '))}

OUTPUT: Alleen de Markdown met frontmatter. Geen uitleg, geen "hier is het artikel"."""
    
    content = call_ollama(SYSTEM_PROMPT, user_prompt)
    
    if content is None:
        print(f"  FAILED")
        continue
    
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"): lines = lines[1:]
        if lines[-1].startswith("```"): lines = lines[:-1]
        content = "\n".join(lines)
    
    out_path = os.path.join(OUT_DIR, f"{comp['slug']}.md")
    with open(out_path, "w") as f:
        f.write(content)
    
    has_tag = "kieskeukennl-21" in content
    has_faq = "faq:" in content[:3000]
    print(f"  OK: {out_path} ({len(content)} chars, tag={'✓' if has_tag else '✗'}, faq={'✓' if has_faq else '✗'})")
    
    if i < len(NEW_ARTICLES) - 1:
        time.sleep(3)

print("\n=== DONE ===")
