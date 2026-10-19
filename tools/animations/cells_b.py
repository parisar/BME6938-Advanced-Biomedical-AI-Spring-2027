"""Animation cells for Weeks 7 to 13. Same contract as cells_a."""

from cells_a import HEAD

CELLS = {}

# ---------------------------------------------------------------- Week 7
CELLS['week07_vision_language'] = (14, '''### 1.5b Watch the embedding space sort itself out

Section 1.5 wrote the loss down. The animation runs it, on six synthetic pairs, so you can watch what it does to the
space.

Every encoder output is a unit vector, so the shared embedding space is a circle here rather than the 512-dimensional
sphere CLIP uses. Blue points are tiles, orange points are captions, and a line joins each tile to its own caption. At
the start the pairing is arbitrary and the similarity matrix on the right is a mess. Each step applies the gradient the
loss asks for: pull a pair together, push everything else in the batch apart.

What to notice is that the matrix goes diagonal without anyone ever being told what a tumour looks like. The only
supervision is which caption came with which tile, and that is free: it is how the data was stored in the first place.''',
 HEAD + '''
N, STEPS, TEMP = 6, 60, 0.10                                 # pairs in the batch, training steps, temperature
LABELS = ["tumour", "stroma", "lymphocytes", "mucosa", "debris", "adipose"]
rng = np.random.default_rng(1)
img = rng.uniform(0, 2 * np.pi, N)                           # each tile embedding, as an angle on the circle
txt = rng.uniform(0, 2 * np.pi, N)                           # each caption embedding, likewise

def sims(a, b):
    """Cosine similarity between every tile and every caption, which on a circle is cos of the angle between them."""
    return np.cos(a[:, None] - b[None, :])

hist = [(img.copy(), txt.copy())]                            # record the whole run, then animate it
for _ in range(STEPS):
    S = sims(img, txt) / TEMP
    P = np.exp(S - S.max(1, keepdims=True)); P = P / P.sum(1, keepdims=True)   # softmax along each row
    # The InfoNCE gradient, in words: move each caption toward its own tile, and
    # away from every tile that is currently giving it weight it has not earned.
    pull = np.zeros(N)
    for i in range(N):
        for j in range(N):
            d = np.sin(img[i] - txt[j])                      # direction that increases cos(img_i - txt_j)
            pull[j] += (1.0 if i == j else 0.0) * d - P[i, j] * d
    txt = (txt + 0.45 * pull) % (2 * np.pi)
    img = (img - 0.18 * np.array([np.sin(img[i] - txt[i]) for i in range(N)])) % (2 * np.pi)
    hist.append((img.copy(), txt.copy()))

fig, (circ, mat) = plt.subplots(1, 2, figsize=(9.2, 3.9),
                                gridspec_kw={"width_ratios": [1.1, 1]})
fig.subplots_adjust(wspace=0.35)

def draw(f):
    a, b = hist[f]
    circ.clear(); mat.clear()

    # ---- left: the shared embedding space
    th = np.linspace(0, 2 * np.pi, 200)
    circ.plot(np.cos(th), np.sin(th), color="#E5E7EB", lw=1.2)
    for i in range(N):
        circ.plot([np.cos(a[i]), np.cos(b[i])], [np.sin(a[i]), np.sin(b[i])],
                  color="#C7CDD1", lw=1.0, zorder=0)         # the line joining a true pair
    circ.scatter(np.cos(a), np.sin(a), s=70, color=UF, zorder=3, label="tile")
    circ.scatter(np.cos(b), np.sin(b), s=70, color=ORANGE, zorder=3, marker="s", label="caption")
    for i in range(N):
        circ.annotate(LABELS[i], (np.cos(a[i]) * 1.17, np.sin(a[i]) * 1.17),
                      ha="center", va="center", fontsize=8.5, color="#374151")
    circ.set_xlim(-1.45, 1.45); circ.set_ylim(-1.45, 1.45)
    circ.set_aspect("equal"); circ.axis("off")
    circ.legend(loc="lower right", fontsize=9, frameon=False)
    circ.set_title(f"step {f} of {STEPS}", loc="left", fontsize=11, color="#374151")

    # ---- right: the similarity matrix the loss actually sees
    S = sims(a, b)
    mat.imshow(S, cmap="Blues", vmin=-1, vmax=1)
    mat.set_xticks(range(N)); mat.set_xticklabels(LABELS, fontsize=8, rotation=40, ha="right")
    mat.set_yticks(range(N)); mat.set_yticklabels(LABELS, fontsize=8)
    mat.set_xlabel("caption", fontsize=10); mat.set_ylabel("tile", fontsize=10)
    acc = (S.argmax(1) == np.arange(N)).mean()               # how many rows pick their own caption
    mat.set_title(f"rows picking their own caption: {acc * 100:.0f}%",
                  loc="left", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=len(hist), interval=90)
plt.close(fig)
HTML(ani.to_jshtml(fps=11))''')

