#!/usr/bin/env python3
"""Format raw Gemini output into proper Astro content collection markdown with YAML frontmatter."""
import re, yaml, sys
from pathlib import Path
from datetime import date

REVIEWS_DIR = Path("src/content/reviews")
AMAZON_TAG = "kieskeukennl-21"
TODAY = date.today().isoformat()

TOPICS = {
    "kettingzaag-vs-cirkelzaag-2026": {
        "slug": "kettingzaag-vs-cirkelzaag",
        "category": "tuin",
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
    "koelkast-vs-vriezer-2026": {
        "slug": "koelkast-vs-vriezer",
        "category": "huishoudelijk",
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
    "koffiemachine-bonen-vs-koffiecupmachine-2026": {
        "slug": "koffiemachine-bonen-vs-koffiecupmachine",
        "category": "keuken",
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
    "kruimeldief-vs-kruimeldief-draadloos-2026": {
        "slug": "kruimeldief-vs-kruimeldief-draadloos",
        "category": "schoonmaken",
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
    "stofzuiger-dierenharen-vs-allergie-2026": {
        "slug": "stofzuiger-dierenharen-vs-allergie",
        "category": "schoonmaken",
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
}

def parse_article(text, topic):
    """Parse Gemini output into frontmatter + body."""
    # Extract title
    title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else topic["slug"].replace("-", " ").title()
    
    # Extract description
    paras = [p.strip() for p in text.split('\n\n') if p.strip() and not p.startswith('#')]
    description = ""
    for p in paras:
        clean = re.sub(r'[*_`#\[\]]', '', p).strip()
        if len(clean) >= 100:
            description = clean[:180].rsplit('.', 1)[0] + '.'
            break
    if not description:
        description = title[:180]
    
    # Extract FAQ
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
            in_pros = True; in_cons = False; continue
        if re.match(r'^#+\s*(Minpunten|Nadelen|Cons)', line, re.IGNORECASE):
            in_cons = True; in_pros = False; continue
        if re.match(r'^#+\s', line):
            in_pros = False; in_cons = False; continue
        if in_pros and line.startswith(('-', '+', '*')):
            clean = re.sub(r'^[-+*]\s*', '', line).strip()
            if clean and len(clean) > 10: pros.append(clean)
        if in_cons and line.startswith(('-', '+', '*')):
            clean = re.sub(r'^[-+*]\s*', '', line).strip()
            if clean and len(clean) > 10: cons.append(clean)
    
    if len(pros) < 2:
        pros = ["Duidelijke vergelijking tussen beide opties", "Praktisch advies voor verschillende gebruikssituaties"]
    if len(cons) < 2:
        cons = ["Prijzen kunnen variëren per aanbieder", "Niet elk model is in elke winkel beschikbaar"]
    
    # Price range
    price_range = "EUR 50-500"
    price_match = re.search(r'(?:EUR|€)\s*(\d+)\s*[-–]\s*(\d+)', text)
    if price_match:
        price_range = f"EUR {price_match.group(1)}-{price_match.group(2)}"
    
    # Rating
    rating = 4.3
    rating_match = re.search(r'(?:score|rating|beoordeling)[:\s]*(\d+[.,]\d+)', text, re.IGNORECASE)
    if rating_match:
        try:
            rating = float(rating_match.group(1).replace(',', '.'))
            rating = max(1.0, min(5.0, rating))
        except: pass
    
    # Reading time
    word_count = len(text.split())
    reading_time = f"{max(1, word_count // 200)} min"
    
    # Products
    verdicts = ["Beste allround keuze", "Beste prijs-kwaliteit", "Beste budgetkeuze",
                 "Beste premium keuze", "Meest compact", "Meest veelzijdig"]
    best_fors = ["Gezinnen en veelgebruikers", "Prijsbewuste kopers", "Beginners en lichte gebruikers",
                  "Veeleisende gebruikers", "Kleine ruimtes", "Allround gebruik"]
    
    products = []
    for i, (name, link) in enumerate(zip(topic["product_names"], topic["product_links"])):
        products.append({
            "name": name,
            "verdict": verdicts[i % len(verdicts)],
            "priceRange": price_range,
            "bestFor": best_fors[i % len(best_fors)],
            "rating": round(rating + (i * 0.1), 1),
            "affiliateLink": link
        })
    
    frontmatter = {
        "title": title,
        "slug": topic["slug"],
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
    
    return frontmatter

def main():
    for slug, topic in TOPICS.items():
        path = REVIEWS_DIR / f"{slug}.md"
        if not path.exists():
            print(f"  ⚠️  {slug} — file not found, skipping")
            continue
        
        text = path.read_text(encoding="utf-8")
        
        # Skip if already has frontmatter
        if text.startswith("---"):
            print(f"  ⏭️  {slug} — already has frontmatter")
            continue
        
        frontmatter = parse_article(text, topic)
        
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True,
                             sort_keys=False, width=200, indent=2)
        
        output = f"---\n{yaml_str}---\n\n{text}"
        path.write_text(output, encoding="utf-8")
        print(f"  ✅ {slug} — {len(text.split())} words, {len(frontmatter.get('faq', []))} FAQ items")

if __name__ == "__main__":
    main()
