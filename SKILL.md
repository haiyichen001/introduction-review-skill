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

#### CRITICAL: Diplomatic Critique — Do Not Attack Prior Work

When pointing out limitations of existing research, use measured, evidence-based language. Never use aggressive or dismissive terms.

**Forbidden phrases (too harsh):**
- "X completely fails to..."
- "X ignores/neglects..."
- "X is fundamentally flawed..."
- "X makes no attempt to..."
- "X is wrong about..."

**Recommended phrasing:**

| Instead of | Use |
|------------|-----|
| X failed to consider Y | X did not account for Y / Y was not within the scope of X |
| X's method is wrong | X's approach has limitations when applied to... |
| Nobody has studied this | Few studies have explored... / Research on X remains limited |
| X is inadequate | X leaves room for improvement in... / X may not fully capture... |
| X ignores Z | Prior work has primarily focused on A rather than Z |

**Structural patterns for diplomatic critique:**

1. **Acknowledge then extend**: "While Smith [1] demonstrated the effectiveness of GNNs on manifold meshes, their evaluation was limited to synthetic datasets. Real-world scans introduce additional challenges such as noise and missing data that warrant further investigation."

2. **Compare, don't condemn**: "Method A [2] achieves high accuracy but requires manual parameter tuning, whereas method B [3] is fully automatic but trades off precision. Neither fully addresses the need for an adaptive, high-precision automated solution."

3. **Scope limitation, not failure**: "The scope of [4] was limited to single-object scenes. Multi-object segmentation introduces inter-object occlusion, a scenario not addressed in that work."

4. **Cite self-admitted limitations**: "As noted by the authors themselves [5], their approach does not scale beyond 10K vertices."

### Phase 4: Review & Polish

**Before showing the draft to the user, the skill MUST proactively ask whether to run the numbering pass.** Do NOT wait for the user to remember — most users forget.

Use `AskUserQuestion`:

```
Question: "Content looks stable. Ready to convert [CITE:key] placeholders to [1][2][3] numbers and generate the reference list?"
Options:
  - "Yes, generate numbers" (Recommended)
  - "Not yet, let me review placeholders first"
```

If user chooses "Yes", run the numbering pass using `scripts/cite_scan.py`. This is deterministic — no LLM guessing. Run the script and stream its output directly to the user:

```
--- Running Numbering Pass (cite_scan.py) ---
```
→ Execute: `python scripts/cite_scan.py <draft_file>`
→ OR: `echo "<draft_text>" | python scripts/cite_scan.py` if draft is in-memory

The script outputs step-by-step:
  1. Scans for all [CITE:xxx] placeholders, prints each in order of first appearance
  2. Builds and prints the mapping table (placeholder → number)
  3. Replaces each occurrence one by one, marking reuse
  4. Outputs the complete numbered text

Stream the script's stdout to the user in real-time. The script prints everything — scan order, mapping, replacements, numbered text. After the script completes, run it again with `--json` to get structured data for Phase 5 reference generation.

If user chooses "Not yet", show the draft with placeholders visible for their review.

**After any edit that touches citations**, ask again: "Citation order changed. Renumber now?" If yes, re-run `cite_scan.py` — it renumbers from scratch.

**Edit workflow**:
1. Revert affected section to placeholder form → 2. Edit with `[CITE:key]` → 3. `python scripts/cite_scan.py <file>` → 4. Regenerate reference list from JSON → 5. Show updated draft

Ask the user for feedback. Iterate on specific sections rather than rewriting the whole thing.

### Phase 5: Generate References

The reference list is auto-generated from the placeholder mapping table after each numbering pass. No manual formatting.

Determine the correct format based on the user's target venue. See the [Citation Format Reference](#citation-format-reference-by-venue) section below for detailed rules.

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

## Citation Format Reference by Venue

### General Principle: Sequential Numbering

All numbered citation systems (IEEE, Vancouver, GB/T 7714, EI, most SCI journals) follow the same core rule:

> **References are numbered in the order they first appear in the text. The reference list at the end mirrors this order. A source keeps the same number every time it is cited.**

### Citation Format Comparison by Venue

