#!/usr/bin/env python3
"""Fix truncated articles and retry rate-limited ones."""
import os, sys, json, time, urllib.request, urllib.error

env_path = os.path.expanduser("~/.hermes/.env")
env = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")

GEMINI_KEY = env.get("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash"
OUT_DIR = "/workspace/kieskeuken/src/content/reviews"

def call_gemini(system_prompt, user_prompt, max_tokens=4096):
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GEMINI_KEY}"}
    body = {"model": MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "temperature": 0.7, "max_tokens": max_tokens}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"  HTTP {e.code}: {error_body[:300]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

# --- Fix truncated articles ---
FIXES = [
    {
        "slug": "vaatwasser-inbouw-vs-vrijstaand-2026",
        "completion_prompt": """Het volgende artikel is afgekapt. Schrijf ALLEEN de ontbrekende secties vanaf waar het stopt. Begin exact waar de tekst afbreekt: "...Een vrijstaande vaatwasser daarentegen is een compleet apparaat met een afgewerkte buiten"

Schrijf de rest van DIT artikel af — dus:
- Maak de lopende paragraaf af
- ## Vergelijkingstabel: Inbouw vs. Vrijstaande Vaatwasser (2026)
- ## Beste Inbouw Vaatwasser Modellen van 2026
- ## Beste Vrijstaande Vaatwasser Modellen van 2026
- ## Wanneer Kies Je voor een Inbouw Vaatwasser?
- ## Wanneer Kies Je voor een Vrijstaande Vaatwasser?
- ## Kostenvergelijking op Lange Termijn
- ## Veelgemaakte Fouten bij het Kiezen
- ## Conclusie
- **Affiliate disclosure** (Amazon.nl, tag kieskeukennl-21)

Schrijf in vlot Nederlands. Geen nieuwe frontmatter. Output: alleen de Markdown voor deze secties."""
    },
    {
        "slug": "slowcooker-vs-snelkookpan-2026",
        "completion_prompt": """Het volgende artikel is afgekapt. Schrijf ALLEEN de ontbrekende secties vanaf waar het stopt. Begin exact waar de tekst afbreekt: "...Voor wie de voorkeur geeft aan een"

Schrijf de rest van DIT artikel af — dus:
- Maak de lopende paragraaf over de Tefal Secure 5 Neo af
- Voeg Ninja Foodi multicooker toe als derde snelkookpan-model
- ## Wanneer Kies Je voor een Slowcooker?
- ## Wanneer Kies Je voor een Snelkookpan?
- ## Kostenvergelijking op Lange Termijn
- ## Veelgemaakte Fouten bij het Kiezen
- ## Conclusie
- **Affiliate disclosure** (Amazon.nl, tag kieskeukennl-21)

Schrijf in vlot Nederlands. Geen nieuwe frontmatter. Output: alleen de Markdown voor deze secties."""
    }
]

print("=== FIXING TRUNCATED ARTICLES ===")
for fix in FIXES:
    path = os.path.join(OUT_DIR, f"{fix['slug']}.md")
    with open(path) as f:
        existing = f.read()
    
    print(f"\nFixing: {fix['slug']} (existing: {len(existing)} chars)")
    completion = call_gemini("Je bent een Nederlandse copywriter. Schrijf alleen de gevraagde secties in vlot Nederlands.", fix['completion_prompt'], max_tokens=3072)
    
    if completion:
        completion = completion.strip()
        if completion.startswith("```"):
            lines = completion.split("\n")
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            completion = "\n".join(lines)
        
        # Append to existing
        full = existing.rstrip() + "\n\n" + completion
        with open(path, "w") as f:
            f.write(full)
        print(f"  OK: now {len(full)} chars")
    else:
        print(f"  FAILED")
    
    time.sleep(3)

# --- Retry rate-limited articles ---
RETRIES = [
    {
        "slug": "ontvochtiger-vs-luchtbevochtiger-2026",
        "title": "Ontvochtiger vs. Luchtbevochtiger 2026: Welke Heb Je Nodig voor een Gezond Binnenklimaat?",
        "category": "huishoudelijk",
        "price_range": "EUR 40-400",
        "reading_time": "9 min",
        "products_keywords": ["Pro Breeze ontvochtiger", "Qlima ontvochtiger", "Philips luchtbevochtiger", "Stadler Form luchtbevochtiger", "Duux luchtbevochtiger", "Meaco ontvochtiger"],
        "related": ["beste-ontvochtiger-2026", "beste-luchtbevochtiger-2026", "luchtreiniger-vs-luchtbevochtiger-2026", "beste-luchtreiniger-2026", "beste-elektrische-kachel-2026", "stroomkosten-apparaten"]
    },
    {
        "slug": "airfryer-vs-stoomoven-2026",
        "title": "Airfryer vs. Stoomoven 2026: Welke Is Gezonder en Veelzijdiger?",
        "category": "keuken",
        "price_range": "EUR 70-500",
        "reading_time": "9 min",
        "products_keywords": ["Philips Airfryer XXL", "Ninja Airfryer Dual", "Miele stoomoven", "Bosch Serie 8 stoomoven", "Siemens iQ700 stoomoven", "Cosori Airfryer"],
        "related": ["beste-airfryer-2026", "beste-stoomoven-2026", "airfryer-vs-heteluchtoven-2026", "airfryer-vs-oven-2026", "slowcooker-vs-stoomoven-2026", "beste-oven-2026"]
    },
    {
        "slug": "hogedrukreiniger-vs-tuinslang-2026",
        "title": "Hogedrukreiniger vs. Tuinslang 2026: Wat Is de Beste Keuze voor Jouw Terras en Oprit?",
        "category": "tuin",
        "price_range": "EUR 15-500",
        "reading_time": "8 min",
        "products_keywords": ["Kärcher K5 hogedrukreiniger", "Nilfisk hogedrukreiniger", "Gardena tuinslang set", "Hozelock tuinslang", "Bosch hogedrukreiniger", "Kärcher K2 hogedrukreiniger"],
        "related": ["beste-hogedrukreiniger-2026", "beste-tuinslang-2026", "stoomreiniger-vs-hogedrukreiniger-2026", "beste-tuingereedschap-set-2026", "beste-barbecue-2026", "beste-grasmaaier-2026"]
    }
]

