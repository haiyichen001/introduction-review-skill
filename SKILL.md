---
name: introduction-review-skill
description: "Academic introduction and literature review writing with citation-aware reference generation. TRIGGER when: user asks to write/rewrite an introduction or literature review, add or remove citations, format references, audit citations, generate bibliography. SKIP when: user asks for a single-paper summary, general writing advice not involving citations, pure grammar fixes."
---

# Introduction Review Skill

Core loop: **normalize → run `cite_table.py` → relay table → self-audit**.

1. **LLM normalizes**: convert ANY citation format (`[REF01]`, `\cite{key}`, `[@key]`, bare `[1]`, etc) to `[CITE:descriptiveKey]`.
2. **Script verifies**: `cite_table.py` only reads `[CITE:key]`. Hard-coded, deterministic.
3. **Table proves**: every normalized citation appears in the output — nothing missed or invented.

## When NOT to Use

Single-paper summary, pure grammar polishing, non-academic writing, format conversion only.

## Phase 0: Environment Check

Run `bash scripts/setup.sh`. Checks Python 3.10+, `rich`, MCP servers (`arxiv`, `scholar`, `paper-search`, `pdf-reader`). Warn if missing, don't block.

## Four Scenarios

| User says | Agent does |
|-----------|-----------|
| New review | Draft with `[CITE:xxx]` → script → **table** |
| Add citation | Insert `[CITE:xxx]` → re-run script → **table** |
| Remove citation | Remove `[CITE:xxx]` → re-run script → **table** |
| Audit | Re-run script → checks → **table** |

Every scenario ends: `cite_table.py` → `Read cite_output.txt` → paste table + checks.

## Always-On Checks

After every citation change, re-run `cite_table.py` and walk through:

1. **Stacking** — >3 in one bracket? Warn. >5? Block.
2. **Format** — venue mismatch? Load `references/citation-formats.md` (on-demand) when user specifies a venue. Re-check after ref generation.
3. **Order** — gaps or jumps? Script catches this.
4. **Orphan** — in-text count != reference count? Report.
5. **Tone** — `references/diplomatic-critique.md` (loaded at startup). Never "fails to", "ignores", "fundamentally flawed".
6. **Citation depth** — most citations: **who + did what + found what + [N]**. Opening/transition sentences can be broad. Body paragraphs: each cited paper gets its own sentence.
   - Two valid positions: sentence-end (`...reduced errors by 23% [5].`) or natural pause (`...as shown in prior work [5,6], the trend...`).
   - NEVER: `, [5],` (comma sandwich) or `Smith [5] proposed` (author-attached). Script flags these as ⚠️.

Report: one line per check, `✅` or `⚠️`. Then full re-scan (never fix one and skip the rest). Then read all `[N]` aloud to catch awkward flow.

## Table Protocol (Mandatory)

Auto-detect `.bib` file in project dir. If found, use `--bib` mode.

```
python scripts/cite_table.py <draft> [--bib <bib_file>]
Read: scripts/cite_output.txt
→ Paste table + audit. Then: "Need to add, remove, or change any citations?"
```

Without `--bib`: 5 columns (# | Author | Body Context | Reference | Status). With `--bib`: 6 columns comparing body order, bib key, bib position, and reference list order. Bilingual (中文/English auto-detected). Repeated citations get `↳` sub-rows.

## Reference Files

- `anti-laziness-protocol.md` — **loaded at startup**. Mandatory 5-step verification gate. Itemized only, no batching.
- `citation-placement-rules.md` — **loaded at startup**. Per-citation placement enforcement.
- `diplomatic-critique.md` — **loaded at startup**. Mandatory tone guard.
- `citation-formats.md` — **loaded on-demand** when user specifies a venue. IEEE/SCI/EI/GB7714/APA/MLA/Chicago/ACM rules.

## Script

- `cite_table.py` — single core engine. Scan, number, table, position check, bilingual, `--bib` mode.