| Venue | In-Text Style | Multiple Cites | Reference List Order | Note |
|-------|--------------|----------------|---------------------|------|
| **IEEE** | `[1]` square brackets, inline on text line | `[1,3,5]` or `[1]-[3]` for consecutive | Sequential by appearance | Widely used in engineering, CS |
| **SCI (Vancouver)** | `[1]` or `(1)` depending on journal | `[1,2]` or `[1-3]` | Sequential by appearance | Common in biomedical/physical sciences |
| **SCI (Elsevier numeric)** | `[1]` square brackets | `[1,2,5]` or `[1-3]` | Sequential by appearance | Most Elsevier journals |
| **EI Journal** | `[1]` square brackets, sequential | `[1,2]` or `[1-3]` | Sequential by appearance | 4-8 references minimum recommended |
| **Chinese Thesis (GB/T 7714)** | `[1]` square brackets, or superscript `¹` | `[1,2]` or `[1-3]` for consecutive | **Sequential by appearance** (顺序编码制) | See detailed rules below |
| **APA 7th** | `(Author, Year)` parenthetical | `(Smith, 2020; Jones, 2021)` | **Alphabetical by author** | Not a numbered system; not recommended for theses |
| **MLA 9th** | `(Author Page)` | — | Alphabetical | Humanities |
| **Chicago** | Footnotes or author-date | — | Alphabetical (author-date) or by footnote order | History, arts |
| **ACM** | `[1]` square brackets | `[1,2]` | Sequential by appearance | Computing |

### IEEE Detailed Rules

- In-text: Bracketed numbers `[1]`, inline (not superscript), before punctuation, space before bracket: `...as shown in [1].`
- Reference list: Numbered `[1]`, `[2]`, `[3]`... in order of first appearance
- Author format: Initials + Last name (e.g., `J. Smith`). Up to 6 authors listed, then `et al.`
- Journal article: `[#] A. Author, "Title," *Journal Abbrev.*, vol. X, no. Y, pp. Z, Year.`
- Conference: `[#] A. Author, "Title," in *Proc. Conf. Name*, City, Year, pp. X-Y.`
- Same source reused: use the original number. Do NOT renumber.

### SCI / Vancouver Detailed Rules

- In-text: Numbers in `[1]` brackets or `(1)` parentheses. Check journal Guide for Authors.
- Sequential numbering by first appearance.
- Author format: Last name + Initials. Up to 6 authors, then `et al.`
- Journal titles abbreviated per Index Medicus / NLM.
- Journal article: `[#] Author AB, Author CD. Title. *J Abbrev.* Year;Vol(Issue):Pages.`
- Some Elsevier journals use "numeric, with titles" style — includes article titles in the reference.

### EI Journal Detailed Rules

- In-text: `[1]`, `[2]`, `[3]` square brackets, sequential. NOT author-year, NOT footnotes/endnotes.
- Reference list: sequential numbering matching text order.
- Minimum 4-8 references recommended.
- Journal: `[#] Author, "Title," *Journal Name*, vol. X, no. Y, pp. Z, Year.`
- Conference: `[#] Author, "Title," *Conference Name*, pp. X-Y, Date.`
- Book: `[#] Author, *Title*, Edition. City: Publisher, Year, pp. X-Y.`
- EI收录的中文期刊：优先使用英文题名著录。

### Chinese Thesis (GB/T 7714-2015) Detailed Rules

Chinese academic theses follow the national standard **GB/T 7714-2015** (现行有效, 2025年仍适用).

**Two systems exist**:
1. **顺序编码制 (Sequential Numbering)** — Most common for theses. Citations numbered `[1]`, `[2]`, `[3]` in order of first appearance.
2. **著者-出版年制 (Author-Year)** — Less common. Uses `(Author, Year)` format.

**For theses using 顺序编码制**:

- **In-text citation placement**:
  - 右上角标形式 (superscript): `...已有研究¹表明...`
  - 正文行内方括号: `...已有研究[1]表明...`
  - 引用连续文献: `[1-3]` (consecutive numbers joined by hyphen)
  - 引用不连续文献: `[1,3,5]` (non-consecutive numbers separated by comma)
  - 同时引用连续和不连续: `[1-3,5]`

- **Reference list format** (sequential order matching text):

