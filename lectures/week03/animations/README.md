# Animation source

The Week 3 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_next_token_generation.py | C1 | Generating text one token at a time |
| clip2_causal_mask.py | C2 | The causal mask |
| clip3_vit_patches.py | C3 | Vision transformer: an image as a sequence of patches |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week03
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required. The H&E tile is in [`lectures/_shared/assets/`](../../_shared/assets/) with its attribution.
