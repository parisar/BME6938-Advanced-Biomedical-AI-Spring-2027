# What changed since 2017

Week 4, clip 1 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week04-clip1-modern-block-narrated.mp4); the [silent
version](../silent/week04-clip1-modern-block.mp4) shows the same steps with on-screen captions only.

A large language model in 2026 is still a stack of decoder blocks, much like the 2017 transformer:
attention, then a feed-forward network, each with a residual connection.

The first change is normalization. It now comes before each sublayer instead of after, and it uses
RMS norm, which only rescales each vector by its root mean square.

Second, the feed-forward network becomes swig-loo. The token is projected twice, and one projection
passes through a smooth activation and acts as a gate on the other.

Third, positions are no longer added at the input. Instead, RoPE rotates every query and key inside
each attention layer, as we saw in week two.

Fourth, attention becomes grouped-query attention. In SmolLM2, 15 query heads share 5 key and value
heads, which saves memory during generation.

The overall shape is unchanged. The 2017 decoder stacked 6 blocks, SmolLM2 stacks 32, and the last
block feeds the prediction of the next token.
