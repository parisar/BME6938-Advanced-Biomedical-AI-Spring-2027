# Generating text one token at a time

Week 3, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week03-clip1-next-token-generation-narrated.mp4); the [silent
version](../silent/week03-clip1-next-token-generation.mp4) shows the same steps with on-screen
captions only.

A decoder, like the one in GPT, writes text one token at a time from left to right. Here the note so
far reads: the patient denies chest.

Given everything written so far, the decoder outputs a probability for every token in its
vocabulary. The numbers on screen are illustrative.

Greedy decoding simply takes the most likely token, so the model writes pain, with a probability of
0.62.

The chosen token, pain, is appended to the input. In step two, the decoder runs again on the longer
sequence and writes the next token: and.

Each forward pass adds exactly one token. In step three, the model runs once more and adds dyspnea,
meaning shortness of breath.

Greedy decoding always takes the top token. Sampling draws a token according to the probabilities,
and the temperature controls how random that draw is: low is nearly greedy, high is more varied.
