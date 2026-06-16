#!/usr/bin/env python3
"""Regenerate airfryer-vs-stoomoven-2026.md cleanly using Ollama with better prompting."""
import subprocess, time

MODEL = "qwen3:14b"
OUT_DIR = "/workspace/kieskeuken/src/content/reviews"

SYSTEM_PROMPT = """Je bent een Nederlandse copywriter. Je schrijft ALLEEN de Markdown output — geen denkproces, geen "Thinking...", geen uitleg. Start direct met de YAML frontmatter.

FORMAT: Exact deze YAML frontmatter, gevolgd door de body in Markdown:

---
title: 'Airfryer vs. Stoomoven 2026: Welke Is Gezonder en Veelzijdiger?'
slug: 'airfryer-vs-stoomoven-2026'
description: 'Airfryer of stoomoven in 2026? Vergelijk gezondheid, veelzijdigheid en kosten. Vind de beste modellen op Amazon.nl (tag: kieskeukennl-21).'
category: 'keuken'
rating: 4.5
priceRange: 'EUR 70-500'
pros:
- Snelle bereiding met airfryer, gezonde stoom met stoomoven
- Beide apparaten veelzijdig inzetbaar
- Energiezuinig vergeleken met traditionele oven
cons:
- Airfryer beperkt in capaciteit voor grote gezinnen
- Stoomoven heeft langere opwarmtijd
- Premium stoomovens zijn prijzig
affiliateLinks:
- https://www.amazon.nl/s?k=philips+airfryer+xxl&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=ninja+airfryer+dual&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=miele+stoomoven&tag=kieskeukennl-21
date: 2026-06-16
modelYear: 2026
featuredProduct: 'Philips Airfryer XXL'
readingTime: '9 min'
products:
- name: 'Philips Airfryer XXL'
  verdict: 'De populairste airfryer van Nederland: snel, gezond en betrouwbaar voor dagelijks gebruik.'
  priceRange: 'EUR 150-250'
  bestFor: 'Gezinnen die snel en gezond willen koken'
  rating: 4.8
  affiliateLink: https://www.amazon.nl/s?k=philips+airfryer+xxl&tag=kieskeukennl-21
- name: 'Ninja Airfryer Dual'
  verdict: 'Flexibele airfryer met twee kookzones voor complete maaltijden tegelijk.'
  priceRange: 'EUR 120-200'
  bestFor: 'Gezinnen die meerdere gerechten tegelijk bereiden'
  rating: 4.6
  affiliateLink: https://www.amazon.nl/s?k=ninja+airfryer+dual&tag=kieskeukennl-21
- name: 'Cosori Airfryer'
  verdict: 'Betaalbaar alternatief met ruime mand en gebruiksvriendelijke bediening.'
  priceRange: 'EUR 70-130'
  bestFor: 'Prijsbewuste kopers die kwaliteit zoeken'
  rating: 4.4
  affiliateLink: https://www.amazon.nl/s?k=cosori+airfryer&tag=kieskeukennl-21
- name: 'Miele Stoomoven'
  verdict: 'Premium stoomoven met perfecte temperatuurcontrole en lange levensduur.'
  priceRange: 'EUR 400-500'
  bestFor: 'Kookliefhebbers die investeren in topkwaliteit'
  rating: 4.9
  affiliateLink: https://www.amazon.nl/s?k=miele+stoomoven&tag=kieskeukennl-21
- name: 'Bosch Serie 8 Stoomoven'
  verdict: 'Betrouwbare stoomoven met uitstekende prijs-kwaliteitverhouding voor dagelijks gebruik.'
  priceRange: 'EUR 300-400'
  bestFor: 'Gezinnen die regelmatig stomen en bakken'
  rating: 4.7
  affiliateLink: https://www.amazon.nl/s?k=bosch+serie+8+stoomoven&tag=kieskeukennl-21
related:
- 'beste-airfryer-2026'
- 'beste-stoomoven-2026'
- 'airfryer-vs-heteluchtoven-2026'
- 'airfryer-vs-oven-2026'
- 'slowcooker-vs-stoomoven-2026'
- 'beste-oven-2026'
faq:
- q: 'Is een airfryer echt gezonder dan een stoomoven?'
  a: 'Beide zijn gezond, maar op verschillende manieren. Een airfryer gebruikt tot 80% minder olie dan frituren, terwijl een stoomoven voedingsstoffen beter behoudt door de lage bereidingstemperatuur. Voor pure voedingswaarde is stomen beter; voor knapperige textuur met weinig vet is de airfryer de winnaar.'
- q: 'Kan een airfryer ook stomen?'
  a: 'Nee, een standaard airfryer kan niet stomen. Sommige hybride modellen hebben een stoomfunctie, maar die zijn zeldzaam en duurder. Voor serieus stoomkoken heb je een echte stoomoven nodig.'
- q: 'Wat is het grootste nadeel van een stoomoven?'
  a: 'De prijs en de benodigde ruimte. Een goede inbouw-stoomoven kost al snel EUR 300-500 en vereist een vaste plek in de keuken. Ook duurt voorverwarmen langer dan bij een airfryer.'
- q: 'Welke is beter voor een klein huishouden?'
  a: 'Voor 1-2 personen is een airfryer meestal de betere keuze: compacter, sneller, en goedkoper in aanschaf. Een stoomoven is interessanter voor gezinnen die regelmatig grotere hoeveelheden groenten, vis en vlees bereiden.'
- q: 'Kan ik een airfryer en stoomoven combineren?'
  a: 'Zeker. Veel kookliefhebbers gebruiken een airfryer voor snelle doordeweekse maaltijden en een stoomoven voor het weekend of gezondere bereidingen. Ze vullen elkaar goed aan.'
---

BODY SECTIES (schrijf deze in vlot Nederlands, 800-1200 woorden totaal):

## Airfryer vs. Stoomoven: Wat Is het Verschil?
[2-3 paragrafen: airfryer = hete lucht circulatie, knapperig resultaat met weinig olie. Stoomoven = stoom op lage temperatuur, behoudt voedingsstoffen. Fundamenteel ander kookprincipe.]

## Vergelijkingstabel: Airfryer vs. Stoomoven (2026)
| Aspect | Airfryer | Stoomoven |
|--------|-------------|-------------|
| Prijs | EUR 70-300 | EUR 200-500 |
| Werking | Hete luchtcirculatie | Stoom op lage temperatuur |
| Gezondheid | Tot 80% minder olie | Behoudt vitamines en mineralen |
| Snelheid | 10-20 minuten | 15-30 minuten |
| Capaciteit | 1-5 liter | 20-50 liter |
| Gebruiksgemak | Plug-and-play, eenvoudig | Inbouw, complexere installatie |
| Onderhoud | Mandje reinigen, weinig werk | Ontkalken, rubbers controleren |
| Geschikt voor | Friet, snacks, kip, groenten roosteren | Groenten, vis, vlees, rijst, dim sum |

## Beste Airfryer Modellen van 2026
[Philips Airfryer XXL EUR 150-250, Ninja Airfryer Dual EUR 120-200, Cosori Airfryer EUR 70-130]

## Beste Stoomoven Modellen van 2026
[Miele EUR 400-500, Bosch Serie 8 EUR 300-400, Siemens iQ700 EUR 350-450]

## Wanneer Kies Je voor een Airfryer?
[3-4 situaties: snel koken, knapperige textuur, kleine keuken, budget onder EUR 200]

## Wanneer Kies Je voor een Stoomoven?
[3-4 situaties: maximale voedingswaarde, grote gezinnen, vis/groenten specialist, keukenrenovatie]

## Kostenvergelijking op Lange Termijn
[Aanschaf + energie + onderhoud over 5 jaar. Airfryer: EUR 150 + EUR 75 energie = EUR 225. Stoomoven: EUR 400 + EUR 120 energie + EUR 30 ontkalken = EUR 550.]

## Veelgemaakte Fouten bij het Kiezen
[3 fouten: alleen naar prijs kijken, vergeten dat stoomoven inbouw nodig heeft, airfryer kopen voor stomen]

## Conclusie
[2 paragrafen: airfryer voor snel/knapperig/klein budget, stoomoven voor gezond/precisie/grote gezinnen. Eventueel combineren.]

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou.

BELANGRIJK:
- Geen "Thinking..." of denkproces in de output
- Geen ANSI escape codes
- Geen "hier is het artikel" of uitleg
- Start direct met ---
- Output ALLEEN de Markdown"""

