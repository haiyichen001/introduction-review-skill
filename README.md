# introduction-review-skill

An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.

## What it does

- Auto-searches papers on arXiv, Semantic Scholar, PubMed, bioRxiv/medRxiv based on your topic
- Drafts structured introductions (hook → gap → related work → approach → contributions)
- Manages citations with a placeholder system — never manually renumber references again
- Generates reference lists in IEEE, APA, GB/T 7714, Vancouver, MLA, Chicago, ACM, BibTeX
- Audits citations for ordering, orphans, unsupported claims, and diplomatic tone

## Install

Copy the `SKILL.md` to your Claude Code skills directory:

```
# Locate your skills directory
ls ~/.claude/skills/

# Copy the skill
cp -r introduction-review-skill ~/.claude/skills/
```

Or install via Smithery:

```
npx skills add haiyichen001/introduction-review-skill
```

Requires MCP servers: `arxiv`, `scholar`, `paper-search`, `pdf-reader`. The skill auto-checks and installs missing ones on first run.

## Usage

In Claude Code, type `/introduction-review-skill` or say "help me write an introduction".

Then provide:
- A research topic (e.g., "neural mesh segmentation for noisy point clouds")
- Or paper IDs (DOI, arXiv ID, title list)
- Or an existing draft to polish

The skill will guide you through 6 phases with visible progress at each step.

## Citation rules enforced

- Sequential numbering `[1]`, `[2]`, `[3]`... by first appearance
- Max 3 citations per bracket (asks before exceeding)
- Diplomatic critique language (no attacking prior work)
- Chinese thesis support: GB/T 7714-2015 with superscript and bracket options

## License

MIT
