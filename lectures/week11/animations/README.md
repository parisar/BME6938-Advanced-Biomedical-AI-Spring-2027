# Animation source

The Week 11 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_forward.py | C1 | Diffusion, part 1: adding noise |
| clip2_reverse.py | C2 | Diffusion, part 2: learning the way back |
| clip3_conditioning.py | C3 | Diffusion, part 3: steering the sampler |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week11
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.

**Data sources.** The backbone chains are drawn from simple formulas, a sine wave for a helix and two strands with a turn for a hairpin. They are illustrative, not structures from any database, and the clips say so on screen. The schedule weights in clip 1 are computed inside the scene file from the standard DDPM schedule, beta linear from 0.0001 to 0.02 over 1,000 steps, so the numbers on screen cannot drift from the arithmetic. The RFdiffusion facts in clips 2 and 3 are from Watson et al., Nature 2023: fine-tuned from pretrained RoseTTAFold weights, residue frames of a C-alpha position plus an N-C-alpha-C orientation, self-conditioning, trajectories of about 200 steps, higher in silico success with no added noise in 17 of 23 solved problems, about 8 ProteinMPNN sequences per backbone, 23 of 25 benchmark problems against 19 for RFjoint inpainting and 15 for hallucination, five binder targets, 19% experimental success, fewer than 100 designs tested per target, a 28 nM influenza hemagglutinin binder, and a 2.9 Å cryo-EM map matching the design to 0.63 Å. The AlphaFold 3 facts in clip 2 are from Abramson et al., Nature 2024: a diffusion module predicting raw atom coordinates directly, with no amino-acid frames and no side-chain torsion angles, covering proteins, nucleic acids, ligands, and ions. The guidance numbers in clip 3 (0.2, 0.5, w = 3, giving 1.1) are illustrative and labelled as such on screen.
