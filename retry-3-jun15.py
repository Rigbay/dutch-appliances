#!/usr/bin/env python3
"""Retry 3 failed comparison articles after Gemini rate limit reset."""
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
OUT_DIR = "/home/cls/kieskeuken/src/content/reviews"

COMPARISONS = [
    {
        "slug": "koelkast-vs-amerikaanse-koelkast-2026",
        "title": "Koelkast vs. Amerikaanse Koelkast 2026: Welke Past Bij Jouw Keuken en Huishouden?",
        "category": "keuken",
        "price_range": "EUR 300-2500",
        "reading_time": "10 min",
        "products_keywords": [
            "Samsung American Fridge Freezer RS8000", "LG InstaView Door-in-Door",
            "Bosch Serie 6 koelkast", "Liebherr koelkast",
            "Siemens iQ500 koelkast", "Haier Amerikaanse koelkast"
        ],
        "related": [
            "beste-koelkast-2026", "beste-koelkast-vriezer-combinatie-2026",
            "koelkast-vs-koelvriescombinatie-2026", "beste-vriezer-2026",
            "stroomkosten-apparaten"
        ]
    },
    {
        "slug": "wasdroger-vs-droogrek-2026",
        "title": "Wasdroger vs. Droogrek 2026: Wat Is Echt Goedkoper en Beter voor Je Was?",
        "category": "huishoudelijk",
        "price_range": "EUR 15-1200",
        "reading_time": "9 min",
        "products_keywords": [
            "Miele T1 warmtepompdroger", "Bosch Serie 6 warmtepompdroger",
            "Siemens iQ500 warmtepompdroger", "Brabantia droogrek",
            "Leifheit droogrek", "AEG warmtepompdroger"
        ],
        "related": [
            "beste-wasdroger-2026", "beste-wasmachine-2026",
            "condensdroger-vs-warmtepompdroger-2026", "wasmachine-vs-wasdroger-2026",
            "stroomkosten-apparaten"
        ]
    },
    {
        "slug": "magnetron-vs-heteluchtoven-2026",
        "title": "Magnetron vs. Heteluchtoven 2026: Welke Is Sneller, Welke Is Lekkerder?",
        "category": "keuken",
        "price_range": "EUR 50-500",
        "reading_time": "9 min",
        "products_keywords": [
            "Samsung combi-magnetron MC28H5015", "Panasonic NN-DS596B combi",
            "Whirlpool heteluchtoven", "Bosch Serie 4 heteluchtoven",
            "Inventum MN308C magnetron", "Sharp R-86STM combi-magnetron"
        ],
        "related": [
            "beste-magnetron-2026", "beste-oven-2026",
            "magnetron-vs-combi-magnetron-2026", "airfryer-vs-magnetron-2026",
            "oven-vs-magnetron-2026", "beste-oven-magnetron-combi-2026"
        ]
    },
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
date: 2026-06-15
modelYear: 2026
featuredProduct: '<BEST_PRODUCT_NAME>'
readingTime: '<READING_TIME>'
products:
- name: '<PRODUCT_1_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
- name: '<PRODUCT_2_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
- name: '<PRODUCT_3_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
- name: '<PRODUCT_4_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
- name: '<PRODUCT_5_NAME>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRICE_RANGE>'
  bestFor: '<BEST_FOR>'
related:
- '<RELATED_1>'
- '<RELATED_2>'
- '<RELATED_3>'
- '<RELATED_4>'
- '<RELATED_5>'
- '<RELATED_6>'
---

BODY STRUCTUUR (volg deze exacte volgorde):

## <Product A> vs. <Product B>: Wat Is het Verschil?

[2-3 paragrafen die het fundamentele verschil uitleggen. Geen productnamen nog, alleen de categorieen vergelijken.]

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

[Korte beschrijving van 2-3 topmodellen met prijsindicatie. Gebruik productnamen uit de products lijst.]

## Beste <Product B> Modellen van 2026

[Korte beschrijving van 2-3 topmodellen met prijsindicatie.]

## Wanneer Kies Je voor <Product A>?

[3-4 situaties/scenario's waarin product A de betere keuze is.]

## Wanneer Kies Je voor <Product B>?

[3-4 situaties/scenario's waarin product B de betere keuze is.]

## Kostenvergelijking op Lange Termijn

[Paragraaf over aanschaf + gebruikskosten over 5 jaar. Energie, onderhoud, verbruiksartikelen.]

## Veelgemaakte Fouten bij het Kiezen

[3 veelgemaakte fouten die kopers maken.]

## FAQ

### Wat is beter: <Product A> of <Product B>?
[2-3 zinnen]

### Is <Product A> goedkoper in gebruik dan <Product B>?
[2-3 zinnen]

### Kan <Product B> hetzelfde als <Product A>?
[2-3 zinnen]

### Hoeveel kost een goede <Product A> minimaal?
[2-3 zinnen]

### Waar kan ik <Product A> en <Product B> het beste kopen in Nederland?
[2-3 zinnen — noem Amazon.nl, Coolblue, MediaMarkt]

## Conclusie

[2-3 paragrafen samenvatting. Eindig met een duidelijke aanbeveling per situatie.]

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou. Rangschikking gebaseerd op productspecificaties, gebruikerservaringen en prijs-kwaliteitverhouding.

REGELS:
- Schrijf in vlot, natuurlijk Nederlands (geen ChatGPT-achtige cliches zoals "in de wereld van..." of "welkom bij...").
- Gebruik concrete prijzen (EUR X-Y) en echte productnamen.
- Wees eerlijk over minpunten — geen marketingtaal.
- Geen Bol.com placeholders. Alle affiliate links naar Amazon.nl met tag kieskeukennl-21.
- Houd het artikel tussen 800-1200 woorden.
- Gebruik ## voor koppen, niet # (de titel komt uit de frontmatter).
- Geen "Introductie" of "Inleiding" kop — start meteen met de vergelijking."""

def call_gemini(system_prompt, user_prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GEMINI_KEY}"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 4096
    }
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

for i, comp in enumerate(COMPARISONS):
    print(f"[{i+1}/3] Generating: {comp['slug']}")
    
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
    
    content = call_gemini(SYSTEM_PROMPT, user_prompt)
    
    if content is None:
        print(f"  FAILED")
        continue
    
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        content = "\n".join(lines)
    
    out_path = os.path.join(OUT_DIR, f"{comp['slug']}.md")
    with open(out_path, "w") as f:
        f.write(content)
    
    has_related = "related:" in content
    has_tag = "kieskeukennl-21" in content
    has_bol_placeholder = "bol.com" in content.lower() and "placeholder" in content.lower()
    body_start = content.find("---", 3)
    words = len(content[body_start+3:].split()) if body_start > 0 else 0
    
    print(f"  OK: {out_path} ({len(content)} chars, ~{words} words)")
    print(f"  Checks: related={has_related}, tag={has_tag}, bol_placeholder={has_bol_placeholder}")
    
    if i < len(COMPARISONS) - 1:
        time.sleep(8)

print("\nDone!")
