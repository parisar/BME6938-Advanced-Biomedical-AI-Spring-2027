# Week 11 storyboard: generative models and AI for science

Lecture Tue Mar 23; papers Thu Mar 25: Watson et al. (RFdiffusion) and Abramson et al. (AlphaFold 3).
Running example: a small protein backbone drawn as a chain of C-alpha points (illustrative). Paper numbers below
were checked against the papers (RFdiffusion, Nature 2023, PMC10468394; AlphaFold 3, Nature 2024, PMC11168924).
Show the storyboard you derive from this before building. Check every paper number again.

## Clip 1: Forward noising

1. Diffusion models learn to generate by learning to undo noise. Start from a real backbone x0 (a short helix,
   illustrative).
2. Add a little Gaussian noise at each step. After t steps, x_t = sqrt(abar_t) x0 + sqrt(1 - abar_t) noise.
3. With the standard DDPM schedule (beta from 0.0001 to 0.02 over 1,000 steps), the signal and noise weights are:
   t = 100: 0.95 and 0.32; t = 250: 0.72 and 0.69; t = 500: 0.28 and 0.96; t = 999: 0.006 and 1.00.
4. By the last step the backbone is pure noise: all structure is gone.
5. Noising needs no learning; the model learns only the way back.

## Clip 2: Learned reverse denoising

1. A network sees x_t and t and predicts the noise (or, equivalently, the clean structure x0).
2. Take a small step toward the prediction, add a little fresh noise, repeat: noise becomes a plausible backbone.
3. Sampling from new noise gives a new backbone each time: generation, not retrieval.
4. RFdiffusion: fine-tunes the structure predictor RoseTTAFold as the denoiser; it works on residue frames (C-alpha
   position plus orientation), predicts x0 at each step with self-conditioning, and typically uses 200 steps.
   ProteinMPNN then designs sequences for each backbone (about 8 per backbone).
5. AlphaFold 3 uses a diffusion module too: it predicts raw atom coordinates for proteins, nucleic acids, and
   ligands, with no frames or torsion angles.

## Clip 3: Conditioning and guidance

1. Unconditional generation makes some protein. Science needs a specific one: around a functional motif, or one
   that binds a target.
2. Conditioning: give the denoiser extra input, such as fixed motif coordinates or the target protein, so every
   step respects it.
3. Guidance (general idea, used widely in image diffusion): mix conditional and unconditional predictions,
   e = e_uncond + w (e_cond - e_uncond). With e_uncond = 0.2, e_cond = 0.5, w = 3: e = 1.1 (illustrative).
   Larger w follows the condition more strongly at the cost of diversity.
4. RFdiffusion results: solves 23 of 25 motif-scaffolding problems versus 15 for hallucination and 19 for RFjoint;
   de novo binders against 5 targets with 19% experimental success overall; a binder to influenza hemagglutinin at
   28 nM with a cryo-EM structure matching the design at 0.63 A.
5. Caution: in silico success uses AlphaFold-family predictions as the judge, which can share blind spots with the
   designer; experimental validation is the real test.

## Notebook (week11_diffusion.ipynb, CPU)

A 2D toy: noise and denoise small backbone-like point chains with a tiny MLP denoiser; the DDPM schedule numbers
above; conditioning on fixed points (a "motif"); guidance strength versus diversity. All examples biomedical;
commit and push after each clip.
