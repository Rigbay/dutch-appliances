#!/usr/bin/env python3
"""Generate 5 new Dutch comparison articles for KiesKeuken using Gemini API.
Cron-safe: no user interaction, handles errors gracefully, verifies output."""

import os, sys, re, time, json
from pathlib import Path
from datetime import datetime

# --- Config ---
REVIEWS_DIR = Path("/workspace/kieskeuken/src/content/reviews")
ENV_FILE = Path(os.path.expanduser("~/.hermes/.env"))
TAG = "kieskeukennl-21"
TODAY = datetime.now().strftime("%Y-%m-%d")
MODEL = "gemini-2.5-flash"

# Load API key
def load_api_key():
    if not ENV_FILE.exists():
        print(f"ERROR: {ENV_FILE} not found")
        sys.exit(1)
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: GEMINI_API_KEY not found in .env")
    sys.exit(1)

# --- Article definitions ---
ARTICLES = [
    {
        "slug": "elektrische-grasmaaier-vs-benzine-grasmaaier-2026",
        "category": "tuin",
        "topic": "elektrische grasmaaier vs benzine grasmaaier",
        "priceRange": "EUR 80-800",
        "featuredProduct": "Bosch Rotak 43 LI (accu) / Honda HRX 476 (benzine)",
        "readingTime": "11 min",
        "related": [
            "beste-grasmaaier-2026",
            "beste-robotgrasmaaier-2026",
            "beste-bosmaaier-2026",
            "beste-tuingereedschap-set-2026",
            "robotgrasmaaier-vs-grasmaaier-2026"
        ],
        "product_ideas": [
            ("Bosch Rotak 43 LI", "Beste accusnoerloze keuze voor middelgrote gazons.", "EUR 250-400", "Accu / Gemak", 4.7),
            ("Honda HRX 476", "Beste benzine grasmaaier voor grote gazons en professioneel gebruik.", "EUR 600-800", "Groot gazon", 4.8),
            ("Makita DLM533Z", "Krachtige 2x18V accu maaier voor halve hectare.", "EUR 350-500", "Accu / Kracht", 4.6),
            ("Bosch ARM 37", "Beste instapmodel elektrisch met snoer voor kleine tuinen.", "EUR 80-120", "Budget / Snoer", 4.3),
            ("Stihl RM 4 RT", "Premium benzine maaier met opvangbak en mulchfunctie.", "EUR 500-700", "Premium / Benzine", 4.7),
        ]
    },
    {
        "slug": "robotstofzuiger-vs-steelstofzuiger-2026",
        "category": "schoonmaken",
        "topic": "robotstofzuiger vs steelstofzuiger",
        "priceRange": "EUR 150-1200",
        "featuredProduct": "Roborock Qrevo S / Dyson V15 Detect",
        "readingTime": "11 min",
        "related": [
            "beste-robotstofzuiger-2026",
            "beste-steelstofzuiger-2026",
            "beste-stofzuiger-2026",
            "robotstofzuiger-vs-stofzuiger-2026",
            "stofzuiger-vs-steelstofzuiger-2026"
        ],
        "product_ideas": [
            ("Roborock Qrevo S", "Beste allround robot met dweilfunctie en zelfreinigend station.", "EUR 700-900", "All-in-one", 4.8),
            ("Dyson V15 Detect", "Beste steelstofzuiger met laserteller en LCD-scherm.", "EUR 550-750", "Premium / Dyson", 4.7),
            ("iRobot Roomba j9+", "Zelfledigende robot met slimme obstakeldetectie.", "EUR 700-900", "Handsfree", 4.6),
            ("Bosch Unlimited 7 BSS711", "Beste prijs-kwaliteit steelstofzuiger met vervangbare accu.", "EUR 250-350", "Prijs-kwaliteit", 4.5),
            ("Dreame L10s Ultra", "Robot met stofzuig- én dweilfunctie, compleet basisstation.", "EUR 600-800", "Dweilen & zuigen", 4.6),
        ]
    },
    {
        "slug": "staafmixer-vs-blender-2026",
        "category": "keuken",
        "topic": "staafmixer vs blender",
        "priceRange": "EUR 20-400",
        "featuredProduct": "Braun MultiQuick 9 / Vitamix E310",
        "readingTime": "10 min",
        "related": [
            "beste-staafmixer-2026",
            "beste-blender-2026",
            "beste-keukenmachine-2026",
            "handmixer-vs-keukenmachine-2026",
            "blender-vs-staafmixer-vs-keukenmachine-2026",
            "beste-hakmolen-2026"
        ],
        "product_ideas": [
            ("Braun MultiQuick 9", "Beste staafmixer met krachtige 1200W motor en slimme snelheidsregeling.", "EUR 80-130", "Premium / Allround", 4.7),
            ("Vitamix E310", "Professionele blender met variabele snelheid voor smoothies en soepen.", "EUR 300-400", "Blender / Professioneel", 4.8),
            ("Bosch MSM6S00", "Beste compacte staafmixer voor dagelijks soep en saus gebruik.", "EUR 30-50", "Budget / Compact", 4.4),
            ("NutriBullet Pro 900", "Populaire personal blender voor smoothies en notenpasta.", "EUR 70-100", "Smoothies", 4.5),
            ("Moulinex DD45", "Staafmixer met handige hakmolen-accessoire voor dubbel gebruik.", "EUR 40-60", "Prijs-kwaliteit", 4.3),
        ]
    },
    {
        "slug": "wasmachine-vs-wasdroger-2026",
        "category": "huishoudelijk",
        "topic": "wasmachine vs wasdroger",
        "priceRange": "EUR 350-1800",
        "featuredProduct": "Samsung Bespoke AI / Miele TSL683 WP",
        "readingTime": "12 min",
        "related": [
            "beste-wasmachine-2026",
            "beste-wasdroger-2026",
            "wasmachine-vs-wasdroger-combi-2026",
            "condensdroger-vs-warmtepompdroger-2026",
            "beste-koelkast-vriezer-combinatie-2026"
        ],
        "product_ideas": [
            ("Samsung Bespoke AI WW11BBA046AE", "Slimme wasmachine met AI-wasprogramma's en 11 kg capaciteit.", "EUR 700-1000", "Smart Home", 4.8),
            ("Miele TSL683 WP", "Premium warmtepompdroger met PerfectDry-systeem en 9 kg lading.", "EUR 1000-1400", "Premium / Miele", 4.9),
            ("Bosch Serie 6 WGG2460XNL", "Beste prijs-kwaliteit wasmachine met i-DOS automatisch doseren.", "EUR 600-800", "Prijs-kwaliteit", 4.4),
            ("LG RH80V9AV2N", "Energiezuinige warmtepompdroger met Dual Inverter motor.", "EUR 700-1000", "Energiezuinig", 4.5),
            ("AEG L6FBG142S", "Instapmodel wasmachine met ProSense-ladingsherkenning.", "EUR 450-600", "Budget / AEG", 4.3),
        ]
    },
    {
        "slug": "koffiemachine-vs-volautomatische-koffiemachine-2026",
        "category": "keuken",
        "topic": "koffiemachine vs volautomatische koffiemachine",
        "priceRange": "EUR 120-2500",
        "featuredProduct": "Jura E8 / De'Longhi Magnifica Start",
        "readingTime": "12 min",
        "related": [
            "beste-koffiemachine-2026",
            "beste-koffiemachine-bonen-2026",
            "beste-volautomatische-koffiemachine-2026",
            "beste-koffiecupmachine-2026",
            "beste-filterkoffiemachine-2026",
            "koffiemachine-bonen-vs-cups-2026"
        ],
        "product_ideas": [
            ("De'Longhi Magnifica Start", "Beste instapmodel volautomaat voor versgemalen bonen espresso.", "EUR 300-450", "Instap / Volautomaat", 4.6),
            ("Jura E8", "Premium volautomaat met P.E.P. extractie en 17 specialiteiten.", "EUR 900-1300", "Premium / Jura", 4.8),
            ("Philips 5400 Serie LatteGo", "Volautomaat met eenvoudig te reinigen melksysteem en touchscreen.", "EUR 500-700", "Melkspecialiteiten", 4.6),
            ("Moccamaster KBG Select", "Beste klassieke filterkoffiemachine met handbediening en 10-kops capaciteit.", "EUR 200-260", "Filter / Kwaliteit", 4.7),
            ("Nespresso Vertuo Next", "Beste koffiecupsysteem voor gemak met crema en variatie.", "EUR 120-180", "Gemak / Cups", 4.4),
        ]
    }
]

