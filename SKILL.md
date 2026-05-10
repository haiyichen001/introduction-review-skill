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

### CRITICAL: Streaming Output Rule — Every Phase

**Every phase below MUST produce live, step-by-step output. NEVER print a static summary all at once. The user must SEE each sub-step happening.**

Example pattern for every operation:
```
--- Phase X: Name ---
[1/N] doing thing A...
[2/N] thing A done ✓
[3/N] doing thing B...
[4/N] thing B done ✓
Complete.
```

This applies to: fetching papers, reading papers, drafting sections, running numbering passes, generating references, auditing citations. Every operation that involves multiple items MUST show each item being processed.

### Phase 0: Check & Install MCP Tools

**This runs FIRST. You MUST execute each check with an actual tool call — NOT just print a summary. The user must see each line appear one at a time as the check happens.**

**Execution protocol (DO NOT SKIP):**

Step 0: Print the banner.
Step 1: Print `Checking required tools...`
Step 2: For EACH of the 4 required MCPs, do a real check (call `ListMcpResourcesTool` with the server name, or check the system prompt for `mcp__<server>__*` tools). After EACH check, print the result line immediately. Do NOT batch.
Step 3: If all 4 pass, print `All required MCPs ready.`
Step 4: If any is missing, install it (detect config path, run installer), showing progress per tool.

**Required output format (one line at a time):**

```
=== Introduction Review Skill ===
Checking required tools...
  arxiv ........................................ found ✓
  scholar ...................................... found ✓
  paper-search ................................. found ✓
  pdf-reader ................................... found ✓
All required MCPs ready.
```

**If a tool is missing**, replace the `found ✓` line with:

```
  arxiv ........................................ missing ✗ — installing via Smithery...
                                          npx @anthropic-ai/mcp-installer add arxiv
  arxiv ........................................ done ✓
```

**Required MCP servers (4 total):**

| MCP Server | Check method |
|------------|-------------|
| `arxiv` | Look for `mcp__arxiv__*` in available tools |
| `scholar` | Look for `mcp__scholar__*` in available tools |
| `paper-search` | Look for `mcp__paper-search__*` in available tools |
| `pdf-reader` | Look for `mcp__pdf-reader__*` in available tools |

**Install missing MCPs**:

1. Detect where the user installs MCPs:
   - Check `C:\Users\<user>\.claude\claude_desktop_config.json` (Claude Desktop)
   - Check `C:\Users\<user>\.claude\mcp.json` (Claude Code project)
   - Check `C:\Users\<user>\AppData\Roaming\Claude\mcp.json` (Claude Code user)

2. Install: `npx @anthropic-ai/mcp-installer add <server-name>`

3. If automatic install fails, print the exact command the user should run manually.

4. Verify again after install.

### CRITICAL: Flexible Routing — User Demand Drives the Flow

**Phases are NOT strict 0→1→2→... This is NOT a pipeline. It's a menu.**

The user may arrive with any need. Detect it and jump directly to the right phase. The full sequence only applies when the user starts from scratch with just a topic.

**CRITICAL: Token efficiency rule — NEVER search for papers if the user already has them.**
- User gave paper IDs, a draft, or reference list → DO NOT call any search API. Waste of tokens.
- User gave only a vague topic and nothing else → search is necessary. Proceed to Phase 2.

Valid entry points and direct jumps:

| User says | Jump to | Search? |
|-----------|---------|---------|
| "帮我搜XXX相关的论文" | Phase 2 (search papers) | Yes — user explicitly asked to search |
| "帮我写topic的introduction" + no papers | Phase 0→1→2→3 | Yes — no papers provided |
| "我有几篇论文，帮我写intro" + gives IDs | Phase 1→2(fetch metadata only)→3 | No — just fetch the given IDs |
| "帮我改这段intro" + pastes draft | Phase 3 (edit mode) → 4 | No — draft is right there |
| "帮我格式化参考文献" + gives list | Phase 5 | No — data provided |
| "检查引用有没有问题" + gives draft+refs | Phase 6 | No — data provided |
| "把这段intro里的引用从APA改IEEE" | Phase 5 (reformat) | No — just reformat |
| "我删了一篇引用，帮我重新编号" | Phase 4 (renumber) | No — just renumber |

