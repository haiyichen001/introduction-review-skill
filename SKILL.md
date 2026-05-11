---
name: introduction-review-skill
description: An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.
---

# Introduction Review Skill

Drafts academic introductions with `[CITE:lastnameYEAR]` placeholders, then runs hard-coded scripts to number citations and generate a reference table. The table is the core output — every task ends with it.

## Four Entry Points

| User scenario | Trigger | What happens |
|--------------|---------|-------------|
| **New review** | "帮我写XX综述" / "write an intro about..." | Search papers → draft with `[CITE:xxx]` → number → **table** |
| **Add citation** | "加一篇引用" / "add a reference..." | Insert `[CITE:xxx]` into draft → renumber → **table** |
| **Remove citation** | "删掉这篇" / "remove this ref..." | Remove `[CITE:xxx]` from draft → renumber → **table** |
| **Audit only** | "检查引用" / "audit citations..." | Scan existing draft → check order + status → **table** |

All four end the same way: run `cite_table.py` → Read `cite_output.txt` → paste table in reply.

## CRITICAL: Placeholder System

**NEVER write `[1]`, `[2]`, `[3]` directly.** Always use `[CITE:lastnameYEAR]` in drafts. The script assigns numbers.

```
Draft:  "Smith [CITE:smith2023] proposed... Jones [CITE:jones2022] improved..."
Number: "Smith [1] proposed... Jones [2] improved..."
```

Adding or removing a citation → edit placeholders → re-run script → all numbers auto-shift.

## Citation Rules (enforced by script)

- **Sequential numbering**: `[1] [2] [3]...` by first-appearance order. Same source reuses its number.
- **Group limit**: max 3 per bracket (`[1,2,4]`), absolute max 5. Over 3 → ask user.
- **Diplomatic critique**: guideline, not hard rule. Critique the work, not the authors.

## Reference Format by Venue

`references/citation-formats.md` covers: IEEE, SCI/Vancouver, EI, GB/T 7714, APA, MLA, Chicago, ACM. Load on-demand in Phase 5.

## MANDATORY: End Every Task With the Table

```
python scripts/cite_table.py <draft_file>
Read: scripts/cite_output.txt
→ Paste table directly in reply message.
```

The table is hard-coded, bilingual (中文/English auto-detected), and proves every citation is real. The disclaimer is also bilingual.

## Key Principles

- **Placeholder-first**: `[CITE:xxx]` only, never hardcoded numbers.
- **Script is law**: `cite_table.py` does all numbering — deterministic, no LLM errors.
- **End with table**: every task, no exceptions.
- **No hallucinated papers**: verify with arxiv/scholar MCP tools.
- **Show progress**: `✅` per step, emoji keep it scannable.

## MCP Servers Required

`arxiv`, `scholar`, `paper-search`, `pdf-reader`. Auto-checked in Phase 0.

## Scripts

- `scripts/cite_table.py` — core engine: scan, number, table. Bilingual, hard-coded.
- `scripts/cite_scan.py` — numbered text output + JSON mapping.
- `scripts/cite_live.py` — rich-formatted tables (optional visual overview).

## Reference Files

- `references/citation-formats.md` — format rules per venue.
- `references/diplomatic-critique.md` — phrase bank (guideline).
