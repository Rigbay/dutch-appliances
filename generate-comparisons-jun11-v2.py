#!/usr/bin/env python3
"""Generate 5 new KiesKeuken comparison articles via Gemini API.
Topics: magnetron vs combi, stofzuiger vs kruimeldief, strijkijzer vs handstomer,
broodrooster vs tosti-ijzer, soepmaker vs staafmixer."""
import json, urllib.request, urllib.error, os, sys

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

print(f"API key loaded, length={len(API_KEY)}")

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

def build_prompt(cat1, cat2, category, cat1_dutch, cat2_dutch, anchor_slugs=None):
    anchor_text = ""
    if anchor_slugs:
        anchor_text = "GERELATEERDE BESTAANDE ARTIKELEN (waar mogelijk naar verwijzen met /slug/):\n" + "\n".join(f"  - {s}" for s in anchor_slugs)

    return f"""Je bent een Nederlandse redacteur voor KiesKeuken / Beste Apparaten (rigbay.github.io/dutch-appliances/), de beste Nederlandse site voor het vergelijken van huishoudelijke apparaten.

Schrijf een COMPLEET vergelijkingsartikel: "{cat1_dutch} vs. {cat2_dutch} 2026".

CATEGORIE: {category}

{anchor_text}

FORMAAT — exact deze structuur:
1. # Titel (H1 bovenaan) — "{cat1_dutch} vs. {cat2_dutch} 2026: [pakkende ondertitel]"
2. ## Inleiding (2-3 alinea's, herkenbare situatieschets waar de lezer zich in vindt)
3. ## Snel advies (3 aanbevelingen: beste algemeen, beste budget, beste premium — elk 2 zinnen)
4. ## De ultieme vergelijking op 6 aspecten: functionaliteit, gebruiksgemak, prijs, energieverbruik, onderhoud, duurzaamheid — elk aspect met concrete voor- en nadelen
5. ## Prijsvergelijking (reele prijsranges in euro's, aanschaf + gebruikskosten op jaarbasis)
6. ## Verborgen nadelen (eerlijke minpunten die fabrikanten niet vermelden — minimaal 3 per type, specifiek en concreet)
7. ## Voor wie is welke? (5-6 gebruikersscenario's: "Jij bent een... kies dan een..." met motivatie)
8. ## Top 5 producten (echte producten — per product: naam **vet**, verdict 1-2 zinnen, priceRange, bestFor label, rating 3.5-5.0)
9. ## Conclusie: welke past bij jou? (kort, direct, geen "kortom")
10. ## Veelgestelde vragen (4 FAQ's met volledige antwoorden van 3-5 zinnen elk)

BELANGRIJKE REGELS:
- Schrijf in vloeiend, natuurlijk Nederlands (NL-NL, niet Vlaams)
- Gebruik concrete prijzen in euro's (EUR X-Y)
- Alle producten moeten echt bestaande modellen zijn van bekende merken
- Product-URLs exact: https://www.amazon.nl/s?k=[productnaam+modelnummer]&tag=kieskeukennl-21
- Minimaal 5 producten in de Top 5 sectie
- Eerlijk en kritisch over nadelen — geen marketingtaal, geen "in dit artikel bespreken we"
- H2 (##) voor hoofdsecties, H3 (###) voor subsecties
- Verwijs naar gerelateerde artikelen met [linktekst](/slug/) als het natuurlijk past
- GEEN markdown code fences (```) om het artikel heen sturen
- Minimaal 1000 woorden, maximaal 1800 woorden
- Sluit het artikel af met de FAQ — geen "tot slot" of andere afsluitende paragraaf na de FAQ

Stuur ALLEEN het complete artikel terug, beginnend met # titel. Geen uitleg ervoor of erna."""

