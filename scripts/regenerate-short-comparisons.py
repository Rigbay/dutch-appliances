#!/usr/bin/env python3
"""Regenerate short comparison articles with higher token limits."""

import os, json, requests, time, sys

key = None
with open(os.path.expanduser('~/.hermes/.env')) as f:
    for line in f:
        if 'GEMINI_API_KEY' in line and not line.strip().startswith('#'):
            key = line.split('=',1)[1].strip().strip('"')
            break

URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}'

# Articles to regenerate (short ones)
TO_REGENERATE = [
    {
        "slug": "filterkoffie-vs-koffiecups-2026",
        "title": "Filterkoffie vs. Koffiecups 2026: Voordelig Zetten of Supersnel Gemak — Wat Past bij Jou?",
        "description": "Vergelijk filterkoffie vs koffiecups in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21).",
        "category": "keuken",
        "priceRange": "EUR 30-300",
        "readingTime": "9 min",
        "rating": 4.4,
        "featuredProduct": "Moccamaster KBG Select vs. Philips Senseo",
        "related": ["beste-filterkoffiemachine-2026", "beste-koffiecupmachine-2026", "beste-koffiemachine-2026", "koffiemachine-bonen-vs-cups-2026"],
        "products": [
            {"name": "Moccamaster KBG Select", "verdict": "De gouden standaard voor filterkoffie — handgemaakt in Nederland, 10 jaar garantie.", "priceRange": "EUR 220-260", "bestFor": "Filterkoffie-puristen die kwaliteit waarderen", "rating": 4.8, "affiliateLink": "https://www.amazon.nl/s?k=Moccamaster+KBG+Select&tag=kieskeukennl-21"},
            {"name": "Philips Grind & Brew", "verdict": "Filterkoffiemachine met ingebouwde bonenmaler — verser dan voorgemalen koffie.", "priceRange": "EUR 120-180", "bestFor": "Liefhebbers van verse filterkoffie zonder aparte maler", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/s?k=Philips+Grind+%26+Brew&tag=kieskeukennl-21"},
            {"name": "Philips Senseo Original", "verdict": "De klassieke cupmachine — snel, eenvoudig en met schuimlaagje.", "priceRange": "EUR 60-90", "bestFor": "Snelle koffiedrinkers die één of twee kopjes per keer zetten", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/s?k=Philips+Senseo+Original&tag=kieskeukennl-21"},
            {"name": "Dolce Gusto Genio S Plus", "verdict": "Veelzijdige cupmachine — espresso, lungo, cappuccino en zelfs thee uit één apparaat.", "priceRange": "EUR 80-120", "bestFor": "Huishoudens met verschillende koffievoorkeuren", "rating": 4.5, "affiliateLink": "https://www.amazon.nl/s?k=Dolce+Gusto+Genio+S+Plus&tag=kieskeukennl-21"},
            {"name": "Melitta AromaFresh II", "verdict": "Filterkoffiemachine met bonenmaler en timer — zet 's ochtends automatisch verse koffie.", "priceRange": "EUR 90-130", "bestFor": "Ochtendmensen die wakker willen worden met verse koffiegeur", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/s?k=Melitta+AromaFresh+II&tag=kieskeukennl-21"},
            {"name": "Nespresso Vertuo Next", "verdict": "Premium cupsysteem met centrifusietechnologie — crema-laag en grote koppen koffie.", "priceRange": "EUR 100-150", "bestFor": "Liefhebbers van café-kwaliteit koffie uit een cup", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/s?k=Nespresso+Vertuo+Next&tag=kieskeukennl-21"},
        ],
        "pros": ["Eerlijke vergelijking met concrete voor- en nadelen per type", "Actuele prijzen en modellen voor 2026", "Helder advies voor elke koffiegewoonte en budget"],
        "cons": ["Prijzen kunnen wijzigen afhankelijk van aanbiedingen", "Niet elk model is getest in dagelijks gebruik", "Koffiesmaak is subjectief — probeer indien mogelijk uit"],
    },
    {
        "slug": "wafelijzer-vs-tosti-ijzer-2026",
        "title": "Wafelijzer vs. Tosti-ijzer 2026: Zoete Wafels of Hartige Tosti's — Welke Past bij Jou?",
        "description": "Vergelijk wafelijzer vs tosti-ijzer in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21).",
        "category": "keuken",
        "priceRange": "EUR 20-150",
        "readingTime": "8 min",
        "rating": 4.3,
        "featuredProduct": "Princess Wafelijzer vs. Tefal Snack Collection",
        "related": ["beste-wafelijzer-2026", "beste-tosti-ijzer-2026", "tosti-ijzer-vs-broodrooster-2026", "beste-broodrooster-2026"],
        "products": [
            {"name": "Princess Bubble Wafelijzer 132010", "verdict": "Populair wafelijzer voor dikke Belgische wafels — instelbare bruiningsgraad.", "priceRange": "EUR 30-45", "bestFor": "Gezinnen die van dikke, luchtige wafels houden", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/s?k=Princess+Bubble+Wafelijzer+132010&tag=kieskeukennl-21"},
            {"name": "Tefal Snack Collection SW854D", "verdict": "Verwisselbare platen — tosti's, wafels, panini's en grillen in één apparaat.", "priceRange": "EUR 60-90", "bestFor": "All-in-one oplossing voor wie beide wil", "rating": 4.5, "affiliateLink": "https://www.amazon.nl/s?k=Tefal+Snack+Collection+SW854D&tag=kieskeukennl-21"},
            {"name": "Princess Tosti-ijzer 3-in-1 112370", "verdict": "Betaalbaar tosti-ijzer met verwisselbare platen voor tosti's, wafels en grillen.", "priceRange": "EUR 25-35", "bestFor": "Budgetbewuste huishoudens die flexibiliteit willen", "rating": 4.2, "affiliateLink": "https://www.amazon.nl/s?k=Princess+Tosti-ijzer+3-in-1+112370&tag=kieskeukennl-21"},
            {"name": "Nostalgia MWF5AQ Wafelijzer", "verdict": "Retro-design wafelijzer — maakt 5 mini-wafels tegelijk, perfect voor kinderen.", "priceRange": "EUR 40-60", "bestFor": "Gezinnen met kinderen die van mini-wafels houden", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/s?k=Nostalgia+MWF5AQ+Wafelijzer&tag=kieskeukennl-21"},
            {"name": "Tefal Optigrill+ XL GC722D", "verdict": "Premium grill met automatische programma's — ook voor tosti's, maar geen wafels.", "priceRange": "EUR 120-180", "bestFor": "Serieuze thuiskoks die grillen belangrijker vinden dan wafels", "rating": 4.6, "affiliateLink": "https://www.amazon.nl/s?k=Tefal+Optigrill%2B+XL+GC722D&tag=kieskeukennl-21"},
            {"name": "Domo DO9047W Wafelijzer", "verdict": "Compact wafelijzer voor hartvormige wafels — schattig en functioneel.", "priceRange": "EUR 20-30", "bestFor": "Kleine keukens en romantische ontbijtjes", "rating": 4.1, "affiliateLink": "https://www.amazon.nl/s?k=Domo+DO9047W+Wafelijzer&tag=kieskeukennl-21"},
        ],
        "pros": ["Eerlijke vergelijking met concrete voor- en nadelen per type", "Actuele prijzen en modellen voor 2026", "Helder advies voor elke snackvoorkeur en budget"],
        "cons": ["Prijzen kunnen wijzigen afhankelijk van aanbiedingen", "Niet elk model is getest in dagelijks gebruik", "Combinatie-apparaten zijn vaak minder goed in beide functies"],
    },
    {
        "slug": "nespresso-vs-espresso-apparaat-2026",
        "title": "Nespresso vs. Espresso Apparaat 2026: Supersnel Gemak of Authentiek Handwerk — Welke Past bij Jou?",
        "description": "Vergelijk Nespresso vs espresso apparaat in 2026. Eerlijke koopgids met prijzen, voor- en nadelen en Amazon NL affiliate links (tag: kieskeukennl-21).",
        "category": "keuken",
        "priceRange": "EUR 80-1500",
        "readingTime": "10 min",
        "rating": 4.5,
        "featuredProduct": "Nespresso Vertuo Next vs. Sage Barista Express",
        "related": ["beste-nespresso-apparaat-2026", "beste-espresso-apparaat-2026", "nespresso-vs-senseo-2026", "nespresso-vs-dolce-gusto-2026"],
        "products": [
            {"name": "Nespresso Vertuo Next", "verdict": "Premium cupsysteem met centrifusietechnologie — crema-laag en 5 kopgroottes.", "priceRange": "EUR 100-150", "bestFor": "Gemakzoekers die café-kwaliteit uit een cup willen", "rating": 4.4, "affiliateLink": "https://www.amazon.nl/s?k=Nespresso+Vertuo+Next&tag=kieskeukennl-21"},
            {"name": "Sage Barista Express Impress", "verdict": "Halfautomaat met ingebouwde maler — authentieke espresso-ervaring met leercurve.", "priceRange": "EUR 500-700", "bestFor": "Koffieliefhebbers die het ambacht willen leren", "rating": 4.7, "affiliateLink": "https://www.amazon.nl/s?k=Sage+Barista+Express+Impress&tag=kieskeukennl-21"},
            {"name": "Nespresso Lattissima One", "verdict": "Nespresso met geïntegreerd melksysteem — één knop voor cappuccino en latte.", "priceRange": "EUR 180-250", "bestFor": "Cappuccino-liefhebbers die geen gedoe willen", "rating": 4.3, "affiliateLink": "https://www.amazon.nl/s?k=Nespresso+Lattissima+One&tag=kieskeukennl-21"},
            {"name": "De'Longhi La Specialista Arte", "verdict": "Stijlvolle pistonmachine — handmatige controle over maalgraad, dosering en temperatuur.", "priceRange": "EUR 350-500", "bestFor": "Espresso-puristen met een beperkt budget", "rating": 4.6, "affiliateLink": "https://www.amazon.nl/s?k=De%27Longhi+La+Specialista+Arte&tag=kieskeukennl-21"},
            {"name": "Nespresso Essenza Mini", "verdict": "Compactste Nespresso — past in elke keuken, maakt uitstekende espresso.", "priceRange": "EUR 80-110", "bestFor": "Kleine keukens en espresso-minimalisten", "rating": 4.2, "affiliateLink": "https://www.amazon.nl/s?k=Nespresso+Essenza+Mini&tag=kieskeukennl-21"},
            {"name": "Gaggia Classic Pro", "verdict": "Klassieke Italiaanse pistonmachine — geliefd door hobbyisten vanwege upgrade-mogelijkheden.", "priceRange": "EUR 400-500", "bestFor": "Hobbyisten die willen sleutelen en upgraden", "rating": 4.5, "affiliateLink": "https://www.amazon.nl/s?k=Gaggia+Classic+Pro&tag=kieskeukennl-21"},
        ],
        "pros": ["Eerlijke vergelijking met concrete voor- en nadelen per type", "Actuele prijzen en modellen voor 2026", "Helder advies voor elke koffievoorkeur en budget"],
        "cons": ["Prijzen kunnen wijzigen afhankelijk van aanbiedingen", "Niet elk model is getest in dagelijks gebruik", "Nespresso-cups zijn duurder per kopje dan zelfgemalen bonen"],
    },
]

def build_frontmatter(comp):
    lines = ['---']
    lines.append(f'title: "{comp["title"]}"')
    lines.append(f'slug: "{comp["slug"].replace("-2026","")}"')
    lines.append(f'description: "{comp["description"]}"')
    lines.append(f'category: "{comp["category"]}"')
    lines.append(f'rating: {comp["rating"]}')
    lines.append(f'priceRange: "{comp["priceRange"]}"')
    lines.append('pros:')
    for p in comp['pros']:
        lines.append(f'  - "{p}"')
    lines.append('cons:')
    for c in comp['cons']:
        lines.append(f'  - "{c}"')
    lines.append('affiliateLinks:')
    for p in comp['products']:
        lines.append(f'  - "{p["affiliateLink"]}"')
    lines.append(f'date: 2026-07-08')
    lines.append(f'modelYear: 2026')
    lines.append(f'featuredProduct: "{comp["featuredProduct"]}"')
    lines.append(f'readingTime: "{comp["readingTime"]}"')
    lines.append('products:')
    for p in comp['products']:
        lines.append(f'  - name: "{p["name"]}"')
        lines.append(f'    verdict: "{p["verdict"]}"')
        lines.append(f'    priceRange: "{p["priceRange"]}"')
        lines.append(f'    bestFor: "{p["bestFor"]}"')
        lines.append(f'    rating: {p["rating"]}')
        lines.append(f'    affiliateLink: "{p["affiliateLink"]}"')
    lines.append('related:')
    for r in comp['related']:
        lines.append(f'  - "{r}"')
    lines.append('draft: false')
    lines.append('---')
    return '\n'.join(lines)

def generate_article(comp):
    prompt = f"""Je bent een Nederlandse consumentenjournalist die schrijft voor Beste Apparaten (KiesKeuken). Schrijf een UITGEBREIDE, informatieve koopgids in het Nederlands die twee keukenapparaten eerlijk vergelijkt. Het artikel moet MINIMAAL 1500 woorden zijn.

TITEL: {comp['title']}

Schrijf een compleet artikel met deze structuur:

## 1. Introductie (3-4 alinea's)
- Pakkende opening die de lezer meteen aanspreekt
- Waarom deze vergelijking relevant is in 2026
- Voor wie is deze gids bedoeld?

## 2. Snel Advies — Wie Kiest Wat? (bullets)
- Duidelijke bullets: "Kies een [A] als u:" en "Kies een [B] als u:"
- Minimaal 5 bullets per apparaat
- Praktisch en concreet, geen vage taal

## 3. Hoe Werkt Het? (2-3 alinea's per apparaat)
- Technische uitleg in begrijpelijke taal
- Wat gebeurt er in het apparaat?
- Wat zijn de belangrijkste technische verschillen?

## 4. Vergelijkingstabel: Topmodellen Anno 2026
- HTML/Markdown tabel met 6 producten (3 per type)
- Kolommen: Product, Type, Belangrijkste Kenmerk, Indicatie Prijs (€), Score (1-10), Beste voor
- Gebruik deze producten:
{json.dumps([{'name': p['name'], 'type': 'Type A' if i < 3 else 'Type B', 'price': p['priceRange'], 'rating': p['rating'], 'bestFor': p['bestFor']} for i, p in enumerate(comp['products'])], indent=2)}

## 5. Diepere Vergelijking (4 subsecties)
- Gerechten: Wat kunt u bereiden? (concreet, met voorbeelden)
- Energieverbruik: Wie is de energievreter? (concrete wattages en kosten)
- Kooktijd: Snelheid vs. geduld (echte tijden, geen vage ranges)
- Schoonmaak: De vloek van elk keukenapparaat (eerlijk over nadelen)

## 6. Specifieke Modellen in de Praktijk (1 alinea per product, 6 totaal)
- Per product: wat maakt het bijzonder, voor wie is het, eerlijke minpunten
- Gebruik de productnamen uit de tabel

## 7. Conclusie: De Keuze is aan U! (3-4 alinea's)
- Samenvatting van de belangrijkste afwegingen
- Geen "het hangt ervan af" — geef richting
- Concrete aanbevelingen per type gebruiker
- Sluit af met een positieve noot

STIJLREGELS:
- Nederlands op moedertaalniveau (geen anglicismen, geen Google Translate-Nederlands)
- Consumentenjournalistiek: kritisch, eerlijk, niet te commercieel
- Gebruik "u" (formeel) consistent
- Prijzen in euro's (€)
- Verwijs naar Amazon NL voor prijzen (niet overdrijven, maximaal 2-3 keer)
- MINIMAAL 1500 woorden, maximaal 2500 woorden
- Gebruik Markdown voor opmaak (## koppen, **vet**, - bullets, | tabellen)
- GEEN placeholder tekst zoals "[Uw Naam]" — gebruik "Beste Apparaten redactie"
- GEEN afsluitende "---" streep

Schrijf ALLEEN het artikel (vanaf "## 1. Introductie" tot en met de conclusie). Geen frontmatter, geen metadata."""

    resp = requests.post(URL, json={
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'temperature': 0.8, 'maxOutputTokens': 8192}
    }, timeout=180)

    if resp.status_code != 200:
        print(f"  API ERROR: {resp.status_code} {resp.text[:200]}")
        return None

    data = resp.json()
    text = data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

    if not text:
        print(f"  EMPTY RESPONSE")
        return None

    return text

def main():
    output_dir = 'src/content/reviews'

    for i, comp in enumerate(TO_REGENERATE):
        slug = comp['slug']
        filepath = os.path.join(output_dir, f'{slug}.md')

        print(f"[{i+1}/3] Regenerating {slug}...")

        body = generate_article(comp)
        if not body:
            print(f"  FAILED")
            continue

        frontmatter = build_frontmatter(comp)
        full_article = frontmatter + '\n\n' + body

        with open(filepath, 'w') as f:
            f.write(full_article)

        word_count = len(body.split())
        print(f"  OK — {word_count} words")

        if i < len(TO_REGENERATE) - 1:
            time.sleep(3)

if __name__ == '__main__':
    main()
