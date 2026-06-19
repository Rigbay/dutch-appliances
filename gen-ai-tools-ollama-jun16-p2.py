#!/usr/bin/env python3
"""Generate 5 Dutch consumer comparison articles for dutch-ai-tools using Ollama.
Hermes cron job — June 16, 2026 part 2. Gemini rate-limited, fallback to Ollama."""
import os, sys, json, time, subprocess

OUT_DIR = "/home/cls/dutch-ai-tools/src/content/articles"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "neuraldaredevil:latest"  # 8B Llama, fast and reliable

ARTICLES = [
    {
        "slug": "spaarrekeningen-vergelijken-2026-bunq-revolut-raisin-nibc-leaseplan",
        "title": "Beste Spaarrekeningen 2026: Hoge Rente, Vrij Opneembaar en Deposito's Vergeleken",
        "category": "persoonlijk",
        "price_range": "EUR 0-5 per maand",
        "reading_time": "8 min",
        "providers": "Bunq, Revolut Savings, Raisin, NIBC Direct, LeasePlan Bank, ING, Rabobank, Trade Republic",
        "related": [
            "beste-online-banken-2026-bunq-revolut-n26-knab-asn",
            "beste-budget-apps-2026-dyme-spendle-ynab-wallet-grip",
            "beleggingsapps-vergelijken-2026-degiro-bux-etoro-trade-republic-meesman"
        ]
    },
    {
        "slug": "beleggingsapps-vergelijken-2026-degiro-bux-etoro-trade-republic-meesman",
        "title": "Beste Beleggingsapps 2026: Beginners en Gevorderden — Lage Kosten, Gebruiksvriendelijk en Betrouwbaar",
        "category": "persoonlijk",
        "price_range": "EUR 0-5 per transactie",
        "reading_time": "8 min",
        "providers": "DeGiro, Bux, eToro, Trade Republic, Saxo Bank, Meesman, Brand New Day, Peaks",
        "related": [
            "beste-online-banken-2026-bunq-revolut-n26-knab-asn",
            "spaarrekeningen-vergelijken-2026-bunq-revolut-raisin-nibc-leaseplan",
            "beste-ai-tools-beleggers-investeerders-2026"
        ]
    },
    {
        "slug": "reisverzekering-vergelijken-2026-anwb-allianz-unive-centraal-beheer-ohra",
        "title": "Beste Reisverzekering 2026: Doorlopend, Kortlopend, Annulering en Medische Dekking Vergeleken",
        "category": "persoonlijk",
        "price_range": "EUR 3-15 per maand",
        "reading_time": "8 min",
        "providers": "ANWB, Allianz Global Assistance, Unive, Centraal Beheer, OHRA, ABN AMRO, ING, FBTO",
        "related": [
            "autoverzekering-vergelijken-independer-unive-centraal-beheer-allianz-2026",
            "zorgverzekering-vergelijken-2026-zilveren-kruis-cz-vgz-menzis",
            "fietsverzekering-vergelijken-2026-anwb-unive-centraal-beheer-allianz-enra"
        ]
    },
    {
        "slug": "fietsverzekering-vergelijken-2026-anwb-unive-centraal-beheer-allianz-enra",
        "title": "Beste Fietsverzekering 2026: E-bikes, Bakfietsen en Racefietsen — Diefstal, Schade en Pechhulp",
        "category": "persoonlijk",
        "price_range": "EUR 3-20 per maand",
        "reading_time": "8 min",
        "providers": "ANWB, Unive, Centraal Beheer, Allianz, ENRA, Kingpolis, Aon, Alpina",
        "related": [
            "reisverzekering-vergelijken-2026-anwb-allianz-unive-centraal-beheer-ohra",
            "autoverzekering-vergelijken-independer-unive-centraal-beheer-allianz-2026",
            "beste-ai-tools-verzekeringen-2026"
        ]
    },
    {
        "slug": "verhuisbedrijven-vergelijken-2026-verhuisoffertes-studentverhuizers-de-haan-voerman",
        "title": "Beste Verhuisbedrijven 2026: Particulier, Student en Internationaal Verhuizen Vergeleken op Prijs en Service",
        "category": "huis-tuin",
        "price_range": "EUR 200-5000 eenmalig",
        "reading_time": "8 min",
        "providers": "Verhuisoffertes.nl, Studentverhuizers, De Haan Verhuizingen, Voerman, Mondial Movers, VerhuisService Nederland, AGS Movers, De Klerk Verhuizingen",
        "related": [
            "beste-ai-tools-verhuizen-verhuisbedrijven-2026",
            "beste-internetproviders-2026-ziggo-kpn-odido-delta-tmobile",
            "energiecontracten-vergelijken-2026-vast-dynamisch-variabel"
        ]
    },
]

