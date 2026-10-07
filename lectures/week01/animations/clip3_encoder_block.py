from kit import *
class C3(Clip):
    TITLE = "Inside an encoder block"
    def construct(self):
        c = 0.36
        X = mat(4, 4, "#0F766E", cell=c, seed=41).move_to(LEFT * 6.2 + UP * 0.2)
        xl = T("input\n4 × 256", 20, GREY, line_spacing=0.8).next_to(X, DOWN, buff=0.25)
        names = ["Multi-head\nattention", "Add &\nNorm", "Feed\nforward", "Add &\nNorm"]
        fills = ["#FAD7A0", "#F7F3A6", "#BFE3F2", "#F7F3A6"]; ws = [2.3, 1.35, 1.7, 1.35]; xs = [-3.2, -0.8, 1.35, 3.5]
        B = VGroup()
        for n, f, w, x in zip(names, fills, ws, xs):
            r = RoundedRectangle(corner_radius=0.12, width=w, height=1.6, stroke_color=INK, stroke_width=2, fill_color=f, fill_opacity=1).move_to(RIGHT * x + UP * 0.2)
            B.add(VGroup(r, T(n, 24, INK, BOLD, line_spacing=0.8).move_to(r)))
        frame = RoundedRectangle(corner_radius=0.25, width=9.75, height=4.95, stroke_color=UF, stroke_width=3).move_to(RIGHT * 0.125 + UP * 0.1)
        ft = T("Encoder block", 24, UF, BOLD).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        Y = mat(4, 4, "#0F766E", cell=c, seed=47).move_to(RIGHT * 6.25 + UP * 0.2)
        yl = T("output\n4 × 256", 20, GREY, line_spacing=0.8).next_to(Y, DOWN, buff=0.25)
        def arr(a, b): return Arrow(a, b, buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        A = [arr(X.get_right(), B[0].get_left()), arr(B[0].get_right(), B[1].get_left()), arr(B[1].get_right(), B[2].get_left()), arr(B[2].get_right(), B[3].get_left()), arr(B[3].get_right(), Y.get_left())]
        self.play(FadeIn(X), FadeIn(xl)); self.play(Create(frame), FadeIn(ft), run_time=0.8)
        self.cap("An encoder block takes the token matrix and refines it in four steps.", hold=2.6)
        # 1 multi-head attention
        self.play(GrowArrow(A[0]), FadeIn(B[0]), run_time=0.7)
        hv = [[[0.6,0.2,0.1,0.1],[0.2,0.5,0.2,0.1],[0.1,0.2,0.6,0.1],[0.1,0.3,0.1,0.5]],
              [[0.1,0.6,0.2,0.1],[0.5,0.1,0.1,0.3],[0.2,0.2,0.2,0.4],[0.3,0.1,0.5,0.1]],
              [[0.25,0.25,0.25,0.25],[0.1,0.1,0.1,0.7],[0.4,0.1,0.1,0.4],[0.7,0.1,0.1,0.1]]]
        heads = VGroup()
        for h, col in zip(hv, (QC, KC, VC)):
            g = VGroup(*[Square(0.22, stroke_color=WHITE, stroke_width=1, fill_color=col, fill_opacity=0.15 + 0.85 * h[i][j]).move_to(RIGHT * j * 0.22 + DOWN * i * 0.22) for i in range(4) for j in range(4)])
            heads.add(g)
        heads.arrange(RIGHT, buff=0.18).next_to(B[0], DOWN, buff=0.4)
        hl = VGroup(*[T(f"head {i+1}", 18, GREY).next_to(heads[i], DOWN, buff=0.08) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.15) for h in heads], lag_ratio=0.3), FadeIn(hl), run_time=1.4)
        self.cap("1. Multi-head attention: several attention heads run in parallel, each with its own Q, K, V projections.", hold=4.0)
        self.cap("Each head can track a different relationship. Their outputs are concatenated.", hold=3.0)
        # 2 residual + norm
        self.play(GrowArrow(A[1]), FadeIn(B[1]), run_time=0.6)
        def skip(i0, i1):
            p0 = A[i0].get_start() + RIGHT * 0.25; p1 = B[i1].get_top()
            up = 1.45
            pts = [p0, p0 + UP * up, np.array([p1[0], p0[1] + up, 0]), p1 + UP * 0.05]
            path = VMobject(stroke_color=AMB, stroke_width=5).set_points_as_corners(pts)
            tip = Triangle(fill_color=AMB, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI).move_to(p1 + UP * 0.12)
            return VGroup(path, tip)
        s1 = skip(0, 1); s1l = T("skip connection", 20, "#B45309", BOLD).next_to(s1[0], UP, buff=0.08)
        self.play(Create(s1[0]), run_time=0.9); self.play(FadeIn(s1[1]), FadeIn(s1l), run_time=0.3)
        self.cap("2. Add & Norm: the block's input is added back to the attention output, then normalized.", hold=3.6)
        self.cap("This residual path keeps gradients flowing when many blocks are stacked.", hold=3.0)
        # 3 FFN
        self.play(GrowArrow(A[2]), FadeIn(B[2]), run_time=0.6)
        rows = VGroup(*[VGroup(mat(1, 4, "#0F766E", cell=0.22, seed=50 + i)[0], T("→", 20, INK), mat(1, 4, "#0E7490", cell=0.22, seed=60 + i)[0]).arrange(RIGHT, buff=0.1) for i in range(4)]).arrange(DOWN, buff=0.1).next_to(B[2], DOWN, buff=0.4)
        self.play(FadeOut(heads), FadeOut(hl), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25), run_time=1.2)
        self.cap("3. Feed forward: a small network transforms each token's vector separately.", hold=3.6)
        # 4 second add & norm
        self.play(GrowArrow(A[3]), FadeIn(B[3]), run_time=0.6)
        s2 = skip(2, 3)
        self.play(Create(s2[0]), run_time=0.8); self.play(FadeIn(s2[1]), run_time=0.2)
        self.cap("4. A second Add & Norm, again with a skip connection.", hold=2.6)
        self.play(GrowArrow(A[4]), FadeIn(Y), FadeIn(yl), run_time=0.8)
        self.cap("The output has the same shape as the input: one refined vector per token.", hold=3.2)
        # stack
        blk = VGroup(frame, ft, B, *A, s1, s1l, s2, rows, X, xl, Y, yl)
        self.play(FadeOut(rows), run_time=0.3); blk.remove(rows)
        mini = VGroup(*[box(f"Encoder block {i+1}", 5.0, 0.7, "#DBEAFE", size=24, stroke=UF) for i in range(6)]).arrange(UP, buff=0.14).move_to(UP * 0.3)
        self.play(FadeOut(blk, scale=0.6), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in mini], lag_ratio=0.2), run_time=1.6)
        inl = T("token embeddings + positions", 21, GREY).next_to(mini, DOWN, buff=0.2)
        outl = T("contextual representations", 21, "#0F766E", BOLD).next_to(mini, UP, buff=0.2)
        self.play(FadeIn(inl), FadeIn(outl))
        self.cap("Because shapes match, blocks stack. The original transformer used six.", hold=4)
