# Week 11: Generative models and AI for science






![A structured chain, a partly noised chain, and a cloud of noise.](../../assets/banners/week11.png)

| Session | Content |
|---|---|
| Tue Mar 23 | Generative models and AI for science, with three animation clips |
| Thu Mar 25 | Paper sessions: [Watson et al., De novo design of protein structure and function with RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8) and [Abramson et al., Accurate structure prediction of biomolecular interactions with AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) |

Progress report due Fri Mar 26.

Slides: [11-1 slides (PDF)](slides/11-1-generative-models-and-ai-for-science.pdf)

## Animation clips

The running example is a short protein backbone drawn as a chain of 16 C-alpha points, illustrative rather than real
structural data. The schedule weights in clip 1 were recomputed from the standard DDPM schedule rather than quoted. The
RFdiffusion and AlphaFold 3 numbers in clips 2 and 3 are from the two Nature papers and were checked against them. The
guidance numbers in clip 3 (0.2, 0.5, w = 3) and all three drawn backbones are illustrative and marked as such on screen.
Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent (captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. Diffusion, part 1: adding noise | [1 min 37 s](clips/narrated/week11-clip1-forward-narrated.mp4) | [47 s](clips/silent/week11-clip1-forward.mp4) |
| 2. Diffusion, part 2: learning the way back | [2 min 5 s](clips/narrated/week11-clip2-reverse-narrated.mp4) | [54 s](clips/silent/week11-clip2-reverse.mp4) |
| 3. Diffusion, part 3: steering the sampler | [1 min 56 s](clips/narrated/week11-clip3-conditioning-narrated.mp4) | [50 s](clips/silent/week11-clip3-conditioning.mp4) |

The narration is an AI-generated voice reading a script written for the course. Captions for the narrated clips are in
a WebVTT file beside each video (`clips/narrated/*.vtt`), which covers WCAG 2.1 criterion 1.2.2; players that read
sidecar subtitle files, such as VLC, load them automatically. The source code for the clips is in
[animations/](animations/) and the narration script is in [clips.json](clips.json). The storyboard brief is in
[storyboard.md](storyboard.md).

**Note for the lecture (clip 2): the textbook reverse step is not what RFdiffusion does.** Standard DDPM sampling adds a
little fresh noise at every reverse step, which is what keeps samples diverse. RFdiffusion reports the opposite for
protein design: in 17 out of 23 of the problems, it generated successful solutions with higher in silico success rates
when noise was not added during the reverse diffusion trajectories. Less diversity is a fair price for more designs that
fold. The clip shows the textbook step first and then this result, in that order.

**Note for the lecture (clip 3): conditioning and guidance are different things.** Conditioning gives the denoiser
information it must respect at every step, such as fixed motif coordinates or a target structure. Classifier-free
guidance mixes a conditional and an unconditional prediction after the fact. RFdiffusion conditions; it does not use
classifier-free guidance. The clip states this on screen so that the guidance arithmetic is not mistaken for part of the
RFdiffusion method.

**Note for the lecture (clip 3): the in silico judge.** The 23 of 25 benchmark result is scored by AlphaFold-family
structure predictions, which are trained on the same structures as the designer. The numbers that do not depend on that
judgement are the experimental ones: 19% success across five targets, a 28 nM influenza hemagglutinin binder, and a
cryo-EM map matching the design to 0.63 Å. The notebook reproduces this problem on purpose, in miniature: its sample
quality is scored by a classifier trained on the same 4,000 synthetic chains that trained the diffusion model.

## Transcripts

Each clip also has a plain-text transcript of its narration in [clips/transcripts/](clips/transcripts/). The
transcript is the text alternative for the silent version, which has no audio track at all (WCAG 2.1 criterion 1.2.1),
and it is the quickest way to review what a clip says when revising.

| Clip | Transcript |
|---|---|
| 1. Diffusion, part 1: adding noise | [week11-clip1-forward.md](clips/transcripts/week11-clip1-forward.md) |
| 2. Diffusion, part 2: learning the way back | [week11-clip2-reverse.md](clips/transcripts/week11-clip2-reverse.md) |
| 3. Diffusion, part 3: steering the sampler | [week11-clip3-conditioning.md](clips/transcripts/week11-clip3-conditioning.md) |

## Notebook

The ungraded reference notebook for this lecture is [week11_diffusion.ipynb](../notebooks/week11_diffusion.ipynb). It
builds a complete diffusion model from scratch on a two-dimensional stand-in for a protein backbone: synthetic 16-point
chains that are either helix-like or hairpin-like. It recomputes the schedule weights from clip 1, trains a
153,000-parameter MLP denoiser in about 30 seconds on CPU, samples from pure noise, conditions on a fixed four-point
motif, and sweeps the guidance strength.

The measured results are reported as they came out, including where they disagree with the clips. Generated chains are
classified correctly 100% of the time by a rotation-invariant logistic regression, with bond lengths slightly short
(0.46 against 0.52 for helices, 0.74 against 0.77 for hairpins). Conditioning holds the motif to an RMSE of 0.026
against a mean coordinate magnitude of 0.80, but the twelve scaffolds generated for one motif spread only 0.65 apart
against 5.66 for free samples: in a toy with two shape families and sixteen points, a four-point motif nearly determines
the chain, which is not true of real motif scaffolding. The guidance sweep does not reproduce the textbook trade-off
either: realism is best at w = 2 and gets worse from there, and diversity falls from w = 1 to w = 2 and then rises again
by w = 8 as the samples distort. The notebook says all of this in section 3.3 and suggests what to change. It runs on
CPU in about 40 seconds with no downloads.

## Further reading

- Watson et al., [De novo design of protein structure and function with RFdiffusion](https://doi.org/10.1038/s41586-023-06415-8), Nature, 2023 ([free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10468394/))
- Abramson et al., [Accurate structure prediction of biomolecular interactions with AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), Nature, 2024 ([free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168924/))
- Ho et al., [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239), NeurIPS, 2020
- Ho and Salimans, [Classifier-Free Diffusion Guidance](https://arxiv.org/abs/2207.12598), NeurIPS workshop, 2021
- Dauparas et al., [Robust deep learning-based protein sequence design using ProteinMPNN](https://doi.org/10.1126/science.add2187), Science, 2022
