# introduction-review-skill

Agent skill for academic introductions and literature reviews. Core engine: `cite_table.py` — a hard-coded script that scans `[CITE:xxx]` placeholders, assigns sequential numbers, and outputs a 5-column reference table.

## How it works

```
Write with [CITE:lastnameYEAR] → run cite_table.py → table in conversation → self-audit
```

The table is the user's trust anchor: deterministic, no LLM involvement, shows every citation mapped to its reference. Re-run it after every edit — it costs nothing.

## Table output (5 columns)

| # | Author | Body Context (--40) | Reference | Status |
|---|--------|--------------------|-----------|--------|

- Repeated citations get sub-rows with `↳` arrows
- Bilingual: auto-detects Chinese/English from draft content
- Disclaimer line included with every output

## Always-On Checks

The agent repeatedly self-audits after every citation change:
1. **Stacking** — max 3 per bracket, absolute 5
2. **Format** — venue mismatch detection (IEEE/GB7714/APA etc)
3. **Order** — no gaps or jumps in `[1][2][3]...`
4. **Orphan** — in-text count = reference count
5. **Tone** — no "fails to", "ignores", "fundamentally flawed"

## Install

```bash
cp -r introduction-review-skill ~/.claude/skills/
# or
npx skills add haiyichen001/introduction-review-skill
```

Requires: `arxiv`, `scholar`, `paper-search`, `pdf-reader` MCP servers. Python package `rich`.

## Project structure

```
├── SKILL.md                     # Core instructions
├── README.md
├── scripts/
│   ├── cite_table.py            # Core engine: scan, number, table (bilingual)
│   └── setup.sh                 # Environment check
└── references/
    ├── anti-laziness-protocol.md     # Mandatory 5-step verification gate
    ├── citation-formats.md           # IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM
    ├── citation-placement-rules.md   # Per-citation placement enforcement
    └── diplomatic-critique.md        # Mandatory tone guard
```

## License

MIT