# ---------------------------------------------------------------- Week 8
CELLS['week08_ehr_time_series'] = (23, '''### 2.6b Watch the risk move as the record grows

The sections above computed one risk estimate from one point in a record. In a hospital the estimate is recomputed as the
record grows, and that is a different thing to look at.

The top panel is a synthetic admission: vitals arriving irregularly, with events marked underneath. The window slides
forward and the model only ever sees what is to the left of it, which is the constraint that makes this prediction rather
than hindsight. The bottom panel is the risk it returns, with the alert threshold drawn across it.

Watch how often the risk crosses the line and comes back. Every one of those crossings is a page to a clinician at three
in the morning, and section 2.6 is where the arithmetic of that burden lives. A model can be well calibrated and still be
unusable if it changes its mind this often.''', HEAD + '''
HOURS, FS = 48, 4                                            # length of the admission, samples per hour
n = HOURS * FS
t = np.arange(n) / FS
rng = np.random.default_rng(3)

# A synthetic admission that deteriorates late: heart rate drifts up, blood pressure down.
hr = 78 + np.cumsum(rng.normal(0, 0.45, n)) + 22 * (1 / (1 + np.exp(-(t - 34) / 2.5)))
sbp = 124 - np.cumsum(rng.normal(0, 0.35, n)) - 18 * (1 / (1 + np.exp(-(t - 36) / 2.5)))
EVENTS = [(6, "antibiotics"), (18, "lactate 2.4"), (31, "ICU transfer"), (40, "vasopressor")]

def risk(upto):
    """A deliberately simple score: recent heart rate up, recent pressure down, over the record so far."""
    k = max(8, upto)
    w = slice(max(0, k - 24), k)                             # the last six hours of samples
    z = (hr[w].mean() - 80) / 18 - (sbp[w].mean() - 120) / 20
    return float(1 / (1 + np.exp(-z)))                       # squashed into 0 to 1

STEP = 4                                                     # advance the window one hour per frame
cuts = list(range(8, n + 1, STEP))
scores = [risk(c) for c in cuts]
THRESH = 0.55

fig, (top, bot) = plt.subplots(2, 1, figsize=(9.2, 4.3), sharex=True,
                               gridspec_kw={"height_ratios": [1.3, 1]})
fig.subplots_adjust(hspace=0.3)

def draw(f):
    c = cuts[f]
    top.clear(); bot.clear()

    # ---- top: the record, with everything after "now" greyed out
    top.plot(t[:c], hr[:c], color=UF, lw=1.3, label="heart rate")
    top.plot(t[:c], sbp[:c], color="#5B8DEF", lw=1.3, label="systolic BP")
    top.plot(t[c:], hr[c:], color="#E5E7EB", lw=1.0)
    top.plot(t[c:], sbp[c:], color="#E5E7EB", lw=1.0)
    top.axvline(t[c - 1], color=ORANGE, lw=1.6)              # "now"
    for h, lab in EVENTS:
        if h <= t[c - 1]:
            top.annotate(lab, (h, 150), fontsize=8.5, rotation=90, va="top", color="#374151")
            top.axvline(h, color="#C7CDD1", lw=0.8, ls=":")
    top.set_ylim(55, 155); top.set_ylabel("value", fontsize=10)
    top.legend(loc="lower left", fontsize=9, frameon=False, ncols=2)
    top.spines[["top", "right"]].set_visible(False)
    top.set_title(f"hour {t[c - 1]:.0f} of {HOURS}: the model sees only the left of the line",
                  loc="left", fontsize=11, color="#374151")

    # ---- bottom: the risk recomputed at every hour
    bot.plot(t[np.array(cuts[:f + 1]) - 1], scores[:f + 1], color=UF, lw=2.0)
    bot.axhline(THRESH, color=ORANGE, lw=1.2, ls="--")
    bot.text(0.3, THRESH + 0.03, f"alert threshold {THRESH}", fontsize=9, color=ORANGE)
    over = [(x, s) for x, s in zip(t[np.array(cuts[:f + 1]) - 1], scores[:f + 1]) if s >= THRESH]
    if over:
        bot.scatter(*zip(*over), color=ORANGE, s=22, zorder=3)
    bot.set_xlim(0, HOURS); bot.set_ylim(0, 1)
    bot.set_xlabel("hours since admission", fontsize=10)
    bot.set_ylabel("risk", fontsize=10)
    bot.spines[["top", "right"]].set_visible(False)
    bot.set_title(f"alerts raised so far: {len(over)}", loc="right", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=len(cuts), interval=95)
plt.close(fig)
HTML(ani.to_jshtml(fps=11))''')

