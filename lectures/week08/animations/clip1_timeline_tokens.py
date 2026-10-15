from kit import *
STC, EVC, LBC, INC = "#6B7280", "#7C3AED", "#0F766E", "#B45309"   # static, event codes, labs, time intervals
FILL = {STC: "#F3F4F6", EVC: "#EDE9FE", LBC: "#CCFBF1", INC: "#FEF3C7"}
EVENTS = [(0.0, "ED admission"), (0.6, "lactate 4.1 mmol/L"), (1.5, "norepinephrine"), (2.2, "sepsis (A41.9)"), (3.5, "ICU transfer")]
X0, XS, YA = -5.6, 3.2, 1.6                        # timeline: x at 0 h, units per hour, axis height
def tk(s, color, size=20):
    """A token box that fits its text."""
    t = T(s, size, color)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.26, height=0.46, stroke_color=color, stroke_width=2, fill_color=FILL[color], fill_opacity=1)
    return VGroup(r, t.move_to(r))
def row(specs, buff=0.08):
    return VGroup(*[tk(s, c) for s, c in specs]).arrange(RIGHT, buff=buff)
class C1(Clip):
    TITLE = "A patient timeline as tokens"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        xt = lambda t: X0 + XS * t
        # 1. the timeline
        self.cap("A hospital record is a timeline of events at irregular times.", hold=0)
        ax = Arrow([X0 - 0.3, YA, 0], [6.6, YA, 0], buff=0, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.02)
        ticks = VGroup(*[VGroup(Line([xt(h), YA - 0.08, 0], [xt(h), YA + 0.08, 0], color=GREY, stroke_width=2), T(f"{h} h", 20, GREY).move_to([xt(h), YA - 0.35, 0])) for h in range(4)])
        D = VGroup(*[Dot([xt(t), YA, 0], radius=0.11, color=INK).set_z_index(2) for t, _ in EVENTS])
        L = VGroup(*[T(s, 20, INK).move_to([xt(t), YA + (0.45 if k % 2 == 0 else 1.0), 0]) for k, (t, s) in enumerate(EVENTS)])
        for d, l in zip(D, L):
            l.add(Line(d.get_center() + UP * 0.12, l.get_bottom() + DOWN * 0.04, color=GREY, stroke_width=1.5))
        sy = T("one synthetic ICU patient (no real patient data)", 20, GREY).move_to([0, -0.3, 0])
        self.play(GrowArrow(ax), FadeIn(ticks), FadeIn(sy), run_time=0.8)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=0.5), FadeIn(l)) for d, l in zip(D, L)], lag_ratio=0.3), run_time=2.0)
        self.rest(2.6)
        # 2. codes
        self.cap("Codes become tokens: ETHOS splits each code into its parts.", hold=0)
        self.play(FadeOut(sy), Indicate(L[3][0], color=EVC), Indicate(L[2][0], color=EVC), run_time=0.8)
        c1 = VGroup(T("sepsis, ICD-10 A41.9", 22, INK), T("→", 26, INK), row([("A41", EVC), ("9", EVC)])).arrange(RIGHT, buff=0.3)
        c2 = VGroup(T("norepinephrine, ATC C01CA03", 22, INK), T("→", 26, INK), row([("C01", EVC), ("CA", EVC), ("03", EVC)])).arrange(RIGHT, buff=0.3)
        CG = VGroup(c1, c2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-0.6, -0.55, 0])
        nt = T("first three characters, then the next two, then the rest", 20, GREY).next_to(CG, DOWN, buff=0.3)
        self.play(FadeIn(c1, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(c2, shift=UP * 0.1), FadeIn(nt), run_time=0.7)
        self.rest(3.0)
        # 3. quantile tokens
        self.cap("Numbers become quantile tokens: each lab is cut into 10 bins computed on the training data.", hold=0)
        self.play(FadeOut(VGroup(CG, nt)), Indicate(L[1][0], color=LBC), run_time=0.8)
        bw, by = 0.62, -1.75
        bins = VGroup(*[Rectangle(width=bw, height=0.5, stroke_color=WHITE, stroke_width=2, fill_color=LBC, fill_opacity=0.15 + 0.08 * k) for k in range(10)]).arrange(RIGHT, buff=0).move_to([-2.0, by, 0])
        bl = VGroup(*[T(f"Q{k + 1}", 20, INK).move_to(b) for k, b in enumerate(bins)])
        hl = T("lactate values in the training data, 10 equal-count bins", 20, GREY).next_to(bins, DOWN, buff=0.2)
        arr = Arrow(bins[9].get_top() + UP * 0.95, bins[9].get_top() + UP * 0.05, buff=0, stroke_width=4, color=LBC, max_tip_length_to_length_ratio=0.3)
        al = T("4.1", 22, LBC, BOLD).next_to(arr, RIGHT, buff=0.1).shift(UP * 0.25)
        out = row([("LACTATE", LBC), ("Q10", LBC)]).move_to([4.6, by, 0])
        oa = Arrow(bins.get_right(), out.get_left(), buff=0.2, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.2)
        cu = T("cutoffs illustrative", 20, GREY).next_to(out, DOWN, buff=0.2)
        self.play(FadeIn(bins), FadeIn(bl), FadeIn(hl), run_time=0.8)
        self.play(GrowArrow(arr), FadeIn(al), run_time=0.6)
        self.play(bins[9].animate.set_fill(LBC, opacity=1), bl[9].animate.set_color(WHITE), GrowArrow(oa), FadeIn(out), FadeIn(cu), run_time=0.8)
        self.rest(3.0)
        # 4. interval tokens
        self.cap("Time gaps become interval tokens: ETHOS uses 13, and none for gaps under 5 minutes.", hold=0)
        self.play(FadeOut(VGroup(bins, bl, hl, arr, al, oa, cu, out)), run_time=0.6)
        gaps = [(0.0, 0.6, "15m-1h"), (0.6, 1.5, "15m-1h"), (1.5, 2.2, "15m-1h"), (2.2, 3.5, "1h-2h")]
        B = VGroup(*[BraceBetweenPoints([xt(b), YA - 0.6, 0], [xt(a), YA - 0.6, 0], color=INC) for a, b, _ in gaps])
        G = VGroup(*[T(f"{b - a:.1f} h", 20, INC, BOLD).next_to(br, DOWN, buff=0.08) for (a, b, _), br in zip(gaps, B)])
        K = VGroup(*[tk(s, INC).next_to(g, DOWN, buff=0.15) for (_, _, s), g in zip(gaps, G)])
        il = T("ETHOS interval labels; the shortest are 5m-15m, 15m-1h, 1h-2h, 2h-6h, 6h-12h", 20, GREY).move_to([0, -2.4, 0])
        self.play(FadeOut(ticks), LaggedStart(*[AnimationGroup(GrowFromCenter(b), FadeIn(g)) for b, g in zip(B, G)], lag_ratio=0.2), run_time=1.2)
        self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.1) for k in K], lag_ratio=0.2), FadeIn(il), run_time=1.0)
        self.rest(3.0)
        # 5. one sequence
        self.cap("Static tokens come first, and the whole record becomes one sequence of 19 tokens.", hold=0)
        self.play(FadeOut(VGroup(B, G, K, il)), run_time=0.6)
        r1 = row([("SEX_F", STC), ("AGE_65-70", STC), ("+ 4 more static", STC), ("ED_ADMIT", EVC), ("15m-1h", INC), ("LACTATE", LBC), ("Q10", LBC)])
        r2 = row([("15m-1h", INC), ("C01", EVC), ("CA", EVC), ("03", EVC), ("15m-1h", INC), ("A41", EVC), ("9", EVC), ("1h-2h", INC), ("ICU_ADMIT", EVC)])
        S = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, -0.85, 0])
        lg = VGroup(*[VGroup(Square(0.24, stroke_width=0, fill_color=c, fill_opacity=1), T(n, 20, c)).arrange(RIGHT, buff=0.12) for n, c in [("static", STC), ("events and codes", EVC), ("lab and quantile", LBC), ("time interval", INC)]]).arrange(RIGHT, buff=0.45).move_to([0, -2.45, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in [*r1, *r2]], lag_ratio=0.07), run_time=2.0)
        self.play(FadeIn(lg), run_time=0.5)
        self.rest(3.0)
        # 6. decoder + next-token loss
        self.cap("A decoder learns to predict the next token, as in Weeks 3 to 5.", hold=0)
        self.play(FadeOut(VGroup(ax, D, L, lg)), S.animate.move_to([0, 2.3, 0]), run_time=0.8)
        dec = box("Decoder (transformer)", 8.0, 0.85, "#E0E7FF", size=24, stroke=UF).move_to([0, 0.75 - 0.05, 0])
        a1 = Arrow([0, 1.7, 0], [0, 1.15, 0], buff=0, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        nx = VGroup(T("next token?", 22, INK, BOLD), tk("DISCHARGE", EVC), tk("15m-1h", INC), tk("LACTATE", LBC), T("…", 24, GREY)).arrange(RIGHT, buff=0.2).move_to([0, -0.35, 0])
        a2 = Arrow([0, 0.3, 0], [0, -0.05, 0], buff=0, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        st = VGroup(T("ETHOS: 241,015 MIMIC-IV patients for training and validation", 22, INK),
                    T("context: the most recent 2,048 tokens of each timeline", 22, INK)).arrange(DOWN, buff=0.15).move_to([0, -1.65, 0])
        src = T("Renc et al., npj Digital Medicine 2024", 20, GREY).move_to([0, -2.55, 0])
        self.play(GrowArrow(a1), FadeIn(dec), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(nx), run_time=0.7)
        self.play(FadeIn(st), FadeIn(src), run_time=0.7)
        self.rest(3.2)
