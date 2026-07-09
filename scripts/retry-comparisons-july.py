#!/usr/bin/env python3
"""Retry failed comparison article generation with backoff."""
import json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

SITE_ROOT = Path("/workspace/kieskeuken")
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"
AMAZON_TAG = "kieskeukennl-21"
TODAY = "2026-07-08"

# Load API key
api_key = None
env_path = Path.home() / ".hermes" / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip("'\"")
            break
if not api_key:
    print("ERROR: GEMINI_API_KEY not found", file=sys.stderr)
    sys.exit(1)

# The 4 failed topics
TOPICS = [
    {
        "slug": "sapcentrifuge-vs-blender-2026",
        "title": "Sapcentrifuge vs. Blender 2026: Sap of Smoothie — Wat Past bij Jouw Gezonde Routine?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Sapcentrifuge vs Blender 2026.

Context: Juli 2026, zomer. Nederlanders willen gezonder leven met sapjes en smoothies. Het grote verschil: een sapcentrifuge scheidt pulp van sap (puur sap, minder vezels), een blender mixt alles (smoothie, meer vezels, dikker).

STRUCTUUR:
1. Inleiding (2-3 alinea's) — sapcentrifuge vs blender: het fundamentele verschil in wat je drinkt
2. Snel advies — 3 bullets wie wat moet kiezen (sap-liefhebber, smoothie-fan, beide)
3. Hoe werkt het? — technisch verschil: centrifuge (sneldraaiend mes + zeef) vs blender (draaiende messen in kan)
4. Vergelijkingstabel — 6 producten: Product | Type | Vermogen | Inhoud | Prijs | Score
5. Diepere vergelijking: voedingswaarde (vezels vs puur sap), schoonmaakgemak, geluidsniveau, veelzijdigheid
6. Conclusie — wanneer kies je wat, en waarom een combi-apparaat niet altijd de oplossing is

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Philips Viva Compact Sapcentrifuge, Princess Sapcentrifuge, Bosch VitaPower Blender, Philips Blender 5000 Series, KitchenBrothers Slowjuicer (als alternatief), NutriBullet Blender
- Minimaal 1500 woorden
- Eerlijk over minpunten (schoonmaken sapcentrifuge is gedoe, blender maakt geen puur sap)
- Prijzen in euro's""",
        "product_names": [
            "Philips Viva Compact Sapcentrifuge HR1832/00",
            "Princess Sapcentrifuge 201950",
            "Bosch VitaPower Blender MMB6174B",
            "Philips Blender 5000 Series HR3573/90",
            "KitchenBrothers Slowjuicer KB696",
            "NutriBullet Blender 600 Series"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Philips+Viva+Compact+sapcentrifuge+HR1832&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Princess+sapcentrifuge+201950&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+VitaPower+blender+MMB6174B&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+blender+5000+series+HR3573&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=KitchenBrothers+slowjuicer+KB696&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=NutriBullet+blender+600&tag={AMAZON_TAG}"
        ],
        "related": ["beste-sapcentrifuge-2026", "beste-blender-2026", "sapcentrifuge-vs-slowjuicer-2026"]
    },
    {
        "slug": "wasmachine-bovenlader-vs-voorlader-2026",
        "title": "Wasmachine Bovenlader vs. Voorlader 2026: Ruimte, Gemak en Wasresultaat Vergeleken",
        "category": "huishoudelijk",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Wasmachine Bovenlader vs Voorlader 2026.

Context: Juli 2026. Nederlanders met kleine badkamers of wasruimtes twijfelen tussen een bovenlader (smaller, geen bukken, sneller) en een voorlader (groter, energiezuiniger, stapelbaar met droger).

STRUCTUUR:
1. Inleiding (2-3 alinea's) — bovenlader vs voorlader: het fundamentele ontwerpverschil
2. Snel advies — wie kiest wat (kleine ruimte, rugklachten, groot gezin)
3. Hoe werkt het? — technisch verschil: bovenlader (trommel verticaal, wassen met minder water) vs voorlader (trommel horizontaal, zwaartekracht helpt)
4. Vergelijkingstabel — 6 producten: Product | Type | Capaciteit | Energielabel | Prijs | Score
5. Diepere vergelijking: wasresultaat, waterverbruik, energieverbruik, geluid, plaatsing (onder aanrecht vs vrijstaand), ergonomie
6. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Miele WDB 030 Bovenlader, Bosch WAT284A9NL Voorlader, AEG L7FEE965R Voorlader, Siemens WU14UT60NL Bovenlader, Samsung WW90T534DAE Voorlader, Whirlpool TDLR 70220 Bovenlader
- Minimaal 1500 woorden
- Eerlijk over minpunten (bovenlader: minder capaciteit, niet stapelbaar; voorlader: bukken, langer programma)
- Prijzen in euro's""",
        "product_names": [
            "Miele WDB 030 Bovenlader",
            "Bosch WAT284A9NL Voorlader",
            "AEG L7FEE965R Voorlader",
            "Siemens WU14UT60NL Bovenlader",
            "Samsung WW90T534DAE Voorlader",
            "Whirlpool TDLR 70220 Bovenlader"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Miele+WDB+030+bovenlader&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+WAT284A9NL+voorlader&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=AEG+L7FEE965R+voorlader&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Siemens+WU14UT60NL+bovenlader&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Samsung+WW90T534DAE+voorlader&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Whirlpool+TDLR+70220+bovenlader&tag={AMAZON_TAG}"
        ],
        "related": ["beste-wasmachine-2026", "wasmachine-vs-wasdroger-2026", "wasmachine-vs-wasdroger-combi-2026"]
    },
    {
        "slug": "airfryer-vs-slowcooker-2026",
        "title": "Airfryer vs. Slowcooker 2026: Snel Krokant of Langzaam Smaakvol — Welke Past bij Jou?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Airfryer vs Slowcooker 2026.

Context: Juli 2026. Twee populaire keukenapparaten met totaal verschillende kookfilosofieën: de airfryer (hete lucht, snel, krokant, friet/snacks) en de slowcooker (lage temperatuur, urenlang, stoofvlees/soepen). Veel Nederlanders vragen zich af welke ze écht nodig hebben.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — airfryer vs slowcooker: snelheid vs smaakontwikkeling
2. Snel advies — wie kiest wat (druk gezin, meal-prepper, frituurliefhebber)
3. Hoe werkt het? — airfryer (hete luchtcirculatie, Maillard-reactie) vs slowcooker (lage temperatuur, lang garen, collageenafbraak)
4. Vergelijkingstabel — 6 producten: Product | Type | Capaciteit | Vermogen | Prijs | Score
5. Diepere vergelijking: gerechten die je kunt maken, energieverbruik, kooktijd, schoonmaak, veelzijdigheid
6. Conclusie — waarom veel huishoudens beide hebben, en welke je eerst moet kopen

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Philips Airfryer XXL, Ninja Foodi Max Dual Zone, Crock-Pot Slowcooker, Instant Pot Duo (multicooker als alternatief), Princess Aerofryer XXL, Russell Hobbs Slowcooker
- Minimaal 1500 woorden
- Eerlijk over minpunten (airfryer: kleine capaciteit, droogt uit; slowcooker: planning nodig, geen krokant resultaat)
- Prijzen in euro's""",
        "product_names": [
            "Philips Airfryer XXL HD9650/90",
            "Ninja Foodi Max Dual Zone AF400EU",
            "Crock-Pot Slowcooker 4.7L",
            "Instant Pot Duo 7-in-1 Multicooker",
            "Princess Aerofryer XXL 182065",
            "Russell Hobbs Slowcooker 3.5L"
        ],
        "product_links": [
            f"https://www.amazon.nl/dp/B07VHKMGFX?tag={AMAZON_TAG}",
            f"https://www.amazon.nl/dp/B09B1XGZ4H?tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Crock-Pot+slowcooker+4.7L&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Instant+Pot+Duo+7-in-1&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Princess+Aerofryer+XXL+182065&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Russell+Hobbs+slowcooker+3.5L&tag={AMAZON_TAG}"
        ],
        "related": ["beste-airfryer-2026", "beste-slowcooker-2026", "airfryer-vs-friteuse-2026", "slowcooker-vs-snelkookpan-2026"]
    },
    {
        "slug": "stofzuiger-vs-bezem-2026",
        "title": "Stofzuiger vs. Bezem 2026: Wanneer is een Bezem Beter dan een Stofzuiger?",
        "category": "schoonmaken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Stofzuiger vs Bezem 2026.

Context: Juli 2026. Een verrassend veelgezochte vergelijking: wanneer volstaat een goede bezem en wanneer heb je echt een stofzuiger nodig? Voor kleine appartementen, studentenkamers, snelle schoonmaakbeurten en harde vloeren is het antwoord niet altijd vanzelfsprekend.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — stofzuiger vs bezem: niet zo gek als het klinkt, zeker voor kleine ruimtes en harde vloeren
2. Snel advies — wie kiest wat (student, appartement met laminaat, gezinswoning met tapijt)
3. Wanneer een bezem beter is — harde vloeren, snelle schoonmaak, geen stopcontact, stil, gratis
4. Wanneer een stofzuiger beter is — tapijt, allergieën, huisdieren, grondige reiniging
5. Vergelijkingstabel — 6 producten: Product | Type | Geschikt voor | Prijs | Score
6. Hybride oplossingen — steelstofzuiger als gulden middenweg, kruimeldief voor kleine rommel
7. Conclusie

BELANGRIJK:
- Amazon NL links met tag={AMAZON_TAG}
- Products: Leifheit Vloerwisser Set, Philips PowerPro Compact Stofzuiger, Dyson V8 Steelstofzuiger, Brabantia Bezemset, Kärcher WD3 Nat/Droog Stofzuiger, Swiffer Dweilsysteem
- Minimaal 1500 woorden
- Eerlijk over minpunten (bezem: stof opwervelen, niet voor tapijt; stofzuiger: lawaai, stroom, zwaar)
- Prijzen in euro's""",
        "product_names": [
            "Leifheit Vloerwisser Set",
            "Philips PowerPro Compact Stofzuiger FC9332/09",
            "Dyson V8 Absolute Steelstofzuiger",
            "Brabantia Bezemset",
            "Kärcher WD3 Nat/Droog Stofzuiger",
            "Swiffer Dweilsysteem"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Leifheit+vloerwisser+set&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+PowerPro+Compact+FC9332&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Dyson+V8+Absolute+steelstofzuiger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Brabantia+bezemset&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=K%C3%A4rcher+WD3+stofzuiger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Swiffer+dweilsysteem&tag={AMAZON_TAG}"
        ],
        "related": ["beste-stofzuiger-2026", "beste-steelstofzuiger-2026", "stofzuiger-vs-steelstofzuiger-2026", "robotstofzuiger-vs-stofzuiger-2026"]
    }
]


def call_gemini(prompt_text, api_key, retries=3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={api_key}"
    body = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192},
    }
    for attempt in range(retries):
        try:
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
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < retries - 1:
                wait = (attempt + 1) * 10
                print(f"503, retrying in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise
        except Exception:
            if attempt < retries - 1:
                wait = (attempt + 1) * 5
                print(f"error, retrying in {wait}s...", end=" ", flush=True)
                time.sleep(wait)
            else:
                raise


def build_article(topic, body_md):
    title = topic["title"]
    slug = topic["slug"]
    category = topic["category"]
    related = topic["related"]
    desc_slug = slug.replace("-vs-", " vs ").replace("-2026", "").replace("-", " ")

    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'slug: "{slug}"')
    lines.append(f'description: "Vergelijk {desc_slug} in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21)."')
    lines.append(f'category: "{category}"')
    lines.append("rating: 4.5")
    lines.append('priceRange: "EUR 15-1500"')
    lines.append("pros:")
    lines.append('  - "Eerlijke vergelijking met concrete voor- en nadelen per type"')
    lines.append('  - "Actuele prijzen en modellen voor 2026"')
    lines.append('  - "Helder advies voor elke woonsituatie en budget"')
    lines.append("cons:")
    lines.append('  - "Prijzen kunnen wijzigen afhankelijk van aanbiedingen"')
    lines.append('  - "Niet elk model is getest in dagelijks gebruik"')
    lines.append('  - "Sommige specificaties zijn afhankelijk van woningtype"')
    lines.append("affiliateLinks:")
    for link in topic["product_links"][:5]:
        lines.append(f'  - "{link}"')
    lines.append(f"date: {TODAY}")
    lines.append("modelYear: 2026")
    lines.append(f'featuredProduct: "{topic["product_names"][0]}"')
    lines.append('readingTime: "10 min"')
    lines.append("products:")
    for i, name in enumerate(topic["product_names"]):
        lines.append(f'  - name: "{name}"')
        lines.append(f'    verdict: "Vergelijkingsproduct — zie tabel voor volledige specificaties."')
        lines.append(f'    priceRange: "EUR 15-1500"')
        lines.append(f'    bestFor: "Vergelijking {desc_slug}"')
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
            time.sleep(5)
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\nDONE: {generated} article(s) generated")


if __name__ == "__main__":
    main()
