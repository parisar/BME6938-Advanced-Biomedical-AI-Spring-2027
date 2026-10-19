# Mixture of experts

Week 4, clip 3 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week04-clip3-mixture-of-experts-narrated.mp4); the [silent
version](../silent/week04-clip3-mixture-of-experts.mp4) shows the same steps with on-screen captions
only.

In a dense model, every token passes through the same feed-forward network, and all of its weights
are used for every token.

A mixture of experts splits this network into many smaller networks, called experts. Here we draw 16
of them, and the numbers in this clip are illustrative.

A small router scores every expert for each token. For chest, experts 3 and 11 score highest, 0.38
and 0.25, so only those 2 run.

Other tokens are routed to other experts: denies to experts 1 and 9, and pain to experts 7 and 14.
Experts that no token chose stay idle.

The output for chest is a weighted sum of its 2 experts: 0.6 times expert 3, plus 0.4 times expert
11. The router weights are rescaled to sum to one.

DeepSeek-V3 has 256 experts plus one shared expert in each layer, and picks 8 per token. It has 671
billion parameters, but uses only 37 billion for each token.
