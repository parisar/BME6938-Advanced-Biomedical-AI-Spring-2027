from kit import *
class C1(Clip):
    TITLE = "Tokenization and embeddings"
    def construct(self):
        sent = T('"My name is John"', 60).move_to(UP * 0.4)
        self.play(Write(sent), run_time=1.2)
        self.cap("A transformer cannot read text. It only computes with numbers.")
        ys = [2.0, 0.9, -0.2, -1.3]
        toks = VGroup(*[tok(t, w=1.7, h=0.66, size=28).move_to(LEFT * 5.8 + UP * y) for t, y in zip(TOK, ys)])
        self.play(FadeOut(sent, shift=UP * 0.3), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.3) for t in toks], lag_ratio=0.25), run_time=1.6)
        self.cap("Step 1: the tokenizer splits the text into tokens.")
        idv = ["2026", "2171", "2003", "2198"]
        ids = VGroup(*[T(i, 30, UF, BOLD).move_to(LEFT * 3.7 + UP * y) for i, y in zip(idv, ys)])
        ar1 = VGroup(*[Arrow(t.get_right(), i.get_left(), buff=0.12, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.25) for t, i in zip(toks, ids)])
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(i)) for a, i in zip(ar1, ids)], lag_ratio=0.2), run_time=1.6)
        self.cap("Each token is replaced by its integer ID in a fixed vocabulary.")
        # embedding matrix
        E = mat(6, 8, EC, cell=0.42, seed=3).move_to(RIGHT * 0.2 + UP * 0.2)
        elab = ["⋮", "2003", "2026", "2171", "2198", "⋮"]
        El = rowlabels(E, elab, 21)
        Et = T("Embedding matrix", 26, INK, BOLD).next_to(E, UP, buff=0.3)
        Es = T("one row per vocabulary entry\n256 columns", 20, GREY, line_spacing=0.8).next_to(E, DOWN, buff=0.25)
        Edots = T("…", 28, GREY).next_to(E, RIGHT, buff=0.1)
        self.play(FadeIn(E), FadeIn(El), FadeIn(Et), FadeIn(Es), FadeIn(Edots), run_time=1)
        self.cap("Step 2: each ID selects one row of the embedding matrix.", hold=1.2)
        X = VGroup(); xpos = RIGHT * 4.75
        sel = {0: 2, 1: 3, 2: 1, 3: 4}
        for i in range(4):
            r = E[sel[i]]
            hl = SurroundingRectangle(r, color=AMB, buff=0.03, stroke_width=4)
            idh = SurroundingRectangle(ids[i], color=AMB, buff=0.08, stroke_width=3)
            cp = r.copy()
            self.play(Create(idh), Create(hl), run_time=0.45)
            self.play(cp.animate.move_to(xpos + UP * ys[i]), run_time=0.7)
            self.play(FadeOut(hl), FadeOut(idh), run_time=0.25)
            X.add(cp)
        xl = VGroup(*[T(t, 22, GREY).next_to(X[i], LEFT, buff=0.2) for i, t in enumerate(TOK)]).set_opacity(0)
        xd = VGroup(*[T("…", 26, GREY).next_to(X[i], RIGHT, buff=0.06) for i in range(4)])
        self.play(FadeIn(xd), run_time=0.5)
        self.cap("That row is a learned vector of 256 numbers: the token's embedding.")
        br = T("4 tokens × 256 dimensions", 24, UF, BOLD).next_to(X, DOWN, buff=0.4).shift(LEFT * 0.2)
        self.play(FadeIn(br))
        self.cap("The sentence is now a 4 × 256 matrix.")
        # positional encoding
        self.play(*[FadeOut(m) for m in (E, El, Et, Es, Edots, ids, ar1, toks, br, xd)], run_time=0.7)
        self.play(X.animate.move_to(LEFT * 4.1 + UP * 0.35), run_time=0.8)
        for i, x in enumerate(xl): x.next_to(X[i], LEFT, buff=0.2).set_opacity(1)
        self.play(FadeIn(xl), run_time=0.4)
        rowgap = ys[0] - ys[1]
        pv = [[0.5 + 0.45 * np.sin((i + 1) * (j + 1) * 0.9) for j in range(8)] for i in range(4)]
        P = VGroup(*[mat(1, 8, PC, cell=0.42, vals=[pv[i]])[0].move_to(RIGHT * 0.25 + X[i].get_center()[1] * UP) for i in range(4)])
        plus = T("+", 48).move_to((X.get_right() + P.get_left()) / 2)
        Pt = T("Positional encoding", 25, PC, BOLD).next_to(P, UP, buff=0.4)
        Xt = T("Token embeddings", 25, EC, BOLD).next_to(X, UP, buff=0.4)
        pl = VGroup()
        self.play(FadeIn(Xt), FadeIn(plus), FadeIn(P), FadeIn(Pt), run_time=0.9)
        self.cap("Step 3: add a positional encoding, because attention has no built-in sense of word order.", hold=3.6)
        R = VGroup(*[mat(1, 8, "#0F766E", cell=0.42, seed=20 + i)[0].move_to(RIGHT * 4.75 + X[i].get_center()[1] * UP) for i in range(4)])
        eq = T("=", 48).move_to(RIGHT * 2.5 + UP * 0.35)
        Rt = T("Input to encoder", 25, "#0F766E", BOLD).next_to(R, UP, buff=0.4)
        self.play(FadeIn(eq), TransformFromCopy(VGroup(X, P), R), FadeIn(Rt), run_time=1.3)
        self.cap("This matrix is the input to the first encoder block.", hold=3.5)
