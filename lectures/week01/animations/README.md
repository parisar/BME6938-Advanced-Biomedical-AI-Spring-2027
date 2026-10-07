# Animation source

The Week 1 clips are written with [Manim Community](https://www.manim.community/), the open-source animation library created for 3Blue1Brown. Each clip is one scene class. The shared colors, caption bar, token boxes, and matrix helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py), and every week reuses them.

| File | Scene | Clip |
|---|---|---|
| clip1_tokenization.py | C1 | Tokenization and embeddings |
| clip2_attention.py | C2 | Query, key, value: how attention works |
| clip3_encoder_block.py | C3 | Inside an encoder block |
| clip4_encoder_decoder.py | C4 | Encoder versus decoder, and masking |

Build all four clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week01
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.