def build_prompt(article_def):
    """Build a detailed prompt for Gemini to generate one article."""
    prods = article_def["product_ideas"]
    prods_formatted = "\n".join(
        f"- {n}: {v} Prijs: {p}. Beste voor: {b}. Rating: {r}/5. "
        f"Affiliate: https://www.amazon.nl/s?k={n.replace(' ', '+')}&tag={TAG}"
        for n, v, p, b, r in prods
    )
    
    related_formatted = "\n".join(f"- {r}" for r in article_def["related"])
    
    prompt = f"""Je bent een Nederlandse contentschrijver voor KiesKeuken (kieskeuken.nl), een affiliate koopgids-website over huishoudelijke apparaten. 
    
Schrijf een complete, SEO-geoptimaliseerde vergelijkingsartikel in het Nederlands over: **{article_def['topic']} in 2026**.

BELANGRIJK: Output ALLEEN de complete Markdown. Geen uitleg, geen "hier is het artikel", alleen de Markdown.

## FORMAT — volg dit PRECIES:

---
title: '{article_def['topic'].title()} 2026: [vul hier een pakkende ondertitel in met voordeel of vraag]'
slug: {article_def['slug']}
description: [140-160 tekens, SEO meta description in Nederlands, bevat "{article_def['topic']}"]
category: {article_def['category']}
rating: 4.5
priceRange: {article_def['priceRange']}
pros:
- [3-4 voordelen van deze vergelijking voor de lezer, kort]
- [focus op helderheid, bespaar tijd, vind beste keuze]
- [minimaal 3]
cons:
- [2-3 beperkingen van de vergelijking, eerlijk]
- [bijv. prijzen wisselen, persoonlijke voorkeur telt]
affiliateLinks:
- https://www.amazon.nl/s?k={article_def['topic'].replace(' ', '+').replace('vs', '+')}&tag={TAG}
modelYear: 2026
featuredProduct: {article_def['featuredProduct']}
readingTime: {article_def['readingTime']}
date: '{TODAY}'
products:
- name: {prods[0][0]}
  verdict: {prods[0][1]}
  priceRange: {prods[0][2]}
  bestFor: {prods[0][3]}
  rating: {prods[0][4]}
  affiliateLink: https://www.amazon.nl/s?k={prods[0][0].replace(' ', '+')}&tag={TAG}
- name: {prods[1][0]}
  verdict: {prods[1][1]}
  priceRange: {prods[1][2]}
  bestFor: {prods[1][3]}
  rating: {prods[1][4]}
  affiliateLink: https://www.amazon.nl/s?k={prods[1][0].replace(' ', '+')}&tag={TAG}
- name: {prods[2][0]}
  verdict: {prods[2][1]}
  priceRange: {prods[2][2]}
  bestFor: {prods[2][3]}
  rating: {prods[2][4]}
  affiliateLink: https://www.amazon.nl/s?k={prods[2][0].replace(' ', '+')}&tag={TAG}
- name: {prods[3][0]}
  verdict: {prods[3][1]}
  priceRange: {prods[3][2]}
  bestFor: {prods[3][3]}
  rating: {prods[3][4]}
  affiliateLink: https://www.amazon.nl/s?k={prods[3][0].replace(' ', '+')}&tag={TAG}
- name: {prods[4][0]}
  verdict: {prods[4][1]}
  priceRange: {prods[4][2]}
  bestFor: {prods[4][3]}
  rating: {prods[4][4]}
  affiliateLink: https://www.amazon.nl/s?k={prods[4][0].replace(' ', '+')}&tag={TAG}
related:
{related_formatted}
---

# [Titel: Pakkende H1 met vraagteken of belofte]

Korte **introductie (~100 woorden)** die de lezer aanspreekt: waarom deze vergelijking belangrijk is in 2026, wat de lezer gaat leren, en een natuurlijke verwijzing naar de twee categorieën die vergeleken worden. Gebruik **vetgedrukte** kernzinnen.

---

## De ultieme vergelijking op 5-6 aspecten

Hieronder een uitgebreide vergelijking op basis van [kies 5 of 6 relevante aspecten zoals: snelheid, prijs, gebruikersgemak, onderhoud, resultaat/kwaliteit, capaciteit, geluidsniveau, energieverbruik, levensduur, formaat]. Kies de 5-6 meest relevante voor DIT specifieke onderwerp.

### 1. [Aspect 1]
*Bullet points met voor- en nadelen per apparaattype. Wees specifiek en noem concrete getallen.*
Winnaar: *[naam of type]*

### 2. [Aspect 2]  
...
Winnaar: *[naam of type]*

### 3. [Aspect 3]
...
Winnaar: *[naam of type]*

### 4. [Aspect 4]
...
Winnaar: *[naam of type]*

### 5. [Aspect 5]
...
Winnaar: *[naam of type]*

### 6. [Aspect 6 — optioneel, alleen als relevant]
...
Winnaar: *[naam of type]*

---

## [Aantal] Topmodellen van 2026 onder de loep

Of je nu kiest voor [type 1] of [type 2]; dit zijn de uitblinkers van dit jaar.

### 1. [{prods[0][0]}](https://www.amazon.nl/s?k={prods[0][0].replace(' ', '+')}&tag={TAG})
[2-3 paragrafen over dit product: waarom het de beste in zijn klasse is, specs, gebruikservaring, voor wie het ideaal is. Gebruik bullet points voor key features.]

### 2. [{prods[1][0]}](https://www.amazon.nl/s?k={prods[1][0].replace(' ', '+')}&tag={TAG})
[2-3 paragrafen...]

### 3. [{prods[2][0]}](https://www.amazon.nl/s?k={prods[2][0].replace(' ', '+')}&tag={TAG})
[2-3 paragrafen...]

### 4. [{prods[3][0]}](https://www.amazon.nl/s?k={prods[3][0].replace(' ', '+')}&tag={TAG})
[2-3 paragrafen...]

### 5. [{prods[4][0]}](https://www.amazon.nl/s?k={prods[4][0].replace(' ', '+')}&tag={TAG})
[2-3 paragrafen...]

---

## Wie moet wat kopen? Ons eindoordeel

| Situatie / Behoefte | Beste keuze |
|---|---|
| [Situatie 1 - budget] | [{prods[3][0]}](https://www.amazon.nl/s?k={prods[3][0].replace(' ', '+')}&tag={TAG}) |
| [Situatie 2 - premium] | [{prods[1][0]}](https://www.amazon.nl/s?k={prods[1][0].replace(' ', '+')}&tag={TAG}) |
| [Situatie 3 - allround] | [{prods[0][0]}](https://www.amazon.nl/s?k={prods[0][0].replace(' ', '+')}&tag={TAG}) |
| [Situatie 4 - specifiek] | [{prods[2][0]}](https://www.amazon.nl/s?k={prods[2][0].replace(' ', '+')}&tag={TAG}) |

[Conclusie paragraaf: vat samen, geef eindoordeel, wanneer kies je wat, en een laatste affiliate call-to-action.]

---

## Veelgestelde vragen (FAQ)

**Wat is het [belangrijkste] verschil tussen [type A] en [type B]?**
[Antwoord in 2-3 zinnen]

**Is een [type A] de investering waard in 2026?**
[Antwoord in 2-3 zinnen]

**[Nog 1-2 FAQ's]**
[Antwoorden]

---

## 📚 Lees ook

Meer keuzehulpen in deze categorie:
[Vul aan met de related slugs als interne links met relevante ankertekst]

## Gerelateerde artikelen
[Zelfde lijst als 📚 Lees ook maar in een ander format]
"""

    return prompt


