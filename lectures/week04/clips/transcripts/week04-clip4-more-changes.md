# More 2026 changes

Week 4, clip 4 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week04-clip4-more-changes-narrated.mp4); the [silent
version](../silent/week04-clip4-more-changes.mp4) shows the same steps with on-screen captions only.

Vocabularies have grown. GPT-2, from 2019, splits this clinical sentence into 21 tokens and cuts
tachycardia into 4 pieces. DeepSeek-V3, with about 129,000 tokens in its vocabulary, needs only 14.

Long patient records need long context. A model is trained on shorter text; rotating 8 times slower
lets position 32,768 land where 4,096 was. DeepSeek-V3 was stretched from 4,000 to 32,000, then
128,000 tokens.

Multi-token prediction adds a second target during training. From the patient denies chest, the main
head predicts pain, and an extra module predicts the token after next: and. This gives more training
signal and can speed up generation.

This week's paper, MedGemma, starts from Gemma 3 and continues training on medical text and medical
images. It comes in 4 billion and 27 billion parameter versions, built from the pieces in these
clips.
