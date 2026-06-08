#!/usr/bin/env python3
"""
Generate contextual inline links from high-authority articles to thin (1-2 incoming) articles.
Uses Gemini API to find natural insertion points and generate Dutch link text.
"""
import os, json, re, subprocess, sys
from pathlib import Path

REVIEWS_DIR = "src/content/reviews"
ENV_FILE = os.path.expanduser("~/.hermes/.env")

# Load Gemini API key from .env
api_key = None
with open(ENV_FILE) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    print("FATAL: No GEMINI_API_KEY in ~/.hermes/.env")
    sys.exit(1)

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

# Thin articles and their best link sources (high-linked articles in same category)
THIN_CROSSLINKS = {
    "beste-vleesmolen-2026": [
        "beste-keukenmachine-2026",
        "beste-staafmixer-2026",
        "hakmolen-vs-keukenmachine-2026",
    ],
    "stoomreiniger-vs-hogedrukreiniger-2026": [
        "beste-stoomreiniger-2026",
        "beste-hogedrukreiniger-2026",
    ],
    "waterkoker-vs-quooker-2026": [
        "beste-waterkoker-2026",
        # beste-quooker doesn't exist; use related comparison
        "beste-koffiemachine-2026",
    ],
    "slowcooker-vs-stoomoven-2026": [
        "beste-slowcooker-2026",
        "beste-stoomoven-2026",
    ],
    "beste-kettingzaag-2026": [
        "beste-heggenschaar-2026",
        "beste-bosmaaier-2026",
    ],
    "beste-bakplaat-2026": [
        "beste-gourmetstel-2026",
        "beste-koekenpan-2026",
    ],
    "tosti-ijzer-vs-broodrooster-2026": [
        "beste-tosti-ijzer-2026",
        "beste-broodrooster-2026",
    ],
    "sapcentrifuge-vs-slowjuicer-2026": [
        "beste-sapcentrifuge-2026",
        "beste-slowjuicer-2026",
    ],
    "beste-kruimeldief-draadloos-2026": [
        "beste-steelstofzuiger-2026",
        "beste-draadloze-stofzuiger-2026",
    ],
    "koffiemachine-vs-senseo-2026": [
        "beste-koffiemachine-2026",
        "beste-senseo-koffiezetapparaat-2026",
    ],
    "beste-koffiecupmachine-2026": [
        "beste-koffiemachine-2026",
        "koffiemachine-bonen-vs-cups-2026",
    ],
    "beste-wafelijzer-2026": [
        "beste-bakplaat-2026",
        "beste-tosti-ijzer-2026",
    ],
    "steelstofzuiger-vs-draadloze-stofzuiger-2026": [
        "beste-steelstofzuiger-2026",
        "beste-draadloze-stofzuiger-2026",
    ],
    "airconditioner-vs-ventilator-2026": [
        "beste-airconditioner-2026",
        "beste-ventilator-2026",
    ],
    "beste-keukenmes-set-2026": [
        "beste-snijplank-2026",
        "beste-koekenpan-2026",
    ],
}

# Read target article info (slug, title)
def get_article_info(slug):
    filepath = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        return None, None
    with open(filepath) as f:
        content = f.read()
    # Extract title from frontmatter
    m = re.search(r"title:\s*'?([^'\n]+)'?", content)
    title = m.group(1).strip() if m else slug
    return content, title

# Read just frontmatter
def read_full(slug):
    filepath = os.path.join(REVIEWS_DIR, f"{slug}.md")
    with open(filepath) as f:
        return f.read()

def split_frontmatter(content):
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return parts[0] + "---" + parts[1] + "---", parts[2]
    return "", content

def call_gemini(prompt_text):
    """Call Gemini API for a single prompt."""
    import urllib.request, urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000}
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"  Gemini API error: {e}")
        return None

def find_unique_sentence_end(content_text, paragraph_start, paragraph_end):
    """Find a unique string boundary in a paragraph for patching."""
    # Get the paragraph
    para = content_text[paragraph_start:paragraph_end].strip()
    # Find last sentence ending (period followed by space)
    sentences = re.split(r'(?<=[.!?])\s+', para)
    if len(sentences) >= 2:
        # Return the last sentence as the anchor
        last = sentences[-1].strip()
        # Trim trailing punctuation for matching
        return last
    return para[-80:]

stats = {"attempted": 0, "inserted": 0, "failed": 0, "skipped": 0}