# ---------------------------------------------------------------- Week 9
CELLS['week09_retrieval_agents'] = (27, '''### 3.1b Watch a run of twenty steps

Section 3.1 printed the curve. The animation runs the agent instead, which makes the same point harder to argue with.

The top row is one trajectory: each box is a step, green if it went right and orange if it did not, sampled at 95%
per-step reliability. The run is counted as a success only if the whole row is green, because an agent that books the
wrong appointment at step 11 has failed no matter how good steps 1 to 10 were.

The bottom panel keeps score over many runs and draws the two curves beside the observed rate. At twenty steps, 95% per
step is a coin flip for the trajectory, and the gap to the 99% curve is the entire argument for fewer steps, checked
results, and a clinician at the end of the chain.''', HEAD + '''
STEPS, RUNS, P95, P99 = 20, 400, 0.95, 0.99                  # steps per run, runs, the two reliabilities
rng = np.random.default_rng(7)
trajectories = rng.random((RUNS, STEPS)) < P95               # True where a step went right
first_fail = np.where(trajectories.all(1), STEPS, trajectories.argmin(1))   # where each run first broke
ns = np.arange(1, STEPS + 1)

fig, (row, curve) = plt.subplots(2, 1, figsize=(9.0, 4.2),
                                 gridspec_kw={"height_ratios": [0.7, 1.3]})
fig.subplots_adjust(hspace=0.55)

def draw(f):
    r = f                                                    # the run being shown
    row.clear(); curve.clear()

    # ---- top: one trajectory, step by step
    ok = trajectories[r]
    row.set_xlim(-0.5, STEPS - 0.5); row.set_ylim(-0.6, 0.6); row.axis("off")
    for s in range(STEPS):
        broke = s >= first_fail[r]                           # everything from the first failure is wasted
        row.add_patch(plt.Rectangle((s - 0.42, -0.3), 0.84, 0.6,
                                    fc=("#E5E7EB" if broke else "#1F9D55") if s != first_fail[r] else ORANGE,
                                    ec="white", lw=1.2))
        row.text(s, 0, str(s + 1), ha="center", va="center", fontsize=8,
                 color="white" if not broke or s == first_fail[r] else "#9CA3AF")
    done = ok.all()
    row.set_title(f"run {r + 1}: " + ("all {} steps correct".format(STEPS) if done
                                      else f"first wrong step at {first_fail[r] + 1}"),
                  loc="left", fontsize=11, color="#1F9D55" if done else ORANGE)

    # ---- bottom: the observed success rate against the two curves
    seen = trajectories[:r + 1]
    obs = [(seen[:, :k].all(1)).mean() for k in ns]          # fraction of runs still correct after k steps
    curve.plot(ns, P95 ** ns, color=ORANGE, lw=2.0, label="0.95 per step")
    curve.plot(ns, P99 ** ns, color=UF, lw=2.0, label="0.99 per step")
    curve.plot(ns, obs, color="#111827", lw=1.4, ls=":", label=f"observed, {r + 1} runs")
    curve.set_xlim(1, STEPS); curve.set_ylim(0, 1.02)
    curve.set_xlabel("steps in the trajectory", fontsize=10)
    curve.set_ylabel("whole run correct", fontsize=10)
    curve.legend(loc="lower left", fontsize=9, frameon=False)
    curve.spines[["top", "right"]].set_visible(False)
    curve.set_title(f"at {STEPS} steps: 0.95 gives {P95 ** STEPS:.2f}, 0.99 gives {P99 ** STEPS:.2f}",
                    loc="right", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=48, interval=140)
plt.close(fig)
HTML(ani.to_jshtml(fps=7))''')

