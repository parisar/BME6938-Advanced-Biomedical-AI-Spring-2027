# Relative positions: RoPE and ALiBi

Week 2, clip 4 of 5. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week02-clip4-relative-positions-narrated.mp4); the [silent
version](../silent/week02-clip4-relative-positions.mp4) shows the same steps with on-screen captions
only.

Chest pain means the same thing wherever it appears. Here it moves from positions two and three to
positions seven and eight, but pain is still one position after chest. What matters is the distance.

First, a reminder. An attention score is the dot product of a query and a key, and a dot product
depends on the angle between the two vectors: the smaller the angle, the higher the score. For chest
and pain, the angle is 15 degrees and the score is 1.04.

Rotary position embeddings, or RoPE, encode position by turning these vectors, 15 degrees per
position. Chest at position 2 turns 30 degrees and pain at position 3 turns 45, so the angle between
them grows to 30 degrees and the score becomes 0.93.

Now move the same phrase to positions seven and eight. Both vectors turn much further, but the gap
between them is still 30 degrees, so the score is still 0.93. Only the distance between the tokens
matters.

If pain comes 4 positions after chest instead of 1, the gap grows to 75 degrees and the score drops
to 0.28. Real models rotate many pairs of dimensions, each at its own speed, like the waves in the
previous clip.

A simpler idea is ALiBi. It leaves the vectors alone and subtracts a penalty from each attention
score, proportional to distance. For cold, with a slope of 0.25, the scores minus 0.5, 0.2, 1.3,
0.6, and 1.6 become minus 1.5, minus 0.55, 0.8, 0.35, and 1.6.

After softmax, the weights shift toward nearby tokens: from 0.05, 0.1, 0.3, 0.15, and 0.4, to 0.02,
0.06, 0.24, 0.15, and 0.53.

Today, RoPE is used in nearly every open large language model, including Llama, Qwen, DeepSeek, and
Gemma, and even in newer encoders like ModernBERT. To read longer records than they were trained on,
models stretch the rotation angles after pretraining.
