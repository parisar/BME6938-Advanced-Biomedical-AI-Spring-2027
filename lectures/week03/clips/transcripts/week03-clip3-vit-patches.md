# Vision transformer: an image as a sequence of patches

Week 3, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week03-clip3-vit-patches-narrated.mp4); the [silent
version](../silent/week03-clip3-vit-patches.mp4) shows the same steps with on-screen captions only.

A vision transformer, or V i T, reads an image as a sequence of patches. Here is a pathology tile
stained with H&E, from a colorectal cancer.

We cut the tile into a four by four grid. That gives 16 square patches, and each patch is handled
separately from here on.

The 16 patches are lined up in reading order, from top left to bottom right. Each patch now plays
the role of a word token.

Each patch is flattened into a list of pixel values, and a shared linear projection maps it to a
vector with d dimensions.

A position vector is added to each patch vector. Without it, the model would not know where in the
image a patch came from.

A learnable CLS token is placed at the front of the sequence. Its output will summarize the whole
image.

These 17 tokens enter a standard transformer encoder. Nothing in the encoder is specific to images:
it is the same architecture used for text.

The output at the CLS position goes to a small prediction head, which classifies the tile as tumor
or normal.

In practice, a 224 by 224 image with 16 by 16 pixel patches gives a 14 by 14 grid: 196 tokens.
