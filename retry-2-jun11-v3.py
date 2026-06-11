#!/usr/bin/env python3
"""Retry 2 failed comparison articles with long delays."""
import json, urllib.request, urllib.error, os, sys, time

KEY_FILE = os.path.expanduser("~/.hermes/.env")
API_KEY = None
with open(KEY_FILE) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

if not API_KEY:
    print("FATAL: No API key")
    sys.exit(1)

def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.5, "maxOutputTokens": 4096, "topP": 0.95}
    }).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.read().decode()[:300]}"
    except Exception as e:
        return f"Error: {e}"

def build_prompt(cat1, cat2, category, c1d, c2d, anchors):
    a = "\n".join(f"  - {s}" for s in anchors)
    return f"""Je bent een Nederlandse redacteur voor KiesKeuken / Beste Apparaten (rigbay.github.io/dutch-appliances/), de beste Nederlandse site voor het vergelijken van huishoudelijke apparaten.

Schrijf een COMPLEET vergelijkingsartikel: "{c1d} vs. {c2d} 2026".

CATEGORIE: {category}

GERELATEERDE ARTIKELEN:
{a}

FORMAAT — exact deze structuur:
1. # Titel (H1) — "{c1d} vs. {c2d} 2026: [pakkende ondertitel]"
2. ## Inleiding (2-3 alinea's, herkenbare situatieschets)
3. ## Snel advies (3 aanbevelingen: beste algemeen, beste budget, beste premium)
4. ## De ultieme vergelijking op 6 aspecten: functionaliteit, gebruiksgemak, prijs, energieverbruik, onderhoud, duurzaamheid
5. ## Prijsvergelijking (reele prijsranges in EUR, aanschaf + jaarlijkse gebruikskosten)
6. ## Verborgen nadelen (minimaal 3 per type, specifiek en eerlijk)
7. ## Voor wie is welke? (5-6 gebruikersscenario's: "Jij bent een... kies dan...")
8. ## Top 5 producten (echte producten — **naam**, verdict 1-2 zinnen, priceRange, bestFor, rating 3.5-5.0)
9. ## Conclusie: welke past bij jou? (kort en direct)
10. ## Veelgestelde vragen (4 FAQ's met antwoorden van 3-5 zinnen)

BELANGRIJKE REGELS:
- Vloeiend Nederlands (NL-NL, niet Vlaams)
- Echte producten van bekende merken (Philips, Dyson, Bosch, Miele, Tefal, Rowenta, Samsung, LG, etc.)
- Amazon URL's: https://www.amazon.nl/s?k=[productnaam+model]&tag=kieskeukennl-21
- Minimaal 1000 woorden, maximaal 1800 woorden
- Geen marketingtaal — eerlijk over nadelen
- Verwijs naar gerelateerde artikelen met [tekst](/slug/) als het natuurlijk past
- Stuur ALLEEN het complete artikel terug, beginnend met # titel
- GEEN markdown code fences (```) om het artikel heen"""

print("Generating stofzuiger vs kruimeldief...")
p1 = build_prompt(
    "stofzuiger", "kruimeldief", "schoonmaken",
    "Stofzuiger", "Kruimeldief",
    ["beste-stofzuiger-2026", "beste-steelstofzuiger-2026", "stofzuiger-vs-steelstofzuiger-2026"]
)
b1 = call_gemini(p1)
print(f"Result: {b1[:80]}...")

if not b1.startswith("HTTP") and not b1.startswith("Error"):
    b1 = b1.strip()
    if b1.startswith("```"):
        parts = b1.split("```")
        b1 = parts[1] if len(parts) >= 3 else b1
        if b1.startswith("markdown"):
            b1 = b1[8:]
    b1 = b1.strip()
    with open("src/content/reviews/stofzuiger-vs-kruimeldief-2026.md", "w") as f:
        f.write(b1)
    print(f"Saved stofzuiger-vs-kruimeldief-2026.md ({len(b1.split())} words)")
else:
    print(f"FAILED: {b1[:200]}")

print("Waiting 45s...")
time.sleep(45)

print("Generating strijkijzer vs handstomer...")
p2 = build_prompt(
    "strijkijzer", "handstomer", "huishoudelijk",
    "Strijkijzer", "Handstomer",
    ["beste-strijkijzer-2026", "strijkijzer-vs-stoomgenerator-2026"]
)
b2 = call_gemini(p2)
print(f"Result: {b2[:80]}...")

if not b2.startswith("HTTP") and not b2.startswith("Error"):
    b2 = b2.strip()
    if b2.startswith("```"):
        parts = b2.split("```")
        b2 = parts[1] if len(parts) >= 3 else b2
        if b2.startswith("markdown"):
            b2 = b2[8:]
    b2 = b2.strip()
    with open("src/content/reviews/strijkijzer-vs-handstomer-2026.md", "w") as f:
        f.write(b2)
    print(f"Saved strijkijzer-vs-handstomer-2026.md ({len(b2.split())} words)")
else:
    print(f"FAILED: {b2[:200]}")

print("\nRETRY COMPLETE")
