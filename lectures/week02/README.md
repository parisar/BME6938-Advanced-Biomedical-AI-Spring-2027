# Week 2: Self-supervised representation learning

| Session | Content |
|---|---|
| Tue Jan 19 | Self-supervised representation learning, with three animation clips |
| Thu Jan 21 | Paper sessions: [He et al., Masked Autoencoders Are Scalable Vision Learners](https://arxiv.org/abs/2111.06377) and [Zhou et al., A foundation model for generalizable disease detection from retinal images (RETFound)](https://doi.org/10.1038/s41586-023-06555-x) |

## Animation clips

The running example is a single-lead ECG. The signal is synthetic, generated in code, so no patient data is used. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. Masked reconstruction: learning by filling in gaps | [1 min 25 s](clips/narrated/week02-clip1-masked-reconstruction-narrated.mp4) | [49 s](clips/silent/week02-clip1-masked-reconstruction.mp4) |
| 2. Contrastive learning: two views, one embedding | [1 min 28 s](clips/narrated/week02-clip2-contrastive-learning-narrated.mp4) | [51 s](clips/silent/week02-clip2-contrastive-learning.mp4) |
| 3. Linear probing: what did the encoder learn? | [1 min 17 s](clips/narrated/week02-clip3-linear-probing-narrated.mp4) | [42 s](clips/silent/week02-clip3-linear-probing.mp4) |

The narration is an AI-generated voice reading a script written for the course. The source code for the clips is in [animations/](animations/) and the narration script is in [clips.json](clips.json).
