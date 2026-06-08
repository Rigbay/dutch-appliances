#!/usr/bin/env python3
"""
Deterministic inline link inserter — no API needed.
For each thin article, finds natural keyword matches in source articles and inserts a contextual link.
"""
import os, re, sys

REVIEWS_DIR = "src/content/reviews"

os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")

# Thin article → [(source_slug, keyword_to_match_in_source, link_anchor_text)]
# keyword: a Dutch phrase likely to appear in the source article
THIN_PLACEMENTS = [
    # beste-vleesmolen
    ("beste-vleesmolen-2026", "beste-keukenmachine-2026", "vlees", "onze beste vleesmolen gids"),
    ("beste-vleesmolen-2026", "hakmolen-vs-keukenmachine-2026", "vlees malen", "onze vleesmolen koopgids"),
    # stoomreiniger-vs-hogedrukreiniger
    ("stoomreiniger-vs-hogedrukreiniger-2026", "beste-stoomreiniger-2026", "hogedrukreiniger", "onze vergelijking stoomreiniger vs hogedrukreiniger"),
    ("stoomreiniger-vs-hogedrukreiniger-2026", "beste-hogedrukreiniger-2026", "stoomreiniger", "onze vergelijking stoomreiniger vs hogedrukreiniger"),
    # waterkoker-vs-quooker
    ("waterkoker-vs-quooker-2026", "beste-waterkoker-2026", "Quooker", "onze waterkoker vs Quooker vergelijking"),
    ("waterkoker-vs-quooker-2026", "beste-koffiemachine-2026", "waterkoker", "onze Quooker vs waterkoker analyse"),
    # slowcooker-vs-stoomoven
    ("slowcooker-vs-stoomoven-2026", "beste-slowcooker-2026", "stoomoven", "onze slowcooker vs stoomoven vergelijking"),
    ("slowcooker-vs-stoomoven-2026", "beste-stoomoven-2026", "slowcooker", "onze slowcooker vs stoomoven vergelijking"),
    # beste-kettingzaag
    ("beste-kettingzaag-2026", "beste-heggenschaar-2026", "kettingzaag", "onze kettingzaag koopgids"),
    ("beste-kettingzaag-2026", "beste-bosmaaier-2026", "kettingzaag", "onze volledige kettingzaag gids"),
    # beste-bakplaat
    ("beste-bakplaat-2026", "beste-gourmetstel-2026", "bakplaat", "onze bakplaat koopgids"),
    ("beste-bakplaat-2026", "beste-koekenpan-2026", "bakplaat", "onze bakplaat gids"),
    # tosti-ijzer-vs-broodrooster
    ("tosti-ijzer-vs-broodrooster-2026", "beste-tosti-ijzer-2026", "broodrooster", "onze tosti-ijzer vs broodrooster vergelijking"),
    ("tosti-ijzer-vs-broodrooster-2026", "beste-broodrooster-2026", "tosti", "onze tosti-ijzer vs broodrooster vergelijking"),
    # sapcentrifuge-vs-slowjuicer
    ("sapcentrifuge-vs-slowjuicer-2026", "beste-sapcentrifuge-2026", "slowjuicer", "onze sapcentrifuge vs slowjuicer vergelijking"),
    ("sapcentrifuge-vs-slowjuicer-2026", "beste-slowjuicer-2026", "sapcentrifuge", "onze sapcentrifuge vs slowjuicer vergelijking"),
    # beste-kruimeldief-draadloos
    ("beste-kruimeldief-draadloos-2026", "beste-steelstofzuiger-2026", "kruimeldief", "onze kruimeldief koopgids"),
    ("beste-kruimeldief-draadloos-2026", "beste-draadloze-stofzuiger-2026", "kruimeldief", "onze beste kruimeldief gids"),
    # koffiemachine-vs-senseo
    ("koffiemachine-vs-senseo-2026", "beste-koffiemachine-2026", "Senseo", "onze koffiemachine vs Senseo vergelijking"),
    ("koffiemachine-vs-senseo-2026", "beste-senseo-koffiezetapparaat-2026", "volautomatische\|filter\|bonen", "onze koffiemachine vs Senseo vergelijking"),
    # beste-koffiecupmachine
    ("beste-koffiecupmachine-2026", "beste-koffiemachine-2026", "cups\|cupmachine", "onze koffiecupmachine koopgids"),
    ("beste-koffiecupmachine-2026", "koffiemachine-bonen-vs-cups-2026", "cupmachine", "onze beste koffiecupmachine gids"),
    # beste-wafelijzer
    ("beste-wafelijzer-2026", "beste-bakplaat-2026", "wafel", "onze wafelijzer koopgids"),
    ("beste-wafelijzer-2026", "beste-tosti-ijzer-2026", "wafel", "onze wafelijzer gids"),
    # steelstofzuiger-vs-draadloze-stofzuiger
    ("steelstofzuiger-vs-draadloze-stofzuiger-2026", "beste-steelstofzuiger-2026", "draadloze stofzuiger", "onze steelstofzuiger vs draadloze stofzuiger vergelijking"),
    ("steelstofzuiger-vs-draadloze-stofzuiger-2026", "beste-draadloze-stofzuiger-2026", "steelstofzuiger", "onze steelstofzuiger vs draadloze stofzuiger vergelijking"),
    # airconditioner-vs-ventilator
    ("airconditioner-vs-ventilator-2026", "beste-airconditioner-2026", "ventilator", "onze airco vs ventilator vergelijking"),
    ("airconditioner-vs-ventilator-2026", "beste-ventilator-2026", "airconditioner\|airco", "onze airco vs ventilator vergelijking"),
    # beste-keukenmes-set
    ("beste-keukenmes-set-2026", "beste-snijplank-2026", "mes\|messen", "onze keukenmes set gids"),
    ("beste-keukenmes-set-2026", "beste-koekenpan-2026", "mes\|messen\|snijden", "onze beste keukenmes set"),
]

