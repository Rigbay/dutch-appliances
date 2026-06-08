#!/usr/bin/env python3
"""Cross-link 6 orphaned comparison articles from Jun 7-8 batches + add reciprocal links."""

import os
import re
import sys

REVIEWS_DIR = "src/content/reviews"

# Map of orphan article slug → related slugs (individual review slugs to link to)
ORPHAN_RELATED = {
    # June 8 batch (5 articles)
    "elektrische-grasmaaier-vs-benzine-grasmaaier-2026": [
        "beste-grasmaaier-2026",
        "beste-robotgrasmaaier-2026",
        "robotgrasmaaier-vs-grasmaaier-2026",
        "beste-accu-boormachine-2026",  # tuin context
        "beste-haakse-slijper-2026",
    ],
    "robotstofzuiger-vs-steelstofzuiger-2026": [
        "beste-robotstofzuiger-2026",
        "beste-steelstofzuiger-2026",
        "beste-stofzuiger-2026",
        "beste-draadloze-stofzuiger-2026",
        "robotstofzuiger-vs-stofzuiger-2026",
        "stofzuiger-vs-steelstofzuiger-2026",
    ],
    "staafmixer-vs-blender-2026": [
        "beste-staafmixer-2026",
        "beste-blender-2026",
        "beste-handmixer-2026",
        "beste-keukenmachine-2026",
        "blender-vs-staafmixer-vs-keukenmachine-2026",
    ],
    "wasmachine-vs-wasdroger-2026": [
        "beste-wasmachine-2026",
        "beste-wasdroger-2026",
        "wasmachine-vs-wasdroger-combi-2026",
        "beste-inductiekookplaat-2026",
        "beste-keukenmachine-2026",
    ],
    "koffiemachine-vs-volautomatische-koffiemachine-2026": [
        "beste-koffiemachine-2026",
        "beste-volautomatische-koffiemachine-2026",
        "beste-koffiemachine-bonen-2026",
        "beste-espresso-apparaat-2026",
        "koffiemachine-bonen-vs-cups-2026",
        "koffiemachine-vs-senseo-2026",
    ],
    # June 7 batch — airco-vs-ventilator was the only fully orphaned one
    "airconditioner-vs-ventilator-2026": [
        "beste-airconditioner-2026",
        "beste-ventilator-2026",
        "airconditioner-vs-luchtkoeler-2026",
        "beste-luchtreiniger-2026",
        "beste-luchtbevochtiger-2026",
    ],
}

# Reciprocal: for each new comparison, add it to related arrays of individual reviews
# slug of comparison → list of individual review slugs to update
RECIPROCAL = {
    "elektrische-grasmaaier-vs-benzine-grasmaaier-2026": [
        "beste-grasmaaier-2026",
        "beste-robotgrasmaaier-2026",
    ],
    "robotstofzuiger-vs-steelstofzuiger-2026": [
        "beste-robotstofzuiger-2026",
        "beste-steelstofzuiger-2026",
        "beste-stofzuiger-2026",
    ],
    "staafmixer-vs-blender-2026": [
        "beste-staafmixer-2026",
        "beste-blender-2026",
    ],
    "wasmachine-vs-wasdroger-2026": [
        "beste-wasmachine-2026",
        "beste-wasdroger-2026",
    ],
    "koffiemachine-vs-volautomatische-koffiemachine-2026": [
        "beste-koffiemachine-2026",
        "beste-volautomatische-koffiemachine-2026",
    ],
    "airconditioner-vs-ventilator-2026": [
        "beste-airconditioner-2026",
        "beste-ventilator-2026",
    ],
}


def read_file(path):
    with open(path, "r") as f:
        return f.read()


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def add_related_array(content, slugs, max_items=6):
    """Add a `related:` YAML array before the first `---` closing frontmatter."""
    # Find the closing --- of frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  WARNING: Can't find frontmatter closing ---")
        return content

    # Check if related already exists
    if "\nrelated:" in parts[1]:
        print(f"  SKIP: related array already exists")
        return content

    slugs = slugs[:max_items]
    related_block = "\nrelated:"
    for s in slugs:
        related_block += f"\n  - {s}"

    # Insert before closing --- (inside frontmatter, after all other fields)
    parts[1] = parts[1].rstrip() + related_block + "\n"
    return "---".join(parts)


