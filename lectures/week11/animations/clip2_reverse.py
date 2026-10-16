from kit import *
CLEAN, NOIS, PRED = "#0F766E", GREY, UF          # clean structure teal, noise grey, model prediction UF blue
FILLS = {CLEAN: "#CCFBF1", UF: "#E0E7FF", GREY: "#F3F4F6", AMB: "#FEF3C7"}
BET = np.linspace(1e-4, 0.02, 1000)
ABAR = np.cumprod(1 - BET)
def wts(t):
    a = ABAR[max(t, 1) - 1]
    return float(np.sqrt(a)), float(np.sqrt(1 - a))
def curve(fx, fy, n=16):
    u = np.linspace(0, 1, n)
    return np.stack([fx(u), fy(u)], 1)
def hairpin(n=16):
    """Two antiparallel strands joined by a turn (illustrative)."""
    u = np.linspace(0, 1, n); x, y = np.empty(n), np.empty(n)
    for k, v in enumerate(u):
        if v < 0.44:   x[k], y[k] = -1.5 + (v / 0.44) * 2.7, 0.5
        elif v < 0.56: a = (v - 0.44) / 0.12 * np.pi; x[k], y[k] = 1.2 + 0.5 * np.sin(a), 0.5 * np.cos(a)
        else:          x[k], y[k] = 1.2 - ((v - 0.56) / 0.44) * 2.7, -0.5
    return np.stack([x, y + 0.09 * np.sin(np.arange(n) * 2.1)], 1)
SHAPES = [curve(lambda u: 3.2 * (u - 0.5), lambda u: 0.52 * np.sin(u * 2.4 * 2 * np.pi)),
          hairpin(),
          curve(lambda u: (0.42 + 0.72 * u) * np.cos(u * 1.6 * 2 * np.pi), lambda u: (0.42 + 0.72 * u) * np.sin(u * 1.6 * 2 * np.pi))]
EPS = [np.random.default_rng(s).normal(size=(16, 2)) for s in (40, 74, 11)]
for e in EPS: e *= min(1.0, 1.5 / abs(e).max())   # keep every cloud inside its panel
def noised(x0, t, e):
    s, q = wts(t)
    return s * x0 + q * e
