from kit import *
NEG = "#9CA3AF"                                   # negatives (other ECGs in the batch)
RHY = [("normal sinus rhythm", "#0F766E"), ("atrial fibrillation", PC), ("other arrhythmia", "#DB2777")]
def dot(p, color, lab=None):
    d = Dot(RIGHT * p[0] + UP * p[1], radius=0.13, color=color).set_z_index(3)
    return VGroup(d, T(lab, 20, color, BOLD).next_to(d, UR, buff=0.04)) if lab else d
class C2(Clip):
    TITLE = "Contrastive learning: two views, one embedding"
    def construct(self):
        fa = ecg_fn(4, hr=75, seed=11)
        A = wave(fa, 0.2, 3.2, 4.2, 0.85).shift(LEFT * 6.4 + UP * 0.1)
        Al = T("ECG A", 24, INK, BOLD).next_to(A, UP, buff=0.4).align_to(A, LEFT)
        self.play(FadeIn(Al), Create(A, rate_func=linear), run_time=1.6)
        f1 = lambda t: fa(t) + 0.05 * np.sin(2 * np.pi * 37 * t) + 0.04 * np.sin(2 * np.pi * 53 * t + 1)
        f2 = lambda t: 0.65 * fa(t) + 0.22 * np.sin(2 * np.pi * 0.35 * t + 0.5)
        V1 = wave(f1, 0.9, 2.7, 4.2, 0.85, color=OC).shift(RIGHT * 1.6 + UP * 1.6)
        V2 = wave(f2, 0.2, 3.2, 4.2, 0.85, color=OC).shift(RIGHT * 1.6 + DOWN * 1.5)
        L1 = T("view 1", 24, OC, BOLD).next_to(V1, UP, buff=0.25).align_to(V1, LEFT)
        L2 = T("view 2", 24, OC, BOLD).next_to(V2, UP, buff=0.25).align_to(V2, LEFT)
        r1 = Arrow(A.get_right() + UP * 0.3, V1.get_left() + DOWN * 0.1, buff=0.25, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.08)
        r2 = Arrow(A.get_right() + UP * 0.3, V2.get_left() + UP * 0.3, buff=0.25, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.08)
        self.play(GrowArrow(r1), GrowArrow(r2), run_time=0.6)
        self.play(Create(V1), Create(V2), FadeIn(L1), FadeIn(L2), run_time=1.2)
        self.cap("Make two augmented views of the same ECG.", hold=2.4)
        g1 = T("crop + noise", 22, GREY).move_to(r1.point_from_proportion(0.5) + UP * 0.45 + LEFT * 0.4)
        g2 = T("scaling + baseline wander", 22, GREY).move_to(RIGHT * -0.9 + DOWN * 1.15)
        self.play(FadeIn(g1), FadeIn(g2), run_time=0.6)
        self.cap("Augmentations change the recording, not the diagnosis.", hold=3.0)
        # shared encoder and embedding space
        self.play(*[FadeOut(m) for m in (A, Al, r1, r2, g1, g2, L1, L2)], run_time=0.5)
        ys = [2.0, 0.95, -0.15, -1.2, -2.25]; sx = -4.2
        self.play(V1.animate.scale(2.8 / 4.2).move_to(RIGHT * sx + UP * ys[0]), V2.animate.scale(2.8 / 4.2).move_to(RIGHT * sx + UP * ys[1]), run_time=0.8)
        others = [ecg_fn(4, hr=58, seed=21), ecg_fn(4, af=True, seed=22), ecg_fn(4, hr=96, seed=23)]
        S = [wave(fo, 0.2, 3.2, 2.8, 0.55, color=NEG).move_to(RIGHT * sx + UP * y) for fo, y in zip(others, ys[2:])]
        names = ["A1", "A2", "B", "C", "D"]
        SL = VGroup(*[T(n, 22, OC if i < 2 else GREY, BOLD).move_to(RIGHT * -6.3 + UP * y) for i, (n, y) in enumerate(zip(names, ys))])
        enc = box("Encoder", 1.6, 4.6, "#E2E8F0", size=26, stroke=EC).move_to(LEFT * 1.6)
        shl = T("shared weights", 20, GREY).next_to(enc, DOWN, buff=0.15)
        ia = [Arrow(RIGHT * (sx + 1.5) + UP * y, RIGHT * (enc.get_left()[0]) + UP * y, buff=0.05, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.5) for y in ys]
        pl = Rectangle(width=5.0, height=4.8, stroke_color=GREY, stroke_width=2).move_to(RIGHT * 3.9 + UP * 0.05)
        pll = T("embedding space", 20, GREY).next_to(pl, UP, buff=0.12)
        oa = Arrow(enc.get_right(), pl.get_left(), buff=0.1, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.2)
        P1, P2 = dot((2.6, 1.3), OC, "A1"), dot((5.0, -0.9), OC, "A2")
        self.play(FadeIn(SL[:2]), FadeIn(enc), FadeIn(shl), GrowArrow(ia[0]), GrowArrow(ia[1]), run_time=0.7)
        self.play(GrowArrow(oa), Create(pl), FadeIn(pll), FadeIn(P1, scale=0.5), FadeIn(P2, scale=0.5), run_time=0.9)
        self.cap("One shared encoder maps each view to a point in embedding space.", hold=3.0)
        N = [dot(p, NEG, n) for p, n in zip([(2.4, -1.4), (5.6, 1.7), (2.1, 0.5)], names[2:])]
        self.play(LaggedStart(*[AnimationGroup(Create(s), FadeIn(l), GrowArrow(a)) for s, l, a in zip(S, SL[2:], ia[2:])], lag_ratio=0.25), run_time=1.3)
        self.play(LaggedStart(*[FadeIn(n, scale=0.5) for n in N], lag_ratio=0.2), run_time=0.8)
        self.cap("The other ECGs in the batch add more points.", hold=2.6)
        # pull together, push apart
        def spring():
            a, b = P1[0].get_center(), P2[0].get_center(); d = b - a; n = np.array([-d[1], d[0], 0]) / (np.linalg.norm(d) + 1e-6)
            pts = [a + d * (i / 14) + (0.12 * n * (1 if i % 2 else -1) if 0 < i < 14 else 0) for i in range(15)]
            return VMobject(stroke_color=OC, stroke_width=3).set_points_as_corners(pts)
        sp = always_redraw(spring)
        c0 = np.array([3.8, 0.2, 0])
        tgt = [np.array(p + (0,)) for p in [(1.9, -2.0), (5.65, 1.95), (1.75, 0.9)]]
        pa = VGroup(*[Arrow(n[0].get_center(), n[0].get_center() + 0.7 * (n[0].get_center() - c0) / np.linalg.norm(n[0].get_center() - c0), buff=0.18, stroke_width=3, color=NEG, max_tip_length_to_length_ratio=0.35) for n in N])
        self.play(Create(sp), LaggedStart(*[GrowArrow(a) for a in pa], lag_ratio=0.15), run_time=0.8)
        self.play(P1.animate.shift(np.array([3.55, 0.4, 0]) - P1[0].get_center()), P2.animate.shift(np.array([4.15, 0.0, 0]) - P2[0].get_center()),
                  FadeOut(pa), *[n.animate.shift(t - n[0].get_center()) for n, t in zip(N, tgt)], run_time=1.6)
        self.cap("Training pulls the two views together and pushes the other ECGs apart.", hold=3.2)
        # the loss as a classification over the batch
        self.play(*[FadeOut(m) for m in (V1, V2, *S, SL, enc, shl, *ia, oa)], run_time=0.6)
        sims, probs = [0.9, 0.2, -0.1, 0.3], [0.59, 0.15, 0.08, 0.18]
        ry = [1.4, 0.7, 0.0, -0.7]
        rl = VGroup(*[T(n, 24, OC if i == 0 else GREY, BOLD).move_to(RIGHT * -6.3 + UP * y) for i, (n, y) in enumerate(zip(names[1:], ry))])
        sb = VGroup(*[tok(f"{s:.1f}".replace("-", "−"), INK, w=1.1, h=0.5, size=24, fill="#FEF3C7").move_to(RIGHT * -5.1 + UP * y) for s, y in zip(sims, ry)])
        h1 = T("similarity to A1", 22, INK, BOLD).move_to(RIGHT * -5.1 + UP * 2.15)
        sm = Arrow(RIGHT * -4.35 + UP * 0.35, RIGHT * -2.9 + UP * 0.35, buff=0, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.15)
        smt = T("softmax", 22, INK).next_to(sm, UP, buff=0.1)
        bars = VGroup(*[Rectangle(width=3.0 * p, height=0.42, stroke_width=0, fill_color=OC if i == 0 else NEG, fill_opacity=1).move_to(RIGHT * -2.6 + UP * y, aligned_edge=LEFT) for i, (p, y) in enumerate(zip(probs, ry))])
        bn = VGroup(*[T(f"{p:.2f}", 24, INK, BOLD).next_to(b, RIGHT, buff=0.12) for p, b in zip(probs, bars)])
        h2 = T("probability", 22, INK, BOLD).move_to(RIGHT * -1.7 + UP * 2.15)
        self.play(FadeIn(rl), FadeIn(h1), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in sb], lag_ratio=0.15), run_time=1.0)
        self.play(GrowArrow(sm), FadeIn(smt), FadeIn(h2), LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(bars, bn)], lag_ratio=0.2), run_time=1.4)
        hl = SurroundingRectangle(VGroup(rl[0], bn[0]), color=OC, buff=0.12, stroke_width=4)
        self.play(Create(hl), run_time=0.5)
        self.cap("The loss asks: which view in the batch is my partner?", hold=3.0)
        tab = VGroup(rl, sb, h1, sm, smt, bars, bn, h2, hl)
        self.play(FadeOut(VGroup(pl, pll, P1, P2, sp, *N)), tab.animate.shift(RIGHT * 3.4 + UP * 0.25), run_time=0.8)
        fm = T("loss = −log( exp(sim(z, z⁺) / τ)  /  Σ exp(sim(z, z′) / τ) )", 30, INK, BOLD).move_to(DOWN * 1.65)
        lg = T("z: A1     z⁺: its partner A2     z′: every other view in the batch     τ: temperature", 20, GREY).next_to(fm, DOWN, buff=0.3)
        self.play(FadeIn(fm), run_time=0.8); self.play(FadeIn(lg), run_time=0.5)
        self.cap("This is the InfoNCE loss: a softmax over similarities with temperature τ.", hold=3.4)
        # what the embedding space looks like after training
        self.play(FadeOut(VGroup(tab, fm, lg)), run_time=0.6)
        pl2 = Rectangle(width=8.4, height=5.2, stroke_color=GREY, stroke_width=2).move_to(LEFT * 2.2 + UP * 0.1)
        rng = np.random.default_rng(4)
        ctr = [(-4.6, 1.2), (-0.5, 1.1), (-2.5, -1.3)]
        D = VGroup(); end = []
        for c, (_, col) in zip(ctr, RHY):
            for _ in range(12):
                D.add(Dot(RIGHT * rng.uniform(-6.0, 1.6) + UP * rng.uniform(-2.2, 2.4), radius=0.11, color=NEG))
                end.append(np.clip(np.array([c[0] + rng.normal(0, 0.5), c[1] + rng.normal(0, 0.42), 0]), [-6.1, -2.2, 0], [1.7, 2.4, 0]))
        self.play(Create(pl2), FadeIn(D), run_time=0.8)
        self.play(*[d.animate.move_to(e) for d, e in zip(D, end)], run_time=2.0)
        lgd = VGroup(*[VGroup(Dot(radius=0.11, color=col), T(n, 20, col, BOLD)).arrange(RIGHT, buff=0.2) for n, col in RHY]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 4.6 + UP * 0.9)
        note = T("labels not used in training", 20, GREY, slant=ITALIC).next_to(lgd, DOWN, buff=0.5).align_to(lgd, LEFT)
        self.play(*[D[i].animate.set_color(RHY[i // 12][1]) for i in range(36)], FadeIn(lgd), FadeIn(note), run_time=1.0)
        self.cap("Without any labels, similar ECGs tend to end up close together.", hold=3.4)
