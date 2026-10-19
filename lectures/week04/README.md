# Week 4: Inside modern LLMs: architectures in 2026

| Session | Content |
|---|---|
| Tue Feb 2 | Inside modern LLMs, with four animation clips |
| Thu Feb 4 | Paper sessions: [DeepSeek-AI, DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) and [Sellergren et al., MedGemma Technical Report](https://arxiv.org/abs/2507.05201) |

Slides: [4-1 slides (PDF)](slides/4-1-inside-modern-llms.pdf)

## Animation clips

The running example continues Week 3: a decoder writing the clinical note "The patient denies chest pain". Architecture numbers come from the published configurations of Qwen3-0.6B, Llama 3, DeepSeek-V3, and Gemma 3; the token splits come from the real GPT-2 and DeepSeek-V3 tokenizers. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. What changed since 2017 | [1 min 23 s](clips/narrated/week04-clip1-modern-block-narrated.mp4) | [39 s](clips/silent/week04-clip1-modern-block.mp4) |
| 2. The KV cache and how models shrink it | [1 min 32 s](clips/narrated/week04-clip2-kv-cache-narrated.mp4) | [46 s](clips/silent/week04-clip2-kv-cache.mp4) |
| 3. Mixture of experts | [1 min 21 s](clips/narrated/week04-clip3-mixture-of-experts-narrated.mp4) | [43 s](clips/silent/week04-clip3-mixture-of-experts.mp4) |
| 4. More 2026 changes | [1 min 17 s](clips/narrated/week04-clip4-more-changes-narrated.mp4) | [36 s](clips/silent/week04-clip4-more-changes.mp4) |

The narration is an AI-generated voice reading a script written for the course. Captions for the narrated clips are in a WebVTT file beside each video (`clips/narrated/*.vtt`), which covers WCAG 2.1 criterion 1.2.2; players that read sidecar subtitle files, such as VLC, load them automatically. The source code for the clips is in [animations/](animations/) and the narration script is in [clips.json](clips.json).

## Notebook

The ungraded reference notebook for this lecture is [week04_modern_llms.ipynb](../notebooks/week04_modern_llms.ipynb). It opens
Qwen3-0.6B and a small mixture-of-experts model (Granite 3.1 1B-A400M), and reproduces every number in the clips. It runs on
Colab or HiPerGator, on CPU or GPU.

## Further reading

- Raschka, [A Visual Guide to Attention Variants in Modern LLMs](https://magazine.sebastianraschka.com/p/visual-attention-variants), Ahead of AI, 2026
- Raschka, [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch): grouped-query attention, latent attention, sliding-window attention, and mixture of experts in code
