#!/usr/bin/env python3
"""Generate FAQ frontmatter for KiesKeuken articles using Gemini API.

For each article, Gemini reads the markdown body and extracts 3-5 FAQ Q&A pairs
relevant to the topic. These are injected as `faq:` frontmatter fields.
Only processes articles that DON'T already have FAQ frontmatter.
"""

import os, sys, json, requests, re, time

REVIEWS_DIR = os.path.expanduser("/workspace/kieskeuken/src/content/reviews")
ENV_PATH = os.path.expanduser("~/.hermes/.env")

# Load API key
api_key = None
with open(ENV_PATH) as f:
    for line in f:
        line = line.strip()
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()
            break

if not api_key:
    print("ERROR: No Gemini API key found", file=sys.stderr)
    sys.exit(1)

MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"

def get_frontmatter_and_body(filepath):
    """Split .md file into frontmatter dict and body string."""
    with open(filepath) as f:
        content = f.read()
    
    if not content.startswith("---"):
        return None, None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    
    fm_text = parts[1].strip()
    body = parts[2].strip()
    
    return fm_text, body

def parse_yaml_simple(fm_text):
    """Simple YAML parser for the frontmatter."""
    lines = fm_text.split("\n")
    result = {}
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        
        # Handle simple key: value
        if ":" in line and not line.startswith(" ") and not line.startswith("-"):
            key = stripped.split(":", 1)[0].strip()
            val = stripped.split(":", 1)[1].strip()
            
            if val.startswith("'") and val.endswith("'"):
                result[key] = val[1:-1]
            elif val.startswith('"') and val.endswith('"'):
                result[key] = val[1:-1]
            elif val in ("true", "false"):
                result[key] = val == "true"
            elif re.match(r'^\d+$', val):
                result[key] = int(val)
            elif re.match(r'^\d+\.\d+$', val):
                result[key] = float(val)
            else:
                result[key] = val
        else:
            # Skip everything else (we only need to check for existing faq: key)
            pass
        
        i += 1
    
    return result

