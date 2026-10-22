# Preference tuning: RLHF and DPO

Week 5, clip 3 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week05-clip3-preference-tuning-narrated.mp4); the [silent
version](../silent/week05-clip3-preference-tuning.mp4) shows the same steps with on-screen captions
only.

Preference data pairs one question with two answers. A clinician marks one as chosen and the other
as rejected. Here the rejected answer gets the negation wrong.

Right now, SmolLM2 rates the wrong answer as far more likely. Its log-probability is minus 2.24,
while the correct answer gets minus 21.09.

The classic method is RLHF. First, a separate reward model learns to score answers from many such
choices. Then reinforcement learning, usually PPO, updates the language model to earn high scores.
That means two models to train, and the training can be unstable.

DPO skips the reward model. It keeps a frozen copy of the starting model, and for each answer it
measures a gain: how much more likely the model in training makes that answer than the frozen copy
does. The frozen copy keeps the model close to what it already knew.

The DPO loss takes the chosen gain minus the rejected gain, scales it by a small number called beta,
here 0.1, and passes it through a sigmoid. The loss gets smaller as the chosen gain pulls ahead.

At the start, the model is identical to its frozen copy, so both gains are zero. The sigmoid of 0 is
one half, and the loss is minus the log of one half, which is 0.69.

After some training, the chosen answer has gained four and the rejected answer has lost six. Beta
times the gap of 10 is 1, the sigmoid of 1 is 0.73, and the loss falls to 0.31.
