"""Animation cells for Weeks 2 to 6.

Each entry is (insert_after_cell_index, markdown, code). The code is numpy and
matplotlib only and depends on nothing earlier in its notebook, so it runs in a
fresh kernel on Colab or HiPerGator and can be tested on its own. Rendering goes
through to_jshtml, which needs no ffmpeg.
"""

HEAD = '''# An animation, drawn by the code below. It renders with to_jshtml, which needs no
# ffmpeg and plays in Colab, in Jupyter, and on nbviewer. Press play, or drag the
# slider to step through it frame by frame.
import numpy as np                                           # arrays
import matplotlib.pyplot as plt                              # figures
from matplotlib.animation import FuncAnimation               # the animation itself
from IPython.display import HTML                             # shows it in the notebook

UF, ORANGE, GREY = "#0021A5", "#FA4616", "#6B7280"           # the course colours
plt.rcParams["figure.dpi"] = 78                              # keeps the rendered animation light
'''

CELLS = {}

# ---------------------------------------------------------------- Week 2
CELLS['week02_transformer_review_part1'] = (22, '''### 5.3 Watch the attention matrix fill in, one query at a time

Section 5.2 computed the whole matrix in one line, which is how it is done and which hides what it means. The animation
below builds the same matrix the way the clip does: one query token at a time. The top panel is the sentence, with an arc
from the current query to every key, the width of each arc being that key's weight. The bottom panel is the row of the
matrix those arcs correspond to.

Two things to watch for. Every row sums to one, because each row is a softmax: a query spreads a fixed budget of attention
over the keys. And "cold" attends to "patient", which is the whole point, since that is what tells the model this is the
illness and not the temperature.''', HEAD + '''
TOKENS = ["The", "patient", "has", "a", "cold"]              # the running example of the lecture
n = len(TOKENS)

# A hand-built attention matrix, not a random one: the numbers are chosen so the
# picture says what section 6 says. Each row is a softmax, so each row sums to 1.
rng = np.random.default_rng(0)
scores = rng.normal(0, 0.35, (n, n))                         # a little background variation
scores[4, 1] += 2.6                                          # "cold" looks hard at "patient"
scores[4, 2] += 0.9                                          # and a little at "has"
scores[1, 4] += 1.4                                          # "patient" looks back at "cold"
scores[0, 0] += 1.0; scores[3, 3] += 1.0                     # "The" and "a" mostly attend to themselves
A = np.exp(scores - scores.max(1, keepdims=True))            # softmax, row by row
A = A / A.sum(1, keepdims=True)                              # every row now sums to 1

HOLD = 8                                                     # frames spent on each query row
fig, (top, bot) = plt.subplots(2, 1, figsize=(8.4, 4.4),
                               gridspec_kw={"height_ratios": [1.25, 1]})
fig.subplots_adjust(hspace=0.45)
xs = np.arange(n)                                            # one x position per token

def draw(f):
    q, t = f // HOLD, (f % HOLD) / (HOLD - 1)                # which query, and how far into its reveal
    top.clear(); bot.clear()

    # ---- top panel: the sentence, with arcs from the query to every key
    top.set_xlim(-0.6, n - 0.4); top.set_ylim(-0.35, 1.25); top.axis("off")
    for i, w in enumerate(TOKENS):
        is_q = (i == q)
        top.text(i, 0, w, ha="center", va="center", fontsize=13,
                 color="white" if is_q else "#111827",
                 bbox=dict(boxstyle="round,pad=0.32",
                           fc=UF if is_q else "#EEF1F6",
                           ec=UF if is_q else "#C7CDD1"))
    for k in range(n):
        if k == q:
            continue
        w = A[q, k] * t                                      # the arc grows in over the hold
        mid, half = (q + k) / 2, abs(k - q) / 2              # a semicircle from query to key
        th = np.linspace(0, np.pi, 60)
        top.plot(mid + half * np.cos(th), 0.22 + 0.62 * half / (n / 2) * np.sin(th),
                 color=ORANGE, lw=0.6 + 7.5 * w, alpha=0.25 + 0.65 * min(1, w * 3), zorder=0)
    top.set_title(f'Query: "{TOKENS[q]}"  attends to every token, including itself',
                  loc="left", fontsize=11, color="#374151")

    # ---- bottom panel: the matrix, filled in up to the current row
    M = np.zeros((n, n))
    M[:q] = A[:q]                                            # rows already finished
    M[q] = A[q] * t                                          # the row being revealed
    bot.imshow(M, cmap="Blues", vmin=0, vmax=A.max(), aspect="auto")
    bot.set_xticks(xs); bot.set_xticklabels(TOKENS, fontsize=10)
    bot.set_yticks(xs); bot.set_yticklabels(TOKENS, fontsize=10)
    bot.set_xlabel("key (attended to)", fontsize=10)
    bot.set_ylabel("query", fontsize=10)
    for k in range(n):                                       # print the weights of the current row
        if M[q, k] > 0.04:
            bot.text(k, q, f"{M[q, k]:.2f}", ha="center", va="center", fontsize=9,
                     color="white" if M[q, k] > 0.45 else "#111827")
    bot.set_title(f"row sum so far: {M[q].sum():.2f}", loc="right", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=n * HOLD, interval=130)
plt.close(fig)                                               # stop the last frame printing twice
HTML(ani.to_jshtml(fps=8))''')

