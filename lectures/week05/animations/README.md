# Animation source

The Week 5 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_post_training.py | C1 | From pretrained model to clinical assistant |
| clip2_lora.py | C2 | LoRA: fine-tuning with a small fraction of the weights |
| clip3_preference_tuning.py | C3 | Preference tuning: RLHF and DPO |
| clip4_reasoning.py | C4 | Reasoning models |

Build all four clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week05
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required. Model outputs, log-probabilities, token counts, and LoRA shapes come from SmolLM2-360M and SmolLM2-360M-Instruct and are reproduced in the [Week 5 notebook](../../notebooks/week05_post_training.ipynb). MedQA accuracies are from Singhal et al. (Med-PaLM 2); the reward design and group size are from Guo et al. (DeepSeek-R1). The thinking text in clip 4, segment 1, the DPO gains, and the four GRPO samples are illustrative.
