from kit import *
CLEAN, NOIS, PRED, MOT = "#0F766E", GREY, UF, AMB   # structure teal, noise grey, model UF blue, motif amber
FILLS = {CLEAN: "#CCFBF1", UF: "#E0E7FF", GREY: "#F3F4F6", AMB: "#FEF3C7", "#DC2626": "#FEE2E2"}
BAD = "#DC2626"
BET = np.linspace(1e-4, 0.02, 1000)
ABAR = np.cumprod(1 - BET)
def wts(t):
    a = ABAR[max(t, 1) - 1]
    return float(np.sqrt(a)), float(np.sqrt(1 - a))
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def curve(fx, fy, n=16):
    u = np.linspace(0, 1, n)
    return np.stack([fx(u), fy(u)], 1)
SHAPES = [curve(lambda u: 3.0 * (u - 0.5), lambda u: 0.50 * np.sin(u * 2.4 * 2 * np.pi)),
          curve(lambda u: (0.40 + 0.70 * u) * np.cos(u * 1.6 * 2 * np.pi), lambda u: (0.40 + 0.70 * u) * np.sin(u * 1.6 * 2 * np.pi)),
          curve(lambda u: 2.6 * (u - 0.5) + 0.35 * np.sin(u * 8), lambda u: 0.75 * np.cos(u * 1.3 * 2 * np.pi))]
EPS = [np.random.default_rng(s).normal(size=(16, 2)) for s in (40, 74, 11)]
for e in EPS: e *= min(1.0, 1.5 / abs(e).max())
MOTIF = list(range(6, 10))                            # the four residues held fixed in the conditioned run
def noised(x0, t, e, keep=()):
    s, q = wts(t)
    x = s * x0 + q * e
    for k in keep: x[k] = x0[k]                       # conditioning: these coordinates never move
    return x
def chain(pts, color=CLEAN, ds=1.0, r=0.07, sw=3.5, at=(0, 0), keep=()):
    p = [np.array([x * ds + at[0], y * ds + at[1], 0]) for x, y in pts]
    g = VGroup(VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(p))
    for k, q in enumerate(p):
        g.add(Dot(radius=(0.105 if k in keep else r), color=(MOT if k in keep else color), fill_opacity=1).move_to(q))
    return g
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    r = RoundedRectangle(corner_radius=0.12, width=max(w, body.width + 0.8), height=body.height + 0.65, stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
def hbar(label, v, vmax, y, x0=-2.2, span=6.6, color=PRED, suffix=""):
    w = span * v / vmax
    b = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x0 + w / 2, y, 0])
    return VGroup(T(label, 22, INK).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT),
                  b, T(f"{v}{suffix}", 22, WHITE, BOLD).move_to(b))