# ---------------------------------------------------------------- Week 3
CELLS['week03_transformer_review_part2'] = (12, '''### 4.1 Watch the mask grow as the text is generated

The mask is easier to believe once you watch it move. On the left the model generates one token at a time; on the right
the causal mask grows with it. The rule never changes: position `i` may attend to positions `0` through `i`, and the
cells above the diagonal stay black for ever.

The reason this matters is in the last frame. Every row of that triangle was a training example, all computed in one
forward pass, which is why a decoder learns from a sentence of five tokens five times over rather than once.''',
 HEAD + '''
TOKENS = ["The", "patient", "has", "a", "cold"]              # the same sentence as Week 2
n = len(TOKENS)
HOLD = 7                                                     # frames per generated token

fig, (left, right) = plt.subplots(1, 2, figsize=(9.2, 3.6),
                                  gridspec_kw={"width_ratios": [1.35, 1]})
fig.subplots_adjust(wspace=0.3)

def draw(f):
    i, t = f // HOLD, (f % HOLD) / (HOLD - 1)                # token being generated, and how far along
    left.clear(); right.clear()

    # ---- left: the sequence so far, with the newest token arriving
    left.set_xlim(-0.6, n - 0.4); left.set_ylim(-1, 1); left.axis("off")
    for k in range(n):
        if k > i:
            continue
        new = (k == i)
        left.text(k, 0, TOKENS[k], ha="center", va="center", fontsize=13,
                  alpha=t if new else 1.0,
                  color="white" if new else "#111827",
                  bbox=dict(boxstyle="round,pad=0.32", alpha=t if new else 1.0,
                            fc=ORANGE if new else "#EEF1F6",
                            ec=ORANGE if new else "#C7CDD1"))
    if i + 1 < n:
        left.text(i + 1, 0, "?", ha="center", va="center", fontsize=13, color=GREY,
                  bbox=dict(boxstyle="round,pad=0.32", fc="white", ec=GREY, ls=":"))
    left.set_title("generating left to right", loc="left", fontsize=11, color="#374151")

    # ---- right: the causal mask, one row per position
    M = np.full((n, n), np.nan)                              # nan is drawn as the background
    for r in range(i + 1):
        for c in range(n):
            M[r, c] = 1.0 if c <= r else 0.0                 # 1 allowed, 0 blocked
    right.imshow(np.nan_to_num(M, nan=0.5), cmap="Blues", vmin=0, vmax=1.4, aspect="auto")
    for r in range(n):
        for c in range(n):
            if r <= i:
                right.text(c, r, "" if c <= r else "x", ha="center", va="center",
                           fontsize=11, color="#9CA3AF")
    right.set_xticks(range(n)); right.set_xticklabels(TOKENS, fontsize=9, rotation=30, ha="right")
    right.set_yticks(range(n)); right.set_yticklabels(TOKENS, fontsize=9)
    right.set_title(f"rows filled: {i + 1} of {n}", loc="left", fontsize=11, color="#374151")
    return []

ani = FuncAnimation(fig, draw, frames=n * HOLD, interval=140)
plt.close(fig)
HTML(ani.to_jshtml(fps=7))''')

