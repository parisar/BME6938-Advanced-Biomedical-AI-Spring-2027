# The KV cache and how models shrink it

Week 4, clip 2 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week04-clip2-kv-cache-narrated.mp4); the [silent
version](../silent/week04-clip2-kv-cache.mp4) shows the same steps with on-screen captions only.

When a decoder writes the next token, its query is compared with the keys of every earlier token,
and their values are mixed in. Here the note so far is: the patient denies chest pain.

Those keys and values do not change, so the model stores them instead of recomputing them at every
step. This store is the KV cache, and each new token adds its own keys and values.

The cache grows with every token, in every layer and every head. For a model shaped like Llama 3,
8B, that is half a megabyte per token, so a patient record of 32,768 tokens needs 16 gigabytes.

Grouped-query attention shrinks it. 32 query heads share 8 key and value heads, so only 8 are
stored, and the same record needs 4 gigabytes instead of 16.

DeepSeek-V3 goes further with multi-head latent attention. It caches one compressed vector of 576
numbers per token and layer, instead of 40,960: about 71 times smaller.

Sliding-window attention is a third approach. In Gemma 3, the base of MedGemma, 5 local layers look
only at the last 1,024 tokens for every global layer that sees everything.