**Rule**: Ask "does the user already have the content?" If yes, work with what's given. Only search when there's nothing to work from.

### Phase 1: Detect Intent

**Analyze user input and route to the correct phase. Show the analysis process.**

```
--- Detecting Intent ---
Input type: [draft / paper IDs / topic only / reference request / audit request]
Target venue: [detected or unspecified]
Action: jump to Phase [N]
```

Stream the detection steps:
1. Scan input for file paths, DOIs, arXiv IDs, pasted text
2. Check for venue keywords (学位论文, IEEE, SCI, EI, etc.)
3. Determine the minimal phase needed
4. Print the routing decision

```
--- Detecting Intent ---
  Scanning for drafts or file paths... [found: pasted text]
  Scanning for paper IDs (DOI, arXiv)... [found: 3 IDs]
  Scanning for venue keywords... [found: "IEEE"]
  Routing decision: Phase 2 (fetch paper metadata) → Phase 3 (draft with IEEE style)
```

### Phase 2: Gather Papers

**If user provided papers** → fetch metadata one by one, printing after each:
```
--- Fetching Paper Metadata ---
[1/3] arXiv:2103.12345 → fetching... "Neural Mesh Segmentation with GNNs" (2021) ✓
[2/3] arXiv:2205.67890 → fetching... "Point Cloud Understanding via Transformers" (2022) ✓
[3/3] 10.1145/3456789 → fetching... "Geometry Processing Survey" (2020) ✓
Done.
```

**If user has NO papers** → search automatically, print each source as it completes:
```
--- Searching for Papers ---
Topic: "neural mesh segmentation"
Searching arXiv... found 15 papers ✓
Searching Semantic Scholar... found 23 papers ✓
Merging, removing duplicates, ranking by citation count...
Top 6 candidates:
  1. "Neural Mesh Segmentation with Deep Learning" (2023, 142 cites)
  2. "3D Geometry Processing: A Survey" (2022, 89 cites)
  3. "Point Cloud Understanding via Transformers" (2023, 76 cites)
  4. "Graph Neural Networks for Mesh Analysis" (2021, 210 cites)
  5. "Hybrid Geometric Deep Learning" (2024, 34 cites)
  6. "Real-time Mesh Segmentation on Mobile Devices" (2023, 28 cites)
```

Then use `AskUserQuestion`: "Which papers should I use? Select by number (e.g., 1,3,5)."

**Read papers** — process one at a time, extracting structured notes:
```
--- Reading Papers ---
[1/4] "Neural Mesh Segmentation..." → downloading full text... extracting key points ✓
      Problem: semantic segmentation of 3D meshes in wild
      Method: GNN + attention on mesh edges
      Key result: 94.3% accuracy on ShapeNet, fails on non-manifold meshes
      Relationship: baseline for mesh-based approach, your method handles non-manifold cases

[2/4] "Point Cloud Understanding..." → downloading full text... extracting key points ✓
      ...
```

### Phase 3: Draft Introduction / Literature Review

Follow standard academic intro structure. Show the structure before writing:

```
--- Drafting Introduction ---
Structure: Hook → Problem Statement → Related Work → Our Approach → Contributions → Roadmap

[1/6] Writing hook (broad context)... ✓
[2/6] Writing problem statement (the gap)... ✓
[3/6] Writing related work with [CITE:xxx] placeholders... ✓
[4/6] Writing our approach... ✓
[5/6] Writing contributions... ✓
[6/6] Writing roadmap... ✓
Draft complete. 8 unique placeholders used.
```

Ask the user for THE key differentiator of their work if not yet stated:
> Before I draft, what is the ONE thing your method does that prior work doesn't?

