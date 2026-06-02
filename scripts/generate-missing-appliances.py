#!/usr/bin/env python3
"""Generate 5 new Dutch appliance review articles for missing high-intent topics."""
import os, json, time, sys, re, urllib.request, urllib.parse, urllib.error
from datetime import date

API_KEY = open(os.path.expanduser("~/.hermes/private/gemini-api-key")).read().strip()
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
OUT_DIR = "/workspace/kieskeuken/src/content/reviews"
COST_LOG = "/workspace/kieskeuken/scripts/cost-log.json"

TOPICS = [
    {
        "slug": "beste-broodmachine-2026",
        "title": "Beste broodmachine 2026: 7 modellen voor zelfgebakken brood thuis",
        "description": "Vergelijk de beste broodbakmachines van 2026: van budget tot premium, met glutenvrije programma's en tijdsinstellingen voor perfect vers brood.",
        "category": "keuken",
        "model_year": 2026,
        "featured": "Moulinex OW6101 Home & Bread",
        "related": ["beste-keukenmachine-2026", "beste-handmixer-2026", "beste-staafmixer-2026"],
        "tools": [
            ("Moulinex OW6101 Home & Bread", 4.5, "80-110", "Beste allround"),
            ("Panasonic SD-ZP2000KXE", 4.7, "150-200", "Beste premium"),
            ("Princess 112020", 4.0, "50-70", "Beste budget"),
            ("Kenwood BM580", 4.3, "90-130", "Beste design"),
            ("Severin BM 3995", 4.2, "60-85", "Beste compact"),
            ("Inventum BM810", 4.1, "55-80", "Beste instapmodel"),
            ("Gastroback 40964 Design Brotbackautomat", 4.4, "120-160", "Beste rijk aan programma's"),
        ],
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste broodbakmachines van 2026.\n\n"
            "Behandel deze 7 modellen:\n"
            "1. Moulinex OW6101 Home & Bread (80-110 EUR, beste allround)\n"
            "2. Panasonic SD-ZP2000KXE (150-200 EUR, beste premium met 3-in-1)\n"
            "3. Princess 112020 (50-70 EUR, beste budget)\n"
            "4. Kenwood BM580 (90-130 EUR, beste design)\n"
            "5. Severin BM 3995 (60-85 EUR, beste compact voor kleine keukens)\n"
            "6. Inventum BM810 (55-80 EUR, beste instapmodel)\n"
            "7. Gastroback 40964 (120-160 EUR, rijk aan programma's)\n\n"
            "Voor elk model: naam, prijs, beste use case, pluspunten, minpunten en verdict.\n"
            "Vergelijkingstabel in markdown met kolommen: model, prijs, beste voor, score (1-5).\n"
            "Advies: voor wie kies je welk model? (beginner, gevorderde bakker, kleine keuken, glutenvrij)\n"
            "3 FAQ-vragen over broodbakmachines.\n"
            "Gebruik ## koppen. Nederlands. Geen YAML frontmatter."
        ),
    },
    {
        "slug": "beste-wafelijzer-2026",
        "title": "Beste wafelijzer 2026: 7 modellen voor Belgische, Luikse en Amerikaanse wafels",
        "description": "Vergelijk de beste wafelijzers van 2026: van klassiek Vierkant tot Luikse en Amerikaanse modellen. Vind het perfecte wafelijzer voor thuis.",
        "category": "keuken",
        "model_year": 2026,
        "featured": "Tefal Waffle'in SW612D",
        "related": ["beste-pannenkoekenpan-2026", "beste-tosti-ijzer-2026", "beste-broodrooster-2026"],
        "tools": [
            ("Tefal Waffle'in SW612D", 4.6, "60-85", "Beste allround"),
            ("Princess 113035", 4.0, "30-45", "Beste budget"),
            ("Clatronic WM 3576", 3.9, "25-40", "Beste goedkoop"),
            ("Lacor 69180", 4.2, "40-60", "Beste Luikse wafels"),
            ("Severin WK 3455", 4.1, "35-50", "Beste compact"),
            ("Tristar WA-2431", 4.0, "25-35", "Beste instap"),
            ("Russell Hobbs 23820-56", 4.3, "50-70", "Beste Amerikaanse wafels"),
        ],
        "prompt": (
            "Schrijf een Nederlands artikel van 1000-1300 woorden over de beste wafelijzers van 2026.\n\n"
            "Behandel deze 7 modellen:\n"
            "1. Tefal Waffle'in SW612D (60-85 EUR, beste allround)\n"
            "2. Princess 113035 (30-45 EUR, beste budget)\n"
            "3. Clatronic WM 3576 (25-40 EUR, beste goedkoop)\n"
            "4. Lacor 69180 (40-60 EUR, beste voor Luikse wafels)\n"
            "5. Severin WK 3455 (35-50 EUR, beste compact)\n"
            "6. Tristar WA-2431 (25-35 EUR, beste instap)\n"
            "7. Russell Hobbs 23820-56 (50-70 EUR, beste voor Amerikaanse wafels)\n\n"
            "Voor elk model: naam, prijs, beste use case, pluspunten, minpunten, verdict.\n"
            "Vergelijkingstabel. Leg uit: verschil tussen Belgische, Luikse en Amerikaanse wafels.\n"
            "Welk model past bij welk type wafel? 3 FAQ-vragen.\n"
            "Gebruik ## koppen. Nederlands. Geen YAML frontmatter."
        ),
    },
    {
        "slug": "beste-rijstkoker-2026",
        "title": "Beste rijstkoker 2026: 7 modellen voor perfecte rijst elke keer",
        "description": "Vergelijk de beste rijstkokers van 2026: van basismodellen tot inductie rijstkokers met meerdere programma's voor sushi, basmati en volkorenrijst.",
        "category": "keuken",
        "model_year": 2026,
        "featured": "Yum Asia Panda Mini",
        "related": ["beste-keukenmachine-2026", "beste-slowcooker-2026", "beste-wokpan-2026"],
        "tools": [
            ("Yum Asia Panda Mini", 4.6, "70-100", "Beste allround"),
            ("Zojirushi NS-YSQ10", 4.8, "150-220", "Beste premium"),
            ("Reishunger Digital", 4.3, "40-60", "Beste middenklasse"),
            ("Princess 102060", 3.9, "25-40", "Beste budget"),
            ("Yum Asia Bamboo", 4.5, "90-130", "Beste inductie"),
            ("Severin RK 7020", 4.0, "30-45", "Beste compact"),
            ("Russell Hobbs 26750-56", 4.1, "35-50", "Beste instap"),
        ],
        "prompt": (
            "Schrijf een Nederlands artikel van 1000-1300 woorden over de beste rijstkokers van 2026.\n\n"
            "Behandel deze 7 modellen:\n"
            "1. Yum Asia Panda Mini (70-100 EUR, beste allround met fuzzy logic)\n"
            "2. Zojirushi NS-YSQ10 (150-220 EUR, beste premium inductie)\n"
            "3. Reishunger Digital (40-60 EUR, beste middenklasse)\n"
            "4. Princess 102060 (25-40 EUR, beste budget)\n"
            "5. Yum Asia Bamboo (90-130 EUR, beste inductie)\n"
            "6. Severin RK 7020 (30-45 EUR, beste compact)\n"
            "7. Russell Hobbs 26750-56 (35-50 EUR, beste instap)\n\n"
            "Voor elk model: naam, prijs, beste use case, pluspunten, minpunten, verdict.\n"
            "Vergelijkingstabel. Leg het verschil uit tussen gewone, fuzzy logic en inductie rijstkokers.\n"
            "3 FAQ-vragen.\n"
            "Gebruik ## koppen. Nederlands. Geen YAML frontmatter."
        ),
    },
    {
        "slug": "beste-ijsmachine-2026",
        "title": "Beste ijsmachine 2026: 7 modellen voor zelfgemaakt roomijs en sorbet",
        "description": "Vergelijk de beste ijsmachines van 2026: van goedkope modellen met vrieskom tot premium compressormodellen voor dagelijks zelfgemaakt ijs.",
        "category": "keuken",
        "model_year": 2026,
        "featured": "Cuisinart ICE-100",
        "related": ["beste-blender-2026", "beste-slowcooker-2026", "beste-keukenmachine-2026"],
        "tools": [
            ("Cuisinart ICE-100", 4.7, "300-400", "Beste compressor"),
            ("Nemox Gelato Chef 2200", 4.5, "200-300", "Beste professioneel"),
            ("UNOLD 48856", 4.3, "80-120", "Beste middenklasse"),
            ("Princess 283039", 3.8, "40-60", "Beste budget"),
            ("Severin Eismaschine KM 3873", 4.0, "50-70", "Beste instap"),
            ("Klarmann Edelstahl", 4.2, "70-100", "Beste design"),
            ("Gastroback 41016", 4.4, "150-200", "Beste groot volume"),
        ],
        "prompt": (
            "Schrijf een Nederlands artikel van 1000-1300 woorden over de beste ijsmachines van 2026.\n\n"
            "Behandel deze 7 modellen:\n"
            "1. Cuisinart ICE-100 (300-400 EUR, beste compressor - geen vrieskom nodig)\n"
            "2. Nemox Gelato Chef 2200 (200-300 EUR, beste professioneel)\n"
            "3. UNOLD 48856 (80-120 EUR, beste middenklasse met vrieskom)\n"
            "4. Princess 283039 (40-60 EUR, beste budget met vrieskom)\n"
            "5. Severin Eismaschine KM 3873 (50-70 EUR, beste instap)\n"
            "6. Klarmann Edelstahl (70-100 EUR, beste design)\n"
            "7. Gastroback 41016 (150-200 EUR, beste groot volume)\n\n"
            "Voor elk model: naam, prijs, beste use case, pluspunten, minpunten, verdict.\n"
            "Vergelijkingstabel. Leg uit: verschil tussen vrieskom en compressor.\n"
            "Hoe lang van tevoren de kom invriezen? Sorbet versus roomijs?\n"
            "3 FAQ-vragen.\n"
            "Gebruik ## koppen. Nederlands. Geen YAML frontmatter."
        ),
    },
    {
        "slug": "beste-espresso-apparaat-2026",
        "title": "Beste espressapparaat 2026: 7 modellen voor de perfecte espresso thuis",
        "description": "Vergelijk de beste espressomachines van 2026: van semiautomatisch tot volautomatisch. Vind het perfecte espressapparaat voor thuis met stoompijpje en ingebouwde molen.",
        "category": "keuken",
        "model_year": 2026,
        "featured": "Sage Barista Express Impress",
        "related": ["beste-nespresso-apparaat-2026", "espresso-vs-filterkoffie-2026", "beste-filterkoffiemachine-2026"],
        "tools": [
            ("Sage Barista Express Impress", 4.7, "700-900", "Beste allround"),
            ("DeLonghi Magnifica S ECAM 22.110.SB", 4.5, "400-550", "Beste volautomatisch"),
            ("Gaggia Classic Pro E24", 4.4, "350-450", "Beste semiautomatisch"),
            ("Sage Bambino Plus", 4.3, "300-400", "Beste compact"),
            ("DeLonghi Dedica Style EC685", 4.2, "200-300", "Beste budget"),
            ("Rancilio Silvia", 4.6, "450-600", "Beste voor liefhebbers"),
            ("ECM Classika PID", 4.7, "1000-1400", "Beste professioneel"),
        ],
        "prompt": (
            "Schrijf een Nederlands artikel van 1200-1500 woorden over de beste espressomachines van 2026.\n\n"
            "Behandel deze 7 modellen:\n"
            "1. Sage Barista Express Impress (700-900 EUR, beste allround met ingebouwde molen)\n"
            "2. DeLonghi Magnifica S ECAM 22.110.SB (400-550 EUR, beste volautomatisch)\n"
            "3. Gaggia Classic Pro E24 (350-450 EUR, beste semiautomatisch)\n"
            "4. Sage Bambino Plus (300-400 EUR, beste compact)\n"
            "5. DeLonghi Dedica Style EC685 (200-300 EUR, beste budget)\n"
            "6. Rancilio Silvia (450-600 EUR, beste voor liefhebbers)\n"
            "7. ECM Classika PID (1000-1400 EUR, beste professioneel single boiler)\n\n"
            "Voor elk model: naam, prijs, beste use case, pluspunten, minpunten, verdict.\n"
            "Vergelijkingstabel. Leg uit: verschil tussen semiautomatisch en volautomatisch.\n"
            "Waarom is een goede molen belangrijk? Wat is het verschil met Nespresso?\n"
            "3 FAQ-vragen.\n"
            "Gebruik ## koppen. Nederlands. Geen YAML frontmatter."
        ),
    },
]


