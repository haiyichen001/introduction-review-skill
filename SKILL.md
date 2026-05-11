---
name: introduction-review-skill
description: "Academic introduction and literature review writing with citation-aware reference generation. TRIGGER when: user asks to write/rewrite an introduction or literature review, add or remove citations, format references, audit citations, generate bibliography. SKIP when: user asks for a single-paper summary, general writing advice not involving citations, pure grammar fixes."
---

# Introduction Review Skill

Core loop: **normalize → run `cite_table.py` → relay table → self-audit**.

1. **LLM normalizes**: scan user's draft for ANY citation format (`[REF01]`, `[REF:key]`, `\cite{key}`, `[@key]`, `[1]`, `①`, whatever) and convert all to `[CITE:descriptiveKey]`. The LLM is flexible; it handles every variant.
2. **Script verifies**: `cite_table.py` only reads `[CITE:key]`. Hard-coded, deterministic, single regex. No guesswork.
3. **Table proves**: the output table shows every normalized citation → the LLM didn't miss or invent anything.

If the LLM misses a citation during normalization, the table will show fewer refs than expected — the user catches it immediately.

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

## Normalization (run before script)

If the user's draft uses any non-`[CITE:key]` citation format, normalize it first. Scan for all citation-like patterns and convert to `[CITE:lastnameYEAR]`:

- `[REF01]` → `[CITE:ref01]`
- `[REF:smith2023]` → `[CITE:smith2023]`
- `\cite{jones2022}` → `[CITE:jones2022]`
- `[@wang2024]` → `[CITE:wang2024]`
- Bare `[1]` `[2]` → `[CITE:paper1]` `[CITE:paper2]` (ask user for descriptive keys)

After normalization, run `cite_table.py`. The script only reads `[CITE:key]` — one format, no ambiguity.

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
6. **Citation depth** — each cited paper should appear as: **who + did what + found what (data/conclusion) + [N]**. A bare `[N]` at the end of a vague sentence tells the reader nothing. Example:
   - Bad: "Recent work [5,6] has formalized agent execution."
   - Good: "Wei [5] analyzed 70 projects and identified five design dimensions---finding registry-oriented tools remain dominant. Guerin and Guerin [6] proposed KAIJU, demonstrating that execution-reasoning separation enforces behavioral guarantees."
   - If a citation is just "prior work exists [3]", rewrite it or remove it. Guideline, not hard rule — adjust to field norms.

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