def generate_faq(article_content, topic, max_chars=8000):
    """Use Gemini to extract FAQ pairs from article body content."""
    
    # Trim content to avoid token limits
    if len(article_content) > max_chars:
        excerpt = article_content[:max_chars] + "\n\n[...artikel vervolgt...]"
    else:
        excerpt = article_content
    
    prompt = f"""Je bent een FAQ-schrijver voor Beste Apparaten, een Nederlandstalige koopgidssite voor huishoudelijke apparaten.

Hieronder volgt de tekst van een koopgids artikel over: {topic}

---ARTIKEL---
{excerpt}
---EINDE---

Taak: Haal 3 tot 5 zinvolle FAQ-vragen met antwoorden uit de inhoud. De vragen moeten aansluiten bij echte kopersvragen die iemand zou googelen. De antwoorden moeten kort, nuttig en informatief zijn (max 3-4 zinnen).

Output ALLEEN valide JSON, geen markdown, geen uitleg. Format:
[
  {{"q": "Eerste vraag?", "a": "Kort en helder antwoord."}},
  {{"q": "Tweede vraag?", "a": "Kort en helder antwoord."}}
]

Geen ```json tags. Geen extra tekst. ALLEEN de JSON array."""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.95,
            "maxOutputTokens": 4000
        }
    }
    
    resp = requests.post(API_URL, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    
    # Strip markdown code blocks if present
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    
    try:
        faqs = json.loads(text)
        if isinstance(faqs, list) and len(faqs) >= 2:
            return faqs
        # Try to salvage: close unterminated strings and arrays
        if text.rstrip().endswith(','):
            text = text.rstrip().rstrip(',') + '\n]'
        elif not text.rstrip().endswith(']'):
            # Try to close the last string and array
            last_comma = text.rfind(',')
            if last_comma > 0:
                text = text[:last_comma] + '\n]'
            else:
                text = text.rstrip() + '"\n]'
        try:
            faqs = json.loads(text)
            if isinstance(faqs, list) and len(faqs) >= 2:
                print(f"  ⚠ Salvaged partial JSON, got {len(faqs)} items", file=sys.stderr)
                return faqs
        except:
            pass
        print(f"  Unexpected structure: {text[:100]}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}", file=sys.stderr)
        print(f"  Raw: {text[:200]}", file=sys.stderr)
        return None

def format_faq_yaml(faqs):
    """Format FAQ list as YAML for frontmatter."""
    lines = ["faq:"]
    for item in faqs:
        q = item["q"].replace("'", "''")
        a = item["a"].replace("'", "''")
        lines.append(f"- q: '{q}'")
        lines.append(f"  a: '{a}'")
    return "\n".join(lines)

def inject_faq_frontmatter(filepath, faqs):
    """Insert FAQ frontmatter into an existing .md file before closing ---."""
    with open(filepath) as f:
        content = f.read()
    
    # Find the closing --- of frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    
    fm_text = parts[1]
    body = parts[2]
    
    # Check if faq already exists
    if "faq:" in fm_text:
        return False  # Already has FAQ, skip
    
    # Format FAQ yaml
    faq_block = format_faq_yaml(faqs)
    
    # Insert before the closing frontmatter
    new_fm = fm_text.rstrip() + "\n" + faq_block
    new_content = f"---\n{new_fm}\n---{body}"
    
    with open(filepath, "w") as f:
        f.write(new_content)
    
    return True

def get_priority_articles():
    """Return list of high-value article filenames to process first."""
    # These are the top traffic-driving / search-intent articles
    priorities = [
        # Kitchen appliances - highest volume
        "beste-airfryer-2026.md",
        "beste-koffiemachine-2026.md",
        "beste-stofzuiger-2026.md",
        "beste-robotstofzuiger-2026.md",
        "beste-wasmachine-2026.md",
        "beste-koelkast-2026.md",
        "beste-vaatwasser-2026.md",
        "beste-inductiekookplaat-2026.md",
        "beste-waterkoker-2026.md",
        "beste-magnetron-2026.md",
        "beste-blender-2026.md",
        "beste-airconditioner-2026.md",
        "beste-strijkijzer-2026.md",
        "beste-luchtreiniger-2026.md",
        "beste-barbecue-2026.md",
        "beste-grasmaaier-2026.md",
        "beste-slowcooker-2026.md",
        "beste-staafmixer-2026.md",
        "beste-stoomreiniger-2026.md",
        "beste-tosti-ijzer-2026.md",
        
        # Comparison articles - high intent
        "airfryer-vs-friteuse-2026.md",
        "airfryer-vs-oven-2026.md",
        "stofzuiger-vs-steelstofzuiger-2026.md",
        "robotstofzuiger-vs-stofzuiger-2026.md",
        "inductie-vs-keramisch-2026.md",
        "wasmachine-vs-wasdroger-combi-2026.md",
        "koffiemachine-bonen-vs-cups-2026.md",
        "gasbarbecue-vs-houtskoolbarbecue-2026.md",
        "airconditioner-vs-luchtkoeler-2026.md",
        "waterkoker-vs-quooker-2026.md",
    ]
    
    results = []
    for fname in priorities:
        fpath = os.path.join(REVIEWS_DIR, fname)
        if os.path.exists(fpath):
            fm_text, body = get_frontmatter_and_body(fpath)
            if fm_text and body:
                parsed = parse_yaml_simple(fm_text)
                if "faq" not in parsed:
                    results.append((fpath, fname, body))
    
    return results

def main():
    print(f"KiesKeuken FAQ Generator — {MODEL}", file=sys.stderr)
    print(f"Scanning for articles without FAQ frontmatter...\n", file=sys.stderr)
    
    articles = get_priority_articles()
    print(f"Found {len(articles)} priority articles without FAQ", file=sys.stderr)
    
    if not articles:
        print("Nothing to do!", file=sys.stderr)
        return
    
    success = 0
    fail = 0
    skipped = 0
    
    for idx, (fpath, fname, body) in enumerate(articles):
        topic = fname.replace(".md", "").replace("-2026", "").replace("-", " ").title()
        print(f"\n[{idx+1}/{len(articles)}] {fname}", file=sys.stderr)
        
        try:
            faqs = generate_faq(body, topic)
            if faqs:
                injected = inject_faq_frontmatter(fpath, faqs)
                if injected:
                    print(f"  ✓ Added {len(faqs)} FAQ items", file=sys.stderr)
                    success += 1
                else:
                    print(f"  ⚠ FAQ already exists in frontmatter", file=sys.stderr)
                    skipped += 1
            else:
                print(f"  ✗ Empty/invalid FAQ response", file=sys.stderr)
                fail += 1
        except Exception as e:
            print(f"  ✗ Error: {e}", file=sys.stderr)
            fail += 1
        
        # Rate limit: 1 request per 2 seconds to avoid 429
        time.sleep(2.5)
    
    # Summary
    summary = {
        "success": success,
        "failed": fail,
        "skipped": skipped,
        "total": len(articles),
        "model": MODEL
    }
    
    print(f"\n\nDONE. Success: {success}, Failed: {fail}, Skipped: {skipped}/{len(articles)}", file=sys.stderr)
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
