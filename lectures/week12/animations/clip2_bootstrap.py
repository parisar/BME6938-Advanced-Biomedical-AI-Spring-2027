from kit import *
from decimal import Decimal, ROUND_HALF_UP
MA, MB, BOTH, NEITHER, BAD = UF, "#0F766E", "#CBD5E1", "#FCA5A5", "#DC2626"   # model A blue, model B teal
FILLS = {MA: "#E0E7FF", MB: "#CCFBF1", GREY: "#F3F4F6", AMB: "#FEF3C7", BAD: "#FEE2E2"}
N = 200
BOTH_RIGHT, A_ONLY, B_ONLY = 156, 14, 8                       # the agreement table (synthetic, illustrative)
BOTH_WRONG = N - BOTH_RIGHT - A_ONLY - B_ONLY                 # 22
A = np.array([1] * BOTH_RIGHT + [1] * A_ONLY + [0] * B_ONLY + [0] * BOTH_WRONG)
B = np.array([1] * BOTH_RIGHT + [0] * A_ONLY + [1] * B_ONLY + [0] * BOTH_WRONG)
_rng = np.random.default_rng(0)
_idx = _rng.integers(0, N, (10000, N))                        # 10,000 bootstrap resamples, drawn once
bA, bB = A[_idx].mean(1), B[_idx].mean(1)
bD = bA - bB                                                  # the paired difference: the same resampled patients for both
uD = A[_rng.integers(0, N, (10000, N))].mean(1) - B[_rng.integers(0, N, (10000, N))].mean(1)
def pct(v): return tuple(float(x) for x in np.percentile(v, [2.5, 97.5]))
CI_A, CI_B, CI_D, CI_U = pct(bA), pct(bB), pct(bD), pct(uD)
def f2(x, n=2):
    """Round half up, so 0.765 prints as 0.77 rather than 0.76."""
    return str(Decimal(repr(x)).quantize(Decimal("1." + "0" * n), rounding=ROUND_HALF_UP))
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    r = RoundedRectangle(corner_radius=0.12, width=max(w, body.width + 0.8), height=body.height + 0.65,
                         stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
def grid(colors, at, cols=20, step=0.33, r=0.115):
    """200 patients as a grid of dots, one colour per patient."""
    g = VGroup()
    for k, c in enumerate(colors):
        g.add(Dot(radius=r, color=c, fill_opacity=1).move_to([(k % cols) * step, -(k // cols) * step, 0]))
    return g.move_to([at[0], at[1], 0])
def ci(lo, hi, est, xmin, xmax, y, ticks, color, cx=0.0, span=9.0, dec=2, zero=True):
    """A point estimate and its interval on a number line; zero, when inside the range, is drawn in red."""
    X = lambda v: cx + (v - (xmin + xmax) / 2) * span / (xmax - xmin)
    g = VGroup(Line([X(xmin), y, 0], [X(xmax), y, 0], color=GREY, stroke_width=3))
    for v in ticks:
        hot = zero and abs(v) < 1e-9
        g.add(Line([X(v), y - 0.13, 0], [X(v), y + 0.13, 0], color=(BAD if hot else GREY), stroke_width=(4 if hot else 3)),
              T(f2(v, dec), 20, (BAD if hot else GREY), (BOLD if hot else NORMAL)).move_to([X(v), y - 0.42, 0]))
    g.add(Line([X(lo), y + 0.5, 0], [X(hi), y + 0.5, 0], color=color, stroke_width=9),
          Line([X(lo), y + 0.3, 0], [X(lo), y + 0.7, 0], color=color, stroke_width=4),
          Line([X(hi), y + 0.3, 0], [X(hi), y + 0.7, 0], color=color, stroke_width=4),
          Dot(radius=0.13, color=color).move_to([X(est), y + 0.5, 0]))
    if zero and lo < 0 < hi:
        g.add(DashedLine([X(0), y + 0.13, 0], [X(0), y + 0.9, 0], color=BAD, stroke_width=3, dash_length=0.1))
    return g
class C2(Clip):
    TITLE = "How sure are we? The bootstrap"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. the test set
        self.cap("A test set of 200 patients: model A is right on 170, model B on 164.", hold=0)
        gA = grid([MA if a else NEITHER for a in A], (-3.1, 1.5))
        lgA = VGroup(VGroup(Dot(radius=0.115, color=MA), T("model A correct", 20, INK)).arrange(RIGHT, buff=0.18),
                     VGroup(Dot(radius=0.115, color=NEITHER), T("model A wrong", 20, INK)).arrange(RIGHT, buff=0.18)
                     ).arrange(RIGHT, buff=0.9).move_to([-3.1, -0.4, 0])
        sc = card("The numbers", [f"model A: 170 of 200 = 85%", f"model B: 164 of 200 = 82%",
                                  "difference: 3 percentage points"], GREY, 5.4, [3.9, 1.5, 0], size=22)
        nt = W("Synthetic test set, illustrative. The question is how much of that 3 points is just which 200 patients we happened to test.", 23, INK).move_to([0, -1.8, 0])
        self.play(LaggedStart(*[FadeIn(d) for d in gA], lag_ratio=0.004), run_time=1.6)
        self.play(FadeIn(lgA), run_time=0.5)
        self.play(FadeIn(sc[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in sc[1]], lag_ratio=0.25), run_time=1.3)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(2.4)
        # 2. resampling
        self.cap("Draw 200 patients with replacement, recompute, and repeat 10,000 times.", hold=0)
        self.play(FadeOut(VGroup(gA, lgA, sc, nt)), run_time=0.6)
        ids = ["p041", "p007", "p007", "p153", "p089", "p198", "p007", "p112"]
        chips = VGroup(*[box(s, 1.0, 0.5, FILLS[AMB] if s == "p007" else FILLS[GREY], 19,
                             AMB if s == "p007" else GREY) for s in ids]).arrange(RIGHT, buff=0.14).move_to([-3.2, 2.2, 0])
        dots = T("...", 24, GREY).next_to(chips, RIGHT, buff=0.18)
        cl = T("one resample: 200 draws, with replacement, so p007 can appear three times", 21, GREY).next_to(chips, DOWN, buff=0.25)
        acc = T("accuracy of model A on this resample: 0.84", 24, MA, BOLD).next_to(cl, DOWN, buff=0.35)
        bars = VGroup()
        hist, edges = np.histogram(bA, bins=26, range=(0.74, 0.96))
        hmax = hist.max()
        for k, h in enumerate(hist):
            bars.add(Rectangle(width=0.30, height=max(0.02, 1.9 * h / hmax), stroke_width=0, fill_color=MA, fill_opacity=0.85)
                     .move_to([-4.0 + k * 0.32, -2.05 + 1.9 * h / hmax / 2, 0]))
        hl = T("10,000 resampled accuracies for model A", 21, GREY).move_to([0, -2.45, 0])
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in chips], lag_ratio=0.12), FadeIn(dots), run_time=1.3)
        self.play(FadeIn(cl), run_time=0.5)
        self.play(FadeIn(acc), run_time=0.5)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), FadeIn(hl), run_time=1.8)
        self.rest(2.2)
        # 3. two intervals that overlap
        self.cap("The two 95% intervals overlap, and that is not a test of the difference.", hold=0)
        self.play(FadeOut(VGroup(chips, dots, cl, acc, bars, hl)), run_time=0.6)
        tks = (0.75, 0.80, 0.85, 0.90, 0.95)
        lA = ci(CI_A[0], CI_A[1], 0.85, 0.74, 0.96, 1.6, tks, MA, cx=1.8, span=8.6, zero=False)
        lB = ci(CI_B[0], CI_B[1], 0.82, 0.74, 0.96, 0.0, tks, MB, cx=1.8, span=8.6, zero=False)
        nA = VGroup(T("model A", 25, MA, BOLD), T("0.85", 25, INK, BOLD),
                    T(f"95% CI {f2(CI_A[0])} to {f2(CI_A[1])}", 21, GREY)).arrange(DOWN, buff=0.14).move_to([-5.3, 2.1, 0])
        nB = VGroup(T("model B", 25, MB, BOLD), T("0.82", 25, INK, BOLD),
                    T(f"95% CI {f2(CI_B[0])} to {f2(CI_B[1])}", 21, GREY)).arrange(DOWN, buff=0.14).move_to([-5.3, 0.5, 0])
        warn = card("A common mistake",
                    ["overlapping intervals do not mean the difference could be zero",
                     "each interval answers a separate question, about one model on its own",
                     "to ask about the difference, build an interval for the difference"], BAD, 11.0, [0, -2.0, 0], size=22)
        self.play(FadeIn(nA), FadeIn(lA), run_time=1.0)
        self.play(FadeIn(nB), FadeIn(lB), run_time=1.0)
        self.play(FadeIn(warn[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in warn[1]], lag_ratio=0.25), run_time=1.5)
        self.rest(2.6)
        # 4. the same patients
        self.cap("The two models were graded on the same patients, so compare them that way.", hold=0)
        self.play(FadeOut(VGroup(nA, nB, lA, lB, warn)), run_time=0.6)
        cats = [BOTH] * BOTH_RIGHT + [MA] * A_ONLY + [MB] * B_ONLY + [NEITHER] * BOTH_WRONG
        g2 = grid(cats, (-3.1, 1.4))
        rows = [("both right", BOTH_RIGHT, BOTH), ("only A right", A_ONLY, MA),
                ("only B right", B_ONLY, MB), ("both wrong", BOTH_WRONG, NEITHER)]
        K = VGroup()
        for name, n, col in rows:
            K.add(VGroup(Dot(radius=0.13, color=col), T(f"{name}", 22, INK), T(f"{n}", 22, INK, BOLD)).arrange(RIGHT, buff=0.25))
        K.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, 1.4, 0])
        nt4 = VGroup(T("A is right where B is wrong 14 times; B is right where A is wrong 8 times.", 23, INK),
                     T("14 − 8 = 6 patients out of 200, which is the 3-point difference.", 23, AMB, BOLD)).arrange(DOWN, buff=0.22).move_to([0, -1.85, 0])
        self.play(LaggedStart(*[FadeIn(d) for d in g2], lag_ratio=0.004), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.1) for k in K], lag_ratio=0.25), run_time=1.3)
        self.play(FadeIn(nt4), run_time=0.7)
        self.rest(2.4)
        # 5. the paired interval
        self.cap("The paired difference is 0.03, with an interval that includes 0.", hold=0)
        self.play(FadeOut(VGroup(g2, K, nt4)), run_time=0.6)
        tk5 = (-0.06, -0.03, 0.0, 0.03, 0.06, 0.09)
        l5 = ci(CI_D[0], CI_D[1], 0.03, -0.07, 0.11, 0.9, tk5, AMB, cx=0.0, span=10.0)
        n5 = VGroup(T("paired bootstrap of the difference", 26, INK, BOLD),
                    T(f"0.03, 95% CI {f2(CI_D[0], 3)} to {f2(CI_D[1], 3)}", 26, AMB, BOLD)).arrange(DOWN, buff=0.22).move_to([0, 2.3, 0])
        nt5 = card("What this does and does not say",
                   ["the interval includes 0, so these data do not show that A is better",
                    "it does not show the two models are equal either",
                    "200 patients is simply too few to resolve 3 points"], GREY, 11.0, [0, -1.75, 0], size=22)
        self.play(FadeIn(n5), run_time=0.8)
        self.play(FadeIn(l5), run_time=1.0)
        self.play(FadeIn(nt5[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in nt5[1]], lag_ratio=0.25), run_time=1.5)
        self.rest(2.6)
        # 6. what pairing buys
        self.cap("Pairing matters: ignoring it makes the interval nearly twice as wide.", hold=0)
        self.play(FadeOut(VGroup(n5, l5, nt5)), run_time=0.6)
        tk6 = (-0.08, -0.04, 0.0, 0.04, 0.08, 0.12)
        p6 = ci(CI_D[0], CI_D[1], 0.03, -0.09, 0.13, 1.5, tk6, AMB, cx=0.6, span=9.6)
        u6 = ci(CI_U[0], CI_U[1], 0.03, -0.09, 0.13, -0.1, tk6, GREY, cx=0.6, span=9.6)
        lp = VGroup(T("same patients", 23, AMB, BOLD), T(f"{f2(CI_D[0], 3)} to {f2(CI_D[1], 3)}", 22, INK)).arrange(DOWN, buff=0.12).move_to([-5.4, 2.0, 0])
        lu = VGroup(T("ignoring the pairing", 23, GREY, BOLD), T(f"{f2(CI_U[0], 3)} to {f2(CI_U[1], 3)}", 22, INK)).arrange(DOWN, buff=0.12).move_to([-5.4, 0.4, 0])
        out = VGroup(T("Report intervals, not point estimates.", 25, INK, BOLD),
                     T("Compare models on the same patients.", 25, INK, BOLD),
                     T("An interval that includes 0 is a real result: say so, and say how many patients it would take.", 22, GREY)
                     ).arrange(DOWN, buff=0.25).move_to([0, -2.1, 0])
        self.play(FadeIn(lp), FadeIn(p6), run_time=1.0)
        self.play(FadeIn(lu), FadeIn(u6), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in out], lag_ratio=0.3), run_time=1.6)
        self.rest(3.2)
