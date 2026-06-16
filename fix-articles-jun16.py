#!/usr/bin/env python3
"""Complete truncated articles and fix frontmatter for KiesKeuken.
Hermes cron job — June 16, 2026
"""

import os, sys, json, time, urllib.request, urllib.error

OUT_DIR = "/home/cls/kieskeuken/src/content/reviews"
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen3.5:9b"

def call_ollama(prompt):
    body = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 2048, "top_p": 0.9}
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "")
    except Exception as e:
        print(f"  Ollama error: {e}")
        return None

def complete_article(filepath, last_section):
    """Read truncated article, generate completion, stitch together."""
    with open(filepath) as f:
        existing = f.read()
    
    # Find where the body starts (after second ---)
    fm_end = existing.find("---", 3)
    if fm_end < 0:
        print(f"  Cannot find frontmatter end in {filepath}")
        return False
    
    frontmatter = existing[:fm_end+3]
    body_start = existing[fm_end+3:]
    
    # Get the last complete section heading
    prompt = f"""Je bent een Nederlandse copywriter. Voltooi dit vergelijkingsartikel voor KiesKeuken.nl.

Het artikel is afgebroken na deze sectie: "{last_section}"

Hier is het bestaande artikel tot nu toe:

{body_start}

Schrijf ALLEEN de ontbrekende secties vanaf waar het artikel is afgebroken. Gebruik ## voor koppen. Schrijf in vlot Nederlands. Eindig met de conclusie en deze affiliate disclosure:

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou. Rangschikking gebaseerd op productspecificaties, gebruikerservaringen en prijs-kwaliteitverhouding.

Schrijf minimaal 400 woorden. Stop niet halverwege."""
    
    completion = call_ollama(prompt)
    if not completion or len(completion) < 200:
        print(f"  Failed to generate completion ({len(completion) if completion else 0} chars)")
        return False
    
    # Stitch: frontmatter + existing body + completion
    full = frontmatter + "\n" + body_start.rstrip() + "\n\n" + completion.strip()
    
    with open(filepath, "w") as f:
        f.write(full)
    
    print(f"  Completed: {filepath} ({len(full)} chars, +{len(completion)} chars)")
    return True

