from kit import *
LC = PC                                            # LoRA matrices (purple)
WF = "#CBD5E1"                                     # frozen weights (grey-blue)
def mrect(w, h, fill, label, size=22, color=INK):
    """A matrix drawn as a rectangle with a centered label."""
    r = Rectangle(width=w, height=h, stroke_color=INK, stroke_width=2, fill_color=fill, fill_opacity=1)
    return VGroup(r, T(label, size, color, BOLD).move_to(r))
def line(*parts):
    """A row of text pieces: (text, size, color, weight)."""
    return VGroup(*[T(s, z, c, w) for s, z, c, w in parts]).arrange(RIGHT, buff=0.15)
class C2(Clip):
    TITLE = "LoRA: fine-tuning with a small fraction of the weights"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. the cost of full fine-tuning
        self.cap("Full fine-tuning with Adam stores about 16 bytes for every parameter.", hold=0)
        parts = [("weights", 4, "#94A3B8"), ("gradients", 4, "#CBD5E1"), ("Adam state m", 4, "#DDD6FE"), ("Adam state v", 4, "#DDD6FE")]
        bars = VGroup(*[mrect(2.6, 0.75, f, n, 22) for n, b, f in parts]).arrange(RIGHT, buff=0).move_to([0, 1.2, 0])
        bt = T("one parameter in fp32 = 16 bytes", 24, INK, BOLD).next_to(bars, UP, buff=0.3)
        bb = VGroup(*[T("4 bytes", 20, GREY).next_to(b, DOWN, buff=0.12) for b in bars]); bars.add(*bb)
        self.play(FadeIn(bt), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.3), run_time=1.6)
        c1 = line(("Qwen3-0.6B:", 26, INK, NORMAL), ("0.6B × 16 bytes ≈ 10 GB", 26, INK, BOLD))
        c2 = line(("A 70B model:", 26, INK, NORMAL), ("70B × 16 bytes ≈ 1,120 GB", 26, INK, BOLD))
        cc = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.55, 0])
        nn_ = T("before counting activations", 20, GREY).next_to(cc, DOWN, buff=0.3).align_to(cc, LEFT)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(c2, shift=UP * 0.1), FadeIn(nn_), run_time=0.7)
        self.rest(2.6)
        # 2. one query projection, frozen
        self.cap("In Qwen3-0.6B, one query projection W has 2,048 × 1,024 weights.", hold=0)
        self.play(*[FadeOut(m) for m in (bars, bt, cc, nn_)], run_time=0.5)
        W = mrect(1.8, 3.6, WF, "W", 30).move_to([-4.6, 0.45, 0])
        wl = VGroup(T("2,048 × 1,024", 22, INK, BOLD), T("= 2,097,152 weights", 22, INK)).arrange(DOWN, buff=0.1).next_to(W, DOWN, buff=0.2)
        x = mrect(0.4, 1.8, "#E2E8F0", "x", 22).move_to([-2.8, 0.45, 0])
        xl = T("token\n1,024", 18, GREY).next_to(x, DOWN, buff=0.15)
        self.play(FadeIn(W), FadeIn(wl), run_time=0.8)
        self.play(FadeIn(x), FadeIn(xl), run_time=0.5)
        fr = T("frozen: never updated", 22, GREY, BOLD).next_to(wl, DOWN, buff=0.15)
        self.play(W[0].animate.set_fill("#E5E7EB"), FadeIn(fr), run_time=0.7)
        self.rest(2.4)
        # 3. LoRA adds B·A beside W
        self.cap("LoRA adds two thin matrices, B and A, beside the frozen W.", hold=0)
        B = mrect(0.32, 3.6, LC, "", 20).move_to([-1.3, 0.45, 0])
        A = mrect(2.0, 0.32, LC, "", 20).next_to(B, RIGHT, buff=0.35).align_to(B, UP)
        bl = VGroup(T("B", 26, LC, BOLD), T("2,048 × 8", 20, INK)).arrange(DOWN, buff=0.08).next_to(B, DOWN, buff=0.2)
        al = VGroup(T("A", 26, LC, BOLD), T("8 × 1,024", 20, INK)).arrange(DOWN, buff=0.08).next_to(A, DOWN, buff=0.15)
        rk = T("rank r = 8", 22, LC, BOLD).next_to(al, DOWN, buff=0.25)
        self.play(GrowFromEdge(B, UP), FadeIn(bl), run_time=0.8)
        self.play(GrowFromEdge(A, LEFT), FadeIn(al), FadeIn(rk), run_time=0.8)
        f = line(("output =", 28, INK, NORMAL), ("W·x", 28, GREY, BOLD), ("+", 28, INK, NORMAL), ("B·A·x", 28, LC, BOLD)).move_to([1.9, 1.75, 0], aligned_edge=LEFT)
        self.play(FadeIn(f, shift=UP * 0.1), run_time=0.8)
        self.rest(2.4)
        # 4. how many weights LoRA trains here
        self.cap("B and A together have 24,576 weights, about 1.2% of W.", hold=0)
        self.play(FadeOut(rk), run_time=0.4)
        cnt = VGroup(line(("B:", 24, LC, BOLD), ("2,048 × 8 = 16,384", 24, INK, NORMAL)),
                     line(("A:", 24, LC, BOLD), ("8 × 1,024 = 8,192", 24, INK, NORMAL)),
                     line(("trained:", 24, INK, BOLD), ("24,576", 24, LC, BOLD)),
                     line(("frozen W:", 24, INK, BOLD), ("2,097,152", 24, GREY, BOLD)),
                     T("24,576 ÷ 2,097,152 ≈ 1.2%", 24, INK, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([1.9, 0.9, 0], aligned_edge=UL)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cnt], lag_ratio=0.3), run_time=1.8)
        self.rest(2.6)
        # 5. B starts at zero
        self.cap("B starts at zero, so training starts exactly from the original model.", hold=0)
        self.play(FadeOut(cnt), run_time=0.4)
        zs = VGroup(*[T("0", 18, INK, BOLD).move_to(B[0].get_top() + DOWN * (0.27 + 0.437 * i)) for i in range(8)])
        self.play(B[0].animate.set_fill(WHITE), FadeIn(zs), run_time=0.8)
        z = VGroup(T("B = 0, so B·A·x = 0", 26, INK, BOLD), T("output = W·x:", 26, INK), T("exactly the original model", 26, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([1.9, 0.9, 0], aligned_edge=UL)
        g = T("training then updates only B and A", 20, LC, BOLD).next_to(z, DOWN, buff=0.3).align_to(z, LEFT)
        self.play(FadeIn(z[0]), run_time=0.6)
        self.play(FadeIn(z[1:]), run_time=0.6)
        self.play(FadeIn(g), run_time=0.5)
        self.rest(2.4)
        # 6. all 28 layers
        self.cap("Across all 28 layers, LoRA trains 2,293,760 weights, about 0.4% of the model.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.5)
        hdr = ["projection", "W shape", "LoRA weights (r = 8)"]
        data = [("query", "2,048 × 1,024", "24,576"), ("key", "1,024 × 1,024", "16,384"), ("value", "1,024 × 1,024", "16,384"), ("output", "1,024 × 2,048", "24,576")]
        xs = [-5.2, -2.2, 1.4]
        rows = VGroup(VGroup(*[T(h, 22, GREY, BOLD).move_to([x, 2.1, 0], aligned_edge=LEFT) for h, x in zip(hdr, xs)]))
        for i, r in enumerate(data):
            rows.add(VGroup(*[T(c, 24, LC if j == 2 else INK, BOLD if j == 2 else NORMAL).move_to([x, 1.45 - 0.55 * i, 0], aligned_edge=LEFT) for j, (c, x) in enumerate(zip(r, xs))]))
        rule = Line([-5.2, -0.9, 0], [4.6, -0.9, 0], stroke_color=GREY, stroke_width=2)
        tot = VGroup(T("per layer", 24, INK).move_to([-5.2, -1.3, 0], aligned_edge=LEFT), T("81,920", 24, LC, BOLD).move_to([1.4, -1.3, 0], aligned_edge=LEFT),
                     T("× 28 layers", 24, INK).move_to([-5.2, -1.9, 0], aligned_edge=LEFT), T("2,293,760", 26, LC, BOLD).move_to([1.4, -1.9, 0], aligned_edge=LEFT))
        pc = T("of 596M ≈ 0.4%", 24, INK, BOLD).next_to(tot[3], RIGHT, buff=0.35)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in rows], lag_ratio=0.2), run_time=1.6)
        self.play(Create(rule), FadeIn(tot[:2]), run_time=0.7)
        self.play(FadeIn(tot[2:]), run_time=0.7)
        self.play(FadeIn(pc), run_time=0.5)
        self.rest(2.6)
        # 7. one frozen model, one small adapter per task
        self.cap("One frozen model can carry a small adapter for each clinical task.", hold=0)
        self.play(*[FadeOut(m) for m in (rows, rule, tot, pc)], run_time=0.5)
        base = box("Qwen3-0.6B, frozen\n1.2 GB in bf16", 4.0, 1.4, "#E5E7EB", 24).move_to([-3.6, 0.2, 0])
        tasks = ["discharge summaries", "radiology impressions", "medication questions"]
        ad = VGroup(*[box(f"adapter: {t}\n4.6 MB", 4.4, 0.95, "#EDE9FE", 21, stroke=LC) for t in tasks]).arrange(DOWN, buff=0.3).move_to([2.9, 0.2, 0])
        ar = VGroup(*[Arrow(base.get_right(), a.get_left(), buff=0.1, stroke_width=3, color=LC, max_tip_length_to_length_ratio=0.08) for a in ad])
        nt = T("2,293,760 weights × 2 bytes ≈ 4.6 MB per adapter", 22, GREY).move_to([0, -2.3, 0])
        self.play(FadeIn(base), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d)) for a, d in zip(ar, ad)], lag_ratio=0.35), run_time=1.6)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.6)
