---
name: introduction-review-skill
description: "Academic introduction and literature review writing with citation-aware reference generation. TRIGGER when: user asks to write/rewrite an introduction or literature review, add or remove citations, format references, audit citations, generate bibliography. SKIP when: user asks for a single-paper summary, general writing advice not involving citations, pure grammar fixes."
model: claude-sonnet-4-6
---

# Introduction Review Skill

Core loop: **write with `[CITE:lastnameYEAR]` placeholders → run `cite_table.py` → relay table in conversation → self-audit**. The script is the authority — no LLM handles citation numbering.

## When NOT to Use

- Single-paper summary or abstract writing (no citation mapping needed)
- Pure grammar or language polishing (no citation changes)
- Non-academic writing (blog posts, marketing copy)
- Format conversion only (e.g. "convert my BibTeX to APA") — use a simpler workflow

## Phase 0: Environment Check

Run `bash scripts/setup.sh` (or equivalent for Windows). This checks:
- Python 3.10+ 
- `rich` package installed
- MCP servers available: `arxiv`, `scholar`, `paper-search`, `pdf-reader`

If any missing, report and offer to install. Don't block — warn and proceed.

## CRITICAL: Placeholder System

**NEVER write `[1]`, `[2]`, `[3]`.** Always use `[CITE:lastnameYEAR]`. The script assigns numbers. Supports multiple input formats: `[CITE:key]`, `[REF:key]`, `\cite{key}`, `\citep{key}`, `[@key]` — all unified to `[N]` on output.

```
Draft:  "Smith [CITE:smith2023] proposed... Jones \cite{jones2022}..."
Script: "Smith [1] proposed... Jones [2]..."
```

Add or remove a citation → edit placeholders → re-run script → all numbers auto-shift. No manual renumbering ever.

## Four Scenarios

| User says | Agent does |
|-----------|-----------|
| New review ("帮我写XX综述") | Write draft with `[CITE:xxx]` → run script → **table** |
| Add citation ("加一篇引用") | Insert `[CITE:xxx]` → re-run script → **table** |
| Remove citation ("删掉这篇") | Remove `[CITE:xxx]` → re-run script → **table** |
| Audit ("检查引用") | Re-run script → run checks below → **table** |

Every scenario ends: `cite_table.py` → `Read cite_output.txt` → paste table + checks in reply.

## Always-On Checks (Repeated)

**After every citation touch, re-run `cite_table.py` and walk through:**

1. **Stacking** — >3 citations in one bracket? Warn. >5? Block.
2. **Format** — venue mismatch? Load `references/citation-formats.md`. Re-check after ref generation.
3. **Order** — gaps or jumps? Script catches this.
4. **Orphan** — in-text count != reference count? Report.
5. **Tone** — "fails to", "ignores", "fundamentally flawed"? Load `references/diplomatic-critique.md`.

Report after table: one line per check, `✅` or `⚠️`.

## Table Protocol (Mandatory)

```
python scripts/cite_table.py <draft_file>
Read: scripts/cite_output.txt
→ Paste table + audit summary in reply.
→ Then ask: "Need to add, remove, or change any citations?"
```

Table is hard-coded, bilingual (中文/English auto-detected). 5 columns: # | Author | Body Context | Reference | Status. Repeated citations get `↳` sub-rows.

## Scripts

- `cite_table.py` — core engine. Scan, number, table, bilingual. Hard-coded.
- `cite_scan.py` — numbered text output + JSON mapping.

## Reference Files

- `citation-formats.md` — IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules.
- `diplomatic-critique.md` — phrase bank. Guideline, not hard rule.
