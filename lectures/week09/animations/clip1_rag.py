from kit import *
DOC, QU, THR = "#0F766E", PC, AMB                         # documents and chunks teal, the question purple, the threshold amber
FILLS = {DOC: "#CCFBF1", QU: "#EDE9FE", UF: "#E0E7FF", GREY: "#F3F4F6"}
def card(lines, color, size=22, pad=0.4, first=None):
    """Rounded card with one or more text lines; `first` colors the first line in bold."""
    tx = VGroup(*[T(s, size, first if (first and i == 0) else INK, BOLD if (first and i == 0) else NORMAL) for i, s in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    r = RoundedRectangle(corner_radius=0.12, width=tx.width + pad, height=tx.height + pad, stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, tx.move_to(r))
def chunk(s, w=3.9):
    return box(s, w, 0.55, FILLS[DOC], size=20, stroke=DOC)
def bars(rows, x0, scale, y0, gap=0.62, color=DOC):
    """Horizontal bars for (label, score) rows: label box ending at x0, bar starting at x0, score at the bar's end."""
    g = VGroup()
    for i, (lab, v) in enumerate(rows):
        y = y0 - i * gap
        c = chunk(lab).move_to([x0 - 2.1, y, 0])
        b = Rectangle(width=v * scale, height=0.4, stroke_width=0, fill_color=color, fill_opacity=0.75).move_to([x0 + v * scale / 2, y, 0])
        n = T(f"{v:.2f}", 22, WHITE, BOLD).move_to(b.get_left() + RIGHT * 0.42)
        g.add(VGroup(c, b, n))
    return g
X0, SC = -1.0, 6.2                                          # bar origin and length of a score of 1
class C1(Clip):
    TITLE = "Retrieval-augmented generation"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. the model alone
        self.cap("A model cannot know your hospital's own protocols.", hold=0)
        q = card(["Within how many hours must antibiotics start", "in our sepsis protocol?"], QU, 24).move_to([0, 2.0, 0])
        llm = box("language model alone", 4.4, 0.8, "#F3F4F6", size=24).move_to([0, 0.35, 0])
        a = card(["“3 hours”"], GREY, 28).move_to([0, -1.15, 0])
        n = T("a reasonable national figure, but not this hospital's rule", 22, GREY).move_to([0, -2.25, 0])
        a1, a2 = Arrow(q.get_bottom(), llm.get_top(), buff=0.1, color=GREY), Arrow(llm.get_bottom(), a.get_top(), buff=0.1, color=GREY)
        self.play(FadeIn(q, shift=DOWN * 0.1), run_time=0.7)
        self.play(GrowArrow(a1), FadeIn(llm), run_time=0.7)
        self.play(GrowArrow(a2), FadeIn(a, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(n), run_time=0.5)
        self.rest(2.6)
        # 2. chunks and embeddings
        self.cap("Split the documents into chunks and embed each chunk once.", hold=0)
        self.play(FadeOut(VGroup(q, llm, a, n, a1, a2)), run_time=0.6)
        docs = VGroup()
        for s in ["Sepsis protocol", "Potassium protocol", "Falls protocol"]:
            r = RoundedRectangle(corner_radius=0.08, width=2.95, height=0.95, stroke_color=DOC, stroke_width=2, fill_color=WHITE, fill_opacity=1)
            ln = VGroup(*[Line(LEFT * 0.9, RIGHT * (0.9 - 0.4 * k), color="#D1D5DB", stroke_width=3) for k in range(2)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            docs.add(VGroup(r, VGroup(T(s, 20, DOC, BOLD), ln).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(r)))
        docs.arrange(DOWN, buff=0.35).move_to([-5.25, 0.3, 0])
        names = ["Sepsis §1: screening", "Sepsis §2: antibiotics", "Sepsis §3: fluids", "Potassium §1: high values", "Falls §1: risk score"]
        ch = VGroup(*[chunk(s) for s in names]).arrange(DOWN, buff=0.18).move_to([-0.4, 0.3, 0])
        vs = VGroup(*[mat(1, 8, DOC, cell=0.36, seed=k) for k in range(5)])
        for v, c in zip(vs, ch): v.next_to(c, RIGHT, buff=1.0)
        ar = VGroup(*[Arrow(c.get_right(), v.get_left(), buff=0.12, color=GREY, max_tip_length_to_length_ratio=0.3) for c, v in zip(ch, vs)])
        hc = T("chunks", 22, DOC, BOLD).next_to(ch, UP, buff=0.25)
        hv = T("embeddings, computed once", 22, DOC, BOLD).next_to(vs, UP, buff=0.25)
        nt = T("Almanac: chunks of 1,000 tokens, 1,536 numbers per embedding", 22, GREY).move_to([0, -2.5, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=RIGHT * 0.1) for d in docs], lag_ratio=0.2), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in ch], lag_ratio=0.15), FadeIn(hc), run_time=1.2)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(r), FadeIn(v)) for r, v in zip(ar, vs)], lag_ratio=0.15), FadeIn(hv), run_time=1.2)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.4)
        # 3. cosine similarity
        self.cap("Embed the question and score every chunk by cosine similarity.", hold=0)
        self.play(FadeOut(VGroup(docs, ar, vs, hv, nt, hc)), run_time=0.6)
        qc = card(["Q: when must antibiotics start in our sepsis protocol?"], QU, 22).move_to([-2.2, 2.55, 0])
        qv = mat(1, 8, QU, cell=0.36, seed=11).next_to(qc, RIGHT, buff=0.5)
        self.play(FadeIn(qc), FadeIn(qv), run_time=0.7)
        scores = {"Sepsis §2: antibiotics": 0.86, "Sepsis §1: screening": 0.79, "Sepsis §3: fluids": 0.62, "Potassium §1: high values": 0.41, "Falls §1: risk score": 0.33}
        B = bars(list(scores.items()), X0, SC, 1.25)
        order = {s: i for i, s in enumerate(scores)}
        self.play(*[ch[k].animate.move_to(B[order[s]][0]) for k, s in enumerate(names)], run_time=1.0)
        self.remove(*ch); self.add(*[b[0] for b in B])
        self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in B], lag_ratio=0.15), run_time=1.4)
        il = T("scores are illustrative", 20, GREY).move_to([-3.1, -1.95, 0])
        self.play(FadeIn(il), run_time=0.4)
        self.rest(2.6)
        # 4. the threshold
        self.cap("Only chunks above a threshold pass: Almanac used λ = 0.83.", hold=0)
        xl = X0 + 0.83 * SC
        th = DashedLine([xl, 1.65, 0], [xl, -1.55, 0], color=THR, stroke_width=4)
        tl = T("λ = 0.83", 24, THR, BOLD).next_to(th.get_bottom(), RIGHT, buff=0.15)
        self.play(Create(th), FadeIn(tl), run_time=0.8)
        self.play(B[0][1].animate.set_fill(UF, 0.9), *[b[1].animate.set_fill("#9CA3AF", 1) for b in B[1:]],
                  *[b[0].animate.set_opacity(0.45) for b in B[1:]], run_time=0.8)
        ps = T("passes", 22, UF, BOLD).next_to(B[0][1], RIGHT, buff=0.25)
        self.play(FadeIn(ps), run_time=0.4)
        self.rest(2.8)
        # 5. nothing passes
        self.cap("If nothing passes, the published Almanac falls back on the model's own knowledge.", hold=0)
        self.play(FadeOut(VGroup(qc, qv, B, th, tl, ps, il)), run_time=0.6)
        q2 = card(["Q: do we have a protocol for rattlesnake bites?"], QU, 22).move_to([-2.6, 2.55, 0])
        q2v = mat(1, 8, QU, cell=0.36, seed=12).next_to(q2, RIGHT, buff=0.5)
        B2 = bars([("Falls §1: risk score", 0.71), ("Sepsis §3: fluids", 0.58), ("Potassium §1: high values", 0.52)], X0, SC, 1.3)
        th2 = DashedLine([xl, 1.65, 0], [xl, -0.15, 0], color=THR, stroke_width=4)
        tl2 = T("λ = 0.83", 22, THR, BOLD).next_to(th2.get_bottom(), RIGHT, buff=0.15)
        self.play(FadeIn(q2), FadeIn(q2v), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in B2], lag_ratio=0.2), Create(th2), FadeIn(tl2), run_time=1.3)
        o1 = card(["Published version (NEJM AI 2024)", "falls back on the model's own knowledge"], UF, 22, first=UF)
        o2 = card(["Preprint version (arXiv 2023)", "abstains: “not found in the sources”"], GREY, 22, first=GREY)
        VGroup(o1, o2).arrange(RIGHT, buff=0.6).move_to([0, -1.55, 0])
        self.play(FadeIn(o1, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(o2, shift=UP * 0.1), run_time=0.6)
        self.rest(3.0)
        # 6. grounded answer
        self.cap("The passing chunk goes into the prompt with its source, and the answer cites it.", hold=0)
        self.play(FadeOut(VGroup(q2, q2v, B2, th2, tl2, o1, o2)), run_time=0.6)
        pr = VGroup(T("Prompt", 22, GREY, BOLD),
                    VGroup(T("Source: Sepsis protocol, section 2", 22, DOC, BOLD), T("“Start antibiotics within 1 hour of recognizing sepsis.”", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                    T("Question: within how many hours must antibiotics start?", 22, QU)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        prr = RoundedRectangle(corner_radius=0.12, width=pr.width + 0.5, height=pr.height + 0.4, stroke_color=GREY, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        P = VGroup(prr, pr.move_to(prr)).move_to([0, 1.85, 0])
        llm = box("language model", 3.6, 0.7, "#F3F4F6", size=24).move_to([0, -0.3, 0])
        ans = card(["“Within 1 hour [Sepsis protocol, section 2]”"], UF, 26).move_to([0, -1.8, 0])
        sy = T("synthetic protocol", 20, GREY).next_to(ans, DOWN, buff=0.2)
        b1, b2 = Arrow(P.get_bottom(), llm.get_top(), buff=0.08, color=GREY), Arrow(llm.get_bottom(), ans.get_top(), buff=0.08, color=GREY)
        self.play(FadeIn(P, shift=DOWN * 0.1), run_time=0.8)
        self.play(GrowArrow(b1), FadeIn(llm), run_time=0.6)
        self.play(GrowArrow(b2), FadeIn(ans, shift=DOWN * 0.1), FadeIn(sy), run_time=0.7)
        self.rest(2.8)
        # 7. results
        self.cap("Almanac ranked first of four systems on 314 clinical questions.", hold=0)
        self.play(FadeOut(VGroup(P, llm, ans, sy, b1, b2)), run_time=0.6)
        cards = [("314", "clinical questions", "9 specialties, 10 clinician graders"), ("1st of 4", "factuality, completeness, preference", "vs ChatGPT-4, Bing, and Bard"), ("91%", "correct citations", "Bing 82%")]
        K = VGroup(*[VGroup(T(x, 36, UF, BOLD), T(y, 22, INK), T(z, 20, GREY)).arrange(DOWN, buff=0.14) for x, y, z in cards]).arrange(RIGHT, buff=0.8).move_to([0, 0.6, 0])
        src = T("Zakka et al., NEJM AI 2024; answers written by GPT-4 with retrieved sources", 20, GREY).move_to([0, -1.6, 0])
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.15) for k in K], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(src), run_time=0.4)
        self.rest(3.0)
        # 8. cautions
        self.cap("Read with care: the adversarial wins come mostly from declining to answer.", hold=0)
        self.play(FadeOut(K), FadeOut(src), run_time=0.6)
        hd = T("Correct under adversarial prompts (25 questions × 5 prompts)", 22, INK, BOLD).move_to([0, 2.3, 0])
        rows = [("Almanac", 100), ("Bard", 77), ("Bing", 70), ("ChatGPT-4", 7)]
        AB = VGroup()
        for i, (m, v) in enumerate(rows):
            y = 1.55 - 0.55 * i
            lab = T(m, 22, INK).move_to([-3.6, y, 0], aligned_edge=RIGHT)
            b = Rectangle(width=max(v, 1) * 0.06, height=0.38, stroke_width=0, fill_color=UF if i == 0 else "#9CA3AF", fill_opacity=0.85).move_to([-3.3 + max(v, 1) * 0.03, y, 0])
            AB.add(VGroup(lab, b, T(f"{v}%", 22, INK, BOLD).next_to(b, RIGHT, buff=0.15)))
        cv = VGroup(T("When an adversarial prompt pushes every match below λ, Almanac declines to answer.", 22, INK),
                    T("The questions and the grading came from the study's own clinicians.", 22, INK),
                    T("Only 25 of the 314 questions are public.", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([0, -1.55, 0])
        self.play(FadeIn(hd), LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in AB], lag_ratio=0.2), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in cv], lag_ratio=0.3), run_time=1.4)
        self.rest(3.2)
