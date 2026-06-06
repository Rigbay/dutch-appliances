#!/usr/bin/env python3
"""Internal linking injector v4 — adapted for canonical clone at /home/cls/kieskeuken/"""

import re, yaml
from pathlib import Path
from collections import defaultdict

REVIEWS_DIR = Path("/home/cls/kieskeuken/src/content/reviews")
OUTPUT_DIR = Path("/home/cls/kieskeuken/internal-linking")

def build_keyword_map(existing_slugs):
    better = {
        "beste-stofzuiger-2026": [(re.compile(r'\bstofzuiger(s)?\b', re.IGNORECASE), "onze [stofzuiger gids](/beste-stofzuiger-2026/)")],
        "beste-robotstofzuiger-2026": [(re.compile(r'\brobotstofzuiger\b', re.IGNORECASE), "onze [robotstofzuiger gids](/beste-robotstofzuiger-2026/)")],
        "beste-draadloze-stofzuiger-2026": [(re.compile(r'\bdraadloze stofzuiger\b', re.IGNORECASE), "onze [draadloze stofzuiger gids](/beste-draadloze-stofzuiger-2026/)")],
        "beste-airfryer-2026": [(re.compile(r'\bairfryer\b', re.IGNORECASE), "onze [airfryer gids](/beste-airfryer-2026/)"), (re.compile(r'\bheteluchtfriteuse\b', re.IGNORECASE), "onze [airfryer gids](/beste-airfryer-2026/)")],
        "beste-wasmachine-2026": [(re.compile(r'\bwasmachine\b', re.IGNORECASE), "onze [wasmachine gids](/beste-wasmachine-2026/)")],
        "beste-wasdroger-2026": [(re.compile(r'\bwasdroger\b', re.IGNORECASE), "onze [wasdroger gids](/beste-wasdroger-2026/)")],
        "beste-vaatwasser-2026": [(re.compile(r'\bvaatwasser\b', re.IGNORECASE), "onze [vaatwasser gids](/beste-vaatwasser-2026/)")],
        "beste-koelkast-2026": [(re.compile(r'\bkoelkast\b', re.IGNORECASE), "onze [koelkast gids](/beste-koelkast-2026/)")],
        "beste-vriezer-2026": [(re.compile(r'\bvriezer\b', re.IGNORECASE), "onze [vriezer gids](/beste-vriezer-2026/)")],
        "beste-airconditioner-2026": [(re.compile(r'\bairco(n?ditioner)?\b', re.IGNORECASE), "onze [airco gids](/beste-airconditioner-2026/)")],
        "beste-grasmaaier-2026": [(re.compile(r'\bgrasmaaier\b', re.IGNORECASE), "onze [grasmaaier gids](/beste-grasmaaier-2026/)")],
        "beste-heggenschaar-2026": [(re.compile(r'\bheggenschaar\b', re.IGNORECASE), "onze [heggenschaar gids](/beste-heggenschaar-2026/)")],
        "beste-hogedrukreiniger-2026": [(re.compile(r'\bhogedrukreiniger\b', re.IGNORECASE), "onze [hogedrukreiniger gids](/beste-hogedrukreiniger-2026/)")],
        "beste-luchtreiniger-2026": [(re.compile(r'\bluchtreiniger\b', re.IGNORECASE), "onze [luchtreiniger gids](/beste-luchtreiniger-2026/)")],
        "beste-keukenmachine-2026": [(re.compile(r'\bkeukenmachine\b', re.IGNORECASE), "onze [keukenmachine gids](/beste-keukenmachine-2026/)")],
        "beste-staafmixer-2026": [(re.compile(r'\bstaafmixer\b', re.IGNORECASE), "onze [staafmixer gids](/beste-staafmixer-2026/)")],
        "beste-blender-2026": [(re.compile(r'\bblender\b', re.IGNORECASE), "onze [blender gids](/beste-blender-2026/)")],
        "beste-handmixer-2026": [(re.compile(r'\bhandmixer\b', re.IGNORECASE), "onze [handmixer gids](/beste-handmixer-2026/)")],
        "beste-broodrooster-2026": [(re.compile(r'\bbroodrooster\b', re.IGNORECASE), "onze [broodrooster gids](/beste-broodrooster-2026/)")],
        "beste-waterkoker-2026": [(re.compile(r'\bwaterkoker\b', re.IGNORECASE), "onze [waterkoker gids](/beste-waterkoker-2026/)")],
        "beste-stoomoven-2026": [(re.compile(r'\bstoomoven\b', re.IGNORECASE), "onze [stoomoven gids](/beste-stoomoven-2026/)")],
        "beste-magnetron-2026": [(re.compile(r'\bmagnetron\b', re.IGNORECASE), "onze [magnetron gids](/beste-magnetron-2026/)")],
        "beste-tosti-ijzer-2026": [(re.compile(r'\btosti\b', re.IGNORECASE), "onze [tosti-ijzer gids](/beste-tosti-ijzer-2026/)")],
        "beste-afzuigkap-2026": [(re.compile(r'\bafzuigkap\b', re.IGNORECASE), "onze [afzuigkap gids](/beste-afzuigkap-2026/)")],
        "beste-inductiekookplaat-2026": [(re.compile(r'\binductie(kookplaat)?\b', re.IGNORECASE), "onze [inductiekookplaat gids](/beste-inductiekookplaat-2026/)")],
        "beste-friteuse-2026": [(re.compile(r'\bfriteuse\b', re.IGNORECASE), "onze [friteuse gids](/beste-friteuse-2026/)")],
        "beste-slowcooker-2026": [(re.compile(r'\bslowcooker\b', re.IGNORECASE), "onze [slowcooker gids](/beste-slowcooker-2026/)")],
        "beste-dweilrobot-2026": [(re.compile(r'\bdweilrobot\b', re.IGNORECASE), "onze [dweilrobot gids](/beste-dweilrobot-2026/)")],
        "beste-steelstofzuiger-2026": [(re.compile(r'\bsteelstofzuiger\b', re.IGNORECASE), "onze [steelstofzuiger gids](/beste-steelstofzuiger-2026/)")],
        "beste-stoomreiniger-2026": [(re.compile(r'\bstoomreiniger\b', re.IGNORECASE), "onze [stoomreiniger gids](/beste-stoomreiniger-2026/)")],
        "beste-kruimeldief-2026": [(re.compile(r'\bkruimeldief\b', re.IGNORECASE), "onze [kruimeldief gids](/beste-kruimeldief-2026/)")],
        "beste-koffiemachine-2026": [(re.compile(r'\bkoffiemachine\b', re.IGNORECASE), "onze [koffiemachine gids](/beste-koffiemachine-2026/)")],
        "beste-filterkoffiemachine-2026": [(re.compile(r'\bfilterkoffie(machine)?\b', re.IGNORECASE), "onze [filterkoffiemachine gids](/beste-filterkoffiemachine-2026/)")],
        "beste-nespresso-apparaat-2026": [(re.compile(r'\b(nespresso|cupsysteem)\b', re.IGNORECASE), "onze [Nespresso gids](/beste-nespresso-apparaat-2026/)")],
        "beste-senseo-koffiezetapparaat-2026": [(re.compile(r'\bsenseo\b', re.IGNORECASE), "onze [Senseo gids](/beste-senseo-koffiezetapparaat-2026/)")],
        "beste-ontvochtiger-2026": [(re.compile(r'\bontvochtiger\b', re.IGNORECASE), "onze [ontvochtiger gids](/beste-ontvochtiger-2026/)")],
        "beste-luchtbevochtiger-2026": [(re.compile(r'\bluchtbevochtiger\b', re.IGNORECASE), "onze [luchtbevochtiger gids](/beste-luchtbevochtiger-2026/)")],
        "beste-elektrische-kachel-2026": [(re.compile(r'\belektrische kachel\b', re.IGNORECASE), "onze [elektrische kachel gids](/beste-elektrische-kachel-2026/)")],
        "beste-strijkijzer-2026": [(re.compile(r'\bstrijkijzer\b', re.IGNORECASE), "onze [strijkijzer gids](/beste-strijkijzer-2026/)")],
        "beste-koffiemolen-2026": [(re.compile(r'\bkoffiemolen\b', re.IGNORECASE), "onze [koffiemolen gids](/beste-koffiemolen-2026/)")],
        "beste-tapijtreiniger-2026": [(re.compile(r'\btapijtreiniger\b', re.IGNORECASE), "onze [tapijtreiniger gids](/beste-tapijtreiniger-2026/)")],
        "beste-bladblazer-2026": [(re.compile(r'\bbladblazer\b', re.IGNORECASE), "onze [bladblazer gids](/beste-bladblazer-2026/)")],
        "beste-bosmaaier-2026": [(re.compile(r'\bbosmaaier\b', re.IGNORECASE), "onze [bosmaaier gids](/beste-bosmaaier-2026/)")],
        "beste-oven-2026": [(re.compile(r'\boven\b', re.IGNORECASE), "onze [oven gids](/beste-oven-2026/)")],
        "beste-broodmachine-2026": [(re.compile(r'\bbroodmachine\b', re.IGNORECASE), "onze [broodmachine gids](/beste-broodmachine-2026/)")],
        "beste-keukenweegschaal-2026": [(re.compile(r'\bkeukenweegschaal\b', re.IGNORECASE), "onze [keukenweegschaal gids](/beste-keukenweegschaal-2026/)")],
        "beste-slowjuicer-2026": [(re.compile(r'\bslowjuicer\b', re.IGNORECASE), "onze [slowjuicer gids](/beste-slowjuicer-2026/)")],
        "beste-ijsmachine-2026": [(re.compile(r'\bijsmachine\b', re.IGNORECASE), "onze [ijsmachine gids](/beste-ijsmachine-2026/)")],
        "beste-pizza-oven-2026": [(re.compile(r'\bpizza.?oven\b', re.IGNORECASE), "onze [pizza oven gids](/beste-pizza-oven-2026/)")],
        "beste-wafelijzer-2026": [(re.compile(r'\bwafelijzer\b', re.IGNORECASE), "onze [wafelijzer gids](/beste-wafelijzer-2026/)")],
        "beste-schoonmaakrobot-2026": [(re.compile(r'\bschoonmaakrobot\b', re.IGNORECASE), "onze [schoonmaakrobot gids](/beste-schoonmaakrobot-2026/)")],
        "beste-robotgrasmaaier-2026": [(re.compile(r'\brobotgrasmaaier\b', re.IGNORECASE), "onze [robotgrasmaaier gids](/beste-robotgrasmaaier-2026/)")],
    }

    km = {}
    for slug in existing_slugs:
        topic = slug.replace('beste-', '').replace('-2026', '').replace('-vs-', ' ')
        words = topic.replace('-', ' ').strip()
        main = words.split()[0] if words.split() else words
        if len(main) >= 4:
            km[slug] = [(re.compile(r'\b' + re.escape(main) + r'\b', re.IGNORECASE),
                        f"onze [{words} gids](/{slug}/)")]
    km.update(better)
    return km


