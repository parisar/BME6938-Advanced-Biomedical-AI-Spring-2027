from kit import *
MODEL, POS, NEG, WARN = UF, "#DC2626", GREY, AMB          # model UF blue, sepsis red, no sepsis grey, warning amber
OK = "#0F766E"
FILLS = {MODEL: "#E0E7FF", GREY: "#F3F4F6", POS: "#FEE2E2", AMB: "#FEF3C7", OK: "#CCFBF1"}
PREV = 0.07                                               # prevalence, illustrative
POINTS = [(0.80, 0.10), (0.50, 0.20), (0.25, 0.35)]       # (sensitivity, positive predictive value)
def alerts_per_100(sens, ppv): return 100 * PREV * sens / ppv
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    if body.width > w - 0.8: body.scale_to_fit_width(w - 0.8)
    r = RoundedRectangle(corner_radius=0.12, width=w, height=body.height + 0.65,
                         stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
class C2(Clip):
    TITLE = "Thresholds, alert burden, and drift"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. the threshold is the only decision left
        self.cap("Once the model is fixed, the threshold is the decision you still make.", hold=0)
        X0, X1, BY, AH = -5.6, 5.0, -1.3, 2.4             # score axis and curve height
        X = lambda s: X0 + (X1 - X0) * s / 10
        def bell(mu, sd, color, fill):
            ss = np.linspace(0, 10, 160)
            pts = [np.array([X(s), BY + AH * np.exp(-0.5 * ((s - mu) / sd) ** 2), 0]) for s in ss]
            cv = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(pts)
            ar = VMobject(stroke_width=0, fill_color=fill, fill_opacity=0.55).set_points_as_corners(
                pts + [np.array([X(10), BY, 0]), np.array([X(0), BY, 0])])
            return VGroup(ar, cv)
        axis = Line([X(0), BY, 0], [X(10), BY, 0], color=GREY, stroke_width=3)
        ticks = VGroup(*[VGroup(Line([X(s), BY - 0.12, 0], [X(s), BY + 0.12, 0], color=GREY, stroke_width=3),
                                T(str(s), 20, GREY).move_to([X(s), BY - 0.42, 0])) for s in (0, 2, 4, 6, 8, 10)])
        neg = bell(3.2, 1.7, NEG, "#D1D5DB")
        pos = bell(6.6, 1.5, POS, "#FCA5A5")
        ln = T("no sepsis", 22, NEG).move_to([X(2.4), BY + AH * 0.55, 0])
        lp = T("sepsis", 22, POS, BOLD).move_to([X(8.1), BY + AH * 0.55, 0])
        thr = DashedLine([X(6), BY, 0], [X(6), BY + AH * 1.18, 0], color=MODEL, stroke_width=4, dash_length=0.14)
        tl = T("threshold", 22, MODEL, BOLD).next_to(thr, UP, buff=0.1)
        sl = T("risk score", 21, GREY).move_to([X(10) + 0.95, BY, 0])
        nt = VGroup(W("The curves are drawn to the same height. Sepsis is 7% of patients, so the red one is really much smaller.", 22, GREY),
                    W("Moving the line trades missed cases against false alarms. Nothing else about the model changes.", 23, INK)
                    ).arrange(DOWN, buff=0.22).move_to([0, -2.3, 0])
        ill = T("illustrative", 19, GREY).move_to([5.9, 1.9, 0])
        self.play(Create(axis), FadeIn(ticks), FadeIn(sl), run_time=0.7)
        self.play(FadeIn(neg), FadeIn(ln), run_time=0.8)
        self.play(FadeIn(pos), FadeIn(lp), FadeIn(ill), run_time=0.8)
        self.play(Create(thr), FadeIn(tl), run_time=0.6)
        self.play(FadeIn(nt), run_time=0.7)
        self.rest(2.4)
        # 2. three operating points
        self.cap("At 7% prevalence, three thresholds give very different alert loads.", hold=0)
        self.play(FadeOut(VGroup(axis, ticks, neg, pos, ln, lp, thr, tl, sl, nt, ill)), run_time=0.6)
        hd = VGroup(T("sensitivity", 23, INK, BOLD), T("PPV", 23, INK, BOLD), T("alerts per 100 admissions", 23, MODEL, BOLD))
        xs = (-4.6, -2.6, 1.6)
        for m, x in zip(hd, xs): m.move_to([x, 2.4, 0])
        R = VGroup()
        for k, (sens, ppv) in enumerate(POINTS):
            a = alerts_per_100(sens, ppv)
            bar = Rectangle(width=a / 56 * 4.6, height=0.46, stroke_width=0, fill_color=MODEL, fill_opacity=0.9)
            bar.move_to([-0.3 + a / 56 * 4.6 / 2, 1.6 - k * 0.85, 0])
            R.add(VGroup(T(f"{sens:.0%}", 23, INK).move_to([xs[0], 1.6 - k * 0.85, 0]),
                         T(f"{ppv:.0%}", 23, INK).move_to([xs[1], 1.6 - k * 0.85, 0]),
                         bar, T(f"{a:g}", 22, WHITE if a > 12 else INK, BOLD).move_to(
                             bar.get_center() if a > 12 else bar.get_right() + RIGHT * 0.35)))
        nt2 = VGroup(T("Every one of these is the same model on the same patients.", 24, INK),
                     T("Choosing a threshold is choosing how many alerts clinicians will see.", 24, MODEL, BOLD)
                     ).arrange(DOWN, buff=0.24).move_to([0, -1.5, 0])
        ill2 = T("illustrative", 19, GREY).move_to([5.9, 2.4, 0])
        self.play(FadeIn(hd), FadeIn(ill2), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in R], lag_ratio=0.3), run_time=1.8)
        self.play(FadeIn(nt2), run_time=0.7)
        self.rest(2.6)
        # 3. number needed to evaluate
        self.cap("The honest unit is patients reviewed per true case.", hold=0)
        self.play(FadeOut(VGroup(hd, R, nt2, ill2)), run_time=0.6)
        BASE, H = -1.4, 2.6
        ax3 = Line([-6.4, BASE, 0], [1.6, BASE, 0], color=GREY, stroke_width=3)
        NB = VGroup()
        for k, (sens, ppv) in enumerate(POINTS):
            nne = 1 / ppv
            h = H * nne / 10
            b = Rectangle(width=1.2, height=h, stroke_width=0, fill_color=MODEL, fill_opacity=0.9).move_to([-5.3 + k * 2.1, BASE + h / 2, 0])
            NB.add(VGroup(b, T(f"{nne:.1f}".rstrip("0").rstrip("."), 25, INK, BOLD).move_to([-5.3 + k * 2.1, BASE + h + 0.3, 0]),
                          T(f"PPV {ppv:.0%}", 21, GREY).move_to([-5.3 + k * 2.1, BASE - 0.38, 0])))
        real = VGroup(DashedLine([-6.4, BASE + H * 0.8, 0], [0.4, BASE + H * 0.8, 0], color=POS, stroke_width=3, dash_length=0.12),
                      T("the sepsis model at its threshold: 8", 21, POS, BOLD).move_to([-1.75, BASE + H * 0.8 + 0.34, 0]))
        nt3 = card("What this number means",
                   ["a clinician reviews this many patients for each real case",
                    "at PPV 12%, that is 8 reviews per sepsis case found",
                    "alerts fired on 18% of all hospitalizations"], POS, 6.0, [3.9, 0.7, 0], size=21)
        self.play(Create(ax3), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in NB], lag_ratio=0.3), run_time=1.6)
        self.play(Create(real[0]), FadeIn(real[1]), run_time=0.8)
        self.play(FadeIn(nt3[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in nt3[1]], lag_ratio=0.25), run_time=1.4)
        self.rest(2.4)
        # 4. the inputs move
        self.cap("And none of it holds still: the inputs change underneath you.", hold=0)
        self.play(FadeOut(VGroup(ax3, NB, real, nt3)), run_time=0.6)
        ds = [("A new lab assay", ["the creatinine method changes", "and the numbers shift slightly"]),
              ("A coding change", ["a diagnosis moves to a new code", "and a feature goes to zero"]),
              ("A new population", ["a unit reopens, a service closes,", "the case mix is not what you fitted"])]
        D = VGroup(*[card(t, l, WARN, 4.3, [-4.5 + k * 4.5, 1.2, 0], size=21) for k, (t, l) in enumerate(ds)])
        nt4 = VGroup(W("None of these generates a ticket. The model keeps producing scores, and they keep looking plausible.", 23, INK),
                     T("Performance is the thing that moves, and nobody is told.", 24, POS, BOLD)
                     ).arrange(DOWN, buff=0.24).move_to([0, -1.6, 0])
        self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.1) for d in D], lag_ratio=0.3), run_time=1.8)
        self.play(FadeIn(nt4), run_time=0.7)
        self.rest(2.4)
        # 5. the monitoring chart
        self.cap("So watch it: a control chart turns drift into something you can see.", hold=0)
        self.play(FadeOut(VGroup(D, nt4)), run_time=0.6)
        vals = [0.78, 0.76, 0.79, 0.77, 0.80, 0.78, 0.76, 0.79, 0.77, 0.75, 0.72, 0.70, 0.68, 0.67]
        cl, ucl, lcl = 0.78, 0.84, 0.72
        gx0, gx1, gy, gh = -5.6, 3.4, -1.6, 3.4
        PX = lambda k: gx0 + (gx1 - gx0) * k / (len(vals) - 1)
        PY = lambda v: gy + gh * (v - 0.62) / 0.26
        g5 = VGroup(Line([gx0 - 0.3, gy, 0], [gx1 + 0.3, gy, 0], color=GREY, stroke_width=3),
                    Line([gx0 - 0.3, gy, 0], [gx0 - 0.3, gy + gh, 0], color=GREY, stroke_width=3))
        for v, lab, col in ((ucl, "upper", GREY), (cl, "expected", MODEL), (lcl, "lower", POS)):
            g5.add(DashedLine([gx0 - 0.3, PY(v), 0], [gx1 + 0.3, PY(v), 0], color=col, stroke_width=3, dash_length=0.12),
                   T(f"{lab} {v:.2f}", 21, col).move_to([gx1 + 0.55, PY(v), 0], aligned_edge=LEFT))
        pts = [np.array([PX(k), PY(v), 0]) for k, v in enumerate(vals)]
        curve = VMobject(stroke_color=MODEL, stroke_width=4).set_points_as_corners(pts)
        dots = VGroup(*[Dot(radius=0.09, color=(POS if v < lcl else MODEL)).move_to(p) for p, v in zip(pts, vals)])
        bad = SurroundingRectangle(VGroup(*[d for d, v in zip(dots, vals) if v < lcl]), color=POS, buff=0.18, stroke_width=3, corner_radius=0.08)
        bl = T("3 months below the limit", 21, POS, BOLD).next_to(bad, DOWN, buff=0.14).shift(LEFT * 1.1)
        yl = VGroup(T("monthly AUC", 21, GREY).rotate(PI / 2).move_to([gx0 - 1.0, gy + gh / 2, 0]),
                    T("months since go-live", 21, GREY).move_to([(gx0 + gx1) / 2, gy - 0.5, 0]))
        ill5 = T("illustrative", 19, GREY).move_to([5.9, 2.2, 0])
        self.play(Create(g5), FadeIn(yl), FadeIn(ill5), run_time=1.1)
        self.play(Create(curve), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.06), run_time=1.6)
        self.play(Create(bad), FadeIn(bl), run_time=0.7)
        self.rest(2.4)
        # 6. the plan
        self.cap("Write the monitoring plan before go-live, not after the first surprise.", hold=0)
        self.play(FadeOut(VGroup(g5, yl, curve, dots, bad, bl, ill5)), run_time=0.6)
        rows = [("Track", "inputs, outputs and outcomes, not just the score", MODEL),
                ("Set limits", "in advance, from a period you agree was stable", WARN),
                ("Name a person", "who is paged when a limit is crossed", POS),
                ("Decide now", "what happens next: retrain, retune, or switch it off", OK)]
        G = VGroup()
        for a, b, c in rows:
            G.add(VGroup(box(a, 3.0, 0.72, FILLS[c], 24, c), T(b, 23, INK)).arrange(RIGHT, buff=0.45))
        G.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.75, 0])
        nt6 = W("A deployed model is not a result, it is a service, and services need someone on call.", 25, INK, BOLD).move_to([0, -2.0, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in G], lag_ratio=0.3), run_time=2.0)
        self.play(FadeIn(nt6), run_time=0.7)
        self.rest(3.0)
