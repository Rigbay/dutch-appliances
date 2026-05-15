#!/usr/bin/env python3
"""Internal linking injector v3 — category-aware, fixes dead related slugs, adds body links."""

import re, yaml
from pathlib import Path
from collections import defaultdict

REVIEWS_DIR = Path("/workspace/agent-workspace/scripts/missions/passive-income/dutch-appliances-site/src/content/reviews")
OUTPUT_FILE = Path("/workspace/agent-workspace/scripts/missions/passive-income/dutch-appliances-site/internal-linking/links-added.md")

def build_keyword_map(existing_slugs):
    overrides = {
        "best-bladblazer-2026": [r"\bbladblazer\b", "onze [bladblazer gids](/reviews/beste-bladblazer-2026/)"],
        "beste-afzuigkap-2026": [r"\bafzuigkap\b", "onze [afzuigkap gids](/reviews/beste-afzuigkap-2026/)"],
        "best-robotstofzuiger-2026": [r"\brobotstofzuiger\b", "onze [robotstofzuiger gids](/reviews/beste-robotstofzuiger-2026/)"],  
    }
    
    # Auto-generate for all slugs: match main topic word
    km = {}
    for slug in existing_slugs:
        topic = slug.replace('beste-', '').replace('-2026', '').replace('-vs-', ' ')
        words = topic.replace('-', ' ').strip()
        main = words.split()[0] if words.split() else words
        if len(main) >= 4:
            km[slug] = [(re.compile(r'\b' + re.escape(main) + r'\b', re.IGNORECASE), 
                        f"onze [{words} gids](/reviews/{slug}/)")]
    
    # Override with better anchors
    better = {
        "beste-stofzuiger-2026": [(re.compile(r'\bstofzuiger(s)?\b', re.IGNORECASE), "onze [stofzuiger gids](/reviews/beste-stofzuiger-2026/)")],
        "beste-robotstofzuiger-2026": [(re.compile(r'\brobotstofzuiger\b', re.IGNORECASE), "onze [robotstofzuiger gids](/reviews/beste-robotstofzuiger-2026/)")],
        "beste-draadloze-stofzuiger-2026": [(re.compile(r'\bdraadloze stofzuiger\b', re.IGNORECASE), "onze [draadloze stofzuiger gids](/reviews/beste-draadloze-stofzuiger-2026/)")],
        "beste-airfryer-2026": [(re.compile(r'\bairfryer\b', re.IGNORECASE), "onze [airfryer gids](/reviews/beste-airfryer-2026/)"), (re.compile(r'\bheteluchtfriteuse\b', re.IGNORECASE), "onze [airfryer gids](/reviews/beste-airfryer-2026/)")],
        "beste-wasmachine-2026": [(re.compile(r'\bwasmachine\b', re.IGNORECASE), "onze [wasmachine gids](/reviews/beste-wasmachine-2026/)")],
        "beste-wasdroger-2026": [(re.compile(r'\bwasdroger\b', re.IGNORECASE), "onze [wasdroger gids](/reviews/beste-wasdroger-2026/)")],
        "beste-vaatwasser-2026": [(re.compile(r'\bvaatwasser\b', re.IGNORECASE), "onze [vaatwasser gids](/reviews/beste-vaatwasser-2026/)")],
        "beste-koelkast-2026": [(re.compile(r'\bkoelkast\b', re.IGNORECASE), "onze [koelkast gids](/reviews/beste-koelkast-2026/)")],
        "beste-vriezer-2026": [(re.compile(r'\bvriezer\b', re.IGNORECASE), "onze [vriezer gids](/reviews/beste-vriezer-2026/)")],
        "beste-airconditioner-2026": [(re.compile(r'\bairco(n?ditioner)?\b', re.IGNORECASE), "onze [airco gids](/reviews/beste-airconditioner-2026/)")],
        "beste-grasmaaier-2026": [(re.compile(r'\bgrasmaaier\b', re.IGNORECASE), "onze [grasmaaier gids](/reviews/beste-grasmaaier-2026/)")],
        "beste-heggenschaar-2026": [(re.compile(r'\bheggenschaar\b', re.IGNORECASE), "onze [heggenschaar gids](/reviews/beste-heggenschaar-2026/)")],
        "beste-hogedrukreiniger-2026": [(re.compile(r'\bhogedrukreiniger\b', re.IGNORECASE), "onze [hogedrukreiniger gids](/reviews/beste-hogedrukreiniger-2026/)")],
        "beste-luchtreiniger-2026": [(re.compile(r'\bluchtreiniger\b', re.IGNORECASE), "onze [luchtreiniger gids](/reviews/beste-luchtreiniger-2026/)")],
        "beste-keukenmachine-2026": [(re.compile(r'\bkeukenmachine\b', re.IGNORECASE), "onze [keukenmachine gids](/reviews/beste-keukenmachine-2026/)")],
        "beste-staafmixer-2026": [(re.compile(r'\bstaafmixer\b', re.IGNORECASE), "onze [staafmixer gids](/reviews/beste-staafmixer-2026/)")],
        "beste-blender-2026": [(re.compile(r'\bblender\b', re.IGNORECASE), "onze [blender gids](/reviews/beste-blender-2026/)")],
        "beste-handmixer-2026": [(re.compile(r'\bhandmixer\b', re.IGNORECASE), "onze [handmixer gids](/reviews/beste-handmixer-2026/)")],
        "beste-broodrooster-2026": [(re.compile(r'\bbroodrooster\b', re.IGNORECASE), "onze [broodrooster gids](/reviews/beste-broodrooster-2026/)")],
        "beste-waterkoker-2026": [(re.compile(r'\bwaterkoker\b', re.IGNORECASE), "onze [waterkoker gids](/reviews/beste-waterkoker-2026/)")],
        "beste-stoomoven-2026": [(re.compile(r'\bstoomoven\b', re.IGNORECASE), "onze [stoomoven gids](/reviews/beste-stoomoven-2026/)")],
        "beste-magnetron-2026": [(re.compile(r'\bmagnetron\b', re.IGNORECASE), "onze [magnetron gids](/reviews/beste-magnetron-2026/)")],
        "beste-tosti-ijzer-2026": [(re.compile(r'\btosti\b', re.IGNORECASE), "onze [tosti-ijzer gids](/reviews/beste-tosti-ijzer-2026/)")],
        "beste-afzuigkap-2026": [(re.compile(r'\bafzuigkap\b', re.IGNORECASE), "onze [afzuigkap gids](/reviews/beste-afzuigkap-2026/)")],
        "beste-inductiekookplaat-2026": [(re.compile(r'\binductie(kookplaat)?\b', re.IGNORECASE), "onze [inductiekookplaat gids](/reviews/beste-inductiekookplaat-2026/)")],
        "beste-friteuse-2026": [(re.compile(r'\bfriteuse\b', re.IGNORECASE), "onze [friteuse gids](/reviews/beste-friteuse-2026/)")],
        "beste-slowcooker-2026": [(re.compile(r'\bslowcooker\b', re.IGNORECASE), "onze [slowcooker gids](/reviews/beste-slowcooker-2026/)")],
        "beste-dweilrobot-2026": [(re.compile(r'\bdweilrobot\b', re.IGNORECASE), "onze [dweilrobot gids](/reviews/beste-dweilrobot-2026/)")],
        "beste-steelstofzuiger-2026": [(re.compile(r'\bsteelstofzuiger\b', re.IGNORECASE), "onze [steelstofzuiger gids](/reviews/beste-steelstofzuiger-2026/)")],
        "beste-stoomreiniger-2026": [(re.compile(r'\bstoomreiniger\b', re.IGNORECASE), "onze [stoomreiniger gids](/reviews/beste-stoomreiniger-2026/)")],
        "beste-kruimeldief-2026": [(re.compile(r'\bkruimeldief\b', re.IGNORECASE), "onze [kruimeldief gids](/reviews/beste-kruimeldief-2026/)")],
        "beste-koffiemachine-2026": [(re.compile(r'\bkoffiemachine\b', re.IGNORECASE), "onze [koffiemachine gids](/reviews/beste-koffiemachine-2026/)")],
        "beste-filterkoffiemachine-2026": [(re.compile(r'\bfilterkoffie(machine)?\b', re.IGNORECASE), "onze [filterkoffiemachine gids](/reviews/beste-filterkoffiemachine-2026/)")],
        "beste-nespresso-apparaat-2026": [(re.compile(r'\b(nespresso|cupsysteem)\b', re.IGNORECASE), "onze [Nespresso gids](/reviews/beste-nespresso-apparaat-2026/)")],
        "beste-senseo-koffiezetapparaat-2026": [(re.compile(r'\bsenseo\b', re.IGNORECASE), "onze [Senseo gids](/reviews/beste-senseo-koffiezetapparaat-2026/)")],
        "beste-ontvochtiger-2026": [(re.compile(r'\bontvochtiger\b', re.IGNORECASE), "onze [ontvochtiger gids](/reviews/beste-ontvochtiger-2026/)")],
        "beste-luchtbevochtiger-2026": [(re.compile(r'\bluchtbevochtiger\b', re.IGNORECASE), "onze [luchtbevochtiger gids](/reviews/beste-luchtbevochtiger-2026/)")],
        "beste-elektrische-kachel-2026": [(re.compile(r'\belektrische kachel\b', re.IGNORECASE), "onze [elektrische kachel gids](/reviews/beste-elektrische-kachel-2026/)")],
        "beste-strijkijzer-2026": [(re.compile(r'\bstrijkijzer\b', re.IGNORECASE), "onze [strijkijzer gids](/reviews/beste-strijkijzer-2026/)")],
        "beste-koffiemolen-2026": [(re.compile(r'\bkoffiemolen\b', re.IGNORECASE), "onze [koffiemolen gids](/reviews/beste-koffiemolen-2026/)")],
        "beste-tapijtreiniger-2026": [(re.compile(r'\btapijtreiniger\b', re.IGNORECASE), "onze [tapijtreiniger gids](/reviews/beste-tapijtreiniger-2026/)")],
        "beste-bladblazer-2026": [(re.compile(r'\bbladblazer\b', re.IGNORECASE), "onze [bladblazer gids](/reviews/beste-bladblazer-2026/)")],
        "beste-bosmaaier-2026": [(re.compile(r'\bbosmaaier\b', re.IGNORECASE), "onze [bosmaaier gids](/reviews/beste-bosmaaier-2026/)")],
    }
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

