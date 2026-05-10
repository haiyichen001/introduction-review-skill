---
name: introduction-review-skill
description: AI-assisted academic introduction and literature review writing with citation-aware reference generation in multiple formats.
---

# Introduction Review Skill

Assists with writing academic paper introductions, literature reviews, and generating properly formatted references with traceable citations.

## When to Use This Skill

Use this skill when the user:

- Writes or rewrites an academic paper introduction section
- Needs a structured literature review / related work section
- Wants to generate a bibliography from cited works in a specific format
- Asks to "polish my intro", "write a lit review", "format my references", or "check my citations"
- Needs to match citations in-text with reference entries
- Reads or summarizes papers and wants to weave them into a coherent narrative

## Workflow

### Phase 1: Gather Context

Ask the user for:

1. **Topic / research area** — one sentence summary of their paper
2. **Key papers** — DOIs, arXiv IDs, or titles (at least 3-5)
3. **Target venue** — journal, conference, or thesis (affects tone and length)
4. **Existing draft** — optional, if they already have something written

### Phase 2: Read Papers

For each paper the user provides:

- Fetch abstract and metadata via arxiv/scholar MCP tools
- If full text needed, download and extract key contributions, methods, and findings
- Store structured notes: problem statement, method, key result, relationship to user's work

### Phase 3: Draft Introduction / Literature Review

Follow the standard academic introduction structure:

1. **Hook** — broad context, why the area matters
2. **Problem statement** — the gap or unsolved issue
3. **Related work** — what others did, what they left unsolved
4. **Our approach** — how the user's work fills the gap
5. **Contributions** — bullet list of novel contributions
6. **Roadmap** — paper structure overview

### Phase 4: Generate References

- Extract all citations from the draft
- Match each citation to its paper metadata
- Generate reference entries in the user's chosen format
- Default formats supported: **BibTeX**, **APA 7th**, **IEEE**, **MLA**, **Chicago**, **ACM**

### Phase 5: Citation Audit

- Verify every in-text citation has a corresponding reference entry
- Flag any "orphan" references (in bibliography but not cited)
- Flag any missing references (cited but not in bibliography)
- Suggest papers for claims that lack citation support

## Key Principles

- **Traceability first**: every citation must resolve to a real paper with verified metadata
- **No hallucinated papers**: never invent titles, authors, or DOIs — use search tools to verify
- **Narrative flow**: the intro tells a story — background → gap → solution → contributions
- **User voice preserved**: polish language but retain the user's technical framing and terminology

## Reference Format Defaults

| Format    | Example entry |
|-----------|--------------|
| BibTeX    | `@article{key, author={...}, title={...}, ...}` |
| APA 7th   | Author, A. A. (Year). *Title*. Journal, Vol(Issue), pp. |
| IEEE      | [1] A. A. Author, "Title," *Journal*, vol. X, no. Y, pp. Z, Year. |
| MLA 9th   | Author, A. A. "Title." *Journal*, vol. X, no. Y, Year, pp. Z. |
| Chicago   | Author, A. A. "Title." *Journal* Vol, no. Issue (Year): Pages. |
| ACM       | A. A. Author. Year. Title. *J.* Vol, Issue (Year), Pages. |

## MCP Tools Used

- `mcp__arxiv__*` — search, abstract, full-text retrieval
- `mcp__scholar__*` — search papers, get citations/references, download PDFs
- `mcp__pdf-reader__read_pdf` — extract text from local PDFs

## Example Session

```
User: Help me write the introduction for my paper on neural mesh segmentation.
      Key papers: arXiv:2103.12345, arXiv:2205.67890, 10.1145/3456789.
      Target: ACM TOG.

Agent:
  1. Fetches abstracts for all 3 papers
  2. Asks user: "What's your method's key novelty compared to these?"
  3. Drafts introduction following hook→gap→approach→contributions structure
  4. Generates ACM-format reference entries for all citations
  5. Runs citation audit — all clear
```
