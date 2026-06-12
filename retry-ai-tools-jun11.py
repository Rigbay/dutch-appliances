#!/usr/bin/env python3
"""Retry the 3 rate-limited articles with longer delays."""
import os, sys, json, time, urllib.request, urllib.error

ARTICLES_DIR = "/workspace/kieskeuken/dutch-ai-tools/src/content/articles"

# Load Gemini key
GEMINI_KEY = ""
env_path = os.path.expanduser("~/.hermes/.env")
with open(env_path) as f:
    for line in f:
        if line.startswith("GEMINI_API_KEY="):
            GEMINI_KEY = line.split("=", 1)[1].strip()
            break

REMAINING = [
    {
        "slug": "beste-ai-tools-fysiotherapie-praktijk-2026",
        "title": "Beste AI Tools voor Fysiotherapie Praktijken 2026: Oefentherapie, Planning & Patiëntenzorg",
        "description": "Welke AI tools helpen fysiotherapeuten in 2026? Van oefen-apps tot patiëntendossiers — vergelijk de 6 beste tools voor fysiotherapiepraktijken in Nederland.",
        "category": "business",
        "tools": [
            {"name": "FysioRoadmap", "verdict": "Nederlands EPD voor fysiotherapeuten — AI-gedreven anamnese, behandelplannen, ROM-metingen", "priceRange": "€80-150/mnd", "bestFor": "Patiëntendossier & administratie", "rating": 4.5, "affiliateLink": "https://fysioroadmap.nl/"},
            {"name": "Physitrack", "verdict": "Oefen-app met AI — video-oefenprogramma's, telehealth, compliance tracking, 3D-animaties", "priceRange": "€25-75/mnd", "bestFor": "Oefenprogramma's & telehealth", "rating": 4.6, "affiliateLink": "https://physitrack.com/"},
            {"name": "Intramed", "verdict": "Nederlandse praktijksoftware — roosters, facturatie, declaratie, koppeling met zorgverzekeraars", "priceRange": "€60-120/mnd", "bestFor": "Praktijkmanagement NL", "rating": 4.3, "affiliateLink": "https://intramed.nl/"},
            {"name": "Healthcoin", "verdict": "AI-gezondheidsplatform — beloningssysteem voor beweging, koppeling met wearables, preventie-tracker", "priceRange": "€15-45/mnd", "bestFor": "Preventie & beweegstimulering", "rating": 4.1, "affiliateLink": "https://healthcoin.com/"},
            {"name": "ZorgDomein AI", "verdict": "Verwijsplatform met AI — automatische triage, verwijsadviezen, wachttijd-checker", "priceRange": "Gratis voor zorgverleners", "bestFor": "Doorverwijzing & netwerk", "rating": 4.4, "affiliateLink": "https://zorgdomein.nl/"},
            {"name": "Keet", "verdict": "Patiëntcommunicatie app — self-service intake, afspraakherinneringen, oefenvideo's, feedback met AI", "priceRange": "€30-80/mnd", "bestFor": "Patiëntcommunicatie & intake", "rating": 4.2, "affiliateLink": "https://keet.nl/"},
        ],
    },
    {
        "slug": "beste-ai-tools-notarissen-juridisch-2026",
        "title": "Beste AI Tools voor Notarissen & Juridische Praktijken 2026: Akte Automatisering, AI-Contract Review",
        "description": "Welke AI tools gebruiken notarissen, juristen en advocatenkantoren in 2026? Vergelijk akte-automatisering, contractanalyse en legal AI in Nederland.",
        "category": "business",
        "tools": [
            {"name": "LegalSifter", "verdict": "AI-contractanalyse — leest contracten in minuten, haalt risico's en clausules eruit, NL-talig", "priceRange": "€50-200/mnd", "bestFor": "Contractanalyse & review", "rating": 4.5, "affiliateLink": "https://legalsifter.com/"},
            {"name": "Henkelman.ai", "verdict": "Nederlandse legal AI — gespecialiseerd in notariële aktes en vastgoedtransacties", "priceRange": "Op aanvraag", "bestFor": "Notariële aktes & vastgoed", "rating": 4.3, "affiliateLink": "https://henkelman.ai/"},
            {"name": "Harvey AI", "verdict": "Premium legal AI — document drafting, legal research, due diligence voor grote kantoren", "priceRange": "€500-2000/mnd", "bestFor": "Grote advocatenkantoren", "rating": 4.7, "affiliateLink": "https://harvey.ai/"},
            {"name": "JuriBlox", "verdict": "Nederlandse automatisering van juridische documenten — modellen, templates, samenvoegen aktes", "priceRange": "€100-400/mnd", "bestFor": "Documentautomatisering NL", "rating": 4.4, "affiliateLink": "https://juriblox.nl/"},
            {"name": "Clio AI", "verdict": "Praktijkmanagement met AI — case management, urenregistratie, facturatie, cliëntportaal", "priceRange": "€60-150/mnd", "bestFor": "Praktijkmanagement", "rating": 4.2, "affiliateLink": "https://clio.com/"},
            {"name": "DeepJudge", "verdict": "AI-rechtspraak-analyse — voorspelt uitkomsten, analyseert jurisprudentie, zoekt precedenten", "priceRange": "€200-800/mnd", "bestFor": "Jurisprudentie & voorspelling", "rating": 4.1, "affiliateLink": "https://deepjudge.ai/"},
        ],
    },
    {
        "slug": "beste-ai-tools-verhuizen-verhuisbedrijven-2026",
        "title": "Beste AI Tools voor Verhuisbedrijven & Verhuizen 2026: Planning, Offerte & Logistiek",
        "description": "Welke AI tools helpen verhuisbedrijven in 2026? Van offerte-tools tot routeplanning en klantcommunicatie — vergelijk de 6 beste tools.",
        "category": "business",
        "tools": [
            {"name": "MoverBase", "verdict": "All-in-one verhuissoftware — offertes, planning, communicatie, schadeclaims, CRM", "priceRange": "€50-150/mnd", "bestFor": "Totaaloplossing verhuisbedrijf", "rating": 4.4, "affiliateLink": "https://moverbase.com/"},
            {"name": "Supermove", "verdict": "AI-gedreven verhuislogistiek — volumecalulatie via foto, routeoptimalisatie, klantportaal", "priceRange": "€80-250/mnd", "bestFor": "Logistieke optimalisatie", "rating": 4.3, "affiliateLink": "https://supermove.ai/"},
            {"name": "Move4U", "verdict": "Digitale inventarisatie met AI — foto's herkennen goederen, automatische offerte-generatie", "priceRange": "€40-120/mnd", "bestFor": "Offerte & inventarisatie", "rating": 4.2, "affiliateLink": "https://move4u.com/"},
            {"name": "OptimoRoute", "verdict": "AI-routeplanning — dynamische routes, real-time verkeer, meerdere stops, brandstofbesparing", "priceRange": "€35-100/mnd", "bestFor": "Routeoptimalisatie", "rating": 4.5, "affiliateLink": "https://optimoroute.com/"},
            {"name": "Wunderflats AI", "verdict": "AI-tijdelijke woonoplossing — matcht verhuizende klanten met gemeubileerde appartementen", "priceRange": "Gratis voor verhuizers / commissie", "bestFor": "Tussenwoningen & relocatie", "rating": 4.1, "affiliateLink": "https://wunderflats.com/"},
            {"name": "What3words", "verdict": "AI-geolocatie — pinpoint adressen via 3-woorden combinaties, essentieel voor lastige bezorglocaties", "priceRange": "Gratis voor basis / €50-200/mnd pro", "bestFor": "Precieze adreslocatie", "rating": 4.0, "affiliateLink": "https://what3words.com/"},
        ],
    },
]

