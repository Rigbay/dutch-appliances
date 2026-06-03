#!/usr/bin/env python3
"""Regenerate 5 DIY/garden gap articles — correct Astro frontmatter schema, no sections field."""

import os

REPO = "/home/cls/kieskeuken"
REVIEWS = os.path.join(REPO, "src", "content", "reviews")

ARTICLES = [
    {
        "slug": "beste-cirkelzaag-2026",
        "title": "Beste cirkelzaag 2026: welke zaagmachine zaagt zuiver en veilig?",
        "description": "Vergelijk de beste cirkelzagen van 2026 — accu-, snoer- en tafelmodellen voor doe-het-zelvers en ervaren klussers naast elkaar met voor- en nadelen.",
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
            {"name": "Ryobi R18CS7-0 ONE+", "verdict": "Betaalbare 18V accu-cirkelzaag voor het ONE+ systeem, voordelig bij al bestaande accus.", "priceRange": "EUR 70-100", "bestFor": "Accu-systeem uitbreiding", "rating": 4.3}
        ],
        "related": ["beste-decoupeerzaag-2026", "beste-accu-boormachine-2026", "beste-haakse-slijper-2026"]
    },
    {
        "slug": "beste-decoupeerzaag-2026",
        "title": "Beste decoupeerzaag 2026: welke figuurzaag zaagt strak en precies?",
        "description": "Zoek je een decoupeerzaag voor curvilijns zagen? Onze vergelijking van de beste modellen van 2026 helpt je kiezen van instap tot professioneel met tips.",
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
        ],
        "related": ["beste-cirkelzaag-2026", "beste-multitool-2026", "beste-schuurmachine-2026"]
    },
    {
        "slug": "beste-schuurmachine-2026",
        "title": "Beste schuurmachine 2026: vlakschuurder, bandschuurder of delta?",
        "description": "Welke schuurmachine past bij jouw klus? Vlakschuurders, bandschuurders en delta- schuurmachines vergeleken voor gladde afwerking van hout, verf en metaal.",
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
        ],
        "related": ["beste-decoupeerzaag-2026", "beste-multitool-2026", "beste-haakse-slijper-2026"]
    },
    {
        "slug": "beste-haakse-slijper-2026",
        "title": "Beste haakse slijper 2026: welke slijptol kies je voor metaal en steen?",
        "description": "De beste haakse slijpers van 2026 voor slijpen, zagen en ontbramen. Vergelijk accu- en snoermodellen van Bosch, Makita, Dewalt, Einhell en Ryobi.",
        "category": "tuin",
        "rating": 4.5,
        "priceRange": "EUR 40-250",
        "pros": [
            "Veelzijdig inzetbaar: slijpen, zagen, ontbramen en polijsten",
            "Accu-modellen bieden mobiliteit op de bouwplaats",
            "Verschillende schijfmaten (125mm en 230mm) voor elk type klus"
        ],
        "cons": [
            "Zeer gevaarlijk gereedschap bij verkeerd gebruik verplicht veiligheidshelm en bril",
            "230mm modellen zijn zwaar en onhandig voor bovenhands werk",
            "Lawaaierig en stoffig met name bij steenbewerking"
        ],
        "products": [
            {"name": "Bosch Professional GWS 18V-125 SC", "verdict": "Krachtigste 18V haakse slijper van Bosch met Bluetooth en constante toerenregeling.", "priceRange": "EUR 180-230", "bestFor": "Professioneel gebruik", "rating": 4.8},
            {"name": "Makita GA5030", "verdict": "Solide 720W snoer-haakse slijper 125mm compact en lichtgewicht voor de prijs.", "priceRange": "EUR 50-70", "bestFor": "Beste prijs-kwaliteit", "rating": 4.6},
            {"name": "Dewalt DCG414N", "verdict": "Professionele 54V accu-haakse slijper voor zwaar dagelijks gebruik.", "priceRange": "EUR 200-260", "bestFor": "Zwaar accu-werk", "rating": 4.7},
            {"name": "Einhell TC-AG 125/850", "verdict": "Betaalbare 850W snoer-haakse slijper met softgrip en extra handgreep.", "priceRange": "EUR 30-45", "bestFor": "Budget", "rating": 4.3},
            {"name": "Ryobi R18AG-0 ONE+", "verdict": "Lichtgewicht 18V accu-haakse slijper voor het ONE+ systeem geschikt voor onderhoud.", "priceRange": "EUR 60-85", "bestFor": "Accu-lijn", "rating": 4.3}
        ],
        "related": ["beste-cirkelzaag-2026", "beste-multitool-2026", "beste-schuurmachine-2026"]
    },
    {
        "slug": "beste-multitool-2026",
        "title": "Beste multitool 2026: oscillatiegereedschap voor zagen schuren en snijden",
        "description": "Multitools oscillatiegereedschap voor precisiewerk zagen schuren en snijden in een. Onze top 5 beste multitools van 2026 voor elke klusser thuis en op de bouw.",
        "category": "tuin",
        "rating": 4.4,
        "priceRange": "EUR 40-200",
        "pros": [
            "Oscillerende beweging voor precieze zaag- en schuursnedes op moeilijke plekken",
            "Universeel inzetbaar met tientallen accessoires voor verschillende toepassingen",
            "Accu-modellen licht en wendbaar voor bovenhands gebruik"
        ],
        "cons": [
            "Niet geschikt voor grote of diepe zaagsnedes daarvoor is een cirkelzaag beter",
            "Trillingen kunnen bij langdurig gebruik vermoeiend zijn",
            "Accessoires zijn relatief duur voor de merk-systemen"
        ],
        "products": [
            {"name": "Bosch Professional GOP 18V-34", "verdict": "Beste accu-multitool met 18V Brushless motor Bluetooth en StarlockMax opname.", "priceRange": "EUR 170-220", "bestFor": "Professioneel", "rating": 4.8},
            {"name": "Makita TM3010C", "verdict": "Krachtige 310W snoer-multitool met constante toerenregeling en gereedschapsloze wissel.", "priceRange": "EUR 90-120", "bestFor": "Vaste werkplek", "rating": 4.6},
            {"name": "Dewalt DCS355N", "verdict": "Solide 18V accu-multitool met LED-verlichting en universeel accessoire-systeem.", "priceRange": "EUR 120-160", "bestFor": "Accu-gebruik", "rating": 4.5},
            {"name": "Einhell TC-MG 250", "verdict": "Uitstekende budget multitool met 250W motor en 35 accessoires inbegrepen.", "priceRange": "EUR 40-55", "bestFor": "Budget starter set", "rating": 4.3},
            {"name": "Ryobi R18MT-0 ONE+", "verdict": "Compacte 18V accu-multitool voor het ONE+ systeem met wissel zonder gereedschap.", "priceRange": "EUR 55-75", "bestFor": "Accu-systeem", "rating": 4.3}
        ],
        "related": ["beste-decoupeerzaag-2026", "beste-cirkelzaag-2026", "beste-schuurmachine-2026"]
    }
]