# ---------------------------------------------------------------- Week 4
CELLS['week04_modern_llms'] = (22, '''### 2.5 Watch the cache grow, and watch what it saves

Section 2.1 did the arithmetic and section 2.4 said why the cache exists. The animation puts the two together as the
sequence gets longer.

The left panel is the cache itself: one column per token, filling as generation proceeds, with the memory it occupies
printed above. It grows in a straight line, which is the problem the whole of section 2.2 exists to attack.

The right panel is why we pay that price anyway. Without a cache, generating token `n` means attending over all `n`
positions again, so the total work grows with the square of the length. With a cache, each new token attends over stored
keys and values and the total grows linearly. The gap between the two curves is what the memory is buying.''',
 HEAD + '''
N = 48                                                       # how many tokens we generate
KB_PER_TOKEN = 0.14                                          # megabytes of cache per token, a small-model figure
no_cache = np.cumsum(np.arange(1, N + 1))                    # work with no cache: 1 + 2 + ... + n, quadratic
with_cache = np.arange(1, N + 1)                             # work with a cache: one step per token, linear

fig, (left, right) = plt.subplots(1, 2, figsize=(9.4, 3.5),
                                  gridspec_kw={"width_ratios": [1.3, 1]})
fig.subplots_adjust(wspace=0.32)

def draw(i):
    n = i + 1                                                # tokens generated so far
    left.clear(); right.clear()

    # ---- left: the cache, one column per stored token
    left.set_xlim(0, N); left.set_ylim(0, 2.6); left.axis("off")
    left.bar(np.arange(n), np.ones(n), width=0.9, color=UF,
             edgecolor="white", linewidth=0.5)                   # the keys of each stored token
    left.bar(np.arange(n), np.ones(n), bottom=1.05, width=0.9, color="#5B8DEF",
             edgecolor="white", linewidth=0.5)                   # and the values
    left.text(0, 2.25, f"KV cache after {n} tokens: {n * KB_PER_TOKEN:.1f} MB",
              fontsize=11, color="#374151")
    left.text(-0.2, 0.5, "K", ha="right", va="center", fontsize=10, color=UF)
    left.text(-0.2, 1.55, "V", ha="right", va="center", fontsize=10, color="#5B8DEF")

    # ---- right: total attention work, with and without the cache
    right.plot(np.arange(1, n + 1), no_cache[:n], color=ORANGE, lw=2.2, label="recompute every step")
    right.plot(np.arange(1, n + 1), with_cache[:n], color=UF, lw=2.2, label="with a KV cache")
    right.set_xlim(1, N); right.set_ylim(0, no_cache[-1] * 1.05)
    right.set_xlabel("tokens generated", fontsize=10)
    right.set_ylabel("attention steps, cumulative", fontsize=10)
    right.legend(loc="upper left", fontsize=9, frameon=False)
    right.spines[["top", "right"]].set_visible(False)
    saved = no_cache[n - 1] - with_cache[n - 1]
    right.set_title(f"saved so far: {saved:,} steps", loc="right", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=N, interval=90)
plt.close(fig)
HTML(ani.to_jshtml(fps=12))''')

# ---------------------------------------------------------------- Week 5
CELLS['week05_post_training'] = (22, '''### 2.2b Watch rank buy back the update

LoRA's claim is that the change a fine-tune makes to a weight matrix is low rank, so a product of two thin matrices can
stand in for it. The animation tests that claim on a synthetic update: it sweeps the rank from 1 upward, and at each rank
shows the best possible approximation of that rank beside the update it is approximating.

The left pair is the target and the reconstruction. The right panel is the error, and the shape of that curve is the whole
argument: it falls steeply over the first few ranks and then flattens, so most of the update lives in a handful of
directions. The rank where it flattens is the rank worth paying for.

The approximation here comes from an SVD, which gives the best reconstruction of each rank and so an upper bound on what
LoRA can learn. A trained LoRA gets close to this curve, not above it.''', HEAD + '''
D, R_TRUE, MAXR = 40, 4, 16                                  # matrix size, true rank, highest rank we try
rng = np.random.default_rng(0)
# A synthetic weight update that is genuinely low rank, plus a little full-rank noise,
# which is what a real fine-tune looks like: mostly a few directions, not exactly.
dW = (rng.normal(0, 1, (D, R_TRUE)) @ rng.normal(0, 1, (R_TRUE, D))) / np.sqrt(R_TRUE)
dW += rng.normal(0, 0.18, (D, D))
U, S, Vt = np.linalg.svd(dW)                                 # the best rank-r approximation for every r at once
err = [np.linalg.norm(dW - (U[:, :r] * S[:r]) @ Vt[:r]) / np.linalg.norm(dW)
       for r in range(1, MAXR + 1)]                          # relative error at each rank
lim = np.abs(dW).max()

HOLD = 3                                                     # frames per rank, so the eye can keep up
fig, (a_t, a_r, a_e) = plt.subplots(1, 3, figsize=(9.6, 3.2),
                                    gridspec_kw={"width_ratios": [1, 1, 1.25]})
fig.subplots_adjust(wspace=0.35)

def draw(f):
    r = f // HOLD + 1                                        # the rank being shown
    approx = (U[:, :r] * S[:r]) @ Vt[:r]                     # B @ A, in LoRA's notation
    for ax in (a_t, a_r, a_e):
        ax.clear()
    a_t.imshow(dW, cmap="RdBu_r", vmin=-lim, vmax=lim); a_t.set_title("the update, dW", fontsize=11)
    a_r.imshow(approx, cmap="RdBu_r", vmin=-lim, vmax=lim)
    a_r.set_title(f"rank {r}: B @ A", fontsize=11)
    for ax in (a_t, a_r):
        ax.set_xticks([]); ax.set_yticks([])
    a_e.plot(range(1, MAXR + 1), err, color="#C7CDD1", lw=1.6)
    a_e.plot(range(1, r + 1), err[:r], color=UF, lw=2.4)
    a_e.scatter([r], [err[r - 1]], color=ORANGE, zorder=3, s=36)
    a_e.set_xlim(1, MAXR); a_e.set_ylim(0, 1.02)
    a_e.set_xlabel("rank r", fontsize=10); a_e.set_ylabel("relative error", fontsize=10)
    a_e.spines[["top", "right"]].set_visible(False)
    params = 2 * D * r                                       # the parameters LoRA would train at this rank
    a_e.set_title(f"{params:,} trained, {D * D:,} full  ({100 * params / D**2:.0f}%)",
                  loc="right", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=MAXR * HOLD, interval=150)
plt.close(fig)
HTML(ani.to_jshtml(fps=7))''')