Then write the draft. Default length: ~800-1200 words, adjust per venue.

#### CRITICAL: Placeholder System — Never Hardcode Citation Numbers

**This is the most important mechanism in this skill. It solves the problem of renumbering when citations are added, removed, or reordered.**

During drafting and editing, ALWAYS use symbolic placeholders — NEVER write `[1]`, `[2]`, `[3]` directly into the text. The numbering pass happens AFTER the content is stable.

**Placeholder format**: `[CITE:lastnameYEAR]` (lowercase, no spaces)

```
Drafting example:
"Neural mesh segmentation has been widely studied [CITE:smith2023].
Point cloud methods offer an alternative [CITE:jones2022].
Smith et al. built on earlier mesh-based work [CITE:smith2023]
to propose a hybrid approach [CITE:lee2021]."
```

**Internal mapping table** — maintained throughout the session:

| Placeholder | Paper | First Appears At | Assigned # |
|-------------|-------|------------------|------------|
| `[CITE:smith2023]` | Smith et al., "Mesh Segmentation with GNNs" (2023) | Paragraph 2 | (pending) |
| `[CITE:jones2022]` | Jones & Lee, "Point Cloud Understanding" (2022) | Paragraph 3 | (pending) |
| `[CITE:lee2021]` | Lee et al., "Hybrid Segmentation" (2021) | Paragraph 3 | (pending) |

**Numbering pass** (run after draft is confirmed, or after any edit that changes citation order):

1. Scan the draft text left-to-right for first occurrence of each distinct placeholder
2. Assign `[1]` to the first distinct placeholder that appears, `[2]` to the second, etc.
3. Replace all occurrences of each placeholder with its assigned number
4. The reference list is auto-generated in `[1]`, `[2]`, `[3]`... order matching the numbering

```
After numbering pass:
"Neural mesh segmentation has been widely studied [1].
Point cloud methods offer an alternative [2].
Smith et al. built on earlier mesh-based work [1]
to propose a hybrid approach [3]."

Reference list:
[1] J. Smith et al., "Mesh Segmentation with GNNs," ...
[2] A. Jones and B. Lee, "Point Cloud Understanding," ...
[3] C. Lee et al., "Hybrid Segmentation," ...
```

**Renumbering after edits** — when the user adds or removes a citation:

1. If a new placeholder is added → insert it into the mapping table → re-run the FULL numbering pass. All numbers may shift. This is expected and the system handles it.
2. If a placeholder is removed → delete it from the mapping table → re-run the FULL numbering pass.
3. The reference list is always regenerated from scratch after each numbering pass.

```
Example: User adds a new citation [CITE:wang2024] before [CITE:smith2023].

Before: [CITE:smith2023]→[1], [CITE:jones2022]→[2], [CITE:lee2021]→[3]
After:  [CITE:wang2024]→[1], [CITE:smith2023]→[2], [CITE:jones2022]→[3], [CITE:lee2021]→[4]

All numbers shifted. Reference list regenerated.
```

**The user NEVER manually types citation numbers. The system always assigns them.**

When showing the draft to the user for review, show the numbered version (after running the numbering pass). But internally, always work with placeholders. If the user requests an edit, revert to placeholder mode, make the change, re-run numbering.

#### CRITICAL: Citation Numbering Rules

**After the numbering pass, citations MUST be in strict sequential order of first appearance in the text.**

- The first paper cited in the body text gets `[1]`, the second distinct paper cited gets `[2]`, etc.
- Once a paper is assigned a number, reuse that number every time you cite it again.
- Never skip numbers. Never assign a higher number before a lower one.
- The reference list at the end MUST also be ordered `[1]`, `[2]`, `[3]`... matching the in-text order.

**Correct:**
```
Neural mesh segmentation has been widely studied [1]. Point cloud methods
offer an alternative [2]. Smith et al. built on earlier mesh-based work [1]
to propose a hybrid approach [3].
Reference list: [1]..., [2]..., [3]...
```