for thin_slug, source_slugs in THIN_CROSSLINKS.items():
    thin_content, thin_title = get_article_info(thin_slug)
    if not thin_content:
        print(f"SKIP: {thin_slug} not found")
        stats["skipped"] += 1
        continue

    # Get short link text from title
    short_title = thin_title.split(":")[0].strip().rstrip(".")
    if len(short_title) > 60:
        short_title = short_title[:57] + "…"

    for source_slug in source_slugs:
        source_content = read_full(source_slug)
        if not source_content:
            continue

        fm, body = split_frontmatter(source_content)

        # Skip if source already links to thin_slug
        if thin_slug in source_content:
            stats["skipped"] += 1
            continue

        stats["attempted"] += 1

        # Get a sample of the body (first 2500 chars) for Gemini
        body_sample = body[:2500]

        prompt = f"""Je bent een SEO-redacteur voor een Nederlandse website over keukenapparaten (KiesKeuken.nl).

Ik heb een bestaand artikel over "{thin_title}" (slug: {thin_slug}) dat meer interne links nodig heeft.

Taak: Voeg één natuurlijke, contextuele interne link toe in het VOLGENDE artikel. De link moet verwijzen naar het artikel "/{thin_slug}/".

Hier is het artikel waar je de link in moet plaatsen:

---
{body_sample}
---

BELANGRIJK:
- Kies één natuurlijk invoegpunt waar het relevant is om te verwijzen naar "{short_title}"
- Schrijf 1-2 nieuwe zinnen die het onderwerp introduceren en de link bevatten, of herschrijf 1-2 bestaande zinnen
- De linktekst moet natuurlijk Nederlands zijn (bijv. "onze uitgebreide {short_title.lower()} gids", "lees meer over {short_title.lower()}", etc.)
- Gebruik exact deze link-URL: /{thin_slug}/
- Plaats de nieuwe tekst logisch in de flow van het artikel

Geef ALLEEN het volgende JSON-object terug, niets anders:

{{"anchor": "de VOLLEDIGE zin die direct vóór de invoeging staat (gebruik deze als unieke zoek-string)", "position": "before" of "after", "new_text": "de nieuwe tekst DIE INGEVOEGD MOET WORDEN (inclusief de Markdown-link)"}}

De "anchor" tekst moet EXACT uit het origineel komen, lang genoeg om uniek te zijn (minimaal 40 karakters)."""

        result = call_gemini(prompt)
        if not result:
            stats["failed"] += 1
            continue

        # Parse JSON from result
        try:
            # Strip markdown code fences if present
            result = result.strip()
            if result.startswith("```"):
                result = re.sub(r'^```(?:json)?\s*\n?', '', result)
                result = re.sub(r'\n?```\s*$', '', result)

            data = json.loads(result)
            anchor = data.get("anchor", "").strip()
            position = data.get("position", "before")
            new_text = data.get("new_text", "").strip()

            if not anchor or not new_text:
                print(f"  FAILED (empty anchor/text): {source_slug} → {thin_slug}")
                stats["failed"] += 1
                continue

            # Verify anchor exists in source
            if anchor not in source_content:
                # Try with different whitespace
                anchor_escaped = re.escape(anchor)
                if not re.search(anchor_escaped, source_content):
                    print(f"  FAILED (anchor not found in source): '{anchor[:60]}...'")
                    stats["failed"] += 1
                    continue

            # Apply the insertion
            if position == "before":
                new_body = source_content.replace(anchor, new_text + " " + anchor, 1)
            else:
                new_body = source_content.replace(anchor, anchor + " " + new_text, 1)

            if new_body == source_content:
                print(f"  FAILED (no change after replace): {source_slug} → {thin_slug}")
                stats["failed"] += 1
                continue

            # Write back
            filepath = os.path.join(REVIEWS_DIR, f"{source_slug}.md")
            with open(filepath, "w") as f:
                f.write(new_body)

            print(f"  INSERTED: {source_slug} → {thin_slug}")
            stats["inserted"] += 1

            # Only insert one link per thin article per source to avoid over-linking
            break

        except json.JSONDecodeError as e:
            print(f"  FAILED (JSON parse): {e}")
            print(f"    Raw: {result[:200]}")
            stats["failed"] += 1
            continue
        except Exception as e:
            print(f"  FAILED: {e}")
            stats["failed"] += 1
            continue

print(f"\n=== Summary ===")
print(f"Attempted: {stats['attempted']}")
print(f"Inserted: {stats['inserted']}")
print(f"Failed: {stats['failed']}")
print(f"Skipped (already linked): {stats['skipped']}")
