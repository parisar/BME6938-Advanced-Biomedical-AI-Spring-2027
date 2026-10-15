# Animation source

The Week 7 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers, including the H&E tile loader (`he_image`), are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_clip.py | C1 | CLIP: matching images with their captions |
| clip2_zero_shot.py | C2 | Zero-shot classification, and where it breaks |
| clip3_med_palm_m.py | C3 | Images as tokens: Med-PaLM M |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week07
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.

**Data sources.** The H&E tiles are from Kather et al. 2016 (CC BY 4.0; see [`_shared/assets/README.md`](../../_shared/assets/README.md)). The chest X-ray in clip 3 is a stylized drawing made in code, not a patient image. In clip 1, the 4 × 4 similarity grid and the figure caption are illustrative. In clip 2, the tumor tile's class probabilities, the zero-shot accuracies, and the linear-probe accuracies are real outputs of CLIP ViT-B/32 (OpenAI) and BiomedCLIP on all 5,000 Kather tiles, reproduced in the [Week 7 notebook](../../notebooks/week07_vision_language.ipynb). In clip 3, the CLIP scores and the report text are illustrative. Paper numbers are from Radford et al. (CLIP), Zhang et al. (BiomedCLIP), and Tu et al. (Med-PaLM M).
