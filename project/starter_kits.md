# Project starter kits

Starting points for the suggested problems, for teams that do not arrive with their own topic. Each kit gives a
question, data and how to get it, a baseline to beat, a plan, how to evaluate, and pitfalls. Treat them as a starting
point: a good proposal narrows the question, names a hypothesis, and says what result would change your mind.

## Before you pick: data access

- **Open data** (download now): MedMNIST, the Kather colorectal H&E datasets, PTB-XL, MedQA, PubMedQA, the MIMIC-IV
  Clinical Database Demo (100 patients), and Synthea synthetic patients.
- **Credentialed or registration data** (start in Week 1): MIMIC-IV, MIMIC-IV-Note, MIMIC-CXR, and eICU on PhysioNet
  need CITI human-subjects training plus a PhysioNet credentialing request, which together can take several weeks. CheXpert
  needs a free registration with Stanford.
- **Rules for credentialed data:** work on HiPerGator, never on Colab or a personal laptop you share; never paste or
  upload records to online AI services (ChatGPT, Claude, Gemini, or any hosted API); never commit data to GitHub.
  Use local open models for anything that touches patient text.
- **Compute:** every kit below is sized for one GPU on HiPerGator, and most can be prototyped on a CPU.

---

## 1. Long clinical notes with a small open LLM (Week 4)

**Question.** For questions about a long discharge summary, does a long-context small model beat a short-context model
plus retrieval?
**Data.** MIMIC-IV-Note discharge summaries (credentialed). Build questions whose answers are in the structured MIMIC-IV
tables (discharge medications, primary diagnosis codes, length of stay), so you get ground truth without manual labels.
**Baseline.** A small open model (about 1B to 8B parameters) reading only the first part of the note that fits its window.
**Plan.** Compare (a) the full note in a long context, (b) chunk, embed, and retrieve the top passages into a short
context, (c) the baseline. Vary note length.
**Evaluate.** Exact-match or F1 against the structured answers, by note length; also memory and time per note.
**Pitfalls.** Notes and structured tables can disagree; check a sample by hand. Run models locally on HiPerGator.

## 2. Reasoning versus non-reasoning on medical question answering (Week 5)

**Question.** When does "thinking" help a small model on medical questions, and is it worth the tokens? Optionally,
does a short LoRA fine-tune beat prompting?
**Data.** MedQA (USMLE-style) and PubMedQA (open).
**Baseline.** The same small open model answering directly, with no reasoning prompt.
**Plan.** A reasoning prompt versus a direct answer; then a LoRA fine-tune on a training split; compare accuracy and tokens per question.
**Evaluate.** Accuracy with bootstrap confidence intervals; calibration of the model's stated confidence; tokens and time.
**Pitfalls.** Benchmark contamination (the model may have seen the questions); report it as a limitation and, if
possible, test on questions you rewrite.

## 3. Label efficiency of imaging foundation models (Week 6)

**Question.** As labeled data shrinks, how do a linear probe and LoRA fine-tuning of a pretrained encoder compare?
**Data.** NCT-CRC-HE-100K or the smaller Kather 2016 tiles (colorectal H&E, CC BY 4.0), or a MedMNIST dataset.
**Baseline.** The same architecture trained from scratch, and the encoder with random weights.
**Plan.** Encoders: DINOv2 and a pathology encoder if you can get access (UNI is gated on Hugging Face). Label budgets of
1, 10, 100 per class and the full set.
**Evaluate.** Balanced accuracy with confidence intervals across several random label samples.
**Pitfalls.** Tiles from the same slide or patient must not appear in both training and test sets.

## 4. Self-supervised pretraining for ECG (Week 6)

**Question.** For ECG, does masked reconstruction or contrastive pretraining give better features with few labels?
**Data.** PTB-XL (PhysioNet, open access, CC BY 4.0): 10-second 12-lead ECGs at 500 Hz, with recommended folds.
**Baseline.** Supervised training from scratch; a random-weight encoder.
**Plan.** Pretrain a small 1D encoder both ways on the training folds, then probe and fine-tune on diagnostic labels
with few labels per class.
**Evaluate.** Macro AUROC on the official test fold; label-efficiency curves.
**Pitfalls.** The Week 6 notebook shows a tiny masked autoencoder can learn almost nothing; check reconstructions and
the loss curve before trusting any probe result. Use the provided folds so patients do not leak.

## 5. Zero-shot versus fine-tuned vision-language models for chest X-ray (Week 7)