SYSTEM_PROMPT = """Je bent een Nederlandse content-schrijver gespecialiseerd in AI-tool vergelijkingen voor specifieke beroepsgroepen.
Je schrijft een compleet vergelijkingsartikel in Markdown voor een Astro.js website.

REGELS:
- Titel: begin met "# " (h1) — een pakkende titel over dit onderwerp
- Gebruik ## voor hoofdsecties, ### voor subsecties
- **Vet** voor belangrijke punten en toolnamen
- Geen placeholder-teksten of [vul in] — alles moet echt en feitelijk zijn
- Geen "in dit artikel" of "kortom" of "conclusie" meta-teksten
- Minimaal 900 woorden, maximaal 1500
- Schrijf in natuurlijk Nederlands, niet overdreven SEO-geoptimaliseerd
- Elke tool krijgt een eigen sectie met: beschrijving, prijs, beste use case, pluspunten en minpunten

STRUCTUUR:
1. Intro (1-2 alinea's — schets de relevantie van AI voor deze beroepsgroep in 2026)
2. Voor elke tool: ## Naam — beschrijving, prijs, beste use case, plus/min
3. ## Vergelijkingstabel (Markdown tabel)
4. ## Welke tool kies je? (per type gebruiker/praktijk een advies)"""


def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.8, "maxOutputTokens": 4000, "topP": 0.95}
    }).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            resp = urllib.request.urlopen(req, timeout=120)
            data = json.loads(resp.read().decode())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            if attempt < 3:
                wait = 30 * (attempt + 1)
                print(f"  Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    return ""


def build_frontmatter(topic):
    lines = ["---"]
    lines.append(f"title: '{topic['title']}'")
    lines.append(f"slug: {topic['slug']}")
    lines.append(f"description: {topic['description']}")
    lines.append(f"category: {topic['category']}")
    lines.append("rating: 4.3")
    lines.append("priceRange: EUR 0-500/mnd")
    lines.append("pros:")
    lines.append("- Actuele 2026 AI-toolvergelijking voor deze sector")
    lines.append("- Praktisch advies per type praktijk of gebruiker")
    lines.append("- Nederlandstalig met relevante tools en prijzen")
    lines.append("cons:")
    lines.append("- Prijzen kunnen wijzigen — check aanbieder")
    lines.append("- Tools continu in ontwikkeling — check actuele features")
    lines.append("- Advies hangt af van specifieke praktijkgrootte en behoeften")
    lines.append("affiliateLinks:")
    lines.append("- https://www.beehiiv.com/?via=anonymous-operator")
    lines.append("date: '2026-06-11'")
    lines.append("modelYear: 2026")
    lines.append(f"featuredTool: {topic['tools'][0]['name']}")
    lines.append("readingTime: 10 min")
    lines.append("tools:")
    for t in topic['tools']:
        lines.append(f"- name: {t['name']}")
        lines.append(f"  verdict: {t['verdict']}")
        lines.append(f"  priceRange: {t['priceRange']}")
        lines.append(f"  bestFor: {t['bestFor']}")
        lines.append(f"  rating: {t['rating']}")
        lines.append(f"  affiliateLink: {t['affiliateLink']}")
    lines.append("related:")
    lines.append("- ai-tools-mkb-starten-2026")
    lines.append("- beste-ai-tools-kleine-ondernemers-2026")
    lines.append("- beste-ai-tools-zzpers-2026")
    lines.append("draft: false")
    lines.append("faq:")
    lines.append("- q: Is AI echt bruikbaar in deze sector?")
    lines.append("  a: Ja, in 2026 gebruiken steeds meer professionals in deze sector AI voor administratie, klantcontact en workflow-automatisering. Begin met een tool die aansluit bij je grootste tijdsdruk.")
    lines.append("- q: Wat is de beste tool voor een startende praktijk?")
    lines.append("  a: Voor startende praktijken is de eerste tool in deze vergelijking een goed beginpunt — goede prijs/kwaliteitverhouding en schaalbaar.")
    lines.append("- q: Zijn deze tools AVG-compliant?")
    lines.append("  a: De meeste genoemde tools voldoen aan AVG-richtlijnen, maar controleer altijd zelf de verwerkersovereenkomst en datalocatie (EU/EER).")
    lines.append("---")
    return "\n".join(lines)


print("RETRY: 3 remaining articles with 30-90s backoff delays")
print(f"API key: {'SET' if GEMINI_KEY else 'MISSING!'}")

succeeded = 0
for i, topic in enumerate(REMAINING):
    filename = f"{topic['slug']}.md"
    filepath = os.path.join(ARTICLES_DIR, filename)
    
    # Check if somehow already generated
    if os.path.exists(filepath) and os.path.getsize(filepath) > 500:
        print(f"\n  ALREADY DONE: {filename} ({os.path.getsize(filepath)} bytes)")
        succeeded += 1
        continue
    
    # Longer initial wait for rate limit reset
    if i > 0:
        print(f"  Pre-delay: 45s for rate limit...")
        time.sleep(45)
    
    print(f"\n{'='*60}")
    print(f"[{i+1}/3] GENERATING: {topic['title']}")
    print(f"{'='*60}")
    
    tool_specs = []
    for t in topic["tools"]:
        tool_specs.append(f"--- {t['name']} ---\nBeschrijving: {t['verdict']}\nPrijs: {t['priceRange']}\nBeste voor: {t['bestFor']}")
    
    prompt = SYSTEM_PROMPT + "\n\n"
    prompt += f"Schrijf een compleet AI-tool vergelijkingsartikel voor:\n\n"
    prompt += f"TITEL: {topic['title']}\n"
    prompt += f"DOELGROEP: {topic['description']}\n"
    prompt += f"TE VERGELIJKEN TOOLS:\n" + "\n".join(tool_specs) + "\n\n"
    prompt += "Schrijf nu het volledige artikel in Markdown (geen frontmatter). Begin met een # titel."
    
    try:
        body = call_gemini(prompt)
    except Exception as e:
        print(f"  FAILED after all retries: {e}")
        continue
    
    if not body or len(body) < 500:
        print(f"  FAILED: too short ({len(body)} chars)")
        continue
    
    frontmatter = build_frontmatter(topic)
    full = frontmatter + "\n" + body
    
    if full.count("---") > 3:
        parts = full.split("---", 2)
        if len(parts) >= 3:
            full = parts[0] + "---" + parts[2]
    
    with open(filepath, 'w') as f:
        f.write(full)
    
    print(f"  SAVED: {filename} ({len(body.split())} words, {len(body)} chars)")
    succeeded += 1

print(f"\n{'='*60}")
print(f"RETRY RESULT: {succeeded}/{len(REMAINING)} generated")
print(f"{'='*60}")

for topic in REMAINING:
    fp = os.path.join(ARTICLES_DIR, f"{topic['slug']}.md")
    exists = os.path.exists(fp)
    size = os.path.getsize(fp) if exists else 0
    print(f"  {'✓' if exists else '✗'} {topic['slug']}.md ({size} bytes)")
