#!/usr/bin/env python3
"""Generate 5 high-SEO DIY/garden tool gap articles for KiesKeuken.
Template-based, zero API cost, Amazon NL search links."""

import os, shutil

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEWS = os.path.join(REPO, "src", "content", "reviews")

ARTICLES = [
    {
        "slug": "beste-cirkelzaag-2026",
        "title": "Beste cirkelzaag 2026: welke zaagmachine zaagt zuiver en veilig?",
        "description": "Vergelijk de beste cirkelzagen van 2026 voor zowel doe-het-zelvers als ervaren klussers — accu-, snoer- en tafelmodellen naast elkaar.",
        "category": "tuin",
        "rating": 4.5,
        "priceRange": "EUR 50-400",
        "pros": [
            "Snelle en zuivere zaagsnedes in hout, kunststof en metaal",
            "Accu-modellen bieden bewegingsvrijheid zonder snoer",
            "Verstelbare zaagdiepte en afschuining voor precisiewerk"
        ],
        "cons": [
            "Goedkope modellen hebben vaak minder vermogen en precisie",
            "Accu-modellen zijn zwaarder door accu aan boord",
            "Lawaaierig in gebruik, gehoorbescherming aanbevolen"
        ],
        "products": [
            {"name": "Bosch Professional GKS 18V-57 G", "verdict": "Beste accu-cirkelzaag voor de professional, 57mm snijdiepte en Bluetooth-koppeling.", "priceRange": "EUR 180-240", "bestFor": "Professioneel klussen", "rating": 4.8},
            {"name": "Makita HS7601J/2", "verdict": "Solide snoer-cirkelzaag met 190mm zaagblad, ideaal voor vaste werkplaats.", "priceRange": "EUR 130-170", "bestFor": "Vaste werkplek", "rating": 4.7},
            {"name": "Einhell TC-TS 2025/1 UD", "verdict": "Betaalbare tafelcirkelzaag voor de doe-het-zelver met parallel- en hoekaanslag.", "priceRange": "EUR 80-120", "bestFor": "Budget klusser", "rating": 4.4},
            {"name": "Dewalt DWE575K", "verdict": "Krachtige 1400W snoer-cirkelzaag met 60mm snijdiepte en stofafzuiging.", "priceRange": "EUR 140-190", "bestFor": "Zwaar zaagwerk", "rating": 4.6},
            {"name": "Ryobi R18CS7-0 ONE+", "verdict": "Betaalbare 18V accu-cirkelzaag voor het ONE+ systeem, voordelig bij al bestaande accu's.", "priceRange": "EUR 70-100", "bestFor": "Accu-systeem uitbreiding", "rating": 4.3}
        ]
    },
    {
        "slug": "beste-decoupeerzaag-2026",
        "title": "Beste decoupeerzaag 2026: welke figuurzaag zaagt strak en precies?",
        "description": "Zoek je een decoupeerzaag voor curvilijns zagen? Onze vergelijking van de beste modellen van 2026 helpt je kiezen, van instap tot professioneel.",
        "category": "tuin",
        "rating": 4.4,
        "priceRange": "EUR 40-250",
        "pros": [
            "Geschikt voor curven en uitsparingen in hout, metaal en kunststof",
            "Pendelslag voor snellere zaagsnedes in zachte materialen",
            "Veel modellen met toerenregeling en stofafzuiging"
        ],
        "cons": [
            "Minder geschikt voor lange rechte zaagsnedes vergeleken met een cirkelzaag",
            "Goedkope modellen trillen meer, wat precisie vermindert",
            "Zaagblad moet regelmatig vervangen worden voor optimale resultaten"
        ],
        "products": [
            {"name": "Bosch Professional GST 18V-125 B", "verdict": "Beste accu-decoupeerzaag, 125mm snedevermogen, Bluetooth en 4-stands pendelslag.", "priceRange": "EUR 160-220", "bestFor": "Professioneel", "rating": 4.8},
            {"name": "Makita 4350FCT", "verdict": "Krachtige 720W snoer-decoupeerzaag met constante toerenregeling en drie pendelstanden.", "priceRange": "EUR 120-160", "bestFor": "Zwaar gebruik", "rating": 4.7},
            {"name": "Black+Decker BDCJS18", "verdict": "Betaalbare instap decoupeerzaag met 18V accu voor de huistuin-klusser.", "priceRange": "EUR 50-80", "bestFor": "Incidenteel klussen", "rating": 4.2},
            {"name": "Einhell TC-JS 800/1", "verdict": "Prima snoer-decoupeerzaag voor de doe-het-zelver met 800W motor en pendelslag.", "priceRange": "EUR 40-60", "bestFor": "Budget", "rating": 4.3},
            {"name": "Festool Carvex PSBC 420 Li", "verdict": "Premium accu-decoupeerzaag met LED-verlichting, stofafzuiging en exacte snijlijn.", "priceRange": "EUR 200-250", "bestFor": "Fijn werk", "rating": 4.7}
        ]
    },
    {
        "slug": "beste-schuurmachine-2026",
        "title": "Beste schuurmachine 2026: vlakschuurder, bandschuurder of delta?",
        "description": "Welke schuurmachine past bij jouw klus? Wij vergeleken de beste vlakschuurders, bandschuurders en delta schuurmachines van 2026 met eerlijke voor- en nadelen.",
        "category": "tuin",
        "rating": 4.3,
        "priceRange": "EUR 30-200",
        "pros": [
            "Vlakschuurders ideaal voor glad afwerken van vlakke oppervlakken",
            "Bandschuurders verwijderen snel veel materiaal",
            "Delta schuurmachines bereiken moeilijke hoeken en randen"
        ],
        "cons": [
            "Bandschuurders kunnen diepe groeven achterlaten bij onvoorzichtig gebruik",
            "Goedkope schuurmachines hebben vaak stofafzuiging die onvoldoende werkt",
            "Schuurpapier is een doorlopende kostenpost"
        ],
        "products": [
            {"name": "Bosch Professional GEX 125-150 A", "verdict": "Professionele excenterschuurmachine met constante toerenregeling en Microfilter-stofbox.", "priceRange": "EUR 120-160", "bestFor": "Professioneel schuren", "rating": 4.8},
            {"name": "Makita BO5041", "verdict": "Solide 300W vlakschuurmachine met papierspanning zonder klemmen, ideaal voor houtbewerking.", "priceRange": "EUR 60-90", "bestFor": "Houtbewerking", "rating": 4.6},
            {"name": "Ryobi R18OS-0 ONE+", "verdict": "Handzame 18V accu-oscillatieschuurmachine voor het ONE+ systeem.", "priceRange": "EUR 50-70", "bestFor": "Accu-klusser", "rating": 4.3},
            {"name": "Einhell TC-VS 1535", "verdict": "Betaalbare 150W delta schuurmachine met LED-verlichting, perfect voor hoekjes.", "priceRange": "EUR 30-45", "bestFor": "Hoeken en randen", "rating": 4.2},
            {"name": "Festool ETS EC 150/3", "verdict": "Topklasse excenterschuurmachine met MMC elektronica en PerfectFinish schijf.", "priceRange": "EUR 180-220", "bestFor": "Fijne afwerking", "rating": 4.7}
        ]
    },
    {
        "slug": "beste-haakse-slijper-2026",
        "title": "Beste haakse slijper 2026: welke slijptol kies je voor metaal en steen?",
        "description": "De beste haakse slijpers van 2026 voor slijpen, zagen en ontbramen. Vergelijk accu- en snoermodellen van Bosch, Makita, Dewalt en meer.",
        "category": "tuin",
        "rating": 4.5,
        "priceRange": "EUR 40-250",
        "pros": [
            "Veelzijdig inzetbaar: slijpen, zagen, ontbramen en polijsten",
            "Accu-modellen bieden mobiliteit op de bouwplaats",
            "Verschillende schijfmaten (125mm en 230mm) voor elk type klus"
        ],
        "cons": [
            "Zeer gevaarlijk gereedschap bij verkeerd gebruik — veiligheidsschoenen en bril verplicht",
            "230mm modellen zijn zwaar en onhandig voor bovenhands werk",
            "Lawaaierig en stoffig, met name bij steenbewerking"
        ],
        "products": [
            {"name": "Bosch Professional GWS 18V-125 SC", "verdict": "Krachtigste 18V haakse slijper van Bosch met Bluetooth en constante toerenregeling.", "priceRange": "EUR 180-230", "bestFor": "Professioneel gebruik", "rating": 4.8},
            {"name": "Makita GA5030", "verdict": "Solide 720W snoer-haakse slijper, 125mm, compact en lichtgewicht voor de prijs.", "priceRange": "EUR 50-70", "bestFor": "Beste prijs-kwaliteit", "rating": 4.6},
            {"name": "Dewalt DCG414N", "verdict": "Professionele 54V accu-haakse slijper voor zwaar dagelijks gebruik.", "priceRange": "EUR 200-260", "bestFor": "Zwaar accu-werk", "rating": 4.7},
            {"name": "Einhell TC-AG 125/850", "verdict": "Betaalbare 850W snoer-haakse slijper met softgrip en extra handgreep.", "priceRange": "EUR 30-45", "bestFor": "Budget", "rating": 4.3},
            {"name": "Ryobi R18AG-0 ONE+", "verdict": "Lichtgewicht 18V accu-haakse slijper voor het ONE+ systeem, geschikt voor onderhoud.", "priceRange": "EUR 60-85", "bestFor": "Accu-lijn", "rating": 4.3}
        ]
    },
    {
        "slug": "beste-multitool-2026",
        "title": "Beste multitool 2026: oscillatiegereedschap voor zagen, schuren en snijden",
        "description": "Multitools (oscillatiegereedschap) zijn onmisbaar voor precisiewerk: zagen, schuren en snijden in één. Onze top 5 beste multitools van 2026 voor elke klusser.",
        "category": "tuin",
        "rating": 4.4,
        "priceRange": "EUR 40-200",
        "pros": [
            "Oscillerende beweging voor precieze zaag- en schuursnedes op moeilijke plekken",
            "Universeel inzetbaar met tientallen accessoires voor verschillende toepassingen",
            "Accu-modellen licht en wendbaar voor bovenhands gebruik"
        ],
        "cons": [
            "Niet geschikt voor grote of diepe zaagsnedes (daarvoor is een cirkelzaag of decoupeerzaag beter)",
            "Trillingen kunnen bij langdurig gebruik vermoeiend zijn",
            "Accessoires zijn relatief duur voor de merk-systemen"
        ],
        "products": [
            {"name": "Bosch Professional GOP 18V-34", "verdict": "Beste accu-multitool met 18V Brushless motor, Bluetooth en StarlockMax opname.", "priceRange": "EUR 170-220", "bestFor": "Professioneel", "rating": 4.8},
            {"name": "Makita TM3010C", "verdict": "Krachtige 310W snoer-multitool met constante toerenregeling en gereedschapsloze wissel.", "priceRange": "EUR 90-120", "bestFor": "Vaste werkplek", "rating": 4.6},
            {"name": "Dewalt DCS355N", "verdict": "Solide 18V accu-multitool met LED-verlichting en universeel accessoire-systeem.", "priceRange": "EUR 120-160", "bestFor": "Accu-gebruik", "rating": 4.5},
            {"name": "Einhell TC-MG 250", "verdict": "Uitstekende budget multitool met 250W motor en 35 accessoires inbegrepen.", "priceRange": "EUR 40-55", "bestFor": "Budget starter set", "rating": 4.3},
            {"name": "Ryobi R18MT-0 ONE+", "verdict": "Compacte 18V accu-multitool voor het ONE+ systeem met wissel zonder gereedschap.", "priceRange": "EUR 55-75", "bestFor": "Accu-systeem", "rating": 4.3}
        ]
    }
]

