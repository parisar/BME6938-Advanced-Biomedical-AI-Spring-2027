from kit import *
SIG, SHORT, MOD = "#0F766E", "#DC2626", UF            # genuine signal teal, shortcut red, model UF blue
FILLS = {SIG: "#CCFBF1", MOD: "#E0E7FF", GREY: "#F3F4F6", AMB: "#FEF3C7", SHORT: "#FEE2E2"}
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    if body.width > w - 0.8: body.scale_to_fit_width(w - 0.8)      # never let a card grow past the width asked for
    r = RoundedRectangle(corner_radius=0.12, width=w, height=body.height + 0.65,
                         stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
def film(at, s=1.0):
    """A schematic chest radiograph, drawn from scratch: no third-party images."""
    g = VGroup()
    g.add(Rectangle(width=3.4, height=4.0, stroke_color=GREY, stroke_width=2, fill_color="#E5E7EB", fill_opacity=1))
    for x in (-0.72, 0.72):                                        # the two lung fields
        g.add(Ellipse(width=1.25, height=2.5, stroke_color="#9CA3AF", stroke_width=2, fill_color="#F9FAFB", fill_opacity=1).move_to([x, 0.35, 0]))
    g.add(Ellipse(width=1.3, height=1.5, stroke_color="#9CA3AF", stroke_width=2, fill_color="#D1D5DB", fill_opacity=1).move_to([0.18, -0.45, 0]))
    g.add(ArcBetweenPoints([-1.45, -1.25, 0], [1.45, -1.25, 0], angle=-0.75, stroke_color="#9CA3AF", stroke_width=3))
    for x in (-1.25, 1.25):                                        # the shoulders
        g.add(ArcBetweenPoints([x - 0.32, 1.85, 0], [x + 0.32, 1.45, 0], angle=(0.9 if x < 0 else -0.9), stroke_color="#9CA3AF", stroke_width=3))
    g.add(T("R", 22, INK, BOLD).move_to([-1.35, 1.65, 0]))         # the laterality marker
    g.add(Arrow([0.55, 1.5, 0], [0.05, 1.05, 0], buff=0, color=INK, stroke_width=3, max_tip_length_to_length_ratio=0.35),
          T("ggo", 17, INK).move_to([0.95, 1.6, 0]))               # an annotation copied in with the figure
    return g.scale(s).move_to([at[0], at[1], 0])
def tag(s, color, at, w=2.9):
    return box(s, w, 0.52, FILLS[color], 20, color).move_to([at[0], at[1], 0])
class C3(Clip):
    TITLE = "Shortcuts and hidden subgroups"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. a model can learn the wrong signal
        self.cap("A model can reach a high score by reading the wrong thing.", hold=0)
        f1 = film((-4.4, 0.9), 0.95)
        q = VGroup(T("?", 60, MOD, BOLD)).move_to([-1.3, 0.9, 0])
        pred = box("COVID-19 positive", 3.6, 0.8, FILLS[MOD], 24, MOD).move_to([2.4, 0.9, 0])
        a1 = Arrow([-2.6, 0.9, 0], [-1.9, 0.9, 0], buff=0, color=GREY, stroke_width=4)
        a2 = Arrow([-0.7, 0.9, 0], [0.5, 0.9, 0], buff=0, color=GREY, stroke_width=4)
        nt = VGroup(T("The score tells you the label was right.", 24, INK),
                    T("It does not tell you which part of the image produced it.", 24, SHORT, BOLD)).arrange(DOWN, buff=0.22).move_to([0, -2.3, 0])
        src = T("schematic radiograph, drawn for this clip", 19, GREY).move_to([-4.4, -1.35, 0])
        self.play(FadeIn(f1), FadeIn(src), run_time=0.9)
        self.play(GrowArrow(a1), FadeIn(q), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(pred), run_time=0.6)
        self.play(FadeIn(nt), run_time=0.7)
        self.rest(2.4)
        # 2. the two datasets
        self.cap("DeGrave et al. built two datasets, and the second was the favorable case.", hold=0)
        self.play(FadeOut(VGroup(f1, q, pred, a1, a2, nt, src)), run_time=0.6)
        d1 = card("Dataset I: the usual setup",
                  ["positives: GitHub-COVID, from figures",
                   "negatives: NIH ChestX-ray14, 1 hospital",
                   "source and label line up almost exactly"], SHORT, 6.8, [-3.6, 1.2, 0], size=21)
        d2 = card("Dataset II: the favorable case",
                  ["positives: BIMCV, negatives: PadChest",
                   "one region, one shared research team",
                   "similar sources on both sides"], SIG, 6.8, [3.6, 1.2, 0], size=21)
        nt2 = W("If shortcut learning only happened in the first setup, it would be a data-collection mistake. It happens in both.", 24, INK).move_to([0, -1.8, 0])
        self.play(FadeIn(d1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in d1[1]], lag_ratio=0.25), run_time=1.5)
        self.play(FadeIn(d2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in d2[1]], lag_ratio=0.25), run_time=1.5)
        self.play(FadeIn(nt2), run_time=0.6)
        self.rest(2.4)
        # 3. what the model actually looked at
        self.cap("Saliency maps and counterfactuals found it reading the margins, not the lungs.", hold=0)
        self.play(FadeOut(VGroup(d1, d2, nt2)), run_time=0.6)
        f2 = film((-4.3, 0.7), 1.0)
        hl = VGroup(Rectangle(width=0.7, height=0.55, stroke_color=SHORT, stroke_width=3.5).move_to([-5.65, 2.35, 0]),
                    Rectangle(width=1.4, height=0.9, stroke_color=SHORT, stroke_width=3.5).move_to([-3.6, 2.0, 0]),
                    Rectangle(width=3.1, height=0.5, stroke_color=SHORT, stroke_width=3.5).move_to([-4.3, -1.05, 0]),
                    Rectangle(width=3.42, height=4.02, stroke_color=SHORT, stroke_width=3.5).move_to([-4.3, 0.7, 0]),
                    Ellipse(width=2.9, height=2.7, stroke_color=SIG, stroke_width=3.5).move_to([-4.3, 1.05, 0]))
        lst = VGroup(T("What the explanations highlighted", 26, INK, BOLD),
                     T("laterality markers, which differ in style between sources", 22, SHORT),
                     T("arrows and text found only in the GitHub-COVID images", 22, SHORT),
                     T("the radiopacity of the image borders", 22, SHORT),
                     T("the shoulders, diaphragm and cardiac silhouette: patient position", 22, SHORT),
                     T("the lung fields, sometimes: genuine pathology", 22, SIG)).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([2.6, 1.0, 0])
        cf = W("A counterfactual test: moving the clavicle region to the top border raised the model's predicted odds of COVID-19.", 23, AMB).move_to([0, -2.0, 0])
        self.play(FadeIn(f2), run_time=0.7)
        self.play(LaggedStart(*[Create(h) for h in hl], lag_ratio=0.25), run_time=1.6)
        self.play(FadeIn(lst[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in lst[1:]], lag_ratio=0.22), run_time=1.8)
        self.play(FadeIn(cf), run_time=0.6)
        self.rest(2.6)
        # 4. half the performance
        self.cap("On radiographs from a new hospital system, half the performance was gone.", hold=0)
        self.play(FadeOut(VGroup(f2, hl, lst, cf)), run_time=0.6)
        BASE, H = -1.2, 2.9
        ax = Line([-6.6, BASE, 0], [-0.6, BASE, 0], color=GREY, stroke_width=3)
        def pbar(x, frac, color, label):
            b = Rectangle(width=1.3, height=H * frac, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, BASE + H * frac / 2, 0])
            return VGroup(b, T(label, 21, GREY).move_to([x, BASE - 0.38, 0]))
        p1 = pbar(-5.0, 1.0, MOD, "internal test set")
        p2 = pbar(-2.2, 0.5, SHORT, "new hospital system")
        dn = DoubleArrow([-0.9, BASE + H * 0.5, 0], [-0.9, BASE + H, 0], buff=0, color=SHORT, stroke_width=5, max_tip_length_to_length_ratio=0.22)
        sl = T("predictive performance (schematic)", 19, GREY).move_to([-3.6, -1.95, 0])
        qt = card("What the authors concluded",
                  ["half the predictive performance is lost",
                   "on radiographs from a new source",
                   "only a minority was genuine pathology",
                   "the rest was the source, not the disease"], SHORT, 7.2, [3.1, 0.9, 0], size=21)
        self.play(Create(ax), FadeIn(p1), run_time=0.9)
        self.play(FadeIn(p2), GrowFromCenter(dn), FadeIn(sl), run_time=0.9)
        self.play(FadeIn(qt[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in qt[1]], lag_ratio=0.25), run_time=1.5)
        self.rest(2.4)
        # 5. the shortcuts that survive
        self.cap("Some shortcuts transfer, so passing external validation proves less than it seems.", hold=0)
        self.play(FadeOut(VGroup(ax, p1, p2, dn, sl, qt)), run_time=0.6)
        s1 = card("Shortcuts that do not transfer",
                  ["laterality marker styles", "annotations from one archive",
                   "these differ between sources,", "so the score falls and you see it"], GREY, 6.2, [-3.5, 1.2, 0], size=21)
        s2 = card("Shortcuts that do transfer",
                  ["patient positioning, AP against PA", "consistent in both datasets",
                   "the score holds, and the model is", "still not reading the lungs"], SHORT, 6.2, [3.5, 1.2, 0], size=21)
        ban = box("External validation: necessary, not sufficient", 9.4, 0.85, FILLS[AMB], 26, AMB).move_to([0, -1.35, 0])
        nt5 = W("The authors' own conclusion: explainable AI is a prerequisite for deployment, not an optional extra.", 23, INK).move_to([0, -2.35, 0])
        self.play(FadeIn(s1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in s1[1]], lag_ratio=0.22), run_time=1.5)
        self.play(FadeIn(s2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in s2[1]], lag_ratio=0.22), run_time=1.5)
        self.play(FadeIn(ban, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(nt5), run_time=0.5)
        self.rest(2.6)
        # 6. subgroups
        self.cap("One more way an average lies: it hides the group it works worst on.", hold=0)
        self.play(FadeOut(VGroup(s1, s2, ban, nt5)), run_time=0.6)
        B2, H2 = -1.1, 2.6
        ax6 = Line([-6.7, B2, 0], [-0.3, B2, 0], color=GREY, stroke_width=3)
        def sbar(x, v, color, l1, l2):
            b = Rectangle(width=1.25, height=H2 * v, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, B2 + H2 * v / 2, 0])
            return VGroup(b, T(f"{v:.2f}", 23, INK, BOLD).move_to([x, B2 + H2 * v + 0.28, 0]),
                          T(l1, 21, INK).move_to([x, B2 - 0.35, 0]), T(l2, 19, GREY).move_to([x, B2 - 0.7, 0]))
        q1 = sbar(-5.4, 0.85, GREY, "overall", "all patients")
        q2 = sbar(-3.3, 0.90, SIG, "group A", "80% of patients")
        q3 = sbar(-1.2, 0.65, SHORT, "group B", "20% of patients")
        ar = T("0.8 × 0.90  +  0.2 × 0.65  =  0.85", 24, AMB, BOLD).move_to([-3.3, -2.25, 0])
        il = T("illustrative", 19, GREY).move_to([-3.3, 2.35, 0])
        chk = card("What to report, and what to check",
                   ["accuracy by subgroup, with an interval",
                    "performance at a new site (not sufficient)",
                    "what the model uses: saliency, occlusion",
                    "whether site is predictable from features"], MOD, 7.2, [3.2, 0.6, 0], size=21)
        self.play(Create(ax6), FadeIn(q1), FadeIn(il), run_time=0.9)
        self.play(FadeIn(q2), FadeIn(q3), run_time=0.9)
        self.play(FadeIn(ar), run_time=0.6)
        self.play(FadeIn(chk[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in chk[1]], lag_ratio=0.22), run_time=1.6)
        self.rest(3.2)
