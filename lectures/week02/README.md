# Week 2: Transformer review, Part 1: attention and the encoder

| Session | Content |
|---|---|
| Tue Jan 19 | Transformer review, Part 1, with three animation clips |
| Thu Jan 21 | Paper sessions: [Devlin et al., BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://aclanthology.org/N19-1423/) and [Yang et al., A large language model for electronic health records (GatorTron)](https://doi.org/10.1038/s41746-022-00742-2) |

## Animation clips

The running example is the sentence "The patient has a cold", with the same numbers as the slides. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. From tokens to vectors | [1 min 25 s](clips/narrated/week02-clip1-tokens-to-vectors-narrated.mp4) | [59 s](clips/silent/week02-clip1-tokens-to-vectors.mp4) |
| 2. Attention for one token | [1 min 13 s](clips/narrated/week02-clip2-attention-one-token-narrated.mp4) | [55 s](clips/silent/week02-clip2-attention-one-token.mp4) |
| 3. Inside the encoder block | [1 min 20 s](clips/narrated/week02-clip3-encoder-block-narrated.mp4) | [55 s](clips/silent/week02-clip3-encoder-block.mp4) |

The narration is an AI-generated voice reading a script written for the course. The source code for the clips is in [animations/](animations/) and the narration script is in [clips.json](clips.json).

## Notebook

The ungraded reference notebook for this lecture is [week02_transformer_review_part1.ipynb](../notebooks/week02_transformer_review_part1.ipynb).