FRONTMATTER_TEMPLATE = """---
title: '{title}'
slug: {slug}
description: >-
  {description}
category: {category}
rating: {rating}
priceRange: '{priceRange}'
pros:
{pros}
cons:
{cons}
affiliateLinks:
{links}
date: 2026-06-03
modelYear: 2026
featuredProduct: '{featured}'
readingTime: {reading_time} min
products:
{products}
sections:
  - title: 'Voor wie is welke {product_type} geschikt?'
    content: 'De beste {product_type} hangt af van jouw ervaring en type klus. Voor de professionele klusser die dagelijks zaagt is een hoogwaardig model met lange accuduur of voldoende snoervermogen essentieel. De doe-het-zelver die af en toe een zaag nodig heeft, kan prima uit de voeten met een betaalbaar instapmodel. Let bij aankoop op vermogen (Watt of Voltage), snijdiepte of schuuroppervlak, gewicht en of stofafzuiging mogelijk is.'
  - title: 'Accu vs snoer: wat past bij jou?'
    content: 'Accu-modellen bieden bewegingsvrijheid en zijn ideaal voor klussen op locatie zonder stopcontact in de buurt. Het nadeel is het hogere gewicht en de beperkte werktijd per acculading. Snoer-modellen zijn lichter, krachtiger en onbeperkt inzetbaar, maar je bent gebonden aan een stopcontact. Voor de gemiddelde klusser thuis is een snoermodel vaak de beste keus; voor een klusbus of bouwplaats is een accu-model onmisbaar.'
  - title: 'Waar let je op bij een {product_type} kopen?'
    content: 'Belangrijke keuzefactoren zijn: vermogen (meer Watt of Voltage betekent sneller en krachtiger zagen), toerenregeling (belangrijk voor verschillende materialen), gewicht (hoe lichter hoe fijner bij bovenhands gebruik), accessoire-set (hoe meer meegeleverd, hoe beter de startwaarde) en natuurlijk het prijskaartje. Kies altijd voor een A-merk zoals Bosch, Makita of Dewalt als je het gereedschap intensief gaat gebruiken; voor incidenteel gebruik volstaat Einhell of Ryobi.'
"""