BODY_TEMPLATE = """

Een goede {pt} is onmisbaar in de gereedschapskist van zowel de professionele klusser als de enthousiaste doe-het-zelver. Of je nu meubels maakt, een verbouwing uitvoert of gewoon af en toe iets in huis repareert — de juiste keuze bespaart tijd, frustratie en levert mooiere resultaten op.

## Vergelijkingstabel

| Model | Type | Best For | Prijsklasse |
|-------|------|----------|-------------|
| **{p0}** | Professioneel | {b0} | {r0} |
| **{p1}** | Vaste werkplek | {b1} | {r1} |
| **{p2}** | Budgetklusser | {b2} | {r2} |
| **{p3}** | Zwaar werk | {b3} | {r3} |
| **{p4}** | Accu-systeem | {b4} | {r4} |

Prijzen zijn indicatief. Check actuele prijzen op Amazon NL via de onderstaande kooplinks.

## Waar let je op bij het kiezen?

### Vermogen en type
Snoer-modellen bieden onbeperkt vermogen en zijn lichter, maar je bent gebonden aan een stopcontact. Accu-modellen geven bewegingsvrijheid, maar wegen meer en werken korter per lading. Voor thuisgebruik is een snoermodel vaak voordeliger; voor op locatie is een accu-model onmisbaar.

### Gewicht en gebruiksgemak
Bij langdurig of bovenhands gebruik is elke ons extra vermoeiend. Professionele modellen wegen 2-4 kg, budgetmodellen vaak 3-5 kg. Let ook op de ergonomie: softgrip handgrepen en goede balans maken een wereld van verschil.

### Accessoires en onderhoud
{pt} gebruikt verbruiksaccessoires die regelmatig vervangen moeten worden. Kijk bij aankoop niet alleen naar de machine zelf, maar ook naar de beschikbaarheid en prijs van zaagbladen, schuurschijven of slijpstenen. Een duur model met dure, zeldzame accessoires is op lange termijn duurder dan een betaalbaar model met universele standaard accessoires.

## Veelgestelde vragen

**Wat is het verschil tussen een goedkope en dure {pt}?**
Een duurder model heeft doorgaans een krachtigere motor, betere bouwkwaliteit, nauwkeurigere afstelling en langere levensduur. Voor incidenteel gebruik (een paar keer per jaar) is een budgetmodel prima. Bij wekelijks of professioneel gebruik loont investeren in kwaliteit.

**Kan ik met een accu-versie evenveel als met een snoermodel?**
Moderne 18V-54V accu-technologie benadert het vermogen van snoermodellen, maar de werktijd blijft beperkt tot 30-60 minuten per lading. Voor een volledige werkdag zijn meerdere accus nodig.

**Hoe onderhoud ik mijn {pt}?**
Houd het gereedschap schoon, verwijder zaagsel en stof na elk gebruik en bewaar het op een droge plek. Vervang accessoires tijdig voor optimale prestaties.

---

*Disclaimer: Als Amazon Associate verdienen wij aan kwalificerende aankopen via de links op deze pagina. Actuele prijzen en beschikbaarheid kunnen afwijken.*
"""

