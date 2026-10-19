# Diffusion, part 3: steering the sampler

Week 11, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week11-clip3-conditioning-narrated.mp4); the [silent
version](../silent/week11-clip3-conditioning.mp4) shows the same steps with on-screen captions only.

Unconditional sampling gives you a valid structure, but not the one you need. A real design project
asks for something specific: hold this functional motif in place, or bind this target protein.

Conditioning is the direct answer. Give the denoiser the motif's coordinates and hold them fixed at
every step. The motif never moves, and the scaffold is sampled, so one motif gives you many
different scaffolds.

Guidance is a different lever, borrowed from image diffusion. Mix the conditional and unconditional
predictions: 0.2, plus 3 times 0.5 minus 0.2, gives 1.1. A larger w follows the condition harder and
cuts diversity. RFdiffusion does not do this; it conditions the denoiser directly.

On 25 motif-scaffolding benchmarks, RFdiffusion solved 23, against 19 for RFjoint inpainting and 15
for hallucination, using one set of settings for every problem. Note that this success is scored in
silico.

Designed binders were tested against five targets, among them influenza hemagglutinin and PD-L1. 19%
worked experimentally, from fewer than a hundred designs per target. The best flu binder reached 28
nanomolar, and a cryo-EM map matched the design to 0.63 angstroms.

Read the in silico numbers with care. The designs are scored by AlphaFold family predictors trained
on the same structures, so the designer and the judge can agree and both be wrong. The 19% is the
number that counts, because it came from a wet lab.
