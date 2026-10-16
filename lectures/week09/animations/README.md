# Animation source

The Week 9 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_rag.py | C1 | Retrieval-augmented generation |
| clip2_react.py | C2 | Reason, act, observe: tool calls |
| clip3_compounding.py | C3 | Errors compound over steps |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week09
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.

**Data sources.** The protocols, the patient P-001, and its potassium values (4.6, 5.1, 5.6 mmol/L) are synthetic: no real patient data. The Almanac design (1,000-token chunks, 1,536-number embeddings, threshold λ = 0.83) and results (314 questions, first of four systems for factuality, completeness, and preference, 91% correct citations, 100% versus 77%, 70%, and 7% under adversarial prompts) are from Zakka et al., NEJM AI 2024; the fallback and abstention behaviors were checked against the published article and the arXiv preprint. The ReAct results (ALFWorld 71% versus 45%, best of six prompts; HotpotQA 27.4, 29.4, 33.4, and 35.1 exact match; failure modes from 50 hand-labelled failures per method) are from Yao et al., ICLR 2023. The similarity scores, the rattlesnake question, and the per-step success rates of 0.95 and 0.99 are illustrative.
