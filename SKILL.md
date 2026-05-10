---
name: introduction-review-skill
description: An agent skill that assists with writing academic introductions, literature reviews, and citation-aware reference generation in multiple formats.
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

## Workflow

### Phase 0: Detect Intent

**Before asking the user anything, analyze what they already have.**

Print a clear status header so the user knows what's happening:

```
=== Introduction Review Skill ===
Analyzing your input...
```

Check for:

| Signal | Intent | Next step |
|--------|--------|-----------|
| User provided a draft (pasted text / file path) | Has draft → review & polish | Jump to Phase 2 |
| User provided paper IDs (DOI, arXiv, title list) | Has papers → read & draft | Jump to Phase 2 |
| User only gave a topic or vague request | Starting from scratch | Continue to Phase 1, then search |
| User asked to "format references" or "check citations" | Reference-only task | Jump to Phase 5 |
| User mentioned a target venue (journal, conference) | Style constraint noted | Apply format in Phase 5 |

**If the user has NOT provided papers**: do NOT ask them to go find papers. Proceed to Phase 1 to search automatically.

### Phase 1: Check & Install MCP Tools

Print progress:

```
--- MCP Tool Check ---
Checking required tools...
```

Required MCP servers:

| MCP Server | Purpose | Required |
|------------|---------|----------|
| `arxiv` | Search & read arXiv papers | Yes |
| `scholar` | Search Semantic Scholar, citations | Yes |
| `paper-search` | Search arXiv/bioRxiv/medRxiv/PubMed/Google Scholar | Yes |
| `pdf-reader` | Read local PDF files | Yes |
| `playwright` | Fallback web search if APIs fail | Optional |

**Check step**: Call `ListMcpResourcesTool` to see what's currently connected. Map which servers are available.

**Install missing MCPs**:

1. Detect where the user installs MCPs:
   - Check `C:\Users\<user>\.claude\claude_desktop_config.json` (Claude Desktop)
   - Check `C:\Users\<user>\.claude\mcp.json` (Claude Code project)
   - Check `C:\Users\<user>\AppData\Roaming\Claude\mcp.json` (Claude Code user)
   - Print the detected location

2. Install each missing MCP server. Show each step:

```
[1/3] arxiv MCP — installing via Smithery...
      npx @anthropic-ai/mcp-installer add arxiv
[2/3] scholar MCP — already installed, skipping
[3/3] pdf-reader MCP — installing via Smithery...
      npx @anthropic-ai/mcp-installer add pdf-reader

All required MCPs ready.
```

3. If automatic install fails, print the exact command the user should run manually.

4. After install, verify by calling `ListMcpResourcesTool` again.

### Phase 2: Gather Papers

**If user provided papers** → fetch metadata for each:
```
--- Fetching Paper Metadata ---
[1/3] arXiv:2103.12345 → "Neural Mesh Segmentation with GNNs" (2021)
[2/3] arXiv:2205.67890 → "Point Cloud Understanding via Transformers" (2022)
[3/3] 10.1145/3456789 → "Geometry Processing Survey" (2020)
Done.
```

**If user has NO papers** → search automatically:
```
--- Searching for Papers ---
Topic: "neural mesh segmentation"
Searching arXiv... found 15 papers
Searching Semantic Scholar... found 23 papers
Ranking by relevance and citations...

Top candidates (show 5-8 papers with title, year, citations):
1. "Neural Mesh Segmentation..." (2023, 142 cites)
2. "Geometry Processing..." (2022, 89 cites)
...

Ask user: "I found these papers. Which ones should I use? You can reply with numbers (e.g., '1,3,5') or provide your own."
```

**Read papers** (for each confirmed paper):
```
--- Reading Papers ---
[1/5] Downloading and extracting key points from "Neural Mesh Segmentation..."
      - Problem: ...
      - Method: ...
      - Key result: ...
[2/5] ...
```

### Phase 3: Draft Introduction

Follow standard academic intro structure. Show the structure before writing:

```
--- Drafting Introduction ---
Structure:
  1. Hook (broad context)
  2. Problem statement (the gap)
  3. Related work (what others did, limitations)
  4. Our approach (how this work fills the gap)
  5. Contributions
  6. Paper roadmap

Drafting...
```

Ask the user for THE key differentiator of their work if not yet stated:
> Before I draft, what is the ONE thing your method does that prior work doesn't?

Then write the draft. Default length: ~800-1200 words, adjust per venue.

After drafting, mark citations with `[CITE:paper_id]` placeholders that will be resolved in Phase 5.

### Phase 4: Review & Polish

```
--- Reviewing Draft ---
- Citation coverage: 8/8 citations linked to papers
- Structure check: OK
- Flow check: transition between related work and our approach could be stronger
```

Ask the user for feedback. Iterate on specific sections rather than rewriting the whole thing.

### Phase 5: Generate References

```
--- Generating References ---
Format: APA 7th (user selected)
Extracting citations from draft...
Matching 8 citations to paper metadata...
All 8 matched.

References (APA 7th):
[1] Author, A. (Year). Title. Journal, Vol(Issue), pp.
[2] ...
```

Supported formats: **BibTeX**, **APA 7th**, **IEEE**, **MLA 9th**, **Chicago**, **ACM**.

If the user didn't specify a format, ask: "Which reference format? BibTeX / APA / IEEE / MLA / Chicago / ACM?"

### Phase 6: Citation Audit

```
--- Citation Audit ---
In-text citations:  8
Reference entries:  8
Orphan references:  0  (in bibliography but not cited)
Missing references: 0  (cited but not in bibliography)
Unsupported claims: 1  — line 45 claims "SOTA performance" without citation

All clear, except: add citation for the SOTA claim on line 45.
```

## Key Principles

- **Traceability first**: every citation must resolve to a real paper with verified metadata
- **No hallucinated papers**: never invent titles, authors, or DOIs — use search tools to verify
- **Narrative flow**: the intro tells a story — background → gap → solution → contributions
- **Show progress always**: print a header before each phase so the user knows exactly what's happening
- **Auto-search over asking**: if the user didn't provide papers, search automatically rather than asking them to find references themselves

## Reference Format Defaults

| Format    | Example entry |
|-----------|--------------|
| BibTeX    | `@article{key, author={...}, title={...}, ...}` |
| APA 7th   | Author, A. A. (Year). *Title*. Journal, Vol(Issue), pp. |
| IEEE      | [1] A. A. Author, "Title," *Journal*, vol. X, no. Y, pp. Z, Year. |
| MLA 9th   | Author, A. A. "Title." *Journal*, vol. X, no. Y, Year, pp. Z. |
| Chicago   | Author, A. A. "Title." *Journal* Vol, no. Issue (Year): Pages. |
| ACM       | A. A. Author. Year. Title. *J.* Vol, Issue (Year), Pages. |

## MCP Tools Referenced

- `mcp__arxiv__*` — search, abstract, full-text retrieval
- `mcp__scholar__*` — search papers, get citations/references, download PDFs
- `mcp__paper-search__*` — search across arXiv, bioRxiv, medRxiv, PubMed, Google Scholar
- `mcp__pdf-reader__read_pdf` — extract text from local PDFs
- `ListMcpResourcesTool` — check available MCP servers
