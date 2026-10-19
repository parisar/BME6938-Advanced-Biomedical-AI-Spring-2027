# Week 7: Vision-language and multimodal models

| Session | Content |
|---|---|
| Tue Feb 23 | Project pitches (2 minutes each) and a short lecture on vision-language models with three animation clips |
| Thu Feb 25 | Paper sessions: [Radford et al., CLIP](https://proceedings.mlr.press/v139/radford21a.html) and [Tu et al., Med-PaLM M](https://doi.org/10.1056/AIoa2300138) |

Slides: [7-1 slides (PDF)](slides/7-1-vision-language-and-multimodal-models.pdf)

## Animation clips

The running example continues Week 6: H&E tiles of colorectal tissue from an open dataset ([Kather et al. 2016](https://doi.org/10.5281/zenodo.53169), CC BY 4.0). Clip 3 uses a stylized chest X-ray drawn in code, not a patient image. The zero-shot and linear-probe accuracies and the tumor tile's class probabilities in clip 2 are real outputs of CLIP ViT-B/32 and BiomedCLIP on all 5,000 Kather tiles, reproduced in the notebook. The similarity grid in clip 1 and the scores and report text in clip 3 are illustrative. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. CLIP: matching images with their captions | [1 min 43 s](clips/narrated/week07-clip1-clip-narrated.mp4) | [49 s](clips/silent/week07-clip1-clip.mp4) |
| 2. Zero-shot classification, and where it breaks | [1 min 58 s](clips/narrated/week07-clip2-zero-shot-narrated.mp4) | [47 s](clips/silent/week07-clip2-zero-shot.mp4) |
| 3. Images as tokens: Med-PaLM M | [1 min 52 s](clips/narrated/week07-clip3-med-palm-m-narrated.mp4) | [52 s](clips/silent/week07-clip3-med-palm-m.mp4) |

The narration is an AI-generated voice reading a script written for the course. Captions for the narrated clips are in a WebVTT file beside each video (`clips/narrated/*.vtt`), which covers WCAG 2.1 criterion 1.2.2; players that read sidecar subtitle files, such as VLC, load them automatically. The source code for the clips is in [animations/](animations/) and the narration script is in [clips.json](clips.json).

**Note for the lecture (clip 2).** On the Kather tiles, general CLIP's zero-shot accuracy is 5.6 to 15.1% depending only on the prompt wording, and chance is 12.5% for 8 classes, so the worst wording is below chance. A linear probe with 10 labels per class does far better on the same embeddings.

## Notebook

The ungraded reference notebook for this lecture is [week07_vision_language.ipynb](../notebooks/week07_vision_language.ipynb). It
follows the three clips: the CLIP loss on the 4 × 4 grid (0.82 and 0.18), BiomedCLIP on the clip's tiles, zero-shot
classification with CLIP and BiomedCLIP on all 5,000 Kather tiles with three prompt wordings, the linear probe, and a small open
vision-language model (SmolVLM-256M) that shows how an image becomes 64 tokens and how the loss is counted only on the report.
It runs on Colab or HiPerGator on CPU in about 10 minutes plus downloads.

## Further reading

- Radford et al., [Learning Transferable Visual Models From Natural Language Supervision](https://proceedings.mlr.press/v139/radford21a.html), ICML, 2021
- Zhang et al., [BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs](https://arxiv.org/abs/2303.00915), 2023
- Tu et al., [Towards Generalist Biomedical AI](https://doi.org/10.1056/AIoa2300138), NEJM AI, 2024
- Driess et al., [PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378), ICML, 2023
- Acosta et al., [Multimodal biomedical AI](https://doi.org/10.1038/s41591-022-01981-2), Nature Medicine, 2022
