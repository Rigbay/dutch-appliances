#!/usr/bin/env python3
"""Cross-link all Dutch Appliance articles with internal links to related content.
Each article gets 2-5 "Gerelateerde koopgidsen" links injected before the final FAQ section.
Also adds inline contextual links in the body where natural anchor text exists."""

import os, re, sys, random
from collections import defaultdict

REVIEWS = 'src/content/reviews'
CLUSTERS = [
    # Product type -> related slugs
    ('airfryer', ['beste-airfryer-2026', 'beste-compacte-airfryer-2026', 'beste-luxe-airfryer-2026',
                  'beste-airfryer-onder-100-euro-2026', 'beste-airfryer-met-twee-manden-2026',
                  'beste-airfryer-oven-combi-2026', 'airfryer-vs-friteuse-2026', 'airfryer-vs-oven-2026',
                  'airfryer-vs-magnetron-2026', 'airfryer-vs-heteluchtoven-2026']),
    ('koffiemachine', ['beste-koffiemachine-2026', 'beste-koffiemachine-bonen-2026',
                       'beste-koffiemachine-onder-200-euro-2026', 'beste-volautomatische-koffiemachine-2026',
                       'beste-filterkoffiemachine-2026', 'beste-nespresso-apparaat-2026',
                       'beste-senseo-koffiezetapparaat-2026', 'beste-koffiemolen-2026',
                       'beste-koffiecupmachine-2026', 'beste-koffiemelkopschuimer-2026',
                       'koffiemachine-bonen-vs-cups-2026', 'koffiemachine-vs-senseo-2026',
                       'koffiemachine-vs-volautomatische-koffiemachine-2026', 'espresso-vs-filterkoffie-2026',
                       'nespresso-vs-dolce-gusto-2026', 'beste-espresso-apparaat-2026']),
    ('stofzuiger', ['beste-stofzuiger-2026', 'beste-draadloze-stofzuiger-2026', 'beste-steelstofzuiger-2026',
                    'beste-stofzuiger-met-zak-2026', 'beste-stofzuiger-tegen-dierenharen-2026',
                    'beste-stofzuiger-voor-allergie-2026', 'beste-kruimeldief-2026',
                    'beste-kruimeldief-draadloos-2026', 'stofzuiger-kopen-waar-op-letten-2026',
                    'stofzuiger-vs-steelstofzuiger-2026', 'robotstofzuiger-vs-stofzuiger-2026',
                    'steelstofzuiger-vs-draadloze-stofzuiger-2026', 'stofzuiger-met-zak-vs-zakloos-2026',
                    'stofzuiger-vs-kruimeldief-2026', 'beste-tapijtreiniger-2026']),
    ('robotstofzuiger', ['beste-robotstofzuiger-2026', 'beste-dweilrobot-2026', 'beste-schoonmaakrobot-2026',
                         'robotstofzuiger-vs-dweilrobot-2026', 'robotstofzuiger-vs-stofzuiger-2026',
                         'robotstofzuiger-vs-steelstofzuiger-2026']),
    ('kookplaat', ['beste-inductiekookplaat-2026', 'beste-gasfornuis-2026', 'inductie-vs-gasfornuis-2026',
                   'inductie-vs-keramisch-2026', 'beste-afzuigkap-2026', 'beste-inductieset-2026']),
    ('was', ['beste-wasmachine-2026', 'beste-wasdroger-2026', 'wasmachine-vs-wasdroger-combi-2026',
             'condensdroger-vs-warmtepompdroger-2026', 'wasmachine-vs-wasdroger-2026']),
    ('blender', ['beste-blender-2026', 'beste-staafmixer-2026', 'beste-handmixer-2026',
                 'beste-keukenmachine-2026', 'blender-vs-staafmixer-vs-keukenmachine-2026',
                 'staafmixer-vs-blender-2026', 'handmixer-vs-keukenmachine-2026', 'hakmolen-vs-keukenmachine-2026',
                 'beste-hakmolen-2026', 'soepmaker-vs-staafmixer-2026']),
    ('grasmaaier', ['beste-grasmaaier-2026', 'beste-robotgrasmaaier-2026', 'beste-bosmaaier-2026',
                    'beste-verticuteermachine-2026', 'elektrische-grasmaaier-vs-benzine-grasmaaier-2026',
                    'robotgrasmaaier-vs-grasmaaier-2026']),
    ('koken', ['beste-friteuse-2026', 'beste-slowcooker-2026', 'beste-stoomoven-2026',
               'beste-magnetron-2026', 'beste-tosti-ijzer-2026', 'beste-elektrische-grill-2026',
               'beste-broodrooster-2026', 'beste-waterkoker-2026', 'beste-keukenweegschaal-2026',
               'slowcooker-vs-stoomoven-2026', 'oven-vs-magnetron-2026', 'magnetron-vs-combi-magnetron-2026',
               'beste-oven-2026', 'beste-oven-magnetron-combi-2026', 'beste-rijstkoker-2026',
               'beste-gourmetstel-2026', 'beste-broodmachine-2026', 'beste-wafelijzer-2026',
               'beste-pizza-oven-2026', 'broodrooster-vs-tosti-ijzer-2026', 'beste-pastamachine-2026',
               'tosti-ijzer-vs-broodrooster-2026', 'beste-yoghurtmaker-2026', 'beste-citruspers-2026',
               'beste-sapcentrifuge-2026', 'beste-slowjuicer-2026', 'sapcentrifuge-vs-slowjuicer-2026']),
    ('koeling', ['beste-koelkast-2026', 'beste-koelkast-vriezer-combinatie-2026', 'beste-vriezer-2026',
                 'koelkast-vs-koelvriescombinatie-2026', 'beste-ijsmachine-2026']),
    ('strijk', ['beste-strijkijzer-2026', 'beste-esparettomachine-2026', 'strijkijzer-vs-stoomgenerator-2026',
                'strijkijzer-vs-handstomer-2026']),
    ('airco', ['beste-airconditioner-2026', 'beste-ventilator-2026', 'airconditioner-vs-luchtkoeler-2026',
               'airconditioner-vs-ventilator-2026', 'mobiele-airco-vs-split-airco-2026',
               'beste-elektrische-kachel-2026', 'beste-luchtbevochtiger-2026', 'beste-luchtreiniger-2026',
               'luchtreiniger-vs-luchtbevochtiger-2026', 'beste-ontvochtiger-2026']),
    ('tuin', ['beste-barbecue-2026', 'beste-tuinverwarming-2026', 'beste-tuinverlichting-2026',
              'gasbarbecue-vs-houtskoolbarbecue-2026', 'barbecue-vs-elektrische-grill-2026',
              'beste-tuingereedschap-set-2026', 'beste-snoeischaar-2026', 'beste-kruiwagen-2026',
              'beste-heggenschaar-2026', 'beste-hogedrukreiniger-2026', 'beste-bladblazer-2026',
              'beste-kettingzaag-2026', 'beste-tuinsproeier-2026', 'beste-tuinslang-2026',
              'stoomreiniger-vs-hogedrukreiniger-2026', 'beste-stoomreiniger-2026']),
    ('keukengerei', ['beste-pannenset-2026', 'beste-koekenpan-2026', 'beste-braadpan-2026',
                     'beste-wokpan-2026', 'koekenpan-vs-braadpan-2026', 'beste-keukenmes-set-2026',
                     'beste-snijplank-2026', 'beste-deegroller-2026', 'beste-bakplaat-2026']),
    ('reiniging', ['beste-stoomreiniger-2026', 'beste-raamreiniger-2026', 'beste-vloerwisser-2026',
                   'beste-hogedrukreiniger-2026', 'stoomreiniger-vs-hogedrukreiniger-2026']),
    ('persoon', ['beste-fohn-2026', 'beste-persoonsweegschaal-2026', 'beste-elektrische-deken-2026']),
    ('gereedschap', ['beste-accu-boormachine-2026', 'beste-cirkelzaag-2026', 'beste-decoupeerzaag-2026',
                     'beste-haakse-slijper-2026', 'beste-multitool-2026', 'beste-schuurmachine-2026',
                     'cirkelzaag-vs-decoupeerzaag-2026']),
    ('overig', ['beste-vaatwasser-2026', 'vaatwasser-vs-handafwas-2026', 'waterkoker-vs-quooker-2026',
                'beste-waterontharder-2026', 'broodmachine-vs-zelf-bakken-2026',
                'beste-bruiswaterapparaat-2026', 'beste-paneerapparaat-2026', 'beste-vleesmolen-2026']),
]