def read_file(slug):
    path = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return f.read()

def find_best_paragraph(body, keyword_pattern):
    """Find the paragraph in the body that best matches the keyword."""
    # Split into paragraphs (double newline)
    paragraphs = re.split(r'\n\n+', body)
    best_idx = -1
    best_count = 0

    for i, para in enumerate(paragraphs):
        # Skip short paragraphs, headers, lists
        if len(para) < 80:
            continue
        if para.strip().startswith('#'):
            continue
        if para.strip().startswith('-') or para.strip().startswith('*'):
            continue

        matches = len(re.findall(keyword_pattern, para, re.IGNORECASE))
        if matches > best_count:
            best_count = matches
            best_idx = i

    return best_idx, paragraphs

def insert_link(body, keyword_pattern, link_text, thin_slug):
    """Find a natural spot and insert an inline link. Falls back to first paragraph."""
    idx, paragraphs = find_best_paragraph(body, keyword_pattern)

    # Fallback: if no keyword match, use the first substantial paragraph
    if idx < 0:
        for i, para in enumerate(paragraphs):
            if len(para) >= 80 and not para.strip().startswith('#') and not para.strip().startswith('-'):
                idx = i
                break

    if idx < 0:
        return body, False

    para = paragraphs[idx]
    link_html = f'<a href="/{thin_slug}/">{link_text}</a>'

    # Insert a natural "Lees ook:" sentence at the end of the paragraph
    # Find the last sentence in the paragraph
    sentences = re.split(r'(?<=[.!?])\s+', para.strip())

    if len(sentences) >= 1:
        # Insert before the last sentence
        insertion = f" 📖 <strong>Lees ook:</strong> {link_html} voor een compleet overzicht van de beste opties."
        if len(sentences) >= 2:
            new_para = " ".join(sentences[:-1]) + " " + insertion + " " + sentences[-1]
        else:
            new_para = sentences[0] + " " + insertion

    paragraphs[idx] = new_para
    new_body = "\n\n".join(paragraphs)

    if new_body == body:
        return body, False

    return new_body, True

stats = {"inserted": 0, "skipped": 0, "failed": 0}

for thin_slug, source_slug, keyword, link_text in THIN_PLACEMENTS:
    source_content = read_file(source_slug)
    if not source_content:
        print(f"MISSING source: {source_slug}")
        stats["failed"] += 1
        continue

    # Skip if already linked
    if thin_slug in source_content:
        print(f"SKIP (already linked): {source_slug} → {thin_slug}")
        stats["skipped"] += 1
        continue

    # Split frontmatter and body
    parts = source_content.split("---", 2)
    if len(parts) < 3:
        print(f"SKIP (no frontmatter): {source_slug}")
        stats["failed"] += 1
        continue

    fm = "---" + parts[1] + "---"
    body = parts[2]

    new_body, changed = insert_link(body, keyword, link_text, thin_slug)

    if changed:
        new_content = fm + new_body
        filepath = os.path.join(REVIEWS_DIR, f"{source_slug}.md")
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"INSERTED: {source_slug} → {thin_slug} (keyword: '{keyword}')")
        stats["inserted"] += 1
    else:
        print(f"FAILED (no match): {source_slug} → {thin_slug} (keyword: '{keyword}')")
        stats["failed"] += 1

print(f"\n=== Summary ===")
print(f"Inserted: {stats['inserted']}")
print(f"Skipped (already linked): {stats['skipped']}")
print(f"Failed: {stats['failed']}")
