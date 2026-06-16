#!/usr/bin/env python3
"""Add internal links to 7 orphan comparison articles in KiesKeuken."""

import os

REVIEWS_DIR = "/workspace/kieskeuken/src/content/reviews"

# Map orphan slug -> list of related slugs to link to
ORPHAN_LINKS = {
    "elektrische-kachel-vs-infraroodpaneel-2026": [
        "beste-elektrische-kachel-2026",
        "beste-airconditioner-2026",
        "airconditioner-vs-ventilator-2026",
        "beste-luchtbevochtiger-2026",
    ],
    "heggenschaar-vs-bosmaaier-2026": [
        "beste-heggenschaar-2026",
        "beste-bosmaaier-2026",
        "beste-grasmaaier-2026",
        "beste-bladblazer-2026",
    ],
    "ijsmachine-vs-diepvries-zelf-maken-2026": [
        "beste-ijsmachine-2026",
        "beste-koelkast-2026",
        "beste-keukenmachine-2026",
        "beste-sapcentrifuge-2026",
    ],
    "kettingzaag-vs-handzaag-2026": [
        "beste-kettingzaag-2026",
        "beste-cirkelzaag-2026",
        "beste-bosmaaier-2026",
        "beste-heggenschaar-2026",
    ],
    "pizza-oven-vs-gewone-oven-2026": [
        "beste-pizza-oven-2026",
        "beste-airfryer-oven-combi-2026",
        "beste-magnetron-2026",
        "beste-stoomoven-2026",
    ],
    "tapijtreiniger-vs-stoomreiniger-2026": [
        "beste-stoomreiniger-2026",
        "beste-stofzuiger-2026",
        "beste-steelstofzuiger-2026",
        "beste-dweilrobot-2026",
    ],
    "waterontharder-vs-ontkalker-2026": [
        "beste-waterontharder-2026",
        "beste-vaatwasser-2026",
        "beste-wasmachine-2026",
        "beste-koffiemachine-2026",
    ],
}

def get_title(slug):
    """Read the title from an article's frontmatter."""
    fpath = os.path.join(REVIEWS_DIR, f"{slug}.md")
    if not os.path.exists(fpath):
        return slug.replace("-", " ").title()
    with open(fpath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return slug.replace("-", " ").title()
    fm = parts[1]
    for line in fm.split("\n"):
        line = line.strip()
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip("'\"")
            return title
    return slug.replace("-", " ").title()

def add_related_frontmatter(filepath, related_slugs):
    """Add related: frontmatter to an article."""
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    fm_text = parts[1]
    body = parts[2]

    if "related:" in fm_text:
        return False  # Already has related

    related_block = "related:\n"
    for slug in related_slugs:
        related_block += f"  - {slug}\n"

    new_fm = fm_text.rstrip() + "\n" + related_block.rstrip()
    new_content = f"---\n{new_fm}\n---{body}"

    with open(filepath, "w") as f:
        f.write(new_content)
    return True

def add_inline_links(filepath, related_slugs):
    """Add 'Lees ook' section at end of body with inline links."""
    with open(filepath) as f:
        content = f.read()
    parts = content.split("---", 2)
    if len(parts) < 3:
        return False
    fm_text = parts[1]
    body = parts[2]

    if "Lees ook:" in body or "Gerelateerde artikelen:" in body:
        return False  # Already has inline links

    links_md = "\n\n**Lees ook:**\n"
    for slug in related_slugs:
        title = get_title(slug)
        links_md += f"- [{title}](/{slug}/)\n"

    new_body = body.rstrip() + links_md
    new_content = f"---\n{fm_text}\n---{new_body}"

    with open(filepath, "w") as f:
        f.write(new_content)
    return True

def main():
    count = 0
    for slug, related in ORPHAN_LINKS.items():
        fpath = os.path.join(REVIEWS_DIR, f"{slug}.md")
        if not os.path.exists(fpath):
            print(f"  ✗ Missing: {slug}")
            continue

        # Add related frontmatter
        fm_ok = add_related_frontmatter(fpath, related)
        # Add inline links
        body_ok = add_inline_links(fpath, related)

        if fm_ok or body_ok:
            print(f"  ✓ {slug}: related={fm_ok}, inline={body_ok}")
            count += 1
        else:
            print(f"  - {slug}: already had links")

    print(f"\nUpdated {count} articles")

if __name__ == "__main__":
    main()
