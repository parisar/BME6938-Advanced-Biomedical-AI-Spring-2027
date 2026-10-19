# Zero-shot prediction by simulating the future

Week 8, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week08-clip2-rollouts-narrated.mp4); the [silent
version](../silent/week08-clip2-rollouts.mp4) shows the same steps with on-screen captions only.

Now we ask a clinical question: will this patient die in the ICU? Ethos answers it with no labels,
no fine-tuning, and no extra model, using only the timeline it was trained to continue.

Starting from the ICU transfer, the model samples the next token, adds it to the timeline, and
repeats, until it writes either discharge or death. Once the context holds 2,048 tokens, the oldest
one drops off.

Because each token is sampled, every run tells a different story. Ethos simulates 20 futures for
each patient. In this example, 7 of the 20 end in death.

The estimated risk is 7 out of 20, or 0.35. With 20 rollouts, the estimate can only take 21 values,
from 0 to 1 in steps of 0.05.

The same simulations answer other questions too, such as the length of the ICU stay, by adding up
the interval tokens. Ethos reports an AUC of 0.927 for ICU mortality, where 7% of patients died, and
0.921 for hospital mortality.

But when few patients die, a high AUC can still mean many false alarms. In this illustration,
flagging 20 of a hundred patients catches 6 of the 7 deaths, yet 14 of the 20 alarms are false.

Read the results with care. The baselines are numbers reported by other studies, with their own
exclusion criteria. MIMIC comes from one hospital, and dense records lose early history in the
window. Wornow and colleagues found that most EHR models are tested on tasks that say little about
their value to a health system.