def parse_fm(text):
    m = re.match(r'^---\n(.*?)\n---\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    try:
        return yaml.safe_load(m.group(1)), m.group(2)
    except:
        return {}, m.group(2)


def split_body(body_text):
    parts = body_text.split('\n## Gerelateerde artikelen\n')
    return parts[0], ('\n## Gerelateerde artikelen\n' + parts[1]) if len(parts) > 1 else ''


def inside_link(text, pos):
    depth = 0
    for i, ch in enumerate(text):
        if i >= pos:
            return depth > 0
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
    return depth > 0


def inject_links(main_text, kw_map, current_slug, cat, cat_map):
    candidates = set()
    for s in cat_map.get(cat, []):
        if s != current_slug:
            candidates.add(s)
    xcat = {'beste-stofzuiger-2026', 'beste-airfryer-2026', 'beste-stoomoven-2026', 'beste-magnetron-2026'}
    candidates.update(xcat)

    matches = []
    for slug in candidates:
        if slug == current_slug or slug not in kw_map:
            continue
        for regex, anchor in kw_map[slug]:
            for m in regex.finditer(main_text):
                pos = m.start()
                if not inside_link(main_text, pos) and anchor not in main_text:
                    matches.append((pos, slug, anchor))
                    break
            break

    if not matches:
        return main_text

    matches.sort()
    seen, selected = set(), []
    for pos, slug, anchor in matches:
        if slug in seen:
            continue
        seen.add(slug)
        selected.append((pos, slug, anchor))
        if len(selected) >= 3:
            break

    for pos, slug, anchor in reversed(selected):
        end = main_text.find('.', pos)
        if end < 0 or end - pos > 200:
            end = main_text.find('\n', pos)
            if end < 0 or end - pos > 200:
                continue
        else:
            end += 1
        main_text = main_text[:end] + " " + anchor + "." + main_text[end:]

    return main_text


def main():
    articles = sorted(REVIEWS_DIR.glob("*.md"))
    existing_slugs = {fp.stem for fp in articles}
    kw_map = build_keyword_map(existing_slugs)

    cat_map = defaultdict(list)
    for fp in articles:
        content = fp.read_text(encoding='utf-8')
        fm, _ = parse_fm(content)
        cat_map[fm.get('category', 'unknown')].append(fp.stem)

    modified, total_links = 0, 0
    link_log = []

    for fp in articles:
        slug = fp.stem
        content = fp.read_text(encoding='utf-8')
        fm, body = parse_fm(content)
        cat = fm.get('category', 'unknown')

        main, rest = split_body(body)
        new_main = inject_links(main, kw_map, slug, cat, cat_map)
        if new_main != main:
            body = new_main + rest
            old_links = len(re.findall(r'\[[^\]]+\]\(/[^)]+\)', main))
            new_links = len(re.findall(r'\[[^\]]+\]\(/[^)]+\)', new_main))
            added = max(0, new_links - old_links)
            total_links += added

            fm_text = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False).strip()
            new_content = f"---\n{fm_text}\n---\n{body}"
            fp.write_text(new_content, encoding='utf-8')
            modified += 1

            # Log what was added
            new_only = re.findall(r'\[([^\]]+)\]\(/[^)]+\)', new_main)
            old_only = set(re.findall(r'\[([^\]]+)\]\(/[^)]+\)', main))
            added_anchors = [a for a in new_only if a not in old_only]
            link_log.append(f"- **{slug}**: +{added} links → {', '.join(added_anchors[:5])}")

    # Write report
    report = f"""# Internal Linking Report — {modified}/{len(articles)} articles updated

**Total links added:** {total_links}

## Articles modified:
{chr(10).join(link_log) if link_log else '_No articles needed links._'}
"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "links-added.md").write_text(report)

    print(f"Done. Modified: {modified}/{len(articles)}, Links added: {total_links}")


if __name__ == "__main__":
    main()
