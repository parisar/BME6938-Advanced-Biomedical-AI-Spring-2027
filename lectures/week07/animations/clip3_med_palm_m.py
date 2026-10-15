from kit import *
IMC, TXC, LMC = "#0F766E", "#B45309", "#1E3A8A"    # image side (teal), text side (amber), language model (navy)
CNT = "#B45309"                                   # tokens counted in the loss (as in Week 5)
def cxr(h=3.2):
    """A stylized frontal chest X-ray: dark film, darker lungs, white spine, heart, clavicles, ribs, and diaphragm."""
    w = h * 0.86
    film = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_width=0, fill_color="#1F2937", fill_opacity=1)
    lungs = VGroup(*[Ellipse(width=w * 0.34, height=h * 0.62, stroke_width=0, fill_color="#0B0F17", fill_opacity=1).move_to([s * w * 0.2, h * 0.02, 0]) for s in (-1, 1)])
    ribs = VGroup(*[ArcBetweenPoints([s * w * 0.04, h * (0.26 - 0.1 * k), 0], [s * w * 0.37, h * (0.17 - 0.1 * k), 0], angle=s * 0.5, stroke_color="#9CA3AF", stroke_width=2.5, stroke_opacity=0.55) for s in (-1, 1) for k in range(5)])
    spine = RoundedRectangle(corner_radius=0.04, width=w * 0.09, height=h * 0.9, stroke_width=0, fill_color="#E5E7EB", fill_opacity=0.85)
    heart = Ellipse(width=w * 0.38, height=h * 0.28, stroke_width=0, fill_color="#D1D5DB", fill_opacity=0.9).move_to([w * 0.05, -h * 0.12, 0])
    clav = VGroup(*[Line([s * w * 0.05, h * 0.33, 0], [s * w * 0.36, h * 0.38, 0], stroke_color="#E5E7EB", stroke_width=5) for s in (-1, 1)])
    dia = VGroup(*[ArcBetweenPoints([s * w * 0.04, -h * 0.27, 0], [s * w * 0.4, -h * 0.3, 0], angle=s * 0.9, stroke_color="#E5E7EB", stroke_width=4) for s in (-1, 1)])
    belly = Rectangle(width=w * 0.86, height=h * 0.16, stroke_width=0, fill_color="#D1D5DB", fill_opacity=0.55).move_to([0, -h * 0.4, 0])
    return VGroup(film, lungs, belly, ribs, spine, heart, clav, dia)
def tokrow(labels, color, fill, w=0.95, size=20):
    """A row of token boxes, each wide enough for its word."""
    return VGroup(*[tok(s, color, w=max(w, T(s, size).width + 0.3), h=0.5, size=size, fill=fill) for s in labels]).arrange(RIGHT, buff=0.08)