# Fix the magnetron article frontmatter
def fix_magnetron_frontmatter():
    filepath = os.path.join(OUT_DIR, "magnetron-vs-heteluchtoven-2026.md")
    with open(filepath) as f:
        content = f.read()
    
    # The article has wrong frontmatter format. Let's rewrite it properly.
    # Extract what we can and rebuild
    new_fm = """---
title: 'Magnetron vs. Heteluchtoven 2026: Welke Is Sneller, Welke Is Lekkerder?'
slug: magnetron-vs-heteluchtoven-2026
description: 'Magnetron of heteluchtoven? Vergelijk snelheid, smaak, energieverbruik en prijs in 2026. Koopadvies met Amazon.nl links (tag: kieskeukennl-21).'
category: keuken
rating: 4.5
priceRange: EUR 50-500
pros:
- Supersnel opwarmen en ontdooien (magnetron)
- Knapperig en gelijkmatig bakresultaat (heteluchtoven)
- Combimagnetron combineert beide werelden
cons:
- Magnetron maakt geen krokant korstje
- Heteluchtoven verbruikt meer energie
- Combimodellen duurder dan losse apparaten
affiliateLinks:
- https://www.amazon.nl/s?k=samsung+combi+magnetron&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=panasonic+combi+magnetron&tag=kieskeukennl-21
- https://www.amazon.nl/s?k=bosch+heteluchtoven&tag=kieskeukennl-21
date: 2026-06-16
modelYear: 2026
featuredProduct: Samsung Combimagnetron MC28H5015
readingTime: 9 min
products:
- name: 'Samsung Combimagnetron MC28H5015'
  verdict: 'Uitstekende combimagnetron met heteluchtfunctie — snel opwarmen én knapperig bakken in één apparaat.'
  priceRange: EUR 300-400
  bestFor: Gezinnen die snelheid en bakkwaliteit willen combineren
  rating: 4.6
  affiliateLink: https://www.amazon.nl/s?k=samsung+combi+magnetron+MC28H5015&tag=kieskeukennl-21
- name: 'Panasonic NN-DS596B Combimagnetron'
  verdict: 'Krachtige inverter-magnetron met stoomfunctie — gelijkmatige garing zonder koude plekken.'
  priceRange: EUR 350-450
  bestFor: Gevorderde thuiskoks die precisie waarderen
  rating: 4.5
  affiliateLink: https://www.amazon.nl/s?k=panasonic+NN-DS596B&tag=kieskeukennl-21
- name: 'Bosch Serie 4 Heteluchtoven'
  verdict: 'Betrouwbare inbouw heteluchtoven met 3D-hete lucht voor gelijkmatig bakken op elk niveau.'
  priceRange: EUR 400-500
  bestFor: Huishoudens die veel bakken en braden
  rating: 4.4
  affiliateLink: https://www.amazon.nl/s?k=bosch+serie+4+heteluchtoven&tag=kieskeukennl-21
- name: 'Whirlpool Heteluchtoven'
  verdict: 'Betaalbare vrijstaande heteluchtoven met ruime inhoud — goede prijs-kwaliteitverhouding.'
  priceRange: EUR 250-350
  bestFor: Budgetbewuste kopers met ruimte voor een vrijstaand model
  rating: 4.2
  affiliateLink: https://www.amazon.nl/s?k=whirlpool+heteluchtoven&tag=kieskeukennl-21
- name: 'Inventum MN308C Magnetron'
  verdict: 'No-nonsense solo-magnetron voor puur opwarmen en ontdooien — compact en betaalbaar.'
  priceRange: EUR 100-180
  bestFor: Studenten, kleine keukens, bijkeuken
  rating: 4.0
  affiliateLink: https://www.amazon.nl/s?k=inventum+magnetron+MN308C&tag=kieskeukennl-21
related:
- beste-magnetron-2026
- beste-oven-2026
- magnetron-vs-combi-magnetron-2026
- airfryer-vs-magnetron-2026
- oven-vs-magnetron-2026
- beste-oven-magnetron-combi-2026
faq:
- q: 'Wat is het verschil tussen een magnetron en een heteluchtoven?'
  a: 'Een magnetron verwarmt voedsel via microgolven die watermoleculen in beweging brengen — supersnel maar zonder korstvorming. Een heteluchtoven circuleert hete lucht met een ventilator voor gelijkmatige garing mét krokante korst. Een combimagnetron combineert beide technieken in één apparaat.'
- q: 'Is een combimagnetron beter dan een losse magnetron en oven?'
  a: 'Een combimagnetron bespaart ruimte en is goedkoper dan twee losse apparaten. De heteluchtfunctie is vaak minder krachtig dan een volwaardige oven, maar voor de meeste huishoudens ruim voldoende. Voor fanatieke bakkers is een losse heteluchtoven aan te raden.'
- q: 'Hoeveel energie verbruikt een heteluchtoven vergeleken met een magnetron?'
  a: 'Een magnetron verbruikt ongeveer 0,7-1,2 kWh per uur, een heteluchtoven 1,5-2,5 kWh. Omdat de magnetron veel korter aan staat, is het energieverbruik per maaltijd vaak lager. Voor grote gerechten die lang moeten garen is de heteluchtoven per portie juist efficiënter.'
- q: 'Kan ik in een magnetron een cake bakken?'
  a: 'In een solo-magnetron niet — je krijgt geen bruine korst. In een combimagnetron met heteluchtfunctie kan het wél, al is het resultaat vaak iets minder gelijkmatig dan in een volwaardige heteluchtoven. Gebruik de heteluchtstand, niet de magnetronstand.'
- q: 'Wat is de levensduur van een magnetron versus een heteluchtoven?'
  a: 'Een magnetron gaat gemiddeld 7-10 jaar mee, een heteluchtoven 10-15 jaar. De magnetron heeft minder bewegende delen maar de magnetronbuis kan na verloop van tijd vermogen verliezen. Regelmatig schoonmaken verlengt de levensduur van beide apparaten.'
---

"""
    
    # Find body start in old content
    old_fm_end = content.find("---", 3)
    if old_fm_end < 0:
        print("  Cannot find body in magnetron article")
        return False
    
    old_body = content[old_fm_end+3:].strip()
    
    # Also complete the body if truncated
    if not old_body.rstrip().endswith(("kieskeukennl-21", "geen extra kosten voor jou", "prijs-kwaliteitverhouding")):
        print("  Magnetron article also truncated, completing...")
        prompt = f"""Je bent een Nederlandse copywriter. Voltooi dit vergelijkingsartikel voor KiesKeuken.nl.

Het artikel is afgebroken. Hier is de bestaande body:

{old_body}

Schrijf ALLEEN de ontbrekende secties. Gebruik ## voor koppen. Schrijf in vlot Nederlands. Eindig met de conclusie en deze affiliate disclosure:

**Affiliate disclosure**: Links verwijzen naar Amazon.nl (tag: kieskeukennl-21). Kleine commissie bij aankoop, geen extra kosten voor jou. Rangschikking gebaseerd op productspecificaties, gebruikerservaringen en prijs-kwaliteitverhouding.

Schrijf minimaal 300 woorden."""
        
        completion = call_ollama(prompt)
        if completion and len(completion) > 150:
            old_body = old_body.rstrip() + "\n\n" + completion.strip()
    
    full = new_fm + old_body
    with open(filepath, "w") as f:
        f.write(full)
    
    print(f"  Fixed: {filepath} ({len(full)} chars)")
    return True

def main():
    # 1. Complete koelkast-vs-amerikaanse-koelkast (truncated at "Beste Koelkast Modellen")
    print("\n[1] Completing koelkast-vs-amerikaanse-koelkast-2026.md...")
    complete_article(
        os.path.join(OUT_DIR, "koelkast-vs-amerikaanse-koelkast-2026.md"),
        "Beste Koelkast Modellen van 2026"
    )
    
    # 2. Complete wasdroger-vs-droogrek (truncated at "Beste Wasdroger Modellen")
    print("\n[2] Completing wasdroger-vs-droogrek-2026.md...")
    complete_article(
        os.path.join(OUT_DIR, "wasdroger-vs-droogrek-2026.md"),
        "Beste Wasdroger Modellen van 2026"
    )
    
    # 3. Fix magnetron article frontmatter + complete body
    print("\n[3] Fixing magnetron-vs-heteluchtoven-2026.md...")
    fix_magnetron_frontmatter()
    
    print("\n=== DONE ===")

if __name__ == "__main__":
    main()