user_prompt = "Schrijf het artikel. Start direct met de YAML frontmatter (---). Geen denkproces, geen uitleg."

print("Regenerating airfryer-vs-stoomoven-2026...")
result = subprocess.run(["ollama", "run", MODEL], input=f"{SYSTEM_PROMPT}\n\n{user_prompt}", capture_output=True, text=True, timeout=180)

output = result.stdout.strip()

# Strip any thinking prefix
if "Thinking..." in output[:500]:
    # Find the first ---
    idx = output.find("\n---")
    if idx > 0:
        output = output[idx+1:].strip()
    elif "---" in output:
        idx = output.find("---")
        output = output[idx:].strip()

# Strip ANSI escape codes
import re
output = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', output)
output = re.sub(r'\x1b\[[0-9;]*[Kk]', '', output)

# Clean up duplicate lines (common Ollama artifact)
lines = output.split("\n")
cleaned = []
prev = ""
for line in lines:
    # Skip lines that are truncated versions of the previous line
    if prev and line.strip() and prev.startswith(line.strip()[:20]) and len(line) < len(prev) * 0.9:
        continue
    cleaned.append(line)
    prev = line
output = "\n".join(cleaned)

out_path = f"{OUT_DIR}/airfryer-vs-stoomoven-2026.md"
with open(out_path, "w") as f:
    f.write(output)

has_tag = "kieskeukennl-21" in output
has_frontmatter = output.startswith("---")
print(f"Written: {out_path} ({len(output)} chars, tag={'✓' if has_tag else '✗'}, fm={'✓' if has_frontmatter else '✗'})")