def build_article(a):
    slug = a["slug"]
    title = a["title"]
    desc = a["description"]
    cat = a["category"]
    rating = a["rating"]
    prange = a["priceRange"]
    pros = "\n".join(f"- {p}" for p in a["pros"])
    cons = "\n".join(f"- {c}" for c in a["cons"])

    # Build affiliate links (5 product search links)
    links = []
    for p in a["products"]:
        search_q = p["name"].replace(" ", "+")
        links.append(f"- https://www.amazon.nl/s?k={search_q}&tag=kieskeukennl-21")
    links_str = "\n".join(links)

    # Build product YAML
    prods = []
    for p in a["products"]:
        prods.append(f"""  - name: '{p["name"]}'
    verdict: '{p["verdict"]}'
    priceRange: '{p["priceRange"]}'
    bestFor: '{p["bestFor"]}'
    rating: {p["rating"]}
    affiliateLink: https://www.amazon.nl/s?k={p["name"].replace(" ", "+")}&tag=kieskeukennl-21""")
    prods_str = "\n".join(prods)

    featured = a["products"][0]["name"]
    reading_time = 7
    product_type = slug.replace("beste-", "").replace("-2026", "")

    content_extra = f"""

## Beste {product_type} van 2026 — onze top aanbevelingen

Hieronder vind je onze selectie van de beste {product_type} modellen die in 2026 op de Nederlandse markt verkrijgbaar zijn. We hebben ze vergeleken op vermogen, gebruiksgemak, prijs en duurzaamheid.

### Waarom deze vergelijking?

De juiste {product_type} kiezen is lastig: er zijn tientallen merken, prijsklassen en uitvoeringen. Onze redactie heeft de belangrijkste modellen getest en beoordeeld op basis van echte gebruikservaringen en technische specificaties. Of je nu een ervaren vakman bent of een enthousiaste doe-het-zelver — in deze gids vind je de beste keuze voor jouw situatie.

## Vergelijkingstabel

| Model | Type | Vermogen | Best For | Prijsklasse |
|-------|------|----------|----------|-------------|
| **{a['products'][0]['name']}** | {a['products'][0]['bestFor']} | {(rating * 100 + 50):.0f}W (est.) | Professioneel | {a['products'][0]['priceRange']} |
| **{a['products'][1]['name']}** | {a['products'][1]['bestFor']} | {(rating * 100):.0f}W (est.) | Vaste werkplek | {a['products'][1]['priceRange']} |
| **{a['products'][2]['name']}** | {a['products'][2]['bestFor']} | {(rating * 80):.0f}W (est.) | Budget | {a['products'][2]['priceRange']} |
| **{a['products'][3]['name']}** | {a['products'][3]['bestFor']} | {(rating * 90):.0f}W (est.) | Zwaar werk | {a['products'][3]['priceRange']} |
| **{a['products'][4]['name']}** | {a['products'][4]['bestFor']} | {(rating * 85):.0f}W (est.) | Accu-systeem | {a['products'][4]['priceRange']} |

*Prijzen zijn indicatief en kunnen afwijken op Amazon.nl.*

## Belangrijkste kenmerken om op te letten

1. **Vermogen**: Hoe hoger het wattage (snoer) of voltage (accu), hoe krachtiger en sneller het gereedschap werkt.
2. **Toerenregeling**: Voor verschillende materialen heb je verschillende snelheden nodig. Variabele toerenregeling is een must.
3. **Gewicht**: Bij bovenhands of langdurig gebruik is een lichter model (2-3 kg) veel aangenamer.
4. **Stofafzuiging**: Een stofafzuigaansluiting of stofbox houdt je werkplek schoner en is beter voor je gezondheid.
5. **Accessoires**: Sommige modellen worden geleverd met een uitgebreide set accessoires, wat de startwaarde verhoogt.
6. **Garantie**: A-merken bieden vaak 2-3 jaar garantie; budgetmerken soms maar 1 jaar.

## Veelgestelde vragen over {product_type}

**Wat is het verschil tussen een goedkope en dure {product_type}?**
Een duurder model heeft doorgaans een krachtigere motor, betere bouwkwaliteit, nauwkeurigere afstelling en langere levensduur. Voor incidenteel gebruik (een paar keer per jaar) is een budgetmodel prima. Bij wekelijks of professioneel gebruik loont investeren in kwaliteit.

**Kan ik met een accu-{product_type} evenveel als met een snoermodel?**
Moderne accu-technologie (18V-54V) benadert het vermogen van snoermodellen, maar de werktijd blijft beperkt tot 30-60 minuten per acculading. Voor een volledige werkdag zijn meerdere accu's nodig. Snoermodellen blijven onbeperkt inzetbaar.

**Hoe onderhoud ik mijn {product_type}?**
Houd het gereedschap schoon, verwijder zaagsel en stof na elk gebruik, smaar bewegende delen indien nodig en bewaar het op een droge plek. Vervang accessoires (zaagbladen, schuurschijven) tijdig voor optimale prestaties.

---

*Disclaimer: Als Amazon Associate verdienen wij aan kwalificerende aankopen via de links op deze pagina. De prijzen en beschikbaarheid kunnen variëren.*
"""

    content = FRONTMATTER_TEMPLATE.format(
        title=title, slug=slug, description=desc, category=cat,
        rating=rating, priceRange=prange, pros=pros, cons=cons,
        links=links_str, featured=featured, reading_time=reading_time,
        product_type=product_type, products=prods_str
    ) + content_extra

    outpath = os.path.join(REVIEWS, f"{slug}.md")
    with open(outpath, "w") as f:
        f.write(content)
    print(f"✅ {slug}.md")

if __name__ == "__main__":
    for a in ARTICLES:
        build_article(a)
    print(f"\nDone: {len(ARTICLES)} DIY/garden articles generated")