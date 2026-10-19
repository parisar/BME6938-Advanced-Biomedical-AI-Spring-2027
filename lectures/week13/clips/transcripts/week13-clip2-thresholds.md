# Thresholds, alert burden, and drift

Week 13, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week13-clip2-thresholds-narrated.mp4); the [silent
version](../silent/week13-clip2-thresholds.mp4) shows the same steps with on-screen captions only.

Once the model is trained, one decision is left: where to put the threshold. These 2 curves are
drawn to the same height, but sepsis is only 7% of patients, so the red 1 is really much smaller.
Moving the line trades missed cases against false alarms.

At 7% prevalence, sensitivity of 80% with a positive predictive value of 10% means 56 alerts for
every 100 admissions. 50% with 20% means 17 and a half. 25% with 35% means 5.

The honest unit is how many patients a clinician reviews for each real case: ten, five, and about
three at those three points. The real sepsis model sat at 8, and it alerted on 18% of all
hospitalizations.

None of this holds still. A lab changes an assay, a diagnosis moves to a new code, a unit reopens
and the case mix shifts. None of these generates a ticket. The model keeps producing scores that
look plausible while the performance moves.

So watch it. Plot the monthly AUC against limits set from a period you agree was stable. Here it
drifts below the lower limit and stays there for three months, which is a signal rather than a bad
month.

Write the plan before go-live. Track inputs, outputs and outcomes. Set the limits in advance. Name
the person who is paged when one is crossed, and decide now whether the answer is to retrain,
retune, or switch it off.
