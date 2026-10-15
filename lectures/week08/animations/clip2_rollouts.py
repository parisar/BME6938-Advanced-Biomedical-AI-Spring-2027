from kit import *
STC, EVC, LBC, INC = "#6B7280", "#7C3AED", "#0F766E", "#B45309"   # static, event codes, labs, time intervals (as in clip 1)
FILL = {STC: "#F3F4F6", EVC: "#EDE9FE", LBC: "#CCFBF1", INC: "#FEF3C7", INK: "#E5E7EB"}
DIS, DTH = "#0F766E", INK                                          # discharge, death
def tk(s, color, size=20):
    t = T(s, size, color)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.26, height=0.46, stroke_color=color, stroke_width=2, fill_color=FILL[color], fill_opacity=1)
    return VGroup(r, t.move_to(r))
def row(specs, buff=0.08):
    return VGroup(*[tk(s, c) for s, c in specs]).arrange(RIGHT, buff=buff)
DEATHS = [1, 4, 6, 9, 12, 15, 18]                                  # which of the 20 rollouts end in DEATH (illustrative)
class C2(Clip):
    TITLE = "Zero-shot prediction by simulating the future"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. the question
        self.cap("Will this patient die in the ICU? ETHOS answers without any task-specific training.", hold=0)
        hist = row([("…", STC), ("LACTATE", LBC), ("Q10", LBC), ("15m-1h", INC), ("C01", EVC), ("CA", EVC), ("03", EVC), ("15m-1h", INC), ("A41", EVC), ("9", EVC), ("1h-2h", INC), ("ICU_ADMIT", EVC)]).move_to([0, 2.2, 0])
        hl = T("the patient's timeline so far (clip 1)", 20, GREY).next_to(hist, DOWN, buff=0.2)
        q = VGroup(T("Question: ICU mortality", 26, INK, BOLD), T("no labels, no fine-tuning, no extra model", 22, GREY)).arrange(DOWN, buff=0.15).move_to([0, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in hist], lag_ratio=0.06), FadeIn(hl), run_time=1.3)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.7)
        self.rest(2.6)
        # 2. one rollout
        self.cap("From the ICU transfer, the model samples one token at a time until DISCHARGE or DEATH.", hold=0)
        self.play(FadeOut(q), FadeOut(hl), hist.animate.move_to([0, 2.45, 0]), run_time=0.7)
        gen = row([("6h-12h", INC), ("LACTATE", LBC), ("Q9", LBC), ("2h-6h", INC), ("C01", EVC), ("CA", EVC), ("03", EVC), ("6h-12h", INC), ("DEATH", DTH)])
        gen.move_to([0, 0.75, 0])
        gl = T("generated, one sampled token at a time", 20, GREY).next_to(gen, UP, buff=0.2)
        self.play(FadeIn(gl), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in gen], lag_ratio=0.35), run_time=2.4)
        sw = VGroup(T("Each new token is added to the context; once it holds 2,048 tokens, the oldest one drops off.", 20, GREY),
                    T("Tokens are illustrative.", 20, GREY)).arrange(DOWN, buff=0.1).move_to([0, -0.6, 0])
        self.play(FadeIn(sw), run_time=0.5)
        self.rest(2.8)
        # 3. twenty rollouts
        self.cap("Repeat 20 times: here, 7 of the 20 simulated futures end in DEATH.", hold=0)
        self.play(FadeOut(VGroup(hist, gen, gl, sw)), run_time=0.6)
        rng = np.random.default_rng(4)
        lines = VGroup()
        for k in range(20):
            col, r = divmod(k, 10)
            x0, y = (-6.3 if col == 0 else 0.6), 2.45 - 0.46 * r
            n = int(rng.integers(5, 11))
            sq = VGroup(*[Square(0.22, stroke_width=0, fill_color=[INC, LBC, EVC][int(rng.integers(0, 3))], fill_opacity=0.55) for _ in range(n)]).arrange(RIGHT, buff=0.05)
            sq.move_to([x0, y, 0], aligned_edge=LEFT)
            end = T("DEATH" if k in DEATHS else "DISCHARGE", 20, DTH if k in DEATHS else DIS, BOLD).next_to(sq, RIGHT, buff=0.15)
            num = T(f"{k + 1}", 20, GREY).next_to(sq, LEFT, buff=0.15)
            lines.add(VGroup(num, sq, end))
        il = T("illustrative", 20, GREY).move_to([5.8, -2.35, 0])
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in lines], lag_ratio=0.1), FadeIn(il), run_time=2.6)
        self.play(*[Indicate(lines[k][2], color=DTH, scale_factor=1.15) for k in DEATHS], run_time=0.8)
        self.rest(2.6)
        # 4. probability
        self.cap("The estimate is 7 / 20 = 0.35; with 20 rollouts, only 21 values are possible.", hold=0)
        self.play(FadeOut(lines), FadeOut(il), run_time=0.6)
        fr = T("P(death in ICU) ≈ 7 / 20 = 0.35", 40, UF, BOLD).move_to([0, 1.3, 0])
        nl = NumberLine(x_range=[0, 1, 0.05], length=11, include_ticks=True, tick_size=0.08, stroke_width=2, color=GREY).move_to([0, -0.5, 0])
        nlab = VGroup(*[T(f"{v:g}", 20, GREY).next_to(nl.n2p(v), DOWN, buff=0.2) for v in (0, 0.25, 0.5, 0.75, 1)])
        dots = VGroup(*[Dot(nl.n2p(k / 20), radius=0.06, color=GREY) for k in range(21)])
        mk = Dot(nl.n2p(0.35), radius=0.14, color=UF).set_z_index(3)
        ml = T("0.35", 22, UF, BOLD).next_to(mk, UP, buff=0.15)
        dl = T("21 possible values: 0, 0.05, 0.10, …, 1", 20, GREY).next_to(nl, DOWN, buff=0.75)
        self.play(FadeIn(fr), run_time=0.7)
        self.play(Create(nl), FadeIn(nlab), FadeIn(dots), run_time=0.8)
        self.play(FadeIn(mk, scale=0.5), FadeIn(ml), FadeIn(dl), run_time=0.6)
        self.rest(3.0)
        # 5. results
        self.cap("ETHOS reports an ICU mortality AUC of 0.927, at 7.0% prevalence.", hold=0)
        self.play(FadeOut(VGroup(fr, nl, nlab, dots, mk, ml, dl)), run_time=0.6)
        cards = [("0.927", "ICU mortality AUC", "7.0% died, 7,483 ICU stays"), ("0.921", "hospital mortality AUC", "2.0% died, from hospital admission"),
                 ("84.8%", "top-1 DRG, 771 classes", "diagnosis-related group at discharge"), ("sum", "of the interval tokens", "ICU length of stay")]
        K = VGroup(*[VGroup(T(a, 36, UF, BOLD), T(b, 22, INK), T(c, 20, GREY)).arrange(DOWN, buff=0.12) for a, b, c in cards]).arrange_in_grid(rows=2, buff=(1.2, 0.55)).move_to([0, 0.55, 0])
        src = T("Renc et al., npj Digital Medicine 2024; test set: 10% of MIMIC-IV patients", 20, GREY).move_to([0, -2.5, 0])
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.15) for k in K], lag_ratio=0.25), FadeIn(src), run_time=1.6)
        self.rest(3.0)
        # 6. prevalence
        self.cap("At low prevalence, a high AUC can still mean many false alarms.", hold=0)
        self.play(FadeOut(K), FadeOut(src), run_time=0.6)
        died = {3, 17, 28, 44, 56, 71, 89}                                     # 7 of 100 (7%)
        flag = died - {89} | {5, 9, 14, 22, 31, 35, 40, 48, 52, 60, 63, 67, 77, 94}   # 20 flagged: 6 deaths, 14 survivors
        cells = VGroup()
        for k in range(100):
            c = Circle(radius=0.15, stroke_width=0, fill_color=DTH if k in died else "#D1D5DB", fill_opacity=1)
            cells.add(c)
        cells.arrange_in_grid(rows=10, buff=0.12).move_to([-3.3, 0.35, 0])
        rings = VGroup(*[Circle(radius=0.21, color=AMB, stroke_width=4).move_to(cells[k]) for k in sorted(flag)])
        tx = VGroup(T("100 ICU patients, 7 died", 22, INK, BOLD),
                    VGroup(Circle(radius=0.12, color=AMB, stroke_width=4), T("20 flagged as high risk", 22, AMB, BOLD)).arrange(RIGHT, buff=0.15),
                    T("6 of the 7 deaths are caught,", 22, INK), T("but 14 of the 20 alarms are false", 22, INK),
                    T("illustrative numbers", 20, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([2.9, 0.35, 0])
        self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.01), FadeIn(tx[0]), run_time=1.2)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.05), FadeIn(tx[1]), run_time=1.0)
        self.play(FadeIn(tx[2:]), run_time=0.6)
        self.rest(3.2)
        # 7. cautions
        self.cap("Read the results with care: other studies' numbers, one hospital, and a 2,048-token window.", hold=0)
        self.play(FadeOut(VGroup(cells, rings, tx)), run_time=0.6)
        items = ["Baselines are numbers reported by other studies, with their own exclusion criteria.",
                 "MIMIC-IV comes from one hospital and may be cleaner than routine data.",
                 "Dense records lose their earliest history in the 2,048-token window.",
                 "Wornow et al. reviewed 84 EHR models: most were trained on MIMIC-III or PubMed",
                 "and tested on tasks that say little about value to a health system."]
        B = VGroup(*[T(s, 22, INK if k < 3 else UF) for k, s in enumerate(items)]).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([0, 0.4, 0])
        B[4].shift(UP * 0.12)
        self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in B], lag_ratio=0.3), run_time=2.0)
        self.rest(3.4)
