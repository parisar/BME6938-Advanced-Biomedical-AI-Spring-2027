from kit import *
class C4(Clip):
    TITLE = "Encoder versus decoder, and masking"
    def construct(self):
        enc = box("Encoder", 3.7, 1.7, "#DBEAFE", size=32, stroke=UF).move_to(LEFT * 3.9 + UP * 0.35)
        dec = box("Decoder", 3.7, 1.7, "#FCE7F3", size=32, stroke="#BE185D").move_to(RIGHT * 3.7 + UP * 0.35)
        src = VGroup(*[tok(t, w=1.08, h=0.58, size=23) for t in TOK]).arrange(RIGHT, buff=0.1).next_to(enc, DOWN, buff=0.6)
        ain = VGroup(*[Arrow(s.get_top(), [s.get_center()[0], enc.get_bottom()[1], 0], buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3) for s in src])
        self.play(FadeIn(enc), FadeIn(src), *[GrowArrow(a) for a in ain])
        mem = VGroup(*[mat(1, 3, KC, cell=0.3, seed=70 + i)[0] for i in range(4)]).arrange(RIGHT, buff=0.24).next_to(enc, UP, buff=0.55)
        aout = VGroup(*[Arrow([m.get_center()[0], enc.get_top()[1], 0], m.get_bottom(), buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3) for m in mem])
        meml = T("encoder output: one vector per token", 22, "#15803D", BOLD).next_to(mem, UP, buff=0.18)
        self.play(*[GrowArrow(a) for a in aout], FadeIn(mem), FadeIn(meml))
        self.cap("The encoder reads the whole input at once. Every token attends to every other token.", hold=3.6)
        # decoder generates
        self.play(FadeIn(dec))
        out_words = ["Me", "llamo", "John"]; ins = ["<start>", "Me", "llamo"]
        xs = [dec.get_center()[0] - 1.3, dec.get_center()[0], dec.get_center()[0] + 1.3]
        din = VGroup(); dout = VGroup()
        self.cap("The decoder writes the output one token at a time.", hold=1.2)
        for i in range(3):
            a = tok(ins[i], "#BE185D", w=1.2, h=0.58, size=21, fill="#FDF2F8").move_to([xs[i], dec.get_bottom()[1] - 0.89, 0])
            ar = Arrow(a.get_top(), [xs[i], dec.get_bottom()[1], 0], buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3)
            b = tok(out_words[i], "#BE185D", w=1.2, h=0.58, size=23, fill="#FBCFE8").move_to([xs[i], dec.get_top()[1] + 0.89, 0])
            br = Arrow([xs[i], dec.get_top()[1], 0], b.get_bottom(), buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3)
            self.play(FadeIn(a, shift=UP * 0.15), GrowArrow(ar), run_time=0.5)
            self.play(GrowArrow(br), FadeIn(b, shift=UP * 0.15), run_time=0.5)
            din.add(VGroup(a, ar)); dout.add(VGroup(b, br))
            if i < 2:
                ghost = b[0].copy().set_stroke(AMB, 4)
                self.play(ghost.animate.move_to([xs[i + 1], dec.get_bottom()[1] - 0.89, 0]), run_time=0.6); self.play(FadeOut(ghost), run_time=0.15)
        self.cap("Each predicted token is fed back in as the next decoder input.", hold=3.2)
        # cross-attention
        ca = VGroup(*[Line(dec.get_left() + UP * 0.2, m.get_right() + RIGHT * 0.02 if i == 3 else m.get_top() + UP * 0.02, color=AMB, stroke_width=3) for i, m in enumerate(mem)])
        ca = CurvedArrow(dec.get_left() + UP * 0.25, mem.get_right() + RIGHT * 0.15, angle=0.7, color=AMB, stroke_width=5)
        cal = T("cross-attention", 24, "#B45309", BOLD).move_to((enc.get_right() + dec.get_left()) / 2 + DOWN * 0.25)
        self.play(Create(ca), FadeIn(cal))
        self.cap("Cross-attention: queries come from the decoder; keys and values come from the encoder output.", hold=4.2)
        # masking
        allm = VGroup(enc, src, ain, mem, aout, meml, dec, din, dout, ca, cal)
        self.play(FadeOut(allm), run_time=0.7)
        dl = ["Me", "llamo", "John"]
        raw = [[0.9, 0.5, 0.3], [0.7, 0.3, 0.6], [0.8, 0.02, 0.33]]
        H0 = heat([[0.55, 0.3, 0.15], [0.42, 0.28, 0.3], [0.48, 0.22, 0.3]], cell=1.05, color="#BE185D", size=24, labels_r=dl, labels_c=dl).move_to(LEFT * 3.6 + UP * 0.3)
        t0 = T("Decoder self-attention scores", 24, INK, BOLD).next_to(H0, UP, buff=0.3)
        self.play(FadeIn(H0), FadeIn(t0))
        self.cap("Problem: while training, the decoder could look ahead at the words it is supposed to predict.", hold=3.6)
        mask = [[False, True, True], [False, False, True], [False, False, False]]
        covers = VGroup()
        for i in range(3):
            for j in range(3):
                if mask[i][j]:
                    sq = Square(1.05, stroke_color=WHITE, stroke_width=2, fill_color=INK, fill_opacity=1).move_to(H0[0][i * 3 + j])
                    covers.add(VGroup(sq, T("−∞", 26, WHITE, BOLD).move_to(sq)))
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in covers], lag_ratio=0.25), run_time=1.2)
        self.cap("Masking: scores for future positions are set to −∞ before the softmax.", hold=3.2)
        H1 = heat([[1, 0, 0], [0.6, 0.4, 0], [0.48, 0.22, 0.3]], cell=1.05, color="#BE185D", size=24, labels_r=dl, labels_c=dl).move_to(RIGHT * 3.6 + UP * 0.3)
        t1 = T("After softmax", 24, INK, BOLD).next_to(H1, UP, buff=0.3)
        ar = Arrow(H0.get_right() + RIGHT * 0.1, H1.get_left() + LEFT * 0.1, buff=0.1, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.12)
        arl = T("softmax", 22, INK).next_to(ar, UP, buff=0.08)
        self.play(GrowArrow(ar), FadeIn(arl), FadeIn(H1), FadeIn(t1))
        self.cap("Future positions get weight 0, so each token attends only to itself and earlier tokens.", hold=4.0)
        # families
        self.play(*[FadeOut(m) for m in (H0, t0, covers, H1, t1, ar, arl)], run_time=0.7)
        fam = [("Encoder only", "sees the whole input", "used for understanding", "e.g. BERT", "#DBEAFE", UF),
               ("Decoder only", "masked, left to right", "used for generation", "e.g. GPT", "#FCE7F3", "#BE185D"),
               ("Encoder-decoder", "linked by cross-attention", "sequence to sequence", "e.g. T5", "#EDE9FE", "#6D28D9")]
        cards = VGroup()
        for n, a, b, e, f, sc in fam:
            r = RoundedRectangle(corner_radius=0.18, width=4.3, height=3.4, stroke_color=sc, stroke_width=3, fill_color=f, fill_opacity=1)
            tx = VGroup(T(n, 28, sc, BOLD), T(a, 22, INK), T(b, 22, INK), T(e, 22, GREY)).arrange(DOWN, buff=0.3).move_to(r)
            cards.add(VGroup(r, tx))
        cards.arrange(RIGHT, buff=0.25).move_to(UP * 0.3)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.35), run_time=1.8)
        self.cap("Three families of transformer models follow from these two parts.", hold=4.5)
