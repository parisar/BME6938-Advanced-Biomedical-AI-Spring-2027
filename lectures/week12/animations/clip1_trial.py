from kit import *
LLM, CTL, ALONE, BAD = UF, GREY, "#0F766E", "#DC2626"      # LLM arm UF blue, control grey, model alone teal, warning red
FILLS = {LLM: "#E0E7FF", CTL: "#F3F4F6", ALONE: "#CCFBF1", AMB: "#FEF3C7", BAD: "#FEE2E2"}
def W(s, size=24, color=INK, weight=NORMAL, w=13.0):
    """A single line, scaled down if it would run off the frame."""
    t = T(s, size, color, weight)
    if t.width > w: t.scale_to_fit_width(w)
    return t
def card(title, lines, color, w, at, size=22):
    body = VGroup(T(title, 26, color, BOLD), *[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    r = RoundedRectangle(corner_radius=0.12, width=max(w, body.width + 0.8), height=body.height + 0.65,
                         stroke_color=color, stroke_width=2, fill_color=FILLS[color], fill_opacity=1)
    return VGroup(r, body.move_to(r)).move_to(at)
def vbar(x, v, vmax, base, h, color, label, iqr=None, suffix="%", bw=1.1):
    """A vertical bar from a full zero baseline, with an optional interquartile whisker."""
    top = base + h * v / vmax
    b = Rectangle(width=bw, height=h * v / vmax, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, (base + top) / 2, 0])
    ly = max(top, base + h * iqr[1] / vmax) if iqr else top          # keep the value label clear of the whisker
    g = VGroup(b, T(f"{v}{suffix}", 24, INK, BOLD).move_to([x, ly + 0.3, 0]))
    if iqr:
        lo, hi = (base + h * q / vmax for q in iqr)
        g.add(Line([x, lo, 0], [x, hi, 0], color=INK, stroke_width=3),
              Line([x - 0.2, lo, 0], [x + 0.2, lo, 0], color=INK, stroke_width=3),
              Line([x - 0.2, hi, 0], [x + 0.2, hi, 0], color=INK, stroke_width=3))
    g.add(T(label, 20, GREY).move_to([x, base - 0.35, 0]))
    return g
def ci(lo, hi, est, xmin, xmax, y, ticks, color, cx=0.0, span=8.0, fmt="{:g}"):
    """A point estimate with a confidence interval on a number line, with zero drawn in red."""
    X = lambda v: cx + (v - (xmin + xmax) / 2) * span / (xmax - xmin)
    g = VGroup(Line([X(xmin), y, 0], [X(xmax), y, 0], color=GREY, stroke_width=3))
    for v in ticks:
        g.add(Line([X(v), y - 0.13, 0], [X(v), y + 0.13, 0], color=(BAD if v == 0 else GREY), stroke_width=(4 if v == 0 else 3)),
              T(fmt.format(v), 20, (BAD if v == 0 else GREY), (BOLD if v == 0 else NORMAL)).move_to([X(v), y - 0.42, 0]))
    g.add(Line([X(lo), y + 0.55, 0], [X(hi), y + 0.55, 0], color=color, stroke_width=9),
          Line([X(lo), y + 0.35, 0], [X(lo), y + 0.75, 0], color=color, stroke_width=4),
          Line([X(hi), y + 0.35, 0], [X(hi), y + 0.75, 0], color=color, stroke_width=4),
          Dot(radius=0.13, color=color).move_to([X(est), y + 0.55, 0]))
    if lo < 0 < hi:
        g.add(DashedLine([X(0), y + 0.13, 0], [X(0), y + 0.95, 0], color=BAD, stroke_width=3, dash_length=0.1))
    return g
class C1(Clip):
    TITLE = "A benchmark score is not a clinical effect"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. two different questions
        self.cap("A model can score well on its own and still not change what clinicians do.", hold=0)
        q1 = card("What a benchmark asks", ["Can the model answer the question?",
                                            "One model, a fixed set of cases,", "one number."], CTL, 6.0, [-3.5, 1.3, 0], size=23)
        q2 = card("What a trial asks", ["Do clinicians do better with it?",
                                        "Two groups of clinicians,", "the same cases, a measured difference."], LLM, 6.0, [3.5, 1.3, 0], size=23)
        nt = W("These are different questions, and the second one is the one that decides whether a tool helps patients.", 24, INK).move_to([0, -1.5, 0])
        self.play(FadeIn(q1[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in q1[1]], lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(q2[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in q2[1]], lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(nt), run_time=0.6)
        self.rest(2.4)
        # 2. the trial
        self.cap("Goh et al. randomized 50 physicians into two groups of 25.", hold=0)
        self.play(FadeOut(VGroup(q1, q2, nt)), run_time=0.6)
        A = box("50 physicians", 2.9, 0.85, FILLS[CTL], 24, CTL).move_to([-4.8, 1.5, 0])
        al = T("26 attendings, 24 residents", 20, GREY).next_to(A, DOWN, buff=0.18)
        B = box("randomize", 2.5, 0.85, FILLS[AMB], 24, AMB).move_to([-1.0, 1.5, 0])
        bl = T("stratified by career stage", 20, GREY).next_to(B, DOWN, buff=0.18)
        C1b = box("25: GPT-4 + usual resources", 5.0, 0.8, FILLS[LLM], 22, LLM).move_to([3.6, 2.35, 0])
        C2b = box("25: usual resources only", 5.0, 0.8, FILLS[CTL], 22, CTL).move_to([3.6, 0.65, 0])
        ars = VGroup(Arrow(A.get_right(), B.get_left(), buff=0.12, color=GREY, stroke_width=4),
                     Arrow(B.get_right(), C1b.get_left(), buff=0.12, color=GREY, stroke_width=3),
                     Arrow(B.get_right(), C2b.get_left(), buff=0.12, color=GREY, stroke_width=3))
        task = card("The task, identical in both groups",
                    ["up to 6 clinical vignettes in 60 minutes",
                     "scored on a structured-reflection rubric by blinded graders",
                     "primary outcome: the diagnostic reasoning score per case"], GREY, 10.4, [0, -1.55, 0], size=22)
        self.play(FadeIn(A), FadeIn(al), run_time=0.7)
        self.play(GrowArrow(ars[0]), FadeIn(B), FadeIn(bl), run_time=0.7)
        self.play(GrowArrow(ars[1]), GrowArrow(ars[2]), FadeIn(C1b), FadeIn(C2b), run_time=0.9)
        self.play(FadeIn(task[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in task[1]], lag_ratio=0.25), run_time=1.4)
        self.rest(2.4)
        # 3. the primary result
        self.cap("Median score per case: 76% with GPT-4, 74% without.", hold=0)
        self.play(FadeOut(VGroup(A, al, B, bl, C1b, C2b, ars, task)), run_time=0.6)
        BASE, H = -1.5, 3.0
        axis = Line([-6.6, BASE, 0], [-1.6, BASE, 0], color=GREY, stroke_width=3)
        b1 = vbar(-5.5, 76, 100, BASE, H, LLM, "+ GPT-4", iqr=(66, 87))
        b2 = vbar(-3.3, 74, 100, BASE, H, CTL, "usual only", iqr=(63, 84))
        bl2 = T("median per case, bars with IQR", 20, GREY).move_to([-4.4, -2.15, 0])
        line = ci(-4, 8, 2, -10, 10, 0.55, (-10, -5, 0, 5, 10), LLM, cx=2.8, span=7.4)
        lt = VGroup(T("adjusted difference: 2 percentage points", 24, INK, BOLD),
                    T("95% CI −4 to 8, P = .60", 24, LLM, BOLD)).arrange(DOWN, buff=0.18).move_to([2.8, 2.2, 0])
        nt3 = T("the interval includes 0: this trial did not show a benefit", 23, BAD).move_to([2.8, -1.3, 0])
        self.play(Create(axis), FadeIn(b1), FadeIn(b2), FadeIn(bl2), run_time=1.3)
        self.play(FadeIn(lt), run_time=0.7)
        self.play(FadeIn(line), run_time=1.0)
        self.play(FadeIn(nt3), run_time=0.5)
        self.rest(2.6)
        # 4. time
        self.cap("Nor was it faster: 519 seconds per case against 565.", hold=0)
        self.play(FadeOut(VGroup(axis, b1, b2, bl2, line, lt, nt3)), run_time=0.6)
        t1 = vbar(-5.5, 519, 700, BASE, H, LLM, "+ GPT-4", suffix=" s")
        t2 = vbar(-3.3, 565, 700, BASE, H, CTL, "usual only", suffix=" s")
        ax2 = Line([-6.6, BASE, 0], [-1.6, BASE, 0], color=GREY, stroke_width=3)
        bl4 = T("median seconds per case", 20, GREY).move_to([-4.4, -2.15, 0])
        line4 = ci(-195, 31, -82, -250, 250, 0.55, (-250, -125, 0, 125, 250), LLM, cx=2.8, span=7.4)
        lt4 = VGroup(T("difference: −82 seconds", 24, INK, BOLD),
                     T("95% CI −195 to 31", 24, LLM, BOLD)).arrange(DOWN, buff=0.18).move_to([2.8, 2.2, 0])
        nt4 = T("this interval includes 0 too", 23, BAD).move_to([2.8, -1.3, 0])
        self.play(Create(ax2), FadeIn(t1), FadeIn(t2), FadeIn(bl4), run_time=1.2)
        self.play(FadeIn(lt4), FadeIn(line4), run_time=1.1)
        self.play(FadeIn(nt4), run_time=0.5)
        self.rest(2.4)
        # 5. the model alone
        self.cap("GPT-4 alone scored 92%, 16 points above the control group.", hold=0)
        self.play(FadeOut(VGroup(ax2, t1, t2, bl4, line4, lt4, nt4)), run_time=0.6)
        ax3 = Line([-6.7, BASE, 0], [-0.7, BASE, 0], color=GREY, stroke_width=3)
        c1 = vbar(-5.7, 92, 100, BASE, H, ALONE, "GPT-4 alone", iqr=(82, 97))
        c2 = vbar(-3.6, 76, 100, BASE, H, LLM, "+ GPT-4")
        c3 = vbar(-1.5, 74, 100, BASE, H, CTL, "usual only")
        y76, y92 = BASE + H * 0.76, BASE + H * 0.92
        gap = VGroup(DashedLine([-6.5, y76, 0], [-0.8, y76, 0], color=AMB, stroke_width=3, dash_length=0.12),
                     DoubleArrow([-4.65, y76, 0], [-4.65, y92, 0], buff=0, color=AMB, stroke_width=5,
                                 max_tip_length_to_length_ratio=0.22))
        rs = card("Read this one carefully",
                  ["3 runs of the model, median 92% (IQR 82 to 97)",
                   "+16 points vs control, 95% CI 2 to 30, P = .03",
                   "physicians with that model scored 76%"], AMB, 6.6, [3.5, 1.2, 0], size=20)
        nt5 = W("The gap between 92 and 76 is about how people use the tool, not about the tool.", 24, INK).move_to([0, -2.5, 0])
        self.play(Create(ax3), FadeIn(c1), FadeIn(c2), FadeIn(c3), run_time=1.3)
        self.play(FadeIn(gap), run_time=0.5)
        self.play(FadeIn(rs[0]), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in rs[1]], lag_ratio=0.25), run_time=1.4)
        self.play(FadeIn(nt5), run_time=0.5)
        self.rest(2.8)
        # 6. the ladder
        self.cap("Each rung of the evaluation ladder answers a question the one below cannot.", hold=0)
        self.play(FadeOut(VGroup(ax3, c1, c2, c3, gap, rs, nt5)), run_time=0.6)
        rungs = [("benchmark", "can it answer?", CTL), ("retrospective study", "on real records", CTL),
                 ("reader study", "with clinicians, offline", LLM), ("prospective trial", "does care change?", LLM),
                 ("deployment", "and keep watching", ALONE)]
        G = VGroup()
        for k, (a, b, col) in enumerate(rungs):
            x = -5.2 + k * 2.6
            y = -1.2 + k * 0.78
            step = Line([x - 1.2, y - 0.42, 0], [x + 1.2, y - 0.42, 0], color=GREY, stroke_width=3)
            G.add(VGroup(step, box(a, 2.4, 0.66, FILLS[col], 21, col).move_to([x, y, 0]),
                         T(b, 19, GREY).move_to([x, y - 0.72, 0])))
        nt6 = W("Goh et al. is the fourth rung. Most published results stop at the first.", 24, INK).move_to([0, -2.75, 0])
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.12) for g in G], lag_ratio=0.3), run_time=2.0)
        self.play(FadeIn(nt6), run_time=0.5)
        self.rest(3.0)
