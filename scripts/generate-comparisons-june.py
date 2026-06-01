#!/usr/bin/env python3
"""Generate high-impact comparison articles for June 2026 using Gemini 2.5 Flash-Lite.

Targets summer search volume gaps with Amazon NL affiliate links (kieskeukennl-21).
"""
import json, os, sys, time
from pathlib import Path
from datetime import date

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"

AMAZON_TAG = "kieskeukennl-21"
TODAY = date.today().isoformat()

# High-value topics for June 2026
TOPICS = [
    {
        "slug": "airconditioner-vs-luchtkoeler-2026",
        "title": "Airconditioner vs. Luchtkoeler 2026: Welke Houdt Jouw Huis Koel deze Zomer?",
        "category": "huishoudelijk",
        "prompt": """Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Airconditioner vs Luchtkoeler 2026.

Context: Juni 2026, Nederlandse zomer. Zoekers vergelijken mobiele airco's met luchtkoelers voor thuisgebruik.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — waarom dit relevant is in juni 2026, verschil tussen echte koeling (airco met compressor) en verdampingskoeling (luchtkoeler)
2. Snel advies — 3 bullets wie wat moet kiezen
3. Hoe werkt het? — technisch verschil tussen compressor vs verdampingskoeling
4. Vergelijkingstabel — 6 producten: Product | Type | Koelvermogen | Energieverbruik | Prijs | Score
5. Kostenvergelijking — aanschaf, stroomkosten per zomer, geluidsniveau
6. Conclusie

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Midea Portofoon Airco, TCL MobiCool, Honeywell Luchtkoeler, Klarstein Icebreaker, Princess Smart Airco, Trotec Luchtkoeler
- Minimaal 1500 woorden
- Eerlijk over minpunten (lawaai, slang, condensafvoer)
- Prijzen in euro's""",
        "product_names": [
            "Midea Portofoon Airco",
            "TCL MobiCool Portable AC",
            "Honeywell Windrunner Luchtkoeler",
            "Klarstein Icebreaker 7000",
            "Princess Smart Airco 372000",
            "Trotec PAC 2600 X"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Midea+Portofoon+Airco&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=TCL+MobiCool+airco&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Honeywell+Windrunner+luchtkoeler&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Klarstein+Icebreaker+7000&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Princess+Smart+Airco+372000&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Trotec+PAC+2600&tag={AMAZON_TAG}"
        ],
        "related": ["beste-airconditioner-2026", "beste-elektrische-kachel-2026", "beste-luchtbevochtiger-2026"]
    },
    {
        "slug": "stoomreiniger-vs-hogedrukreiniger-2026",
        "title": "Stoomreiniger vs. Hogedrukreiniger 2026: Welke Kies Je voor Binnen of Buiten?",
        "category": "schoonmaken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Stoomreiniger vs Hogedrukreiniger 2026.

Context: Juni 2026. Nederlandse huishoudens die terras, tuinmeubelen, keuken of badkamer grondig willen reinigen - met stoom of hoge druk.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — verschil tussen stoomreinigen (binnen, ontsmetten, vet) en hogedrukreinigen (buiten, terras, auto)
2. Snel advies — wie kiest wat
3. Hoe werkt het en wanneer?
4. Vergelijkingstabel — 6 producten: Product | Type | Druk/Temp | Toepassing | Prijs | Score
5. Verdieping: schoonmaakresultaat, waterverbruik, onderhoud
6. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Kärcher SC 5 Stoomreiniger, Kärcher K5 Hogedrukreiniger, Bissell SteamShot, Nilfisk C120, Polti Vaporetto, Kärcher K2 Classic
- Minimaal 1500 woorden
- Eerlijk over minpunten
- Prijzen in euro's""",
        "product_names": [
            "Kärcher SC 5 Stoomreiniger",
            "Kärcher K5 Premium Hogedrukreiniger",
            "Bissell SteamShot Deluxe",
            "Nilfisk C120 Hogedrukreiniger",
            "Polti Vaporetto Lympha",
            "Kärcher K2 Classic"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=K%C3%A4rcher+SC+5+stoomreiniger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=K%C3%A4rcher+K5+hogedrukreiniger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bissell+SteamShot&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Nilfisk+C120+hogedrukreiniger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Polti+Vaporetto+Lympha&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=K%C3%A4rcher+K2+classic&tag={AMAZON_TAG}"
        ],
        "related": ["beste-stoomreiniger-2026", "beste-hogedrukreiniger-2026", "beste-tapijtreiniger-2026"]
    },
    {
        "slug": "inductie-vs-keramisch-2026",
        "title": "Inductie vs. Keramische Kookplaat 2026: Snelheid vs. Budget — Wat Past bij Jou?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Inductie vs Keramische Kookplaat 2026.

Context: Juni 2026. Nederlandse huishoudens die geen gas meer willen en kiezen tussen inductie (magneetveld, snel, duur) en keramisch (stralingswarmte, goedkoper).

STRUCTUUR:
1. Inleiding — inductie vs keramisch: snelheid vs betaalbaarheid
2. Snel advies — wie kiest wat
3. Technisch verschil: hoe werkt inductie (magneetveld) vs keramisch (stralingswarmte)
4. Vergelijkingstabel — 6 kookplaten
5. Diepere vergelijking: kooksnelheid, veiligheid, pannen, energieverbruik, prijs
6. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Siemens EX875KVS1E Inductie, Bosch PXE875DC1E Inductie, AEG IKE85471FB Inductie, Siemens EX645HEC1E Keramisch, Bosch NKN645G14 Keramisch, Inventum IK3015 Inductie
- Minimaal 1500 woorden
- Eerlijk over minpunten
- Prijzen in euro's""",
        "product_names": [
            "Siemens EX875KVS1E Inductie",
            "Bosch PXE875DC1E Inductie",
            "AEG IKE85471FB Inductie",
            "Siemens EX645HEC1E Keramisch",
            "Bosch NKN645G14 Keramisch",
            "Inventum IK3015 Inductie"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Siemens+EX875KVS1E+inductiekookplaat&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+PXE875DC1E+inductiekookplaat&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=AEG+IKE85471FB+inductiekookplaat&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Siemens+keramische+kookplaat&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+NKN645G14+keramische+kookplaat&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Inventum+IK3015+inductiekookplaat&tag={AMAZON_TAG}"
        ],
        "related": ["beste-inductiekookplaat-2026", "inductie-vs-gasfornuis-2026", "beste-afzuigkap-2026"]
    }
]


