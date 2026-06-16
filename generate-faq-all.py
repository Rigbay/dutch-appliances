#!/usr/bin/env python3
"""Generate FAQ frontmatter for ALL KiesKeuken articles without it, using Gemini API.

Processes every article in src/content/reviews/ that lacks `faq:` frontmatter.
Rate limit: 5s between calls. Skips articles that already have FAQ.
"""

import os, sys, json, requests, re, time

REVIEWS_DIR = os.path.expanduser("/home/cls/kieskeuken/src/content/reviews")
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
    with open(filepath) as f:
        content = f.read()
    if not content.startswith("---"):
        return None, None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, None
    return parts[1].strip(), parts[2].strip()

def has_faq(fm_text):
    """Check if frontmatter already has faq: key."""
    return "faq:" in fm_text

def generate_faq(article_content, topic, max_chars=8000):
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
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "topP": 0.95,
            "maxOutputTokens": 4000
        }
    }

    resp = None
    for attempt in range(8):
        try:
            resp = requests.post(API_URL, json=payload, timeout=60)
            if resp.status_code == 429:
                wait = 35 * (attempt + 1)
                print(f"  429 wait {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            if resp.status_code in (503, 500):
                print(f"  {resp.status_code} retry 30s", file=sys.stderr)
                time.sleep(30)
                continue
            if resp.status_code != 200:
                print(f"  HTTP {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
                return None
            break
        except requests.exceptions.Timeout:
            print(f"  Timeout, retry 15s", file=sys.stderr)
            time.sleep(15)
        except Exception as e:
            print(f"  Exception: {e}", file=sys.stderr)
            time.sleep(15)
    
    if resp is None or resp.status_code != 200:
        return None
    
    data = resp.json()
    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()

    # Strip markdown code blocks
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    try:
        faqs = json.loads(text)
        if isinstance(faqs, list) and len(faqs) >= 2:
            return faqs
    except json.JSONDecodeError:
        pass

    # Salvage attempts
    if text.rstrip().endswith(','):
        text = text.rstrip().rstrip(',') + '\n]'
    elif not text.rstrip().endswith(']'):
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

def format_faq_yaml(faqs):
    lines = ["faq:"]
    for item in faqs:
        q = item["q"].replace("'", "''")
        a = item["a"].replace("'", "''")
        lines.append(f"- q: '{q}'")
        lines.append(f"  a: '{a}'")
    return "\n".join(lines)

def inject_faq_frontmatter(filepath, faqs):
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    fm_text = parts[1]
    body = parts[2]
    if "faq:" in fm_text:
        return False
    faq_block = format_faq_yaml(faqs)
    new_fm = fm_text.rstrip() + "\n" + faq_block
    new_content = f"---\n{new_fm}\n---{body}"
    with open(filepath, "w") as f:
        f.write(new_content)
    return True

def get_all_articles_needing_faq():
    """Return ALL articles that don't have FAQ frontmatter."""
    results = []
    for fname in sorted(os.listdir(REVIEWS_DIR)):
        if not fname.endswith(".md"):
            continue
        fpath = os.path.join(REVIEWS_DIR, fname)
        fm_text, body = get_frontmatter_and_body(fpath)
        if fm_text and body and not has_faq(fm_text):
            results.append((fpath, fname, body))
    return results

def main():
    print(f"KiesKeuken FAQ Generator (ALL articles) — {MODEL}", file=sys.stderr)

    articles = get_all_articles_needing_faq()
    print(f"Found {len(articles)} articles without FAQ\n", file=sys.stderr)

    if not articles:
        print("All articles have FAQ! Nothing to do.", file=sys.stderr)
        print(json.dumps({"success": 0, "failed": 0, "skipped": 0, "total": 0}))
        return

    success = 0
    fail = 0
    skipped = 0

    for idx, (fpath, fname, body) in enumerate(articles):
        topic = fname.replace(".md", "").replace("-2026", "").replace("-", " ").title()
        print(f"[{idx+1}/{len(articles)}] {fname}", file=sys.stderr)

        try:
            faqs = generate_faq(body, topic)
            if faqs:
                injected = inject_faq_frontmatter(fpath, faqs)
                if injected:
                    print(f"  ✓ Added {len(faqs)} FAQ items", file=sys.stderr)
                    success += 1
                else:
                    print(f"  ⚠ FAQ already exists (race?)", file=sys.stderr)
                    skipped += 1
            else:
                print(f"  ✗ Empty/invalid FAQ response", file=sys.stderr)
                fail += 1
        except Exception as e:
            print(f"  ✗ Error: {e}", file=sys.stderr)
            fail += 1

        # Rate limit: 5s between calls
        time.sleep(5.0)

    summary = {
        "success": success,
        "failed": fail,
        "skipped": skipped,
        "total": len(articles),
        "model": MODEL
    }

    print(f"\nDONE. Success: {success}, Failed: {fail}, Skipped: {skipped}/{len(articles)}", file=sys.stderr)
    print(json.dumps(summary))

if __name__ == "__main__":
    main()
