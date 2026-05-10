# Status: needs-human

The Dutch content site is built and compiles. Kiara needs to complete these steps to go live.

## Human-Only Checklist

### 1. Buy domain (~€10/year)
- Suggested: `beste-apparaten.nl` or `besteapparaten.nl` (check availability at TransIP or Namecheap)
- After purchase: point A-record to Vercel's DNS (76.76.21.21)

### 2. Create GitHub repo and push code
- Create private repo (e.g. `kiara/beste-apparaten`)
- Add the built site directory as initial commit:
  ```bash
  cd /home/cls/clawd/scripts/missions/passive-income/dutch-appliances-site/
  git init
  git remote add origin git@github.com:<user>/<repo>.git
  git add .
  git commit -m "Initial Astro site: 5 articles + templates"
  git push -u origin main
  ```

### 3. Create Vercel project and link
- Import GitHub repo at vercel.com
- Framework preset: Astro
- Build command: `npm run build`
- Output directory: `dist`
- Add custom domain from step 1

### 4. Apply for Bol.com Partner Program
- URL: https://partnerplatform.bol.com/
- Requirements: live website with real content (we have 5 articles ready)
- Approval typically takes 1–3 business days
- After approval: replace placeholder links `https://partner.bol.com/.../[TODO]` with real deep links

### 5. Set Gemini API key (optional — for content pipeline)
- Get free API key at https://aistudio.google.com/app/apikey
- Set in Vercel environment variables or local `.env`:
  ```
  GEMINI_API_KEY=your_key_here
  ```

### 6. Publish remaining 5 articles
- Fill body content in the 5 draft templates (marked `draft: true`)
- Set `draft: false` in frontmatter
- Push → Vercel auto-deploys

## Post-Launch Cadence
- Week 1–2: Fill + publish 5 draft templates → 10 articles live
- Week 3–4: Generate 10 more articles via Gemini API or manual writing
- Month 2 Target: 50 articles
- Month 6 Target: 200+ articles
- Maintenance: <1 hour/week (monitor rankings, update seasonal models)

## Blockers
None — Kiara can proceed whenever she has 15 minutes for the domain/GitHub/Vercel steps.
