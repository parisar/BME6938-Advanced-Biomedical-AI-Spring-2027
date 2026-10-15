# Week 8 storyboard: foundation models for EHR and physiological time series

Lecture Tue Mar 2; papers Thu Mar 4: Wornow et al. (shaky foundations) and Renc et al. (ETHOS).
Running example: one synthetic ICU patient (no real patient data). ETHOS details below are from the paper
(arXiv 2407.21124); anything marked illustrative is invented for teaching. Show the storyboard you derive from
this before building, as for Week 7.

## Clip 1: A patient timeline as tokens

1. A hospital record is a timeline of events at irregular times. Synthetic patient: ED admission at 0 h;
   lactate 4.1 mmol/L at 0.6 h; norepinephrine at 1.5 h; diagnosis sepsis (ICD-10 A41.9) at 2.2 h;
   ICU transfer at 3.5 h.
2. Codes become tokens directly: one token for A41.9, one for norepinephrine.
3. Numbers become quantile tokens: each lab is binned into 10 quantiles computed on training data (as in ETHOS).
   Lactate 4.1 is above the 90th percentile (illustrative cutoff), so it becomes [LACTATE] [Q10].
4. Time gaps become interval tokens: ETHOS uses 13 interval tokens and adds none for gaps under 5 minutes.
   Gaps here: 0.6 h, 0.9 h, and 0.7 h -> [30m-1h]; 1.3 h -> [1h-2h] (bin labels illustrative).
5. Static tokens come first (ETHOS uses 6, such as sex and age). The whole record is now one sequence:
   [SEX_F] [AGE_65-70] [ED_ADMIT] [30m-1h] [LACTATE] [Q10] ...
6. A decoder is trained with the next-token loss (Week 3) on many timelines: ETHOS used 241,015 MIMIC-IV
   patients for training, context 2,048 tokens.

## Clip 2: Zero-shot prediction by simulating the future

1. Question: will this patient die in hospital? No task-specific training.
2. From the timeline at ICU admission, generate tokens with sampling until a terminal token: DISCHARGE or DEATH.
3. Repeat 20 times (ETHOS uses 20 trajectories). Show 20 short lines; 7 end in DEATH (illustrative).
4. Predicted probability = 7 / 20 = 0.35.
5. The same rollouts answer other questions (time to discharge, readmission). ETHOS results: in-hospital
   mortality AUC 0.921 (2.0% prevalence), ICU mortality AUC 0.927, DRG top-1 accuracy 84.8%.
6. Cautions: the authors say their baselines are not like for like; single site (MIMIC-IV); the 2,048-token
   context truncates the longest, sickest timelines. Wornow et al.: most EHR models are trained on MIMIC or
   PubMed and evaluated on tasks that say little about value to a health system.

## Clip 3: Irregular sampling and physiological signals

1. Measurements arrive at irregular times: heart rate charted about hourly, lactate a few times, long overnight
   gaps (illustrative).
2. Option 1: resample onto an hourly grid, fill gaps, and add a mask marking which values were actually measured.
3. Missingness carries information: a lactate ordered at 2 a.m. signals concern; the mask lets the model use it.
4. Option 2: interval tokens (clip 1). Option 3: a continuous time embedding, like the Week 2 position waves but
   in real time. t = 2.5 h with 8-hour and 24-hour periods: sin 0.92, cos -0.38 and sin 0.61, cos 0.79.
5. Dense signals are cut into patches as in Week 6: a 10 s ECG at 500 Hz becomes 10 one-second patches of 500
   samples each, the tokens of an ECG foundation model.
6. Summary: events -> tokens; values -> quantile tokens; time -> interval tokens or time embeddings;
   dense signals -> patches.

## Notebook (week08_ehr_time_series.ipynb, CPU)

A synthetic timeline generator; the tokenizer with 10 quantiles and interval tokens; a tiny decoder trained on
synthetic timelines; 20 rollouts turned into a probability; the time embedding; ECG patching with the Week 6 ECG
generator. Optional: the MIMIC-IV Clinical Database Demo (100 patients, open access on PhysioNet); confirm its
license before using it. All examples biomedical; commit and push after each clip.
