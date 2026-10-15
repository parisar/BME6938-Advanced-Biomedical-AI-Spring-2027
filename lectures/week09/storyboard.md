# Week 9 storyboard: retrieval, tool use, and agentic systems

Lecture Tue Mar 9; papers Thu Mar 11: Yao et al. (ReAct) and Zakka et al. (Almanac).
Running example: a synthetic hospital (no real patient data). Paper numbers below were checked against the papers
(ReAct, ICLR 2023; Almanac, arXiv 2303.01229, NEJM AI 2024); anything marked illustrative is invented for teaching.
Show the storyboard you derive from this before building, as for Weeks 7 and 8. Check every paper number again.

## Clip 1: Retrieval-augmented generation

1. A model cannot know your hospital's own protocols. Question: "Within how many hours must antibiotics start in
   our sepsis protocol?" The model alone guesses (illustrative wrong answer: 3 hours).
2. Split the hospital's documents into chunks (Almanac used 1,000-token chunks) and embed each chunk once
   (Almanac used 1,536-number embeddings in an approximate nearest-neighbor index).
3. Embed the question and compare it with every chunk by cosine similarity. Top 3 scores: 0.86, 0.79, 0.62
   (illustrative).
4. Almanac abstains when the best match is below a threshold (lambda = 0.83). Here only the first chunk passes.
   Show a second question whose best score is 0.71: the system answers "not found in the sources".
5. The passing chunk is inserted into the prompt with its source; the model answers "within 1 hour" (from the
   synthetic protocol) and cites it.
6. Almanac results: factuality 18 points higher than ChatGPT averaged over specialties; adversarial prompts 95%
   versus 0%, largely by abstaining; yet physicians preferred ChatGPT's answers 57% of the time. Caution: abstention
   inflates the adversarial score, and the benchmark has 130 questions written by the authors' group.

## Clip 2: Reason, act, observe (ReAct) and tool calls

1. An agent alternates thought, action, and observation. Task: "Is this patient's potassium rising, and is it
   abnormal?" (synthetic patient P-001).
2. Thought: "I need the last three potassium results." Action as structured output (JSON):
   {"tool": "get_labs", "args": {"patient_id": "P-001", "test": "potassium", "last": 3}}
3. Observation from the tool: 4.6, 5.1, 5.6 mmol/L (synthetic).
4. Thought: "Rising; 5.6 is above the usual upper limit of about 5.0." Action: finish with the answer and the values.
5. A tool call is just text the model writes in an agreed format; the program runs the tool and appends the result
   to the context. This is the Week 5 decoder, post-trained to write tool calls.
6. ReAct results: ALFWorld 57% average success versus 45% for acting without reasoning (best of 6); on HotpotQA,
   ReAct alone scored 27.4 exact match, below chain of thought with self-consistency (33.4); the hybrid won.
   Hallucination caused 56% of chain-of-thought failures and 0% of ReAct failures.

## Clip 3: Errors compound over steps

1. Each step of an agent can fail: a wrong tool, a wrong argument, a misread result.
2. If each step succeeds with probability 0.95 and steps are independent (illustrative assumption), a task of n
   steps succeeds with 0.95^n: 5 steps 0.77, 10 steps 0.60, 20 steps 0.36.
3. At 0.99 per step: 10 steps 0.90, 20 steps 0.82. Small per-step gains matter a lot for long tasks.
4. Mitigations: verify results (re-read the lab table), limit the action space (read-only tools), ask a human at
   checkpoints for any action that changes care (orders, messages).
5. Summary: retrieval grounds answers in sources; tools let the model act; every added step is another chance to fail.

## Notebook (week09_retrieval_agents.ipynb, CPU)

A small synthetic protocol corpus; chunking and embeddings with a small open embedding model; cosine top-k with an
abstention threshold; a toy ReAct loop with two read-only tools on a synthetic patient (get_labs, get_meds) and a
JSON tool-call parser; a simulation of error compounding. All examples biomedical; commit and push after each clip.