def chain(pts, color=CLEAN, ds=1.0, r=0.07, sw=3.5, at=(0, 0)):
    p = [np.array([x * ds + at[0], y * ds + at[1], 0]) for x, y in pts]
    g = VGroup(VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(p))
    for q in p: g.add(Dot(radius=r, color=color, fill_opacity=1).move_to(q))
    return g
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    """A single line that is scaled down if it would run off the frame."""
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    r = RoundedRectangle(corner_radius=0.12, width=max(w, body.width + 0.8), height=body.height + 0.65, stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
class C2(Clip):
    TITLE = "Diffusion, part 2: learning the way back"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. what the network does
        self.cap("The network sees a noisy structure and the step number, and predicts the noise.", hold=0)
        xt = chain(noised(SHAPES[1], 400, EPS[0]), NOIS, ds=1.15, at=(-4.7, 1.1))
        xl = VGroup(T("x_t", 26, NOIS, BOLD), T("t = 400", 22, GREY)).arrange(DOWN, buff=0.12).move_to([-4.7, -0.8, 0])
        net = RoundedRectangle(corner_radius=0.12, width=2.7, height=1.5, stroke_color=PRED, stroke_width=2.5, fill_color=FILLS[UF], fill_opacity=1).move_to([-0.7, 1.1, 0])
        nl = VGroup(T("denoiser", 26, PRED, BOLD), T("one neural network", 20, GREY)).arrange(DOWN, buff=0.1).move_to(net)
        x0 = chain(SHAPES[1], CLEAN, ds=1.15, at=(3.9, 1.1))
        ol = VGroup(T("x̂₀", 26, CLEAN, BOLD), T("the predicted clean structure", 22, INK)).arrange(DOWN, buff=0.12).move_to([3.9, -0.8, 0])
        a1 = Arrow([-3.0, 1.1, 0], [-2.1, 1.1, 0], buff=0, color=GREY, stroke_width=4)
        a2 = Arrow([0.7, 1.1, 0], [2.0, 1.1, 0], buff=0, color=GREY, stroke_width=4)
        eq = VGroup(T("Predicting the noise and predicting x₀ are the same job:", 22, INK),
                    T("x̂₀ = ( x_t − √(1 − signal_t) · predicted noise ) / √(signal_t)", 22, PRED, BOLD)).arrange(DOWN, buff=0.2).move_to([0, -2.1, 0])
        self.play(FadeIn(xt), FadeIn(xl), run_time=0.8)
        self.play(GrowArrow(a1), FadeIn(net), FadeIn(nl), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(x0), FadeIn(ol), run_time=0.8)
        self.play(FadeIn(eq), run_time=0.5)
        self.rest(2.4)
        # 2. one reverse step
        self.cap("One reverse step moves a little toward that prediction, then adds fresh noise.", hold=0)
        self.play(FadeOut(VGroup(xt, xl, net, nl, x0, ol, a1, a2, eq)), run_time=0.6)
        ds, ys = 0.68, 1.3
        c = [chain(noised(SHAPES[1], t, EPS[0]), col, ds=ds, at=(x, ys)) for t, col, x in
             ((400, NOIS, -5.0), (330, NOIS, 0.0), (360, NOIS, 5.0))]
        lb = VGroup(*[T(s, 24, INK, BOLD).move_to([x, -0.25, 0]) for s, x in (("x_t", -5.0), ("a step toward x̂₀", 0.0), ("x_(t−1)", 5.0))])
        s1 = Arrow([-3.5, ys, 0], [-1.4, ys, 0], buff=0, color=PRED, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        s2 = Arrow([1.4, ys, 0], [3.5, ys, 0], buff=0, color=NOIS, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        t1 = T("move toward x̂₀", 21, PRED).next_to(s1, UP, buff=0.18)
        t2 = T("add fresh noise", 21, NOIS).next_to(s2, UP, buff=0.18)
        nt = VGroup(T("Repeat from t = 1000 down to 1.", 24, INK, BOLD),
                    W("The fresh noise keeps the samples diverse: without it, every run from the same start is identical.", 22, GREY)).arrange(DOWN, buff=0.2).move_to([0, -1.9, 0])
        self.play(FadeIn(c[0]), FadeIn(lb[0]), run_time=0.6)
        self.play(GrowArrow(s1), FadeIn(t1), FadeIn(c[1]), FadeIn(lb[1]), run_time=0.9)
        self.play(GrowArrow(s2), FadeIn(t2), FadeIn(c[2]), FadeIn(lb[2]), run_time=0.9)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(2.4)
        # 3. the whole trajectory
        self.cap("Run the step a thousand times and noise becomes a plausible backbone.", hold=0)
        self.play(FadeOut(VGroup(*c, lb, s1, s2, t1, t2, nt)), run_time=0.6)
        TS = [(999, NOIS), (700, NOIS), (400, NOIS), (150, CLEAN), (0, CLEAN)]
        xs = np.linspace(-5.3, 5.3, 5)
        tr, tl = VGroup(), VGroup()
        for (t, col), x in zip(TS, xs):
            tr.add(chain(noised(SHAPES[1], t, EPS[0]), col, ds=0.60, at=(x, 1.2)))
            tl.add(T(f"t = {t}", 22, INK if t == 0 else GREY, BOLD if t == 0 else NORMAL).move_to([x, -0.55, 0]))
        ar = VGroup(*[Arrow([xs[k] + 0.95, 1.2, 0], [xs[k + 1] - 0.95, 1.2, 0], buff=0, color=PRED, stroke_width=4, max_tip_length_to_length_ratio=0.35) for k in range(4)])
        nt3 = VGroup(T("start: pure noise", 24, NOIS), T("end: a backbone that folds (illustrative)", 24, CLEAN)).arrange(RIGHT, buff=1.4).move_to([0, -1.7, 0])
        self.play(FadeIn(tr[0]), FadeIn(tl[0]), run_time=0.6)
        for k in range(4):
            self.play(GrowArrow(ar[k]), FadeIn(tr[k + 1]), FadeIn(tl[k + 1]), run_time=0.6)
        self.play(FadeIn(nt3), run_time=0.5)
        self.rest(2.4)
        # 4. generation, not retrieval
        self.cap("New starting noise gives a new structure every time: generation, not retrieval.", hold=0)
        self.play(FadeOut(VGroup(tr, tl, ar, nt3)), run_time=0.6)
        G, GL = VGroup(), VGroup()
        for k, x in enumerate((-4.3, 0.0, 4.3)):
            G.add(chain(SHAPES[k], CLEAN, ds=1.1, at=(x, 1.3)))
            GL.add(VGroup(T(f"sample {k + 1}", 24, INK, BOLD), T(f"noise draw {k + 1}", 20, GREY)).arrange(DOWN, buff=0.1).move_to([x, -0.6, 0]))
        nt4 = VGroup(T("All three are illustrative drawings, not real designs.", 24, GREY),
                     W("None of them has to appear in the training set: the model samples, it does not look up.", 24, INK)).arrange(DOWN, buff=0.22).move_to([0, -1.95, 0])
        self.play(LaggedStart(*[AnimationGroup(FadeIn(g), FadeIn(l)) for g, l in zip(G, GL)], lag_ratio=0.35), run_time=1.8)
        self.play(FadeIn(nt4), run_time=0.6)
        self.rest(2.6)
        # 5. RFdiffusion
        self.cap("RFdiffusion builds its denoiser out of a structure predictor.", hold=0)
        self.play(FadeOut(VGroup(G, GL, nt4)), run_time=0.6)
        rf = card("RFdiffusion (Watson et al., Nature 2023)",
                  ["fine-tuned from pretrained RoseTTAFold weights, not trained from scratch",
                   "works on residue frames: a C-alpha position plus an N-C-alpha-C orientation",
                   "predicts x̂₀ at every step and feeds it back as a template (self-conditioning)",
                   "a trajectory is typically 200 steps, not 1,000"], PRED, 11.0, [0, 1.35, 0], size=22)
        nz = card("One difference from the textbook step",
                  ["for motif scaffolding, adding no fresh noise on the way back worked better",
                   "in 17 of the 23 solved problems: less diversity, more structures that fold"], AMB, 11.0, [0, -1.55, 0], size=22)
        self.play(FadeIn(rf[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in rf[1]], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(nz[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in nz[1]], lag_ratio=0.3), run_time=1.3)
        self.rest(2.8)
        # 6. backbone to sequence
        self.cap("A backbone is a shape, not a protein: ProteinMPNN writes the sequence.", hold=0)
        self.play(FadeOut(VGroup(rf, nz)), run_time=0.6)
        bb = chain(SHAPES[2], CLEAN, ds=1.1, at=(-5.0, 1.2))
        bl = VGroup(T("backbone", 24, CLEAN, BOLD), T("coordinates only", 20, GREY)).arrange(DOWN, buff=0.1).move_to([-5.0, -0.5, 0])
        mp = RoundedRectangle(corner_radius=0.12, width=2.6, height=1.3, stroke_color=PRED, stroke_width=2.5, fill_color=FILLS[UF], fill_opacity=1).move_to([-1.0, 1.2, 0])
        ml = T("ProteinMPNN", 24, PRED, BOLD).move_to(mp)
        seqs = ["M K T A Y I A K Q R Q I S F V", "M R E L V I A K E R Q L T F L A", "M K Q A Y L A R E R Q V S F I N", "M T E L V I A K Q R H I S Y V D"]
        SQ = VGroup(*[T(s, 21, INK) for s in seqs]).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([4.0, 1.25, 0])
        sl = T("about 8 sequences per backbone", 22, GREY).move_to([4.0, -0.4, 0])
        a1 = Arrow([-3.7, 1.2, 0], [-2.4, 1.2, 0], buff=0, color=GREY, stroke_width=4)
        a2 = Arrow([0.4, 1.2, 0], [1.6, 1.2, 0], buff=0, color=GREY, stroke_width=4)
        nt6 = W("These sequences are what you can order, express, and test in a lab (invented here).", 24, INK).move_to([0, -1.9, 0])
        self.play(FadeIn(bb), FadeIn(bl), run_time=0.7)
        self.play(GrowArrow(a1), FadeIn(mp), FadeIn(ml), run_time=0.7)
        self.play(GrowArrow(a2), LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in SQ], lag_ratio=0.2), FadeIn(sl), run_time=1.2)
        self.play(FadeIn(nt6), run_time=0.5)
        self.rest(2.6)
        # 7. AlphaFold 3
        self.cap("AlphaFold 3 has a diffusion module too, straight on the atoms.", hold=0)
        self.play(FadeOut(VGroup(bb, bl, mp, ml, SQ, sl, a1, a2, nt6)), run_time=0.6)
        af2 = card("AlphaFold 2", ["a structure module built on",
                                   "amino-acid frames and",
                                   "side-chain torsion angles",
                                   "proteins"], GREY, 5.2, [-4.0, 1.1, 0], size=22)
        af3 = card("AlphaFold 3", ["a diffusion module that predicts",
                                   "raw atom coordinates directly,",
                                   "with no frames and no torsions",
                                   "proteins, nucleic acids, ligands, ions"], PRED, 6.4, [3.4, 1.1, 0], size=22)
        ar7 = Arrow(af2.get_right(), af3.get_left(), buff=0.12, color=AMB, stroke_width=7, max_tip_length_to_length_ratio=0.35)
        nt7 = VGroup(W("Dropping the protein-specific machinery is what lets one model cover every kind of molecule.", 23, INK),
                     T("Abramson et al., Nature 2024", 20, GREY)).arrange(DOWN, buff=0.2).move_to([0, -1.9, 0])
        self.play(FadeIn(af2[0]), FadeIn(af2[1]), run_time=0.8)
        self.play(GrowArrow(ar7), run_time=0.4)
        self.play(FadeIn(af3[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in af3[1]], lag_ratio=0.2), run_time=1.3)
        self.play(FadeIn(nt7), run_time=0.6)
        self.rest(3.0)
