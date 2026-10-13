from kit import *
TK = ["The", "patient", "has", "a", "cold"]
SC = [-0.5, 0.2, 1.3, 0.6, 1.6]                   # scores from the slides
WT = [0.05, 0.10, 0.30, 0.15, 0.40]               # softmax of SC, rounded
class C2(Clip):
    TITLE = "Attention for one token"
    PACE, HOLD = 1.5, 1.6
    def construct(self):
        self.cap("Take the token “cold”: its query is compared with the key of every token.", hold=0)
        c = 0.42; ys = [1.6, 0.85, 0.1, -0.65, -1.4]
        q = mat(1, 4, QC, cell=c, seed=7)[0].move_to(RIGHT * -5.3 + UP * 0.1)
        ql = T("query of “cold”", 24, QC, BOLD).next_to(q, UP, buff=0.3)
        K = [mat(1, 4, KC, cell=c, seed=20 + j)[0].move_to(RIGHT * -1.6 + UP * y) for j, y in enumerate(ys)]
        KL = VGroup(*[T(t, 22, INK if t == "cold" else GREY, BOLD if t == "cold" else NORMAL).next_to(k, LEFT, buff=0.25) for t, k in zip(TK, K)])
        kh = T("keys", 24, KC, BOLD).move_to(RIGHT * -1.6 + UP * 2.35)
        self.play(FadeIn(q), FadeIn(ql), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(k, shift=LEFT * 0.2) for k in K], lag_ratio=0.12), FadeIn(KL), FadeIn(kh), run_time=1.0)
        self.rest(2.8)
        self.cap("Each score is a dot product: how well that key matches the query.", hold=0)
        sh = T("score = q·k ÷ √d", 24, INK, BOLD).move_to(RIGHT * 0.75 + UP * 2.35)
        self.play(FadeIn(sh), run_time=0.3)
        SB = VGroup()
        for j in range(5):
            ln = Line(q.get_right(), K[j].get_left() + LEFT * 0.75, color=AMB, stroke_width=4).set_z_index(3)
            kb = SurroundingRectangle(K[j], color=KC, buff=0.04, stroke_width=4)
            b = tok(f"{SC[j]:.1f}".replace("-", "−"), INK, w=1.1, h=0.5, size=24, fill="#FEF3C7").move_to(RIGHT * 0.75 + UP * ys[j])
            self.play(Create(ln), Create(kb), run_time=0.35)
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.35)
            self.play(FadeOut(ln), FadeOut(kb), run_time=0.2)
            SB.add(b)
            if j == 0: self.rest(0.6)
        self.wait(1.2)
        hl = VGroup(*[SurroundingRectangle(VGroup(KL[j], SB[j]), color=AMB, buff=0.08, stroke_width=4) for j in (2, 4)])
        self.cap("The highest scores go to “has” and to “cold” itself.", hold=0)
        self.play(Create(hl), run_time=0.6)
        self.wait(2.6 + self.HOLD)
        self.cap("Softmax turns the scores into weights between 0 and 1 that sum to 1.", hold=0)
        sm = Arrow(RIGHT * 1.45 + UP * 0.1, RIGHT * 2.85 + UP * 0.1, buff=0, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.15)
        smt = T("softmax", 22, INK).next_to(sm, UP, buff=0.1)
        wh = T("weight", 24, INK, BOLD).move_to(RIGHT * 4.2 + UP * 2.35)
        bars = VGroup(*[Rectangle(width=5.5 * w, height=0.42, stroke_width=0, fill_color=AMB, fill_opacity=1).move_to(RIGHT * 3.05 + UP * y, aligned_edge=LEFT) for w, y in zip(WT, ys)])
        WN = VGroup(*[T(f"{w:.2f}", 24, INK, BOLD).next_to(b, RIGHT, buff=0.12) for w, b in zip(WT, bars)])
        sum1 = T("sum = 1", 24, INK, BOLD).move_to(RIGHT * 4.2 + DOWN * 2.15)
        self.play(FadeOut(hl), GrowArrow(sm), FadeIn(smt), FadeIn(wh), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(bars, WN)], lag_ratio=0.2), run_time=1.4)
        self.play(FadeIn(sum1), run_time=0.4)
        self.rest(3.0)
        # weighted sum of values
        self.cap("The new vector for “cold” is the weighted sum of the five value vectors.", hold=0)
        self.play(*[FadeOut(m) for m in (q, ql, *K, kh, sh, SB, sm, smt, wh, bars, sum1)], run_time=0.7)
        V = [mat(1, 4, VC, cell=c, seed=40 + j)[0].move_to(RIGHT * -1.0 + UP * y) for j, y in enumerate(ys)]
        vh = T("values", 24, VC, BOLD).move_to(RIGHT * -1.0 + UP * 2.35)
        self.play(*[KL[j].animate.move_to(RIGHT * -5.4 + UP * ys[j]) for j in range(5)], *[WN[j].animate.move_to(RIGHT * -3.9 + UP * ys[j]) for j in range(5)], run_time=0.8)
        X = VGroup(*[T("×", 26, INK).move_to(RIGHT * -2.8 + UP * y) for y in ys])
        self.play(FadeIn(X), FadeIn(vh), LaggedStart(*[FadeIn(v, shift=LEFT * 0.2) for v in V], lag_ratio=0.12), run_time=1.0)
        self.play(*[V[j].animate.set_opacity(0.2 + 1.8 * WT[j]) for j in range(5)], run_time=0.7)
        sl = Line(RIGHT * -2.2 + DOWN * 1.85, RIGHT * 0.2 + DOWN * 1.85, color=INK, stroke_width=3)
        st = T("sum", 22, INK).next_to(sl, LEFT, buff=0.2)
        o = mat(1, 4, OC, cell=c, seed=61)[0].move_to(RIGHT * -1.0 + DOWN * 2.4)
        ol = T("new vector for “cold”", 24, "#A16207", BOLD).next_to(o, RIGHT, buff=0.35)
        self.play(Create(sl), FadeIn(st), run_time=0.4)
        self.play(*[TransformFromCopy(v, o) for v in V], FadeIn(ol), run_time=1.2)
        self.rest(3.0)
        self.cap("Now 'cold' carries its context: has a cold means an infection.", hold=0)
        ctx = VGroup(T("has a cold", 32, INK, BOLD), T("an infection, not a temperature", 24, PC, BOLD)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.75 + UP * 0.5)
        fr = SurroundingRectangle(ctx, color=PC, buff=0.3, stroke_width=3, corner_radius=0.15)
        self.play(FadeIn(ctx), Create(fr), run_time=0.8)
        self.rest(3.4)
