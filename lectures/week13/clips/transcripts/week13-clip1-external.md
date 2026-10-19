# What external validation found

Week 13, clip 1 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week13-clip1-external-narrated.mp4); the [silent
version](../silent/week13-clip1-external.mp4) shows the same steps with on-screen captions only.

The Epic Sepsis Model ships with a widely used health record and runs at hundreds of US hospitals.
It scores every adult inpatient every 15 minutes and alerts when that score crosses a threshold. Its
vendor reported an AUC between 0.76 and 0.83.

Wong and colleagues validated it at Michigan Medicine: 27,697 patients and 38,455 hospitalizations,
of which 2,552, or 7%, had sepsis.

The AUC was 0.63, with a 95% interval from 0.62 to 0.64. The authors also report per-horizon AUCs of
0.72 to 0.76, then explain why those are misleading: the predictions are not independent of each
other.

At the vendor's threshold of 6, sensitivity was 33%, so two thirds of sepsis cases were never
flagged. The positive predictive value was 12%. Alerts fired on 18% of all hospitalizations: 8
patients to evaluate for every sepsis case.

Now ask what the alert added. Of the 2,552 sepsis cases, 843 were flagged, and of those only 183 had
not already received timely antibiotics. Of the 1,709 that were missed, 1,030 were treated in time
anyway.

Two lessons. Validate locally before deployment, because a vendor's AUC came from a vendor's
population, not yours. And measure the increment over current practice, not the model on its own. A
model is worth deploying only if it changes what happens to a patient.
