# Week 12: Evaluation, robustness, and fairness

| Session | Content |
|---|---|
| Tue Mar 30 | Evaluation, robustness, and fairness, with three animation clips |
| Thu Apr 1 | Paper sessions: [Goh et al., Large Language Model Influence on Diagnostic Reasoning: A Randomized Clinical Trial](https://doi.org/10.1001/jamanetworkopen.2024.40969) and [DeGrave et al., AI for radiographic COVID-19 detection selects shortcuts over signal](https://doi.org/10.1038/s42256-021-00338-7) |

## Animation clips

The Goh and DeGrave numbers were checked against the papers. The 200-patient test set in clip 2, the subgroup split in
clip 3, and the schematic radiograph drawn for clip 3 are synthetic and marked illustrative on screen. The bootstrap
intervals shown in clip 2 are computed in the scene file from the same resamples the notebook uses, so the clip and the
notebook cannot drift apart. Each clip comes in two versions: narrated (voice-over plus on-screen captions) and silent
(captions only).

| Clip | Narrated | Silent |
|---|---|---|
| 1. A benchmark score is not a clinical effect | [1 min 50 s](clips/narrated/week12-clip1-trial-narrated.mp4) | [48 s](clips/silent/week12-clip1-trial.mp4) |
| 2. How sure are we? The bootstrap | [1 min 53 s](clips/narrated/week12-clip2-bootstrap-narrated.mp4) | [50 s](clips/silent/week12-clip2-bootstrap.mp4) |
| 3. Shortcuts and hidden subgroups | [1 min 56 s](clips/narrated/week12-clip3-shortcuts-narrated.mp4) | [51 s](clips/silent/week12-clip3-shortcuts.mp4) |

The narration is an AI-generated voice reading a script written for the course. The source code for the clips is in
[animations/](animations/) and the narration script is in [clips.json](clips.json). The storyboard brief is in
[storyboard.md](storyboard.md).

**Note for the lecture (clip 1): read the 92% carefully.** The headline of the trial is the null result: a median
diagnostic reasoning score of 76% with GPT-4 against 74% without, an adjusted difference of 2 percentage points with a
95% CI of −4 to 8. The 92% for the model alone comes from a secondary exploratory analysis of **three runs**, and its
16-point lead over the control group has a 95% CI of 2 to 30. The clip shows the three-run caveat on screen. The time
outcome is shown with its interval (−82 s, 95% CI −195 to 31) and no P value, because the article text reports P = .20
while Table 3 reports .15; the interval makes the point without that discrepancy.

**Note for the lecture (clip 3): external validation is necessary, not sufficient.** This is DeGrave et al.'s own
conclusion, and it is easy to miss. Their models lost half their predictive performance at a new hospital system, which
is the familiar story. But some shortcuts transferred: patient positioning, AP against PA, was consistent across both
datasets, so a model relying on it keeps its score at a new site while still not reading the lungs. The authors write
that "external test set validation alone may be insufficient to detect poorly behaved models" and that explainable AI
should be a prerequisite for deployment. The clip gives this its own segment, and the notebook reproduces it with a
third synthetic site where external validation passes and the model is at chance once the marker is removed.

**Note for the lecture (clip 3): Dataset II was the favorable case.** Dataset I drew positives from GitHub-COVID and
negatives from NIH ChestX-ray14, so source and label almost coincide. Dataset II drew both from one region and a shared
research team, which is closer to how a careful study would collect data, and shortcut learning still happened. The
lesson is not only about careless data collection.

## Notebook

The ungraded reference notebook for this lecture is [week12_evaluation.ipynb](../notebooks/week12_evaluation.ipynb). It
has three parts, and reports every number as it came out.

**The bootstrap.** On the same 200-patient agreement table as clip 2 (156 both right, 14 only A, 8 only B, 22 both
wrong), the marginal intervals are 0.800 to 0.900 and 0.765 to 0.870 and the paired difference is 0.03 with a 95% CI of
−0.015 to 0.075. Two extras the clip had no room for: a hypothetical pair with the same accuracies and the same
marginal intervals but only 6 disagreements, whose paired interval is 0.010 to 0.055 and excludes zero, which shows
directly that marginal intervals carry no information about the difference; and a rough sample-size calculation, about
466 patients, with its assumption stated.

**The shortcut.** A 17,682-parameter convolutional network on synthetic 32 by 32 films where the genuine signal is a
faint lung opacity and the shortcut is a bright corner marker. It scores 1.000 on the internal test set and 1.000 at a
second site that uses the same marker convention, so external validation passes, and 0.502 at a site that does not use
it. Three checks catch it without needing that third site: painting out the marker drops site C from 1.000 to 0.500,
stamping a marker onto negative films raises the mean predicted probability of disease from 0.001 to 0.696, and a probe
reads the site from the model's features at 0.695 against a chance level of 0.50. The same architecture trained where no
marker exists reaches 0.947, 0.925 and 0.895 across the three sites, so the genuine signal was learnable all along. The
toy is deliberately more extreme than the paper: our model lands at chance without its shortcut, while the real
classifiers lost about half their performance.

**Subgroups.** A cohort whose true sensitivities are 0.90 and 0.65 in groups that are 80% and 20% of patients. In our
draw of 400, group B got 74 patients, an estimate of 0.743, and a 95% CI of 0.635 to 0.838. The estimate missed the
truth by nearly 10 points and only the interval kept it in view, which is the argument for never reporting a subgroup
number without one.

It runs on CPU in about 15 seconds with no downloads.

## Further reading

- Goh et al., [Large Language Model Influence on Diagnostic Reasoning: A Randomized Clinical Trial](https://doi.org/10.1001/jamanetworkopen.2024.40969), JAMA Network Open, 2024 ([free full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11519755/))
- DeGrave et al., [AI for radiographic COVID-19 detection selects shortcuts over signal](https://doi.org/10.1038/s42256-021-00338-7), Nature Machine Intelligence, 2021 ([free preprint full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7523163/))
- Geirhos et al., [Shortcut Learning in Deep Neural Networks](https://doi.org/10.1038/s42256-020-00257-z), Nature Machine Intelligence, 2020
- Efron and Tibshirani, *An Introduction to the Bootstrap*, Chapman and Hall, 1993
- Obermeyer et al., [Dissecting racial bias in an algorithm used to manage the health of populations](https://doi.org/10.1126/science.aax2342), Science, 2019
