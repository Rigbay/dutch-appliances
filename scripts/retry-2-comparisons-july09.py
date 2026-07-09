#!/usr/bin/env python3
"""Retry the 2 failed comparison articles with longer delays."""
import os, json, time, re
from pathlib import Path
from datetime import date
import urllib.request, urllib.error

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"
AMAZON_TAG = "kieskeukennl-21"
TODAY = date.today().isoformat()

# Load API key
env_path = Path.home() / ".hermes" / ".env"
api_key = None
with open(env_path) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.strip().split("=", 1)[1].strip()
            break

if not api_key or "your_gemini_key" in api_key:
    print("ERROR: No valid GEMINI_API_KEY found")
    exit(1)

TOPICS = [
    {
        "slug": "broodmachine-vs-broodrooster-2026",
        "title": "Broodmachine vs. Broodrooster 2026: Zelf Bakken of Kant-en-Klaar Roosteren?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Broodmachine vs Broodrooster 2026.

Context: Juli 2026. Een broodmachine bakt zelf vers brood (3-4 uur, ingrediënten erin, brood eruit). Een broodrooster roostert bestaand brood in 2-3 minuten. Totaal verschillende apparaten maar vaak verward door beginnende kopers. Broodmachine: €50-200, broodrooster: €15-80.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — het fundamentele verschil: zelf bakken vs roosteren
2. Snel advies — 3 bullets wie wat moet kiezen
3. Hoe werkt een broodmachine? — kneedt, rijst, bakt automatisch
4. Hoe werkt een broodrooster? — infrarood/weerstandsdraden, roostert bestaand brood
5. Vergelijkingstabel — 6-8 rijen: functie, tijd, kosten per gebruik, gebruiksgemak, schoonmaak, veelzijdigheid, ruimte op aanrecht
6. Top 3 broodmachines 2026 — met Amazon NL links (tag: kieskeukennl-21)
7. Top 3 broodroosters 2026 — met Amazon NL links
8. Prijsvergelijking
9. Voor wie is een broodmachine beter?
10. Voor wie is een broodrooster beter?
11. Conclusie

AMAZON LINKS (gebruik deze exact):
- Panasonic SD-YR2550 broodmachine: https://www.amazon.nl/s?k=Panasonic+SD-YR2550+broodmachine&tag=kieskeukennl-21
- Inventum BM90 broodmachine: https://www.amazon.nl/s?k=Inventum+BM90+broodmachine&tag=kieskeukennl-21
- Princess broodmachine: https://www.amazon.nl/s?k=Princess+broodmachine+2026&tag=kieskeukennl-21
- KitchenAid broodrooster: https://www.amazon.nl/s?k=KitchenAid+broodrooster+2026&tag=kieskeukennl-21
- Philips broodrooster: https://www.amazon.nl/s?k=Philips+broodrooster+2026&tag=kieskeukennl-21
- Inventum broodrooster: https://www.amazon.nl/s?k=Inventum+broodrooster+2026&tag=kieskeukennl-21

FORMAT: Markdown zonder frontmatter. Gebruik ## voor koppen. Minimaal 1500 woorden. Eerlijk, kritisch, Nederlands."""
    },
    {
        "slug": "kettingzaag-vs-cirkelzaag-2026",
        "title": "Kettingzaag vs. Cirkelzaag 2026: Welke Zaag voor Jouw Klus?",
        "category": "tuin",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Kettingzaag vs Cirkelzaag 2026.

Context: Juli 2026. Een kettingzaag zaagt met een ronddraaiende ketting (bomen, dik hout, tuin). Een cirkelzaag zaagt met een ronddraaiend zaagblad (planken, plaatmateriaal, precisie). Totaal verschillende toepassingen. Kettingzaag: €60-400, cirkelzaag: €40-250.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — fundamenteel verschil in toepassing
2. Snel advies — 3 bullets wie wat moet kiezen
3. Hoe werkt een kettingzaag? — ketting rond zwaard, voor grof werk
4. Hoe werkt een cirkelzaag? — ronddraaiend blad, voor precisie
5. Vergelijkingstabel — 6-8 rijen: toepassing, precisie, veiligheid, onderhoud, geluid, gewicht, prijs
6. Top 3 kettingzagen 2026 — met Amazon NL links (tag: kieskeukennl-21)
7. Top 3 cirkelzagen 2026 — met Amazon NL links
8. Prijsvergelijking
9. Voor wie is een kettingzaag beter?
10. Voor wie is een cirkelzaag beter?
11. Veiligheidstips voor beide
12. Conclusie

AMAZON LINKS (gebruik deze exact):
- Husqvarna kettingzaag: https://www.amazon.nl/s?k=Husqvarna+kettingzaag+2026&tag=kieskeukennl-21
- Stihl kettingzaag: https://www.amazon.nl/s?k=Stihl+kettingzaag+2026&tag=kieskeukennl-21
- Makita accu kettingzaag: https://www.amazon.nl/s?k=Makita+accu+kettingzaag+2026&tag=kieskeukennl-21
- Makita cirkelzaag: https://www.amazon.nl/s?k=Makita+cirkelzaag+2026&tag=kieskeukennl-21
- Bosch Professional cirkelzaag: https://www.amazon.nl/s?k=Bosch+Professional+cirkelzaag+2026&tag=kieskeukennl-21
- DeWalt cirkelzaag: https://www.amazon.nl/s?k=DeWalt+cirkelzaag+2026&tag=kieskeukennl-21

FORMAT: Markdown zonder frontmatter. Gebruik ## voor koppen. Minimaal 1500 woorden. Eerlijk, kritisch, Nederlands."""
    }
]

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "topP": 0.95
        }
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                wait = 15 * (attempt + 1)
                print(f"  Waiting {wait}s...")
                time.sleep(wait)
    return None