**Wrong:**
```
Neural mesh segmentation [3]... Point cloud methods [1]...  ← numbers out of order
```

#### CRITICAL: Citation Group Size Limit

**Grouped citations `[1,3,5]` or `[1-5]` are allowed, but with strict limits.**

- **Default max**: 3 papers per citation bracket (e.g., `[1,2,4]` or `[1-3]`)
- **Absolute max**: 5 papers per bracket — never exceed this
- **If the draft needs more than 3 citations at one point**: MUST use `AskUserQuestion` to confirm with the user. Let them choose which papers to keep or approve the larger group.

AskUserQuestion format:
```
Question: "This claim currently cites 6 papers [3-8]. Keep all 6, or select up to 5?"
Options:
  - "Keep the first 3: [3-5]"
  - "Keep the last 3: [6-8]"
  - "Keep all 6 (override, max 5 allowed but user approved)"
  - "Let me choose manually"
```

**Correct (each claim → specific supporting papers):**
```
Smith [1] proposed a graph-based segmentation method. However, their approach
assumes watertight meshes, which limits applicability to real-world scans [2,3].
```

**Avoid (unrelated claims bundled into one bracket):**
```
Segmentation is important. GNNs are good for meshes. Transformers handle
point clouds well. Recent methods combine both [1-4].
```
— This is wrong not because of the number, but because each sentence should cite the paper(s) supporting THAT specific statement.

**When to group citations**: Multiple papers that independently support the SAME claim can share a bracket. Example: `Several studies [4-7] have confirmed this finding.` If this exceeds 3, ask the user.

#### Guideline: Diplomatic Critique (NOT a Hard Rule)

**This is a guideline, not a requirement.** Adjust tone to your field and the actual situation.

General principle: critique the work, not the authors. Point out limitations with evidence, not emotion. But if a paper genuinely has serious methodological flaws or the field norms are direct, use straightforward language.

The phrase bank in `references/diplomatic-critique.md` is a reference, not a straitjacket. Use common sense — some papers do ignore obvious factors, some methods are wrong for a specific task. Say what's true.

### Phase 4: Review & Polish

**Before showing the draft to the user, the skill MUST proactively ask whether to run the numbering pass.** Do NOT wait for the user to remember — most users forget.

Use `AskUserQuestion`:

```
Question: "Content looks stable. Ready to convert [CITE:key] placeholders to [1][2][3] numbers and generate the reference list?"
Options:
  - "Yes, generate numbers" (Recommended)
  - "Not yet, let me review placeholders first"
```

If user chooses "Yes", run the numbering pass with `cite_live.py` (three rich-formatted tables):

→ Save the draft with placeholders to a temp file.
→ Run: `python scripts/cite_live.py <draft_file>`

The script outputs three progressive tables:
  **Step 1/3 — Citation Scan**: all [CITE:xxx] found, in first-appearance order
  **Step 2/3 — Number Assignment**: mapping table # | Key | Paper | Meta
  **Step 3/3 — Numbered Text**: full draft with [1][2][3]... citations

Parse the trailing JSON for Phase 5 reference generation.

If user chooses "Not yet", show the draft with placeholders visible for their review.

**After any edit that touches citations**, ask again: "Citation order changed. Renumber now?" If yes, re-run `cite_scan.py` — it renumbers from scratch.

**Edit workflow**:
1. Revert affected section to placeholder form → 2. Edit with `[CITE:key]` → 3. `python scripts/cite_scan.py <file>` → 4. Regenerate reference list from JSON → 5. Show updated draft

Ask the user for feedback. Iterate on specific sections rather than rewriting the whole thing.

### Phase 5: Generate References

The reference list is auto-generated from the placeholder mapping table after each numbering pass. No manual formatting.

**Load `references/citation-formats.md` for detailed formatting rules per venue** (IEEE, SCI/Vancouver, EI, GB/T 7714, APA, MLA, Chicago, ACM).

