# Retrieval-augmented generation

Week 9, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week09-clip1-rag-narrated.mp4); the [silent
version](../silent/week09-clip1-rag.mp4) shows the same steps with on-screen captions only.

A language model learns from public text, so it cannot know your hospital's own protocols. Asked
when antibiotics must start under our sepsis protocol, it says three hours: a reasonable national
figure, but not our rule.

Retrieval starts by splitting the hospital's documents into chunks. Almanac used chunks of 1,000
tokens. Each chunk is embedded once into a vector, which in Almanac had 1,536 numbers.

At question time, the question is embedded the same way and compared with every chunk by cosine
similarity. Here the 3 best chunks score 0.86, 0.79, and 0.62.

Only chunks that score above a threshold are passed on. Almanac used a threshold, lambda, of 0.83,
so here only the first chunk, from the sepsis protocol, passes.

A second question, about rattlesnake bites, finds no good match: its best score is only 0.71. The
published Almanac then falls back on the model's own knowledge. The preprint version abstained
instead, and said the answer was not found in the sources.

The passing chunk is pasted into the prompt, together with its source. The model now answers within
one hour, which is what the synthetic protocol says, and it cites section two of that protocol.

Clinicians compared Almanac with ChatGPT-4, Bing, and Bard on 314 clinical questions. Almanac ranked
first for factuality, completeness, and preference, and its citations were correct 91% of the time.

Read these results with care. Against adversarial prompts, Almanac scored 100% and ChatGPT-4 7%,
mostly because Almanac declined to answer. The questions and the grading came from the study's own
clinicians, and only 25 questions are public.