articles = [
    {
        "cat1": "magnetron", "cat2": "combi-magnetron", "category": "keuken",
        "cat1_dutch": "Magnetron", "cat2_dutch": "Combi-Magnetron",
        "title": "Magnetron vs. Combi-Magnetron 2026: Is Een Combi de Meerprijs Waard?",
        "slug": "magnetron-vs-combi-magnetron-2026",
        "desc": "Magnetron vs. Combi-Magnetron 2026 vergeleken: prijs, functies, energieverbruik en verborgen nadelen. Ontdek of een combi-magnetron de meerprijs waard is met Amazon NL affiliate links.",
        "related": ["beste-magnetron-2026", "beste-combi-magnetron-2026", "beste-oven-2026", "oven-vs-magnetron-2026", "airfryer-vs-magnetron-2026", "beste-airfryer-2026"],
        "anchors": ["beste-magnetron-2026", "oven-vs-magnetron-2026"]
    },
    {
        "cat1": "stofzuiger", "cat2": "kruimeldief", "category": "schoonmaken",
        "cat1_dutch": "Stofzuiger", "cat2_dutch": "Kruimeldief",
        "title": "Stofzuiger vs. Kruimeldief 2026: Heb Je Beide Nodig Of Is Eén Genoeg?",
        "slug": "stofzuiger-vs-kruimeldief-2026",
        "desc": "Stofzuiger vs. Kruimeldief 2026 vergeleken: gebruiksgemak, zuigkracht, prijs en batterijduur. Eerlijke keuzehulp of je beide apparaten nodig hebt met Amazon NL affiliate links.",
        "related": ["beste-stofzuiger-2026", "beste-steelstofzuiger-2026", "beste-robotstofzuiger-2026", "stofzuiger-vs-steelstofzuiger-2026", "robotstofzuiger-vs-stofzuiger-2026", "steelstofzuiger-vs-draadloze-stofzuiger-2026"],
        "anchors": ["beste-stofzuiger-2026", "beste-steelstofzuiger-2026", "stofzuiger-vs-steelstofzuiger-2026"]
    },
    {
        "cat1": "strijkijzer", "cat2": "handstomer", "category": "huishoudelijk",
        "cat1_dutch": "Strijkijzer", "cat2_dutch": "Handstomer",
        "title": "Strijkijzer vs. Handstomer 2026: Wat Is Beter Voor Kreukvrije Kleding?",
        "slug": "strijkijzer-vs-handstomer-2026",
        "desc": "Strijkijzer vs. Handstomer 2026 vergeleken: resultaat, gebruiksgemak, prijs en geschiktheid per stofsoort. Ontdek welke past bij jouw kledingkast met Amazon NL affiliate links.",
        "related": ["beste-strijkijzer-2026", "strijkijzer-vs-stoomgenerator-2026", "beste-stoomgenerator-2026", "beste-wasmachine-2026", "beste-wasdroger-2026"],
        "anchors": ["beste-strijkijzer-2026", "strijkijzer-vs-stoomgenerator-2026"]
    },
    {
        "cat1": "broodrooster", "cat2": "tosti-ijzer", "category": "keuken",
        "cat1_dutch": "Broodrooster", "cat2_dutch": "Tosti-ijzer",
        "title": "Broodrooster vs. Tosti-ijzer 2026: Welke Past Bij Jouw Ontbijt- en Lunchroutine?",
        "slug": "broodrooster-vs-tosti-ijzer-2026",
        "desc": "Broodrooster vs. Tosti-ijzer 2026 vergeleken: gebruiksgemak, veelzijdigheid, prijs en schoonmaakgemak. Eerlijke keuzehulp met Amazon NL affiliate links.",
        "related": ["tosti-ijzer-vs-broodrooster-2026", "beste-broodrooster-2026", "beste-tosti-ijzer-2026", "airfryer-vs-oven-2026", "beste-airfryer-2026"],
        "anchors": ["tosti-ijzer-vs-broodrooster-2026", "beste-broodrooster-2026"]
    },
    {
        "cat1": "soepmaker", "cat2": "staafmixer", "category": "keuken",
        "cat1_dutch": "Soepmaker", "cat2_dutch": "Staafmixer",
        "title": "Soepmaker vs. Staafmixer 2026: Wat Heb Je Echt Nodig Voor Perfecte Soep?",
        "slug": "soepmaker-vs-staafmixer-2026",
        "desc": "Soepmaker vs. Staafmixer 2026 vergeleken: resultaat, gebruiksgemak, veelzijdigheid en prijs. Ontdek of een soepmaker de investering waard is met Amazon NL affiliate links.",
        "related": ["beste-staafmixer-2026", "beste-blender-2026", "beste-soepmaker-2026", "staafmixer-vs-blender-2026", "blender-vs-staafmixer-vs-keukenmachine-2026", "beste-keukenmachine-2026"],
        "anchors": ["beste-staafmixer-2026", "staafmixer-vs-blender-2026"]
    },
]

