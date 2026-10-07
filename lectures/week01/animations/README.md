# Animation source

The Week 1 clips are written with [Manim Community](https://www.manim.community/), the open-source animation library created for 3Blue1Brown. Each clip is one scene class; `kit.py` holds the shared colors, caption bar, token boxes, and matrix helpers that later weeks reuse.

Render one clip at 1080p, 30 fps:

```bash
pip install manim
manim -qh --fps 30 clip2_attention.py C2
```

| File | Scene | Clip |
|---|---|---|
| clip1_tokenization.py | C1 | Tokenization and embeddings |
| clip2_attention.py | C2 | Query, key, value: how attention works |
| clip3_encoder_block.py | C3 | Inside an encoder block |
| clip4_encoder_decoder.py | C4 | Encoder versus decoder, and masking |

The clips use only text objects, so LaTeX is not required. Manim needs the Pango and Cairo system libraries. The font is Inter; if it is not installed, Manim falls back to a default font.
