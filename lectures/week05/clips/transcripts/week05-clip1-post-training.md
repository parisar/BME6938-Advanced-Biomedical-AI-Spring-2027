# From pretrained model to clinical assistant

Week 5, clip 1 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week05-clip1-post-training-narrated.mp4); the [silent
version](../silent/week05-clip1-post-training.mp4) shows the same steps with on-screen captions
only.

A pretrained model only continues the text it is given. We gave the base Qwen3 model the start of a
discharge summary, and it simply kept writing a note about a different patient.

Now we ask it a question about the note. The base model does not answer like an assistant. It treats
the text as a quiz and keeps inventing new questions.

The post-trained version of the same model answers the question directly. But here its answer is
wrong: the note says the patient denies chest pain. Clips three and four show two ways to fix this.

Post-training adds stages after pretraining: supervised fine-tuning, then preference tuning, then
reinforcement learning with rewards that a program can check. We cover the last stage in clip four.

Supervised fine-tuning trains on instruction and answer pairs. Each pair is wrapped in a chat
template, with special markers for where the user's turn and the assistant's turn begin and end.

The loss is the same next-token loss as in pretraining. The only difference is that it is counted on
the answer tokens, not on the instruction, so the model learns to write answers.

So the architecture is the same and the loss is the same. Only the training data changes, from raw
text to instruction and answer pairs, and that is what turns a text generator into an assistant.
