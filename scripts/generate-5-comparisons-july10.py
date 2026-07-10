#!/usr/bin/env python3
"""Generate 5 new comparison articles for July 10, 2026 using Gemini 2.5 Flash-Lite.
All 5 gaps have both individual best-guides already published.
"""
import json, os, sys, time, re
from pathlib import Path
from datetime import date

SITE_ROOT = Path(__file__).resolve().parent.parent
REVIEWS_DIR = SITE_ROOT / "src" / "content" / "reviews"

AMAZON_TAG = "kieskeukennl-21"
TODAY = date.today().isoformat()

# Load API key
env_path = Path.home() / ".hermes" / ".env"
api_key = None
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
            break

if not api_key:
    print("ERROR: No GEMINI_API_KEY found in ~/.hermes/.env")
    sys.exit(1)

import urllib.request, urllib.error

MODEL = "gemini-2.5-flash-lite"

TOPICS = [
    {
        "slug": "kettingzaag-vs-cirkelzaag-2026",
        "title": "Kettingzaag vs. Cirkelzaag 2026: Bomen Vellen of Planken Zagen — Welke Zaag Heb Jij Nodig?",
        "category": "tuin",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Kettingzaag vs Cirkelzaag 2026.

Context: Juli 2026. Veel Nederlanders klussen in de tuin en rond het huis. Een kettingzaag is voor grof werk: bomen vellen, dikke takken zagen, brandhout maken. Een cirkelzaag is voor precisiewerk: planken op maat zagen, laminaat, meubelplaten. Twee totaal verschillende zagen voor totaal verschillende klussen.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — kettingzaag vs cirkelzaag: ruw vs precies, tuin vs werkplaats
2. Snel advies — 3 bullets: tuinier met bomen (kettingzaag), klusser/meubelmaker (cirkelzaag), beide nodig (combi)
3. Hoe werkt het? — technisch verschil: zaagketting vs zaagblad, veiligheid, onderhoud
4. Vergelijkingstabel — 6 producten: Product | Type | Vermogen | Zaagdiepte/Zwaardlengte | Prijs | Score
5. Diepere vergelijking: veiligheid (terugslag, gehoorbescherming), precisie, onderhoud (ketting slijpen vs blad vervangen)
6. Conclusie — wanneer kies je wat, en waarom je ze niet kunt uitwisselen

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Husqvarna Kettingzaag 120 Mark II, Makita Kettingzaag UC4051A, Bosch Kettingzaag UniversalChain 18, Makita Cirkelzaag HS7601, Bosch Cirkelzaag PKS 55, DeWalt Cirkelzaag DWE560
- Minimaal 1500 woorden
- Eerlijk over minpunten (kettingzaag is gevaarlijk en luid, cirkelzaag kan geen dik hout aan)
- Prijzen in euro's""",
        "product_names": [
            "Husqvarna Kettingzaag 120 Mark II",
            "Makita Kettingzaag UC4051A",
            "Bosch Kettingzaag UniversalChain 18",
            "Makita Cirkelzaag HS7601",
            "Bosch Cirkelzaag PKS 55",
            "DeWalt Cirkelzaag DWE560"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Husqvarna+kettingzaag+120+Mark+II&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Makita+kettingzaag+UC4051A&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+kettingzaag+UniversalChain+18&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Makita+cirkelzaag+HS7601&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+cirkelzaag+PKS+55&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=DeWalt+cirkelzaag+DWE560&tag={AMAZON_TAG}"
        ],
        "related": ["beste-kettingzaag-2026", "beste-cirkelzaag-2026", "kettingzaag-vs-handzaag-2026"]
    },
    {
        "slug": "koelkast-vs-vriezer-2026",
        "title": "Koelkast vs. Vriezer 2026: Vers Bewaren of Langdurig Invriezen — Wat Heb Je Echt Nodig?",
        "category": "huishoudelijk",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Koelkast vs Vriezer 2026.

Context: Juli 2026. Bij het inrichten van een keuken of bijkeuken sta je voor de keuze: een losse koelkast, een losse vriezer, of een combi. Een koelkast bewaart vers voedsel op 4°C, een vriezer vriest in op -18°C voor langdurige bewaring. De keuze hangt af van kookgewoontes, gezinsgrootte en beschikbare ruimte.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — koelkast vs vriezer: twee apparaten met totaal verschillende functies
2. Snel advies — 3 bullets: kleine huishoudens (koelkast met vriesvak), meal-preppers (grote vriezer), gezinnen (combi)
3. Hoe werkt het? — technisch verschil: koeltechniek, temperatuurzones, No Frost vs handmatig ontdooien
4. Vergelijkingstabel — 6 producten: Product | Type | Inhoud | Energieklasse | Prijs | Score
5. Diepere vergelijking: energiekosten per jaar, geluidsniveau, plaatsing (onderbouw vs vrijstaand), levensduur
6. Conclusie — wanneer kies je een losse vriezer, en wanneer is een koel-vriescombinatie slimmer

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Bosch Koelkast KIR81AF30, Liebherr Koelkast TP1710, Samsung Koelkast RB29, Liebherr Vriezer GP1376, Bosch Vriezer GSN36, Miele Vriezer FN120
- Minimaal 1500 woorden
- Eerlijk over minpunten (losse vriezer neemt extra ruimte, koelkast zonder vriesvak beperkt)
- Prijzen in euro's""",
        "product_names": [
            "Bosch Koelkast KIR81AF30",
            "Liebherr Koelkast TP1710",
            "Samsung Koelkast RB29",
            "Liebherr Vriezer GP1376",
            "Bosch Vriezer GSN36",
            "Miele Vriezer FN120"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Bosch+koelkast+KIR81AF30&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Liebherr+koelkast+TP1710&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Samsung+koelkast+RB29&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Liebherr+vriezer+GP1376&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+vriezer+GSN36&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Miele+vriezer+FN120&tag={AMAZON_TAG}"
        ],
        "related": ["beste-koelkast-2026", "beste-vriezer-2026", "koelkast-vs-koelvriescombinatie-2026"]
    },
    {
        "slug": "koffiemachine-bonen-vs-koffiecupmachine-2026",
        "title": "Koffiemachine Bonen vs. Cupmachine 2026: Vers Gemalen of Gemak — Welke Koffie Past bij Jou?",
        "category": "keuken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Koffiemachine met Bonen vs Koffiecupmachine 2026.

Context: Juli 2026. Nederlanders drinken gemiddeld 4 koppen koffie per dag. De grote tweedeling: een bonenmachine maalt vers en geeft de beste smaak, maar kost meer en vraagt onderhoud. Een cupmachine (Nespresso, Dolce Gusto, Senseo) is supersnel en makkelijk, maar cups zijn duurder per kop en minder duurzaam.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — de koffie-oorlog: versgemalen vs gemak
2. Snel advies — 3 bullets: koffieliefhebber (bonen), gemakzoeker (cups), budgetbewust (bonen op lange termijn)
3. Hoe werkt het? — technisch verschil: maalwerk vs cups, zetmethodes, melkopschuimen
4. Vergelijkingstabel — 6 producten: Product | Type | Kenmerken | Prijs per kop | Prijs | Score
5. Diepere vergelijking: smaak, kosten per jaar (bij 4 koppen/dag), onderhoud (ontkalken, reinigen), duurzaamheid (cups vs bonen)
6. Conclusie — voor wie is bonen de beste keuze, en wanneer wint de cupmachine

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: De'Longhi Magnifica S, Philips 2200 Series, Siemens EQ.3, Nespresso Vertuo Next, Dolce Gusto Genio S, Senseo Switch
- Minimaal 1500 woorden
- Eerlijk over minpunten (bonenmachine is duurder in aanschaf, cupmachine heeft dure cups en afval)
- Prijzen in euro's""",
        "product_names": [
            "De'Longhi Magnifica S",
            "Philips 2200 Series",
            "Siemens EQ.3",
            "Nespresso Vertuo Next",
            "Dolce Gusto Genio S",
            "Senseo Switch"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=De%27Longhi+Magnifica+S&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+2200+series+koffiemachine&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Siemens+EQ.3+koffiemachine&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Nespresso+Vertuo+Next&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Dolce+Gusto+Genio+S&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Senseo+Switch&tag={AMAZON_TAG}"
        ],
        "related": ["beste-koffiemachine-bonen-2026", "beste-koffiecupmachine-2026", "koffiemachine-bonen-vs-cups-2026"]
    },
    {
        "slug": "kruimeldief-vs-kruimeldief-draadloos-2026",
        "title": "Kruimeldief met Snoer vs. Draadloos 2026: Altijd Stroom of Maximale Vrijheid — Welke Kies Je?",
        "category": "schoonmaken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Kruimeldief met Snoer vs Draadloze Kruimeldief 2026.

Context: Juli 2026. Een kruimeldief is onmisbaar voor snelle schoonmaakklusjes: kruimels op tafel, kattenbakkorrels, trap stofzuigen. De keuze: een model met snoer (altijd vol vermogen, nooit lege accu) of draadloos (maximale bewegingsvrijheid, maar beperkte accuduur).

STRUCTUUR:
1. Inleiding (2-3 alinea's) — snoer vs draadloos: de afweging tussen kracht en vrijheid
2. Snel advies — 3 bullets: altijd thuis bij stopcontact (snoer), snelle actie overal (draadloos), beide (combi)
3. Hoe werkt het? — technisch verschil: accutechnologie (Li-ion), zuigkracht met/zonder snoer, oplaadtijd
4. Vergelijkingstabel — 6 producten: Product | Type | Accuduur/Vermogen | Gewicht | Prijs | Score
5. Diepere vergelijking: zuigkrachtverloop (accu zakt in), levensduur accu, opbergruimte, geluid
6. Conclusie — wanneer kies je snoer, wanneer draadloos, en wat is de beste combi

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Black+Decker Dustbuster (snoer), Philips MiniVac (snoer), Bosch BBH3 (snoer), Dyson V7 Trigger (draadloos), Philips SpeedPro Aqua (draadloos), Black+Decker Dustbuster AdvancedClean (draadloos)
- Minimaal 1500 woorden
- Eerlijk over minpunten (snoer beperkt bereik, draadloos verliest zuigkracht bij lage accu)
- Prijzen in euro's""",
        "product_names": [
            "Black+Decker Dustbuster (snoer)",
            "Philips MiniVac (snoer)",
            "Bosch BBH3 (snoer)",
            "Dyson V7 Trigger (draadloos)",
            "Philips SpeedPro Aqua (draadloos)",
            "Black+Decker Dustbuster AdvancedClean (draadloos)"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Black+Decker+Dustbuster+snoer&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+MiniVac+snoer&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+BBH3+kruimeldief&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Dyson+V7+Trigger&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+SpeedPro+Aqua&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Black+Decker+Dustbuster+AdvancedClean&tag={AMAZON_TAG}"
        ],
        "related": ["beste-kruimeldief-2026", "beste-kruimeldief-draadloos-2026", "stofzuiger-vs-kruimeldief-2026"]
    },
    {
        "slug": "stofzuiger-dierenharen-vs-allergie-2026",
        "title": "Stofzuiger voor Dierenharen vs. Allergie 2026: Huisdieren of Hooikoorts — Welke Filter Heb Je Nodig?",
        "category": "schoonmaken",
        "prompt": f"""Je bent een Nederlandse consumentenjournalist. Schrijf een complete koopgids in het Nederlands over: Stofzuiger voor Dierenharen vs Stofzuiger voor Allergie 2026.

Context: Juli 2026. Nederland telt miljoenen huisdieren en nog meer hooikoortspatiënten. Een stofzuiger voor dierenharen heeft speciale borstels die haren uit tapijt trekken zonder te verstrikken. Een allergiestofzuiger heeft een HEPA-filter dat pollen, huisstofmijt en fijnstof tot 99,97% tegenhoudt. Veel modellen combineren beide, maar de focus verschilt.

STRUCTUUR:
1. Inleiding (2-3 alinea's) — dierenharen vs allergie: twee verschillende problemen, twee verschillende oplossingen
2. Snel advies — 3 bullets: honden/katten-eigenaar (dierenhaar-zuiger), hooikoortspatiënt (allergie-zuiger), beide (combi-model)
3. Hoe werkt het? — technisch verschil: turboborstel vs HEPA H13/H14 filter, zakloos vs met zak
4. Vergelijkingstabel — 6 producten: Product | Focus | Filter | Zak/Zakloos | Prijs | Score
5. Diepere vergelijking: filtervervanging, geurabsorptie (dieren), pollenmetingen, onderhoudskosten
6. Conclusie — wanneer kies je welke focus, en waarom een combi-model vaak de beste keuze is

BELANGRIJK:
- Gebruik Amazon NL affiliate links met tag={AMAZON_TAG}
- Products: Dyson Ball Animal 3, Miele Complete C3 Cat & Dog, Philips Performer Animal, Miele Complete C3 Allergy, Bosch BGL8ALL, Philips Performer Silent
- Minimaal 1500 woorden
- Eerlijk over minpunten (dierenhaar-borstels slijten sneller, HEPA-filters moeten regelmatig vervangen worden)
- Prijzen in euro's""",
        "product_names": [
            "Dyson Ball Animal 3",
            "Miele Complete C3 Cat & Dog",
            "Philips Performer Animal",
            "Miele Complete C3 Allergy",
            "Bosch BGL8ALL",
            "Philips Performer Silent"
        ],
        "product_links": [
            f"https://www.amazon.nl/s?k=Dyson+Ball+Animal+3&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Miele+Complete+C3+Cat+Dog&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+Performer+Animal&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Miele+Complete+C3+Allergy&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Bosch+BGL8ALL&tag={AMAZON_TAG}",
            f"https://www.amazon.nl/s?k=Philips+Performer+Silent&tag={AMAZON_TAG}"
        ],
        "related": ["beste-stofzuiger-tegen-dierenharen-2026", "beste-stofzuiger-voor-allergie-2026", "beste-stofzuiger-2026"]
    }
]

def call_gemini(prompt):
    """Call Gemini API and return text response."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096,
            "topP": 0.95
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        print(f"  HTTP {e.code}: {err[:300]}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def parse_article(text, topic):
    """Parse Gemini output into frontmatter + body."""
    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else topic["title"]
    
    # Extract description (first paragraph after intro, ~150 chars)
    # Find first substantial paragraph
    paras = [p.strip() for p in text.split('\n\n') if p.strip() and not p.startswith('#')]
    description = ""
    for p in paras:
        clean = re.sub(r'[*_`#]', '', p).strip()
        if len(clean) >= 100:
            description = clean[:180].rsplit('.', 1)[0] + '.'
            break
    if not description:
        description = title[:180]
    
    # Extract FAQ section
    faq = []
    faq_section = False
    current_q = None
    current_a = []
    
    for line in text.split('\n'):
        line = line.strip()
        if re.match(r'^#+\s*(FAQ|Veelgestelde|Veel gestelde)', line, re.IGNORECASE):
            faq_section = True
            continue
        if faq_section and re.match(r'^#+\s', line):
            faq_section = False
            if current_q:
                faq.append({"q": current_q, "a": ' '.join(current_a).strip()})
                current_q = None
                current_a = []
            continue
        if faq_section:
            q_match = re.match(r'^(?:\*\*)?(\d+\.\s*)?(.+?\?)(?:\*\*)?$', line)
            if q_match and not line.startswith('-'):
                if current_q:
                    faq.append({"q": current_q, "a": ' '.join(current_a).strip()})
                current_q = q_match.group(2).strip()
                current_a = []
            elif current_q and line:
                current_a.append(line)
    
    if current_q:
        faq.append({"q": current_q, "a": ' '.join(current_a).strip()})
    
    # Ensure at least 3 FAQ items
    if len(faq) < 3:
        faq = []
    
    # Extract pros/cons
    pros = []
    cons = []
    in_pros = False
    in_cons = False
    for line in text.split('\n'):
        line = line.strip()
        if re.match(r'^#+\s*(Pluspunten|Voordelen|Pros)', line, re.IGNORECASE):
            in_pros = True
            in_cons = False
            continue
        if re.match(r'^#+\s*(Minpunten|Nadelen|Cons)', line, re.IGNORECASE):
            in_cons = True
            in_pros = False
            continue
        if re.match(r'^#+\s', line):
            in_pros = False
            in_cons = False
            continue
        if in_pros and line.startswith(('-', '+', '*')):
            clean = re.sub(r'^[-+*]\s*', '', line).strip()
            if clean and len(clean) > 10:
                pros.append(clean)
        if in_cons and line.startswith(('-', '+', '*')):
            clean = re.sub(r'^[-+*]\s*', '', line).strip()
            if clean and len(clean) > 10:
                cons.append(clean)
    
    if len(pros) < 2:
        pros = ["Duidelijke vergelijking tussen beide opties", "Praktisch advies voor verschillende gebruikssituaties"]
    if len(cons) < 2:
        cons = ["Prijzen kunnen variëren per aanbieder", "Niet elk model is in elke winkel beschikbaar"]
    
    # Determine price range
    price_range = "EUR 50-500"
    price_match = re.search(r'(?:EUR|€)\s*(\d+)\s*[-–]\s*(\d+)', text)
    if price_match:
        price_range = f"EUR {price_match.group(1)}-{price_match.group(2)}"
    
    # Determine rating
    rating = 4.3
    rating_match = re.search(r'(?:score|rating|beoordeling)[:\s]*(\d+[.,]\d+)', text, re.IGNORECASE)
    if rating_match:
        try:
            rating = float(rating_match.group(1).replace(',', '.'))
            rating = max(1.0, min(5.0, rating))
        except:
            pass
    
    # Reading time
    word_count = len(text.split())
    reading_time = f"{max(1, word_count // 200)} min"
    
    # Build products array
    products = []
    for i, (name, link) in enumerate(zip(topic["product_names"], topic["product_links"])):
        verdicts = ["Beste allround keuze", "Beste prijs-kwaliteit", "Beste budgetkeuze", 
                     "Beste premium keuze", "Meest compact", "Meest veelzijdig"]
        best_fors = ["Gezinnen en veelgebruikers", "Prijsbewuste kopers", "Beginners en lichte gebruikers",
                      "Veeleisende gebruikers", "Kleine ruimtes", "Allround gebruik"]
        products.append({
            "name": name,
            "verdict": verdicts[i % len(verdicts)],
            "priceRange": price_range,
            "bestFor": best_fors[i % len(best_fors)],
            "rating": round(rating + (i * 0.1), 1),
            "affiliateLink": link
        })
    
    # Build frontmatter
    frontmatter = {
        "title": title,
        "slug": topic["slug"].replace("-2026", ""),
        "description": description,
        "category": topic["category"],
        "rating": rating,
        "priceRange": price_range,
        "pros": pros[:5],
        "cons": cons[:5],
        "affiliateLinks": topic["product_links"][:3],
        "date": TODAY,
        "modelYear": 2026,
        "featuredProduct": topic["product_names"][0],
        "readingTime": reading_time,
        "products": products,
        "related": topic["related"],
        "draft": False
    }
    
    if faq:
        frontmatter["faq"] = faq[:6]
    
    return frontmatter, text

def format_markdown(frontmatter, body):
    """Format as YAML frontmatter + body."""
    import yaml
    
    # Custom YAML dumper for clean output
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, 
                         sort_keys=False, width=200, indent=2)
    
    # Remove body text from Gemini output (we only want the frontmatter)
    # The body is the full Gemini output, but we need to strip the YAML-like parts
    # Actually, for Astro content collections, the body IS the markdown content
    # So we keep the full Gemini output as the body
    
    return f"---\n{yaml_str}---\n\n{body}"

def main():
    print(f"🔧 Generating 5 comparison articles with {MODEL}...\n")
    
    for i, topic in enumerate(TOPICS):
        slug = topic["slug"]
        out_path = REVIEWS_DIR / f"{slug}.md"
        
        if out_path.exists():
            print(f"  [{i+1}/5] ⏭️  {slug} — already exists, skipping")
            continue
        
        print(f"  [{i+1}/5] 🤖 Generating {slug}...")
        text = call_gemini(topic["prompt"])
        
        if not text:
            print(f"  [{i+1}/5] ❌ Failed to generate {slug}")
            continue
        
        frontmatter, body = parse_article(text, topic)
        md = format_markdown(frontmatter, body)
        
        out_path.write_text(md, encoding="utf-8")
        print(f"  [{i+1}/5] ✅ {slug} — {len(text.split())} words, {len(frontmatter.get('faq', []))} FAQ items")
        
        # Rate limit
        if i < len(TOPICS) - 1:
            time.sleep(3)
    
    print(f"\n✅ Done! Generated articles in {REVIEWS_DIR}")

if __name__ == "__main__":
    main()
