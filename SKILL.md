---
name: introduction-review-skill
description: An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.
---

# Introduction Review Skill

Core loop: **write with `[CITE:lastnameYEAR]` placeholders → run `cite_table.py` → relay table in conversation → self-audit**. The script is the authority — no LLM handles citation numbering.

## CRITICAL: Placeholder System

**NEVER write `[1]`, `[2]`, `[3]`.** Always use `[CITE:lastnameYEAR]`. The script assigns numbers.

```
Draft:  "Smith [CITE:smith2023] proposed... Jones [CITE:jones2022] improved..."
Script: "Smith [1] proposed... Jones [2] improved..."
```

Add or remove a citation → edit placeholders → re-run script → all numbers auto-shift. No manual renumbering ever.

## Four Scenarios

| User says | Action |
|-----------|--------|
| New review ("帮我写XX综述") | Write draft with `[CITE:xxx]` → run script → **table** |
| Add citation ("加一篇引用") | Insert `[CITE:xxx]` → re-run script → **table** |
| Remove citation ("删掉这篇") | Remove `[CITE:xxx]` → re-run script → **table** |
| Audit ("检查引用") | Re-run script → run checks below → **table** |

Every scenario ends the same way: `cite_table.py` → `Read cite_output.txt` → paste table + audit results in reply.

## Citation Rules (enforced by script)

- Sequential numbering `[1][2][3]...` by first-appearance order. Same source = same number.
- Group limit: max 3 per bracket, absolute 5. Over 3 → warn user.
- References ordered by appearance, not alphabetically (unless APA).

## Always-On Checks

**After every citation touch, self-audit. Flag issues alongside the table.**

1. **Stacking** — >3 citations in one bracket? Warn.
2. **Format** — venue mismatch? (e.g. APA style used for GB7714 thesis). Load `references/citation-formats.md` when user specifies venue.
3. **Order** — gaps or jumps in `[1][2][3]...`? Script catches this.
4. **Orphan** — ref in bibliography but not cited? Or cited but missing from refs? Count must match.
5. **Tone** — forbidden phrases ("fails to", "ignores", "fundamentally flawed")? Reference `references/diplomatic-critique.md`.

Report check results with the table: one line per check, `✅` or `⚠️`.

## Table Protocol (Mandatory)

```
python scripts/cite_table.py <draft_file>
Read: scripts/cite_output.txt
→ Paste table + audit summary in reply.
```

Table is bilingual (中文/English auto-detected). Disclaimer is auto-included. This is the only output format the user needs.

## Scripts

- `cite_table.py` — core engine. Scan, number, table, bilingual. Hard-coded.
- `cite_scan.py` — numbered text output + JSON mapping.

## Reference Files

- `citation-formats.md` — IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules. Load on-demand.
- `diplomatic-critique.md` — phrase bank. Guideline, not hard rule.

## MCP

`arxiv`, `scholar`, `paper-search`, `pdf-reader`. Auto-check on load.