```
--- Generating References ---
Venue detected: IEEE Conference
Format: IEEE (sequential numbering, square brackets)

Generating each reference entry one by one...
  [1/5] Smith et al. → formatted as IEEE journal article ✓
  [2/5] Jones & Lee  → formatted as IEEE conference paper ✓
  [3/5] Lee et al.   → formatted as IEEE journal article ✓
  [4/5] Wang et al.  → formatted as IEEE conference paper ✓
  [5/5] Brown et al. → formatted as IEEE journal article ✓
All 5 references formatted.

References (IEEE):
[1] J. Smith et al., "Mesh Segmentation with GNNs," IEEE Trans. Vis. Comput. Graph., vol. 27, pp. 1234-1245, 2023.
[2] A. Jones and B. Lee, "Point Cloud Understanding via Transformers," in Proc. CVPR, 2022, pp. 567-570.
...
```

**If the user edits citations in Phase 4**, the reference list is regenerated automatically after the re-numbering pass.

If the user didn't specify a format, ask: "Which target venue? Options: IEEE / SCI Journal / EI Journal / Chinese Thesis / APA / MLA / Chicago / BibTeX (LaTeX)."

### Phase 6: Citation Audit

```
--- Citation Audit ---
Running 7 checks one by one...
  [1/7] Placeholder resolution... 5/5 resolved, 0 orphan ✓
  [2/7] In-text citation count... 5 ✓
  [3/7] Reference entry count... 5 ✓
  [4/7] Sequential order check... [1]→[2]→[3]→[4]→[5], no gaps ✓
  [5/7] Orphan reference check... 0 orphan (all refs cited in text) ✓
  [6/7] Citation group size... max 3 per bracket, all within limit ✓
  [7/7] Tone check... no forbidden phrases detected ✓
  Extra: Unsupported claims... line 45 "SOTA" has no citation ⚠

All checks passed. 1 warning: add citation for the SOTA claim on line 45.
```

---

## Key Principles

- **Placeholder system**: draft and edit with `[CITE:lastnameYEAR]` placeholders, never hardcoded numbers. Numbering pass runs after content is stable. Renumbering is automatic when citations are added, removed, or reordered.
- **Sequential numbering is law**: after the numbering pass, citations `[1]`, `[2]`, `[3]`... appear in strict order of first mention in the text. References at the end also numbered `[1]`, `[2]`, `[3]`... in that same order.
- **Citation group limit**: max 3 papers per bracket by default, absolute max 5. Exceeding 3 triggers `AskUserQuestion` confirmation.
- **Critique through comparison, not attack**: point out scope limitations and trade-offs, not failures. Use "while/however/although" structures.
- **Traceability first**: every citation must resolve to a real paper with verified metadata.
- **No hallucinated papers**: never invent titles, authors, or DOIs — use search tools to verify.
- **Show progress always**: print a header before each phase.
- **Auto-search over asking**: if the user didn't provide papers, search automatically.

## External Resources

**MCP Servers**:
- `mcp__arxiv__*` — search, abstract, full-text retrieval
- `mcp__scholar__*` — search papers, get citations/references, download PDFs
- `mcp__paper-search__*` — search across arXiv, bioRxiv, medRxiv, PubMed, Google Scholar
- `mcp__pdf-reader__read_pdf` — extract text from local PDFs
- `ListMcpResourcesTool` — check available MCP servers

**Reference files** (load on-demand when format/tone details needed):
- `references/citation-formats.md` — IEEE, SCI, EI, GB/T 7714, APA, MLA, Chicago, ACM format rules
- `references/diplomatic-critique.md` — phrase bank for diplomatic literature review writing

**Scripts** (deterministic, no LLM guessing):
- `scripts/cite_live.py` — **primary**: rich-formatted progressive tables (Scan → Mapping → Numbered Text), use in Phase 4
- `scripts/cite_scan.py` — plain-text version for headless/pipe usage
