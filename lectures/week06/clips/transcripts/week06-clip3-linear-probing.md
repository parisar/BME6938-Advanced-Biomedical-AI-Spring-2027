# Linear probing: what did the encoder learn?

Week 6, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week06-clip3-linear-probing-narrated.mp4); the [silent
version](../silent/week06-clip3-linear-probing.mp4) shows the same steps with on-screen captions
only.

Now we test what pretraining learned. Take the pretrained encoder and freeze it, so none of its
weights can change.

We need only a small labeled dataset. Here, each ECG is labeled either atrial fibrillation, AF, or
normal sinus rhythm.

The frozen encoder maps each ECG to an embedding of 256 numbers. We draw these embeddings as points
in two dimensions.

On top, we add a single linear prediction head. It computes a weighted sum of the embedding plus a
bias, and a sigmoid turns that into the probability of AF.

During training, gradients flow into the head only. The encoder is frozen, so its weights never
change.

If one straight line can separate AF from normal, the information was already in the embedding. The
head only has to read it out.

With fine-tuning, every weight is trainable, including the encoder. A linear probe trains only 257
weights, so it measures what the pretrained encoder already learned.

The same linear probe works for pathology. A frozen encoder embeds each H&E tile, and a single
linear head separates tumor from normal mucosa.
