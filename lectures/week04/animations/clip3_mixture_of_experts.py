from kit import *
TOKS = [("denies", "#0891B2"), ("chest", "#DB2777"), ("pain", "#9333EA")]   # token colors (cyan, pink, purple)
ROUTE = {"denies": (0, 8), "chest": (2, 10), "pain": (6, 13)}                # top-2 experts per token (illustrative)
SCORES = [0.02, 0.04, 0.38, 0.03, 0.05, 0.02, 0.06, 0.03, 0.04, 0.02, 0.25, 0.01, 0.02, 0.01, 0.01, 0.01]   # router weights for "chest"
EF = "#DBEAFE"                                                             # expert box fill
class C3(Clip):
    TITLE = "Mixture of experts"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. dense: one feed-forward network for every token
        self.cap("In a dense model, every token goes through the same feed-forward network.", hold=0)
        ty = [1.4, 0.2, -1.0]
        T3 = VGroup(*[tok(w, c, w=1.5, h=0.55, size=22, fill="#FFFFFF").move_to([-5.6, y, 0]) for (w, c), y in zip(TOKS, ty)])
        ffn = box("Feed-forward network", 3.2, 3.3, EF, 24, stroke=UF).move_to([0.2, 0.2, 0])
        ar = VGroup(*[Arrow(t.get_right(), ffn.get_left() + UP * (y - 0.2) * 0.6, buff=0.1, stroke_width=3, color=c, max_tip_length_to_length_ratio=0.06) for t, (w, c), y in zip(T3, TOKS, ty)])
        self.play(LaggedStart(*[FadeIn(t) for t in T3], lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(ffn), LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.15), run_time=1.0)
        dn = T("all of its weights are used for every token", 22, GREY).next_to(ffn, DOWN, buff=0.35)
        self.play(FadeIn(dn), run_time=0.5)
        self.rest(2.4)
        # 2. split into experts
        self.cap("A mixture of experts splits it into many smaller networks, called experts.", hold=0)
        gx = [-0.7 + 0.9 * j for j in range(4)]; gy = [1.55 - 0.9 * i for i in range(4)]
        E = VGroup(*[box(f"E{4 * i + j + 1}", 0.78, 0.78, EF, 22, stroke=UF).move_to([gx[j], gy[i], 0]) for i in range(4) for j in range(4)])
        el = T("16 experts (illustrative)", 22, UF, BOLD).next_to(E, DOWN, buff=0.3)
        self.play(FadeOut(ar), FadeOut(dn), run_time=0.4)
        self.play(FadeTransform(ffn, E), run_time=1.2)
        self.play(FadeIn(el), run_time=0.5)
        self.rest(2.4)
        # 3. the router picks the top experts for "chest"
        self.cap("A router scores the experts for each token and picks the top two.", hold=0)
        rt = box("router", 1.3, 3.3, "#F3F4F6", 22).move_to([-3.4, 0.2, 0])
        self.play(FadeIn(rt), run_time=0.5)
        bx = [3.3 + 0.22 * k for k in range(16)]
        BR = VGroup(*[Rectangle(width=0.18, height=max(4.0 * v, 0.03), stroke_width=0, fill_color=(TOKS[1][1] if k in ROUTE["chest"] else "#D1D5DB"), fill_opacity=1).move_to([x, -1.0, 0], aligned_edge=DOWN) for k, (x, v) in enumerate(zip(bx, SCORES))])
        bh = T("router weights for “chest”", 22, INK, BOLD).move_to([5.0, 1.75, 0])
        bv = VGroup(T("E3: 0.38", 22, TOKS[1][1], BOLD).next_to(BR[2], UP, buff=0.12), T("E11: 0.25", 22, TOKS[1][1], BOLD).next_to(BR[10], UP, buff=0.12))
        bxl = T("E1 … E16", 20, GREY).move_to([5.0, -1.35, 0])
        a1 = Arrow(T3[1].get_right(), rt.get_left() + UP * 0.0, buff=0.1, stroke_width=3, color=TOKS[1][1], max_tip_length_to_length_ratio=0.15)
        self.play(GrowArrow(a1), run_time=0.5)
        self.play(FadeIn(bh), FadeIn(bxl), LaggedStart(*[GrowFromEdge(b, DOWN) for b in BR], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(bv), run_time=0.5)
        gate = Arrow(rt.get_right(), E.get_left(), buff=0.1, stroke_width=4, color=GREY, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(gate), *[E[k][0].animate.set_fill(TOKS[1][1], 0.45).set_stroke(TOKS[1][1], 4) for k in ROUTE["chest"]], run_time=0.9)
        self.rest(2.2)
        # 4. other tokens go to other experts
        self.cap("Different tokens go to different experts.", hold=0)
        self.play(FadeOut(BR), FadeOut(bh), FadeOut(bv), FadeOut(bxl), run_time=0.4)
        for i in (0, 2):
            w, c = TOKS[i]
            ai = Arrow(T3[i].get_right(), rt.get_left() + UP * (ty[i] - 0.2) * 0.5, buff=0.1, stroke_width=3, color=c, max_tip_length_to_length_ratio=0.15)
            self.play(GrowArrow(ai), run_time=0.4)
            self.play(*[E[k][0].animate.set_fill(c, 0.45).set_stroke(c, 4) for k in ROUTE[w]], run_time=0.8)
        idle = VGroup(T("colored: chosen by that token", 22, INK), T("blue: idle for these tokens", 22, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([5.0, 0.2, 0])
        self.play(FadeIn(idle), run_time=0.5)
        self.rest(2.2)
        # 5. the output is a weighted sum of the chosen experts
        self.cap("Each token's output is a weighted sum of its chosen experts.", hold=0)
        self.play(FadeOut(idle), run_time=0.3)
        f = VGroup(T("output for “chest”", 22, TOKS[1][1], BOLD),
                   T("= 0.60 × E3(chest)", 24, INK),
                   T("+ 0.40 × E11(chest)", 24, INK),
                   T("from 0.38 and 0.25, rescaled", 20, GREY),
                   T("only 2 of 16 experts run", 22, INK, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.95, 0.2, 0], aligned_edge=LEFT)
        self.play(Indicate(VGroup(E[2], E[10]), color=TOKS[1][1], scale_factor=1.1), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.1) for m in f], lag_ratio=0.25), run_time=1.6)
        self.rest(2.4)
        # 6. DeepSeek-V3 in numbers
        self.cap("DeepSeek-V3 has 671B parameters in total, but uses only 37B for each token.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.6)
        h = T("DeepSeek-V3, in every mixture-of-experts layer", 24, INK, BOLD).move_to([0, 2.4, 0])
        cnt = VGroup(T("256 routed experts + 1 shared expert", 24, INK), T("8 routed experts chosen per token", 24, INK)).arrange(DOWN, buff=0.2).next_to(h, DOWN, buff=0.35)
        b1 = Rectangle(width=9.0, height=0.5, stroke_width=0, fill_color="#9CA3AF", fill_opacity=1).move_to([-5.5, -0.65, 0], aligned_edge=LEFT)
        b2 = Rectangle(width=9.0 * 37 / 671, height=0.5, stroke_width=0, fill_color=TOKS[1][1], fill_opacity=1).move_to([-5.5, -1.85, 0], aligned_edge=LEFT)
        l1 = T("parameters in total", 22, INK).next_to(b1, UP, buff=0.12).align_to(b1, LEFT); v1 = T("671B", 26, INK, BOLD).next_to(b1, RIGHT, buff=0.2)
        l2 = T("parameters used for each token", 22, INK).next_to(b2, UP, buff=0.12).align_to(b2, LEFT); v2 = T("37B", 26, INK, BOLD).next_to(b2, RIGHT, buff=0.2)
        self.play(FadeIn(h), FadeIn(cnt), run_time=0.8)
        self.play(GrowFromEdge(b1, LEFT), FadeIn(l1), FadeIn(v1), run_time=0.9)
        self.play(GrowFromEdge(b2, LEFT), FadeIn(l2), FadeIn(v2), run_time=0.9)
        self.rest(2.6)