def build_frontmatter(topic, body):
    slug = topic["slug"]
    title = topic["title"]
    category = topic["category"]
    
    clean_body = re.sub(r'#+\s*', '', body)
    clean_body = re.sub(r'\*\*', '', clean_body)
    clean_body = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean_body)
    clean_body = re.sub(r'\n+', ' ', clean_body).strip()
    desc = clean_body[:160].rsplit('.', 1)[0] + '.'
    
    word_count = len(body.split())
    reading_time = f"{max(1, word_count // 200)} min"
    
    links = re.findall(r'https://www\.amazon\.nl[^\s)\]]+', body)
    links = list(set(links))[:8]
    
    products = []
    for link in links[:6]:
        link_pos = body.find(link)
        if link_pos > 0:
            context = body[max(0, link_pos-200):link_pos]
            name_match = re.search(r'(?:de |De )?([A-Z][a-z]+(?:\s[A-Z][a-z]+(?:\s[A-Z][a-z0-9]+)?)?(?:\s[A-Z][a-z0-9]+)*)', context)
            if name_match:
                name = name_match.group(1).strip()
            else:
                name = f"Model {len(products)+1}"
        else:
            name = f"Model {len(products)+1}"
        
        products.append({
            "name": name,
            "verdict": f"Aanrader in {category} categorie",
            "priceRange": "€50-300",
            "bestFor": f"Beste keuze {category}",
            "rating": 4.0 + (len(products) * 0.1),
            "affiliateLink": link
        })
    
    price_range = "€15-200" if "brood" in slug else "€40-400"
    
    products_yaml = "\n".join(
        f'- name: {p["name"]}\n  verdict: {p["verdict"]}\n  priceRange: {p["priceRange"]}\n  bestFor: {p["bestFor"]}\n  rating: {p["rating"]}\n  affiliateLink: {p["affiliateLink"]}'
        for p in products
    )
    
    links_yaml = "\n".join(f'- {link}' for link in links[:6])
    
    fm = f"""---
title: '{title}'
slug: {slug}
description: '{desc}'
category: {category}
rating: 4.3
priceRange: {price_range}
pros:
- Directe vergelijking op prijs, prestaties en gebruiksgemak
- Eerlijke voor- en nadelen van beide opties
- Actuele Amazon NL prijzen en aanbiedingen
cons:
- Persoonlijke voorkeur speelt een grote rol
- Prijzen kunnen fluctueren per seizoen
affiliateLinks:
{links_yaml}
date: {TODAY}
modelYear: 2026
featuredProduct: ''
readingTime: {reading_time}
products:
{products_yaml}
related:
- beste-espresso-apparaat-2026
- beste-filterkoffiemachine-2026
draft: false
---
"""
    return fm + "\n" + body

def main():
    results = []
    for i, topic in enumerate(TOPICS):
        print(f"\n[{i+1}/2] Generating: {topic['slug']}")
        body = call_gemini(topic["prompt"])
        if not body:
            print(f"  FAILED to generate {topic['slug']}")
            continue
        
        article = build_frontmatter(topic, body)
        out_path = REVIEWS_DIR / f"{topic['slug']}.md"
        out_path.write_text(article)
        print(f"  Written: {out_path} ({len(body.split())} words)")
        results.append(topic['slug'])
        time.sleep(20)  # Long delay between calls
    
    print(f"\nDone. Generated {len(results)}/{len(TOPICS)} articles.")
    for r in results:
        print(f"  {r}")

if __name__ == "__main__":
    main()
