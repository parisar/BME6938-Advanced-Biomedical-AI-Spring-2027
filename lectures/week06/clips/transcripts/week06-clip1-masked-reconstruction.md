# Masked reconstruction: learning by filling in gaps

Week 6, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week06-clip1-masked-reconstruction-narrated.mp4); the [silent
version](../silent/week06-clip1-masked-reconstruction.mp4) shows the same steps with on-screen
captions only.

We start with a single lead ECG recording, ten seconds long. Nobody has labeled it with a diagnosis,
so all we have is the raw signal.

We cut the signal into one second patches. Just like words in a sentence, each patch becomes one
token for a transformer encoder.

Then we hide most of the patches at random. Here, six of the ten patches are masked out.

The encoder sees only the four visible patches, and turns each of them into an embedding vector.

A small decoder takes these embeddings, plus a placeholder mask token for every hidden patch, and
predicts the missing waveform.

The loss is the mean squared error between the prediction and the true signal, computed only on the
patches that were hidden.

Over many training steps, the predictions improve. To fill the gaps well, the encoder has to learn
the structure of a heartbeat: the P wave, the QRS complex, and the T wave.

After pretraining, the decoder has done its job and is discarded. We keep the encoder, which now
produces useful representations of ECG signals.

The same recipe works for pathology. A masked autoencoder hides most patches of an H&E tile, here 12
of 16, and learns to reconstruct the missing pixels.
