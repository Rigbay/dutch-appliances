# KiesKeuken — Upgrade search URLs to ASIN product links

## Goal

Replace ~753 Amazon search links (earning zero commission) with direct ASIN product links across 104 KiesKeuken articles. This is the highest-ROI affiliate fix — 104 articles currently earn 0c from Amazon because search URLs rarely convert.

## Scope

- **104 articles** with zero ASIN links (all product buttons are `amazon.nl/s?k=...`)
- **~753 unique search terms** (product names like "Philips Airfryer XXL HD9867/90")
- **18 articles** have at least one real ASIN link — these are the bootstrap reference
- **Known-ASIN map** at `scripts/known-asins.json` — 69 product names mapped to ASINs

## NEW FINDING — Cross-article same-ASIN collisions (2026-06-03 22:17)

The earlier same-ASIN fix only caught cases where ALL products in ONE article shared the same wrong ASIN. There's a subtler variant: **7 ASINs reused across completely different products, where only 1 product per article has the wrong ASIN.** These need browser verification:

| ASIN | Used For | Suspect |
|------|----------|---------|
| B0020P15BQ | Liebherr koelkast, De'Longhi koffiemachine, Severin melkopschuimer, Liebherr vriezer | Only 1 is correct |
| B07VV4NZW5 | 9 different Philips products (lattego, stofzuiger, luchtreiniger, handmixer, blender, staafmixer, melkopschuimer, waterkoker, speedpro) | Almost certainly wrong for 8/9 |
| B08CKZFR8N | Bosch koelkast, Samsung stofzuiger, Samsung magnetron, Samsung koelkast, Samsung vriezer, Siemens koelkast | Wrong for most |
| B06XDPNQ1R | 4 KitchenAid products (staafmixer, waterkoker, handmixer, blender) | Confirm correct or not |
| B09MJ7QL6H | Dyson Purifier, Dyson V15 Detect (2x), Xiaomi Air Purifier | Wrong for Xiaomi |
| B0CQ8GHBRG | Bosch inbouwoven, Samsung AI Oven | Wrong for one |
| B07HFY6N2R | Moccamaster KBG Select (2 articles, same product) | Likely correct |

**Priority fix:** The 18 articles with at least one real ASIN link likely have the WRONG ASIN on 1 product (the collision ASIN). These are the highest-value first-pass: VERIFY each collision ASIN belongs to the product it's linked to in that article. If it doesn't, find the correct ASIN.

## Strategy

1. **Work one article at a time.** Each `.md` file under `src/content/reviews/` has a `products:` array in frontmatter. Each product entry has a `name:` and `affiliateLink:` — the latter is either a search URL (needs fixing) or a real ASIN link (needs VERIFICATION per the collision list).

2. **For each product** with a search URL:
   - Check `scripts/known-asins.json` first — if the product name is there, reuse the ASIN without browsing
   - If not found, search Amazon.nl for the exact product name
   - Find the correct product page (match the exact model number in the search term)
   - Extract the ASIN from the product URL (`/dp/B0XXXXXXXX`)
   - Build: `https://www.amazon.nl/dp/ASIN?tag=kieskeukennl-21`

3. **For each product** with an ASIN listed in the `collisions` section above:
   - VERIFY the ASIN matches the actual product
   - If wrong, find the correct ASIN on Amazon.nl

4. **Reuse discovered ASINs** — when the same product name appears across articles, use the same ASIN.

5. **When you encounter a tough search** (ambiguous results, discontinued model, many variants):
   - Try the most specific match (same model number, year, specs)
   - If truly ambiguous, leave it as a search URL and note it in RESULT.md
   - Do NOT use a wrong ASIN — that's worse than a search URL

## What "done" looks like

After fixing an article file (edit the affiliateLink in the products frontmatter), the file should have:
- `https://www.amazon.nl/dp/B0XXXXXXXX?tag=kieskeukennl-21` in the affiliateLink
- The same tag `kieskeukennl-21` (do NOT change the StoreID)
- The ASIN matches the specific product model listed in `name:`
- All 7 collision ASINs verified or corrected

## Caveats

- Some products are genuinely discontinued on Amazon.nl — leave those as search URLs
- Comparison articles (inductie-vs-gasfornuis, etc.) reference many products — those need the most ASINs
- The `affiliateLinks:` list at the top of the frontmatter (not per-product) should also get ASINs when possible
- Do NOT touch non-Amazon links (Coolblue, Bol.com placeholders, etc.)
- Do NOT navigate to any site other than amazon.nl and file:///workspace/kieskeuken/

## Recording

After each batch, append to `scripts/asin-progress.md` (create if absent):
- Which articles fixed
- How many links upgraded
- Any products that couldn't be resolved
- Any collision ASINs confirmed as correct or fixed