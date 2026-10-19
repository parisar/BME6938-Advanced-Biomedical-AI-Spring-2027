# Contrastive learning: two views, one embedding

Week 6, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week06-clip2-contrastive-learning-narrated.mp4); the [silent
version](../silent/week06-clip2-contrastive-learning.mp4) shows the same steps with on-screen
captions only.

Contrastive learning starts by making two different views of the same ECG, using random
augmentations.

Here, view one is cropped and has added noise, and view two is rescaled with a slow baseline drift.
The heart rhythm, and so the diagnosis, stays the same.

Both views pass through the same encoder, with shared weights. Each view becomes one point in the
embedding space.

In practice we train on a batch, so the other ECGs in the batch, here B, C, and D, also become
points.

Training pulls the two views of ECG A toward each other, and pushes the other ECGs in the batch
further away.

The loss turns this into a classification. Compare A1 with every other view in the batch, apply a
softmax, and its partner, A2, should win, here with 0.59.

This is the InfoNCE loss. It is a softmax over the similarities, each divided by a temperature tau,
and we minimize the negative log probability of the true partner.

After training on many unlabeled ECGs, recordings with similar rhythms tend to land close together,
even though the model never saw a single diagnosis.

For pathology tiles, the two views come from random crops, flips and rotations, and changes in stain
color, because tissue has no fixed orientation and staining varies between labs.
