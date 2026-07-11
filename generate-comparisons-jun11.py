#!/usr/bin/env python3
"""Generate 5 high-value Dutch-market comparison articles via Gemini API.
Topics: Streaming, Dating, Autoverzekering, Leasemaatschappijen, Fitness apps."""

import os, sys, json, time, subprocess

ARTICLES_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not GEMINI_KEY:
    # Read from .env
    env_path = os.path.expanduser("~/.hermes/.env")
    with open(env_path) as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_KEY = line.split("=", 1)[1].strip()
                break

# Topics with detailed specs
TOPICS = [
    {
        "slug": "streamingdiensten-vergelijken-netflix-videoland-disney-hbo-viaplay-npo-2026",
        "title": "Streamingdiensten Vergelijken 2026: Netflix vs Videoland vs Disney+ vs HBO Max vs Viaplay vs NPO Start",
        "description": "Netflix, Videoland, Disney+, HBO Max, Viaplay of NPO Start in 2026? Vergelijk prijs, aanbod, Nederlands ondertiteld en 4K-kwaliteit.",
        "category": "entertainment",
        "tools": [
            {"name": "Netflix", "verdict": "Grootste internationale aanbod — series, films, docs, steeds meer Nederlands ondertiteld en origineel", "priceRange": "€7,99-19,99/mnd", "bestFor": "Internationale series & films", "rating": 4.7, "affiliateLink": "https://netflix.com/nl/"},
            {"name": "Videoland", "verdict": "Beste Nederlandse content — Gooische Vrouwen, Mocro Maffia, Echte Meisjes in de Jungle, RTL-content", "priceRange": "€4,99-9,99/mnd", "bestFor": "Nederlandse series & reality", "rating": 4.3, "affiliateLink": "https://videoland.com/"},
            {"name": "Disney+", "verdict": "Familie-aanbod — Disney, Pixar, Marvel, Star Wars, National Geographic, Star voor volwassenen", "priceRange": "€5,99-13,99/mnd", "bestFor": "Families & Disney/Marvel fans", "rating": 4.5, "affiliateLink": "https://disneyplus.com/nl-nl/"},
            {"name": "HBO Max", "verdict": "Premium kwaliteit — HBO Originals, Warner Bros, DC, Harry Potter, Game of Thrones-spin-offs", "priceRange": "€5,99-13,99/mnd", "bestFor": "Premium series & films", "rating": 4.4, "affiliateLink": "https://hbomax.com/nl-nl/"},
            {"name": "Viaplay", "verdict": "Sport + entertainment — F1, Premier League, Formule 1, darts, Scandinavische series", "priceRange": "€15,99/mnd", "bestFor": "Sportfans & Scandinavië", "rating": 4.0, "affiliateLink": "https://viaplay.nl/"},
            {"name": "NPO Start", "verdict": "Gratis Nederlandse content — NPO-programma's, journaal, documentaires, series, geen abonnement", "priceRange": "Gratis (NPO Plus €2,95/mnd)", "bestFor": "Publieke omroep & gratis kijken", "rating": 4.2, "affiliateLink": "https://npostart.nl/"},
        ],
    },
    {
        "slug": "datingapps-vergelijken-tinder-bumble-happn-breeze-lexa-2026",
        "title": "Datingapps Vergelijken 2026: Tinder vs Bumble vs Happn vs Breeze vs Lexa",
        "description": "Tinder, Bumble, Happn, Breeze of Lexa in 2026? Vergelijk de beste datingapps op prijs, type relatie, matching-methode en succesratio.",
        "category": "lifestyle",
        "tools": [
            {"name": "Tinder", "verdict": "Grootste gebruikersbasis — swipen, hoog volume, voor casual tot serieus, wereldwijd de standaard", "priceRange": "Gratis / Tinder Plus €7,99/mnd / Gold €24,99/mnd", "bestFor": "Grootste bereik, casual tot serieus", "rating": 4.5, "affiliateLink": "https://tinder.com/"},
            {"name": "Bumble", "verdict": "Vrouwen maken eerste zet — feministisch model, ook Bumble BFF en Bumble Bizz, kwaliteit boven kwantiteit", "priceRange": "Gratis / Premium €14,99/mnd", "bestFor": "Vrouwen die controle willen, serieus daten", "rating": 4.4, "affiliateLink": "https://bumble.com/"},
            {"name": "Happn", "verdict": "Real-life ontmoetingen — match met mensen die je fysiek bent tegengekomen, locatie-gebaseerd", "priceRange": "Gratis / Premium €19,99/mnd", "bestFor": "Spontane ontmoetingen, stedelijk", "rating": 4.1, "affiliateLink": "https://happn.com/"},
            {"name": "Breeze", "verdict": "Geen chatten — meteen op date, AI-match, volledig Nederlands concept, innovatief", "priceRange": "€9 per date", "bestFor": "Geen chatgedoe, meteen echt daten", "rating": 4.3, "affiliateLink": "https://breeze.social/"},
            {"name": "Lexa", "verdict": "Serieuze relaties — grootste Nederlandse datingplatform voor lange termijn, profiel-gedreven", "priceRange": "€20-30/mnd", "bestFor": "Serieuze relatiezoekers, 30+", "rating": 4.2, "affiliateLink": "https://lexa.nl/"},
        ],
    },
    {
        "slug": "autoverzekering-vergelijken-independer-unive-centraal-beheer-allianz-2026",
        "title": "Autoverzekering Vergelijken 2026: Independer vs Univé vs Centraal Beheer vs Allianz Direct",
        "description": "Independer, Univé, Centraal Beheer (Even Apeldoorn Bellen), Allianz Direct of FBTO in 2026? Vergelijk WA, WA+ en All-risk autoverzekeringen op prijs en service.",
        "category": "finance",
        "tools": [
            {"name": "Independer", "verdict": "Beste vergelijkingssite — alle verzekeraars in één overzicht, heldere filters, jaarlijks bespaaradvies", "priceRange": "Gratis te gebruiken", "bestFor": "Objectief vergelijken & besparen", "rating": 4.6, "affiliateLink": "https://independer.nl/"},
            {"name": "Univé", "verdict": "Coöperatief met ledenvoordeel — geen winstoogmerk, elk jaar winstdeling, hoge klanttevredenheid", "priceRange": "WA: €25-55/mnd", "bestFor": "Klantvriendelijk & ledengericht", "rating": 4.5, "affiliateLink": "https://unive.nl/"},
            {"name": "Centraal Beheer", "verdict": "Even Apeldoorn bellen — beste bereikbaarheid, 24/7 schadeservice, scherpe premie via online afsluiten", "priceRange": "WA: €22-50/mnd", "bestFor": "Service & bereikbaarheid", "rating": 4.4, "affiliateLink": "https://centraalbeheer.nl/"},
            {"name": "Allianz Direct", "verdict": "Online prijsvechter — direct online afsluiten, scherpe premies, onderdeel van wereldwijde Allianz-groep", "priceRange": "WA: €20-45/mnd", "bestFor": "Online afsluiten & lage premie", "rating": 4.3, "affiliateLink": "https://allianzdirect.nl/"},
            {"name": "FBTO", "verdict": "Eenvoudig & transparant — heldere polissen, goede prijs/kwaliteit, geen poespas", "priceRange": "WA: €23-48/mnd", "bestFor": "Eenvoud & transparantie", "rating": 4.3, "affiliateLink": "https://fbto.nl/"},
        ],
    },
    {
        "slug": "leaseauto-vergelijken-leasplan-justlease-alphabet-athlon-2026",
        "title": "Private Lease Auto Vergelijken 2026: LeasePlan vs Justlease vs Alphabet vs Athlon vs ANWB",
        "description": "Private Lease vergelijken in 2026? LeasePlan, Justlease, Alphabet, Athlon of ANWB Lease op prijs, voorwaarden, contractduur en kilometerbundel.",
        "category": "finance",
        "tools": [
            {"name": "LeasePlan", "verdict": "Grootste leasemaatschappij — breedste aanbod, flexibele contracten, incl. verzekering en onderhoud", "priceRange": "€250-600/mnd", "bestFor": "Keuzevrijheid & flexibiliteit", "rating": 4.6, "affiliateLink": "https://leaseplan.com/nl-nl/"},
            {"name": "Justlease", "verdict": "Scherpe prijzen — jonge occasions mogelijk, korte looptijden (12 maanden), transparant", "priceRange": "€220-550/mnd", "bestFor": "Lage instap & flexibele duur", "rating": 4.4, "affiliateLink": "https://justlease.nl/"},
            {"name": "Alphabet", "verdict": "Premium zakelijke leasemaatschappij — ook private lease, duurzaam aanbod, EV-specialist", "priceRange": "€300-700/mnd", "bestFor": "EV-rijders & premium", "rating": 4.3, "affiliateLink": "https://alphabet.com/nl-nl/"},
            {"name": "Athlon", "verdict": "Internationaal en innovatief — sterke EV-focus, mobiliteitsbudget in plaats van vaste auto", "priceRange": "€280-650/mnd", "bestFor": "Duurzaamheid & mobiliteitsoplossingen", "rating": 4.2, "affiliateLink": "https://athlon.com/nl-nl/"},
            {"name": "ANWB Lease", "verdict": "Betrouwbaar & ledenvoordeel — ANWB-service, uitgebreide pechhulp, vertrouwde naam", "priceRange": "€270-600/mnd", "bestFor": "Betrouwbaarheid & ANWB-leden", "rating": 4.5, "affiliateLink": "https://anwb.nl/private-lease/"},
        ],
    },
    {
        "slug": "fitness-apps-vergelijken-strava-runkeeper-fitbit-apple-fitness-fitnotes-2026",
        "title": "Fitness Apps Vergelijken 2026: Strava vs Runkeeper vs Fitbit Premium vs Apple Fitness+ vs FitNotes",
        "description": "Strava, Runkeeper, Fitbit Premium, Apple Fitness+ of FitNotes in 2026? Vergelijk de beste fitness apps op sporttracking, coaching, community en prijs.",
        "category": "lifestyle",
        "tools": [
            {"name": "Strava", "verdict": "Beste community — hardlopen + fietsen, segmenten, challenges, wereldwijde sportcommunity", "priceRange": "Gratis / €5,99/mnd Premium", "bestFor": "Sportcommunity & competities", "rating": 4.7, "affiliateLink": "https://strava.com/"},
            {"name": "Runkeeper", "verdict": "Beste voor beginners — hardloop-trainingen, ASICS-oefeningen, eenvoudig instappen", "priceRange": "Gratis / Go Premium €9,99/mnd", "bestFor": "Beginnende hardlopers", "rating": 4.3, "affiliateLink": "https://runkeeper.com/"},
            {"name": "Fitbit Premium", "verdict": "Holistisch — slaap, stress, voeding + activiteit, koppeling met Fitbit wearables", "priceRange": "€8,99/mnd", "bestFor": "Allround gezondheid & wearables", "rating": 4.4, "affiliateLink": "https://fitbit.com/nl/premium"},
            {"name": "Apple Fitness+", "verdict": "Beste geleide workouts — HIIT, yoga, kracht, meditatie, naadloos met Apple Watch", "priceRange": "€9,99/mnd (of in Apple One)", "bestFor": "Apple-gebruikers met Watch", "rating": 4.5, "affiliateLink": "https://apple.com/nl/apple-fitness-plus/"},
            {"name": "FitNotes", "verdict": "No-nonsense krachttraining log — gratis, offline, geen social features, puur notities", "priceRange": "Gratis", "bestFor": "Krachtsporters & minimalisten", "rating": 4.2, "affiliateLink": "https://fitnotes.app/"},
        ],
    },
]

