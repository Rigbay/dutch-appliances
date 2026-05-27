# KiesKeuken — AGENTS.md for autonomous agents

## Repository: Rigbay/dutch-appliances (KiesKeuken)

Astro 5 + Tailwind CSS static site. 86 kitchen appliance reviews in `src/content/reviews/`.

## Rules

1. **No remote git push** — local-only
2. **No builds** — don't run `npm run build` or `astro build`
3. **`git diff --check` clean** before committing
4. **Affiliate registry** lives at `~/.hermes/affiliates/merchants.json` — never hardcode affiliate status text in components
5. **Do not edit `~/.openclaw/` or `~/.hermes/` config files** — those are separate agent profiles
