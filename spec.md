# Pilot Spec: Dutch Home Appliance Review Site

## Mission
Build a Dutch-language SEO content site focused on home appliance reviews and comparisons ("beste [apparaat] 2026"), monetized via Bol.com affiliate links. Target: reach 50 published articles within 2 weeks, begin earning affiliate commissions within 6-12 months.

## Constraints (non-negotiable)
- No active daily time required from Kiara after build (<1 hr/week monitoring)
- No crypto/trading/dropshipping
- All content in Dutch (native-speaker quality)
- Capital budget: €200 first year
- Low-stress: no client management, no sales calls, no inventory

## Tech Stack
- **Framework:** Astro 5.x (static site, SEO-native, fast)
- **Styling:** Tailwind CSS (via Astro integration)
- **Content:** Markdown files in `src/content/reviews/` — no CMS
- **Hosting:** Vercel (free tier, auto-deploy on git push)
- **Domain:** TransIP or Namecheap (~€10/year) — Kiara buys after site is built
- **Git:** GitHub repo (Kiara creates after build)
- **Content generation:** Python script calling Gemini API (free tier) for Dutch article drafts
- **Monetization:** Bol.com Partner Program (apply after 10+ articles live)

## What Codex WILL build autonomously (now)
1. Astro project scaffold with proper SEO config (sitemap, robots.txt, structured data)
2. Layout components: Header, Footer, ArticleCard, ReviewLayout
3. Theme/styling: clean, trustworthy, mobile-first, Dutch-language navigation
4. Content collection schema for review articles (frontmatter: title, slug, category, rating, price range, pros/cons, affiliate links, date, model year)
6. 5 seed articles (fully written by you now) covering the highest-value Dutch appliance queries:
   - beste-airfryer-2026.md
   - beste-stofzuiger-2026.md
   - beste-robotstofzuiger-2026.md
   - beste-koffiemachine-2026.md
   - beste-waterkoker-2026.md
   PLUS article templates (ready to fill) for:
   - beste-broodrooster-2026.md
   - beste-magnetron-2026.md
   - beste-stoomoven-2026.md
   - beste-draadloze-stofzuiger-2026.md
   - beste-handmixer-2026.md
6. Each article: 1,500-2,500 words, comparison table, "beste keuze" recommendation, price-range filter, Bol.com affiliate link placeholders (format: `https://partner.bol.com/.../[PRODUCT_ID]`)
7. Homepage: latest reviews grid, category navigation, about section
8. Category pages: Huishoudelijk, Keuken, Schoonmaken
9. A Python script `scripts/generate-article.py` that:
   - Reads a product name + target keywords from a JSON list
   - Calls Gemini Flash (API key from env var `GEMINI_API_KEY`) 
   - Generates a Dutch review article in the correct Markdown format with frontmatter
   - Saves to `src/content/reviews/`
   - Has rate limiting and cost logging
10. Build verification: `npm run build` passes, no broken links, Lighthouse score >80

## What requires Kiara / human hands (Codex writes STATUS.md for these)
- Buy domain (~€10) and point DNS to Vercel
- Create GitHub repo and push initial code
- Create Vercel project and link to GitHub
- Apply for Bol.com Partner Program (needs live site URL)
- Set `GEMINI_API_KEY` env var (Kiara already has Google AI Studio access)
- Replace affiliate link placeholders with real Bol.com deep links after approval

## File structure to create
```
dutch-appliances-site/
├── astro.config.mjs
├── package.json
├── tailwind.config.mjs
├── public/
│   └── robots.txt
├── src/
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── ReviewLayout.astro
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── ArticleCard.astro
│   │   ├── ComparisonTable.astro
│   │   └── AffiliateNotice.astro
│   ├── content/
│   │   ├── config.ts
│   │   └── reviews/
│   │       ├── beste-airfryer-2026.md
│   │       ├── beste-stofzuiger-2026.md
│   │       ├── beste-robotstofzuiger-2026.md
│   │       ├── beste-koffiemachine-2026.md
│   │       ├── beste-waterkoker-2026.md
│   │       ├── beste-broodrooster-2026.md
│   │       ├── beste-magnetron-2026.md
│   │       ├── beste-stoomoven-2026.md
│   │       ├── beste-draadloze-stofzuiger-2026.md
│   │       └── beste-handmixer-2026.md
│   ├── pages/
│   │   ├── index.astro
│   │   ├── [slug].astro
│   │   ├── categorie/
│   │   │   ├── huishoudelijk.astro
│   │   │   ├── keuken.astro
│   │   │   └── schoonmaken.astro
│   │   └── over.astro
│   └── styles/
│       └── global.css
├── scripts/
│   ├── generate-article.py
│   ├── article-list.json
│   └── cost-logger.py
├── STATUS.md          <-- Codex fills this with human-only checklist
└── RESULT.md          <-- Codex fills this with what was built
```

## SEO requirements
- Every page: unique `<title>` and `<meta name="description">` in Dutch
- Structured data: `Product` schema with aggregateRating on review pages
- Sitemap.xml generated at build time (Astro sitemap integration)
- Canonical URLs
- Open Graph tags for social sharing
- Internal linking: 2-3 links between related articles
- URL pattern: `/beste-[product]-2026/` (Dutch slug, hyphenated)
- No thin content — minimum 1,500 words per article

## Content quality standard
- Dutch must feel natural (not translated-English awkwardness)
- Articles must include: introduction, top 5-7 products compared, "beste keuze per budget" (beste koop, beste prestaties, beste prijs-kwaliteit), buying guide, FAQ
- Comparison tables with real product names (from Bol.com catalog — use real products that exist)
- No fake reviews — honest pros/cons, mention known flaws
- Affiliate disclosure at bottom of every review article (required by Dutch law + Bol.com terms)

## Deployment path
1. Codex builds everything in `dutch-appliances-site/` locally in WSL
2. Codex writes RESULT.md with build summary
3. Codex writes STATUS.md with human-only checklist (domain, GitHub repo, Vercel, Bol.com signup)
4. Hermes reads RESULT.md + STATUS.md, updates opportunities.md
5. Kiara completes human checklist when she has 10 minutes
6. Once live: run `scripts/generate-article.py` weekly to add new articles
7. Goal: 50 articles by end of month 2, 200+ by month 6

## Exit criteria for this pilot
- ✅ Site builds successfully (`npm run build` passes)
- ✅ 10 seed articles published with proper Dutch content
- ✅ Homepage + category pages render correctly
- ✅ All SEO meta tags present
- ✅ Affiliate disclosure included on every article
- ✅ Mobile-responsive (test via browser devtools)
- ✅ STATUS.md lists exactly what Kiara needs to do (domain, GitHub, Vercel, Bol.com)

## Kill condition
If after 4 months of being live with 50+ articles, the site earns <€50/month and shows no traffic growth trend — archive and post-mortem. Otherwise: iterate and scale.