def build_yaml(a):
    """Build the YAML frontmatter string."""
    lines = ["---"]
    lines.append(f"title: '{a['title']}'")
    lines.append(f"slug: {a['slug']}")
    lines.append(f"description: >-")
    lines.append(f"  {a['description']}")
    lines.append(f"category: {a['category']}")
    lines.append(f"rating: {a['rating']}")
    lines.append(f"priceRange: '{a['priceRange']}'")
    
    lines.append("pros:")
    for p in a['pros']:
        lines.append(f"- {p}")
    
    lines.append("cons:")
    for c in a['cons']:
        lines.append(f"- {c}")
    
    lines.append("affiliateLinks:")
    for p in a['products']:
        sq = p['name'].replace(" ", "+")
        lines.append(f"- https://www.amazon.nl/s?k={sq}&tag=kieskeukennl-21")
    
    lines.append("date: 2026-06-03")
    lines.append("modelYear: 2026")
    lines.append(f"featuredProduct: '{a['products'][0]['name']}'")
    lines.append("readingTime: 7 min")
    
    lines.append("products:")
    for p in a['products']:
        sq = p['name'].replace(" ", "+")
        lines.append(f"  - name: '{p['name']}'")
        lines.append(f"    verdict: '{p['verdict']}'")
        lines.append(f"    priceRange: '{p['priceRange']}'")
        lines.append(f"    bestFor: '{p['bestFor']}'")
        lines.append(f"    rating: {p['rating']}")
        lines.append(f"    affiliateLink: https://www.amazon.nl/s?k={sq}&tag=kieskeukennl-21")
    
    lines.append("related:")
    for r in a['related']:
        lines.append(f"- {r}")
    
    lines.append("draft: false")
    lines.append("---")
    return "\n".join(lines)

def build_body(a):
    pt = a['slug'].replace("beste-", "").replace("-2026", "").replace("-", " ")
    p0 = a['products'][0]['name']
    p1 = a['products'][1]['name']
    p2 = a['products'][2]['name']
    p3 = a['products'][3]['name']
    p4 = a['products'][4]['name']
    b0 = a['products'][0]['bestFor']
    b1 = a['products'][1]['bestFor']
    b2 = a['products'][2]['bestFor']
    b3 = a['products'][3]['bestFor']
    b4 = a['products'][4]['bestFor']
    r0 = a['products'][0]['priceRange']
    r1 = a['products'][1]['priceRange']
    r2 = a['products'][2]['priceRange']
    r3 = a['products'][3]['priceRange']
    r4 = a['products'][4]['priceRange']
    
    return BODY_TEMPLATE.format(pt=pt, p0=p0, p1=p1, p2=p2, p3=p3, p4=p4,
                                b0=b0, b1=b1, b2=b2, b3=b3, b4=b4,
                                r0=r0, r1=r1, r2=r2, r3=r3, r4=r4)

if __name__ == "__main__":
    for a in ARTICLES:
        content = build_yaml(a) + build_body(a)
        path = os.path.join(REVIEWS, f"{a['slug']}.md")
        with open(path, "w") as f:
            f.write(content)
        print(f"✅ {a['slug']}.md")

    print(f"\nDone: {len(ARTICLES)} articles regenerated")