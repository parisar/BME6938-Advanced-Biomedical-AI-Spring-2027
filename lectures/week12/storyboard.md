# Week 12 storyboard: evaluation, robustness, and fairness

Lecture Tue Mar 30; papers Thu Apr 1: Goh et al. (LLM diagnostic reasoning RCT) and DeGrave et al. (COVID-19
shortcuts). Paper numbers below were checked against the papers (Goh, JAMA Netw Open 2024; DeGrave, Nature Machine
Intelligence 2021, medRxiv version). Anything marked illustrative is invented. Show the storyboard first.

## Clip 1: A benchmark score is not a clinical effect

1. A model can score well alone and still not help clinicians. Goh et al. randomized 50 physicians: 25 with GPT-4
   plus usual resources, 25 with usual resources only.
2. Diagnostic reasoning score: 76% with GPT-4 versus 74% without; difference 2 points (95% CI -4 to 8), p = 0.60.
3. GPT-4 alone, in an exploratory arm, scored 92%, 16 points above the usual-resources group.
4. The gap between 92% and 76% is about how people use the tool, not about the tool alone.
5. Evaluation ladder: benchmark, retrospective study, reader study, prospective trial, deployment with monitoring.

## Clip 2: How sure are we? Bootstrap confidence intervals

1. A test set of 200 patients (synthetic). Model A is right on 170 (85%), model B on 164 (82%).
2. Resample the 200 patients with replacement 10,000 times and recompute accuracy each time.
3. 95% intervals: A 0.80 to 0.90; B 0.77 to 0.87. They overlap.
4. Paired bootstrap of the difference (same patients for both models): 0.03, 95% CI -0.015 to 0.075. The interval
   includes 0, so the data do not show that A is better.
5. Always report intervals, and compare models on the same patients.

## Clip 3: Shortcuts and hidden subgroups

1. A model can learn the wrong signal. DeGrave et al.: COVID-19 classifiers trained on positives and negatives from
   different sources learned the sources.
2. Saliency and counterfactual images showed laterality markers, text annotations, image borders, and patient
   positioning driving predictions, not only the lungs.
3. On data from new sources, performance fell by about half.
4. Averages hide subgroups (synthetic): sensitivity 0.85 overall, but 0.90 in group A (80% of patients) and 0.65 in
   group B (20%): 0.8 x 0.90 + 0.2 x 0.65 = 0.85.
5. Checks: external validation on new sites, subgroup reporting, and tests for whether site or scanner can be
   predicted from the model's features.

## Notebook (week12_evaluation.ipynb, CPU)

Bootstrap and paired bootstrap on the synthetic 200-patient example; a toy shortcut: a classifier that learns a
"hospital marker" in synthetic images and fails when the marker moves; subgroup sensitivity tables. All examples
biomedical; commit and push after each clip.
