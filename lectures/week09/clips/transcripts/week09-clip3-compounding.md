# Errors compound over steps

Week 9, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week09-clip3-compounding-narrated.mp4); the [silent
version](../silent/week09-clip3-compounding.mp4) shows the same steps with on-screen captions only.

Every step of an agent is a chance to fail. It can pick the wrong tool, pass the wrong patient
number, misread a result, or repeat the same call again and again. In ReAct, most failures were
reasoning errors like these.

Suppose each step succeeds 95% of the time, and steps fail independently. Then a task of n steps
succeeds with 0.95 to the power n: 0.77 for 5 steps, 0.6 for 10, and only 0.36 for 20.

Raise each step to 99%, and 10 steps succeed 90% of the time, 20 steps 82%. A small gain per step
makes a large difference for long tasks.

Mitigations start with the tools. The agent checks its own results, for example by re-reading the
lab table, and a mismatch stops the task. It gets only read-only tools, such as get labs and get
meds, never one that places orders or sends messages.

Any action that changes care, such as an order or a message to a patient, stops at a checkpoint. The
agent proposes it, here a repeat potassium and an ECG, and a clinician approves or rejects it before
anything happens.

To sum up: retrieval grounds answers in sources, tools let the model act on real data through text
it writes, and every added step is another chance to fail. So check results, limit the tools, and
ask a clinician.
