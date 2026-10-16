# Term project: a research paper on an open problem in biomedical AI

Teams of three carry out an original study on an open problem in biomedical AI of their own choosing and report it as a research paper. Topics are approved at the proposal stage. Teams that do not have a topic may choose from the suggested problems below.

## Evaluation standard

Every paper must include:

- a comparison against an appropriate baseline,
- an evaluation that goes beyond a single aggregate metric (for example calibration, subgroup performance, or a distribution-shift or robustness test, as appropriate to the problem),
- a failure analysis.

## Milestones

| Milestone | Date | Deliverable | Weight |
|---|---|---|---|
| Start data-access training (if using credentialed data) | Jan 14 | CITI training and PhysioNet credentialing started |  |
| Teams formed | Jan 28 | Teams of three; names submitted |  |
| Proposal | Feb 19 | One page: open problem and why it matters, data, models and methods, hypothesis, evaluation plan | 5% |
| Pitch and peer review | Feb 23 | 2-min pitch in class; written review of one other proposal (counts toward participation) |  |
| Progress report | Mar 26 | One page with baseline results and remaining plan | 5% |
| Final presentation | Apr 13 | 12 min talk + 4 min questions; Tue Apr 13 (3 teams), Thu Apr 15 (5 teams), Tue Apr 20 (2 teams). Slides from all teams due before Tue Apr 13. | 10% |
| Final paper and repository | Apr 21 | 4-page conference-style paper; reproducible GitHub repository with README | 20% |

Templates: [proposal](proposal_template.md), [peer review](peer_review_form.md), [progress report](progress_report_template.md).

Pitch day (Tue Feb 23): [pitch_day.md](pitch_day.md). Final talk rubric: [presentation_rubric.md](presentation_rubric.md).

## Final paper rubric (100 points)

| Criterion | Points | What is assessed |
|---|---|---|
| Problem and clinical motivation | 15 | Clear open problem; why it matters; what is new relative to prior work |
| Methods | 25 | Sound choice and correct use of data, models, and methods for the stated problem; appropriate baseline |
| Evaluation rigor | 25 | Goes beyond a single aggregate metric (for example calibration, subgroups, or a shift or robustness test, as appropriate); proper data splits |
| Analysis and limitations | 15 | Failure analysis; honest limitations; what is shown versus claimed |
| Reproducibility | 10 | Repository runs from README; fixed seeds; environment specified |
| Writing and presentation | 10 | Clear figures and tables; conference format; within 4 pages |

## Suggested problems

| Problem | Course week | Possible open data |
|---|---|---|
| Long clinical notes with a small open LLM: sliding-window or compressed attention versus retrieval for discharge-summary question answering | 4 | MIMIC-IV-Note (credentialed), MedQA |
| Reasoning versus non-reasoning modes on medical question answering: accuracy, token cost, and calibration; LoRA fine-tuning versus prompting | 5 | MedQA, PubMedQA |
| Label efficiency of imaging foundation models: linear probe versus LoRA fine-tuning as labeled data shrinks | 6 | MedMNIST, Kather H&E tiles (NCT-CRC-HE-100K) |
| Self-supervised pretraining for ECG: masked modeling versus contrastive objectives | 6 | PTB-XL |
| Zero-shot versus fine-tuned vision-language models for chest X-ray findings, with a subgroup performance audit | 7 | CheXpert, MIMIC-CXR (credentialed) |
| Tokenized-timeline EHR transformer versus gradient-boosted baseline for ICU outcome prediction; calibration under temporal shift | 8 | MIMIC-IV, eICU (credentialed) |
| Does multimodal fusion help when a modality is missing? Late versus intermediate fusion of notes, vitals, or images | 7 | MIMIC-IV with MIMIC-CXR (credentialed) |
| Retrieval augmentation for clinical question answering: accuracy and faithfulness of cited evidence | 9 | MedQA, PubMedQA |
| Tool-using LLM agent for a structured clinical task; taxonomy of failure modes | 9 | Synthea synthetic patients, MIMIC-IV Clinical Database Demo |
| Shortcut audit of a medical imaging classifier: can site or scanner be decoded from embeddings, and does it hurt external validity? | 12 | CheXpert, MedMNIST |
| Uncertainty under distribution shift: conformal prediction for a medical classifier | 12 | Any of the above |
| Reproduce a key result from a course paper and add one extension | any | Dataset of the chosen paper |

Each problem has a starter kit (data and access, a baseline to beat, a plan, evaluation, and pitfalls): [starter_kits.md](starter_kits.md).

## Data and computing

- Datasets that require credentialed access (for example MIMIC-IV and MIMIC-CXR) need human-subjects training that can take several weeks. Start in Week 1 if you plan to use them.
- Open datasets such as PTB-XL, MedMNIST, and TCGA need no credentialing.
- Never commit patient data, credentials, or credentialed datasets to a repository.
- Computing is provided through HiPerGator.

## Final submission

- A 4-page conference-style paper (references do not count toward the limit).
- A GitHub repository that reproduces the main results from its README, with fixed seeds and a specified environment.
