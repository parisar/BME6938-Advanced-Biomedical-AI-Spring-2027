# Animation source

The Week 6 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers, including the synthetic ECG generator (`ecg_fn`, `wave`) and the H&E tile loader (`he_image`), are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_masked_reconstruction.py | C1 | Masked reconstruction: learning by filling in gaps |
| clip2_contrastive.py | C2 | Contrastive learning: two views, one embedding |
| clip3_linear_probe.py | C3 | Linear probing: what did the encoder learn? |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week06
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.