def append_to_related(content, new_slug, max_items=6):
    """Append a slug to an existing related array, capped at max_items."""
    parts = content.split("---", 2)
    if len(parts) < 3:
        return content

    fm = parts[1]
    if "\nrelated:" not in fm:
        return content

    # Check if slug already present
    if f"\n  - {new_slug}\n" in fm or f"\n  - {new_slug}" in fm:
        return content

    # Count existing related items (both indented and unindented)
    rel_section = fm.split("related:")[1]
    rel_lines = rel_section.split("\n")
    existing_count = 0
    for line in rel_lines:
        if re.match(r"^\s*-\s+\S", line):
            existing_count += 1
        elif line.strip() and not line.startswith(" ") and not line.startswith("-"):
            break  # next top-level key

    if existing_count >= max_items:
        print(f"  SKIP (reciprocal): related array already at {max_items}")
        return content

    # Find insertion point — right before the next top-level key or end of frontmatter
    # Simple approach: append at end of related block
    lines = fm.split("\n")
    new_lines = []
    in_related = False
    inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if line.startswith("related:"):
            in_related = True
            continue
        if in_related:
            if line.startswith("  - "):
                continue  # we're collecting related items
            else:
                # End of related block
                if not inserted:
                    new_lines.insert(len(new_lines) - 1, f"  - {new_slug}")
                    inserted = True
                in_related = False

    # If we never left the related block (it's at end of FM)
    if in_related and not inserted:
        new_lines.append(f"  - {new_slug}")
        inserted = True

    if inserted:
        parts[1] = "\n".join(new_lines)
        return "---".join(parts)
    return content


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    stats = {"orphan_fixed": 0, "orphan_skip": 0, "reciprocal_added": 0, "reciprocal_skip": 0}

    # Phase 1: Add related arrays to orphaned comparison articles
    print("=== Phase 1: Adding related arrays to orphaned comparisons ===")
    for slug, related_slugs in ORPHAN_RELATED.items():
        filename = f"{slug}.md"
        filepath = os.path.join(REVIEWS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  MISSING: {filename}")
            continue

        content = read_file(filepath)
        new_content = add_related_array(content, related_slugs)
        if new_content != content:
            write_file(filepath, new_content)
            print(f"  FIXED: {slug} → {len(related_slugs)} related links")
            stats["orphan_fixed"] += 1
        else:
            stats["orphan_skip"] += 1

    # Phase 2: Add reciprocal links from individual reviews → comparison articles
    print("\n=== Phase 2: Adding reciprocal links ===")
    for comp_slug, review_slugs in RECIPROCAL.items():
        for review_slug in review_slugs:
            filename = f"{review_slug}.md"
            filepath = os.path.join(REVIEWS_DIR, filename)
            if not os.path.exists(filepath):
                print(f"  MISSING: {filename} (for reciprocal from {comp_slug})")
                continue

            content = read_file(filepath)
            new_content = append_to_related(content, comp_slug)
            if new_content != content:
                write_file(filepath, new_content)
                print(f"  ADDED: {comp_slug} → {review_slug}")
                stats["reciprocal_added"] += 1
            else:
                stats["reciprocal_skip"] += 1

    print(f"\n=== Summary ===")
    print(f"Orphans fixed: {stats['orphan_fixed']}")
    print(f"Orphans skipped (already had related): {stats['orphan_skip']}")
    print(f"Reciprocal links added: {stats['reciprocal_added']}")
    print(f"Reciprocal skipped: {stats['reciprocal_skip']}")
    print(f"Total changes: {stats['orphan_fixed'] + stats['reciprocal_added']}")


if __name__ == "__main__":
    main()
