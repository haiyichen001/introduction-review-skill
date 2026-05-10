# Diplomatic Critique Phrase Bank

> Loaded on-demand during Phase 3 (Drafting) and Phase 6 (Audit) when checking tone.

## Highlighting Gaps (Not Failures)

| Situation | Recommended Phrasing |
|-----------|---------------------|
| A topic is understudied | "Few studies have explored..." / "Research on X remains limited..." |
| A method has a limitation | "While effective for [scenario A], this approach may not generalize to [scenario B]..." |
| Conflicting findings exist | "Findings on X remain inconclusive. Smith [1] reports A, whereas Jones [2] finds B, suggesting that..." |
| A study used small data | "The generalizability of these findings is constrained by the limited sample size..." |
| An assumption is restrictive | "This framework operates under the assumption that..., which may not hold in..." |
| A method is outdated | "Early approaches to X primarily relied on [old method]. Recent advances in [new method] offer opportunities to..." |
| Results are inconsistent | "There is no consensus on X. Studies using method A report Y [1,2], while those using method B find Z [3]." |

## Acknowledging Contributions Before Critiquing

Always pair criticism with acknowledgment. The structure is: "X achieved [positive], however/although/despite [limitation]."

- "Smith [1] pioneered the use of GNNs for mesh segmentation, achieving state-of-the-art results on clean synthetic data. However, their method assumes watertight input meshes, which rarely occur in real-world 3D scans."
- "The dataset introduced by Jones [2] has become a standard benchmark. While comprehensive, it focuses exclusively on indoor objects and does not represent outdoor or large-scale scenes."
- "Lee [3] proposed an elegant solution for real-time segmentation. The trade-off is a 15% drop in accuracy compared to offline methods, which may be unacceptable for precision-critical applications."

## DO NOT Use These Phrases

- "To the best of our knowledge, no prior work has..." → Replace with "We are not aware of prior work that specifically addresses..." (softer, and factually honest)
- "X fails to..." → Replace with "X does not..."
- "X is unable to..." → Replace with "X is not designed to handle..."
- "X ignores..." → Replace with "X does not account for..."
- "Surprisingly, X did not consider..." → Remove "Surprisingly" — it reads as condescending
- "It is astonishing that..." → Never use. Subjective, unprofessional.