def make_amazon_slug(name):
    """Make a URL-safe search term from a product name."""
    s = name.lower()
    s = s.replace("'", "").replace("&", " ").replace("  ", " ")
    s = s.replace("(", "").replace(")", "").replace(",", "")
    return s.replace(" ", "+")


def call_gemini(prompt_text, retries=3):
    """Call Gemini API and return generated content."""
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4000,
        }
    }
    url = BASE_URL + "?key=" + API_KEY

    for attempt in range(retries):
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    resp_data = json.loads(resp.read().decode("utf-8"))
                    candidates = resp_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            text = parts[0].get("text", "")
                            if text:
                                return text
            print(f"  No text in response, attempt {attempt+1}")
            time.sleep(3)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            if e.code == 429:
                wait = (attempt + 1) * 5
                print(f"  Rate limited (429), waiting {wait}s...")
                time.sleep(wait)
            elif e.code == 400:
                print(f"  400 error: {body[:300]}")
                if "SAFETY" in body:
                    return "[BLOCKED]"
                return None
            else:
                print(f"  HTTP {e.code}: {body[:200]}")
                time.sleep(3)
        except Exception as e:
            print(f"  Error: {e}")
            time.sleep(3)
    return None


def clean_body_text(text):
    """Remove accidental YAML frontmatter from body."""
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    return text.strip()


