# Inside the encoder block

Week 2, clip 5 of 5. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week02-clip5-encoder-block-narrated.mp4); the [silent
version](../silent/week02-clip5-encoder-block.mp4) shows the same steps with on-screen captions
only.

An encoder block starts from the five token vectors. Each one is combined with a position vector, so
the block knows where every token sits.

Multi-head self-attention lets every token look at every other token. BERT base runs 12 attention
heads in parallel.

Then comes add and normalize. A residual connection adds the block's input back to the attention
output, and layer normalization keeps the values well scaled.

Next, a feed-forward network transforms each token separately. It expands each vector from d to four
d dimensions, then projects it back down to d.

A second add and normalize wraps the feed-forward network, again with a residual connection around
it.

The output has exactly the same shape as the input: five by d in, five by d out, with one updated
vector per token.

Because the shapes match, blocks can be stacked one on top of another. BERT base stacks 12 encoder
blocks, each with its own weights.
