#!/usr/bin/env python3
"""Enrich ONE thin article at a time with generous delays."""
import os, re, sys, json, time
import urllib.request, urllib.error

REVIEWS_DIR = "src/content/reviews"
TARGET = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET:
    print("Usage: python3 enrich-one.py <filename>")
    sys.exit(1)

# Read API key
API_KEY = ""
env_path = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"): continue
            if stripped.startswith("GEMINI_API_KEY=") and "your_gemini" not in stripped.lower():
                API_KEY = stripped.split("=", 1)[1].strip().strip('"').strip("'")
                break

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

def call_gemini(prompt):
    body = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096, "topP": 0.95}}
    data = json.dumps(body).encode("utf-8")
    for attempt in range(5):
        try:
            req = urllib.request.Request(f"{API_URL}?key={API_KEY}", data=data, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 15 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"  HTTP {e.code}")
                time.sleep(5)
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(5)
    return ""

filepath = os.path.join(REVIEWS_DIR, TARGET)
with open(filepath) as f:
    original = f.read()

parts = original.split("---", 2)
fm_text = parts[1]
body = parts[2]
word_count = len(body.split())

# Parse frontmatter
fm = {}
for line in fm_text.strip().split("\n"):
    line = line.strip()
    if not line or line.startswith("#"): continue
    if ":" in line:
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip().strip("'\"")

title = fm.get("title", "")
desc = fm.get("description", "")
featured = fm.get("featuredProduct", "")
price = fm.get("priceRange", "")

prompt = f"""Je bent een Nederlandse copywriter voor koopgidsen. Schrijf een complete artikel-body (800-1200 woorden) voor:

TITEL: {title}
BESCHRIJVING: {desc}
HOOFDPRODUCT: {featured}
PRIJSKLASSE: {price}

BESTAANDE CONTENT (dun):
{body[:500]}

STRUCTUUR:
## Inleiding (2-3 alinea's)
## Snel advies
## Waar let je op bij het kopen? (4-6 punten, **vette** kernbegrippen)
## Onze topkeuzes (per product: naam, prijs, voor wie, sterk/minpunt)
## Veelgestelde vragen (3-5)
## Conclusie

REGELS: vlot NL-NL, korte alinea's, prijzen in €, Amazon.nl (tag: kieskeukennl-21), geen placeholders, ALLEEN body — begin met ## Inleiding"""

print(f"Enriching {TARGET} ({word_count} words)...")
new_body = call_gemini(prompt)

if not new_body or len(new_body.split()) < 200:
    print(f"FAILED: {len(new_body.split()) if new_body else 0} words")
    sys.exit(1)

new_body = re.sub(r'^```[a-z]*\s*', '', new_body.strip())
new_body = re.sub(r'\s*```$', '', new_body)

new_content = f"---{fm_text}---\n\n{new_body.strip()}\n"
if "affiliate" not in new_body.lower():
    new_content += "\n---\n\n*Dit artikel is bijgewerkt voor 2026. Productvermeldingen en prijzen kunnen afwijken. Sommige links in dit artikel zijn affiliate-links. Als je via deze links een product koopt, ontvangen wij een kleine commissie zonder dat jij extra betaalt.*\n"

with open(filepath, "w") as f:
    f.write(new_content)

print(f"DONE: {word_count} → {len(new_body.split())} words")
