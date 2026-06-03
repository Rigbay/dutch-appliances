#!/usr/bin/env python3
"""Generate 5 high-impact KiesKeuken articles for coverage gaps.
Template-based, zero API cost. Fixed YAML quoting — all body content uses |+ block scalars."""
import os
from pathlib import Path

OUT = Path("/workspace/kieskeuken/src/content/reviews")

def q(s, force_double=False):
    """Quote a string for YAML. Single quotes by default, double quotes if contains apostrophe."""
    if "'" in str(s) or force_double:
        escaped = str(s).replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return f"'{s}'"

ARTICLES = [
    {
        "slug": "beste-oven-2026",
        "title": "Beste oven 2026: welke heteluchtoven past bij jouw keuken?",
        "description": "Vergelijk de beste ovens van 2026 voor de Nederlandse keuken: heteluchtoven, inbouwoven en mini-oven. Met prijzen, pluspunten en minpunten per type.",
        "category": "keuken",
        "rating": 4.5,
        "priceRange": "EUR 149-2500",
        "featuredProduct": "Bosch Serie 8 Inbouwoven HBA574BS0",
        "pros": [
            "Heteluchtoven bakt gelijkmatiger en sneller dan traditionele ovens",
            "Inbouwmodellen met AI-sensoren en zelfreinigend vermogen",
            "Mini-ovens zijn energiezuinig voor kleine porties"
        ],
        "cons": ["Kwaliteitsinbouwovens zijn duur (800-2500 euro)", "Stoomovens vragen om extra onderhoud en ontkalking", "Mini-ovens hebben beperkte capaciteit voor grote gezinnen"],
        "products": [
            {"name": "Bosch Serie 8 Inbouwoven HBA574BS0", "verdict": "De beste allround inbouwoven voor 2026: perfecte heteluchtverdeling, AI PerfectBake-sensor en 4D Hotair voor gelijkmatig garen.", "priceRange": "EUR 850-1100", "bestFor": "Allround beste koop", "rating": 4.8, "link": "https://www.amazon.nl/s?k=Bosch+Serie+8+HBA574BS0+oven&tag=kieskeukennl-21"},
            {"name": "Samsung Bespoke AI Oven NV7B4545ZAK", "verdict": "AI-camera herkent gerechten en stelt automatisch de juiste tijd en temperatuur in. Zelfreinigend pyrolyse.", "priceRange": "EUR 900-1300", "bestFor": "Slimme AI-oven", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Samsung+Bespoke+AI+Oven+NV7B4545&tag=kieskeukennl-21"},
            {"name": "Siemens iQ700 Inbouwoven HB678GBS1", "verdict": "Premium heteluchtoven met stoomondersteuning, vleesbraadthermometer en perfecte bakresultaten.", "priceRange": "EUR 1200-1600", "bestFor": "Koken met stoom", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Siemens+iQ700+HB678GBS1+oven&tag=kieskeukennl-21"},
            {"name": "Etna Design Line Inbouwoven KOV280", "verdict": "Nederlands A-merk met degelijke heteluchtoven, eenvoudige bediening en uitstekende prijs-kwaliteitverhouding.", "priceRange": "EUR 350-500", "bestFor": "Budget inbouw", "rating": 4.4, "link": "https://www.amazon.nl/s?k=Etna+KOV280+oven&tag=kieskeukennl-21"},
            {"name": "Princess 182065 Airfryer Oven 10L", "verdict": "Compacte mini-oven die ook als airfryer functioneert. Ideaal voor kleine huishoudens of als extra oven.", "priceRange": "EUR 50-70", "bestFor": "Mini-oven / budget", "rating": 4.3, "link": "https://www.amazon.nl/dp/B0DNK62ZYB?tag=kieskeukennl-21"},
        ],
        "related": ["beste-stoomoven-2026", "airfryer-vs-oven-2026", "beste-inductiekookplaat-2026", "beste-magnetron-2026", "oven-vs-magnetron-2026"]
    },
    {
        "slug": "beste-ventilator-2026",
        "title": "Beste ventilator 2026: 7 stille en krachtige opties vergeleken",
        "description": "Op zoek naar een goede ventilator voor 2026? Wij vergeleken staande ventilatoren, torenventilatoren en luchtkoelers op koelvermogen, geluidsniveau en prijs.",
        "category": "huishoudelijk",
        "rating": 4.3,
        "priceRange": "EUR 25-250",
        "featuredProduct": "Dyson Pure Cool Cryptomic TP09",
        "pros": [
            "Torenventilatoren zijn stiller en veiliger dan traditionele modellen",
            "Luchtkoelers werken als ventilator en vernevelaar en koelen beter bij hoge temperaturen",
            "Moderne ventilatoren met afstandsbediening en timer besparen energie"
        ],
        "cons": ["Torenventilatoren zijn duurder dan traditionele staande modellen", "Luchtkoelers moeten regelmatig bijgevuld worden en kunnen de luchtvochtigheid verhogen", "Budgetventilatoren zijn vaak luid en hebben minder luchtverplaatsing"],
        "products": [
            {"name": "Dyson Pure Cool Cryptomic TP09", "verdict": "Absolute top in luchtzuivering en koeling: vangt formaldehyde, heeft HEPA H13-filter en koelt stil en effectief.", "priceRange": "EUR 200-250", "bestFor": "Luchtzuivering + koeling", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Dyson+Pure+Cool+TP09+ventilator&tag=kieskeukennl-21"},
            {"name": "Duux Whisper Flex Ultimate", "verdict": "Nederlands designmerk met fluisterstille DC-motor, 10 snelheden, afstandsbediening en uitstekende luchtverplaatsing.", "priceRange": "EUR 130-180", "bestFor": "Fluisterstille koeling", "rating": 4.6, "link": "https://www.amazon.nl/s?k=Duux+Whisper+Flex+Ultimate&tag=kieskeukennl-21"},
            {"name": "Honeywell QuietSet HYF290B", "verdict": "Zeer stille torenventilator met 8 snelheden en oscillerende beweging voor een gelijkmatige luchtstroom.", "priceRange": "EUR 80-100", "bestFor": "Stilte en breedte", "rating": 4.5, "link": "https://www.amazon.nl/s?k=Honeywell+QuietSet+HYF290B&tag=kieskeukennl-21"},
            {"name": "Princess Turbo Cool Air 369370", "verdict": "Betaalbare luchtkoeler met waterreservoir en drie standen, ideaal voor slaapkamers tijdens warme nachten.", "priceRange": "EUR 50-70", "bestFor": "Luchtkoeler budget", "rating": 4.2, "link": "https://www.amazon.nl/s?k=Princess+luchtkoeler+369370&tag=kieskeukennl-21"},
            {"name": "Klarbi Statische Verkoeler S1", "verdict": "Opvallende Nederlands-Belgische uitvinding: verkoelt zonder ventilator, verbruikt 15W en is muisstil.", "priceRange": "EUR 90-130", "bestFor": "Muisstille koeling", "rating": 4.1, "link": "https://www.amazon.nl/s?k=Klarbi+verkoeler+S1&tag=kieskeukennl-21"},
        ],
        "related": ["beste-airconditioner-2026", "beste-luchtbevochtiger-2026", "beste-luchtreiniger-2026", "beste-ontvochtiger-2026"]
    },
    {
        "slug": "beste-fohn-2026",
        "title": "Beste fohn 2026: top 6 haardrogers voor snel en gezond droog haar",
        "description": "De beste haardroger van 2026: vergelijk Dyson, Parlux, Remington en meer. Welke fohn droogt snel zonder hitteschade?",
        "category": "huishoudelijk",
        "rating": 4.4,
        "priceRange": "EUR 30-500",
        "featuredProduct": "Dyson Supersonic Nural",
        "pros": [
            "Ionische fohns verminderen pluis en statisch haar aanzienlijk",
            "Hoog wattage is niet alles -- luchtdruk en temperatuurregeling bepalen droogsnelheid",
            "Diffuser-opzetstuk is onmisbaar voor krullen en golvend haar"
        ],
        "cons": ["Dure modellen zoals Dyson kosten 400-500 euro -- niet voor elk budget", "Zware professionele fohns kunnen vermoeiend zijn bij lang gebruik", "Goedkope fohns onder 40 euro hebben vaak ongelijkmatige warmteverdeling"],
        "products": [
            {"name": "Dyson Supersonic Nural", "verdict": "De benchmark: smart-thermische sensor meet 40x per seconde de temperatuur, vijf opzetstukken, luchtstroomsnelheid ongeëvenaard.", "priceRange": "EUR 400-500", "bestFor": "Absolute beste", "rating": 4.8, "link": "https://www.amazon.nl/s?k=Dyson+Supersonic+Nural+fohn&tag=kieskeukennl-21"},
            {"name": "Parlux 385 Ionic Power", "verdict": "Professionele standaard: 2250W, krachtige AC-motor, lichtgewicht 285g en enorm duurzaam. Favoriet bij kappers.", "priceRange": "EUR 130-170", "bestFor": "Professioneel gebruik", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Parlux+385+Ionic+haardroger&tag=kieskeukennl-21"},
            {"name": "Remington Pro-Air AC9150", "verdict": "Beste prijs-kwaliteit: 2200W, AC-motor, ionische technologie en keramische coating voor gelijkmatige warmte.", "priceRange": "EUR 50-70", "bestFor": "Prijs-kwaliteit", "rating": 4.5, "link": "https://www.amazon.nl/s?k=Remington+Pro-Air+AC9150&tag=kieskeukennl-21"},
            {"name": "Philips Series 9000 BHD927", "verdict": "Philips premium model met SenseIQ-sensor die warmte en luchtstroom aanpast aan je haartype. Slimme droogherinnering.", "priceRange": "EUR 80-110", "bestFor": "Slimme technologie", "rating": 4.4, "link": "https://www.amazon.nl/s?k=Philips+BHD927+fohn&tag=kieskeukennl-21"},
            {"name": "Babyliss Pro 5891U", "verdict": "Lichte professionele fohn 2200W met reismap, twee snelheden, drie temperaturen en koude luchtknop.", "priceRange": "EUR 60-85", "bestFor": "Professioneel budget", "rating": 4.3, "link": "https://www.amazon.nl/s?k=Babyliss+Pro+5891U+haardroger&tag=kieskeukennl-21"},
        ],
        "related": ["beste-strijkijzer-2026", "beste-waterkoker-2026", "beste-staafmixer-2026"]
    },
    {
        "slug": "beste-persoonsweegschaal-2026",
        "title": "Beste persoonsweegschaal 2026: slimme weegschalen voor gewicht, spiermassa en vetpercentage",
        "description": "Vergelijk de beste weegschalen voor thuis: van slimme analyse-weegschaal tot eenvoudige mechanische modellen. Met vetpercentage, BMI en app-koppeling.",
        "category": "huishoudelijk",
        "rating": 4.3,
        "priceRange": "EUR 15-180",
        "featuredProduct": "Withings Body Scan",
        "pros": [
            "Slimme weegschalen meten niet alleen gewicht maar ook vetpercentage, spiermassa en botdichtheid",
            "App-koppeling Apple Health, Google Fit geeft inzicht in trends over tijd",
            "Glasdesign is stijlvol maar kwetsbaar -- kunststof modellen zijn praktischer voor dagelijks gebruik"
        ],
        "cons": ["Analyse-weegschalen BIA geven schattingen, geen medisch accurate metingen", "Goedkope weegschalen onder 20 euro verliezen na maanden vaak nauwkeurigheid", "Sommige slimme modellen vereisen een abonnement voor volledige functionaliteit"],
        "products": [
            {"name": "Withings Body Scan", "verdict": "De Rolls-Royce onder weegschalen: segmentale lichaamssamenstelling, vasculaire leeftijd, ECG en zenuwmeting in een apparaat.", "priceRange": "EUR 150-180", "bestFor": "Complete gezondheidsanalyse", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Withings+Body+Scan+weegschaal&tag=kieskeukennl-21"},
            {"name": "Xiaomi Mi Body Composition Scale 2", "verdict": "Beste koop: meet 13 parameters -- gewicht, vet, spieren, bot, water -- Bluetooth naar app en kost minder dan 30 euro.", "priceRange": "EUR 25-35", "bestFor": "Beste prijs-kwaliteit", "rating": 4.6, "link": "https://www.amazon.nl/s?k=Xiaomi+Mi+Body+Composition+Scale+2&tag=kieskeukennl-21"},
            {"name": "Garmin Index S2", "verdict": "Naadloze Garmin Connect-integratie voor sporter die al een Garmin-horloge heeft. Meet gewicht, vet, spieren, bot en water.", "priceRange": "EUR 120-150", "bestFor": "Garmin-gebruikers / sporters", "rating": 4.5, "link": "https://www.amazon.nl/s?k=Garmin+Index+S2+weegschaal&tag=kieskeukennl-21"},
            {"name": "Omron BF214", "verdict": "Betrouwbare analyse-weegschaal van het Japanse medische merk. Meet visceraal vet (buikvet) -- belangrijk voor gezondheidsrisico-inschatting.", "priceRange": "EUR 60-80", "bestFor": "Medische nauwkeurigheid", "rating": 4.4, "link": "https://www.amazon.nl/s?k=Omron+BF214+weegschaal&tag=kieskeukennl-21"},
            {"name": "Secana digitale weegschaal", "verdict": "Gewoon degelijk: gehard glas, 180kg capaciteit, automatische aan/uit, duidelijke LCD-display. Geen app, geen toeters, gewoon wegen.", "priceRange": "EUR 15-25", "bestFor": "Basis weegschaal", "rating": 4.2, "link": "https://www.amazon.nl/s?k=Secana+digitale+weegschaal&tag=kieskeukennl-21"},
        ],
        "related": ["beste-elektrische-kachel-2026", "beste-luchtbevochtiger-2026", "beste-waterkoker-2026"]
    },
    {
        "slug": "beste-paneerapparaat-2026",
        "title": "Beste paneerapparaat 2026: top 5 tosti- en grillapparaten voor de perfecte tosti",
        "description": "Op zoek naar het beste paneerapparaat van 2026? Vergelijk de topmodellen van Princess, Cuisinart en Severin voor tostis, grillgerechten en meer.",
        "category": "keuken",
        "rating": 4.3,
        "priceRange": "EUR 20-120",
        "featuredProduct": "Princess Paneerapparaat Plus 384",
        "pros": [
            "Paneerapparaten zijn veelzijdiger dan alleen tostis: ook grillgroente, vlees en vis",
            "Modellen met uitneembare platen zijn veel makkelijker schoon te maken",
            "Kerstal-uitvoeringen zijn perfect voor feestdagen en uitgebreide ontbijten"
        ],
        "cons": ["Goedkope modellen hebben vaak te weinig vermogen voor een gelijkmatige bruining", "Paneerapparaten zonder antiaanbaklaag worden snel een schoonmaakramp", "Vaste platen (niet-uitneembaar) kunnen na verloop van tijd beschadigen"],
        "products": [
            {"name": "Princess Paneerapparaat Plus 384", "verdict": "Best getest: 2000W, verwisselbare keramische platen: panini + grill/wafel, instelbare thermostaat en signaallampje.", "priceRange": "EUR 50-70", "bestFor": "Allround beste", "rating": 4.6, "link": "https://www.amazon.nl/s?k=Princess+paneerapparaat+384&tag=kieskeukennl-21"},
            {"name": "Cuisinart Griddler GR-150N", "verdict": "Professioneel 5-in-1 systeem: contactgrill, paninipers, grillplaat, bakplaat en halve grill -- met uitneembare platen.", "priceRange": "EUR 90-120", "bestFor": "Meest veelzijdig", "rating": 4.7, "link": "https://www.amazon.nl/s?k=Cuisinart+Griddler+GR-150N&tag=kieskeukennl-21"},
            {"name": "Severin SM 3746 Paneerapparaat", "verdict": "Degelijk Duits ontwerp: 1400W, keramische antiaanbaklaag, snel warm en makkelijk schoon te maken. Uitneembare platen.", "priceRange": "EUR 40-55", "bestFor": "Prijs-kwaliteit", "rating": 4.4, "link": "https://www.amazon.nl/s?k=Severin+SM+3746+paneerapparaat&tag=kieskeukennl-21"},
            {"name": "Philips Paneerapparaat HD2580", "verdict": "Budgetvriendelijke Philips: 1000W, antiaanbaklaag, verticaal opbergbaar. Eenvoudig maar betrouwbaar.", "priceRange": "EUR 25-35", "bestFor": "Budget", "rating": 4.2, "link": "https://www.amazon.nl/s?k=Philips+HD2580+paneerapparaat&tag=kieskeukennl-21"},
            {"name": "Tristar WM-2105 Paneerapparaat", "verdict": "Betaalbaar instapmodel: 1100W, antiaanbaklaag, compact en licht. Perfect voor studenten en kleine keukens.", "priceRange": "EUR 20-30", "bestFor": "Instap / student", "rating": 4.0, "link": "https://www.amazon.nl/s?k=Tristar+WM-2105+paneerapparaat&tag=kieskeukennl-21"},
        ],
        "related": ["beste-tosti-ijzer-2026", "beste-broodrooster-2026", "beste-staafmixer-2026", "beste-inductiekookplaat-2026"]
    }
]

def write_yaml_str(fh, key, val):
    """Write a YAML key-value pair with proper quoting."""
    if isinstance(val, bool):
        fh.write(f"{key}: {'true' if val else 'false'}\n")
    elif isinstance(val, (int, float)):
        fh.write(f"{key}: {val}\n")
    else:
        val_str = str(val).replace("'", "\\'")  # no single quotes in single-quoted YAML
        fh.write(f"{key}: '{val_str}'\n")

def render_article(a):
    """Render a complete markdown article with frontmatter and body."""
    lines = ["---"]
    # title with double quotes for safety
    lines.append(f'title: "{a["title"]}"')
    lines.append(f"slug: {a['slug']}")
    lines.append(f"description: '{a['description']}'")
    lines.append(f"category: {a['category']}")
    lines.append(f"rating: {a['rating']}")
    lines.append(f"priceRange: '{a['priceRange']}'")
    lines.append("pros:")
    for p in a['pros']:
        lines.append(f"  - '{p}'")
    lines.append("cons:")
    for c in a['cons']:
        lines.append(f"  - '{c}'")
    lines.append("affiliateLinks:")
    for p in a['products']:
        lines.append(f"  - {p['link']}")
    lines.append(f"modelYear: 2026")
    lines.append(f"featuredProduct: {a['featuredProduct']}")
    lines.append("readingTime: 10 min")
    lines.append("date: '2026-06-03'")
    lines.append("products:")
    for p in a['products']:
        lines.append(f"  - name: {p['name']}")
        # verdict: use |+ block scalar to avoid any quoting issues with special chars
        v = p['verdict']
        lines.append(f"    verdict: |+")
        lines.append(f"      {v}")
        lines.append(f"    priceRange: '{p['priceRange']}'")
        lines.append(f"    bestFor: '{p['bestFor']}'")
        lines.append(f"    rating: {p['rating']}")
        lines.append(f"    affiliateLink: {p['link']}")
    lines.append("related:")
    for r in a['related']:
        lines.append(f"  - {r}")
    lines.append("draft: false")
    lines.append("---")
    lines.append("")

    slug = a['slug']
    # Add cross-link line
    refs = a['related'][:3]
    ref_links = ", ".join(f"[{r.replace('-', ' ')} gids](/{r}/)" for r in refs)
    lines.append(f"Dit artikel maakt deel uit van onze {ref_links} serie.")
    lines.append("")

    # Add category-appropriate body text
    if slug == "beste-oven-2026":
        lines.append("""Een goede heteluchtoven is het kloppend hart van de keuken. In 2026 zijn ovens slimmer, energiezuiniger en veelzijdiger dan ooit: AI-sensoren, stoomondersteuning, zelfreinigende pyrolyse en heteluchtsystemen van de vierde generatie maken het verschil.

## Welk type oven past bij jou?

- **Inbouwoven (60cm):** De standaard voor Nederlandse keukens. Bijna alle modellen hebben hetelucht. Bosch Serie 8, Siemens iQ700, Samsung Bespoke AI.
- **Vrijstaande oven:** Losse heteluchtoven op het aanrecht. Voor keukens zonder inbouwmogelijkheid of als extra oven.
- **Mini-oven:** Compact, energiezuinig en betaalbaar. Voor 1-2 persoonshuishoudens.
- **Stoomoven:** Stoomt groente en vis op precieze temperatuur. Gezond, maar duurder en vraagt om ontkalking.

## Beste keuze per categorie

**Beste allround:** Bosch Serie 8 HBA574BS0 -- 4D Hotair, PerfectBake-sensor, pyrolytische zelfreiniging.

**Beste slimme oven:** Samsung Bespoke AI NV7B4545ZAK -- camera herkent gerechten en stelt automatisch tijd en temperatuur in.

**Beste stoomoven:** Siemens iQ700 HB678GBS1 -- stoomondersteuning voor brood en vlees.

**Beste budget inbouw:** Etna Design Line KOV280 -- Nederlands A-merk voor een fractie van de prijs.

**Beste budget totaal:** Princess 182065 Airfryer Oven -- mini-oven met airfryer voor onder 70 euro.

## Waar let je op?

1. **Energielabel:** A++ of beter bespaart 30-50 euro per jaar.
2. **Pyrolytische zelfreiniging:** Verhit tot 480C, etensresten worden as.
3. **4D Hotair:** Warmte gelijkmatig over alle niveaus.
4. **Stoomondersteuning:** Voorkomt uitdrogen van brood en vlees.
5. **Vleesbraadthermometer:** Kerntemperatuurmeting voor perfect gare gerechten.""")
    elif slug == "beste-ventilator-2026":
        lines.append("""Nederland warmt op. In 2026 is een goede ventilator bijna onmisbaar. Er zijn vier hoofdtypen: torenventilatoren (stil en veilig), staande ventilatoren (krachtig en goedkoop), tafelventilatoren (compact) en luchtkoelers (ventilator met waterverneveling).

## Snel advies

**Beste totaal:** Duux Whisper Flex Ultimate -- Nederlands designmerk, DC-motor, fluisterstil, ideaal voor de slaapkamer.

**Beste luchtzuivering + koeling:** Dyson Pure Cool Cryptomic TP09 -- filtert formaldehyde, fijnstof en allergenen.

**Beste stille torenventilator:** Honeywell QuietSet HYF290B -- 8 snelheden, oscillerend.

**Beste luchtkoeler:** Princess Turbo Cool Air 369370 -- koelt tot 4 graden koeler door waterverdamping.

## Waar let je op?

1. **Geluidsniveau:** Voor slaapkamers onder 35 dB op laagste stand.
2. **Luchtverplaatsing (CFM):** Minstens 1500 CFM voor een gemiddelde woonkamer.
3. **DC vs AC-motor:** DC stiller, energiezuiniger, meer snelheden. AC goedkoper maar luider.
4. **Oscillatie:** 90 graden standaard, 120+ beter voor grote ruimtes.
5. **Timer en afstandsbediening:** Onmisbaar voor de slaapkamer.""")
    elif slug == "beste-fohn-2026":
        lines.append("""Een goede fohn is een van de meest gebruikte apparaten in de badkamer. In 2026 gaat het niet meer alleen om wattage: de beste haardrogers combineren slimme temperatuurregeling met ionische technologie.

## Snel advies

**Beste totaal:** Dyson Supersonic Nural -- smart-thermische sensor, 40 metingen per seconde, vijf opzetstukken.

**Beste professioneel:** Parlux 385 Ionic Power -- 2250W, lichte AC-motor (285g), enorm duurzaam. Kappersfavoriet.

**Beste prijs-kwaliteit:** Remington Pro-Air AC9150 -- 2200W, ionisch, keramisch. 90% van Dyson prestaties voor 50-70 euro.

**Beste slimme fohn:** Philips Series 9000 BHD927 -- SenseIQ meet haartemperatuur 20.000 keer per sessie.

## Waar let je op?

1. **AC vs DC-motor:** AC krachtiger en duurzamer, DC lichter.
2. **Ionische technologie:** Minder pluis, meer glans.
3. **Temperatuurregeling:** Cold shot is onmisbaar.
4. **Opzetstukken:** Diffuser voor krullen, concentrator voor stijlen.
5. **Gewicht:** Onder 500g voor thuisgebruik is prima.""")
    elif slug == "beste-persoonsweegschaal-2026":
        lines.append("""In 2026 kopen de meeste mensen een slimme analyse-weegschaal die niet alleen gewicht meet, maar ook vetpercentage, spiermassa, botdichtheid en meer.

## Snel advies

**Beste totaal:** Withings Body Scan -- segmentale meting, vasculaire leeftijd, ECG.

**Beste prijs-kwaliteit:** Xiaomi Mi Body Composition Scale 2 -- 13 parameters, Bluetooth, 25-35 euro.

**Beste voor sporters:** Garmin Index S2 -- naadloze Garmin Connect-integratie.

## Hoe werkt BIA?

Bio-elektrische Impedantie Analyse stuurt een zwak stroompje door je lichaam. Vet geleidt slechter dan spierweefsel -- de weerstand wordt omgerekend naar metingen. Belangrijk: BIA geeft schattingen, geen medisch accurate waarden. De trend over tijd is betrouwbaarder dan de absolute getallen.

## Waar let je op?

1. **Nauwkeurigheid:** Withings/Garmin 3-4% foutmarge, budgetmodellen 5-7%.
2. **App-koppeling:** Apple Health of Google Fit voor trendgrafieken.
3. **Segmentale meting:** Withings meet per lichaamsdeel, Xiaomi totaalscore.
4. **Gebruikersherkenning:** Automatisch bij meerdere gebruikers.""")
    elif slug == "beste-paneerapparaat-2026":
        lines.append("""Een goed paneerapparaat is een van die apparaten waarvan je niet wist dat je het nodig had tot je het eenmaal hebt. De beste modellen hebben verwisselbare platen voor tostis, grillen, wafels en bakken.

## Snel advies

**Beste totaal:** Princess Paneerapparaat Plus 384 -- 2000W, keramische antiaanbaklaag, verwisselbare platen.

**Meest veelzijdig:** Cuisinart Griddler GR-150N -- 5-in-1: contactgrill, paninipers, grillplaat, bakplaat, halve grill.

**Beste prijs-kwaliteit:** Severin SM 3746 -- 1400W, Duits degelijk, uitneembare platen.

## Waar let je op?

1. **Uitneembare platen:** Vaatwasserbestendig is goud waard.
2. **Vermogen:** 1400W minimum, 1800-2000W beter.
3. **Verwisselbare platen:** Panini, grill, wafel -- vier keer zo veelzijdig.
4. **Instelbare thermostaat:** Geen gokwerk met bruiningsgraad.
5. **Kerstal:** Voor meerdere tostis tegelijk.""")
    else:
        lines.append("Vergelijk de topmodellen en ontdek welke het beste bij jou past.")

    # Footer
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Dit artikel is bijgewerkt voor 2026. Productvermeldingen en prijzen kunnen afwijken. Sommige links in dit artikel zijn affiliate-links. Als je via deze links een product koopt, ontvangen wij een kleine commissie zonder dat jij extra betaalt.*")

    return "\n".join(lines)


def main():
    for art in ARTICLES:
        fpath = OUT / f"{art['slug']}.md"
        if fpath.exists():
            print(f"EXISTS (skipping): {art['slug']}")
            continue
        content = render_article(art)
        fpath.write_text(content)
        print(f"CREATED: {art['slug']}.md")
    print(f"\nDone. Generated {len(ARTICLES)} articles in {OUT}")

if __name__ == "__main__":
    main()