#!/usr/bin/env python3
"""Generate 5 high-impact comparison articles for July 9, 2026 using Gemini 2.5 Flash-Lite.

Targets missing comparison gaps with high Dutch search volume.
Amazon NL affiliate links (kieskeukennl-21).
"""
import json, os, sys, time
from pathlib import Path
from datetime import date

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"

AMAZON_TAG = "kieskeukennl-21"
TODAY = date.today().isoformat()

# 5 high-value comparison gaps — none exist yet, all have individual articles
TOPICS = [
    {
        "slug": "braadpan-vs-wokpan-2026",
        "title": "Braadpan vs. Wokpan 2026: Stoofpot of Roerbak — Welke Pan Past bij Jouw Kookstijl?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Braadpan vs Wokpan 2026.

Context: Juli 2026. Nederlanders koken steeds diverser — van Hollandse stoofpot tot Aziatische roerbak. Het grote verschil: een braadpan (dikke bodem, hoge rand, deksel) is voor sudderen, stoven en braden. Een wokpan (dunne bodem, schuine hoge rand) is voor snel roerbakken op hoog vuur.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — braadpan vs wokpan: twee totaal verschillende kookfilosofieën
2. Snel advies — 3 bullets wie wat moet kiezen (stoofpot-liefhebber, roerbak-fan, beide)
3. Hoe werkt het? — technisch verschil: materiaal (gietijzer vs carbonstaal), warmteverdeling, kooktechniek
4. Vergelijkingstabel — 6 producten: Product | Type | Materiaal | Diameter | Prijs | Score
5. Diepere vergelijking: warmtebron (inductie vs gas), onderhoud (inbranden wok vs schoonmaken braadpan), veelzijdigheid
6. Conclusie — wanneer kies je wat, en waarom een combi niet altijd werkt

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: BK Braadpan Gietijzer 24cm, Le Creuset Braadpan 24cm, Tefal Braadpan Jamie Oliver, Tefal Wokpan Unlimited, BK Wokpan Carbonstaal 32cm, Scanpan Wokpan CTX
- Minimaal 1500 woorden
- Eerlijk over minpunten (braadpan is zwaar, wokpan moet ingebrand worden)
- Prijzen in euro's""",
        "product_names": [
            "BK Braadpan Gietijzer 24cm",
            "Le Creuset Braadpan 24cm",
            "Tefal Braadpan Jamie Oliver",
            "Tefal Wokpan Unlimited",
            "BK Wokpan Carbonstaal 32cm",
            "Scanpan Wokpan CTX"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=BK+braadpan+gietijzer+24cm&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Le+Creuset+braadpan+24cm&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Tefal+braadpan+Jamie+Oliver&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Tefal+wokpan+Unlimited&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=BK+wokpan+carbonstaal+32cm&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Scanpan+wokpan+CTX&tag={AMAZON_TAG}"
        ],
        "related": ["beste-braadpan-2026", "beste-wokpan-2026", "koekenpan-vs-braadpan-2026"]
    },
    {
        "slug": "pannenset-vs-losse-pannen-2026",
        "title": "Pannenset vs. Losse Pannen 2026: Complete Set of Zelf Samenstellen — Wat is Slimmer?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Pannenset vs Losse Pannen 2026.

Context: Juli 2026. Bij het inrichten van een keuken sta je voor de keuze: een complete pannenset kopen of zelf losse pannen samenstellen. Een pannenset is voordeliger per pan en matcht qua design, maar je krijgt misschien pannen die je nooit gebruikt. Losse pannen zijn duurder per stuk maar je koopt alleen wat je echt nodig hebt.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — de eeuwige keukenvraag: set of los?
2. Snel advies — 3 bullets: starter (set), ervaren kok (los), budgetbewust (set)
3. Wat zit er in een pannenset? — typische samenstelling (koekenpan, steelpan, kookpan, braadpan) en wat je echt gebruikt
4. Vergelijkingstabel — 6 opties: 3 sets + 3 losse pannen: Product | Type | Aantal stuks | Materiaal | Prijs | Score
5. Diepere vergelijking: kosten per pan, kwaliteit per stuk, opbergruimte, garantie
6. Conclusie — voor wie is een set de beste keuze, en wanneer loont los kopen

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Tefal Ingenio Pannenset 10-delig, BK Pannenset 5-delig, GreenPan Pannenset Memphis, BK Koekenpan 28cm (los), Tefal Steelpan 16cm (los), GreenPan Braadpan 24cm (los)
- Minimaal 1500 woorden
- Eerlijk over minpunten (set bevat pannen die je nooit gebruikt, los kopen is duurder per pan)
- Prijzen in euro's""",
        "product_names": [
            "Tefal Ingenio Pannenset 10-delig",
            "BK Pannenset 5-delig",
            "GreenPan Pannenset Memphis",
            "BK Koekenpan 28cm",
            "Tefal Steelpan 16cm",
            "GreenPan Braadpan 24cm"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Tefal+Ingenio+pannenset+10+delig&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=BK+pannenset+5+delig&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=GreenPan+pannenset+Memphis&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=BK+koekenpan+28cm&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Tefal+steelpan+16cm&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=GreenPan+braadpan+24cm&tag={AMAZON_TAG}"
        ],
        "related": ["beste-pannenset-2026", "beste-koekenpan-2026", "beste-braadpan-2026"]
    },
    {
        "slug": "elektrische-deken-vs-infraroodpaneel-2026",
        "title": "Elektrische Deken vs. Infraroodpaneel 2026: Persoonlijk Verwarmen of de Hele Kamer — Wat Bespaart Meer?",
        "category": "huishouden",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Elektrische Deken vs Infraroodpaneel 2026.

Context: Juli 2026. Met hoge energieprijzen zoeken Nederlanders naar manieren om gericht te verwarmen in plaats van het hele huis. Een elektrische deken verwarmt alleen jouw lichaam (zeer zuinig, ~0,06 kWh per uur). Een infraroodpaneel verwarmt objecten en personen in de ruimte (~0,3-0,8 kWh). Beide zijn goedkoper dan centrale verwarming maar werken fundamenteel anders.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — energie besparen in 2026: gericht verwarmen vs hele huis
2. Snel advies — 3 bullets: bankzitter (deken), thuiswerker (paneel), beide (combi)
3. Hoe werkt het? — technisch verschil: weerstandsdraden in textiel vs infraroodstraling op objecten
4. Vergelijkingstabel — 6 producten: Product | Type | Vermogen | Verwarmd oppervlak | Prijs | Score
5. Diepere vergelijking: energieverbruik per uur, warmtegevoel, veiligheid, levensduur
6. Conclusie — wanneer kies je wat, en waarom een combi vaak de beste oplossing is

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Stoov Big Hug Elektrische Deken, Inventum Elektrische Deken HN131, Medisana Elektrische Onderdeken, Eurom Infraroodpaneel 400W, Mill Infraroodpaneel 600W, Klarstein Infraroodpaneel 800W
- Minimaal 1500 woorden
- Eerlijk over minpunten (deken alleen voor zittend/liggend, paneel verwarmt niet de lucht)
- Prijzen in euro's, energieverbruik in kWh en euro's per uur""",
        "product_names": [
            "Stoov Big Hug Elektrische Deken",
            "Inventum Elektrische Deken HN131",
            "Medisana Elektrische Onderdeken",
            "Eurom Infraroodpaneel 400W",
            "Mill Infraroodpaneel 600W",
            "Klarstein Infraroodpaneel 800W"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Stoov+Big+Hug+elektrische+deken&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Inventum+elektrische+deken+HN131&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Medisana+elektrische+onderdeken&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Eurom+infraroodpaneel+400W&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Mill+infraroodpaneel+600W&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Klarstein+infraroodpaneel+800W&tag={AMAZON_TAG}"
        ],
        "related": ["beste-elektrische-deken-2026", "beste-elektrische-kachel-2026", "elektrische-kachel-vs-infraroodpaneel-2026"]
    },
    {
        "slug": "snoeischaar-vs-heggenschaar-2026",
        "title": "Snoeischaar vs. Heggenschaar 2026: Precisie Snoeien of Meters Maken — Welk Gereedschap voor Jouw Tuin?",
        "category": "tuin",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Snoeischaar vs Heggenschaar 2026.

Context: Juli 2026, midden in het tuinseizoen. Nederlanders met een tuin staan voor de keuze: een snoeischaar voor precisiewerk aan takken en struiken, of een heggenschaar voor het snel bijwerken van hagen en grote struiken. Het fundamentele verschil: snoeischaar = precisie per tak (handmatig, tot ~2,5 cm dikte), heggenschaar = snelheid over oppervlak (elektrisch/accu, scheert hele vlakken).

STRUCTUUR:
1. Inleiding (2-3 alinea's) — tuinseizoen 2026: het juiste gereedschap voor elke klus
2. Snel advies — 3 bullets: rozen/fruitbomen (snoeischaar), haagbezitter (heggenschaar), beide (combi)
3. Hoe werkt het? — technisch verschil: bypass vs aambeeld snoeischaar, accu vs elektrisch vs benzine heggenschaar
4. Vergelijkingstabel — 6 producten: Product | Type | Snijlengte/Meslengte | Gewicht | Prijs | Score
5. Diepere vergelijking: precisie, snelheid, vermoeidheid bij lang gebruik, onderhoud (slijpen vs olie)
6. Conclusie — wanneer kies je wat, en waarom de meeste tuiniers beide nodig hebben

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Felco 2 Snoeischaar, Gardena Bypass Snoeischaar, Fiskars PowerGear Snoeischaar, Bosch Heggenschaar EasyHedgeCut 18V, Gardena Heggenschaar Accu 18V, Black+Decker Heggenschaar 600W
- Minimaal 1500 woorden
- Eerlijk over minpunten (snoeischaar is traag voor hagen, heggenschaar te grof voor precisiewerk)
- Prijzen in euro's""",
        "product_names": [
            "Felco 2 Snoeischaar",
            "Gardena Bypass Snoeischaar",
            "Fiskars PowerGear Snoeischaar",
            "Bosch Heggenschaar EasyHedgeCut 18V",
            "Gardena Heggenschaar Accu 18V",
            "Black+Decker Heggenschaar 600W"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Felco+2+snoeischaar&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Gardena+bypass+snoeischaar&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Fiskars+PowerGear+snoeischaar&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+EasyHedgeCut+18V+heggenschaar&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Gardena+heggenschaar+accu+18V&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Black+Decker+heggenschaar+600W&tag={AMAZON_TAG}"
        ],
        "related": ["beste-snoeischaar-2026", "beste-heggenschaar-2026", "heggenschaar-vs-bosmaaier-2026"]
    },
    {
        "slug": "yoghurtmaker-vs-zelf-maken-2026",
        "title": "Yoghurtmaker vs. Zelf Yoghurt Maken 2026: Apparaat of Oven/Pan — Wat Geeft de Beste Yoghurt?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Yoghurtmaker vs Zelf Yoghurt Maken 2026.

Context: Juli 2026. Zelf yoghurt maken is populair: goedkoper dan supermarkt, controle over ingrediënten, minder plastic afval. Je kunt een speciaal yoghurtmaker-apparaat kopen (constante temperatuur, set-and-forget) of yoghurt maken met bestaande keukenspullen (ovenlamp, pan, thermoskan). Het fundamentele verschil: gemak en consistentie vs kosten en flexibiliteit.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — zelf yoghurt maken: apparaat of DIY-methode?
2. Snel advies — 3 bullets: gemakzoeker (yoghurtmaker), budgetbewust (zelf maken), experimenteerlustig (zelf maken)
3. Hoe werkt het? — technisch verschil: yoghurtmaker (thermostaat, 42°C constant) vs DIY (ovenlamp, warmhoudpan, thermoskan)
4. Vergelijkingstabel — 6 opties: 3 apparaten + 3 DIY-methoden: Product/Methode | Type | Capaciteit | Consistentie | Kosten | Score
5. Diepere vergelijking: smaakconsistentie, tijdsinvestering, schoonmaak, elektriciteitsverbruik
6. Conclusie — wanneer loont een yoghurtmaker, en wanneer is DIY net zo goed

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Severin Yoghurtmaker JG3521, Rommelsbacher Yoghurtmaker JG80, Tefal Yoghurtmaker YG654, DIY met ovenlamp, DIY met thermoskan, DIY met warmhoudpan
- Minimaal 1500 woorden
- Eerlijk over minpunten (yoghurtmaker neemt kastruimte, DIY is minder consistent)
- Prijzen in euro's""",
        "product_names": [
            "Severin Yoghurtmaker JG3521",
            "Rommelsbacher Yoghurtmaker JG80",
            "Tefal Yoghurtmaker YG654",
            "DIY Yoghurt met Ovenlamp",
            "DIY Yoghurt met Thermoskan",
            "DIY Yoghurt met Warmhoudpan"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Severin+yoghurtmaker+JG3521&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Rommelsbacher+yoghurtmaker+JG80&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Tefal+yoghurtmaker+YG654&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=yoghurt+maken+startpakket&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=thermoskan+1+liter&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=yoghurt+culturen+starter&tag={AMAZON_TAG}"
        ],
        "related": ["beste-yoghurtmaker-2026", "beste-keukenmachine-2026", "beste-slowcooker-2026"]
    },
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
    link_count = min(5, len(topic["product_links"]))
    for link in topic["product_links"][:link_count]:
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
            time.sleep(3)
        except Exception as e:
            print(f"FAILED: {e}")

    print(f"\nDONE: {generated} article(s) generated")
    if generated > 0:
        print("To deploy: git add src/content/reviews/*.md && git commit && git push")


if __name__ == "__main__":
    main()
