from kit import *
PR = [("pain", 0.62), ("tightness", 0.15), ("discomfort", 0.12), ("pressure", 0.09), ("wall", 0.02)]   # illustrative, as on the slides
NXT, NXTF = "#B45309", "#FEF3C7"                   # the position being generated
def word(s, color=INK, fill="#F3F4F6"):
    return tok(s, color, w=max(1.0, 0.19 * len(s) + 0.5), h=0.62, size=26, fill=fill)
def qbox():
    return tok("?", NXT, w=0.8, h=0.62, size=28, fill=NXTF)
class C1(Clip):
    TITLE = "Generating text one token at a time"
    PACE, HOLD = 1.6, 2.5
    def append(self, row, s):
        old = row[-1]
        nw = word(s, NXT, NXTF).next_to(row[-2], RIGHT, buff=0.12)
        nq = qbox().next_to(nw, RIGHT, buff=0.12)
        row.remove(old); row.add(nw)
        self.play(ReplacementTransform(old, nw), run_time=0.7)
        self.play(FadeIn(nq, shift=RIGHT * 0.2), run_time=0.4)
        row.add(nq)
        return nw
    def settle(self, w):
        return AnimationGroup(w[0].animate.set_fill("#F3F4F6").set_stroke(INK), w[1].animate.set_color(INK))
    def construct(self):
        row = VGroup(*[word(w) for w in ["The", "patient", "denies", "chest"]], qbox()).arrange(RIGHT, buff=0.12)
        row.move_to(UP * 2.3).to_edge(LEFT, buff=0.7)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in row], lag_ratio=0.15), run_time=1.2)
        self.cap("A decoder writes text one token at a time, from left to right.", hold=2.6)
        dec = box("Decoder", 2.6, 1.0, "#EDE9FE", size=28, stroke=PC).move_to(RIGHT * -4.2 + DOWN * 0.3)
        a1 = Arrow(RIGHT * -4.2 + UP * 1.9, dec.get_top(), buff=0.06, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.15)
        stp = T("step 1", 22, GREY).next_to(dec, DOWN, buff=0.25)
        self.play(GrowArrow(a1), FadeIn(dec), FadeIn(stp), run_time=0.8)
        ys = [0.95, 0.4, -0.15, -0.7, -1.25]
        hd = T("next-token probability", 22, INK, BOLD).move_to(RIGHT * 1.4 + UP * 1.55)
        L = VGroup(*[T(w, 24, INK).move_to(RIGHT * -0.2 + UP * y, aligned_edge=RIGHT) for (w, _), y in zip(PR, ys)])
        bars = VGroup(*[Rectangle(width=max(5.0 * p, 0.04), height=0.4, stroke_width=0, fill_color=AMB, fill_opacity=1).move_to(UP * y, aligned_edge=LEFT) for (_, p), y in zip(PR, ys)])
        N = VGroup(*[T(f"{p:.2f}", 24, INK, BOLD).next_to(b, RIGHT, buff=0.12) for (_, p), b in zip(PR, bars)])
        nt = T("illustrative numbers", 20, GREY).move_to(RIGHT * 1.4 + DOWN * 1.85)
        a2 = Arrow(dec.get_right(), RIGHT * -1.95 + DOWN * 0.3, buff=0.08, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(a2), FadeIn(hd), FadeIn(L), FadeIn(nt), run_time=0.7)
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(bars, N)], lag_ratio=0.15), run_time=1.4)
        self.cap("It predicts a probability for every token in the vocabulary.", hold=3.0)
        hl = SurroundingRectangle(VGroup(L[0], N[0]), color=NXT, buff=0.1, stroke_width=4)
        self.play(Create(hl), run_time=0.5)
        self.cap("Greedy decoding picks the most likely token: “pain”.", hold=1.6)
        w1 = self.append(row, "pain")
        self.wait(0.8)
        self.play(FadeOut(VGroup(hd, L, bars, N, nt, hl, a2)), self.settle(w1), run_time=0.6)
        self.play(Transform(stp, T("step 2", 22, GREY).move_to(stp)), Indicate(dec, color=PC, scale_factor=1.1), run_time=0.8)
        self.cap("The new token is appended, and the model runs again.", hold=1.4)
        w2 = self.append(row, "and")
        self.wait(1.0)
        self.play(self.settle(w2), Transform(stp, T("step 3", 22, GREY).move_to(stp)), Indicate(dec, color=PC, scale_factor=1.1), run_time=0.8)
        w3 = self.append(row, "dyspnea")
        self.cap("Each forward pass adds one token: first “and”, then “dyspnea”.", hold=2.6)
        # greedy versus sampling with temperature
        self.play(FadeOut(VGroup(dec, a1, stp)), self.settle(w3), run_time=0.6)
        p = np.array([q for _, q in PR])
        G = VGroup()
        for tau, cx, sub in ((0.5, -4.2, "low: close to greedy"), (1.0, 0.0, "the model's probabilities"), (2.0, 4.2, "high: more random")):
            pt = p ** (1 / tau); pt = pt / pt.sum()
            bs = VGroup(*[Rectangle(width=0.5, height=max(1.9 * v, 0.03), stroke_width=0, fill_color=NXT if i == 0 else AMB, fill_opacity=1) for i, v in enumerate(pt)]).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
            bs.move_to(RIGHT * cx + DOWN * 1.35, aligned_edge=DOWN)
            base = Line(bs.get_corner(DL) + LEFT * 0.15, bs.get_corner(DR) + RIGHT * 0.15, color=GREY, stroke_width=2)
            ht = T(f"temperature {tau:g}", 24, INK, BOLD).move_to(RIGHT * cx + UP * 1.45)
            st = T(sub, 20, GREY).next_to(ht, DOWN, buff=0.12)
            bl = T("pain … wall", 20, GREY).next_to(base, DOWN, buff=0.12)
            G.add(VGroup(ht, st, bs, base, bl))
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in G], lag_ratio=0.25), run_time=1.4)
        self.cap("Greedy takes the top token; sampling draws by probability; temperature sets how random.", hold=3.6)