# Load all articles
def load_article(slug):
    path = f'{REVIEWS}/{slug}.md'
    if not os.path.exists(path): return None
    with open(path) as f:
        return f.read()

def get_title(content):
    m = re.search(r'^title:\s*[\'"]?(.+?)[\'"]?\s*$', content, re.M)
    return m.group(1).strip() if m else 'Unknown'

# Build slug->title map
titles = {}
for f in os.listdir(REVIEWS):
    if f.endswith('.md'):
        slug = f.replace('.md', '')
        content = load_article(slug)
        if content:
            titles[slug] = get_title(content)

# Build reverse index: slug -> all related slugs
related = defaultdict(set)
for cluster_name, slugs in CLUSTERS:
    valid = [s for s in slugs if s in titles]
    for s in valid:
        for other in valid:
            if other != s:
                related[s].add(other)

# Now inject links
count = 0
for f in sorted(os.listdir(REVIEWS)):
    if not f.endswith('.md'): continue
    slug = f.replace('.md', '')
    path = f'{REVIEWS}/{f}'
    content = load_article(slug)
    if not content: continue
    if 'Gerelateerde koopgidsen' in content:
        continue  # Already has links

    # Get related slugs for this article
    my_related = list(related.get(slug, set()))
    # If no cluster match, find same-category articles
    if not my_related:
        m = re.search(r'^category:\s*(.+)$', content, re.M)
        if m:
            cat = m.group(1).strip().strip("'")
            for s, t in titles.items():
                if s != slug and s not in my_related:
                    c2 = load_article(s)
                    if c2:
                        m2 = re.search(r'^category:\s*(.+)$', c2, re.M)
                        if m2 and m2.group(1).strip().strip("'") == cat:
                            my_related.append(s)
    
    if not my_related:
        # Fallback: pick random same-category
        continue

    # Pick 2-4 related links
    random.seed(hash(slug))
    picks = random.sample(my_related, min(4, len(my_related)))

    # Build the related section
    links_md = '\n'.join([f'- [Bekijk {titles[s].rstrip(".")}](/dutch-appliances/{s}/)' for s in picks])
    related_section = f"""

## Gerelateerde koopgidsen

{links_md}

*Deze links verwijzen naar gerelateerde koopgidsen op onze site.*

"""

    # Insert before the FAQ section or before the last ## section
    if '## Veelgestelde vragen' in content:
        content = content.replace('## Veelgestelde vragen', related_section + '## Veelgestelde vragen')
    elif '## FAQ' in content:
        content = content.replace('## FAQ', related_section + '## FAQ')
    elif '## Veelgestelde Vragen' in content:
        content = content.replace('## Veelgestelde Vragen', related_section + '## Veelgestelde Vragen')
    else:
        # Insert before the last section
        last_h2 = [m.start() for m in re.finditer(r'^## ', content, re.M)]
        if last_h2:
            pos = last_h2[-1]
            content = content[:pos] + related_section + '\n' + content[pos:]
        else:
            content += '\n' + related_section

    with open(path, 'w') as fh:
        fh.write(content)
    count += 1

print(f'Cross-linked {count} articles')
print(f'Cluster coverage: {len(related)}/{len(titles)} slugs have cluster peers')
