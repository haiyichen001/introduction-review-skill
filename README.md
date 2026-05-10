# introduction-review-skill

An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.

## Features

- Auto-searches papers on arXiv, Semantic Scholar, PubMed, bioRxiv/medRxiv
- Drafts structured introductions (hook -> gap -> related work -> approach -> contributions)
- **Placeholder system** — edit with `[CITE:xxx]`, run numbering pass to get `[1][2][3]`. Add or remove citations, renumber with one command
- **Reference table** — `cite_table.py` generates a 4-column summary (# | Author | Context | Status) as mandatory conversation output
- **Hard-coded scripts** — all citation logic is deterministic, no LLM guessing
- Generates references in IEEE, SCI/Vancouver, EI, GB/T 7714, APA, MLA, Chicago, ACM, BibTeX
- Citation audit: ordering, orphans, missing refs, group size, unsupported claims
- Flexible routing: jumps to the phase you need, skips what you don't
- Adaptive CN/EN headers based on draft language

## Project structure

```
introduction-review-skill/
├── SKILL.md                    # Core instructions
├── README.md
├── scripts/
│   ├── cite_table.py           # Primary: reference table output (hard-coded)
│   ├── cite_scan.py            # Numbered text + JSON mapping
│   └── cite_live.py            # Rich-formatted progressive tables (optional)
└── references/
    ├── citation-formats.md     # IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules
    └── diplomatic-critique.md  # Phrase bank (guideline, not hard rule)
```

## Install

```bash
cp -r introduction-review-skill ~/.claude/skills/
```

Or via Smithery:

```bash
npx skills add haiyichen001/introduction-review-skill
```

Requires MCP servers: `arxiv`, `scholar`, `paper-search`, `pdf-reader`. Auto-checks and installs missing ones. Requires Python package `rich`.

## Usage

```
/introduction-review-skill
```

Provide a topic, paper IDs, or a draft. Every task ends with a hard-coded reference table in the conversation — no hallucinated citations.

## License

MIT
