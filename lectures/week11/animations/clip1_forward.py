from kit import *
CLEAN, NOIS, PRED = "#0F766E", GREY, UF          # clean structure teal, noise grey, model prediction UF blue
FILLS = {CLEAN: "#CCFBF1", UF: "#E0E7FF", GREY: "#F3F4F6", AMB: "#FEF3C7"}
DS = 1.3                                          # display units per data unit
BET = np.linspace(1e-4, 0.02, 1000)               # standard DDPM schedule: beta from 0.0001 to 0.02 over 1,000 steps
ABAR = np.cumprod(1 - BET)                        # cumulative product of (1 - beta)
def wts(t):
    """Signal and noise weights after t forward steps: sqrt(abar_t) and sqrt(1 - abar_t)."""
    a = ABAR[t - 1]
    return float(np.sqrt(a)), float(np.sqrt(1 - a))
def helix(n=16, w=3.2, amp=0.52, turns=2.4):
    """A short alpha helix seen from the side: C-alpha positions along a sine wave (illustrative)."""
    x = np.linspace(-w / 2, w / 2, n)
    return np.stack([x, amp * np.sin(np.linspace(0, turns * 2 * np.pi, n))], 1)
X0 = helix()
EPS = np.random.default_rng(40).normal(size=X0.shape)   # one fixed noise draw, reused at every t (bounded, so the cloud stays on screen)
def noised(t):
    if t == 0: return X0
    s, q = wts(t)
    return s * X0 + q * EPS
def chain(pts, color=CLEAN, r=0.085, sw=4, at=(0, 0)):
    """A backbone drawn as C-alpha dots joined by bonds."""
    p = [np.array([x * DS + at[0], y * DS + at[1], 0]) for x, y in pts]
    g = VGroup(VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(p))
    for q in p: g.add(Dot(radius=r, color=color, fill_opacity=1))
    for d, q in zip(g[1:], p): d.move_to(q)
    return g