# ---------------------------------------------------------------- Week 11
CELLS['week11_diffusion'] = (12, '''### 1.4 Watch the forward process run

Section 1.3 printed four checkpoints. The animation runs the same closed form continuously, on one synthetic backbone, so
you can see where the structure actually goes.

The left panel is the chain at step `t`, drawn against the clean chain in grey. The right panel is `signal_t`, the
fraction of the original that survives, with a marker at the current step.

The thing worth watching is how uneven the loss of structure is. Almost nothing happens for the first hundred steps, the
chain is unrecognisable somewhere in the middle, and the last few hundred steps only rearrange noise. That is why the
sampler in section 2.3 spends most of its effort in the middle of the schedule, and why the model is trained on steps
drawn uniformly: the interesting ones have to be hit often enough.

This is the forward direction only, which needs no model at all. The learned reverse is section 2.3.''',
 HEAD + '''
N, STEPS = 16, 1000                                          # points in a chain, steps in the schedule
rng = np.random.default_rng(0)

# One synthetic helix, the same family of shapes as section 1.1.
u = np.linspace(0, 1, N)
chain = np.stack([u * 2 - 1, 0.5 * np.sin(2.4 * 2 * np.pi * u)], 1)
chain = chain / np.abs(chain).max()                          # the rescaling section 1.1 explains

betas = np.linspace(1e-4, 0.02, STEPS)                       # the standard DDPM schedule
abar = np.cumprod(1.0 - betas)                               # signal_t: how much of x_0 is left at step t
eps = rng.normal(0, 1, chain.shape)                          # one fixed noise draw, so the animation is smooth

TS = np.unique(np.linspace(0, STEPS - 1, 45).astype(int))    # the steps we render

fig, (ax, sched) = plt.subplots(1, 2, figsize=(9.2, 3.6),
                                gridspec_kw={"width_ratios": [1.15, 1]})
fig.subplots_adjust(wspace=0.3)

def draw(f):
    t = TS[f]
    a = abar[t]
    x = np.sqrt(a) * chain + np.sqrt(1 - a) * eps            # the closed form, straight from clip 1
    ax.clear(); sched.clear()

    ax.plot(chain[:, 0], chain[:, 1], "-o", ms=3.5, color="#D1D5DB", lw=1.2)   # the clean chain, for reference
    ax.plot(x[:, 0], x[:, 1], "-o", ms=4.5, color=UF, lw=1.6)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(f"t = {t}      signal_t = {a:.3f}", loc="left", fontsize=11, color="#374151")

    sched.plot(np.arange(STEPS), abar, color="#C7CDD1", lw=1.6)
    sched.plot(np.arange(t + 1), abar[:t + 1], color=UF, lw=2.2)
    sched.scatter([t], [a], color=ORANGE, s=38, zorder=3)
    sched.set_xlim(0, STEPS); sched.set_ylim(0, 1.02)
    sched.set_xlabel("step t", fontsize=10)
    sched.set_ylabel("signal_t", fontsize=10)
    sched.spines[["top", "right"]].set_visible(False)
    return []

ani = FuncAnimation(fig, draw, frames=len(TS), interval=110)
plt.close(fig)
HTML(ani.to_jshtml(fps=9))''')

