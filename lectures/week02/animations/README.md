# Animation source

The Week 2 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_tokens_to_vectors.py | C1 | From tokens to vectors |
| clip2_attention_one_token.py | C2 | Attention for one token |
| clip3_encoder_block.py | C3 | Inside the encoder block |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week02
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.
