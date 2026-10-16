from kit import *
MODEL, VENDOR, LOCAL, CLIN = UF, GREY, "#DC2626", "#0F766E"   # model UF blue, vendor claim grey, local result red, clinicians teal
FILLS = {MODEL: "#E0E7FF", GREY: "#F3F4F6", LOCAL: "#FEE2E2", CLIN: "#CCFBF1", AMB: "#FEF3C7"}
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
def stat(big, small, color, at, size=40):
    g = VGroup(T(big, size, color, BOLD), T(small, 21, GREY)).arrange(DOWN, buff=0.16)
    return g.move_to([at[0], at[1], 0])
class C1(Clip):
    TITLE = "What external validation found"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. a model already in hundreds of hospitals
        self.cap("A sepsis model running in hundreds of hospitals, scored every 15 minutes.", hold=0)
        who = card("The Epic Sepsis Model",
                   ["proprietary, shipped with the health record",
                    "deployed at hundreds of US hospitals",
                    "scored every 15 minutes, every inpatient",
                    "the vendor reported an AUC of 0.76 to 0.83"], MODEL, 6.6, [-3.6, 1.1, 0], size=21)
        x0, y0, wd, ht = 0.9, -0.5, 5.4, 2.6
        ax = VGroup(Line([x0, y0, 0], [x0 + wd, y0, 0], color=GREY, stroke_width=3),
                    Line([x0, y0, 0], [x0, y0 + ht, 0], color=GREY, stroke_width=3))
        pts = [0.6, 0.9, 1.4, 2.0, 2.6, 3.4, 4.6, 5.9, 7.2, 8.0]
        curve = VMobject(stroke_color=MODEL, stroke_width=4).set_points_as_corners(
            [np.array([x0 + wd * k / (len(pts) - 1), y0 + ht * v / 10, 0]) for k, v in enumerate(pts)])
        thr = DashedLine([x0, y0 + ht * 0.6, 0], [x0 + wd, y0 + ht * 0.6, 0], color=LOCAL, stroke_width=3, dash_length=0.12)
        tl = T("threshold 6", 21, LOCAL).next_to(thr, UP, buff=0.08).shift(LEFT * 1.9)
        cross = Dot(radius=0.11, color=LOCAL).move_to([x0 + wd * 7 / 9, y0 + ht * 0.59, 0])
        al = T("alert", 22, LOCAL, BOLD).next_to(cross, DOWN, buff=0.25).shift(RIGHT * 0.5)
        axl = VGroup(T("ESM score", 21, GREY).rotate(PI / 2).next_to(ax[1], LEFT, buff=0.2),
                     T("time in hospital", 21, GREY).next_to(ax[0], DOWN, buff=0.25))
        nt = W("It had been deployed for years. No independent validation had been published.", 24, INK).move_to([0, -2.3, 0])
        self.play(FadeIn(who[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in who[1]], lag_ratio=0.22), run_time=1.7)
        self.play(Create(ax), FadeIn(axl), run_time=0.7)
        self.play(Create(curve), run_time=1.1)
        self.play(Create(thr), FadeIn(tl), run_time=0.5)
        self.play(GrowFromCenter(cross), FadeIn(al), run_time=0.5)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(2.2)
        # 2. the cohort
        self.cap("Wong et al. validated it on 38,455 hospitalizations at one health system.", hold=0)
        self.play(FadeOut(VGroup(who, ax, axl, curve, thr, tl, cross, al, nt)), run_time=0.6)
        S = VGroup(stat("27,697", "patients", INK, (-4.4, 1.9)),
                   stat("38,455", "hospitalizations", INK, (0.0, 1.9)),
                   stat("2,552", "with sepsis, 7%", LOCAL, (4.4, 1.9)))
        bw, by = 11.6, 0.2
        bar = VGroup(Rectangle(width=bw, height=0.7, stroke_width=0, fill_color="#E5E7EB", fill_opacity=1).move_to([0, by, 0]),
                     Rectangle(width=bw * 0.0664, height=0.7, stroke_width=0, fill_color=LOCAL, fill_opacity=1)
                     .move_to([-bw / 2 + bw * 0.0332, by, 0]))
        bl = VGroup(T("sepsis, 7%", 21, LOCAL).move_to([-5.0, by - 0.65, 0]),
                    T("no sepsis, 93%", 21, GREY).move_to([0.6, by - 0.65, 0]))
        st = card("The study",
                  ["Michigan Medicine, 6 December 2018 to 20 October 2019",
                   "sepsis defined from the record, not from the vendor's labels",
                   "the model was scored on every adult hospitalization"], GREY, 10.2, [0, -1.9, 0], size=22)
        self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.1) for s in S], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(bar), FadeIn(bl), run_time=0.8)
        self.play(FadeIn(st[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in st[1]], lag_ratio=0.25), run_time=1.4)
        self.rest(2.4)
        # 3. discrimination
        self.cap("The AUC was 0.63, well below the 0.76 to 0.83 the vendor reported.", hold=0)
        self.play(FadeOut(VGroup(S, bar, bl, st)), run_time=0.6)
        lo, hi, span, cx, ay = 0.50, 0.90, 10.4, 0.0, -0.35
        X = lambda v: cx + (v - (lo + hi) / 2) * span / (hi - lo)
        line = VGroup(Line([X(lo), ay, 0], [X(hi), ay, 0], color=GREY, stroke_width=3))
        for v in (0.50, 0.60, 0.70, 0.80, 0.90):
            line.add(Line([X(v), ay - 0.14, 0], [X(v), ay + 0.14, 0], color=GREY, stroke_width=3),
                     T(f"{v:.2f}", 21, GREY).move_to([X(v), ay - 0.45, 0]))
        def row(a, b, y, color, label, lcolor, bold=True, dot=None):
            """One result on the shared axis: a band from a to b, with its label directly above it."""
            mid = (X(a) + X(b)) / 2
            g = VGroup(Rectangle(width=max(0.14, X(b) - X(a)), height=0.42, stroke_width=0,
                                 fill_color=color, fill_opacity=0.85).move_to([mid, y, 0]),
                       T(label, 23, lcolor, BOLD if bold else NORMAL).move_to([mid, y + 0.52, 0]))
            if dot is not None: g.add(Dot(radius=0.12, color=color).move_to([X(dot), y, 0]))
            return g
        band = row(0.76, 0.83, 2.60, "#9CA3AF", "vendor: 0.76 to 0.83", INK)
        th = row(0.72, 0.76, 1.55, AMB, "by time horizon: 0.72 to 0.76", INK, bold=False)
        loc = row(0.62, 0.64, 0.50, LOCAL, "this health system: 0.63 (0.62 to 0.64)", LOCAL, dot=0.63)
        nt3 = VGroup(W("The authors answer the obvious objection themselves: they call the per-horizon", 23, AMB, BOLD),
                     W("AUCs misleading, because those predictions are not independent of each other.", 23, AMB, BOLD),
                     W("Calibration was poor at every horizon as well.", 23, INK)).arrange(DOWN, buff=0.22).move_to([0, -2.0, 0])
        self.play(FadeIn(line), run_time=0.9)
        self.play(FadeIn(band), run_time=0.7)
        self.play(FadeIn(loc), run_time=0.9)
        self.play(FadeIn(th), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in nt3], lag_ratio=0.3), run_time=1.4)
        self.rest(2.6)
        # 4. at the vendor's threshold
        self.cap("At the recommended threshold it missed two thirds of sepsis and alerted on 18%.", hold=0)
        self.play(FadeOut(VGroup(line, band, th, loc, nt3)), run_time=0.6)
        rows = [("sensitivity", "33%", "two thirds of sepsis cases are never flagged", LOCAL),
                ("specificity", "83%", "so 17% of everyone else is flagged too", INK),
                ("PPV", "12%", "positive predictive value: about 1 alert in 8 is sepsis", LOCAL),
                ("NPV", "95%", "negative predictive value: the easy one, sepsis is rare", GREY)]
        R = VGroup()
        for name, val, note, col in rows:
            r = VGroup(T(name, 23, INK).move_to([-4.6, 0, 0], aligned_edge=RIGHT),
                       T(val, 28, col, BOLD).move_to([-3.6, 0, 0]),
                       T(note, 22, GREY).move_to([-2.7, 0, 0], aligned_edge=LEFT))
            R.add(r)
        for k, r in enumerate(R): r.shift(UP * (2.0 - k * 0.72))
        burden = card("The burden",
                      ["alerts on 6,971 of 38,455 hospitalizations: 18%",
                       "number needed to evaluate: 8 patients per sepsis case"], LOCAL, 9.4, [0, -1.75, 0], size=23)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in R], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(burden[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in burden[1]], lag_ratio=0.3), run_time=1.3)
        self.rest(2.6)
        # 5. what did the alert add
        self.cap("The question is not what the model scored, but what the alert added.", hold=0)
        self.play(FadeOut(VGroup(R, burden)), run_time=0.6)
        top = box("2,552 hospitalizations with sepsis", 6.4, 0.8, FILLS[LOCAL], 25, LOCAL).move_to([0, 2.4, 0])
        bA = box("flagged: 843 (33%)", 4.6, 0.75, FILLS[MODEL], 23, MODEL).move_to([-3.4, 0.9, 0])
        bB = box("never flagged: 1,709 (67%)", 4.8, 0.75, FILLS[GREY], 23, GREY).move_to([3.4, 0.9, 0])
        cA = card("of those", ["183 had not already received", "timely antibiotics", "the only ones it could help",
                               "7% of all sepsis cases"], CLIN, 5.6, [-3.4, -1.1, 0], size=21)
        cB = card("of those", ["1,030 (60%) received timely", "antibiotics anyway", "clinicians got there without it", "the alert added nothing for them"], GREY, 5.6, [3.4, -1.1, 0], size=21)
        A = VGroup(Arrow(top.get_bottom(), bA.get_top(), buff=0.1, color=GREY, stroke_width=3),
                   Arrow(top.get_bottom(), bB.get_top(), buff=0.1, color=GREY, stroke_width=3),
                   Arrow(bA.get_bottom(), cA.get_top(), buff=0.1, color=GREY, stroke_width=3),
                   Arrow(bB.get_bottom(), cB.get_top(), buff=0.1, color=GREY, stroke_width=3))
        self.play(FadeIn(top), run_time=0.6)
        self.play(GrowArrow(A[0]), GrowArrow(A[1]), FadeIn(bA), FadeIn(bB), run_time=0.9)
        self.play(GrowArrow(A[2]), FadeIn(cA), run_time=0.9)
        self.play(GrowArrow(A[3]), FadeIn(cB), run_time=0.9)
        self.rest(2.8)
        # 6. the lesson
        self.cap("Validate locally, and measure what the alert adds to current practice.", hold=0)
        self.play(FadeOut(VGroup(top, bA, bB, cA, cB, A)), run_time=0.6)
        l1 = card("Validate locally, before deployment",
                  ["a vendor's AUC came from vendor data",
                   "your case mix and workflow are not theirs",
                   "0.76 to 0.83 became 0.63 here"], LOCAL, 6.8, [-3.55, 1.2, 0], size=21)
        l2 = card("Measure the increment, not the model",
                  ["the comparison is current practice",
                   "clinicians already treat most in time",
                   "median lead time 2.5 h (IQR 0.5 to 15.6)"], CLIN, 6.8, [3.55, 1.2, 0], size=21)
        nt6 = VGroup(W("A model can be worth deploying only if it changes what happens to a patient.", 25, INK, BOLD),
                     T("Wong et al., JAMA Internal Medicine, 2021", 20, GREY)).arrange(DOWN, buff=0.25).move_to([0, -1.9, 0])
        self.play(FadeIn(l1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in l1[1]], lag_ratio=0.25), run_time=1.5)
        self.play(FadeIn(l2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in l2[1]], lag_ratio=0.25), run_time=1.5)
        self.play(FadeIn(nt6), run_time=0.7)
        self.rest(3.0)
