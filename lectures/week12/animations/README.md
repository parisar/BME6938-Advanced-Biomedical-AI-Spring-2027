# Animation source

The Week 12 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_trial.py | C1 | A benchmark score is not a clinical effect |
| clip2_bootstrap.py | C2 | How sure are we? The bootstrap |
| clip3_shortcuts.py | C3 | Shortcuts and hidden subgroups |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week12
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects and shapes drawn in code, so LaTeX is not required and no third-party figures are used.

**Data sources.** The trial numbers in clip 1 are from Goh et al., JAMA Network Open 2024: 50 physicians randomized 25 and 25, stratified by career stage, up to 6 vignettes in 60 minutes, a median diagnostic reasoning score per case of 76% (IQR 66 to 87) against 74% (IQR 63 to 84), an adjusted difference of 2 percentage points (95% CI −4 to 8, P = .60), a median time per case of 519 s against 565 s with a difference of −82 s (95% CI −195 to 31), and a standalone arm of 3 runs with a median of 92% (IQR 82 to 97) scoring 16 points above the control group (95% CI 2 to 30, P = .03). The time outcome is shown with its interval and no P value: the article text reports P = .20 and Table 3 reports .15.

The 200-patient test set in clip 2 is synthetic and illustrative, built from an agreement table of 156 both right, 14 only A, 8 only B, and 22 both wrong, which gives 170 and 164. The confidence intervals on screen are not typed in: the scene file draws 10,000 bootstrap resamples with a fixed seed and computes the percentiles, so the clip and [the notebook](../../notebooks/week12_evaluation.ipynb) report the same numbers.

The shortcut findings in clip 3 are from DeGrave et al., Nature Machine Intelligence 2021: Dataset I from GitHub-COVID and NIH ChestX-ray14, Dataset II from BIMCV and PadChest, saliency maps and generative counterfactuals highlighting laterality markers, arrows and annotations unique to one archive, the radiopacity of image borders, and the shoulders, diaphragm and cardiac silhouette as proxies for patient positioning and AP against PA projection; moving the clavicle region to the top border raised the predicted odds of COVID-19; half the predictive performance is lost on the new source, and only a minority of it was genuine pathology. The chest radiograph is a schematic drawn from Manim primitives in `film()`, labelled as such on screen: no radiographic images are used. The subgroup numbers in the final segment (0.85 overall, 0.90 in 80% of patients, 0.65 in 20%) are illustrative and marked as such.
