# Animation source

The Week 8 clips are written with [Manim Community](https://www.manim.community/). Each clip is one scene class. The shared colors, caption bar, and helpers, including the synthetic ECG generator (`ecg_fn`, `wave`), are in [`lectures/_shared/kit.py`](../../_shared/kit.py).

| File | Scene | Clip |
|---|---|---|
| clip1_timeline_tokens.py | C1 | A patient timeline as tokens |
| clip2_rollouts.py | C2 | Zero-shot prediction by simulating the future |
| clip3_irregular_signals.py | C3 | Irregular sampling and physiological signals |

Build all three clips, silent and narrated, from the repository root:

```bash
python tools/build_clips.py week08
```

The narration lines are in [`../clips.json`](../clips.json). See [`tools/README.md`](../../../tools/README.md) for setup. The clips use only text objects, so LaTeX is not required.

**Data sources.** The patient, the ICU day, and the ECG are synthetic: no real patient data. The tokenization rules (codes split into up to three parts, 10 quantiles from the training data, 13 interval tokens with none under 5 minutes, 6 static tokens, a 2,048-token sliding context, 20 simulated trajectories) and the results (ICU mortality AUC 0.927 at 7.0% prevalence, hospital mortality AUC 0.921 at 2.0%, DRG top-1 accuracy 84.8% of 771 classes, 241,015 patients for training and validation) are from Renc et al. (ETHOS), checked against the arXiv preprint and the npj Digital Medicine article. The 84 reviewed models are from Wornow et al. The 20 rollouts, the 7 deaths, the false-alarm example, the quantile cutoffs, and the ICU-day values are illustrative.