| 文献类型 | 格式 |
|----------|------|
| 期刊 [J] | `[序号] 作者. 题名[J]. 刊名, 年, 卷(期): 起止页码.` |
| 专著 [M] | `[序号] 作者. 书名[M]. 出版地: 出版社, 年: 页码.` |
| 会议 [C] | `[序号] 作者. 题名[C]. 会议名, 地点, 年: 页码.` |
| 学位论文 [D] | `[序号] 作者. 题名[D]. 学校所在地: 学校, 年.` |
| 专利 [P] | `[序号] 专利权人. 专利名[P]. 专利号, 日期.` |
| 电子资源 [EB/OL] | `[序号] 作者. 题名[EB/OL]. [引用日期]. URL.` |

- **Author formatting**: 3 authors or fewer → list all. More than 3 → list first 3 + "等" (or "et al." for English).
- **English author names**: Last name first, initials after. Example: `Smith J, Jones A B, Lee C, et al.`
- **Bilingual references**: If required, cite in original language first, then in translation.

### APA 7th (Author-Year) — For Reference

APA is NOT a numbered system. References are alphabetical by author last name. Only use APA if:
- The user explicitly requests it
- The target journal requires APA
- The user is in psychology, social sciences, education

**In-text**: `(Smith, 2020)` or `Smith (2020)`
**Reference list**: Alphabetical by author, not numbered.
**Multiple citations**: `(Smith, 2020; Jones, 2021)` — alphabetical, separated by semicolons.

### Determining Which Format to Use

Ask the user (or infer from context):

| User says | Apply |
|-----------|-------|
| "学位论文" / "毕业论文" / "硕士论文" / "博士论文" | GB/T 7714 顺序编码制 |
| "IEEE 期刊" / "IEEE 会议" | IEEE |
| "SCI 期刊" / "Elsevier" / "Springer" | Vancouver / Elsevier numeric |
| "EI 期刊" / "EI 会议" | EI sequential numbering |
| "APA" / "心理学期刊" | APA 7th |
| "BibTeX" / "LaTeX" | BibTeX |

---

## Diplomatic Critique Phrase Bank

### Highlighting Gaps (Not Failures)

| Situation | Recommended Phrasing |
|-----------|---------------------|
| A topic is understudied | "Few studies have explored..." / "Research on X remains limited..." |
| A method has a limitation | "While effective for [scenario A], this approach may not generalize to [scenario B]..." |
| Conflicting findings exist | "Findings on X remain inconclusive. Smith [1] reports A, whereas Jones [2] finds B, suggesting that..." |
| A study used small data | "The generalizability of these findings is constrained by the limited sample size..." |
| An assumption is restrictive | "This framework operates under the assumption that..., which may not hold in..." |
| A method is outdated | "Early approaches to X primarily relied on [old method]. Recent advances in [new method] offer opportunities to..." |
| Results are inconsistent | "There is no consensus on X. Studies using method A report Y [1,2], while those using method B find Z [3]." |

### Acknowledging Contributions Before Critiquing

Always pair criticism with acknowledgment. The structure is: "X achieved [positive], however/although/despite [limitation]."

- "Smith [1] pioneered the use of GNNs for mesh segmentation, achieving state-of-the-art results on clean synthetic data. However, their method assumes watertight input meshes, which rarely occur in real-world 3D scans."
- "The dataset introduced by Jones [2] has become a standard benchmark. While comprehensive, it focuses exclusively on indoor objects and does not represent outdoor or large-scale scenes."
- "Lee [3] proposed an elegant solution for real-time segmentation. The trade-off is a 15% drop in accuracy compared to offline methods, which may be unacceptable for precision-critical applications."

### DO NOT Use These Phrases

- "To the best of our knowledge, no prior work has..." → Replace with "We are not aware of prior work that specifically addresses..." (softer, and factually honest)
- "X fails to..." → Replace with "X does not..."
- "X is unable to..." → Replace with "X is not designed to handle..."
- "X ignores..." → Replace with "X does not account for..."
- "Surprisingly, X did not consider..." → Remove "Surprisingly" — it reads as condescending
- "It is astonishing that..." → Never use. Subjective, unprofessional.

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

**Scripts** (deterministic, no LLM guessing):
- `scripts/cite_scan.py` — placeholder scanner + numbering pass engine. Always use this for numbering, never do it manually.
