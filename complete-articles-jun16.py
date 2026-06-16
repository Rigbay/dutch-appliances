#!/usr/bin/env python3
"""Complete 3 truncated articles using llama3.2 via Ollama.
Hermes cron job — June 16, 2026
"""

import os, sys, json, urllib.request, urllib.error

OUT_DIR = "/workspace/kieskeuken/src/content/reviews"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:latest"

def call_ollama(prompt):
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 2048, "top_p": 0.9}
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

def complete_article(filepath, description):
    with open(filepath) as f:
        existing = f.read()
    
    fm_end = existing.find("---", 3)
    if fm_end < 0:
        print(f"  Cannot find frontmatter end in {filepath}")
        return False
    
    frontmatter = existing[:fm_end+3]
    body = existing[fm_end+3:].strip()
    
    # Find the last complete section heading
    last_headings = [l for l in body.split("\n") if l.startswith("## ")]
    last_section = last_headings[-1] if last_headings else "het artikel"
    
    prompt = f"""Je bent een Nederlandse copywriter voor KiesKeuken.nl. Voltooi dit vergelijkingsartikel over {description}.

Het artikel is afgebroken na de sectie "{last_section}".

Hier is het bestaande artikel:

{body}

Schrijf ALLEEN de ontbrekende secties vanaf waar het artikel is afgebroken. Gebruik ## voor koppen. Schrijf in vlot, natuurlijk Nederlands. Wees eerlijk over minpunten. Eindig met de conclusie en deze exacte affiliate disclosure:

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou. Rangschikking gebaseerd op productspecificaties, gebruikerservaringen en prijs-kwaliteitverhouding.

Schrijf minimaal 400 woorden. Stop niet halverwege. Eindig met de disclosure."""
    
    completion = call_ollama(prompt)
    if not completion or len(completion) < 200:
        print(f"  Failed ({len(completion) if completion else 0} chars)")
        return False
    
    # Clean up
    completion = completion.strip()
    if completion.startswith("```"):
        lines = completion.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        completion = "\n".join(lines)
    
    full = frontmatter + "\n" + body + "\n\n" + completion
    
    with open(filepath, "w") as f:
        f.write(full)
    
    print(f"  Completed: {filepath} ({len(full)} chars, +{len(completion)} chars)")
    return True

def main():
    articles = [
        ("koelkast-vs-amerikaanse-koelkast-2026.md", "koelkasten vs Amerikaanse koelkasten"),
        ("wasdroger-vs-droogrek-2026.md", "wasdrogers vs droogrekken"),
        ("magnetron-vs-heteluchtoven-2026.md", "magnetrons vs heteluchtovens"),
    ]
    
    for slug, desc in articles:
        filepath = os.path.join(OUT_DIR, slug)
        if not os.path.exists(filepath):
            print(f"  SKIP: {slug} not found")
            continue
        print(f"\nCompleting: {slug}...")
        complete_article(filepath, desc)
    
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
