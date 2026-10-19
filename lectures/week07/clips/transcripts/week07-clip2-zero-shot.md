# Zero-shot classification, and where it breaks

Week 7, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week07-clip2-zero-shot-narrated.mp4); the [silent
version](../silent/week07-clip2-zero-shot.mp4) shows the same steps with on-screen captions only.

Once images and text share one space, we can classify without any training. We write one text prompt
for each of the eight tissue classes, such as an H&E image of tumor stroma.

The text encoder turns each prompt into a vector. Together, the eight vectors act as the weights of
a linear classifier, written in text instead of learned from labels.

A new tile goes through the image encoder, its embedding is compared with every class vector, and a
softmax picks the class. BiomedCLIP gives this tumor tile 0.57 for adenocarcinoma: correct, but not
confident.

On natural images this works remarkably well. CLIP's best model reaches 76.2% on ImageNet without a
single ImageNet label, matching a ResNet-50 trained on 1.28 million labeled images. The same paper
notes it is weak on lymph node tumor detection.

On our 5,000 H&E tiles in 8 classes, general CLIP scores between 5.6 and 15.1%, depending only on
the wording of the prompt. Chance is 12.5%, so the worst prompt is below chance.

BiomedCLIP, trained on figures and captions from biomedical papers, does much better, at 34 to 39%.
That is still far from reliable, and the wording of the prompt still changes the result.

Now train a linear probe on the same frozen embeddings, with only ten labeled tiles per class. It
reaches 64% with CLIP and 77% with BiomedCLIP. A few labels beat a clever prompt.