def inject_links(main_text, kw_map, existing_slugs, current_slug, cat, cat_map):
    """Find and inject 2-3 contextual links."""
    # Priority 1: related slugs from the article's frontmatter
    candidates = set()
    # Priority 2: same category slugs
    for s in cat_map.get(cat, []):
        if s != current_slug:
            candidates.add(s)
    # Priority 3: popular cross-category slugs
    xcat = {'beste-stofzuiger-2026', 'beste-airfryer-2026', 'beste-stoomoven-2026', 'beste-magnetron-2026'}
    candidates.update(xcat)
    
    matches = []
    for slug in candidates:
        if slug == current_slug or slug not in kw_map:
            continue
        for regex, anchor in kw_map[slug]:
            for m in regex.finditer(main_text):
                pos = m.start()
                if not inside_link(main_text, pos):
                    matches.append((pos, slug, anchor))
                    break  # one match per slug
            break  # one regex entry per slug
    
    if not matches:
        return main_text
    
    # Deduplicate, keep top 3 earliest
    matches.sort()
    seen, selected = set(), []
    for pos, slug, anchor in matches:
        if slug in seen:
            continue
        seen.add(slug)
        selected.append((pos, slug, anchor))
        if len(selected) >= 3:
            break
    
    # Insert from end to start
    for pos, slug, anchor in reversed(selected):
        # Find end of sentence containing this match
        end = main_text.find('.', pos)
        if end < 0 or end - pos > 200:
            end = main_text.find('\n', pos)
            if end < 0 or end - pos > 200:
                continue
        else:
            end += 1  # include period
        
        main_text = main_text[:end] + " " + anchor + "." + main_text[end:]
    
    return main_text

