# KiesKeuken — AGENTS.md for autonomous agents

## Repository: Rigbay/dutch-appliances (KiesKeuken)

Astro 5 + Tailwind CSS static site. 86 kitchen appliance reviews in `src/content/reviews/`.

## Rules

1. **No remote git push** — local-only
2. **No builds** — don't run `npm run build` or `astro build`
3. **`git diff --check` clean** before committing
4. **Affiliate registry** lives at `~/.hermes/affiliates/merchants.json` — never hardcode affiliate status text in components
5. **Do not edit `~/.openclaw/` or `~/.hermes/` config files** — those are separate agent profiles


## LLM Preamble Leak Validation (added 2026-07-10 by Fable)

Before committing ANY generated article (kieskeuken or dutch-ai-tools), scan body AND frontmatter description for model-wrapper preamble that leaked into content:

```bash
grep -rn -iE 'geschreven vanuit het perspectief|Door uw consumentenjournalist|^(Oke|Oké|Absoluut|Zeker|Natuurlijk)., (hier|Hier) is' src/content/
```

Any hit = the generation script pasted the model's framing sentence ("Oké, hier is de koopgids...") into the article. Strip it: the article body must START at its first real heading; the description must be a real meta description, never the model's reply preamble. Root cause: generation scripts writing the raw model response without trimming the conversational wrapper — add a trim step to every new gen-*.py.

Receipt: 2026-07-10 Fable found 14 PUBLISHED articles with this leak (13 kieskeuken + 1 dutch-ai-tools, 2 leaked into SEO meta descriptions), stripped them (commits ab3a6ec / 09f8d276).
