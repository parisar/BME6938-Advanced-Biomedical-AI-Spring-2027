from kit import *
# tokens from the real tokenizers (see the Week 4 notebook)
GPT2 = ["Pat", "ient", " denies", " chest", " pain", ";", " trop", "on", "in", " negative", ";", " EC", "G", " shows", " sin", "us", " t", "achy", "card", "ia", "."]
DSV3 = ["Patient", " denies", " chest", " pain", ";", " trop", "onin", " negative", ";", " ECG", " shows", " sinus", " tachycardia", "."]
SPLIT = "#FDE68A"                                  # highlight for words cut into pieces
def chips(pieces, y, hl):
    # One chip per token, wrapped to fit the frame; pieces of a split word are highlighted.
    out = VGroup(); x, row = -6.2, 0
    for i, p in enumerate(pieces):
        s = p.strip() or "␣"
        c = tok(s, INK, w=0.16 * len(s) + 0.42, h=0.5, size=20, fill=(SPLIT if i in hl else "#F3F4F6"))
        if x + c.width > 6.4: x, row = -6.2, row + 1
        c.move_to([x + c.width / 2, y - 0.62 * row, 0]); x += c.width + 0.08; out.add(c)
    return out
class C4(Clip):
    TITLE = "More 2026 changes"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. bigger vocabularies
        self.cap("Bigger vocabularies: the same clinical note in fewer tokens.", hold=0)
        s = T("“Patient denies chest pain; troponin negative; ECG shows sinus tachycardia.”", 24, INK).move_to([0, 2.55, 0])
        h1 = T("GPT-2 (2019): 50,257 tokens in its vocabulary → 21 tokens", 22, INK, BOLD).move_to([-6.2, 1.75, 0], aligned_edge=LEFT)
        c1 = chips(GPT2, 1.15, {0, 1, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 19})
        h2 = T("DeepSeek-V3 (2024): about 129,000 tokens in its vocabulary → 14 tokens", 22, INK, BOLD).move_to([-6.2, -0.4, 0], aligned_edge=LEFT)
        c2 = chips(DSV3, -1.0, {5, 6})
        c2[12][0].set_fill("#BBF7D0", 1)                          # "tachycardia" is one token here
        nt = T("“tachycardia”: 4 pieces in GPT-2, 1 token in DeepSeek-V3", 22, GREY).move_to([0, -2.4, 0])
        self.play(FadeIn(s), run_time=0.6)
        self.play(FadeIn(h1), LaggedStart(*[FadeIn(c) for c in c1], lag_ratio=0.04), run_time=1.4)
        self.play(FadeIn(h2), LaggedStart(*[FadeIn(c) for c in c2], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(nt), Indicate(VGroup(*c1[16:20]), color=AMB), Indicate(c2[12], color=AMB), run_time=1.0)
        self.rest(2.4)
        # 2. longer context: stretch the RoPE angles
        self.cap("Longer context: train on short text, then stretch the RoPE angles.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.6)
        x0, xs, x8 = -6.0, -4.5, 6.0                                    # angle 0, end of training range, 8 times further
        ax = Line([x0, 1.0, 0], [x8, 1.0, 0], stroke_width=6, color="#E5E7EB")
        seen = Line([x0, 1.0, 0], [xs, 1.0, 0], stroke_width=14, color=KC)
        hd = T("rotation angle of the slowest RoPE pair", 22, INK, BOLD).move_to([x0, 1.8, 0], aligned_edge=LEFT)
        l0 = T("0", 20, GREY).move_to([x0, 0.55, 0]); l4 = T("4,096", 20, KC, BOLD).move_to([xs, 0.55, 0])
        sl = T("seen in training", 20, KC, BOLD).move_to([(x0 + xs) / 2, 1.35, 0])
        self.play(Create(ax), FadeIn(hd), FadeIn(l0), run_time=0.7)
        self.play(Create(seen), FadeIn(l4), FadeIn(sl), run_time=0.8)
        RED = "#B91C1C"
        far = Line([xs, 1.0, 0], [x8, 1.0, 0], stroke_width=14, color=RED).set_opacity(0.35)
        mk = Dot([x8, 1.0, 0], radius=0.14, color=RED)
        l32 = T("position 32,768: angles never seen", 20, RED, BOLD).move_to([x8, 0.55, 0], aligned_edge=RIGHT)
        self.play(Create(far), FadeIn(mk), FadeIn(l32), run_time=1.0)
        t1 = T("Stretch: rotate 8 times slower, so position 32,768 lands where 4,096 was", 22, INK).move_to([0, -0.6, 0])
        self.play(FadeIn(t1), run_time=0.6)
        l32b = T("32,768", 20, KC, BOLD).move_to([xs, 0.1, 0])
        self.play(mk.animate.move_to([xs, 1.0, 0]).set_color(KC), FadeOut(far), FadeOut(l32), FadeIn(l32b), run_time=1.4)
        t6 = T("DeepSeek-V3: trained at 4K tokens, stretched to 32K, then 128K", 22, INK, BOLD).move_to([0, -1.6, 0])
        t7 = T("(YaRN, a refined version of this idea)", 20, GREY).next_to(t6, DOWN, buff=0.2)
        self.play(FadeIn(t6), FadeIn(t7), run_time=0.6)
        self.rest(2.4)
        # 3. multi-token prediction
        self.cap("Multi-token prediction: in training, also predict the token after next.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.6)
        ctx = VGroup(*[tok(w, INK, w=1.45, h=0.55, size=22) for w in ["The", "patient", "denies", "chest"]]).arrange(RIGHT, buff=0.12).move_to([-3.6, -1.7, 0])
        mdl = box("model", 6.2, 0.8, "#E0E7FF", 24, stroke=UF).move_to([-3.6, -0.5, 0])
        h1 = box("next-token head", 2.9, 0.6, "#DCFCE7", 20).move_to([-5.2, 0.85, 0]); h2 = box("extra prediction module", 3.4, 0.6, "#FEF3C7", 20).move_to([-1.75, 0.85, 0])
        o1 = tok("pain", INK, w=1.4, h=0.55, size=24, fill="#DCFCE7").move_to([-5.2, 2.05, 0]); o2 = tok("and", INK, w=1.4, h=0.55, size=24, fill="#FEF3C7").move_to([-1.75, 2.05, 0])
        l1 = T("next token", 20, GREY).next_to(o1, RIGHT, buff=0.15); l2 = T("token after next", 20, GREY).next_to(o2, RIGHT, buff=0.15)
        A = VGroup(*[Arrow(a.get_top(), b.get_bottom(), buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3) for a, b in ((ctx, mdl), (h1, o1), (h2, o2))],
                   Arrow(mdl.get_top() + LEFT * 1.6, h1.get_bottom(), buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3),
                   Arrow(mdl.get_top() + RIGHT * 1.85, h2.get_bottom(), buff=0.06, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.3))
        self.play(FadeIn(ctx), FadeIn(mdl), FadeIn(A[0]), run_time=0.8)
        self.play(FadeIn(h1), FadeIn(A[3]), run_time=0.5)
        self.play(FadeIn(A[1]), FadeIn(o1), FadeIn(l1), run_time=0.6)
        self.play(FadeIn(h2), FadeIn(A[4]), run_time=0.5)
        self.play(FadeIn(A[2]), FadeIn(o2), FadeIn(l2), run_time=0.6)
        nt = VGroup(T("DeepSeek-V3: one extra module", 22, INK, BOLD), T("more training signal per token", 22, INK), T("it can also speed up generation", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.1, -0.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(2.4)
        # 4. MedGemma
        self.cap("MedGemma: Gemma 3 adapted to medical text and images.", hold=0)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.6)
        g = box("Gemma 3", 2.6, 1.0, "#E0E7FF", 26, stroke=UF).move_to([-4.6, 0.5, 0])
        d = VGroup(T("+ medical text", 22, INK), T("+ medical images", 22, INK), T("(radiology, pathology,", 20, GREY), T("dermatology, ophthalmology)", 20, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-1.0, 0.5, 0])
        m = box("MedGemma", 2.8, 1.0, "#DCFCE7", 26, stroke=KC).move_to([3.4, 0.5, 0])
        a1 = Arrow(g.get_right(), d.get_left(), buff=0.25, stroke_width=4, color=GREY); a2 = Arrow(d.get_right(), m.get_left(), buff=0.25, stroke_width=4, color=GREY)
        sz = T("4B and 27B versions", 22, INK, BOLD).next_to(m, DOWN, buff=0.3)
        pp = T("Built from the pieces in these clips: RoPE, grouped-query attention, sliding windows", 22, GREY).move_to([0, -1.9, 0])
        self.play(FadeIn(g), run_time=0.5)
        self.play(GrowArrow(a1), FadeIn(d), run_time=0.9)
        self.play(GrowArrow(a2), FadeIn(m), FadeIn(sz), run_time=0.9)
        self.play(FadeIn(pp), run_time=0.6)
        self.rest(2.8)