# ---------------------------------------------------------------- Week 6
CELLS['week06_self_supervised_learning'] = (10, '''### 1.3b Watch the mask ratio climb

Section 1.3 hid 75% of the patches, which is the figure from the MAE paper and sounds reckless the first time you read it.
The animation sweeps the ratio from nothing to almost everything so you can judge it for yourself.

Watch the top panel, which is what the encoder actually receives. Somewhere around half the signal the shape of each beat
is still obvious from what is left; by 90% it is not. The ratio is chosen to sit just below the point where a person
would also start guessing, because a task that is too easy teaches the encoder to interpolate neighbouring samples and a
task that is impossible teaches it nothing.

The counter under the panel is the other half of the argument. The encoder only ever sees the visible patches, so a high
ratio makes pretraining cheaper per step as well as harder.''', HEAD + '''
FS, SECONDS, PATCH = 125, 8, 1                               # sampling rate, length, patch length in seconds
n = FS * SECONDS
t = np.arange(n) / FS
rng = np.random.default_rng(0)

def ecg(t, bpm=66):
    """A synthetic single-lead ECG: a P wave, a QRS complex and a T wave per beat."""
    beat = 60.0 / bpm                                        # seconds between beats
    phase = (t % beat) / beat                                # position within the current beat, 0 to 1
    g = lambda c, w, a: a * np.exp(-0.5 * ((phase - c) / w) ** 2)   # one Gaussian bump
    return (g(0.18, 0.030, 0.12)                             # P wave
            - g(0.33, 0.012, 0.18)                           # Q
            + g(0.36, 0.011, 1.00)                           # R
            - g(0.40, 0.014, 0.28)                           # S
            + g(0.60, 0.055, 0.28))                          # T wave

x = ecg(t) + rng.normal(0, 0.012, n)                         # a little measurement noise
P = n // (FS * PATCH)                                        # number of one-second patches
patches = x.reshape(P, -1)

RATIOS = np.linspace(0, 0.9, 37)                             # the sweep, 0% to 90%
order = rng.permutation(P)                                   # the order patches get hidden in, fixed once

fig, (vis, full) = plt.subplots(2, 1, figsize=(9.0, 4.0), sharex=True)
fig.subplots_adjust(hspace=0.35)

def draw(f):
    ratio = RATIOS[f]
    k = int(round(ratio * P))                                # how many patches are hidden
    hidden = set(order[:k].tolist())
    vis.clear(); full.clear()

    # ---- top: what the encoder sees
    for p in range(P):
        seg = slice(p * FS * PATCH, (p + 1) * FS * PATCH)
        if p in hidden:
            vis.axvspan(t[seg][0], t[seg][-1], color="#E5E7EB", zorder=0)   # a grey hole
        else:
            vis.plot(t[seg], x[seg], color=UF, lw=1.1)
    vis.set_ylim(-0.5, 1.2); vis.set_ylabel("visible", fontsize=10)
    vis.spines[["top", "right"]].set_visible(False)
    vis.set_title(f"mask ratio {ratio * 100:3.0f}%     encoder sees {P - k} of {P} patches",
                  loc="left", fontsize=11, color="#374151")

    # ---- bottom: the recording the decoder is asked to reconstruct
    full.plot(t, x, color=GREY, lw=1.0, alpha=0.65)
    for p in sorted(hidden):
        seg = slice(p * FS * PATCH, (p + 1) * FS * PATCH)
        full.plot(t[seg], x[seg], color=ORANGE, lw=1.3)      # the parts the loss is computed on
    full.set_ylim(-0.5, 1.2); full.set_xlabel("seconds", fontsize=10)
    full.set_ylabel("target", fontsize=10)
    full.spines[["top", "right"]].set_visible(False)
    full.set_title("orange is where the loss is computed", loc="left", fontsize=10, color=GREY)
    return []

ani = FuncAnimation(fig, draw, frames=len(RATIOS), interval=110)
plt.close(fig)
HTML(ani.to_jshtml(fps=9))''')
