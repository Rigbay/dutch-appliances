#!/usr/bin/env python3
"""
Dutch content site: article generation pipeline.

Usage:
  python generate-article.py --topic "beste-friteuse-2026" --model gemini
  python generate-article.py --batch article-list.json --model gemini

Requires: GEMINI_API_KEY env var (or pass via --api-key).
Produces: src/content/reviews/<slug>.md with correct frontmatter schema.
"""

import argparse
import json
import os
import sys
import time
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"
PROMPT_PATH = Path(__file__).resolve().parent / "prompt-template.txt"

CATEGORIES = ["huishoudelijk", "keuken", "schoonmaken"]

FIELDS = [
    "title",
    "slug",
    "description",
    "category",
    "rating",
    "priceRange",
    "pros",
    "cons",
    "affiliateLinks",
    "modelYear",
    "featuredProduct",
    "readingTime",
    "products",
    "related",
]

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = """Je bent een Nederlandse consumentenjournalist die eerlijke, praktische koopgidsen schrijft voor een Nederlandstalige website over huishoudelijke apparaten. Je schrijft vanuit het perspectief van iemand die de producten daadwerkelijk kent, maar je baseert je op productspecificaties en gebruikerservaringen — niet op een eigen fysieke test.

Schrijf een complete koopgids in het Nederlands over dit onderwerp:

ONDERWERP: {topic_nl}
CATEGORIE: {category}
DOELGROEP: {audience}
PRODUCTIDEEËN (suggesties, pas aan op basis van actuele kennis): {product_ideas}

STRUCTUUR (volg exact, maar wees creatief binnen elk blok):

1. **Inleiding** — 2-3 alinea's: waarom dit apparaat relevant is in 2026, welke praktische vragen de lezer moet stellen, en wat de gids wel/niet claimt. Noem de beste keuze (featured product) met concrete argumenten.

2. **Snel advies** — 3 bullets: "Kies X als je...", "Kies Y als je...", "Kies Z als je...". Per bullet: productnaam + de specifieke situatie/behoefte + het doorslaggevende voordeel.

3. **Beste keuze per budget** — 3-4 secties (Beste koop, Beste prestaties, Beste budget, Beste voor kleine keuken). Per sectie: productnaam, prijsrange, voor wie, concrete voor-/nadelen.

4. **Waar op letten?** — 3-4 alinea's: de onzichtbare eigenschappen die pas na weken gebruik duidelijk worden. Schoonmaak, geluidsniveau, formaat, vervangbare onderdelen, garantie.

5. **Vergelijkingstabel** — Markdown-tabel met 5+ producten, kolommen: Product | Inhoud | Vermogen | Prijs | Beste voor | Score.

6. **Conclusie** — 1-2 alinea's: de echte afweging, geen loze aanbeveling. Benoem wie beter voor een ander model kan kiezen.

UITVOERFORMAT — stuur ALLEEN de volgende JSON, geen andere tekst:

{{
  "title": "Beste [product] 2026: [ondertitel met doelgroep of use-case]",
  "description": "[120-170 tekens, SEO-geoptimaliseerd, met primaire keyword vooraan]",
  "category": "{category}",
  "priceRange": "EUR [min]-[max]",
  "pros": ["pro 1 (Nederlands)", "pro 2", "pro 3"],
  "cons": ["con 1 (Nederlands)", "con 2", "con 3"],
  "affiliateLinks": ["https://partner.bol.com/.../[SKU1]", "https://partner.bol.com/.../[SKU2]"],
  "featuredProduct": "[Naam beste product]",
  "readingTime": "[aantal] min",
  "modelYear": 2026,
  "products": [
    {{
      "name": "[Volledige productnaam]",
      "verdict": "[1 zin: waarom deze keuze]",
      "priceRange": "EUR [min]-[max]",
      "bestFor": "[Gebruiksscenario]",
      "rating": [1.0-5.0],
      "affiliateLink": "https://partner.bol.com/.../[SKU]"
    }}
  ],
  "related": ["[slug1]", "[slug2]", "[slug3]"],
  "body_markdown": "[DE VOLLEDIGE ARTIKELTEKST in Markdown, beginnend bij de inleiding, zonder de frontmatter — ALLEEN de body]"
}}

BELANGRIJK:
- Schrijf levendig, concreet, Nederlands. Geen ChatGPT-stijl superlatieven als "revolutionair" of "game-changer".
- Noem echte Nederlandse winkelnamen (Bol.com, Coolblue, MediaMarkt) waar relevant.
- Prijzen in euro's.
- Minimaal 1,500 woorden body tekst.
- Wees eerlijk over minpunten — een gids zonder kritiek is ongeloofwaardig.
"""

# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_gemini(prompt: str, api_key: str) -> dict:
    """Call Gemini 2.0 Flash API, return parsed JSON response."""
    import urllib.request
    import urllib.error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 8192,
        },
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Strip markdown code fences if present
            text = text.strip()
            if text.startswith("```"):
                lines = text.split("\n")
                lines = lines[1:]  # drop opening fence
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]  # drop closing fence
                text = "\n".join(lines)
            return json.loads(text)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"Gemini API error {e.code}: {body}") from e


# ---------------------------------------------------------------------------
# Article builder
# ---------------------------------------------------------------------------

def build_article(data: dict, slug: str, model_year: int = 2026) -> str:
    """Convert API response dict to a .md file with Astro frontmatter."""

    today = date.today().isoformat()

    lines = ["---"]

    # Static fields
    lines.append(f'title: "{data.get("title", slug)}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'description: "{data.get("description", "")}"')
    lines.append(f'category: "{data.get("category", "keuken")}"')
    rating = data.get("featuredProduct_rating", data.get("products", [{}])[0].get("rating", 4.5))
    lines.append(f"rating: {rating}")
    lines.append(f'priceRange: "{data.get("priceRange", "EUR 50-200")}"')

    # Pros (list)
    pros = data.get("pros", [])
    lines.append("pros:")
    for p in pros:
        lines.append(f'  - "{p}"')

    # Cons (list)
    cons = data.get("cons", [])
    lines.append("cons:")
    for c in cons:
        lines.append(f'  - "{c}"')

    # Affiliate links
    links = data.get("affiliateLinks", [])
    lines.append("affiliateLinks:")
    for link in links:
        lines.append(f'  - "{link}"')

    lines.append(f'date: {today}')
    lines.append(f"modelYear: {model_year}")
    lines.append(f'featuredProduct: "{data.get("featuredProduct", "")}"')
    lines.append(f'readingTime: "{data.get("readingTime", "8 min")}"')

    # Products array
    products = data.get("products", [])
    lines.append("products:")
    for p in products:
        lines.append(f'  - name: "{p.get("name", "")}"')
        lines.append(f'    verdict: "{p.get("verdict", "")}"')
        lines.append(f'    priceRange: "{p.get("priceRange", "")}"')
        lines.append(f'    bestFor: "{p.get("bestFor", "")}"')
        lines.append(f'    rating: {p.get("rating", 4.0)}')
        lines.append(f'    affiliateLink: "{p.get("affiliateLink", "")}"')

    # Related
    related = data.get("related", [])
    lines.append("related:")
    for r in related:
        lines.append(f'  - "{r}"')

    lines.append("draft: true")
    lines.append("---")
    lines.append("")

    # Body markdown
    body = data.get("body_markdown", "")
    lines.append(body.strip())

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Article list
# ---------------------------------------------------------------------------

DEFAULT_ARTICLES = [
    {
        "slug": "beste-friteuse-2026",
        "topic_nl": "de beste friteuses (hetelucht én olie) voor thuisgebruik",
        "category": "keuken",
        "audience": "gezinnen en thuiskoks die friet, snacks en zelfgemaakte gerechten willen frituren",
        "product_ideas": "Philips Premium Airfryer XXL, Princess Classic Friteuse, Tefal Oleoclean Pro, Inventum Professionele Friteuse, Domo Frituurpan",
    },
    {
        "slug": "beste-senseo-koffiezetapparaat-2026",
        "topic_nl": "de beste Senseo en pad-koffiezetapparaten voor snelle koffie",
        "category": "keuken",
        "audience": "Nederlandse koffiedrinkers die snel en makkelijk 1-2 kopjes willen zetten",
        "product_ideas": "Philips Senseo Original, Philips Senseo Switch, Melitta Purista, De'Longhi Nespresso, Krups Nespresso",
    },
    {
        "slug": "beste-slowcooker-2026",
        "topic_nl": "de beste slowcookers voor maaltijdvoorbereiding en stoofgerechten",
        "category": "keuken",
        "audience": "drukke huishoudens en meal-preppers die 's ochtends willen voorbereiden en 's avonds willen eten",
        "product_ideas": "Crock-Pot klassiek, Instant Pot Duo, Russell Hobbs, Tefal Cook4Me, Ninja Foodi",
    },
    {
        "slug": "beste-wasmachine-2026",
        "topic_nl": "de beste wasmachines voor gezinnen, energiezuinig en betrouwbaar",
        "category": "huishoudelijk",
        "audience": "Nederlandse huishoudens die een betrouwbare, energiezuinige wasmachine zoeken voor dagelijks gebruik",
        "product_ideas": "Miele W1, Bosch Serie 8, Siemens iQ500, Samsung EcoBubble, LG Direct Drive, AEG ProTex",
    },
    {
        "slug": "beste-wasdroger-2026",
        "topic_nl": "de beste wasdrogers: warmtepomp, condens en energiezuinig",
        "category": "huishoudelijk",
        "audience": "huishoudens die een droger willen naast of in plaats van de waslijn",
        "product_ideas": "Miele T1 Excellence, Bosch Serie 8 warmtepompdroger, AEG T8, Samsung OptimalDry, LG Dual Inverter",
    },
    {
        "slug": "beste-strijkijzer-2026",
        "topic_nl": "de beste strijkijzers en stoomgeneratoren voor kreukvrij wasgoed",
        "category": "huishoudelijk",
        "audience": "huishoudens die veel strijken en een betrouwbaar apparaat willen",
        "product_ideas": "Philips PerfectCare, Tefal Pro Express, Braun CareStyle, Bosch Sensixx, Laurastar",
    },
    {
        "slug": "beste-stofzuiger-met-zak-2026",
        "topic_nl": "de beste stofzuigers met zak: krachtig, hygiënisch en betrouwbaar",
        "category": "schoonmaken",
        "audience": "huishoudens die de voorkeur geven aan een traditionele stofzuiger met zak om hygiënische redenen of allergieën",
        "product_ideas": "Miele Complete C3, Bosch BGL8, Siemens VSQ8, Philips PowerPro Compact, AEG VX9",
    },
    {
        "slug": "beste-dweilrobot-2026",
        "topic_nl": "de beste dweilrobots en vloerreinigers voor harde vloeren",
        "category": "schoonmaken",
        "audience": "huishoudens met harde vloeren (laminaat, tegels, PVC) die dweilen willen automatiseren",
        "product_ideas": "iRobot Braava Jet, Roborock Dyad, Bissell CrossWave, Kärcher FC 7, Tineco Floor One S5",
    },
    {
        "slug": "beste-raamreiniger-2026",
        "topic_nl": "de beste elektrische raamreinigers en ramenwissers",
        "category": "schoonmaken",
        "audience": "huishoudens die ramen, douchewanden en spiegels streeploos schoon willen zonder gedoe",
        "product_ideas": "Kärcher WV 6 Plus, Leifheit Window Vac, Vileda Windomatic, Bosch GlassVAC, Kärcher WV 2",
    },
    {
        "slug": "beste-staafmixer-2026",
        "topic_nl": "de beste staafmixers voor soep, smoothies en babyvoeding",
        "category": "keuken",
        "audience": "thuiskoks die een veelzijdige staafmixer willen voor dagelijks gebruik",
        "product_ideas": "Braun MultiQuick, Philips ProMix, Bosch ErgoMixx, KitchenAid staafmixer, Tefal Optiblend",
    },
]


# ---------------------------------------------------------------------------
# Cost logger
# ---------------------------------------------------------------------------

class CostLogger:
    """Tracks API usage so we don't get surprise bills."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self.entries: list[dict] = []
        if log_path.exists():
            self.entries = json.loads(log_path.read_text())

    def record(self, model: str, tokens_in: int, tokens_out: int, cost_est: float, slug: str):
        entry = {
            "date": date.today().isoformat(),
            "model": model,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "cost_est": cost_est,
            "slug": slug,
        }
        self.entries.append(entry)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text(json.dumps(self.entries, indent=2))

    @property
    def total_cost(self) -> float:
        return sum(e["cost_est"] for e in self.entries)


# ---------------------------------------------------------------------------
# Cost estimation
# ---------------------------------------------------------------------------

# Gemini 2.5 Flash-Lite pricing (May 2026): $0.10/1M input, $0.40/1M output tokens
GEMINI_INPUT_COST = 0.10 / 1_000_000
GEMINI_OUTPUT_COST = 0.40 / 1_000_000


def estimate_cost_gemini(prompt_chars: int) -> tuple[int, int, float]:
    """Estimate tokens and cost for a Gemini article generation call."""
    tokens_in = int(prompt_chars / 3.5)
    tokens_out = 4000  # rough estimate for 1500-word Dutch article + JSON
    cost = (tokens_in * GEMINI_INPUT_COST) + (tokens_out * GEMINI_OUTPUT_COST)
    return tokens_in, tokens_out, cost


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Generate Dutch review articles")
    parser.add_argument("--topic", help="single topic slug to generate")
    parser.add_argument("--batch", help="JSON file with article list (see DEFAULT_ARTICLES for format)")
    parser.add_argument("--model", default="gemini", choices=["gemini"], help="LLM backend")
    parser.add_argument("--api-key", help="API key (or set GEMINI_API_KEY env)")
    parser.add_argument("--dry-run", action="store_true", help="show prompt, don't call API")
    parser.add_argument("--list", action="store_true", help="list built-in article topics and exit")
    parser.add_argument("--count", type=int, default=1, help="number of articles to generate (with --batch, take first N)")

    args = parser.parse_args()

    if args.list:
        for a in DEFAULT_ARTICLES:
            print(f"  {a['slug']}  [{a['category']}]  {a['topic_nl'][:80]}")
        return

    # API key
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key and not args.dry_run:
        print("ERROR: Set GEMINI_API_KEY env var or pass --api-key", file=sys.stderr)
        print("Get a free key: https://aistudio.google.com/app/apikey", file=sys.stderr)
        sys.exit(1)

    # Load article specs
    if args.batch:
        specs = json.loads(Path(args.batch).read_text())
    elif args.topic:
        spec = next((a for a in DEFAULT_ARTICLES if a["slug"] == args.topic), None)
        if spec is None:
            print(f"ERROR: topic '{args.topic}' not found in built-in list", file=sys.stderr)
            sys.exit(1)
        specs = [spec]
    else:
        specs = [DEFAULT_ARTICLES[0]]
        print(f"No --topic or --batch given. Defaulting to: {specs[0]['slug']}")

    specs = specs[: args.count]

    cost_logger = CostLogger(Path(__file__).resolve().parent / "cost-log.json")
    generated = 0

    for spec in specs:
        slug = spec["slug"]
        out_path = REVIEWS_DIR / f"{slug}.md"

        if out_path.exists() and not args.dry_run:
            print(f"SKIP {slug} — already exists")
            continue

        prompt = PROMPT_TEMPLATE.format(
            topic_nl=spec["topic_nl"],
            category=spec["category"],
            audience=spec["audience"],
            product_ideas=spec["product_ideas"],
        )

        if args.dry_run:
            print(f"=== PROMPT for {slug} ===")
            print(prompt[:500] + "...")
            print(f"=== Would write to {out_path} ===\n")
            continue

        tokens_in, tokens_out, cost = estimate_cost_gemini(len(prompt))

        print(f"GENERATING {slug} ({spec['category']}) — est. ${cost:.4f}...", end=" ", flush=True)
        t0 = time.time()

        try:
            data = call_gemini(prompt, api_key)
            article = build_article(data, slug, model_year=2026)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(article)
            cost_logger.record(args.model, tokens_in, tokens_out, cost, slug)
            elapsed = time.time() - t0
            print(f"OK ({elapsed:.1f}s, ${cost:.4f})")
            generated += 1
            time.sleep(2)  # rate-limit courtesy
        except Exception as e:
            print(f"FAILED: {e}")

    if generated > 0:
        print(f"\nDONE: {generated} article(s) generated")
        print(f"Total API cost this session: ${cost_logger.total_cost:.4f}")
        print(f"To build site: cd {SITE_ROOT} && npm run build")


if __name__ == "__main__":
    main()
