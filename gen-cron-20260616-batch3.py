#!/usr/bin/env python3
"""Generate 5 comparison articles using Gemini API for KiesKeuken.
Retries 2 missing from batch2 + 3 new high-value gaps.
Hermes cron job — June 16, 2026 batch 3
"""

import os, sys, json, time, re

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
OUT_DIR = "/home/cls/kieskeuken/src/content/reviews"

COMPARISONS = [
    # --- RETRIES from batch2 (still missing) ---
    {
        "slug": "vaatwasser-inbouw-vs-vrijstaand-2026",
        "title": "Inbouw vs. Vrijstaande Vaatwasser 2026: Welke Past in Jouw Keuken?",
        "category": "keuken",
        "price_range": "EUR 350-1500",
        "reading_time": "9 min",
        "products_keywords": [
            "Bosch inbouw vaatwasser Serie 6", "Siemens inbouw vaatwasser iQ500",
            "Miele inbouw vaatwasser", "Bosch vrijstaande vaatwasser Serie 4",
            "Siemens vrijstaande vaatwasser", "AEG vrijstaande vaatwasser"
        ],
        "related": [
            "beste-vaatwasser-2026", "vaatwasser-vs-handafwas-2026",
            "beste-afzuigkap-2026", "beste-keukenmachine-2026",
            "stroomkosten-apparaten", "beste-koelkast-2026"
        ]
    },
    {
        "slug": "slowcooker-vs-snelkookpan-2026",
        "title": "Slowcooker vs. Snelkookpan 2026: Langzaam Garen of Supersnel Koken?",
        "category": "keuken",
        "price_range": "EUR 40-250",
        "reading_time": "9 min",
        "products_keywords": [
            "Crock-Pot slowcooker", "Russell Hobbs slowcooker",
            "Instant Pot Duo snelkookpan", "Tefal Secure 5 snelkookpan",
            "Philips All-in-One Cooker", "Ninja Foodi multicooker"
        ],
        "related": [
            "beste-slowcooker-2026", "slowcooker-vs-stoomoven-2026",
            "beste-stoomoven-2026", "beste-rijstkoker-2026",
            "stroomkosten-apparaten", "beste-pannenset-2026"
        ]
    },
    # --- NEW high-value gaps ---
    {
        "slug": "ontvochtiger-vs-luchtbevochtiger-2026",
        "title": "Ontvochtiger vs. Luchtbevochtiger 2026: Welke Heb Je Nodig voor een Gezond Binnenklimaat?",
        "category": "huishoudelijk",
        "price_range": "EUR 40-400",
        "reading_time": "9 min",
        "products_keywords": [
            "Pro Breeze ontvochtiger", "Qlima ontvochtiger",
            "Philips luchtbevochtiger", "Stadler Form luchtbevochtiger",
            "Duux luchtbevochtiger", "Meaco ontvochtiger"
        ],
        "related": [
            "beste-ontvochtiger-2026", "beste-luchtbevochtiger-2026",
            "luchtreiniger-vs-luchtbevochtiger-2026", "beste-luchtreiniger-2026",
            "beste-elektrische-kachel-2026", "stroomkosten-apparaten"
        ]
    },
    {
        "slug": "airfryer-vs-stoomoven-2026",
        "title": "Airfryer vs. Stoomoven 2026: Welke Is Gezonder en Veelzijdiger?",
        "category": "keuken",
        "price_range": "EUR 70-500",
        "reading_time": "9 min",
        "products_keywords": [
            "Philips Airfryer XXL", "Ninja Airfryer Dual",
            "Miele stoomoven", "Bosch Serie 8 stoomoven",
            "Siemens iQ700 stoomoven", "Cosori Airfryer"
        ],
        "related": [
            "beste-airfryer-2026", "beste-stoomoven-2026",
            "airfryer-vs-heteluchtoven-2026", "airfryer-vs-oven-2026",
            "slowcooker-vs-stoomoven-2026", "beste-oven-2026"
        ]
    },
    {
        "slug": "hogedrukreiniger-vs-tuinslang-2026",
        "title": "Hogedrukreiniger vs. Tuinslang 2026: Wat Is de Beste Keuze voor Jouw Terras en Oprit?",
        "category": "tuin",
        "price_range": "EUR 15-500",
        "reading_time": "8 min",
        "products_keywords": [
            "Kärcher K5 hogedrukreiniger", "Nilfisk hogedrukreiniger",
            "Gardena tuinslang set", "Hozelock tuinslang",
            "Bosch hogedrukreiniger", "Kärcher K2 hogedrukreiniger"
        ],
        "related": [
            "beste-hogedrukreiniger-2026", "beste-tuinslang-2026",
            "stoomreiniger-vs-hogedrukreiniger-2026", "beste-tuingereedschap-set-2026",
            "beste-barbecue-2026", "beste-grasmaaier-2026"
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

[2-3 paragrafen die het fundamentele verschil uitleggen. Geen productnamen nog, alleen de categorieën vergelijken.]

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

## Conclusie

[2-3 paragrafen samenvatting. Eindig met een duidelijke aanbeveling per situatie.]

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou. Rangschikking gebaseerd op productspecificaties, gebruikerservaringen en prijs-kwaliteitverhouding.

REGELS:
- Schrijf in vlot, natuurlijk Nederlands (geen ChatGPT-achtige clichés zoals "in de wereld van..." of "welkom bij...").
- Gebruik concrete prijzen (EUR X-Y) en echte productnamen.
- Wees eerlijk over minpunten — geen marketingtaal.
- Geen Bol.com placeholders. Alle affiliate links naar Amazon.nl met tag kieskeukennl-21.
- Houd het artikel tussen 800-1200 woorden.
- Gebruik ## voor koppen, niet # (de titel komt uit de frontmatter).
- Geen "Introductie" of "Inleiding" kop — start meteen met de vergelijking.
- De FAQ sectie moet 5 vragen bevatten met concrete antwoorden."""

def call_gemini(system_prompt, user_prompt):
    """Call Gemini API via OpenAI-compatible endpoint."""
    import urllib.request, urllib.error
    
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
        print(f"  HTTP {e.code}: {error_body[:500]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def validate_frontmatter(content, comp):
    """Basic validation of generated article."""
    issues = []
    
    if not content.startswith("---"):
        issues.append("Missing opening ---")
    
    required_fields = ["title:", "slug:", "description:", "category:", "rating:",
                       "priceRange:", "pros:", "cons:", "affiliateLinks:", "date:",
                       "products:", "related:", "faq:"]
    for field in required_fields:
        if field not in content[:3000]:
            issues.append(f"Missing field: {field}")
    
    if "kieskeukennl-21" not in content:
        issues.append("Missing affiliate tag kieskeukennl-21")
    
    if "bol.com" in content.lower() and "placeholder" in content.lower():
        issues.append("Contains Bol.com placeholder text")
    
    body_start = content.find("---", 3)
    if body_start > 0:
        body = content[body_start+3:]
        words = len(body.split())
        if words < 600:
            issues.append(f"Too short: {words} words (min 800)")
        if words > 1500:
            issues.append(f"Too long: {words} words (max 1200)")
    
    return issues

def main():
    results = []
    
    for i, comp in enumerate(COMPARISONS):
        print(f"\n[{i+1}/5] Generating: {comp['slug']}")
        
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
            print(f"  FAILED: No response from Gemini")
            results.append({"slug": comp['slug'], "status": "FAILED"})
            continue
        
        # Clean up any markdown code fences
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines)
        
        # Validate
        issues = validate_frontmatter(content, comp)
        if issues:
            print(f"  WARNINGS: {'; '.join(issues)}")
        
        # Write to file
        out_path = os.path.join(OUT_DIR, f"{comp['slug']}.md")
        with open(out_path, "w") as f:
            f.write(content)
        
        print(f"  OK: {out_path} ({len(content)} chars)")
        results.append({"slug": comp['slug'], "status": "OK", "path": out_path, "issues": issues})
        
        # Rate limit: 5s between calls
        if i < len(COMPARISONS) - 1:
            time.sleep(5)
    
    # Summary
    print("\n=== SUMMARY ===")
    ok = sum(1 for r in results if r['status'] == 'OK')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    print(f"Generated: {ok}/{len(COMPARISONS)}")
    print(f"Failed: {failed}/{len(COMPARISONS)}")
    
    for r in results:
        if r['issues']:
            print(f"  {r['slug']}: {r['issues']}")
    
    return results

if __name__ == "__main__":
    main()
