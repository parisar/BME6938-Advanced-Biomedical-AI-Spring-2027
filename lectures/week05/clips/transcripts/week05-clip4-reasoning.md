# Reasoning models

Week 5, clip 4 of 4. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week05-clip4-reasoning-narrated.mp4); the [silent
version](../silent/week05-clip4-reasoning.mp4) shows the same steps with on-screen captions only.

A reasoning model writes out its thinking before it answers. For this ECG question, it reasons that
ST elevation in leads II, III, and aVF points to the inferior wall, usually supplied by the right
coronary artery, and answers B.

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

Thinking can also help at test time. With thinking off, the small Qwen3 model gets the chest pain
question wrong in nine tokens. With thinking on, it writes 119 tokens and gets it right, but it
takes much longer.

Med-PaLM 2 samples several reasoning paths for a medical question, then reads them all to write one
refined answer. Together with a stronger base model and medical fine-tuning, this raised MedQA
accuracy from 67.2 to 86.5%.

But a fluent explanation is not proof. On the ECG question, the same small model picks the right
artery with thinking off. With thinking on, it argues confidently for the wrong artery, and after
1,500 tokens it is still unsure. We return to checking reasoning in week 12.
