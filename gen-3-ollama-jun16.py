#!/usr/bin/env python3
"""Generate 3 comparison articles using Ollama (local, no rate limits)."""
import os, sys, json, time, urllib.request

MODEL = "qwen3:14b"  # Strong multilingual, good Dutch
OUT_DIR = "/workspace/kieskeuken/src/content/reviews"
OLLAMA_URL = "http://localhost:11434/api/generate"

COMPS = [
    {
        "slug": "waterkoker-vs-fluitketel-2026",
        "title": "Waterkoker vs. Fluitketel 2026: Wat Is Sneller, Stiller en Zuiniger?",
        "cat": "keuken", "price": "EUR 15-180", "read": "8 min",
        "kw": ["Philips Daily Collection waterkoker", "Russell Hobbs waterkoker",
               "Bosch Styline waterkoker", "Le Creuset fluitketel",
               "BK fluitketel inductie", "Demeyere fluitketel"],
        "rel": ["beste-waterkoker-2026", "waterkoker-vs-quooker-2026",
                "beste-inductiekookplaat-2026", "beste-gasfornuis-2026",
                "stroomkosten-apparaten", "beste-keukenapparatuur-2026"]
    },
    {
        "slug": "inductie-vs-elektrisch-fornuis-2026",
        "title": "Inductie vs. Elektrisch Fornuis 2026: Welke Kookplaat Past Bij Jouw Keuken?",
        "cat": "keuken", "price": "EUR 200-2000", "read": "10 min",
        "kw": ["Bosch inductie kookplaat Serie 6", "Siemens iQ700 inductie",
               "Etna keramisch fornuis", "Inventum elektrisch fornuis",
               "Whirlpool keramische kookplaat", "AEG inductie kookplaat"],
        "rel": ["beste-inductiekookplaat-2026", "inductie-vs-gasfornuis-2026",
                "inductie-vs-keramisch-2026", "beste-gasfornuis-2026",
                "stroomkosten-apparaten", "beste-inductieset-2026"]
    },
    {
        "slug": "broodrooster-vs-broodrooster-met-eierkoker-2026",
        "title": "Broodrooster vs. Broodrooster met Eierkoker 2026: Is een Combi de Meerprijs Waard?",
        "cat": "keuken", "price": "EUR 20-120", "read": "8 min",
        "kw": ["Philips Daily Collection broodrooster", "Russell Hobbs broodrooster",
               "Tefal broodrooster met eierkoker", "Severin broodrooster met eierkoker",
               "Bosch Styline broodrooster", "Princess broodrooster met eierkoker"],
        "rel": ["beste-broodrooster-2026", "broodrooster-vs-tosti-ijzer-2026",
                "beste-tosti-ijzer-2026", "beste-waterkoker-2026",
                "beste-eierkoker-2026", "beste-keukenapparatuur-2026"]
    },
]

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

def call_ollama(system, user):
    """Call Ollama API."""
    full_prompt = f"{system}\n\n{user}"
    body = json.dumps({
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(OLLAMA_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        print(f"  Error: {e}")
        return None

def main():
    for i, c in enumerate(COMPS):
        print(f"[{i+1}/3] {c['slug']}")
        
        user = f"""Schrijf een vergelijkingsartikel voor:

TITEL: {c['title']}
SLUG: {c['slug']}
CATEGORIE: {c['cat']}
PRIJSRANGE: {c['price']}
LEESTIJD: {c['read']}

PRODUCTEN OM TE NOEMEN: {', '.join(c['kw'])}

GERELATEERDE ARTIKELEN (gebruik deze exacte slugs in de 'related' lijst):
{chr(10).join('- ' + r for r in c['rel'])}

OUTPUT: Alleen de Markdown met frontmatter. Geen uitleg, geen "hier is het artikel"."""
        
        content = call_ollama(SYSTEM, user)
        if content is None or len(content) < 500:
            print(f"  FAILED: {'None' if content is None else f'too short ({len(content)} chars)'}")
            continue
        
        content = content.strip()
        # Clean up any markdown code fences
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```"): lines = lines[1:]
            if lines[-1].startswith("```"): lines = lines[:-1]
            content = "\n".join(lines)
        
        # Validate basics
        issues = []
        if not content.startswith("---"):
            issues.append("Missing opening ---")
        if "kieskeukennl-21" not in content:
            issues.append("Missing affiliate tag")
        if "bol.com" in content.lower() and "placeholder" in content.lower():
            issues.append("Contains Bol.com placeholder")
        
        if issues:
            print(f"  WARNINGS: {'; '.join(issues)}")
        
        out_path = os.path.join(OUT_DIR, f"{c['slug']}.md")
        with open(out_path, "w") as f:
            f.write(content)
        
        print(f"  OK: {out_path} ({len(content)} chars)")
        
        # Small delay between calls
        if i < len(COMPS) - 1:
            time.sleep(3)
    
    print("DONE")

if __name__ == "__main__":
    main()
