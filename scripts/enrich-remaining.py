#!/usr/bin/env python3
"""Enrich remaining thin articles - robust version with proper rate limiting."""
import os, re, sys, json, time, subprocess

REVIEWS_DIR = "src/content/reviews"
TARGETS = sys.argv[1:] if len(sys.argv) > 1 else [
    "beste-paneerapparaat-2026.md",
    "beste-persoonsweegschaal-2026.md", 
    "beste-ventilator-2026.md",
    "beste-vleesmolen-2026.md",
    "koffiemolen-vs-voorgemalen-koffie-2026.md",
]

# Get API key via grep (bypass env var issues)
result = subprocess.run(
    ["grep", "^GEMINI_API_KEY=", os.path.expanduser("~/.hermes/.env")],
    capture_output=True, text=True
)
API_KEY = ""
for line in result.stdout.strip().split("\n"):
    if line.startswith("#") or "your_gemini" in line.lower():
        continue
    API_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
    break

if not API_KEY:
    print("ERROR: No valid API key found")
    sys.exit(1)

print(f"API key: {API_KEY[:10]}... (len={len(API_KEY)})")

def call_gemini(prompt):
    """Call Gemini via subprocess curl for reliability."""
    prompt_json = json.dumps(prompt)
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    })
    
    for attempt in range(5):
        result = subprocess.run([
            "curl", "-s", "--max-time", "120",
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}",
            "-H", "Content-Type: application/json",
            "-d", payload
        ], capture_output=True, text=True, timeout=130)
        
        try:
            data = json.loads(result.stdout)
            if "candidates" in data:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
            elif "error" in data:
                err = data["error"]
                code = err.get("code", 0)
                msg = err.get("message", "")
                print(f"  API error (code={code}): {msg[:100]}")
                if code == 429:
                    wait = 20 * (attempt + 1)
                    print(f"  Rate limited, waiting {wait}s...")
                    time.sleep(wait)
                    continue
                else:
                    return ""
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"  Parse error: {e}")
            print(f"  Raw: {result.stdout[:200]}")
        
        time.sleep(5 * (attempt + 1))
    
    return ""

for target in TARGETS:
    filepath = os.path.join(REVIEWS_DIR, target)
    if not os.path.exists(filepath):
        print(f"SKIP: {target} not found")
        continue
    
    with open(filepath) as f:
        original = f.read()
    
    parts = original.split("---", 2)
    if len(parts) < 3:
        print(f"SKIP: {target} can't parse frontmatter")
        continue
    
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

BESTAANDE CONTENT (dun, moet vervangen):
{body[:500]}

STRUCTUUR:
## Inleiding (2-3 alinea's)
## Snel advies
## Waar let je op bij het kopen? (4-6 punten, **vette** kernbegrippen)
## Onze topkeuzes (per product: naam, prijs, voor wie, sterk/minpunt)
## Veelgestelde vragen (3-5)
## Conclusie

REGELS: vlot NL-NL, korte alinea's, prijzen in euro, Amazon.nl (tag: kieskeukennl-21), geen placeholders, ALLEEN body — begin met ## Inleiding"""
    
    print(f"\n--- {target} ({word_count} words) ---")
    new_body = call_gemini(prompt)
    
    if not new_body or len(new_body.split()) < 200:
        print(f"  FAILED: {len(new_body.split()) if new_body else 0} words")
        continue
    
    # Clean up code fences
    new_body = re.sub(r'^```[a-z]*\s*\n?', '', new_body)
    new_body = re.sub(r'\n?```\s*$', '', new_body)
    
    new_content = f"---{fm_text}---\n\n{new_body.strip()}\n"
    if "affiliate" not in new_body.lower():
        new_content += "\n---\n\n*Dit artikel is bijgewerkt voor 2026. Productvermeldingen en prijzen kunnen afwijken. Sommige links in dit artikel zijn affiliate-links. Als je via deze links een product koopt, ontvangen wij een kleine commissie zonder dat jij extra betaalt.*\n"
    
    with open(filepath, "w") as f:
        f.write(new_content)
    
    new_words = len(new_body.split())
    print(f"  ENRICHED: {word_count} → {new_words} words")
    
    # Long delay between calls
    time.sleep(15)

print("\nDone.")
