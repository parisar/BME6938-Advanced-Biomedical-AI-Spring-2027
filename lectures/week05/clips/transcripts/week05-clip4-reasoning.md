# Reasoning models

Week 5, clip 4 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week05-clip4-reasoning-narrated.mp4); the [silent
version](../silent/week05-clip4-reasoning.mp4) shows the same steps with on-screen captions only.

A reasoning model writes out its thinking before it answers. For this ECG question, it reasons that
ST elevation in leads II, III, and aVF points to the inferior wall, usually supplied by the right
coronary artery, and answers B. The trace shown is illustrative.

DeepSeek-R1 learned this with rewards that a simple program can check: one point if the final answer
is correct, and one point if the reasoning sits inside the think tags. R1-Zero used reinforcement
learning alone. R1 first saw a small set of long reasoning examples.

The training method is called GRPO. For each question, the model writes a group of answers, and each
one is scored. Here, only the first of four answers picks the right artery.

Each reward is compared with its own group. The mean reward is 0.25, and the standard deviation is
0.433. So the correct answer scores plus 1.73, and each wrong answer scores minus 0.58. No separate
critic model is needed.

The model is then updated so that answers above their group's average become more likely, and
answers below it become less likely. Over many questions, reasoning that reaches correct answers is
reinforced.

Test time is different. Asked directly, SmolLM2 gets the chest pain question wrong in nine tokens.
Asked to reason first, it spends all 600 tokens looping through 28 numbered steps and never reaches
an answer. The cost arrives, the benefit does not. Reasoning is something a model is trained to do,
not something a prompt adds. Both are real output from the model.

Med-PaLM 2 samples several reasoning paths for a medical question, then reads them all to write one
refined answer. Together with a stronger base model and medical fine-tuning, this raised MedQA
accuracy from 67.2 to 86.5%.

And a fluent explanation is not proof. On the ECG question, the same model answers D, the left main,
which is wrong. Asked to reason, it invents a finding that was never in the question, argues its way
to the left anterior descending, and then answers D anyway. The rationale does not even agree with
the letter beside it. We return to checking reasoning in week 12.