SYSTEM_PROMPT = """Je bent een Nederlandse content-schrijver gespecialiseerd in productvergelijkingen voor consumenten. 
Je schrijft een compleet vergelijkingsartikel in Markdown voor een Astro.js website.

REGELS:
- Titel: begin met "# " (h1) — de titel uit de frontmatter
- Gebruik ## voor hoofdsecties, ### voor subsecties
- **Vet** voor belangrijke punten en toolnamen
- Gebruik geen placeholder-teksten of [vul in] — alles moet echt en feitelijk zijn
- Geen "in dit artikel" of "kortom" of "conclusie" — gewoon helder eindigen
- Minimaal 800 woorden, maximaal 1500
- Schrijf in natuurlijk Nederlands, niet overdreven SEO-geoptimaliseerd
- Elke tool moet een eigen sectie krijgen met: beschrijving, prijs, beste use case, pluspunten/minpunten

STRUCTUUR:
1. Intro (1-2 alinea's die het landschap in 2026 schetsen)
2. Voor elke tool: ## Naam — beschrijving, prijs, beste use case, pluspunten en minpunten
3. ## Vergelijkingstabel (in Markdown)
4. ## Welke kies je? (per use case advies)"""

def call_gemini(prompt):
    """Call Gemini API and return text."""
    import urllib.request, urllib.error
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.8,
            "maxOutputTokens": 4000,
            "topP": 0.95,
        }
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read().decode())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < 2:
                time.sleep(5)
            else:
                raise
    
    return ""