# ---------------------------------------------------------------- Week 12
CELLS['week12_evaluation'] = (7, '''### 1.2b Watch the interval appear

The bootstrap is one of those methods that sounds like cheating until you watch it run. The animation draws one resample
at a time and keeps the AUROC of each.

The left panel is the current resample: 200 patients drawn from the same 200 with replacement, so some appear twice and
some not at all. The right panel is the growing histogram of AUROCs, with the 2.5th and 97.5th percentiles marked.

What to watch is the interval settling. After twenty resamples the ends are still moving around; after a few hundred they
have stopped. That is the honest reading of a bootstrap interval: it is a statement about how much this test set could
have told you, and it stops shrinking because the limit is the sample, not the number of resamples.''', HEAD + '''
NPAT, NBOOT = 200, 300                                       # patients in the test set, resamples
rng = np.random.default_rng(0)
y = (rng.random(NPAT) < 0.3).astype(int)                     # 30% of patients have the outcome
score = np.clip(rng.normal(0.35 + 0.28 * y, 0.17), 0, 1)     # a model that separates them, imperfectly

def auroc(labels, s):
    """AUROC by ranks, which is the probability a random positive outranks a random negative."""
    pos, neg = labels.sum(), (1 - labels).sum()
    if pos == 0 or neg == 0:
        return np.nan
    order = np.argsort(s, kind="mergesort")
    ranks = np.empty(len(s)); ranks[order] = np.arange(1, len(s) + 1)
    return (ranks[labels == 1].sum() - pos * (pos + 1) / 2) / (pos * neg)

point = auroc(y, score)                                      # the estimate on the test set itself
idx = rng.integers(0, NPAT, (NBOOT, NPAT))                   # every resample, drawn up front
aucs = np.array([auroc(y[i], score[i]) for i in idx])

# Bin over the range the resamples actually cover: a fixed 0.5 to 1.0 window would
# put this whole interval inside three bars.
pad = (aucs.max() - aucs.min()) * 0.25
BINS = np.linspace(aucs.min() - pad, aucs.max() + pad, 34)

fig, (draw_ax, hist) = plt.subplots(1, 2, figsize=(9.4, 3.5),
                                    gridspec_kw={"width_ratios": [1, 1.25]})
fig.subplots_adjust(wspace=0.32)
STRIDE = 6                                                   # resamples added per frame, after the first few

def frame(f):
    b = min(NBOOT, 1 + f * STRIDE)                           # how many resamples drawn so far
    draw_ax.clear(); hist.clear()

    # ---- left: who is in the current resample, and how many times
    counts = np.bincount(idx[b - 1], minlength=NPAT)
    cols = [ORANGE if yi == 1 else UF for yi in y]           # orange for the patients with the outcome
    draw_ax.bar(np.arange(NPAT), counts, width=1.0, color=cols, linewidth=0)
    draw_ax.set_ylim(0, 5); draw_ax.set_xlim(0, NPAT)
    draw_ax.set_xlabel("patient in the test set", fontsize=10)
    draw_ax.set_ylabel("times drawn", fontsize=10)
    draw_ax.spines[["top", "right"]].set_visible(False)
    draw_ax.set_title(f"resample {b}: {int((counts == 0).sum())} patients left out",
                      loc="left", fontsize=11, color="#374151")

    # ---- right: the sampling distribution the resamples trace out
    hist.hist(aucs[:b], bins=BINS, color="#C7D2E8", edgecolor="white")
    lo, hi = np.percentile(aucs[:b], [2.5, 97.5]) if b > 2 else (np.nan, np.nan)
    for v, c in ((point, "#111827"), (lo, ORANGE), (hi, ORANGE)):
        if np.isfinite(v):
            hist.axvline(v, color=c, lw=1.8 if c == "#111827" else 1.3,
                         ls="-" if c == "#111827" else "--")
    hist.set_xlim(BINS[0], BINS[-1])
    hist.set_xlabel("AUROC of a resample", fontsize=10)
    hist.set_ylabel("count", fontsize=10)
    hist.spines[["top", "right"]].set_visible(False)
    if np.isfinite(lo):
        hist.set_title(f"AUROC {point:.3f}   95% CI {lo:.3f} to {hi:.3f}",
                       loc="left", fontsize=11, color="#374151")
    return []

ani = FuncAnimation(fig, frame, frames=NBOOT // STRIDE + 1, interval=90)
plt.close(fig)
HTML(ani.to_jshtml(fps=12))''')

