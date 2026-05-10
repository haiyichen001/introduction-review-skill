# introduction-review-skill

An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.

## What it does

- Auto-searches papers on arXiv, Semantic Scholar, PubMed, bioRxiv/medRxiv
- Drafts structured introductions (hook → gap → related work → approach → contributions)
- **Placeholder system** — edit with `[CITE:xxx]`, run numbering pass to get `[1][2][3]`
- **Live streaming panel** — citation mapping builds up in real-time within the conversation
- **Deterministic scripts** — numbering pass via `scripts/cite_live.py`, no LLM guessing
- Generates references in IEEE, SCI/Vancouver, EI, GB/T 7714, APA, MLA, Chicago, ACM, BibTeX
- Cites audit: ordering, orphans, missing refs, group size, unsupported claims
- Flexible routing: jumps to the phase you need, skips what you don't

## How the live panel works

When Phase 4 (numbering pass) runs, `cite_live.py` streams output line-by-line via Monitor:

```
 Step 1/3: Citation Scan
  [1] [CITE:smith2023] — Smith et al., "Mesh Segmentation with GNNs" (2023)
  [2] [CITE:jones2022] — Jones & Lee, "Point Cloud Understanding" (2022)
  ...

 Step 2/3: Number Assignment
  [1] ← [CITE:smith2023]
  [2] ← [CITE:jones2022]
  ...

 Step 3/3: Numbered Text
  ...Smith [1]... Jones [2]...
```

Each line appears in the conversation as it's generated, then stays visible after completion.

## Project structure

```
introduction-review-skill/
├── SKILL.md                    # Core instructions
├── README.md
├── scripts/
│   ├── cite_live.py            # Live streaming citation dashboard
│   └── cite_scan.py            # Plain-text numbering pass (pipe-friendly)
├── references/
│   ├── citation-formats.md     # IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules
│   └── diplomatic-critique.md  # Phrase bank for lit review writing (guideline)
└── statusline-cite.ps1/.sh    # Claude Code status line integration (optional)
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
