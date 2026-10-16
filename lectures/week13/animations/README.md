# Animation source

The Week 13 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_external.py | C1 | What external validation found |
| clip2_thresholds.py | C2 | Thresholds, alert burden, and drift |
| clip3_teaming.py | C3 | Humans and models together |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week13
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects and shapes drawn in code, so LaTeX is not required and no third-party figures are used.

**Data sources.** The sepsis numbers in clip 1 are from Wong et al., JAMA Internal Medicine 2021: 27,697 patients and 38,455 hospitalizations at Michigan Medicine between 6 December 2018 and 20 October 2019, sepsis in 2,552 (7%), the Epic Sepsis Model scored every 15 minutes, a hospitalization-level AUC of 0.63 (95% CI 0.62 to 0.64) against 0.76 to 0.83 reported by Epic Systems in internal documentation shared with permission, per-time-horizon AUCs of 0.72 to 0.76 that the authors describe as misleading because the predictions are not independent, poor calibration at every horizon, and at a score threshold of 6 a sensitivity of 33%, specificity 83%, positive predictive value 12%, negative predictive value 95%, alerts for 6,971 of 38,455 hospitalizations (18%), a number needed to evaluate of 8, and a median lead time of 2.5 hours (IQR 0.5 to 15.6). The model missed 1,709 patients with sepsis (67%), of whom 1,030 (60%) still received timely antibiotics, and identified 183 (7%) who had not received timely antibiotics.

The three operating points in clip 2 (sensitivity 80% with PPV 10%, 50% with 20%, 25% with 35%) are illustrative and labelled as such. The alerts per 100 admissions and the number needed to evaluate are computed in the scene file from those pairs at 7% prevalence rather than typed in, so they cannot drift from the arithmetic. The score distributions in segment 1 are drawn to the same height, with a note on screen that sepsis is 7% of patients so the red curve is really much smaller. The monitoring chart in segment 5 is illustrative.

The clinician and model sensitivities in clip 3 (0.80 and 0.75) are illustrative. The 100-case grids are computed in the scene file under two stated assumptions, independent errors and nested misses, and both are labelled as assumptions on screen. The ambient intelligence results are from the primary studies rather than from the Haque et al. review: Singh et al., JAMIA 2020 (16 privacy-safe depth sensors in one acute care unit, algorithm sensitivity 92.1% with 95% CI 84.3 to 96.7 against human observers at 85.2% with 95% CI 76.1 to 91.1, on a test set of 88 dispenser-use events) and Yeung et al., npj Digital Medicine 2019 (7 wall-mounted depth sensors, 563 mobility-activity instances, mean sensitivity 87.2% over four activities, 68.8% accuracy at counting the personnel involved). Haque et al., Nature 2020, is cited for what ambient intelligence is and for the barriers its abstract names: rigorous clinical validation, appropriate data privacy, and model transparency.