def fix_dead_related(fm, existing_slugs, cat_map, current_slug):
    """Replace hallucinated related slugs with real same-category ones."""
    related = fm.get('related', [])
    if not related:
        return False
    valid = [r for r in related if r in existing_slugs]
    if valid:
        return False  # at least one real slug — keep
    # All dead — replace
    cat = fm.get('category', 'keuken')
    same_cat = [s for s in cat_map.get(cat, []) if s != current_slug][:5]
    if len(same_cat) >= 2:
        fm['related'] = same_cat[:3]
        return True
    return False

def main():
    articles = sorted(REVIEWS_DIR.glob("*.md"))
    existing_slugs = {fp.stem for fp in articles}
    kw_map = build_keyword_map(existing_slugs)
    
    # Category map
    cat_map = defaultdict(list)
    for fp in articles:
        content = fp.read_text(encoding='utf-8')
        fm, _ = parse_fm(content)
        cat_map[fm.get('category', 'unknown')].append(fp.stem)
    
    modified, total_links, fixed_related = 0, 0, 0
    
    for fp in articles:
        slug = fp.stem
        content = fp.read_text(encoding='utf-8')
        fm, body = parse_fm(content)
        cat = fm.get('category', 'unknown')
        
        change = False
        added = 0
        
        # Fix dead related slugs
        if fix_dead_related(fm, existing_slugs, cat_map, slug):
            fixed_related += 1
            change = True
        
        # Inject contextual links in body (not Gerelateerde section)
        main, rest = split_body(body)
        new_main = inject_links(main, kw_map, existing_slugs, slug, cat, cat_map)
        if new_main != main:
            body = new_main + rest
            change = True
            old_links = len(re.findall(r'\[[^\]]+\]\(/reviews/[^)]+\)', main))
            new_links = len(re.findall(r'\[[^\]]+\]\(/reviews/[^)]+\)', new_main))
            added = max(0, new_links - old_links)
            total_links += added
        
        if change:
            fm_text = yaml.dump(fm, allow_unicode=True, default_flow_style=False, sort_keys=False).strip()
            new_content = f"---\n{fm_text}\n---\n{body}"
            fp.write_text(new_content, encoding='utf-8')
            modified += 1
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(f"# Internal Linking Results (v3)\n\nModified: {modified}/{len(articles)}\nLinks added: {total_links}\nRelated slugs fixed: {fixed_related}\n")
    
    print(f"Done. Modified: {modified}/{len(articles)}, Links: {total_links}, Related-fixed: {fixed_related}")

if __name__ == "__main__":
    main()