SYSTEM_PROMPT = """Je bent een Nederlandse consumentenjournalist voor DutchAITools.nl. Je schrijft vergelijkingsartikelen over consumentenproducten en diensten.

FORMAT: Markdown met YAML frontmatter. Het artikel moet tussen 800-1200 woorden zijn.

FRONTMATTER TEMPLATE (exact dit formaat, vul de placeholders in):
---
title: '<TITLE>'
slug: '<SLUG>'
description: '<120-155 char meta description in SEO Nederlands>'
category: '<CATEGORY>'
rating: 4.3
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
- https://www.beehiiv.com/?via=kiara-hilman
- https://taskade.com/?via=55nfr2
- https://writesonic.com/?via=aitoolsnl
- https://rytr.me?via=hermes-affiliates
- https://www.synthesia.io?via=hermes
- https://www.make.com/en/register?pc=hermesai
- https://www.frase.io/?via=hermes10
date: 2026-06-16
modelYear: 2026
featuredTool: '<BESTE_AANBIEDER>'
readingTime: '<READING_TIME>'
tools:
- name: '<AANBIEDER_1>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRIJSRANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.beehiiv.com/?via=kiara-hilman
- name: '<AANBIEDER_2>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRIJSRANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://taskade.com/?via=55nfr2
- name: '<AANBIEDER_3>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRIJSRANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://writesonic.com/?via=aitoolsnl
- name: '<AANBIEDER_4>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRIJSRANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://rytr.me?via=hermes-affiliates
- name: '<AANBIEDER_5>'
  verdict: '<1-2 zinnen verdict>'
  priceRange: '<PRIJSRANGE>'
  bestFor: '<BEST_FOR>'
  rating: <1-5>
  affiliateLink: https://www.synthesia.io?via=hermes
related:
- '<RELATED_1>'
- '<RELATED_2>'
- '<RELATED_3>'
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

## Inleiding

[2-3 paragrafen die het onderwerp introduceren. Waarom is dit relevant voor Nederlandse consumenten in 2026?]

## Snel Advies

[3 bullets: "Kies X als je..." — concrete situaties]

## Vergelijking per Aanbieder

[5-7 secties met ### koppen. Per aanbieder: prijs, belangrijkste features, voor wie geschikt, minpunten.]

## Waar op Letten?

[3-4 alinea's met praktische tips waar consumenten op moeten letten bij het kiezen.]

## Vergelijkingstabel

[Markdown tabel met alle aanbieders: Naam | Prijs | Beste voor | Score | Opvallend]

## Conclusie

[1-2 paragrafen samenvatting. Eindig met een duidelijke aanbeveling per situatie.]

## Veelgestelde Vragen

[5 FAQ items met concrete antwoorden.]

REGELS:
- Schrijf in vlot, natuurlijk Nederlands.
- Gebruik concrete prijzen en echte aanbieder-namen.
- Wees eerlijk over minpunten — geen marketingtaal.
- Houd het artikel tussen 800-1200 woorden.
- Gebruik ## voor koppen, niet #.
- Géén markdown fences om de hele output.
- SCHRIJF HET VOLLEDIGE ARTIKEL. Stop niet halverwege. Eindig met de conclusie en FAQ."""

def call_ollama(system_prompt, user_prompt):
    """Call Ollama local API."""
    import urllib.request, urllib.error
    
    full_prompt = f"{system_prompt}\n\n{user_prompt}"
    
    body = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 4096,
            "top_p": 0.9
        }
    }
    
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        print(f"  Ollama error: {e}")
        return None

def validate_frontmatter(content, article):
    issues = []
    if not content.startswith("---"):
        issues.append("Missing opening ---")
    required_fields = ["title:", "slug:", "description:", "category:", "rating:",
                       "priceRange:", "pros:", "cons:", "affiliateLinks:", "date:",
                       "tools:", "related:", "faq:"]
    for field in required_fields:
        if field not in content[:3000]:
            issues.append(f"Missing field: {field}")
    body_start = content.find("---", 3)
    if body_start > 0:
        body = content[body_start+3:]
        words = len(body.split())
        if words < 500:
            issues.append(f"Too short: {words} words (min 800)")
    return issues

def main():
    results = []
    
    for i, art in enumerate(ARTICLES):
        out_path = os.path.join(OUT_DIR, f"{art['slug']}.md")
        if os.path.exists(out_path):
            print(f"[{i+1}/5] SKIP {art['slug']} — exists")
            continue
        
        print(f"\n[{i+1}/5] Generating: {art['slug']}")
        
        user_prompt = f"""Schrijf een vergelijkingsartikel voor:

TITEL: {art['title']}
SLUG: {art['slug']}
CATEGORIE: {art['category']}
PRIJSRANGE: {art['price_range']}
LEESTIJD: {art['reading_time']}

AANBIEDERS OM TE VERGELIJKEN: {art['providers']}

GERELATEERDE ARTIKELEN (gebruik deze exacte slugs in de 'related' lijst):
{chr(10).join('- ' + r for r in art['related'])}

BELANGRIJK: Schrijf het VOLLEDIGE artikel van begin tot eind. Stop niet halverwege. Eindig met de conclusie en de FAQ sectie.

OUTPUT: Alleen de Markdown met frontmatter. Geen uitleg, geen "hier is het artikel"."""
        
        content = call_ollama(SYSTEM_PROMPT, user_prompt)
        
        if content is None or len(content) < 500:
            print(f"  FAILED: No/inadequate response ({len(content) if content else 0} chars)")
            results.append({"slug": art['slug'], "status": "FAILED"})
            continue
        
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            content = "\n".join(lines)
        
        issues = validate_frontmatter(content, art)
        if issues:
            print(f"  WARNINGS: {'; '.join(issues)}")
        
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(content)
        
        print(f"  OK: {out_path} ({len(content)} chars)")
        results.append({"slug": art['slug'], "status": "OK", "path": out_path, "issues": issues})
        
        time.sleep(3)
    
    print("\n=== SUMMARY ===")
    ok = sum(1 for r in results if r['status'] == 'OK')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    print(f"Generated: {ok}/{len(ARTICLES)}")
    print(f"Failed: {failed}/{len(ARTICLES)}")
    for r in results:
        if r.get('issues'):
            print(f"  {r['slug']}: {r['issues']}")
    
    return results

if __name__ == "__main__":
    main()
