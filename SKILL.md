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

### Phase 0: Check & Install MCP Tools

**This runs FIRST, before anything else. Show each check individually with a checkmark so the user sees liveness — don't batch them all at once.**

Print the skill banner and check each tool one by one:

```
=== Introduction Review Skill ===
Checking required tools...
  arxiv ............... found ✓
  scholar ............. found ✓
  paper-search ........ found ✓
  pdf-reader .......... found ✓
All required MCPs ready.
```

Required MCP servers (4 total):

| MCP Server | Purpose | Required |
|------------|---------|----------|
| `arxiv` | Search & read arXiv papers | Yes |
| `scholar` | Search Semantic Scholar, citations | Yes |
| `paper-search` | Search arXiv/bioRxiv/medRxiv/PubMed/Google Scholar | Yes |
| `pdf-reader` | Read local PDF files | Yes |

**Check step**: Call `ListMcpResourcesTool` to see what's currently connected, then map each required server against available tools. Print each line as it completes — do NOT wait for all checks before showing output.

**If any MCP is missing**, output:

```
  arxiv ............... missing ✗ — installing...
```

Then install it:

1. Detect where the user installs MCPs:
   - Check `C:\Users\<user>\.claude\claude_desktop_config.json` (Claude Desktop)
   - Check `C:\Users\<user>\.claude\mcp.json` (Claude Code project)
   - Check `C:\Users\<user>\AppData\Roaming\Claude\mcp.json` (Claude Code user)
   - Print the detected location

2. Install and show progress:

```
  arxiv ............... installing via Smithery...
                        npx @anthropic-ai/mcp-installer add arxiv
                        done ✓
```

3. If automatic install fails, print the exact command the user should run manually.

4. After install, verify all tools again and print the final status block.

### Phase 1: Detect Intent

**Now analyze what the user provided.**

```
--- Detecting Intent ---
Analyzing your input...
```

| Signal | Intent | Next step |
|--------|--------|-----------|
| User provided a draft (pasted text / file path) | Has draft → review & polish | Jump to Phase 3 |
| User provided paper IDs (DOI, arXiv, title list) | Has papers → read & draft | Jump to Phase 2 |
| User only gave a topic or vague request | Starting from scratch | Continue to Phase 2, search automatically |
| User asked to "format references" or "check citations" | Reference-only task | Jump to Phase 5 |
| User mentioned a target venue (journal, conference, thesis) | Style constraint noted | Apply format rules in Phase 3 and 5 |

**If the user has NOT provided papers**: do NOT ask them to go find papers. Proceed to Phase 2 to search automatically.

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
      - Relationship to your work: ...
[2/5] ...
```

### Phase 3: Draft Introduction / Literature Review

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

If user chooses "Yes":
- Run the numbering pass
- Replace all placeholders with real numbers
- Generate the reference list
- Show the complete numbered draft

```
--- Numbering Pass ---
Scanning placeholder order...
  [CITE:smith2023] → first appears in paragraph 2 → assigned [1]
  [CITE:jones2022] → first appears in paragraph 3 → assigned [2]
  [CITE:lee2021]   → first appears in paragraph 3 → assigned [3]
All placeholders replaced. Reference list generated.

--- Reviewing Draft ---
- Citation numbering: OK (sequential [1]-[3])
- Citation coverage: 3/3 citations linked to papers
- Citation group size: all within limit
- Structure check: OK
- Tone check: all critiques use diplomatic language
- Flow check: transition between related work and our approach could be stronger
```

If user chooses "Not yet", show the draft with placeholders visible for their review.

**After any subsequent edit that touches citations**, the skill MUST proactively ask again: "Citation order changed. Renumber now?" Same two-option prompt as above.

**If user requests edits** (add/remove/reorder citations):
1. Revert the affected section back to placeholder form
2. Apply the edit with `[CITE:key]` placeholders
3. Re-run the numbering pass — ALL numbers may shift, this is expected
4. Regenerate the reference list
5. Show the updated draft

**If no citation changes**, iterate on wording directly.

Ask the user for feedback. Iterate on specific sections rather than rewriting the whole thing.

### Phase 5: Generate References

The reference list is auto-generated from the placeholder mapping table after each numbering pass. No manual formatting.

Determine the correct format based on the user's target venue. See the [Citation Format Reference](#citation-format-reference-by-venue) section below for detailed rules.

```
--- Generating References ---
Venue detected: IEEE Conference
Format: IEEE (sequential numbering, square brackets)
Mapping table → numbering pass → reference list:

  [CITE:smith2023] → [1] J. Smith et al., "Mesh Segmentation with GNNs," ...
  [CITE:jones2022] → [2] A. Jones and B. Lee, "Point Cloud Understanding," ...
  [CITE:lee2021]   → [3] C. Lee et al., "Hybrid Segmentation," ...

All 3 citations mapped. Reference list in sequential order.
```

**If the user edits citations in Phase 4**, the reference list is regenerated automatically after the re-numbering pass.

If the user didn't specify a format, ask: "Which target venue? Options: IEEE / SCI Journal / EI Journal / Chinese Thesis / APA / MLA / Chicago / BibTeX (LaTeX)."

### Phase 6: Citation Audit

```
--- Citation Audit ---
Placeholder check:       8 placeholders → 8 resolved → 0 orphan placeholders
In-text citations:       8
Reference entries:       8
Sequential order check:  PASS ([1]→[8], no gaps, no skipped numbers)
Orphan references:       0  (in reference list but not cited in text)
Missing references:      0  (cited in text but not in reference list)
Citation group size:     PASS (max 3 per bracket, all within limit)
Tone check:              PASS (all critiques diplomatically phrased)
Unsupported claims:      1  — line 45 claims "SOTA performance" without citation

All clear, except: add citation for the SOTA claim on line 45.
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

## MCP Tools Referenced

- `mcp__arxiv__*` — search, abstract, full-text retrieval
- `mcp__scholar__*` — search papers, get citations/references, download PDFs
- `mcp__paper-search__*` — search across arXiv, bioRxiv, medRxiv, PubMed, Google Scholar
- `mcp__pdf-reader__read_pdf` — extract text from local PDFs
- `ListMcpResourcesTool` — check available MCP servers
