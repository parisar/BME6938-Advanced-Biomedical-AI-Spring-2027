from kit import *
TK = ["The", "patient", "has", "a", "cold"]
IDS = [1996, 5776, 2038, 1037, 3147]               # illustrative IDs, as on the slides
ROWS = ["0", "⋮", "1037", "1996", "2038", "3147", "5776", "⋮", "30521"]
IDC = "#A16207"                                    # token IDs
class C1(Clip):
    TITLE = "From tokens to vectors"
    PACE, HOLD = 1.3, 1.0
    def construct(self):
        self.cap("A transformer cannot read text: it needs numbers.", hold=0)
        s = T("“The patient has a cold”", 40, INK, BOLD).move_to(UP * 2.1)
        self.play(FadeIn(s, shift=UP * 0.2), run_time=0.8)
        self.rest(2.4)
        self.cap("A tokenizer splits the sentence into tokens.", hold=0)
        B = VGroup(*[tok(t, INK, w=1.9, h=0.7, size=28) for t in TK]).arrange(RIGHT, buff=0.3).move_to(UP * 0.8)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.3) for b in B], lag_ratio=0.15), run_time=1.2)
        self.rest(2.4)
        self.cap("Each token gets an integer ID from the tokenizer's vocabulary.", hold=0)
        I = VGroup(*[T(str(i), 28, IDC, BOLD).next_to(b, DOWN, buff=0.3) for i, b in zip(IDS, B)])
        note = T("IDs are illustrative", 22, GREY).next_to(I, DOWN, buff=0.45)
        self.play(LaggedStart(*[FadeIn(i, shift=DOWN * 0.15) for i in I], lag_ratio=0.15), FadeIn(note), run_time=1.2)
        self.rest(2.8)
        # embedding lookup
        self.cap("Each ID looks up one row of a learned embedding table.", hold=0)
        ys = [1.6, 0.8, 0.0, -0.8, -1.6]
        self.play(FadeOut(s), FadeOut(note), *[B[k].animate.scale(0.8).move_to(RIGHT * -5.6 + UP * ys[k]) for k in range(5)],
                  *[I[k].animate.scale(0.85).move_to(RIGHT * -3.75 + UP * ys[k]) for k in range(5)], run_time=1.0)
        c = 0.42; rng = np.random.default_rng(12)
        ty = [2.0 - 0.42 * i for i in range(9)]
        tab = VGroup(); lab = VGroup(); row = {}; labi = {}
        for r, y in zip(ROWS, ty):
            if r == "⋮":
                lab.add(vdots(r=0.035, gap=0.07).move_to(RIGHT * 0.2 + UP * y)); continue
            rr = VGroup(*[Square(c, stroke_color=WHITE, stroke_width=1.5, fill_color=EC, fill_opacity=float(rng.uniform(0.2, 0.95))).move_to(RIGHT * (0.2 - 1.5 * c + j * c) + UP * y) for j in range(4)])
            l = T(r, 20, GREY).next_to(rr, LEFT, buff=0.2)
            tab.add(rr); lab.add(l); row[r] = rr; labi[r] = l
        tt = T("embedding table: 30,522 rows × d", 22, EC, BOLD).move_to(RIGHT * 0.2 + UP * 2.65)
        self.play(FadeIn(tab), FadeIn(lab), FadeIn(tt), run_time=0.8)
        out = []
        for k in range(5):
            key = str(IDS[k])
            a = Arrow(I[k].get_right(), labi[key].get_left(), buff=0.1, stroke_width=3, color=IDC, max_tip_length_to_length_ratio=0.12)
            h = SurroundingRectangle(row[key], color=IDC, buff=0.04, stroke_width=4)
            v = row[key].copy()
            self.play(GrowArrow(a), Create(h), run_time=0.6 if k == 0 else 0.35)
            self.play(v.animate.move_to(RIGHT * 3.4 + UP * ys[k]), run_time=0.8 if k == 0 else 0.5)
            self.play(FadeOut(a), FadeOut(h), run_time=0.2)
            out.append(v)
            if k == 0: self.rest(1.2)
        OL = VGroup(*[T(t, 22, GREY).next_to(v, RIGHT, buff=0.25) for t, v in zip(TK, out)])
        self.play(FadeIn(OL), run_time=0.4)
        # stack into a matrix
        self.cap("The five vectors stack into a 5 × d matrix: one row per token.", hold=0)
        self.play(*[v.animate.move_to(RIGHT * 3.4 + UP * (0.84 - k * c)) for k, v in enumerate(out)],
                  *[OL[k].animate.move_to(RIGHT * (3.4 + 2 * c + 0.25) + UP * (0.84 - k * c), aligned_edge=LEFT) for k in range(5)], run_time=0.9)
        M = VGroup(*out)
        fr = SurroundingRectangle(M, color=INK, buff=0.06, stroke_width=3)
        ml = T("5 × d matrix", 26, INK, BOLD).next_to(fr, DOWN, buff=0.3)
        md = T("d = 4 drawn here, 768 in BERT-base", 20, GREY).next_to(ml, DOWN, buff=0.15)
        self.play(Create(fr), FadeIn(ml), FadeIn(md), run_time=0.7)
        self.rest(3.0)
        # the problem
        self.cap("Problem: the token “cold” always gets the same vector.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.7)
        def sent(words, y):
            return VGroup(*[tok(w, INK, w=1.25, h=0.55, size=22) for w in words]).arrange(RIGHT, buff=0.12).move_to(UP * y).to_edge(LEFT, buff=0.55)
        S1, S2 = sent(TK, 1.9), sent(["The", "patient", "feels", "cold"], -0.1)
        self.play(FadeIn(S1), FadeIn(S2), run_time=0.7)
        vals = [[float(x) for x in np.random.default_rng(5).uniform(0.2, 0.95, 4)]]
        for S, y in ((S1, 1.9), (S2, -0.1)):
            h = SurroundingRectangle(S[-1], color=IDC, buff=0.05, stroke_width=4)
            idl = T("ID 3147", 22, IDC, BOLD).move_to(RIGHT * 1.7 + UP * y)
            v = mat(1, 4, EC, cell=c, vals=vals)[0].move_to(RIGHT * 4.3 + UP * y)
            a1 = Arrow(S[-1].get_right(), idl.get_left(), buff=0.12, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.2)
            a2 = Arrow(idl.get_right(), v.get_left(), buff=0.12, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.2)
            self.play(Create(h), GrowArrow(a1), FadeIn(idl), run_time=0.5); self.play(GrowArrow(a2), FadeIn(v), run_time=0.5)
        same = T("identical vectors", 24, INK, BOLD).move_to(RIGHT * 4.3 + UP * 0.9)
        self.play(FadeIn(same), run_time=0.4)
        self.rest(2.8)
        self.cap("But the meanings differ: an infection versus a temperature.", hold=0)
        m1 = T("has a cold: an infection", 24, PC, BOLD).next_to(S1, DOWN, buff=0.3).align_to(S1, LEFT)
        m2 = T("feels cold: a low temperature", 24, "#0369A1", BOLD).next_to(S2, DOWN, buff=0.3).align_to(S2, LEFT)
        self.play(FadeIn(m1), FadeIn(m2), run_time=0.7)
        self.rest(3.0)
        self.cap("Attention fixes this by giving each token a vector that depends on its context.", hold=0)
        nx = T("Next: attention mixes in context from the other tokens.", 26, UF, BOLD).move_to(DOWN * 2.0)
        self.play(FadeIn(nx, shift=UP * 0.15), run_time=0.6)
        self.rest(3.2)
