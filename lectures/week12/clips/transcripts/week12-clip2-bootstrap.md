# How sure are we? The bootstrap

Week 12, clip 2 of 3. This is the narration of the clip, which an AI-generated voice reads in the
[narrated version](../narrated/week12-clip2-bootstrap-narrated.mp4); the [silent
version](../silent/week12-clip2-bootstrap.mp4) shows the same steps with on-screen captions only.

A synthetic test set of 200 patients. Model A is right on 170, 85%, and model B on 164, 82%. The
question is how much of that three-point gap is just which patients we happened to test.

The bootstrap answers that by resampling. Draw 200 patients with replacement, so some appear more
than once, recompute the accuracy, and repeat 10,000 times. The spread of those 10,000 numbers is
the uncertainty.

Model A's interval runs from 0.80 to 0.90, and model B's from 0.77 to 0.87. They overlap, but
overlapping intervals are not a test. Each one answers a question about one model on its own.

Both models were graded on the same 200 patients. A is right where B is wrong 14 times, and B is
right where A is wrong 8 times. 14 minus 8 is 6 patients, which is exactly the three-point
difference.

Bootstrapping the difference on the same resampled patients gives 0.03, with a 95% interval from
minus 0.015 to 0.075. It includes zero, so these data do not show that A is better. They do not show
the models are equal either.

Pairing matters. On the same data, ignoring it widens the interval to minus 0.045 to 0.105, about
two thirds wider. Report intervals rather than point estimates, and compare models on the same
patients.