def extract_reading_time(text):
    """Estimate reading time from word count."""
    words = len(text.split())
    minutes = max(5, round(words / 200))
    return f"{minutes} min"


def build_frontmatter(topic, body_text):
    """Build YAML frontmatter for an article."""
    products_lines = []
    for tool_name, rating, price, best_for in topic["tools"]:
        amz_slug = make_amazon_slug(tool_name)
        escaped_name = tool_name.replace('"', "'")
        verdict = f"De {best_for.lower()} met een score van {rating}/5."
        products_lines.append(
            f'  - name: "{escaped_name}"\n'
            f'    verdict: "{verdict}"\n'
            f'    priceRange: "EUR {price}"\n'
            f'    bestFor: "{best_for}"\n'
            f'    rating: {rating}\n'
            f'    affiliateLink: "https://www.amazon.nl/s?k={amz_slug}&tag=kieskeukennl-21"'
        )

    affiliate_links = []
    for tool_name, _rating, _price, _best_for in topic["tools"]:
        amz_slug = make_amazon_slug(tool_name)
        affiliate_links.append(
            f'- "https://www.amazon.nl/s?k={amz_slug}&tag=kieskeukennl-21"'
        )

    related_str = "\n".join(f'- "{r}"' for r in topic["related"])

    title_escaped = topic["title"].replace("'", "\\'")
    desc_escaped = topic["description"].replace('"', "'")

    price_ranges = [p for _, _, p, _ in topic["tools"]]
    low_prices = []
    high_prices = []
    for pr in price_ranges:
        parts = pr.split("-")
        if len(parts) == 2:
            try:
                low_prices.append(float(parts[0]))
                high_prices.append(float(parts[1]))
            except ValueError:
                pass

    if low_prices and high_prices:
        price_range_str = f"EUR {min(low_prices):.0f}-{max(high_prices):.0f}"
    else:
        price_range_str = "EUR 50-500"

    frontmatter = (
        "---\n"
        f"title: '{title_escaped}'\n"
        f"slug: {topic['slug']}\n"
        f'description: "{desc_escaped}"\n'
        f"category: {topic['category']}\n"
        f"rating: 4.2\n"
        f"priceRange: '{price_range_str}'\n"
        "pros:\n"
        "- Uitgebreide keuze in elke prijsklasse\n"
        "- Duidelijke specificaties beschikbaar voor vergelijken\n"
        "cons:\n"
        "- Prijs en kwaliteit verschillen sterk per merk\n"
        "- Niet alle modellen geschikt voor elke keuken\n"
        "affiliateLinks:\n"
        + "\n".join(affiliate_links) + "\n"
        f"date: {date.today().isoformat()}\n"
        f"modelYear: {topic['model_year']}\n"
        f'featuredProduct: "{topic["featured"]}"\n'
        f'readingTime: "{extract_reading_time(body_text)}"\n'
        "products:\n"
        + "\n".join(products_lines) + "\n"
        "related:\n"
        + related_str + "\n"
        "draft: false\n"
        "---\n"
    )
    return frontmatter


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    cost = {"model": "gemini-2.5-flash-lite", "requests": 0, "tokens_input": 0, "tokens_output": 0, "cost_eur": 0.0}

    for i, topic in enumerate(TOPICS):
        slug = topic["slug"]
        fpath = os.path.join(OUT_DIR, f"{slug}.md")

        if os.path.exists(fpath):
            print(f"[{i+1}/{len(TOPICS)}] SKIP: {slug}.md exists")
            continue

        print(f"[{i+1}/{len(TOPICS)}] Generating: {topic['title']}...")

        body = call_gemini(topic["prompt"])
        if body is None:
            print(f"  FAILED after retries")
            continue
        if body == "[BLOCKED]":
            print(f"  BLOCKED by safety filters")
            continue

        body = clean_body_text(body)
        cost["requests"] += 1

        frontmatter = build_frontmatter(topic, body)
        content = frontmatter + body + "\n"

        with open(fpath, "w") as f:
            f.write(content)

        input_chars = len(topic["prompt"])
        output_chars = len(body)
        cost["tokens_input"] += input_chars // 4
        cost["tokens_output"] += output_chars // 4

        print(f"  Written to {slug}.md ({len(body)} chars, {extract_reading_time(body)})")
        time.sleep(3)

    cost["cost_eur"] = round(
        cost["tokens_input"] * 0.075 / 1_000_000 + cost["tokens_output"] * 0.30 / 1_000_000, 4
    )

    try:
        existing = json.loads(open(COST_LOG).read()) if os.path.exists(COST_LOG) else []
        existing.append(cost)
        with open(COST_LOG, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        print(f"Cost log write failed: {e}")

    print(f"\nSummary:")
    print(f"  New articles: {cost['requests']}")
    print(f"  Estimated input tokens: {cost['tokens_input']}")
    print(f"  Estimated output tokens: {cost['tokens_output']}")
    print(f"  Estimated cost: EUR {cost['cost_eur']}")


if __name__ == "__main__":
    main()