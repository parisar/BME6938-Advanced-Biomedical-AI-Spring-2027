# CLIP: matching images with their captions

Week 7, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week07-clip1-clip-narrated.mp4); the [silent
version](../silent/week07-clip1-clip.mp4) shows the same steps with on-screen captions only.

In week six, contrastive learning matched two views of the same ECG. CLIP keeps the same idea, but
matches an image with the text that describes it, such as an H&E tile and its caption.

CLIP has two encoders. A vision transformer encodes the image, and a text transformer encodes the
caption. Both produce 512 numbers, scaled to length 1, in the same embedding space.

Take a batch of four tiles and their four captions. Comparing every tile with every caption gives a
four by four grid of cosine similarities. The true pairs sit on the diagonal.

Each row is divided by a temperature, here 0.07, and passed through a softmax. The tumor tile then
gives its own caption a probability of 0.82.

The loss is cross-entropy in both directions. Along each row, a tile must pick its caption. Down
each column, a caption must pick its tile. The 2 are averaged, here to 0.18.

CLIP was trained on 400 million image and text pairs collected from the web, in batches of 32,768
pairs. The temperature starts at 0.07 and is learned.

BiomedCLIP uses the same recipe on biomedical data: 15 million figures and their captions, taken
from 4.4 million articles in PubMed Central.