class C3(Clip):
    TITLE = "Images as tokens: Med-PaLM M"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. CLIP matches, but cannot write
        self.cap("CLIP can match an image with a caption, but it cannot write a report.", hold=0)
        X = cxr(3.0).move_to([-4.6, 0.45, 0])
        xl = T("stylized chest X-ray", 20, GREY).next_to(X, DOWN, buff=0.15)
        m = VGroup(T("CLIP: pick the best caption", 22, IMC, BOLD),
                   tok("“normal chest X-ray”  0.61", TXC, w=4.4, h=0.5, size=20, fill="#FEF3C7"),
                   tok("“pleural effusion”  0.27", TXC, w=4.4, h=0.5, size=20, fill="#FEF3C7"),
                   tok("“pneumothorax”  0.12", TXC, w=4.4, h=0.5, size=20, fill="#FEF3C7")).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([1.6, 1.25, 0])
        r = VGroup(T("Needed: write the report", 22, LMC, BOLD), T("Findings: The lungs are clear. No pleural", 22, INK), T("effusion or pneumothorax. Heart size is normal.", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(m, DOWN, buff=0.55).align_to(m, LEFT)
        il = T("scores and report are illustrative", 20, GREY).next_to(r, DOWN, buff=0.12).align_to(r, LEFT)
        self.play(FadeIn(X), FadeIn(xl), run_time=0.8)
        self.play(FadeIn(m, shift=RIGHT * 0.15), run_time=0.8)
        self.play(FadeIn(r, shift=RIGHT * 0.15), FadeIn(il), run_time=0.8)
        self.rest(2.8)
        # 2. vision transformer + projection
        self.cap("A vision transformer turns the X-ray into patch vectors, and a projection resizes them to tokens.", hold=0)
        self.play(FadeOut(VGroup(m, r, il)), X.animate.scale(0.8).move_to([-5.4, 0.6, 0]), xl.animate.move_to([-5.4, -0.85, 0]), run_time=0.7)
        gl = VGroup(*[Line(X.get_corner(UL) + RIGHT * k * X.width / 4, X.get_corner(DL) + RIGHT * k * X.width / 4, stroke_color="#F59E0B", stroke_width=2) for k in range(1, 4)],
                    *[Line(X.get_corner(UL) + DOWN * k * X.height / 4, X.get_corner(UR) + DOWN * k * X.height / 4, stroke_color="#F59E0B", stroke_width=2) for k in range(1, 4)])
        vit = box("Vision\ntransformer", 2.0, 1.3, "#CCFBF1", size=22, stroke=IMC).move_to([-2.45, 0.6, 0])
        a1 = Arrow(X.get_right(), vit.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        pv = VGroup(*[mat(4, 1, IMC, cell=0.28, seed=40 + k) for k in range(4)]).arrange(RIGHT, buff=0.12).move_to([-0.2, 0.6, 0])
        a2 = Arrow(vit.get_right(), pv.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        pvl = T("patch vectors", 20, IMC, BOLD).next_to(pv, DOWN, buff=0.2)
        pj = box("Projection", 1.7, 0.8, "#E0E7FF", size=22, stroke=LMC).move_to([2.25, 0.6, 0])
        a3 = Arrow(pv.get_right(), pj.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        it = VGroup(*[mat(6, 1, LMC, cell=0.24, seed=60 + k) for k in range(4)]).arrange(RIGHT, buff=0.1).move_to([4.65, 0.6, 0])
        a4 = Arrow(pj.get_right(), it.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        itl = VGroup(T("image tokens,", 20, LMC, BOLD), T("same size as word tokens", 20, LMC)).arrange(DOWN, buff=0.05).next_to(it, DOWN, buff=0.2)
        self.play(Create(gl), run_time=0.6)
        self.play(GrowArrow(a1), FadeIn(vit), run_time=0.6)
        self.play(GrowArrow(a2), LaggedStart(*[FadeIn(v, shift=RIGHT * 0.1) for v in pv], lag_ratio=0.15), FadeIn(pvl), run_time=0.9)
        self.play(GrowArrow(a3), FadeIn(pj), run_time=0.5)
        self.play(GrowArrow(a4), LaggedStart(*[FadeIn(v, shift=RIGHT * 0.1) for v in it], lag_ratio=0.15), FadeIn(itl), run_time=0.9)
        self.rest(2.8)
        # 3. one sequence for the decoder
        self.cap("Image tokens and text tokens form one sequence for the same decoder as in Weeks 4 and 5.", hold=0)
        self.play(FadeOut(VGroup(gl, vit, a1, pv, a2, pvl, pj, a3, a4, itl)), FadeOut(X), FadeOut(xl), it.animate.scale(0.9).move_to([-5.6, 1.7, 0]), run_time=0.8)
        txt = tokrow(["Write", "the", "findings", "for", "this", "X-ray."], TXC, "#FEF3C7", w=1.12)
        txt.next_to(it, RIGHT, buff=0.15)
        ib = SurroundingRectangle(it, color=LMC, buff=0.08, stroke_width=2)
        itl2 = T("image", 20, LMC, BOLD).next_to(ib, UP, buff=0.1)
        txl = T("instruction", 20, TXC, BOLD).next_to(txt, UP, buff=0.1)
        dec = box("Language model (decoder)", 9.6, 0.9, "#E0E7FF", size=24, stroke=LMC).move_to([0, 0.15, 0])
        ar = Arrow([0, 1.25, 0], [0, 0.65, 0], buff=0, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        out = tokrow(["The", "lungs", "are", "clear.", "No", "pleural", "effusion."], INK, "#F3F4F6", w=1.12).move_to([0, -1.35, 0])
        ao = Arrow([0, -0.35, 0], [0, -0.98, 0], buff=0, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        ol = T("report, one token at a time (illustrative)", 20, GREY).next_to(out, DOWN, buff=0.15)
        self.play(Create(ib), FadeIn(itl2), LaggedStart(*[FadeIn(t) for t in txt], lag_ratio=0.08), FadeIn(txl), run_time=1.0)
        self.play(GrowArrow(ar), FadeIn(dec), run_time=0.6)
        self.play(GrowArrow(ao), LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in out], lag_ratio=0.2), FadeIn(ol), run_time=1.4)
        self.rest(2.8)
        # 4. same loss, report tokens only
        self.cap("Training uses the same next-token loss, counted only on the report tokens.", hold=0)
        self.play(it.animate.set_opacity(0.3), ib.animate.set_stroke(opacity=0.3), txt.animate.set_opacity(0.3), FadeOut(VGroup(ar, ao, ol)), run_time=0.7)
        nc = T("not counted", 22, GREY, BOLD).move_to([0, 2.6, 0])
        self.play(*[t[0].animate.set_stroke(CNT, width=4) for t in out], FadeIn(nc), run_time=0.8)
        cl = T("counted in the loss (as in Week 5)", 22, CNT, BOLD).next_to(out, DOWN, buff=0.2)
        self.play(FadeIn(cl), run_time=0.5)
        self.rest(3.0)
        # 5. Med-PaLM M
        self.cap("Med-PaLM M fine-tunes PaLM-E on 14 biomedical tasks, with one set of weights for all of them.", hold=0)
        self.play(FadeOut(VGroup(it, ib, itl2, txt, txl, dec, out, nc, cl)), run_time=0.6)
        base = VGroup(T("PaLM-E", 30, LMC, BOLD), T("PaLM + vision transformer", 22, INK), T("sizes: 12B, 84B, 562B", 22, GREY)).arrange(DOWN, buff=0.15).move_to([-4.0, 1.2, 0])
        bench = VGroup(T("MultiMedBench", 30, LMC, BOLD), T("14 tasks · 12 datasets · 7 modalities", 22, INK)).arrange(DOWN, buff=0.15).move_to([3.5, 1.2, 0])
        mods = ["clinical text", "radiology", "pathology", "dermatology", "mammography", "genomics"]
        mt = VGroup(*[tok(s, LMC, w=2.15, h=0.5, size=20, fill="#E0E7FF") for s in mods]).arrange_in_grid(rows=2, buff=(0.15, 0.15)).move_to([0, -1.1, 0])
        ml = T("including", 20, GREY).next_to(mt, UP, buff=0.15)
        ar5 = Arrow(base.get_right(), bench.get_left(), buff=0.2, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.15)
        ar5l = T("fine-tune", 20, INK).next_to(ar5, UP, buff=0.1)
        src = T("Tu et al., NEJM AI 2024", 20, GREY).move_to([0, -2.55, 0])
        self.play(FadeIn(base), run_time=0.6)
        self.play(GrowArrow(ar5), FadeIn(ar5l), FadeIn(bench), run_time=0.7)
        self.play(FadeIn(ml), LaggedStart(*[FadeIn(t) for t in mt], lag_ratio=0.1), FadeIn(src), run_time=1.0)
        self.rest(3.0)
        # 6. results
        self.cap("Clinicians preferred its chest X-ray report to the radiologist's in up to 40.5% of 246 cases.", hold=0)
        self.play(FadeOut(VGroup(base, bench, mt, ml, ar5, ar5l)), run_time=0.6)
        X2 = cxr(2.4).move_to([-5.0, 0.6, 0])
        k1 = VGroup(T("up to 40.5%", 40, UF, BOLD), T("of 246 chest X-rays: Med-PaLM M's report", 22, INK), T("preferred to the radiologist's", 22, INK)).arrange(DOWN, buff=0.12).move_to([1.4, 1.35, 0])
        k2 = VGroup(T("87.7%  vs  92.6%", 34, UF, BOLD), T("tuberculosis on chest X-rays: Med-PaLM M zero-shot", 22, INK), T("vs a specialist model trained on 138 images", 22, INK)).arrange(DOWN, buff=0.12).move_to([1.4, -0.95, 0])
        self.play(FadeIn(X2), FadeIn(k1, shift=UP * 0.15), run_time=0.9)
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.8)
        self.rest(3.2)
        # 7. caution
        self.cap("That is a retrospective ranking, not clinical use: in most cases, the model's report was not preferred.", hold=0)
        self.play(FadeOut(k2), k1.animate.move_to([1.4, 1.5, 0]), run_time=0.6)
        bar = VGroup(Rectangle(width=8.0 * 0.405, height=0.55, stroke_width=0, fill_color=LMC, fill_opacity=1),
                     Rectangle(width=8.0 * 0.595, height=0.55, stroke_width=0, fill_color="#9CA3AF", fill_opacity=1)).arrange(RIGHT, buff=0).move_to([1.4, 0.0, 0])
        bl1 = T("Med-PaLM M preferred", 20, LMC, BOLD).next_to(bar, DOWN, buff=0.15).align_to(bar, LEFT)
        bl2 = VGroup(T("radiologist preferred,", 20, GREY), T("or no preference", 20, GREY)).arrange(DOWN, aligned_edge=RIGHT, buff=0.05).next_to(bar, DOWN, buff=0.15).align_to(bar, RIGHT)
        nt = VGroup(T("Side-by-side ranking of past cases, not a prospective trial.", 22, INK), T("Evaluation and deployment: Week 12.", 22, GREY)).arrange(DOWN, buff=0.12).move_to([1.4, -1.75, 0])
        self.play(GrowFromEdge(bar[0], LEFT), FadeIn(bl1), run_time=0.7)
        self.play(GrowFromEdge(bar[1], LEFT), FadeIn(bl2), run_time=0.7)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(3.4)
