# introduction-review-skill

An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.

## What it does

- Auto-searches papers on arXiv, Semantic Scholar, PubMed, bioRxiv/medRxiv
- Drafts structured introductions (hook → gap → related work → approach → contributions)
- **Placeholder system** — edit with `[CITE:xxx]`, run numbering pass to get `[1][2][3]`. Add or remove citations, renumber with one command
- **Deterministic scripts** — numbering pass runs via `scripts/cite_scan.py`, no LLM guessing
- Generates references in IEEE, SCI/Vancouver, EI, GB/T 7714, APA, MLA, Chicago, ACM, BibTeX
- Cites audit: ordering, orphans, missing refs, group size, unsupported claims
- Flexible routing: jumps to the phase you need, skips what you don't

## Project structure

```
introduction-review-skill/
├── SKILL.md                    # Core instructions (~18KB)
├── README.md
├── scripts/
│   └── cite_scan.py            # Placeholder scanner + numbering pass engine
└── references/
    ├── citation-formats.md     # IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules
    └── diplomatic-critique.md  # Phrase bank for lit review writing (guideline)
```

## Install

Copy to your Claude Code skills directory:

```
cp -r introduction-review-skill ~/.claude/skills/
```

Or via Smithery:

```
npx skills add haiyichen001/introduction-review-skill
```

Requires MCP servers: `arxiv`, `scholar`, `paper-search`, `pdf-reader`. Auto-checks and installs missing ones on first run.

## Usage

In Claude Code: `/introduction-review-skill` or say "help me write an introduction".

Provide a topic, paper IDs, or a draft — the skill detects intent and routes to the right phase. Every step streams progress so you see what's happening.

## License

MIT
