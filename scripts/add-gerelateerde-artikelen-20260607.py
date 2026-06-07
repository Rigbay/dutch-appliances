#!/usr/bin/env python3
"""Add 'Gerelateerde artikelen' sections to 8 orphaned KiesKeuken articles from June 7 batch."""

import os, re

REVIEWS_DIR = "src/content/reviews"

RELATED = {
    "airconditioner-vs-ventilator-2026": [
        ("/reviews/beste-airconditioner-2026/", "Beste airconditioner 2026: koopgids voor mobiele en split-unit airco's"),
        ("/reviews/airconditioner-vs-luchtkoeler-2026/", "Airconditioner vs luchtkoeler: welke past bij jouw situatie?"),
        ("/reviews/beste-ventilator-2026/", "Beste ventilator 2026: plafond, tafel, toren en vloerventilatoren vergeleken"),
        ("/reviews/beste-elektrische-kachel-2026/", "Beste elektrische kachel 2026: efficiënt verwarmen zonder gas"),
    ],
    "beste-bruiswaterapparaat-2026": [
        ("/reviews/beste-blender-2026/", "Beste blender 2026: smoothies, sauzen en soepen in één apparaat"),
        ("/reviews/beste-waterkoker-2026/", "Beste waterkoker 2026: snel, zuinig en stijlvol"),
        ("/reviews/beste-sapcentrifuge-2026/", "Beste sapcentrifuge 2026: vers sap op de juiste snelheid"),
        ("/reviews/beste-citruspers-2026/", "Beste citruspers 2026: elektrisch vs handmatig verse sinaasappelsap"),
    ],
    "beste-elektrische-deken-2026": [
        ("/reviews/beste-elektrische-kachel-2026/", "Beste elektrische kachel 2026: efficiënt verwarmen zonder gas"),
        ("/reviews/beste-strijkijzer-2026/", "Beste strijkijzer 2026: stoomgenerator vs traditioneel vergeleken"),
        ("/reviews/beste-wasmachine-2026/", "Beste wasmachine 2026: koopgids voor elk budget en huishouden"),
        ("/reviews/beste-wasdroger-2026/", "Beste wasdroger 2026: warmtepomp vs condensdroger vergeleken"),
    ],
    "beste-gourmetstel-2026": [
        ("/reviews/beste-bakplaat-2026/", "Beste bakplaat 2026: perfect voor pannenkoeken, vlees en vis"),
        ("/reviews/beste-friteuse-2026/", "Beste friteuse 2026: hetelucht vs traditioneel frituren vergeleken"),
        ("/reviews/beste-barbecue-2026/", "Beste barbecue 2026: gas, houtskool of elektrisch — welke kies jij?"),
        ("/reviews/beste-koekenpan-2026/", "Beste koekenpan 2026: anti-aanbak, RVS, gietijzer en keramisch vergeleken"),
    ],
    "cirkelzaag-vs-decoupeerzaag-2026": [
        ("/reviews/beste-cirkelzaag-2026/", "Beste cirkelzaag 2026: handcirkelzagen, tafelcirkelzagen en afkortzagen"),
        ("/reviews/beste-decoupeerzaag-2026/", "Beste decoupeerzaag 2026: de ultieme gids voor figuurzagen"),
        ("/reviews/beste-bosmaaier-2026/", "Beste bosmaaier 2026: borstmaaier, bosmaaier op accu en benzine vergeleken"),
        ("/reviews/beste-haakse-slijper-2026/", "Beste haakse slijper 2026: doorslijpen, slijpen en polijsten"),
    ],
    "hakmolen-vs-keukenmachine-2026": [
        ("/reviews/beste-keukenmachine-2026/", "Beste keukenmachine 2026: kneed, klop en mix als een professionele bakker"),
        ("/reviews/beste-hakmolen-2026/", "Beste hakmolen 2026: uien, noten en kruiden in seconden fijn"),
        ("/reviews/beste-blender-2026/", "Beste blender 2026: smoothies, sauzen en soepen in één apparaat"),
        ("/reviews/beste-staafmixer-2026/", "Beste staafmixer 2026: soepen pureren en sauzen mixen direct in de pan"),
    ],
    "koekenpan-vs-braadpan-2026": [
        ("/reviews/beste-koekenpan-2026/", "Beste koekenpan 2026: anti-aanbak, RVS, gietijzer en keramisch vergeleken"),
        ("/reviews/beste-braadpan-2026/", "Beste braadpan 2026: gietijzer, emaille en RVS voor stoof- en braadgerechten"),
        ("/reviews/beste-bakplaat-2026/", "Beste bakplaat 2026: perfect voor pannenkoeken, vlees en vis"),
        ("/reviews/beste-inductiekookplaat-2026/", "Beste inductiekookplaat 2026: snel, zuinig en veilig koken"),
    ],
    "koelkast-vs-koelvriescombinatie-2026": [
        ("/reviews/beste-koelkast-2026/", "Beste koelkast 2026: tafelmodel, vrijstaand en Amerikaanse koelkasten"),
        ("/reviews/beste-vriezer-2026/", "Beste vriezer 2026: tafelmodel, kastmodel en NoFrost vriezers vergeleken"),
        ("/reviews/beste-vaatwasser-2026/", "Beste vaatwasser 2026: inbouw, vrijstaand en compact vergeleken"),
        ("/reviews/beste-magnetron-2026/", "Beste magnetron 2026: solo, combi en grill magnetrons voor elke keuken"),
    ],
}

count = 0
for slug, links in RELATED.items():
    filepath = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(filepath):
        print(f"  ✗ NOT FOUND: {slug}")
        continue

    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    if "Gerelateerde artikelen" in content:
        print(f"  - SKIP (already has): {slug}")
        continue

    # Build the section
    section = "\n## Gerelateerde artikelen\n\n"
    for url, title in links:
        section += f"- [{title}]({url})\n"

    # Append to end of file (after final content)
    content = content.rstrip() + "\n" + section

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✓ ADDED: {slug} (+{len(links)} links)")
    count += 1

print(f"\n=== Done: {count}/8 articles updated ===")
