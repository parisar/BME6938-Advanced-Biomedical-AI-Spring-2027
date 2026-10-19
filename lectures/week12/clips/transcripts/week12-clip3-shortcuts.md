# Shortcuts and hidden subgroups

Week 12, clip 3 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week12-clip3-shortcuts-narrated.mp4); the [silent
version](../silent/week12-clip3-shortcuts.mp4) shows the same steps with on-screen captions only.

A model can reach a high score by reading the wrong thing. The score tells you the label came out
right. It does not tell you which part of the image produced it.

DeGrave and colleagues built two datasets. The first takes positives from GitHub-COVID and negatives
from ChestX-ray14, so source and label line up almost exactly. The second, from BIMCV and PadChest,
is one region and one research team: the favorable case.

Saliency maps and generative counterfactuals showed what the models used: laterality markers, arrows
and text found only in one archive, the radiopacity of the image borders, and patient positioning.
Moving the clavicle region to the top border raised the predicted odds of COVID 19.

On radiographs from a new hospital system, half of the predictive performance was lost. The authors
concluded that only a minority of it was ever genuine COVID 19 pathology. The rest was the source,
not the disease.

Here is the part that catches people out. Some shortcuts do not transfer, so the score falls and you
see it. Others, like patient positioning, are consistent in both datasets: the score holds up and
the model is still not reading the lungs. External validation is necessary, not sufficient.

An average hides the group a model works worst on. Sensitivity of 0.85 overall can be 0.90 in 80% of
patients and 0.65 in the other 20. Report subgroups with intervals, validate externally, look at
what the model uses, and test whether the site can be predicted from its features.
