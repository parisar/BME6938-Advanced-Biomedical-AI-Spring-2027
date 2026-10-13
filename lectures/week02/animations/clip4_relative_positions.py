from kit import *
TK = ["The", "patient", "has", "a", "cold"]
SC = ["−0.5", "0.2", "1.3", "0.6", "1.6"]          # scores for "cold" from clip 2
DIST = ["4", "3", "2", "1", "0"]
PEN = ["−1.0", "−0.75", "−0.5", "−0.25", "0"]      # ALiBi penalty, slope 0.25
NEW = ["−1.5", "−0.55", "0.8", "0.35", "1.6"]
W0 = [0.05, 0.10, 0.30, 0.15, 0.40]                # softmax before ALiBi
W1 = [0.02, 0.06, 0.24, 0.15, 0.53]                # softmax after ALiBi
# RoPE: |q| |k| cos(15°) = 1.04 with the key 15° ahead of the query; 15° of rotation per position
QL, KL0, Q0, K0 = 1.2, 1.0767 / 1.2, 20.0, 35.0
def d2(a):
    return np.array([np.cos(np.radians(a)), np.sin(np.radians(a)), 0])
class C4(Clip):
    TITLE = "Relative positions: RoPE and ALiBi"
    PACE, HOLD = 1.0, 0.2
    def construct(self):
        # 1. distance, not absolute position
        self.cap("What matters is often distance, not absolute position.", hold=0)
        sx = [-5.25 + k * 1.5 for k in range(8)]
        S = VGroup(*[RoundedRectangle(corner_radius=0.08, width=1.25, height=0.6, stroke_color="#D1D5DB", stroke_width=2).move_to([x, 0.6, 0]) for x in sx])
        N = VGroup(*[T(str(k + 1), 22, GREY).move_to([x, 1.3, 0]) for k, x in enumerate(sx)])
        pl = T("position", 20, GREY).next_to(N, LEFT, buff=0.3)
        ch = tok("chest", INK, w=1.25, h=0.6, size=24, fill="#FEE2E2").move_to([sx[1], 0.6, 0])
        pn = tok("pain", INK, w=1.25, h=0.6, size=24, fill="#DCFCE7").move_to([sx[2], 0.6, 0])
        br = VGroup(Line([sx[1], -0.1, 0], [sx[2], -0.1, 0]), Line([sx[1], -0.1, 0], [sx[1], 0.15, 0]), Line([sx[2], -0.1, 0], [sx[2], 0.15, 0])).set_stroke("#B45309", 4)
        bl = T("distance 1", 22, "#B45309", BOLD).next_to(br, DOWN, buff=0.15)
        ab = T("absolute positions 2 and 3", 22, INK).move_to([0, -1.6, 0])
        self.play(FadeIn(S), FadeIn(N), FadeIn(pl), run_time=0.7)
        self.play(FadeIn(ch), FadeIn(pn), Create(br), FadeIn(bl), FadeIn(ab), run_time=0.9)
        self.play(VGroup(ch, pn, br, bl).animate.shift(RIGHT * 7.5), Transform(ab, T("absolute positions 7 and 8", 22, INK).move_to(ab)), run_time=1.6)
        self.rest(2.8)
        # 2. a score depends on the angle between query and key
        self.cap("A query-key score depends on the angle between the two vectors.", hold=0)
        self.play(*[FadeOut(x) for x in (S, N, pl, ch, pn, br, bl, ab)], run_time=0.6)
        O = np.array([-2.8, -0.7, 0]); U = 2.0
        tq, tk = ValueTracker(Q0), ValueTracker(K0)
        axes = VGroup(Line(O + LEFT * 2.4, O + RIGHT * 3.0), Line(O + DOWN * 1.5, O + UP * 2.9)).set_stroke("#D1D5DB", 2)
        qa = always_redraw(lambda: Arrow(O, O + U * QL * d2(tq.get_value()), buff=0, color=QC, stroke_width=6, max_tip_length_to_length_ratio=0.1))
        ka = always_redraw(lambda: Arrow(O, O + U * KL0 * d2(tk.get_value()), buff=0, color=KC, stroke_width=6, max_tip_length_to_length_ratio=0.12))
        ql = always_redraw(lambda: T("q: chest", 22, QC, BOLD).move_to(O + (U * QL + 0.55) * d2(tq.get_value())))
        kl = always_redraw(lambda: T("k: pain", 22, KC, BOLD).move_to(O + (U * KL0 + 0.5) * d2(tk.get_value())))
        arc = always_redraw(lambda: Arc(radius=0.75, start_angle=np.radians(tq.get_value()), angle=np.radians(tk.get_value() - tq.get_value()), arc_center=O, color=AMB, stroke_width=6))
        al = always_redraw(lambda: T(f"{tk.get_value() - tq.get_value():.0f}°", 22, "#B45309", BOLD).move_to(O + 1.4 * d2((tq.get_value() + tk.get_value()) / 2)))
        px = 1.3
        h1 = T("score = |q| × |k| × cos(angle)", 24, INK, BOLD).move_to([px, 2.2, 0], aligned_edge=LEFT)
        h2 = T("smaller angle, higher score", 22, GREY).move_to([px, 1.6, 0], aligned_edge=LEFT)
        def rows(pc, pp):
            return VGroup(T(f"chest, position {pc}: rotate {15 * pc}°", 22, QC, BOLD).move_to([px, 1.4, 0], aligned_edge=LEFT),
                          T(f"pain, position {pp}: rotate {15 * pp}°", 22, KC, BOLD).move_to([px, 0.85, 0], aligned_edge=LEFT))
        def score(v, sub):
            return VGroup(T(f"score q·k = {v}", 30, INK, BOLD).move_to([px, -0.3, 0], aligned_edge=LEFT),
                          T(sub, 20, GREY).move_to([px, -0.85, 0], aligned_edge=LEFT))
        self.play(Create(axes), run_time=0.5)
        self.play(GrowArrow(qa), GrowArrow(ka), FadeIn(ql), FadeIn(kl), run_time=1.0)
        self.remove(qa, ka); self.add(qa, ka)
        self.play(FadeIn(h1), FadeIn(h2), run_time=0.7)
        self.play(Create(arc), FadeIn(al), run_time=0.7)
        sc = score("1.04", "no position yet")
        self.play(FadeIn(sc), run_time=0.6)
        self.rest(2.4)
        # 3. RoPE: rotate by position
        self.cap("RoPE rotates each query and key by an angle set by its position.", hold=0)
        rw = rows(2, 3)
        self.play(Transform(h1, T("RoPE: rotate by 15° per position", 24, INK, BOLD).move_to([px, 2.2, 0], aligned_edge=LEFT)), FadeOut(h2), run_time=0.7)
        self.play(FadeIn(rw), run_time=0.6)
        self.play(tq.animate.set_value(Q0 + 30), tk.animate.set_value(K0 + 45), run_time=1.8)
        self.play(Transform(sc, score("0.93", "positions 2 and 3: angle 30°")), Indicate(al, color=AMB), run_time=0.8)
        self.rest(2.4)
        # 4. same distance, same score
        self.cap("The score depends only on the distance between the two tokens.", hold=0)
        self.play(tq.animate.set_value(Q0 + 105), tk.animate.set_value(K0 + 120), Transform(rw, rows(7, 8)), run_time=2.0)
        self.play(Transform(sc, score("0.93", "positions 7 and 8: still 30°")), Indicate(al, color=AMB), run_time=0.8)
        self.rest(2.4)
        # 5. farther apart
        self.cap("Farther apart means a larger angle and a lower score.", hold=0)
        self.play(tq.animate.set_value(Q0 + 30), tk.animate.set_value(K0 + 90), Transform(rw, rows(2, 6)), run_time=2.0)
        self.play(Transform(sc, score("0.28", "4 positions apart: angle 75°")), Indicate(al, color=AMB), run_time=0.8)
        nt = T("real models: many pairs, different speeds", 20, GREY).move_to([px, -1.7, 0], aligned_edge=LEFT)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.6)
        # 6. ALiBi table
        self.cap("ALiBi: subtract a penalty that grows with distance.", hold=0)
        self.play(*[FadeOut(x) for x in (axes, qa, ka, ql, kl, arc, al, h1, rw, sc, nt)], run_time=0.6)
        cx = [-1.9 + k * 1.6 for k in range(5)]
        H = VGroup(*[T(t, 24, INK, BOLD if t == "cold" else NORMAL).move_to([x, 2.15, 0]) for t, x in zip(TK, cx)])
        def cell(s, x, y, fill="#F3F4F6"):
            return tok(s, INK, w=1.3, h=0.5, size=24, fill=fill).move_to([x, y, 0])
        ry = [1.35, 0.55, -0.25, -1.15]
        labels = ["score for “cold”", "distance to “cold”", "penalty: 0.25 × distance", "new score"]
        RL = VGroup(*[T(s, 22, INK, BOLD if i == 3 else NORMAL).move_to([-2.9, y, 0], aligned_edge=RIGHT) for i, (s, y) in enumerate(zip(labels, ry))])
        r1 = VGroup(*[cell(v, x, ry[0], "#FEF3C7") for v, x in zip(SC, cx)])
        r2 = VGroup(*[cell(v, x, ry[1]) for v, x in zip(DIST, cx)])
        r3 = VGroup(*[cell(v, x, ry[2], "#FFEDD5") for v, x in zip(PEN, cx)])
        r4 = VGroup(*[cell(v, x, ry[3], "#FDE68A") for v, x in zip(NEW, cx)])
        mline = Line([cx[0] - 0.7, (ry[2] + ry[3]) / 2, 0], [cx[4] + 0.7, (ry[2] + ry[3]) / 2, 0], color=INK, stroke_width=2)
        self.play(FadeIn(H), FadeIn(RL[0]), LaggedStart(*[FadeIn(c) for c in r1], lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(RL[1]), LaggedStart(*[FadeIn(c) for c in r2], lag_ratio=0.1), run_time=0.9)
        self.play(FadeIn(RL[2]), LaggedStart(*[FadeIn(c) for c in r3], lag_ratio=0.1), run_time=0.9)
        self.play(Create(mline), FadeIn(RL[3]), LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in r4], lag_ratio=0.15), run_time=1.2)
        self.rest(3.0)
        # 7. weights before and after
        self.cap("Nearby tokens gain weight; distant tokens lose it.", hold=0)
        self.play(*[FadeOut(x) for x in (H, RL, r1, r2, r3, r4, mline)], run_time=0.6)
        ys = [1.4, 0.7, 0.0, -0.7, -1.4]
        def chart(ws, lx, head, col):
            lab = VGroup(*[T(t, 22, INK if t == "cold" else GREY, BOLD if t == "cold" else NORMAL).move_to([lx, y, 0], aligned_edge=RIGHT) for t, y in zip(TK, ys)])
            bars = VGroup(*[Rectangle(width=max(5.0 * w, 0.04), height=0.42, stroke_width=0, fill_color=col, fill_opacity=1).move_to([lx + 0.2, y, 0], aligned_edge=LEFT) for w, y in zip(ws, ys)])
            nums = VGroup(*[T(f"{w:.2f}", 22, INK, BOLD).next_to(b, RIGHT, buff=0.12) for w, b in zip(ws, bars)])
            hd = T(head, 24, INK, BOLD).move_to([lx + 1.2, 2.2, 0])
            return VGroup(hd, lab, bars, nums)
        C0 = chart(W0, -4.9, "without ALiBi", "#D1D5DB"); C1 = chart(W1, 1.2, "with ALiBi (slope 0.25)", AMB)
        self.play(FadeIn(C0[0]), FadeIn(C0[1]), LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(C0[2], C0[3])], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(C1[0]), FadeIn(C1[1]), LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(C1[2], C1[3])], lag_ratio=0.15), run_time=1.2)
        self.rest(3.0)
        # 8. today
        self.cap("Today: RoPE in nearly every open LLM.", hold=0)
        self.play(FadeOut(C0), FadeOut(C1), run_time=0.6)
        def chip(s, col=INK, fill="#F3F4F6"):
            return tok(s, col, w=0.2 * len(s) + 0.7, h=0.6, size=26, fill=fill)
        l1 = T("RoPE in open LLMs:", 24, INK, BOLD).move_to([-6.3, 1.5, 0], aligned_edge=LEFT)
        c1 = VGroup(*[chip(s) for s in ("Llama", "Qwen", "DeepSeek", "Gemma")]).arrange(RIGHT, buff=0.25).next_to(l1, RIGHT, buff=0.4)
        l2 = T("and in newer encoders:", 24, INK, BOLD).move_to([-6.3, 0.3, 0], aligned_edge=LEFT)
        c2 = chip("ModernBERT").next_to(l2, RIGHT, buff=0.4)
        l3 = T("Longer records than in training: stretch the rotation angles after pretraining.", 24, INK).move_to([-6.3, -1.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(l1), LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in c1], lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(l2), FadeIn(c2, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(l3), run_time=0.6)
        self.rest(3.2)