def call_gemini(prompt_text, api_key):
    import urllib.request, urllib.error
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text


def build_article(topic, body_md):
    """Build full .md content with frontmatter."""
    title = topic["title"]
    slug = topic["slug"]
    category = topic["category"]
    related = topic["related"]

    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'description: "Vergelijk {slug.replace("-vs-", " vs ").replace("-2026", "").replace("-", " ")} in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21)."')
    lines.append(f'category: "{category}"')
    lines.append("rating: 4.5")
    lines.append("priceRange: \"EUR 40-1500\"")
    lines.append("pros:")
    lines.append("  - \"Eerlijke vergelijking met concrete voor- en nadelen per type\"")
    lines.append("  - \"Actuele prijzen en modellen voor 2026\"")
    lines.append("  - \"Helder advies voor elke woonsituatie en budget\"")
    lines.append("cons:")
    lines.append("  - \"Prijzen kunnen wijzigen afhankelijk van aanbiedingen\"")
    lines.append("  - \"Niet elk model is getest in dagelijks gebruik\"")
    lines.append("  - \"Sommige specificaties zijn afhankelijk van woningtype\"")
    lines.append("affiliateLinks:")
    link_count = min(5, len(topic["product_links"]))
    for link in topic["product_links"][:link_count]:
        lines.append(f'  - "{link}"')
    lines.append(f"date: {TODAY}")
    lines.append("modelYear: 2026")
    lines.append(f'featuredProduct: "{topic["product_names"][0]}"')
    lines.append("readingTime: \"10 min\"")
    lines.append("products:")
    for i, name in enumerate(topic["product_names"]):
        lines.append(f'  - name: "{name}"')
        lines.append(f'    verdict: "Vergelijkingsproduct — zie tabel voor volledige specificaties."')
        lines.append(f'    priceRange: "EUR 50-800"')
        lines.append(f'    bestFor: "Vergelijking {slug.replace("-vs-", " vs ").replace("-2026", "").replace("-", " ")}"')
        lines.append(f'    rating: 4.5')
        lines.append(f'    affiliateLink: "{topic["product_links"][i]}"')
    lines.append("related:")
    for r in related:
        lines.append(f'  - "{r}"')
    lines.append("draft: false")
    lines.append("---")
    lines.append("")
    lines.append(body_md)
    return "\n".join(lines) + "\n"


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        env_path = Path.home() / ".hermes" / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip("'\"")
                    break
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    generated = 0
    for topic in TOPICS:
        slug = topic["slug"]
        out_path = REVIEWS_DIR / f"{slug}.md"
        if out_path.exists():
            print(f"SKIP {slug} — already exists")
            continue

        print(f"GENERATING {slug}...", end=" ", flush=True)
        t0 = time.time()
        try:
            body_md = call_gemini(topic["prompt"], api_key)
            article = build_article(topic, body_md)
            REVIEWS_DIR.mkdir(parents=True, exist_ok=True)
            out_path.write_text(article)
            elapsed = time.time() - t0
            print(f"OK ({elapsed:.1f}s, ~{len(body_md)} chars)")
            generated += 1
            time.sleep(2)
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\nDONE: {generated} article(s) generated")
    if generated > 0:
        print(f"To build: cd {SITE_ROOT} && npm run build")
        print(f"To deploy: git add src/content/reviews/*.md && git commit -m 'Add June comparison articles' && git push")


if __name__ == "__main__":
    main()