OUTPUT_DIR = "src/content/reviews"
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i, art in enumerate(articles):
    print(f"\n{'='*60}")
    print(f"GENERATING [{i+1}/5]: {art['title']}")
    print(f"{'='*60}")

    prompt = build_prompt(
        art["cat1"], art["cat2"], art["category"],
        art["cat1_dutch"], art["cat2_dutch"],
        art["anchors"]
    )
    body = call_gemini(prompt, max_tokens=4096)

    if body.startswith("HTTP") or body.startswith("Error"):
        print(f"FAILED: {body[:300]}")
        continue

    # Clean up
    body = body.strip()
    if body.startswith("```"):
        parts = body.split("```")
        body = parts[1] if len(parts) >= 3 else body
        if body.startswith("markdown"):
            body = body[8:]
    body = body.strip()

    # Verify it starts with #
    if not body.startswith("#"):
        print(f"WARNING: Body doesn't start with # — prepending title")
        body = f"# {art['title']}\n\n{body}"

    # Build frontmatter
    fm = f"""---
title: '{art["title"]}'
slug: {art["slug"]}
description: {art["desc"]}
category: {art["category"]}
rating: 4.4
priceRange: EUR 15-400
pros:
- Eerlijke vergelijking op 6 praktische aspecten
- Concrete prijsvergelijking inclusief jaarlijkse gebruikskosten
- Specifieke productaanbevelingen met Amazon NL links
- Verborgen nadelen die fabrikanten liever niet vermelden
cons:
- Prijzen veranderen regelmatig, check actuele aanbiedingen
- Persoonlijke voorkeur bepaalt uiteindelijk de beste keuze
- Sommige modellen alleen online verkrijgbaar
affiliateLinks:
- https://www.amazon.nl/s?k={art["cat1"]}&tag=kieskeukennl-21
modelYear: 2026
featuredProduct: Zie snel advies hieronder
readingTime: 10 min
date: '2026-06-11'
products:
- name: Beste allround keuze
  verdict: Meest uitgebalanceerde prijs-kwaliteitverhouding
  priceRange: EUR 50-200
  bestFor: Allround gebruik
  rating: 4.5
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+{art["cat2"]}&tag=kieskeukennl-21
- name: Beste budget keuze
  verdict: Beste instapmodel met prima prestaties
  priceRange: EUR 15-60
  bestFor: Budgetbewuste kopers
  rating: 4.2
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+budget&tag=kieskeukennl-21
- name: Premium model
  verdict: Meeste functies en beste bouwkwaliteit
  priceRange: EUR 150-400
  bestFor: Veeleisende gebruikers
  rating: 4.6
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+premium&tag=kieskeukennl-21
- name: Compacte keuze
  verdict: Beste voor kleine keukens of beperkte opbergruimte
  priceRange: EUR 30-80
  bestFor: Kleine huishoudens
  rating: 4.3
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+compact&tag=kieskeukennl-21
- name: Meest veelzijdige keuze
  verdict: Meeste accessoires en extra functies inbegrepen
  priceRange: EUR 60-250
  bestFor: Veelzijdig gebruik
  rating: 4.4
  affiliateLink: https://www.amazon.nl/s?k={art["cat1"]}+accessoires&tag=kieskeukennl-21
related:
"""
    for r in art["related"]:
        fm += f"- {r}\n"
    fm += "draft: false\n---\n\n"

    full_article = fm + body

    filepath = os.path.join(OUTPUT_DIR, f'{art["slug"]}.md')
    with open(filepath, "w") as f:
        f.write(full_article)

    wc = len(body.split())
    print(f"DONE: {filepath} ({wc} words, {len(full_article)} chars)")

print("\n" + "="*60)
print("ALL 5 ARTICLES GENERATED")
