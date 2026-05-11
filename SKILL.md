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

## Always-On Checks (Self-Awareness)

The skill MUST proactively sniff for these issues every time it touches citations — not just when the user says "audit". After any edit, draft, renumber, or table generation, mentally run through this list and flag problems in the reply.

### 1. Citation Stacking (pile-up)
- **Rule**: max 3 per bracket, absolute max 5.
- **Check**: scan for `[N,N+1,N+2,N+3]` patterns. If >3 in one bracket, warn user and offer to split or reduce.
- **Why**: one sentence citing 8 papers is lazy; each claim should cite its specific source.

### 2. Format Compliance
- **Rule**: venue-specific (IEEE/GB7714/EI/SCI/APA etc). Load `references/citation-formats.md` when user specifies a venue.
- **Check**: 
  - IEEE/GB7714/EI → numbered `[1] [2]`, references sequential by appearance.
  - APA → author-year, references alphabetical. Not numbered.
  - If user says "学位论文" but draft uses APA → warn immediately.
  - Superscript vs inline bracket per venue convention.
- **Why**: wrong format = desk rejection.

### 3. Sequential Order
- **Rule**: `[1] [2] [3]...` by first-appearance order.
- **Check**: `cite_table.py` handles this, but verify no gaps or jumps after renumber.
- **Why**: out-of-order citations confuse reviewers and break reference mapping.

### 4. Orphan / Missing
- **Rule**: every in-text citation has a reference entry; every reference entry is cited in text.
- **Check**: count unique placeholders vs reference entries. Mismatch = flag.
- **Why**: orphan refs look sloppy; missing refs break traceability.

### 5. Tone (Diplomatic Critique)
- **Rule**: guideline from `references/diplomatic-critique.md`. Not hard, but worth checking.
- **Check**: scan for forbidden phrases ("fails to", "ignores", "fundamentally flawed"). Flag if found.
- **Why**: overly harsh critique weakens credibility.

### When to Run Checks

| Trigger | Checks to run |
|---------|--------------|
| After drafting | 3 (order), 5 (tone) |
| After renumbering | 1 (stacking), 3 (order), 4 (orphan) |
| After generating refs | 2 (format), 4 (orphan) |
| User mentions venue | 2 (format) |
| Before final output | ALL 1-5 |

If any check fails, report it alongside the table. Don't block — warn and let the user decide.

## Key Principles

- **Placeholder-first**: `[CITE:xxx]` only, never hardcoded numbers.
- **Script is law**: `cite_table.py` does all numbering — deterministic, no LLM errors.
- **End with table**: every task, no exceptions.
- **Always check**: after every citation touch, run relevant Always-On Checks.
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
