# Notebook animations

One animation per notebook, inserted after the section it illustrates. Each is matplotlib `FuncAnimation` rendered
with `to_jshtml`, which needs no ffmpeg and plays in Colab, in Jupyter and on nbviewer.

```
python tools/animations/run.py cells_a      # render each cell on its own and report its size
python tools/animations/insert.py           # write them into lectures/notebooks/*.ipynb
```

`insert.py` is idempotent: it removes what an earlier run inserted, by looking for the `FuncAnimation` import, before
inserting again. Edit the cell in `cells_a.py` or `cells_b.py` and re-run it rather than editing a notebook by hand.

Two rules the cells follow, both so they can be tested without running the notebook they live in:

- **numpy and matplotlib only, and self-contained.** No torch, no network, no variable from an earlier cell. A reader
  can run the animation on its own, and `run.py` can execute all eleven in a few seconds.
- **the week's own running example.** The sentence "The patient has a cold" in Weeks 2 and 3, a synthetic ECG in Week 6,
  backbone chains in Week 11, and so on, so the animation and the rest of the notebook are about the same thing.

Keep the figures small, around 9 by 4 inches at 78 dpi with 35 to 60 frames. `to_jshtml` embeds every frame as a
base64 PNG, so the rendered output runs to 1 to 2 MB; at twice the dpi it is four times that and the slider stutters.
Notebook outputs are not committed, so this costs the repository nothing.