def generate_article(genai_client, article_def, retries=2):
    """Generate one article via Gemini, with retry logic."""
    prompt = build_prompt(article_def)
    
    for attempt in range(retries + 1):
        try:
            response = genai_client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={"temperature": 0.7, "maxOutputTokens": 4096}
            )
            text = response.text
            
            # Verify it looks like an article (has --- frontmatter)
            if not text.strip().startswith("---"):
                print(f"  WARNING: Generated text doesn't start with --- on attempt {attempt+1}")
                if attempt < retries:
                    continue
            
            # Check minimum length
            if len(text) < 2000:
                print(f"  WARNING: Generated text too short ({len(text)} chars) on attempt {attempt+1}")
                if attempt < retries:
                    continue
            
            # Verify it has the required YAML frontmatter fields
            if "slug:" not in text or "title:" not in text or "category:" not in text:
                print(f"  WARNING: Missing frontmatter fields on attempt {attempt+1}")
                if attempt < retries:
                    continue
                    
            return text
            
        except Exception as e:
            print(f"  ERROR on attempt {attempt+1}: {e}")
            if attempt < retries:
                time.sleep(3 * (attempt + 1))  # Exponential-ish backoff
            else:
                raise
    
    raise Exception(f"Failed to generate article after {retries+1} attempts")


