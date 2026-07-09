#!/usr/bin/env python3
"""Retry enriching the 5 remaining thin articles with longer delays."""

import os, re, sys, json, time
import urllib.request, urllib.error

REVIEWS_DIR = "src/content/reviews"

# Read API key from .env file
API_KEY = ""
env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if stripped.startswith("GEMINI_API_KEY=") and "your_gemini" not in stripped.lower():
                API_KEY = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                break

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def call_gemini(prompt: str, max_retries: int = 3) -> str:
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "topP": 0.95,
        }
    }
    data = json.dumps(body).encode("utf-8")
    
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                f"{API_URL}?key={API_KEY}",
                data=data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 10 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {e.code}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(3)
        except Exception as e:
            print(f"  Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
    return ""

def extract_frontmatter_and_body(filepath: str) -> tuple:
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1]
    body = parts[2]
    fm = {}
    for line in fm_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip("'\"")
            fm[key] = val
    return fm, body

def build_enrichment_prompt(fm: dict, existing_body: str, filename: str) -> str:
    title = fm.get("title", "").strip("'\"")
    description = fm.get("description", "").strip("'\"")
    category = fm.get("category", "keuken")
    price_range = fm.get("priceRange", "")
    featured = fm.get("featuredProduct", "")
    
    prompt = f"""Je bent een Nederlandse copywriter gespecialiseerd in koopgidsen voor huishoudelijke apparaten. Schrijf een complete, informatieve artikel-body (800-1200 woorden) voor onderstaand artikel.

TITEL: {title}
BESCHRIJVING: {description}
CATEGORIE: {category}
PRIJSKLASSE: {price_range}
HOOFDPRODUCT: {featured}

BESTAANDE CONTENT (dun, moet vervangen worden):
{existing_body[:500]}

SCHRIJF NU DE VOLLEDIGE BODY. Gebruik deze structuur:

## Inleiding (2-3 alinea's)
- Waarom dit onderwerp belangrijk is voor Nederlandse kopers in 2026
- Wat de lezer gaat leren

## Snel advies (korte alinea)
- De beste keuze in één zin per gebruiksscenario

## Waar let je op bij het kopen? (4-6 punten)
- Concrete kooptips met uitleg
- Gebruik **vette** tekst voor kernbegrippen

## Onze topkeuzes (per product een korte alinea)
- Productnaam, prijsindicatie, voor wie het beste is
- Eén sterk punt en één minpunt per product

## Veelgestelde vragen (3-5 FAQ's)
- Vraag en antwoord in natuurlijk Nederlands

## Conclusie
- Samenvatting en eindadvies

REGELS:
- Schrijf in vlot, natuurlijk Nederlands (NL-NL, niet Vlaams)
- Gebruik korte alinea's (2-4 zinnen)
- Geen Engelse termen tenzij onvermijdelijk
- Gebruik tussenkopjes (##) voor structuur
- Noem prijzen in euro's (€)
- Verwijs naar Amazon.nl voor aankoop (tag: kieskeukennl-21)
- Geen placeholder-tekst, geen [TODO]
- Schrijf ALLEEN de body — geen frontmatter, geen --- scheidingstekens
- Begin direct met ## Inleiding
"""
    return prompt

def main():
    remaining = [
        "beste-paneerapparaat-2026.md",
        "beste-persoonsweegschaal-2026.md",
        "beste-ventilator-2026.md",
        "beste-vleesmolen-2026.md",
        "koffiemolen-vs-voorgemalen-koffie-2026.md",
    ]
    
    enriched = []
    failed = []
    
    for filename in remaining:
        filepath = os.path.join(REVIEWS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP: {filename} not found")
            continue
        
        fm, body = extract_frontmatter_and_body(filepath)
        word_count = len(body.split())
        print(f"\n--- {filename} ({word_count} words) ---")
        
        prompt = build_enrichment_prompt(fm, body, filename)
        new_body = call_gemini(prompt)
        
        if not new_body or len(new_body.split()) < 200:
            print(f"  FAILED: generated body too short or empty")
            failed.append(filename)
            continue
        
        new_body = re.sub(r'^```[a-z]*\s*', '', new_body.strip())
        new_body = re.sub(r'\s*```$', '', new_body)
        
        with open(filepath) as f:
            original = f.read()
        
        parts = original.split("---", 2)
        if len(parts) < 3:
            print(f"  FAILED: can't parse frontmatter")
            failed.append(filename)
            continue
        
        new_content = f"---{parts[1]}---\n\n{new_body.strip()}\n"
        
        if "*Dit artikel is bijgewerkt" not in new_body and "affiliate" not in new_body.lower():
            new_content += "\n---\n\n*Dit artikel is bijgewerkt voor 2026. Productvermeldingen en prijzen kunnen afwijken. Sommige links in dit artikel zijn affiliate-links. Als je via deze links een product koopt, ontvangen wij een kleine commissie zonder dat jij extra betaalt.*\n"
        
        with open(filepath, "w") as f:
            f.write(new_content)
        
        new_words = len(new_body.split())
        print(f"  ENRICHED: {word_count} → {new_words} words")
        enriched.append((filename, word_count, new_words))
        
        # Longer delay to avoid rate limits
        time.sleep(8)
    
    print(f"\n=== RETRY SUMMARY ===")
    print(f"Enriched: {len(enriched)}")
    for f, old, new in enriched:
        print(f"  {f}: {old} → {new} words")
    print(f"Failed: {len(failed)}")
    for f in failed:
        print(f"  {f}")

if __name__ == "__main__":
    main()