**Question.** How far is zero-shot classification from a few-label linear probe on chest X-ray findings, and do
subgroups differ?
**Data.** CheXpert (registration) or MIMIC-CXR (credentialed).
**Baseline.** A linear probe on a general CLIP image encoder.
**Plan.** BiomedCLIP or another medical vision-language encoder: zero-shot with several prompt wordings, then linear
probes with small label budgets.
**Evaluate.** AUROC per finding with confidence intervals; the same metrics by sex and age group.
**Pitfalls.** Labels extracted from reports are noisy; uncertain labels need an explicit policy.

## 6. Patient timelines as tokens versus gradient boosting (Week 8)

**Question.** Does a small timeline transformer beat gradient-boosted trees for an ICU outcome, and which stays
calibrated when time moves on?
**Data.** MIMIC-IV (credentialed); its anchor year groups allow a train-on-earlier, test-on-later split. eICU for a
second site.
**Baseline.** Gradient-boosted trees on hand-built features from the first 24 hours.
**Plan.** Tokenize timelines as in ETHOS (codes, quantile tokens, time-gap tokens); train a small decoder; predict
in-ICU mortality.
**Evaluate.** AUROC, AUPRC (low prevalence), and calibration, on a random split and on a later-years split.
**Pitfalls.** Leakage from events after the prediction time; define the prediction time first and cut the timeline there.

## 7. Multimodal fusion when a modality is missing (Week 7)

**Question.** Does late or intermediate fusion of chest X-rays and EHR data still help when one modality is missing?
**Data.** MIMIC-IV with MIMIC-CXR (credentialed), linked by patient and time.
**Baseline.** The best single-modality model.
**Plan.** Late fusion (average predictions) versus intermediate fusion (combine embeddings), trained with random
modality dropout; test with each modality removed.
**Evaluate.** AUROC with confidence intervals for complete and missing-modality test sets.
**Pitfalls.** Patients with imaging differ from patients without it; missingness itself is a signal.

## 8. Retrieval for clinical question answering (Week 9)

**Question.** Does retrieval improve accuracy and faithfulness of a small model's answers, and when should it abstain?
**Data.** PubMedQA (questions with source abstracts) and MedQA; a corpus of PubMed abstracts.
**Baseline.** The same model without retrieval.
**Plan.** Embed and retrieve passages; vary top-k and an abstention threshold, as in Almanac.
**Evaluate.** Accuracy; faithfulness (is each claim supported by a retrieved passage, judged on a sample by hand);
abstention rate on answerable questions.
**Pitfalls.** An abstaining system looks safe on adversarial tests; always report how often it abstains on real questions.

## 9. A tool-using agent for a structured clinical task (Week 9)

**Question.** Where do tool-using agents fail on a structured clinical task, such as medication reconciliation or a
lab-trend question?
**Data.** Synthea synthetic patients or the MIMIC-IV Clinical Database Demo (open); no credentialed data needed.
**Baseline.** The same model answering from a pasted record without tools.
**Plan.** Build two or three read-only tools (get labs, get medications, get notes); run a ReAct-style loop on 50 to
100 tasks with known answers.
**Evaluate.** Task success; a failure taxonomy (wrong tool, wrong arguments, misread result, reasoning error).
**Pitfalls.** Keep every tool read-only; log full trajectories so failures can be classified.

## 10. Shortcut audit of a medical imaging classifier (Week 12)

**Question.** Can the hospital or scanner be predicted from an imaging model's features, and does that hurt
performance at a new site?
**Data.** Two chest X-ray sources (for example CheXpert and MIMIC-CXR), or two MedMNIST-style sources.
**Baseline.** Internal test performance.
**Plan.** Train on one source; probe the features for source; test on the other source; try a mitigation (for example
balancing or source-adversarial training).
**Evaluate.** Source-prediction accuracy from features; internal versus external AUROC with confidence intervals.
**Pitfalls.** Differences in labels between sources can look like a shortcut; compare findings both sources label the same way.

## 11. Uncertainty under distribution shift (Week 12)

**Question.** Do conformal prediction sets keep their promised coverage when the test data shift?
**Data.** Any classifier above, with an in-distribution and a shifted test set (another site, later years, or another stain).
**Baseline.** Coverage and set size in distribution.
**Plan.** Split conformal prediction at 90% target coverage; measure coverage under shift; try a simple fix such as
recalibrating on a small sample from the new setting.
**Evaluate.** Coverage, average set size, and coverage by subgroup.
**Pitfalls.** Coverage is a promise about averages; report subgroups, where it often fails first.

## 12. Reproduce a key result and extend it (any week)

**Question.** Does a central result of one course paper hold, and does it survive one change you choose (a new dataset,
subgroup, or metric)?
**Plan.** Pick a paper with public code and data; reproduce one table or figure; then make one extension.
**Evaluate.** How close your reproduction is, with confidence intervals; what the extension changes.
**Pitfalls.** Budget most of your time for the reproduction; contact the authors early if something does not match.
