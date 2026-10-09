# Week 3: Transformer review, Part 2: decoder, masking, and model families

| Session | Content |
|---|---|
| Tue Jan 26 | Transformer review, Part 2, with three animation clips |
| Thu Jan 28 | Paper sessions: [Luo et al., BioGPT: generative pre-trained transformer for biomedical text generation and mining](https://doi.org/10.1093/bib/bbac409) and [Dosovitskiy et al., An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale (ViT)](https://arxiv.org/abs/2010.11929) |

## Animation clips

The running examples are the clinical phrase "The patient denies chest pain" and a real H&E tile of colorectal cancer from an open dataset ([Kather et al. 2016](https://doi.org/10.5281/zenodo.53169), CC BY 4.0). The numbers match the slides. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. Generating text one token at a time | [1 min 14 s](clips/narrated/week03-clip1-next-token-generation-narrated.mp4) | [57 s](clips/silent/week03-clip1-next-token-generation.mp4) |
| 2. The causal mask | [1 min 11 s](clips/narrated/week03-clip2-causal-mask-narrated.mp4) | [55 s](clips/silent/week03-clip2-causal-mask.mp4) |
| 3. Vision transformer: an image as a sequence of patches | [1 min 36 s](clips/narrated/week03-clip3-vit-patches-narrated.mp4) | [50 s](clips/silent/week03-clip3-vit-patches.mp4) |

The narration is an AI-generated voice reading a script written for the course. The source code for the clips is in [animations/](animations/) and the narration script is in [clips.json](clips.json).

## Notebook

The ungraded reference notebook for this lecture is [week03_transformer_review_part2.ipynb](../notebooks/week03_transformer_review_part2.ipynb).