def write_article(article_def, content):
    """Write generated article to file and verify it."""
    out_path = REVIEWS_DIR / f"{article_def['slug']}.md"
    
    # Verify content isn't empty
    if not content or len(content) < 1000:
        print(f"  ERROR: Content too short for {article_def['slug']} ({len(content)} chars)")
        return False
    
    # Check for common Gemini refusals or errors
    if "I cannot" in content[:500] or "I'm not able" in content[:500]:
        print(f"  ERROR: Gemini refusal detected in {article_def['slug']}")
        print(f"  First 200 chars: {content[:200]}")
        return False
    
    out_path.write_text(content, encoding='utf-8')
    print(f"  ✓ Wrote {out_path} ({len(content)} chars)")
    
    # Quick verification: re-read and check required frontmatter fields
    reread = out_path.read_text(encoding='utf-8')
    required_fields = ['title:', 'slug:', 'description:', 'category:', 'rating:', 'priceRange:', 
                       'pros:', 'cons:', 'affiliateLinks:', 'products:', 'related:']
    missing = [f for f in required_fields if f not in reread.split('---')[1] if f not in reread[:2000]]
    if missing:
        print(f"  WARNING: Missing fields in frontmatter: {missing}")
    
    return True


def main():
    print(f"=== KiesKeuken Comparison Generator ===")
    print(f"Date: {TODAY} | Model: {MODEL}")
    print(f"Output: {REVIEWS_DIR}")
    print()
    
    # Load API key and init client
    api_key = load_api_key()
    from google import genai
    client = genai.Client(api_key=api_key)
    print(f"✓ Gemini client initialized")
    print()
    
    success_count = 0
    for i, article_def in enumerate(ARTICLES, 1):
        slug = article_def['slug']
        print(f"[{i}/{len(ARTICLES)}] Generating: {slug}")
        
        # Skip if already exists (idempotent)
        out_path = REVIEWS_DIR / f"{slug}.md"
        if out_path.exists():
            existing = out_path.read_text(encoding='utf-8')
            # Only skip if it looks complete (has frontmatter and body)
            if existing.count('---') >= 2 and len(existing) > 2000:
                print(f"  ⏭ Already exists with valid content ({len(existing)} chars), skipping")
                success_count += 1
                continue
            else:
                print(f"  ⚠ exists but incomplete ({len(existing)} chars), regenerating")
        
        try:
            content = generate_article(client, article_def)
            if write_article(article_def, content):
                success_count += 1
            # Rate limit: 1 second between API calls
            time.sleep(1.5)
        except Exception as e:
            print(f"  ✗ FAILED: {e}")
        
        print()
    
    print(f"=== DONE: {success_count}/{len(ARTICLES)} articles generated ===")
    
    # Verify integrity of all generated files
    print("\n=== Verification ===")
    for article_def in ARTICLES:
        out_path = REVIEWS_DIR / f"{article_def['slug']}.md"
        if out_path.exists():
            size = out_path.stat().st_size
            content = out_path.read_text(encoding='utf-8')
            fm_count = content.count('---')
            has_body = len(content.split('---', 2)[-1].strip()) if fm_count >= 2 else 0
            tag_count = content.count(f'tag={TAG}')
            print(f"  {article_def['slug']}: {size}B, {fm_count} fm blocks, ~{len(content)} chars, {tag_count} affiliate links")
        else:
            print(f"  {article_def['slug']}: MISSING!")
    
    sys.exit(0 if success_count == len(ARTICLES) else 1)


if __name__ == "__main__":
    main()