SYSTEM_PROMPT = """Je bent een Nederlandse copywriter voor KiesKeuken (BesteApparaten.nl). Je schrijft vergelijkingsartikelen voor huishoudelijke apparaten.

FORMAT: Markdown met YAML frontmatter. Het artikel moet tussen 800-1200 woorden zijn.

FRONTMATTER TEMPLATE (exact dit formaat, vul de placeholders in):
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

[2-3 paragrafen die het fundamentele verschil uitleggen.]

## Vergelijkingstabel: <Product A> vs. <Product B> (2026)

| Aspect | <Product A> | <Product B> |
|--------|-------------|-------------|
| Prijs | EUR X-Y | EUR X-Y |
| Snelheid | ... | ... |
| Resultaat/kwaliteit | ... | ... |
| Gebruiksgemak | ... | ... |
| Energieverbruik | ... | ... |
| Onderhoud | ... | ... |
| Levensduur | ... | ... |
| Geschikt voor | ... | ... |

## Beste <Product A> Modellen van 2026

[Korte beschrijving van 2-3 topmodellen met prijsindicatie.]

## Beste <Product B> Modellen van 2026

[Korte beschrijving van 2-3 topmodellen met prijsindicatie.]

## Wanneer Kies Je voor <Product A>?

[3-4 situaties/scenario's.]

## Wanneer Kies Je voor <Product B>?

[3-4 situaties/scenario's.]

## Kostenvergelijking op Lange Termijn

[Paragraaf over aanschaf + gebruikskosten over 5 jaar.]

## Veelgemaakte Fouten bij het Kiezen

[3 veelgemaakte fouten.]

## Conclusie

[2-3 paragrafen. Eindig met duidelijke aanbeveling per situatie.]

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou.

REGELS:
- Schrijf in vlot, natuurlijk Nederlands.
- Gebruik concrete prijzen (EUR X-Y) en echte productnamen.
- Wees eerlijk over minpunten — geen marketingtaal.
- Geen Bol.com placeholders. Alle affiliate links naar Amazon.nl met tag kieskeukennl-21.
- Houd het artikel tussen 800-1200 woorden.
- Gebruik ## voor koppen, niet #.
- Geen "Introductie" of "Inleiding" kop — start meteen met de vergelijking.
- De FAQ sectie moet 5 vragen bevatten met concrete antwoorden."""

print("\n=== RETRYING RATE-LIMITED ARTICLES ===")
time.sleep(15)  # Wait for rate limit reset

for i, comp in enumerate(RETRIES):
    print(f"\n[{i+1}/3] Generating: {comp['slug']}")
    
    user_prompt = f"""Schrijf een vergelijkingsartikel voor:

TITEL: {comp['title']}
SLUG: {comp['slug']}
CATEGORIE: {comp['category']}
PRIJSRANGE: {comp['price_range']}
LEESTIJD: {comp['reading_time']}

PRODUCTEN OM TE NOEMEN: {', '.join(comp['products_keywords'])}

GERELATEERDE ARTIKELEN (gebruik deze exacte slugs in de 'related' lijst):
{chr(10).join('- ' + r for r in comp['related'])}

OUTPUT: Alleen de Markdown met frontmatter. Geen uitleg, geen "hier is het artikel"."""
    
    content = call_gemini(SYSTEM_PROMPT, user_prompt, max_tokens=4096)
    
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
    
    # Quick check
    has_tag = "kieskeukennl-21" in content
    has_faq = "faq:" in content[:3000]
    words = len(content.split("---", 2)[-1].split()) if content.count("---") >= 2 else 0
    print(f"  OK: {out_path} ({len(content)} chars, tag={'✓' if has_tag else '✗'}, faq={'✓' if has_faq else '✗'}, body~{words}w)")
    
    if i < len(RETRIES) - 1:
        time.sleep(8)

print("\n=== DONE ===")
