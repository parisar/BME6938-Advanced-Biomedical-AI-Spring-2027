# Reason, act, observe: tool calls

Week 9, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week09-clip2-react-narrated.mp4); the [silent
version](../silent/week09-clip2-react.mp4) shows the same steps with on-screen captions only.

An agent works in a loop of thought, action, and observation. Our task, for the synthetic patient
P001: is the potassium rising, and is it abnormal?

First the model writes a thought: I need the last three potassium results. Then it writes an action,
a tool call in JSON, naming the tool, get labs, and its arguments: the patient, the test, and how
many results.

The program, not the model, runs the tool against the record and appends the result to the context:
4.6, 5.1, and 5.6 millimoles per liter.

The model reads the observation and writes a new thought: the potassium is rising, and 5.6 is above
the usual upper limit of about 5.0. Its last action is finish, with the answer and the values.

A tool call is just text that the model writes in an agreed format. ReAct got this behavior from a
few worked examples in the prompt, with no training at all. Today's models are post-trained to write
tool calls, as in week five.

On ALFWorld, a text-based benchmark of household tasks, the best of 6 ReAct prompts succeeded 71% of
the time, versus 45 for acting without thoughts. Even the worst ReAct prompt beat the best
acting-only one.

On HotpotQA, multi-hop questions answered from Wikipedia, ReAct alone scored 27.4, below chain of
thought at 29.4. Falling back to chain of thought with self-consistency when ReAct got stuck did
best, at 35.1.

The authors labelled 50 failed runs of each method by hand. Hallucination caused 56% of
chain-of-thought failures and none of ReAct's. But 47% of ReAct's failures were reasoning errors,
such as repeating the same step.
