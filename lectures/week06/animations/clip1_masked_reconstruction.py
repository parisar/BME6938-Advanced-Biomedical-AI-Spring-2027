from kit import *
MASK = [1, 2, 4, 6, 7, 9]                    # hidden patches (6 of 10)
PW, STEP, H, Y0 = 1.1, 1.22, 0.9, 1.15       # patch width, patch spacing after the split, ECG height, strip baseline
class C1(Clip):
    TITLE = "Masked reconstruction: learning by filling in gaps"
    def construct(self):
        self.cap("Start with an ECG recording that has no label.", hold=0)
        f = ecg_fn(10, hr=72, seed=3)
        x0 = -5 * PW
        P = VGroup(*[wave(f, k, k + 1, PW, H).shift(RIGHT * (x0 + k * PW) + UP * Y0).set_z_index(2) for k in range(10)])
        lab = T("single lead, 10 s, no diagnosis", 22, GREY).move_to(UP * 2.65).align_to(P, LEFT)
        self.play(FadeIn(lab), LaggedStart(*[Create(p, rate_func=linear) for p in P], lag_ratio=1, run_time=2.4))
        self.rest(2.4)
        # split into patches
        self.cap("Cut the signal into one-second patches: each patch becomes a token.", hold=0)
        div = VGroup(*[DashedLine(RIGHT * (x0 + k * PW) + UP * (Y0 - 0.4), RIGHT * (x0 + k * PW) + UP * (Y0 + 1.05), color=GREY, stroke_width=2) for k in range(1, 10)])
        self.play(Create(div), run_time=0.7)
        xl = -(10 * STEP - (STEP - PW)) / 2
        xs = [xl + k * STEP + PW / 2 for k in range(10)]
        B = VGroup(*[RoundedRectangle(corner_radius=0.08, width=PW + 0.06, height=1.5, stroke_color=EC, stroke_width=2, fill_color="#F8FAFC", fill_opacity=1).move_to(RIGHT * xs[k] + UP * (Y0 + 0.3)) for k in range(10)])
        self.play(FadeOut(div), *[P[k].animate.shift(RIGHT * (xs[k] - PW / 2 - (x0 + k * PW))) for k in range(10)], run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b) for b in B], lag_ratio=0.08), run_time=0.8)
        self.rest(2.8)
        # mask
        self.cap("Hide most of the patches at random.", hold=0)
        q = VGroup(*[T("?", 34, GREY, BOLD).move_to(B[k]) for k in MASK])
        self.play(*[B[k].animate.set_fill("#D1D5DB") for k in MASK], *[P[k].animate.set_stroke(opacity=0) for k in MASK], FadeIn(q), run_time=0.9)
        self.rest(2.4)
        # encoder on the visible patches
        self.cap("The encoder sees only the visible patches.", hold=0)
        yb = -1.0
        enc = box("Encoder", 3.4, 1.3, "#E2E8F0", size=28, stroke=EC).move_to(RIGHT * -4.9 + UP * yb)
        self.play(FadeIn(enc), run_time=0.5)
        vis = [k for k in range(10) if k not in MASK]
        cp = [P[k].copy() for k in vis]
        self.play(LaggedStart(*[c.animate.scale(0.45).move_to(enc).set_stroke(opacity=0) for c in cp], lag_ratio=0.2), run_time=1.3)
        self.remove(*cp)
        cx = [-2.2 + j * 0.46 for j in range(10)]
        E = {k: mat(4, 1, EC, cell=0.36, seed=70 + k).move_to(RIGHT * cx[k] + UP * yb) for k in vis}
        a1 = Arrow(enc.get_right(), RIGHT * (cx[0] - 0.3) + UP * yb, buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        l1 = T("encoder output", 20, EC, BOLD).next_to(E[vis[0]], DOWN, buff=0.3).align_to(E[vis[0]], LEFT)
        self.play(GrowArrow(a1), LaggedStart(*[FadeIn(E[k], shift=RIGHT * 0.2) for k in vis], lag_ratio=0.2), FadeIn(l1), run_time=1.2)
        self.rest(2.6)
        # decoder with mask tokens
        self.cap("A small decoder predicts the missing waveform from the encoder's output.", hold=0)
        M = {k: mat(4, 1, "#D1D5DB", cell=0.36, vals=[[1.0]] * 4).move_to(RIGHT * cx[k] + UP * yb) for k in MASK}
        l2 = T("+ mask tokens", 20, GREY, BOLD).next_to(l1, RIGHT, buff=0.15)
        dec = box("Decoder", 2.2, 1.0, "#EDE9FE", size=26, stroke=PC).move_to(RIGHT * 3.9 + UP * yb)
        a2 = Arrow(RIGHT * (cx[9] + 0.2) + UP * yb, dec.get_left(), buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        a3 = Arrow(dec.get_top(), UP * (Y0 - 0.42) + RIGHT * 3.9, buff=0.08, stroke_width=3.5, color=OC, max_tip_length_to_length_ratio=0.25)
        self.play(LaggedStart(*[FadeIn(M[k], shift=DOWN * 0.2) for k in MASK], lag_ratio=0.12), FadeIn(l2), run_time=1.0)
        self.play(GrowArrow(a2), FadeIn(dec), run_time=0.6)
        alpha = ValueTracker(0.0)
        def pf(k):
            return lambda t: f(t) + (1 - alpha.get_value()) * (-0.5 * f(t) + 0.14 * np.sin(2 * np.pi * 1.6 * t + k))
        def pred(k):
            return wave(pf(k), k, k + 1, PW, H, color=OC, sw=4).shift(RIGHT * (xs[k] - PW / 2) + UP * Y0).set_z_index(3)
        G = VGroup(*[always_redraw(lambda k=k: pred(k)) for k in MASK])
        self.play(GrowArrow(a3), FadeOut(q), LaggedStart(*[Create(g) for g in G], lag_ratio=0.15), run_time=1.4)
        self.rest(3.2)
        # loss on hidden patches
        self.cap("The loss compares prediction and truth only on the hidden patches.", hold=0)
        bottom = VGroup(enc, a1, l1, l2, dec, a2, a3, *E.values(), *M.values())
        def shade(k):
            ts = np.linspace(k, k + 1, 160); bx = xs[k] - PW / 2
            p = lambda fn: [np.array([bx + (t - k) * PW, Y0 + H * v, 0]) for t, v in zip(ts, fn(ts))]
            return Polygon(*(p(f) + p(pf(k))[::-1]), stroke_width=0, fill_color=QC, fill_opacity=0.35).set_z_index(1)
        S = VGroup(*[always_redraw(lambda k=k: shade(k)) for k in MASK])
        loss = T("loss = mean squared error, on hidden patches only", 26, INK, BOLD).move_to(UP * -0.4)
        self.play(FadeOut(bottom), run_time=0.6)
        self.play(*[P[k].animate.set_stroke(opacity=0.85) for k in MASK], *[B[k].animate.set_fill("#F8FAFC") for k in MASK], FadeIn(S), FadeIn(loss), run_time=0.9)
        self.rest(3.0)
        # training, and what the encoder learns
        self.cap("To fill the gaps, the encoder has to learn what a heartbeat looks like.", hold=0)
        steps = [T(f"training step {s}", 26, GREY).move_to(RIGHT * -3.6 + UP * -1.75) for s in ("1", "1,000", "100,000")]
        self.play(FadeIn(steps[0]), run_time=0.4)
        self.play(alpha.animate.set_value(0.55), Transform(steps[0], steps[1]), run_time=1.2)
        self.play(alpha.animate.set_value(0.93), Transform(steps[0], steps[2]), run_time=1.2)
        fb = ecg_fn(3, hr=60, seed=0); ts = np.linspace(0, 1.5, 3000); r = ts[np.argmax(fb(ts))]
        t0, t1, bx, by, bw, bh = r - 0.32, r + 0.5, 1.0, -2.5, 4.6, 1.3
        beat = wave(fb, t0, t1, bw, bh, sw=4).shift(RIGHT * bx + UP * by)
        tx = lambda t: bx + (t - t0) / (t1 - t0) * bw
        bl = VGroup(T("P", 22, PC, BOLD).move_to(RIGHT * tx(r - 0.17) + UP * (by + 0.5)),
                    T("QRS", 22, PC, BOLD).move_to(RIGHT * (tx(r) + 0.55) + UP * (by + bh - 0.15)),
                    T("T", 22, PC, BOLD).move_to(RIGHT * tx(r + 0.28) + UP * (by + 0.7)))
        self.play(Create(beat), run_time=1.0)
        self.play(FadeIn(bl), run_time=0.5)
        self.rest(3.0)
        # keep the encoder
        self.cap("After pretraining, keep the encoder and discard the decoder.", hold=0)
        self.play(*[FadeOut(m) for m in (P, B, G, S, loss, steps[0], beat, bl, lab)], run_time=0.7)
        enc2 = box("Encoder", 3.6, 1.6, "#E2E8F0", size=32, stroke=EC).move_to(LEFT * 2.6 + UP * 0.3)
        dec2 = box("Decoder", 2.4, 1.2, "#EDE9FE", size=28, stroke=PC).move_to(RIGHT * 2.9 + UP * 0.3)
        a4 = Arrow(enc2.get_right(), dec2.get_left(), buff=0.12, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.15)
        self.play(FadeIn(enc2), GrowArrow(a4), FadeIn(dec2), run_time=0.8)
        X = VGroup(Line(dec2.get_corner(UL), dec2.get_corner(DR)), Line(dec2.get_corner(DL), dec2.get_corner(UR))).set_stroke(GREY, 4)
        dl = T("discarded", 24, GREY).next_to(dec2, DOWN, buff=0.3)
        el = T("pretrained encoder", 26, EC, BOLD).next_to(enc2, DOWN, buff=0.3)
        hl = SurroundingRectangle(enc2, color=UF, buff=0.12, stroke_width=5, corner_radius=0.15)
        self.play(Create(X), FadeIn(dl), dec2.animate.set_opacity(0.35), a4.animate.set_opacity(0.35), run_time=0.8)
        self.play(Create(hl), FadeIn(el), run_time=0.7)
        self.rest(3.4)
        # the same recipe on a pathology tile
        self.cap("The same recipe works for pathology: hide image patches, reconstruct the pixels.", hold=0)
        self.play(*[FadeOut(m) for m in (enc2, dec2, a4, X, dl, el, hl)], run_time=0.7)
        arr = he_image("he_tumor.png", 320); ts, cp, yc = 3.0, 0.75, 0.35
        hid = sorted(np.random.default_rng(2).choice(16, 12, replace=False))
        at = lambda k, cx: [cx - ts / 2 + (k % 4 + 0.5) * cp, yc + ts / 2 - (k // 4 + 0.5) * cp, 0]
        L = ImageMobject(arr).set_height(ts).move_to([-4.3, yc, 0])
        R = ImageMobject(arr).set_height(ts).move_to([4.3, yc, 0])
        M = VGroup(*[Square(cp, stroke_color=WHITE, stroke_width=3, fill_color="#D1D5DB", fill_opacity=1).move_to(at(k, -4.3)) for k in hid])
        Q = VGroup(*[T("?", 24, GREY, BOLD).move_to(at(k, -4.3)) for k in hid])
        O = VGroup(*[Square(cp, stroke_color=OC, stroke_width=4).move_to(at(k, 4.3)) for k in hid])
        mid = box("Encoder + decoder", 3.0, 0.9, "#E2E8F0", size=24, stroke=EC).move_to([0, yc, 0])
        b1 = Arrow([-2.7, yc, 0], mid.get_left(), buff=0.1, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.25)
        b2 = Arrow(mid.get_right(), [2.7, yc, 0], buff=0.1, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.25)
        l1 = T("12 of 16 patches hidden", 22, GREY).next_to(L, DOWN, buff=0.25)
        l2 = T("target: the original pixels", 22, GREY).next_to(R, DOWN, buff=0.25)
        cr = T(HE_CREDIT, 20, GREY).move_to(DOWN * 2.55)
        self.play(FadeIn(L), FadeIn(cr), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(m), FadeIn(q)) for m, q in zip(M, Q)], lag_ratio=0.06), FadeIn(l1), run_time=1.0)
        self.play(GrowArrow(b1), FadeIn(mid), run_time=0.6)
        self.play(GrowArrow(b2), FadeIn(R), FadeIn(l2), run_time=0.7)
        self.play(LaggedStart(*[Create(o) for o in O], lag_ratio=0.05), run_time=0.8)
        self.rest(3.6)