def build_frontmatter(topic):
    """Build YAML frontmatter."""
    lines = ["---"]
    lines.append(f"title: '{topic['title']}'")
    lines.append(f"slug: {topic['slug']}")
    lines.append(f"description: {topic['description']}")
    lines.append(f"category: {topic['category']}")
    lines.append("rating: 4.3")
    lines.append("priceRange: EUR 0-100/mnd")
    lines.append("pros:")
    lines.append("- Uitgebreide 2026 vergelijking")
    lines.append("- Duidelijke prijsranges en use cases")
    lines.append("- Nederlandstalig en actueel")
    lines.append("cons:")
    lines.append("- Prijzen kunnen wijzigen — check aanbieder")
    lines.append("- Functies continu in ontwikkeling")
    lines.append("- Keuze hangt af van je specifieke situatie")
    lines.append("affiliateLinks:")
    lines.append("- https://www.beehiiv.com/")
    lines.append(f"date: '2026-06-11'")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: {topic['tools'][0]['name']}")
    lines.append("readingTime: 9 min")
    lines.append("tools:")
    for t in topic['tools']:
        lines.append(f"- name: {t['name']}")
        lines.append(f"  verdict: {t['verdict']}")
        lines.append(f"  priceRange: {t['priceRange']}")
        lines.append(f"  bestFor: {t['bestFor']}")
        lines.append(f"  rating: {t['rating']}")
        lines.append(f"  affiliateLink: {t['affiliateLink']}")
    lines.append("related:")
    lines.append("- adobe-acrobat-vs-smallpdf-vs-ilovepdf-vs-pdf-expert-2026")
    lines.append("- afas-vs-exact-vs-odoo-vs-sap-business-one-2026")
    lines.append("- ahrefs-vs-semrush-vs-moz-2026")
    lines.append("draft: false")
    lines.append("faq:")
    lines.append("- q: Wat is de beste keuze?")
    lines.append("  a: Dat hangt af van je situatie. De eerste tool in deze vergelijking is voor de meeste gebruikers een prima startpunt.")
    lines.append("- q: Zijn er gratis alternatieven?")
    lines.append("  a: Ja, meerdere opties hebben gratis tiers of proefperiodes. Perfect om te beginnen.")
    lines.append("- q: Hoe kies ik de juiste optie?")
    lines.append("  a: Begin met je use case en budget. Filter de tabel op score en prijs.")
    lines.append("---")
    return "\n".join(lines)

