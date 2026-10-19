# Diffusion, part 1: adding noise

Week 11, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week11-clip1-forward-narrated.mp4); the [silent
version](../silent/week11-clip1-forward.mp4) shows the same steps with on-screen captions only.

Diffusion models learn to generate by learning to undo noise. We start from a real backbone, x 0,
drawn here as 16 C-alpha points in a short helix. Training runs in two directions.

The forward direction adds a little Gaussian noise at every step. Each point drifts by a random
amount, and after the first few steps the helix is still obvious.

You never have to take the steps one at a time. After t steps, x t is a single weighted mix: the
square root of the signal weight times x zero, plus the square root of one minus that weight, times
one Gaussian draw.

The schedule fixes those weights. With beta rising from 0.0001 to 0.02 over a thousand steps, the
signal weight is 0.95 at step 100, 0.72 at 250, and 0.28 at 500.

By step 999 the signal weight is 0.006: a Gaussian cloud. Every protein ends in the same place,
which is exactly why sampling can start from noise alone.

Noising needs no learning at all, just a random number generator. The network only ever learns the
way back. One real structure gives a thousand training examples, one for every step.
