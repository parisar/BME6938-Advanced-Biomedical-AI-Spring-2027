from kit import *
CLIN, MODEL, BOTH, NEITHER, WARN = "#0F766E", UF, "#CBD5E1", "#DC2626", AMB   # clinician teal, model UF blue
FILLS = {CLIN: "#CCFBF1", MODEL: "#E0E7FF", GREY: "#F3F4F6", AMB: "#FEF3C7", NEITHER: "#FEE2E2"}
CS, MS = 0.80, 0.75                                   # clinician and model sensitivity, illustrative
def counts(nested):
    """How 100 cases with disease split between clinician and model, under one assumption about their errors."""
    if nested:                                        # the clinician's misses are a subset of the model's
        both = round(MS * 100); c_only = round((CS - MS) * 100); m_only = 0
    else:                                             # independent errors
        both = round(CS * MS * 100); c_only = round(CS * (1 - MS) * 100); m_only = round((1 - CS) * MS * 100)
    return both, c_only, m_only, 100 - both - c_only - m_only
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
def grid100(nested, at, step=0.30, r=0.105):
    """100 cases with disease, one dot each, coloured by who catches them."""
    b, c, m, n = counts(nested)
    cols = [BOTH] * b + [CLIN] * c + [MODEL] * m + [NEITHER] * n
    g = VGroup(*[Dot(radius=r, color=col, fill_opacity=1).move_to([(k % 10) * step, -(k // 10) * step, 0])
                 for k, col in enumerate(cols)])
    return g.move_to([at[0], at[1], 0])
def legend(nested, at):
    b, c, m, n = counts(nested)
    rows = [("both catch it", b, BOTH), ("clinician only", c, CLIN), ("model only", m, MODEL), ("neither", n, NEITHER)]
    g = VGroup(*[VGroup(Dot(radius=0.12, color=col), T(name, 22, INK), T(str(v), 22, INK, BOLD)).arrange(RIGHT, buff=0.22)
                 for name, v, col in rows])
    return g.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([at[0], at[1], 0])
class C3(Clip):
    TITLE = "Humans and models together"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. two ways to combine
        self.cap("Put a clinician and a model together and there are two obvious rules.", hold=0)
        s1 = VGroup(T("clinician", 25, CLIN, BOLD), T("0.80", 36, CLIN, BOLD), T("sensitivity", 20, GREY)).arrange(DOWN, buff=0.14).move_to([-5.2, 1.5, 0])
        s2 = VGroup(T("model", 25, MODEL, BOLD), T("0.75", 36, MODEL, BOLD), T("sensitivity", 20, GREY)).arrange(DOWN, buff=0.14).move_to([-2.6, 1.5, 0])
        r1 = card("Flag if either flags", ["catches more cases", "and raises more false alarms"], CLIN, 5.8, [2.4, 2.1, 0], size=22)
        r2 = card("Flag only if both flag", ["fewer false alarms", "and catches fewer cases"], MODEL, 5.8, [2.4, 0.3, 0], size=22)
        ill = T("illustrative", 19, GREY).move_to([-3.9, -0.3, 0])
        nt = W("Which rule is better depends on something nobody measures: whether the two make the same mistakes.", 24, INK).move_to([0, -1.9, 0])
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(ill), run_time=0.9)
        self.play(FadeIn(r1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in r1[1]], lag_ratio=0.25), run_time=1.1)
        self.play(FadeIn(r2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in r2[1]], lag_ratio=0.25), run_time=1.1)
        self.play(FadeIn(nt), run_time=0.7)
        self.rest(2.4)
        # 2. assumption A: independent errors
        self.cap("Assume their errors are independent, and either-flags reaches 0.95.", hold=0)
        self.play(FadeOut(VGroup(s1, s2, r1, r2, nt, ill)), run_time=0.6)
        hdA = VGroup(W("Assumption A: independent errors", 26, INK, BOLD, w=5.8),
                     W("100 cases that really have the condition", 21, GREY, w=5.8)).arrange(DOWN, buff=0.14).move_to([-3.9, 2.5, 0])
        gA = grid100(False, (-4.0, 0.5))
        lgA = legend(False, (0.6, 0.5))
        resA = VGroup(VGroup(T("either flags", 24, INK), T("0.95", 32, CLIN, BOLD)).arrange(RIGHT, buff=0.45),
                      VGroup(T("both flag", 24, INK), T("0.60", 32, MODEL, BOLD)).arrange(RIGHT, buff=0.45)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.6, 0.5, 0])
        ntA = W("1 − 0.20 × 0.25 = 0.95 for either, and 0.80 × 0.75 = 0.60 for both. This is the textbook picture.", 23, GREY).move_to([0, -2.1, 0])
        self.play(FadeIn(hdA), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d) for d in gA], lag_ratio=0.008), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in lgA], lag_ratio=0.22), run_time=1.1)
        self.play(FadeIn(resA), run_time=0.7)
        self.play(FadeIn(ntA), run_time=0.6)
        self.rest(2.4)
        # 3. assumption B: the misses coincide
        self.cap("Assume the clinician's misses are a subset of the model's, and both numbers flip.", hold=0)
        self.play(FadeOut(VGroup(hdA, gA, lgA, resA, ntA)), run_time=0.6)
        hdB = VGroup(W("Assumption B: the misses are nested", 26, INK, BOLD, w=5.8),
                     W("the model misses whatever the clinician misses", 21, GREY, w=5.8)).arrange(DOWN, buff=0.14).move_to([-3.9, 2.5, 0])
        gB = grid100(True, (-4.0, 0.5))
        lgB = legend(True, (0.6, 0.5))
        resB = VGroup(VGroup(T("either flags", 24, INK), T("0.80", 32, NEITHER, BOLD)).arrange(RIGHT, buff=0.45),
                      VGroup(T("both flag", 24, INK), T("0.75", 32, MODEL, BOLD)).arrange(RIGHT, buff=0.45)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.6, 0.5, 0])
        ntB = VGroup(W("Either-flags falls from 0.95 to 0.80, which is the clinician alone: the model adds nothing.", 23, NEITHER, BOLD),
                     W("Both-flags rises from 0.60 to 0.75. The same two sensitivities, opposite conclusions.", 23, INK)
                     ).arrange(DOWN, buff=0.22).move_to([0, -2.1, 0])
        self.play(FadeIn(hdB), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d) for d in gB], lag_ratio=0.008), run_time=1.5)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in lgB], lag_ratio=0.22), run_time=1.1)
        self.play(FadeIn(resB), run_time=0.7)
        self.play(FadeIn(ntB), run_time=0.8)
        self.rest(2.6)
        # 4. people are not rules
        self.cap("And people are not rules: the combination has to be measured.", hold=0)
        self.play(FadeOut(VGroup(hdB, gB, lgB, resB, ntB)), run_time=0.6)
        a1 = card("Automation bias", ["a confident score talks people out of",
                                      "a correct judgement they already had"], NEITHER, 6.2, [-3.6, 1.9, 0], size=22)
        a2 = card("Alert fatigue", ["at 1 true case in 8 alerts, the rational",
                                    "response is to stop reading them"], WARN, 6.2, [3.6, 1.9, 0], size=22)
        a3 = card("So measure it", ["Goh et al. (Week 12) ran exactly this experiment: physicians with GPT-4 against",
                                    "physicians without. The model alone scored 92%. The physicians using it scored 76%,",
                                    "against 74% for those without, a difference of 2 points with an interval from −4 to 8."], MODEL, 11.8, [0, -0.6, 0], size=22)
        nt4 = W("Neither assumption in the last two slides is testable from the two sensitivities alone.", 24, INK, BOLD).move_to([0, -2.4, 0])
        self.play(FadeIn(a1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in a1[1]], lag_ratio=0.25), run_time=1.2)
        self.play(FadeIn(a2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in a2[1]], lag_ratio=0.25), run_time=1.2)
        self.play(FadeIn(a3[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in a3[1]], lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(nt4), run_time=0.6)
        self.rest(2.6)
        # 5. ambient intelligence
        self.cap("Ambient intelligence watches the room instead of waiting to be told.", hold=0)
        self.play(FadeOut(VGroup(a1, a2, a3, nt4)), run_time=0.6)
        hd5 = W("Contactless depth sensors, so the record fills itself. Two studies with measured numbers:", 24, INK).move_to([0, 2.5, 0])
        h1 = card("Hand hygiene (Singh et al., 2020)",
                  ["16 privacy-safe depth sensors, one acute care unit",
                   "algorithm: 92.1% sensitive (95% CI 84.3 to 96.7)",
                   "human observers: 85.2% (95% CI 76.1 to 91.1)",
                   "but the test set held only 88 dispenser-use events"], CLIN, 6.5, [-3.5, 0.6, 0], size=21)
        h2 = card("ICU mobility (Yeung et al., 2019)",
                  ["7 wall-mounted depth sensors, 563 mobility events",
                   "detecting the activity: 87.2% sensitivity",
                   "counting the staff involved: 68.8% accuracy",
                   "the weaker number is the one that matters"], MODEL, 6.5, [3.5, 0.6, 0], size=21)
        nt5 = W("The algorithm beat the human gold standard on sensitivity, on 88 events. Read the interval, not the point.", 23, WARN, BOLD).move_to([0, -2.3, 0])
        self.play(FadeIn(hd5), run_time=0.6)
        self.play(FadeIn(h1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in h1[1]], lag_ratio=0.22), run_time=1.5)
        self.play(FadeIn(h2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in h2[1]], lag_ratio=0.22), run_time=1.5)
        self.play(FadeIn(nt5), run_time=0.7)
        self.rest(2.6)
        # 6. privacy and consent
        self.cap("Sensing a care space is a governance question before it is a technical one.", hold=0)
        self.play(FadeOut(VGroup(hd5, h1, h2, nt5)), run_time=0.6)
        p1 = card("What depth sensing does help with",
                  ["no identifiable images leave the room",
                   "a shape is not a face",
                   "the papers call this privacy-safe"], CLIN, 6.6, [-3.6, 1.5, 0], size=21)
        p2 = card("What it does not settle",
                  ["patients are observed, and so is staff",
                   "who consents, who sees it, who uses it",
                   "and how long any of it is kept"], NEITHER, 6.6, [3.6, 1.5, 0], size=21)
        close = VGroup(W("Haque et al. name the barriers: rigorous clinical validation, data privacy, and model transparency.", 23, INK),
                       W("Clip 1: validate locally. Clip 2: watch it after go-live. Clip 3: measure the team, not the model.", 24, MODEL, BOLD)
                       ).arrange(DOWN, buff=0.28).move_to([0, -1.6, 0])
        self.play(FadeIn(p1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in p1[1]], lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(p2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in p2[1]], lag_ratio=0.25), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in close], lag_ratio=0.35), run_time=1.4)
        self.rest(3.2)
