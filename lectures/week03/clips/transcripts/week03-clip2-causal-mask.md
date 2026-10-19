# The causal mask

Week 3, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week03-clip2-causal-mask-narrated.mp4); the [silent
version](../silent/week03-clip2-causal-mask.mp4) shows the same steps with on-screen captions only.

Here are the attention scores for five tokens: the patient denies chest pain. Each row is one
token's query, and each column is a key.

But a decoder is trained to predict the next token. If patient could look at denies, chest, and
pain, it would simply copy the answer.

The causal mask fixes this. Every score above the diagonal, where a query would look at a later
token, is set to minus infinity.

After the softmax, minus infinity becomes zero. Each row now sums to one over the tokens it is
allowed to see: itself and the tokens before it.

For example, the row for chest spreads its attention over the, patient, denies, and chest itself,
and gives nothing to pain.

Because of the mask, a single forward pass trains every position at once: each token's output is
used to predict the token that follows it.
