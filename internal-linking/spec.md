# Internal Linking Implementation Spec

**Mission:** Add contextual body-text internal links across all 62 Dutch appliance review articles.
**Delegation:** Implementation only — Hermes decides what + why, Codex does how.

## Problem

The site has 62 articles with `related` frontmatter arrays (2-3 related slugs per article) and some have a "Gerelateerde artikelen" section at the bottom with markdown links. But **NO articles have contextual mid-body cross-references** (e.g., "zoals we bespraken in onze [airfryer gids](/reviews/beste-airfryer-2026/)").

This is the #1 SEO gap remaining after the May 15 schema/robots.txt fix batch. The KündigungExpress case study (0→8,500 impressions in 10 weeks) listed internal linking as a top-3 growth driver. Google uses internal link context to understand topical authority and content relationships.

## What to Do

For each of the 62 articles in `src/content/reviews/*.md`, add 2-4 contextual body-text links to related articles. These should:

1. **Be in the body text** (after the `---` frontmatter), not just the "Gerelateerde artikelen" section
2. **Use natural Dutch anchor text** that describes what the linked article covers (NOT generic "lees hier" / "klik hier")
3. **Make logical sense in context** — the link should be inserted where the topic naturally comes up
4. **NOT break the article structure** — don't modify frontmatter, product lists, or existing markdown formatting

## Article Structure

Articles are at: `/home/cls/clawd/scripts/missions/passive-income/dutch-appliances-site/src/content/reviews/*.md`

Each article has:
- YAML frontmatter (between `---` lines) with a `related` array of 2-3 slugs
- Body text in markdown with sections like: `## Snel advies`, `## Beste keuze per budget`, `## Waar moet je op letten?`, `## Bekende minpunten`, `## Gerelateerde artikelen`

The `related` array in frontmatter already maps related articles — use these as the primary link targets. Example: `beste-airfryer-2026.md` has `related: ["beste-magnetron-2026", "beste-waterkoker-2026", "beste-stoomoven-2026"]`.

## Linking Categories by Article Topic

Group articles by category + semantic overlap. Examples:

**Keuken (kitchen):** airfryer, friteuse, blender, broodrooster, citruspers, filterkoffiemachine, handmixer, inductiekookplaat, keukenmachine, koelkast, koelkast-vriezer-combinatie, koffiemachine (all variants), koffiemolen, magnetron, nespresso-apparaat, sapcentrifuge, senseo, slowcooker, slowjuicer, staafmixer, stoomoven, tosti-ijzer, vaatwasser, vriezer, waterkoker

**Schoonmaken (cleaning):** stofzuiger (all variants), dweilrobot, kruimeldief, raamreiniger, stoomreiniger, tapijtreiniger

**Huishoudelijk (household):** airconditioner, elektrische-kachel, luchtbevochtiger, luchtreiniger, ontvochtiger, strijkijzer, wasdroger, wasmachine, afzuigkap

**Tuin (garden):** bladblazer, bosmaaier, grasmaaier, heggenschaar, hogedrukreiniger, verticuteermachine

## Link Insertion Rules

1. **Natural placement:** Insert links where the target topic organically mentioned. E.g., an airfryer article discussing baking → link to magnetron. A stofzuiger article discussing pet hair → link to stofzuiger-voor-allergie or stofzuiger-tegen-dierenharen.

2. **Anchor text variety:** Use descriptive anchors like "onze [stofzuiger gids](/reviews/beste-stofzuiger-2026/)" or "bij het [vergelijken van robotstofzuigers](/reviews/beste-robotstofzuiger-2026/)" — avoid repetitive patterns.

3. **Frontmatter `related` as primary targets:** Each article already declares 2-3 related slugs. Use these plus 1-2 additional category-appropriate targets for depth.

4. **Preserve existing structure:** Don't change frontmatter, section headings, product tables, or the existing "Gerelateerde artikelen" section at the bottom.

5. **Keep markdown valid:** Use `[anchor text](/reviews/slug/)` format matching existing link style. The site uses `/reviews/slug/` path pattern.

6. **File must still parse as valid Astro content** — frontmatter must remain valid YAML, body must remain valid markdown.

## Success Criteria

1. All 62 articles have 2-4 contextual body-text internal links
2. Links use natural Dutch anchor text, not generic "click here"
3. Frontmatter and existing sections are untouched
4. All markdown remains valid (no broken syntax)
5. Site builds successfully after changes (`npm run build` in the project root)
6. A summary file is created at `/home/cls/clawd/scripts/missions/passive-income/dutch-appliances-site/internal-linking/links-added.md` listing each article slug + the links added

## Environment

- Working directory: `/home/cls/clawd/scripts/missions/passive-income/dutch-appliances-site/`
- Articles: `src/content/reviews/`
- Build command: `npm run build`
- Python available for scripting
- Gemini API key at `~/.hermes/private/gemini-api-key` (env var `GEMINI_API_KEY`)

## Approach Recommendation

A Python script that:
1. Reads each article's frontmatter `related` array + category
2. Builds a link-target map (slug → article title + description for context)
3. For each article, identifies 2-4 natural insertion points in the body text
4. Uses Gemini API (minimal, cost ~$0.02 total) to suggest Dutch anchor text + insertion points
5. Inserts the links, writes the file back, verifies with `npm run build`

Alternative if Gemini is unreliable: pure rule-based insertion using keyword matching (e.g., if body contains "magnetron", insert link to beste-magnetron-2026).

## Output

- Modified article files in `src/content/reviews/`
- Summary file: `internal-linking/links-added.md`
- Build verification: `npm run build` passes
- RESULT.md in this directory with what was done