def generate_article(topic):
    """Generate and save a single article."""
    filename = f"{topic['slug']}.md"
    filepath = os.path.join(ARTICLES_DIR, filename)
    
    # Check if already exists
    if os.path.exists(filepath):
        print(f"  SKIP: {filename} already exists")
        return False
    
    print(f"\n{'='*60}")
    print(f"GENERATING: {topic['title']}")
    print(f"{'='*60}")
    
    # Build prompt for body content
    tool_names = [t['name'] for t in topic['tools']]
    
    # Build tool specs for prompt
    tool_specs = []
    for t in topic["tools"]:
        spec = "--- {} ---\nBeschrijving: {}\nPrijs: {}\nBeste voor: {}".format(
            t["name"], t["verdict"], t["priceRange"], t["bestFor"]
        )
        tool_specs.append(spec)
    tool_specs_text = "\n".join(tool_specs)
    
    prompt = SYSTEM_PROMPT + "\n\n"
    prompt += "Schrijf een compleet vergelijkingsartikel over het volgende onderwerp:\n\n"
    prompt += "TITEL: {}\n".format(topic["title"])
    prompt += "ONDERWERP: Vergelijk {}\n".format(", ".join(tool_names))
    prompt += "DOELGROEP: Nederlandse consumenten die willen kiezen tussen deze opties in 2026\n\n"
    prompt += "Gebruik de onderstaande gegevens per tool in je artikel:\n\n"
    prompt += tool_specs_text + "\n\n"
    prompt += 'Schrijf nu het volledige artikel in Markdown (geen frontmatter, die komt er al). Begin met "# " gevolgd door een pakkende titel. Eindig met een vergelijkingstabel en use-case adviezen.'

    try:
        body = call_gemini(prompt)
    except Exception as e:
        print(f"  FAILED to generate: {e}")
        return False
    
    if not body or len(body) < 400:
        print(f"  FAILED: response too short ({len(body)} chars)")
        return False
    
    # Assemble full article
    frontmatter = build_frontmatter(topic)
    full_article = frontmatter + "\n" + body
    
    # Strip any frontmatter the LLM might have generated
    if full_article.count("---") > 3:
        # Too many --- delimiters, try to fix
        parts = full_article.split("---", 2)
        if len(parts) >= 3:
            full_article = parts[0] + "---" + parts[2]
    
    # Write
    with open(filepath, 'w') as f:
        f.write(full_article)
    
    word_count = len(body.split())
    print(f"  SAVED: {filename} ({word_count} words, {len(body)} chars)")
    return True

def main():
    print("=" * 60)
    print("JUNE 11 COMPARISON GENERATOR")
    print(f"API key: {'SET' if GEMINI_KEY else 'MISSING!'}")
    print(f"Output: {ARTICLES_DIR}")
    print("=" * 60)
    
    if not GEMINI_KEY:
        print("ERROR: GEMINI_API_KEY not found!")
        sys.exit(1)
    
    succeeded = 0
    for topic in TOPICS:
        if generate_article(topic):
            succeeded += 1
        time.sleep(1)  # Rate limit buffer
    
    print(f"\n{'='*60}")
    print(f"RESULT: {succeeded}/{len(TOPICS)} articles generated")
    print(f"{'='*60}")
    
    # Verify
    for topic in TOPICS:
        filepath = os.path.join(ARTICLES_DIR, f"{topic['slug']}.md")
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✓ {topic['slug']}.md ({size} bytes)")
        else:
            print(f"  ✗ {topic['slug']}.md MISSING")

if __name__ == "__main__":
    main()