# ---------------------------------------------------------------- Week 13
CELLS['week13_deployment'] = (7, '''### 1.2b Watch the threshold move

The table in section 1.2 has one row per threshold. The animation sweeps it instead, because the table makes the
trade-off look like a menu and the sweep makes it look like what it is: one dial, and everything moving at once.

The left panel is the two score distributions with the threshold laid across them. The right is what that threshold buys:
how many patients are flagged, how many of those flags are real, and how many real cases are missed.

The number to watch is precision. Sensitivity rises smoothly as the line moves left, which is the number that gets quoted,
while precision falls off a cliff, because at this prevalence the negatives outnumber the positives so heavily that even a
small false-positive rate buries the true alerts. That cliff is what section 1.3 asks you to pick a point on, and the
honest version of the question is not "which threshold is best" but "how many false alarms per real case will this ward
tolerate".''', HEAD + '''
N, PREV = 4000, 0.04                                         # patients on the ward over a year, and the event rate
rng = np.random.default_rng(2)
y = (rng.random(N) < PREV).astype(int)                       # who actually deteriorates
score = np.clip(rng.normal(0.30 + 0.30 * y, 0.14), 0, 1)     # the model's risk score
THS = np.linspace(0.95, 0.05, 46)                            # the sweep, strict to permissive

fig, (dist, bars) = plt.subplots(1, 2, figsize=(9.6, 3.6),
                                 gridspec_kw={"width_ratios": [1.2, 1]})
fig.subplots_adjust(wspace=0.35)
bins = np.linspace(0, 1, 45)

def draw(f):
    th = THS[f]
    flag = score >= th
    tp = int((flag & (y == 1)).sum()); fp = int((flag & (y == 0)).sum())
    fn = int((~flag & (y == 1)).sum())
    sens = tp / max(1, tp + fn)                              # of the real cases, how many were flagged
    prec = tp / max(1, tp + fp)                              # of the flags, how many were real
    dist.clear(); bars.clear()

    # ---- left: the two distributions and the line between them
    dist.hist(score[y == 0], bins=bins, color="#C7D2E8", edgecolor="white", label="no event")
    dist.hist(score[y == 1], bins=bins, color=ORANGE, edgecolor="white", alpha=0.85, label="deteriorates")
    dist.axvline(th, color="#111827", lw=2.0)
    dist.set_yscale("log")                                   # log, or the 4% of positives are invisible
    dist.set_xlabel("risk score", fontsize=10); dist.set_ylabel("patients (log)", fontsize=10)
    dist.legend(loc="upper right", fontsize=9, frameon=False)
    dist.spines[["top", "right"]].set_visible(False)
    dist.set_title(f"threshold {th:.2f}", loc="left", fontsize=11, color="#374151")

    # ---- right: what the ward actually experiences
    bars.barh([2, 1, 0], [tp + fp, tp, fn],
              color=["#111827", "#1F9D55", ORANGE], height=0.6)
    bars.set_yticks([2, 1, 0])
    bars.set_yticklabels(["flagged", "real, caught", "real, missed"], fontsize=10)
    bars.set_xlim(0, 700); bars.set_xlabel("patients per year", fontsize=10)
    for yy, v in ((2, tp + fp), (1, tp), (0, fn)):
        bars.text(v + 10, yy, str(v), va="center", fontsize=10, color="#374151")
    bars.spines[["top", "right"]].set_visible(False)
    bars.set_title(f"sensitivity {sens:.2f}    precision {prec:.2f}    "
                   f"{(tp + fp) / 365:.1f} alerts a day",
                   loc="left", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=len(THS), interval=110)
plt.close(fig)
HTML(ani.to_jshtml(fps=9))''')
