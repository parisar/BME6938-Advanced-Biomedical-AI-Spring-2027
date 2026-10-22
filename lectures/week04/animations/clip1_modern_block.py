from kit import *
NEW = "#B45309"                                    # highlight for what changed (amber)
LX, RX, NX = -5.2, -0.3, 2.0                      # 2017 column, 2026 column, notes panel (left edge)
def up(a, b):
    return Arrow(a.get_top(), b.get_bottom(), buff=0.04, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.35)
def plus(y):
    c = Circle(0.2, stroke_color=INK, stroke_width=2.5, fill_color=WHITE, fill_opacity=1).move_to([RX, y, 0])
    return VGroup(c, T("+", 24, INK, BOLD).move_to(c))
def note(*lines):
    return VGroup(*[T(s, 22, INK if i else NEW, BOLD if i == 0 else NORMAL) for i, s in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([NX, 1.6, 0], aligned_edge=UL)
class C1(Clip):
    TITLE = "What changed since 2017"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. both blocks: same overall shape
        self.cap("A 2026 LLM is still a stack of decoder blocks, like the 2017 transformer.", hold=0)
        W, WL = 4.2, 3.3                              # widths of the 2026 and 2017 boxes
        L = [box("token + position", WL, 0.55, "#E2E8F0", 20).move_to([LX, -2.55, 0]),
             box("Masked self-attention", WL, 0.55, "#FDE68A", 20).move_to([LX, -1.5, 0]),
             box("Add & LayerNorm", WL, 0.55, "#FEF9C3", 20).move_to([LX, -0.6, 0]),
             box("Feed-forward (ReLU)", WL, 0.55, "#BFDBFE", 20).move_to([LX, 0.3, 0]),
             box("Add & LayerNorm", WL, 0.55, "#FEF9C3", 20).move_to([LX, 1.2, 0])]
        LA = VGroup(*[up(a, b) for a, b in zip(L, L[1:])])
        lh = T("2017 transformer", 24, INK, BOLD).move_to([LX, 2.75, 0])
        tok_r = box("token", W, 0.55, "#E2E8F0", 20).move_to([RX, -2.55, 0])
        n1 = box("RMSNorm", W, 0.5, "#FEF9C3", 20).move_to([RX, -1.85, 0])
        att = box("Multi-head attention", W, 0.55, "#FDE68A", 20).move_to([RX, -1.15, 0])
        p1 = plus(-0.45)
        n2 = box("RMSNorm", W, 0.5, "#FEF9C3", 20).move_to([RX, 0.2, 0])
        ffn = box("Feed-forward", W, 0.55, "#BFDBFE", 20).move_to([RX, 0.9, 0])
        p2 = plus(1.6)
        R = [tok_r, n1, att, p1, n2, ffn, p2]
        RA = VGroup(*[up(a, b) for a, b in zip(R, R[1:])])
        rh = T("2026 LLM (Llama, Qwen, Gemma)", 24, INK, BOLD).move_to([RX, 2.75, 0])
        self.play(FadeIn(lh), LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in L], lag_ratio=0.15), FadeIn(LA), run_time=1.4)
        self.play(FadeIn(rh), LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in R], lag_ratio=0.12), FadeIn(RA), run_time=1.4)
        same = note("Same shape", "attention, then feed-forward,", "each with a residual add")
        self.play(FadeIn(same), run_time=0.6)
        self.rest(2.4)
        # 2. pre-norm with RMSNorm
        self.cap("Normalization moves before each sublayer and becomes RMSNorm.", hold=0)
        h_old = VGroup(*[SurroundingRectangle(L[i], color=NEW, buff=0.06, stroke_width=3) for i in (2, 4)])
        h_new = VGroup(*[SurroundingRectangle(m, color=NEW, buff=0.06, stroke_width=4) for m in (n1, n2)])
        nt = note("Normalization", "now before each sublayer", "(pre-norm)", "RMSNorm: rescale by the", "root mean square only")
        self.play(FadeOut(same), Create(h_old), run_time=0.6)
        self.play(TransformFromCopy(h_old, h_new), FadeIn(nt), run_time=1.0)
        self.rest(2.4)
        # 3. SwiGLU feed-forward
        self.cap("The feed-forward network becomes SwiGLU, a gated version.", hold=0)
        ffn2 = box("SwiGLU feed-forward", W, 0.55, "#BFDBFE", 20).move_to(ffn)
        hf_old = SurroundingRectangle(L[3], color=NEW, buff=0.06, stroke_width=3)
        hf = SurroundingRectangle(ffn2, color=NEW, buff=0.06, stroke_width=4)
        nt2 = note("SwiGLU", "two projections of the token;", "one, through SiLU, gates", "the other", "gate = SiLU(x·W1)", "out = (gate × x·W3)·W2")
        self.play(FadeOut(h_old), FadeOut(h_new), FadeOut(nt), Create(hf_old), run_time=0.6)
        self.play(FadeTransform(ffn, ffn2), Create(hf), FadeIn(nt2), run_time=1.0)
        self.rest(2.4)
        # 4. RoPE inside attention
        self.cap("Positions move inside attention: RoPE rotates each query and key.", hold=0)
        hp_old = SurroundingRectangle(L[0], color=NEW, buff=0.06, stroke_width=3)
        att2 = box("Multi-head attention + RoPE", W, 0.55, "#FDE68A", 20).move_to(att)
        ha = SurroundingRectangle(att2, color=NEW, buff=0.06, stroke_width=4)
        nt3 = note("RoPE", "no position vector at input;", "queries and keys are rotated", "in every attention layer", "(Week 2, clip 4)")
        self.play(FadeOut(hf_old), FadeOut(hf), FadeOut(nt2), Create(hp_old), run_time=0.6)
        self.play(FadeTransform(att, att2), Create(ha), FadeIn(nt3), run_time=1.0)
        self.rest(2.4)
        # 5. grouped-query attention
        self.cap("Attention becomes grouped-query attention: query heads share keys and values.", hold=0)
        att3 = box("Grouped-query attention + RoPE", W, 0.55, "#FDE68A", 20).move_to(att)
        nt4 = note("Grouped-query attention", "SmolLM2-360M: 15 query heads", "share 5 key/value heads").move_to([NX, 1.6, 0], aligned_edge=UL)
        qh = VGroup(*[Square(0.2, stroke_width=0, fill_color=QC, fill_opacity=0.85) for _ in range(15)]).arrange(RIGHT, buff=0.05).move_to([NX, -0.75, 0], aligned_edge=LEFT)
        kv = VGroup(*[VGroup(Square(0.2, stroke_width=0, fill_color=KC, fill_opacity=0.85), Square(0.2, stroke_width=0, fill_color=VC, fill_opacity=0.85)).arrange(RIGHT, buff=0.02) for _ in range(5)])
        for g in range(5): kv[g].move_to([qh[3 * g + 1].get_x(), -1.8, 0])   # 3 queries per group
        lk = VGroup(*[Line(qh[i].get_bottom(), kv[i // 3].get_top(), stroke_width=2, color=GREY) for i in range(15)])
        ql = T("15 query heads", 20, QC, BOLD).next_to(qh, UP, buff=0.15).align_to(qh, LEFT)
        kl = T("5 key/value heads", 20, KC, BOLD).next_to(kv, DOWN, buff=0.15).align_to(qh, LEFT)
        self.play(FadeOut(hp_old), FadeOut(nt3), run_time=0.5)
        self.play(FadeTransform(att2, att3), FadeIn(nt4), run_time=0.8)
        self.play(FadeIn(qh), FadeIn(ql), run_time=0.6)
        self.play(Create(lk), FadeIn(kv), FadeIn(kl), run_time=1.2)
        self.rest(2.2)
        # 6. still a stack of blocks
        self.cap("The shape is unchanged: stack the blocks, then predict the next token.", hold=0)
        self.play(*[FadeOut(m) for m in (ha, nt4, qh, kv, lk, ql, kl)], run_time=0.6)
        bl = SurroundingRectangle(VGroup(*L[1:]), color=GREY, buff=0.12, stroke_width=2)
        br = SurroundingRectangle(VGroup(*R[1:]), color=GREY, buff=0.12, stroke_width=2)
        ol = box("next token", 2.0, 0.5, "#DCFCE7", 20).move_to([LX - 0.6, 2.15, 0]); orr = box("next token", 2.0, 0.5, "#DCFCE7", 20).move_to([RX - 0.8, 2.15, 0])
        xl = T("× 6 blocks", 24, UF, BOLD).next_to(ol, RIGHT, buff=0.25)
        xr = T("× 32 blocks (SmolLM2-360M)", 24, UF, BOLD).next_to(orr, RIGHT, buff=0.25)
        self.play(Create(bl), Create(br), FadeIn(xl), FadeIn(xr), run_time=1.0)
        self.play(FadeIn(ol, shift=UP * 0.1), FadeIn(orr, shift=UP * 0.1), Create(up(VGroup(L[4]).copy().set_x(ol.get_x()), ol)), Create(up(VGroup(p2).copy().set_x(orr.get_x()), orr)), run_time=0.8)
        nt5 = note("Same recipe", "trains more stably", "and runs more cheaply").move_to([NX + 0.2, 0.9, 0], aligned_edge=UL)
        self.play(FadeIn(nt5), run_time=0.6)
        self.rest(2.6)
