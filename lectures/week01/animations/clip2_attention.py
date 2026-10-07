from kit import *
W = [[0.47, 0.23, 0.16, 0.14], [0.17, 0.48, 0.14, 0.21], [0.16, 0.19, 0.44, 0.21], [0.12, 0.26, 0.14, 0.48]]  # values from the Spring 2026 deck
class C2(Clip):
    TITLE = "Query, key, value: how attention works"
    def construct(self):
        c = 0.4
        X = mat(4, 6, EC, cell=c, seed=5).move_to(LEFT * 4.6 + UP * 0.15)
        xl = rowlabels(X, TOK, 22)
        Xt = T("Embeddings", 24, EC, BOLD).next_to(X, UP, buff=0.3)
        self.play(FadeIn(X), FadeIn(xl), FadeIn(Xt))
        self.cap("Start with one embedding vector per token.", hold=2.4)
        ys = [1.95, 0.15, -1.65]; cols = [QC, KC, VC]; names = ["Query", "Key", "Value"]; wn = ["Q", "K", "V"]
        M, Mt, Ar, Wl = [], [], [], []
        for y, col, n, w, sd in zip(ys, cols, names, wn, (11, 12, 13)):
            m = mat(4, 6, col, cell=c, seed=sd).move_to(RIGHT * 0.4 + UP * y); M.append(m)
            Mt.append(T(n, 24, col, BOLD).next_to(m, RIGHT, buff=0.3))
            a = Arrow(X.get_right(), m.get_left(), buff=0.25, stroke_width=3.5, color=col, max_tip_length_to_length_ratio=0.08); Ar.append(a)
            Wl.append(wsub(w, col).move_to(a.point_from_proportion(0.45) + {1.95: UP * 0.45 + LEFT * 0.35, 0.15: UP * 0.32, -1.65: DOWN * 0.45 + LEFT * 0.35}[y]))
        Q, K, V = M
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(w), FadeIn(m), FadeIn(t)) for a, w, m, t in zip(Ar, Wl, M, Mt)], lag_ratio=0.35), run_time=2.4)
        self.cap("Three learned projections turn each embedding into a query, a key, and a value.", hold=3.8)
        self.cap("Query: what this token is looking for.  Key: what each token offers.  Value: what it passes on.", hold=4.2)
        # focus on "My"
        self.play(*[FadeOut(m) for m in (X, xl, Xt, *Ar, *Wl)], run_time=0.6)
        grp = VGroup(Q, K, V, *Mt)
        self.play(grp.animate.shift(LEFT * 4.6), run_time=0.8)
        ql = rowlabels(Q, TOK, 21); kl = rowlabels(K, TOK, 21); vl = rowlabels(V, TOK, 21)
        self.play(FadeIn(ql), FadeIn(kl), FadeIn(vl), run_time=0.4)
        qh = SurroundingRectangle(Q[0], color=QC, buff=0.04, stroke_width=5)
        self.play(Create(qh), *[Q[i].animate.set_opacity(0.15) for i in (1, 2, 3)], run_time=0.7)
        self.cap("Follow one token. The query of \"My\" is compared with the key of every token.", hold=2.0)
        raw = [2.1, 1.4, 1.0, 0.9]
        sx = 0.9
        st = T("score = q · k / √d", 22, INK, BOLD).move_to(RIGHT * sx + UP * 1.55)
        sc = VGroup(); self.play(FadeIn(st), run_time=0.4)
        for j in range(4):
            ln = Line(Q[0].get_right(), K[j].get_right() + RIGHT * 0.05, color=AMB, stroke_width=4).set_z_index(3)
            kh = SurroundingRectangle(K[j], color=KC, buff=0.04, stroke_width=4)
            b = tok(f"{raw[j]:.1f}", INK, w=1.1, h=0.5, size=24, fill="#FEF3C7").move_to(RIGHT * sx + UP * (K[j].get_center()[1] + 0.0) )
            b.move_to(RIGHT * sx + UP * (0.84 - j * 0.6))
            self.play(Create(kh), Create(ln), run_time=0.35)
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.35)
            self.play(FadeOut(ln), FadeOut(kh), run_time=0.2)
            sc.add(b)
        sl = VGroup(*[T(t, 18, GREY).next_to(sc[j], LEFT, buff=0.15) for j, t in enumerate(TOK)])
        self.play(FadeIn(sl), run_time=0.3)
        self.cap("Each comparison is a dot product: a large score means the key matches the query.", hold=3.4)
        wx = 4.6
        wt = T("attention weight", 22, INK, BOLD).move_to(RIGHT * wx + UP * 1.55)
        sm = Arrow(RIGHT * (sx + 0.7) + DOWN * 0.06, RIGHT * (wx - 1.15) + DOWN * 0.06, buff=0, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.12)
        smt = T("softmax", 22, INK).next_to(sm, UP, buff=0.1)
        wb = VGroup(); wn_ = VGroup()
        for j in range(4):
            bar = Rectangle(width=2.6 * W[0][j], height=0.42, stroke_width=0, fill_color=AMB, fill_opacity=1).move_to(RIGHT * (wx - 0.9) + UP * (0.84 - j * 0.6), aligned_edge=LEFT)
            wb.add(bar); wn_.add(T(f"{W[0][j]:.2f}", 24, INK, BOLD).next_to(bar, RIGHT, buff=0.12))
        self.play(GrowArrow(sm), FadeIn(smt), FadeIn(wt), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(wb, wn_)], lag_ratio=0.2), run_time=1.4)
        self.cap("Softmax turns the four scores into attention weights that sum to 1.", hold=3.4)
        # weighted sum of values
        self.play(*[FadeOut(m) for m in (Q, K, ql, kl, qh, Mt[0], Mt[1], sc, sl, st, sm, smt, wt, wb)], run_time=0.7)
        Vg = VGroup(V, vl, Mt[2])
        self.play(Vg.animate.scale(1.35).move_to(RIGHT * 0.6 + UP * 0.9), run_time=0.8)
        self.play(*[wn_[j].animate.move_to(RIGHT * (V.get_left()[0] - 2.6) + UP * V[j].get_center()[1]) for j in range(4)], run_time=0.8)
        times = VGroup(*[T("×", 24, INK).move_to(RIGHT * (V.get_left()[0] - 1.95) + UP * V[j].get_center()[1]) for j in range(4)])
        self.play(FadeIn(times), *[V[j].animate.set_opacity(0.25 + 1.5 * W[0][j]) for j in range(4)], run_time=0.8)
        self.cap("The weights say how much of each token's value to take.", hold=2.6)
        out = mat(1, 6, OC, cell=c * 1.35, seed=31)[0].move_to(RIGHT * V.get_center()[0] + DOWN * 1.55)
        ol = T("new representation of \"My\"", 24, "#A16207", BOLD).next_to(out, RIGHT, buff=0.3)
        sumline = Line(V.get_corner(DL) + DOWN * 0.25 + LEFT * 0.2, V.get_corner(DR) + DOWN * 0.25 + RIGHT * 0.2, color=INK, stroke_width=3)
        plus = T("sum", 22, INK).next_to(sumline, LEFT, buff=0.2)
        self.play(Create(sumline), FadeIn(plus), run_time=0.4)
        self.play(TransformFromCopy(V, out), FadeIn(ol), run_time=1.2)
        self.cap("The output for \"My\" is the weighted sum of the values: now it carries context from the whole sentence.", hold=4.2)
        # full matrix
        self.play(*[FadeOut(m) for m in (Vg, wn_, times, out, ol, sumline, plus)], run_time=0.7)
        H = heat(W, cell=1.05, color=AMB, size=26, labels_r=TOK, labels_c=TOK).move_to(LEFT * 3.2 + UP * 0.15)
        for l in H[2][:4]: l.set_color(QC)
        ht = T("Attention weights", 24, INK, BOLD).next_to(H, UP, buff=0.25)
        rl = T("rows: queries", 20, QC, BOLD).next_to(H, DOWN, buff=0.25).shift(LEFT * 1.1)
        cl = T("columns: keys", 20, KC, BOLD).next_to(rl, RIGHT, buff=0.4)
        self.play(FadeIn(H[0]), FadeIn(H[2]), FadeIn(ht), FadeIn(rl), FadeIn(cl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(H[1][i * 4:(i + 1) * 4]) for i in range(4)], lag_ratio=0.4), run_time=1.6)
        self.cap("Repeat for every token to get the full attention matrix. Each row sums to 1.", hold=3.2)
        f1 = T("Attention(Q, K, V)", 30, INK, BOLD).move_to(RIGHT * 3.6 + UP * 0.9)
        f2 = T("= softmax( Q·Kᵀ / √d ) · V", 30, INK, BOLD).next_to(f1, DOWN, buff=0.3)
        self.play(FadeIn(f1), FadeIn(f2), run_time=0.8)
        self.cap("All of it in one line: scores, softmax, weighted sum.", hold=4)
