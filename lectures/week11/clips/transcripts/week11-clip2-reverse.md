# Diffusion, part 2: learning the way back

Week 11, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week11-clip2-reverse-narrated.mp4); the [silent
version](../silent/week11-clip2-reverse.mp4) shows the same steps with on-screen captions only.

A single network sees the noisy structure x t and the step number t, and predicts the noise that was
added. Predicting the noise and predicting the clean structure are the same job: either one gives
you the other.

One reverse step moves a little way toward the predicted clean structure, then adds a little fresh
noise. Repeat from a thousand down to one. The fresh noise is what keeps the samples diverse.

Run that step a thousand times and the Gaussian cloud tightens into a backbone that could fold. The
drawing is illustrative, but the trajectory is real: structure appears gradually, not all at once.

Start from different noise and you get a different structure. This is generation, not retrieval:
none of these has to appear anywhere in the training set.

RFdiffusion fine-tunes the structure predictor RoseTTAFold into its denoiser. It works on residue
frames, a C-alpha position plus an orientation, predicts the clean structure at every step and feeds
it back as a template, and runs about 200 steps. One twist: for motif scaffolding, adding no fresh
noise on the way back worked better in 17 of the 23 solved problems.

RFdiffusion makes a shape, not a protein. ProteinMPNN then designs sequences for that backbone,
typically about eight of them. Those sequences are what you can actually order, express, and test.

AlphaFold 3 uses a diffusion module as well, but it predicts raw atom coordinates directly, with no
amino acid frames and no torsion angles. Dropping that protein-specific machinery is what lets one
model cover proteins, nucleic acids, ligands, and ions.
