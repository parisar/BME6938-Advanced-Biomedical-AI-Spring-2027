# From tokens to vectors

Week 2, clip 1 of 5. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week02-clip1-tokens-to-vectors-narrated.mp4); the [silent
version](../silent/week02-clip1-tokens-to-vectors.mp4) shows the same steps with on-screen captions
only.

Take a short sentence from a clinical note: the patient has a cold. A transformer cannot work with
text directly. Everything has to become numbers first.

First, a tokenizer splits the sentence into tokens. Here we get five: the, patient, has, a, and
cold.

Each token is mapped to an integer ID from the tokenizer's vocabulary. The exact numbers on screen
are only illustrative.

Each ID selects one row of a learned embedding table, which has one row for every entry in the
vocabulary. That row becomes the token's vector.

Stacking the five vectors gives a five by d matrix, with one row per token. We draw d as four. In
BERT base, d is 768.

But there is a problem. In the patient has a cold and the patient feels cold, the token cold has the
same ID, 3147, so it gets an identical vector.

In the patient has a cold, the word means an infection. In the patient feels cold, it means a low
temperature. The embedding cannot tell them apart.

Attention solves this. It updates each token's vector using the other tokens in the sentence, so the
vector depends on context.
