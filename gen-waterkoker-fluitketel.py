#!/usr/bin/env python3
"""Generate waterkoker-vs-fluitketel comparison article."""
import os, sys, json, time, urllib.request, urllib.error

env_path = os.path.expanduser("~/.hermes/.env")
GEMINI_KEY = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("GEMINI_API_KEY=***            GEMINI_KEY = line.split("=", 1)[1].strip()
            break

if not GEMINI_KEY:
    print("FATAL: No GEMINI_API_KEY")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
OUT_DIR = "/home/cls/kieskeuken/src/content/reviews"

SYSTEM = """Je bent een Nederlandse copywriter voor KiesKeuken (BesteApparaten.nl). Je schrijft vergelijkingsartikelen voor huishoudelijke apparaten.

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

BODY STRUCTUUR:
## <Product A> vs. <Product B>: Wat Is het Verschil?
[2-3 paragrafen]
## Vergelijkingstabel: <Product A> vs. <Product B> (2026)
| Aspect | <Product A> | <Product B> |
## Beste <Product A> Modellen van 2026
## Beste <Product B> Modellen van 2026
## Wanneer Kies Je voor <Product A>?
## Wanneer Kies Je voor <Product B>?
## Kostenvergelijking op Lange Termijn
## Veelgemaakte Fouten bij het Kiezen
## Conclusie
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

def call_gemini(system, user):
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {GEMINI_KEY}"}
    body = {"model": MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0.7, "max_tokens": 4096}
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

user = """Schrijf een vergelijkingsartikel voor:

TITEL: Waterkoker vs. Fluitketel 2026: Wat Is Sneller, Stiller en Zuiniger?
SLUG: waterkoker-vs-fluitketel-2026
CATEGORIE: keuken
PRIJSRANGE: EUR 15-180
LEESTIJD: 8 min

PRODUCTEN OM TE NOEMEN: Philips Daily Collection waterkoker, Russell Hobbs waterkoker, Bosch Styline waterkoker, Le Creuset fluitketel, BK fluitketel inductie, Demeyere fluitketel

GERELATEERDE ARTIKELEN (gebruik deze exacte slugs in de 'related' lijst):
- beste-waterkoker-2026
- waterkoker-vs-quooker-2026
- beste-inductiekookplaat-2026
- beste-gasfornuis-2026
- stroomkosten-apparaten
- beste-keukenapparatuur-2026

OUTPUT: Alleen de Markdown met frontmatter. Geen uitleg, geen "hier is het artikel"."""

content = call_gemini(SYSTEM, user)
if content is None:
    print("FAILED")
    sys.exit(1)

content = content.strip()
if content.startswith("```"):
    lines = content.split("\n")
    if lines[0].startswith("```"): lines = lines[1:]
    if lines[-1].startswith("```"): lines = lines[:-1]
    content = "\n".join(lines)

out_path = os.path.join(OUT_DIR, "waterkoker-vs-fluitketel-2026.md")
with open(out_path, "w") as f:
    f.write(content)
print(f"OK: {out_path} ({len(content)} chars)")