class C3(Clip):
    TITLE = "Diffusion, part 3: steering the sampler"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. unconditional is not enough
        self.cap("Unconditional sampling makes some protein, not the one you need.", hold=0)
        G = VGroup(*[chain(SHAPES[k], CLEAN, ds=0.85, at=(-4.4 + k * 4.4, 2.0)) for k in range(3)])
        gl = T("unconditional samples: valid structures, but nobody asked for these (illustrative)", 22, GREY).move_to([0, 0.6, 0])
        need = card("What a design project actually asks for",
                    ["hold this functional motif in place and build a scaffold around it",
                     "bind this target protein, at this site, tightly enough to matter"], MOT, 10.6, [0, -0.85, 0], size=22)
        nt = W("Both are questions about one specific structure, so the sampler has to be steered.", 24, INK).move_to([0, -2.35, 0])
        self.play(LaggedStart(*[FadeIn(g) for g in G], lag_ratio=0.3), FadeIn(gl), run_time=1.4)
        self.play(FadeIn(need[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in need[1]], lag_ratio=0.3), run_time=1.4)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.4)
        # 2. conditioning
        self.cap("Conditioning pins part of the structure and lets the rest form around it.", hold=0)
        self.play(FadeOut(VGroup(G, gl, need, nt)), run_time=0.6)
        xs = (-4.4, 0.0, 4.4)
        cs, cl = VGroup(), VGroup()
        for (t, col), x in zip(((800, NOIS), (400, NOIS), (0, CLEAN)), xs):
            cs.add(chain(noised(SHAPES[2], t, EPS[0], keep=MOTIF), col, ds=1.0, at=(x, 1.4), keep=MOTIF))
            cl.add(T(f"t = {t}", 22, INK if t == 0 else GREY).move_to([x, -0.35, 0]))
        ar = VGroup(*[Arrow([xs[k] + 1.6, 1.4, 0], [xs[k + 1] - 1.6, 1.4, 0], buff=0, color=PRED, stroke_width=4, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        key = VGroup(Dot(radius=0.105, color=MOT), T("the motif: fixed coordinates, given to the denoiser at every step", 23, INK)).arrange(RIGHT, buff=0.25).move_to([0, -1.3, 0])
        nt2 = W("The motif never moves. The scaffold is sampled, so you get many different scaffolds for one motif.", 23, GREY).move_to([0, -2.05, 0])
        self.play(FadeIn(cs[0]), FadeIn(cl[0]), run_time=0.7)
        for k in range(2):
            self.play(GrowArrow(ar[k]), FadeIn(cs[k + 1]), FadeIn(cl[k + 1]), run_time=0.8)
        self.play(FadeIn(key), run_time=0.6)
        self.play(FadeIn(nt2), run_time=0.5)
        self.rest(2.4)
        # 3. guidance
        self.cap("Guidance is a different lever, from image diffusion, not used by RFdiffusion.", hold=0)
        self.play(FadeOut(VGroup(cs, cl, ar, key, nt2)), run_time=0.6)
        fm = VGroup(T("prediction  =  uncond  +  w · ( cond − uncond )", 30, INK, BOLD),
                    T("0.2  +  3 · ( 0.5 − 0.2 )  =  1.1   (illustrative numbers)", 26, PRED, BOLD)).arrange(DOWN, buff=0.3).move_to([0, 2.35, 0])
        AY = -0.2
        ax = Line([-4.6, AY, 0], [4.6, AY, 0], color=GREY, stroke_width=3)
        def tick(x, v, col, lab):
            m = VGroup(Line([x, AY - 0.16, 0], [x, AY + 0.16, 0], color=col, stroke_width=4), T(v, 22, col, BOLD).move_to([x, AY + 0.42, 0]), T(lab, 20, GREY).move_to([x, AY - 0.45, 0]))
            return m
        tk = VGroup(tick(-3.4, "0.2", NOIS, "unconditional"), tick(-0.6, "0.5", CLEAN, "conditional"), tick(4.0, "1.1", PRED, "guided, w = 3"))
        pull = Arrow([-0.6, AY + 0.95, 0], [4.0, AY + 0.95, 0], buff=0, color=PRED, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        pl = T("guidance extrapolates past the conditional prediction", 21, PRED).next_to(pull, UP, buff=0.12)
        nt3 = card("Where this is used",
                   ["image diffusion: a larger w follows the prompt harder and cuts diversity",
                    "RFdiffusion does not use classifier-free guidance: it conditions the denoiser directly"], PRED, 11.0, [0, -2.0, 0], size=22)
        self.play(FadeIn(fm[0]), run_time=0.7)
        self.play(FadeIn(fm[1]), run_time=0.6)
        self.play(Create(ax), LaggedStart(*[FadeIn(t) for t in tk], lag_ratio=0.3), run_time=1.4)
        self.play(GrowArrow(pull), FadeIn(pl), run_time=0.7)
        self.play(FadeIn(nt3[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in nt3[1]], lag_ratio=0.3), run_time=1.3)
        self.rest(2.4)
        # 4. motif scaffolding results
        self.cap("On 25 motif-scaffolding benchmarks, RFdiffusion solved 23.", hold=0)
        self.play(FadeOut(VGroup(fm, ax, tk, pull, pl, nt3)), run_time=0.6)
        B = VGroup(hbar("RFdiffusion", 23, 25, 1.75, color=PRED),
                   hbar("RFjoint inpainting", 19, 25, 0.85, color=NOIS),
                   hbar("hallucination", 15, 25, -0.05, color=NOIS))
        sc = T("out of 25 benchmark problems", 20, GREY).move_to([1.8, -0.75, 0])
        nt4 = card("How to read this",
                   ["one set of settings for every problem: no tuning problem by problem",
                    "success here is scored in silico, before anything reaches a lab"], PRED, 11.0, [0, -2.0, 0], size=22)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in B], lag_ratio=0.35), run_time=1.9)
        self.play(FadeIn(sc), run_time=0.4)
        self.play(FadeIn(nt4[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in nt4[1]], lag_ratio=0.3), run_time=1.3)
        self.rest(2.4)
        # 5. binders in the lab
        self.cap("Binders against five targets: 19% worked in the lab.", hold=0)
        self.play(FadeOut(VGroup(B, sc, nt4)), run_time=0.6)
        tg = card("Five targets",
                  ["influenza A H1 hemagglutinin", "IL-7R alpha", "PD-L1", "insulin receptor", "TrkA"], CLEAN, 5.2, [-3.9, 0.85, 0], size=22)
        rs = card("What came back",
                  ["19% experimental success overall",
                   "fewer than 100 designs tested per target",
                   "best flu binder: 28 nM",
                   "cryo-EM map at 2.9 Å, 0.63 Å from the design"], PRED, 6.8, [3.1, 0.85, 0], size=22)
        nt5 = W("19% is a low number and a very good one: these are binders designed from scratch, with no starting template.", 23, INK).move_to([0, -1.85, 0])
        self.play(FadeIn(tg[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in tg[1]], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(rs[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in rs[1]], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(nt5), run_time=0.6)
        self.rest(2.6)
        # 6. the caution
        self.cap("The in silico judge can share the designer's blind spots.", hold=0)
        self.play(FadeOut(VGroup(tg, rs, nt5)), run_time=0.6)
        c1 = card("The screen", ["designs are scored by AlphaFold-family",
                                 "structure predictions, not by experiment",
                                 "designer and judge learn from the same",
                                 "structures, so they can agree and be wrong"], BAD, 6.3, [-3.4, 0.9, 0], size=21)
        c2 = card("The test", ["express the protein and measure it",
                               "19% success, 28 nM, a cryo-EM map",
                               "a predicted structure is a hypothesis,",
                               "a measurement is evidence"], CLEAN, 6.3, [3.4, 0.9, 0], size=21)
        nt6 = VGroup(W("Clip 1: noising is free. Clip 2: the network learns the way back. Clip 3: conditioning is what makes it useful.", 23, INK),
                     T("Watson et al., Nature 2023; Abramson et al., Nature 2024", 20, GREY)).arrange(DOWN, buff=0.22).move_to([0, -2.0, 0])
        self.play(FadeIn(c1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in c1[1]], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(c2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in c2[1]], lag_ratio=0.2), run_time=1.5)
        self.play(FadeIn(nt6), run_time=0.6)
        self.rest(3.2)