class C1(Clip):
    TITLE = "Diffusion, part 1: adding noise"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        AT = (-3.45, 0.35)
        # 1. a real structure, and the plan
        self.cap("Diffusion models learn to generate by learning to undo noise.", hold=0)
        c0 = chain(X0, at=AT)
        l0 = VGroup(T("x₀", 30, CLEAN, BOLD), T("a real backbone", 22, INK), T("16 C-alpha points (illustrative)", 20, GREY)).arrange(DOWN, buff=0.14).move_to([-3.45, -1.75, 0])
        plan = VGroup(T("Training has two directions", 26, INK, BOLD),
                      T("forward: add noise, step by step", 24, NOIS),
                      T("reverse: the network learns to undo it", 24, PRED)).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.3, 0.9, 0])
        self.play(Create(c0[0], run_time=1.0), LaggedStart(*[GrowFromCenter(d) for d in c0[1:]], lag_ratio=0.08, run_time=1.2))
        self.play(FadeIn(l0), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.12) for p in plan], lag_ratio=0.3), run_time=1.4)
        self.rest(2.2)
        # 2. one forward step
        self.cap("One forward step adds a little Gaussian noise to every point.", hold=0)
        self.play(FadeOut(plan), FadeOut(l0), run_time=0.5)
        c1 = chain(noised(40), at=AT)
        arrows = VGroup(*[Arrow(c0[k + 1].get_center(), c1[k + 1].get_center(), buff=0, color=NOIS, stroke_width=2.5, max_tip_length_to_length_ratio=0.5) for k in range(16) if np.linalg.norm(c1[k + 1].get_center() - c0[k + 1].get_center()) > 0.10])
        nt2 = VGroup(T("each point drifts by a random amount", 24, INK),
                     T("the helix is still obvious", 24, CLEAN)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, 0.9, 0])
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.06), run_time=1.2)
        self.play(Transform(c0, c1), FadeOut(arrows), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.12) for p in nt2], lag_ratio=0.3), run_time=1.0)
        self.rest(2.2)
        # 3. the closed form
        self.cap("After t steps the result is one weighted mix of structure and noise.", hold=0)
        self.play(FadeOut(nt2), FadeOut(c0), run_time=0.5)
        fm = VGroup(T("x_t  =", 32, INK, BOLD), T("√(signal_t) · x₀", 32, CLEAN, BOLD),
                    T("+", 32, INK, BOLD), T("√(1 − signal_t) · noise", 32, NOIS, BOLD)).arrange(RIGHT, buff=0.28).move_to([0, 1.9, 0])
        k1 = VGroup(T("signal_t", 24, CLEAN, BOLD), T("how much of the real structure is left after t steps", 24, INK)).arrange(RIGHT, buff=0.3)
        k2 = VGroup(T("noise", 24, NOIS, BOLD), T("one draw from a standard Gaussian, the same size as x₀", 24, INK)).arrange(RIGHT, buff=0.3)
        k3 = T("the two weights always trade off: as one falls, the other rises", 24, GREY)
        K = VGroup(k1, k2, k3).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.4, 0])
        nt3 = T("no need to take t steps one at a time: any t is one line of arithmetic", 24, PRED).move_to([0, -2.1, 0])
        self.play(LaggedStart(*[FadeIn(f) for f in fm], lag_ratio=0.3), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(k, shift=RIGHT * 0.12) for k in K], lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(nt3), run_time=0.5)
        self.rest(2.4)
        # 4. the schedule
        self.cap("The schedule sets those weights: at t = 500 the structure is nearly gone.", hold=0)
        self.play(FadeOut(VGroup(fm, K, nt3)), run_time=0.5)
        hd = VGroup(T("t", 22, GREY, BOLD), T("signal", 22, CLEAN, BOLD), T("noise", 22, NOIS, BOLD))
        for m, x in zip(hd, (1.7, 3.1, 4.6)): m.move_to([x, 2.35, 0])
        TS = (100, 250, 500, 999)
        rows = VGroup()
        for i, t in enumerate(TS):
            s, q = wts(t)
            r = VGroup(T(f"{t}", 22, INK), T(f"{s:.3f}".rstrip("0") if t == 999 else f"{s:.2f}", 22, CLEAN), T(f"{q:.2f}", 22, NOIS))
            for m, x in zip(r, (1.7, 3.1, 4.6)): m.move_to([x, 1.8 - i * 0.55, 0])
            rows.add(r)
        hl = SurroundingRectangle(rows[0], color=AMB, buff=0.14, stroke_width=3, corner_radius=0.08)
        sch = T("beta from 0.0001 to 0.02 over 1,000 steps", 20, GREY).move_to([3.15, -0.75, 0])
        tl = T("t = 100", 26, INK, BOLD).move_to([-5.9, 2.5, 0])
        cur = chain(noised(TS[0]), at=AT)
        self.play(FadeIn(hd), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.25), FadeIn(sch), run_time=1.5)
        self.play(FadeIn(cur), FadeIn(tl), Create(hl), run_time=0.8)
        for i, t in enumerate(TS[1:3], start=1):
            self.play(Transform(cur, chain(noised(t), at=AT)),
                      Transform(tl, T(f"t = {t}", 26, INK, BOLD).move_to([-5.9, 2.5, 0])),
                      Transform(hl, SurroundingRectangle(rows[i], color=AMB, buff=0.14, stroke_width=3, corner_radius=0.08)), run_time=1.3)
            self.wait(0.9)
        self.rest(1.8)
        # 5. pure noise
        self.cap("By the last step nothing of the original structure is left.", hold=0)
        self.play(Transform(cur, chain(noised(999), color=NOIS, at=AT)),
                  Transform(tl, T("t = 999", 26, NOIS, BOLD).move_to([-5.9, 2.5, 0])),
                  Transform(hl, SurroundingRectangle(rows[3], color=AMB, buff=0.14, stroke_width=3, corner_radius=0.08)), run_time=1.6)
        nt5 = VGroup(T("a Gaussian cloud", 24, NOIS, BOLD),
                     T("every protein ends in the same place", 24, INK),
                     T("so sampling can start from noise alone", 24, PRED)).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.9, -1.75, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.12) for p in nt5], lag_ratio=0.3), run_time=1.3)
        self.rest(2.4)
        # 6. the asymmetry
        self.cap("Noising needs no learning, so training pairs are free.", hold=0)
        self.play(FadeOut(VGroup(hd, rows, hl, sch, tl, cur, nt5)), run_time=0.6)
        left = VGroup(T("Forward", 28, NOIS, BOLD),
                      T("a random number generator", 24, INK),
                      T("no parameters, nothing to learn", 24, INK),
                      T("gives (x_t, t, noise) for any t", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        right = VGroup(T("Reverse", 28, PRED, BOLD),
                       T("a trained network", 24, INK),
                       T("sees x_t and t, predicts the noise", 24, INK),
                       T("clip 2", 24, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        pane = lambda fill, stroke, x: RoundedRectangle(corner_radius=0.12, width=5.9, height=2.6, stroke_color=stroke, stroke_width=2, fill_color=fill, fill_opacity=1).move_to([x, 0.55, 0])
        L, R = pane(FILLS[GREY], NOIS, -3.3), pane(FILLS[UF], PRED, 3.3)
        left.move_to(L); right.move_to(R)
        nt6 = T("one real structure gives a thousand training examples, one per step", 24, INK).move_to([0, -1.6, 0])
        self.play(FadeIn(L), FadeIn(left), run_time=0.9)
        self.play(FadeIn(R), FadeIn(right), run_time=0.9)
        self.play(FadeIn(nt6), run_time=0.5)
        self.rest(3.0)
