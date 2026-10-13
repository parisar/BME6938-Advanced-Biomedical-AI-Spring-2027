# Animation source

The Week 4 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_modern_block.py | C1 | What changed since 2017 |
| clip2_kv_cache.py | C2 | The KV cache and how models shrink it |
| clip3_mixture_of_experts.py | C3 | Mixture of experts |
| clip4_more_changes.py | C4 | More 2026 changes |

Build all four clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week04
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required. Architecture numbers come from the published model configurations and reports (Qwen3-0.6B, DeepSeek-V3, Gemma 3, Llama 3); the token splits in clip 4 come from the real GPT-2 and DeepSeek-V3 tokenizers. The router weights and the 16 experts in clip 3 are illustrative.
