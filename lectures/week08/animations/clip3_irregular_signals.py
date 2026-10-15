from kit import *
STC, EVC, LBC, INC = "#6B7280", "#7C3AED", "#0F766E", "#B45309"   # as in clips 1 and 2
HRC = "#0369A1"                                                     # heart rate
FILL = {STC: "#F3F4F6", EVC: "#EDE9FE", LBC: "#CCFBF1", INC: "#FEF3C7", HRC: "#E0F2FE"}
HR_T = [0, 1, 2, 3, 4, 5, 8, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]   # hours after 6 p.m. with a charted heart rate
LAC_T = [0.6, 8, 14]                                                # lactate draws: 6:36 p.m., 2 a.m., 8 a.m.
CLOCK = ["6 p.m.", "10 p.m.", "2 a.m.", "6 a.m.", "10 a.m.", "2 p.m."]
def tk(s, color, size=20):
    t = T(s, size, color)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.26, height=0.46, stroke_color=color, stroke_width=2, fill_color=FILL[color], fill_opacity=1)
    return VGroup(r, t.move_to(r))
class C3(Clip):
    TITLE = "Irregular sampling and physiological signals"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        X0, XS = -5.2, 0.48                          # x at 6 p.m., units per hour
        xt = lambda t: X0 + XS * t
        # 1. irregular times
        self.cap("Measurements arrive at irregular times: heart rate about hourly, lactate only three times.", hold=0)
        ax = Line([xt(0) - 0.2, -0.4, 0], [xt(24) + 0.1, -0.4, 0], color=GREY, stroke_width=2)
        tl = VGroup(*[T(c, 20, GREY).move_to([xt(4 * k), -0.75, 0]) for k, c in enumerate(CLOCK)])
        r1 = T("heart rate", 22, HRC, BOLD).move_to([-6.2, 1.4, 0])
        r2 = T("lactate", 22, LBC, BOLD).move_to([-6.2, 0.3, 0])
        H = VGroup(*[Dot([xt(t), 1.4, 0], radius=0.09, color=HRC) for t in HR_T])
        La = VGroup(*[Dot([xt(t), 0.3, 0], radius=0.11, color=LBC) for t in LAC_T])
        gp = BraceBetweenPoints([xt(5.2), 1.7, 0], [xt(7.8), 1.7, 0], direction=UP, color=GREY)
        gl = T("overnight gap", 20, GREY).next_to(gp, UP, buff=0.08)
        il = T("one synthetic ICU day (illustrative)", 20, GREY).move_to([0, -1.6, 0])
        self.play(Create(ax), FadeIn(tl), FadeIn(r1), FadeIn(r2), FadeIn(il), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in H], lag_ratio=0.06), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in La], lag_ratio=0.3), GrowFromCenter(gp), FadeIn(gl), run_time=1.0)
        self.rest(2.6)
        # 2. hourly grid with a mask
        self.cap("Option 1: put the values on an hourly grid, fill the gaps, and add a mask of what was measured.", hold=0)
        self.play(FadeOut(VGroup(ax, tl, r1, r2, H, La, gp, gl, il)), run_time=0.6)
        HR = [118, 112, 108, 104, 101, 99, None, None, 110, None, None, 96]
        LA = [4.1] + [None] * 7 + [3.2] + [None] * 3
        cw, gx = 0.82, -3.9                          # cell width, x of the first cell
        def grid_row(vals, y, color, fmt):
            cells, last = VGroup(), None
            for k, v in enumerate(vals):
                meas = v is not None
                last = v if meas else last
                sq = Square(cw, stroke_color=WHITE, stroke_width=2, fill_color=color, fill_opacity=0.85 if meas else 0.18).move_to([gx + k * cw, y, 0])
                tx = T(fmt(last), 20, WHITE if meas else GREY).move_to(sq)
                cells.add(VGroup(sq, tx))
            return cells
        def mask_row(vals, y):
            return VGroup(*[VGroup(Square(cw, stroke_color=GREY, stroke_width=1.5, fill_color=WHITE, fill_opacity=1).move_to([gx + k * cw, y, 0]),
                                   T("1" if v is not None else "0", 20, INK if v is not None else GREY, BOLD if v is not None else NORMAL).move_to([gx + k * cw, y, 0])) for k, v in enumerate(vals)])
        G1, M1 = grid_row(HR, 1.55, HRC, lambda v: f"{v}"), mask_row(HR, 0.7)
        G2, M2 = grid_row(LA, -0.45, LBC, lambda v: f"{v:.1f}"), mask_row(LA, -1.3)
        labs = VGroup(*[T(s, 20, c, BOLD).next_to(np.array([gx - cw / 2, y, 0]), LEFT, buff=0.2) for s, c, y in
                        [("heart rate", HRC, 1.55), ("measured?", GREY, 0.7), ("lactate", LBC, -0.45), ("measured?", GREY, -1.3)]])
        hrs = VGroup(*[T(c, 20, GREY).move_to([gx + 4 * k * cw, 2.3, 0]) for k, c in enumerate(CLOCK[:3])])
        fl = T("pale cells: filled with the last measured value", 20, GREY).move_to([0.6, -2.2, 0])
        self.play(FadeIn(labs[0]), FadeIn(hrs), LaggedStart(*[FadeIn(c) for c in G1], lag_ratio=0.05), run_time=1.0)
        self.play(FadeIn(labs[2]), LaggedStart(*[FadeIn(c) for c in G2], lag_ratio=0.05), FadeIn(fl), run_time=1.0)
        self.play(FadeIn(labs[1]), FadeIn(labs[3]), FadeIn(M1), FadeIn(M2), run_time=0.8)
        self.rest(3.0)
        # 3. missingness is informative
        self.cap("Missing values carry information: a lactate drawn at 2 a.m. signals that someone was worried.", hold=0)
        hb = SurroundingRectangle(VGroup(G2[8], M2[8]), color=AMB, buff=0.06, stroke_width=5)
        hn = VGroup(T("2 a.m. lactate:", 22, AMB, BOLD), T("the mask lets the model use when it was measured", 22, INK)).arrange(RIGHT, buff=0.2).move_to([0.6, -2.2, 0])
        self.play(Create(hb), FadeOut(fl), run_time=0.6)
        self.play(FadeIn(hn), run_time=0.6)
        self.rest(3.2)
        # 4. interval tokens
        self.cap("Option 2: interval tokens, as in clip 1, so the gap itself becomes part of the input.", hold=0)
        self.play(FadeOut(VGroup(G1, G2, M1, M2, labs, hrs, hb, hn)), run_time=0.6)
        seq = VGroup(tk("HR", HRC), tk("Q9", HRC), tk("1h-2h", INC), tk("HR", HRC), tk("Q8", HRC), tk("2h-6h", INC), tk("LACTATE", LBC), tk("Q9", LBC), tk("HR", HRC), tk("Q9", HRC)).arrange(RIGHT, buff=0.08).move_to([0, 0.6, 0])
        sl = T("the overnight gap is the [2h-6h] token", 20, INC, BOLD).next_to(seq[5], DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in seq], lag_ratio=0.1), run_time=1.3)
        self.play(Indicate(seq[5], color=INC), FadeIn(sl), run_time=0.7)
        self.rest(2.8)
        # 5. continuous time embedding
        self.cap("Option 3: a time embedding, like the Week 2 position waves but in real hours.", hold=0)
        self.play(FadeOut(VGroup(seq, sl)), run_time=0.6)
        ax2 = Axes(x_range=[0, 24, 4], y_range=[-1.2, 1.2, 1], x_length=7.2, y_length=2.6, tips=False, axis_config={"color": GREY, "stroke_width": 2}).move_to([-2.4, 0.45, 0])
        w8 = ax2.plot(lambda t: np.sin(2 * np.pi * t / 8), color=PC, stroke_width=4)
        w24 = ax2.plot(lambda t: np.sin(2 * np.pi * t / 24), color=OC, stroke_width=4)
        xl = VGroup(*[T(f"{h} h", 20, GREY).next_to(ax2.c2p(h, -1.2), DOWN, buff=0.1) for h in (0, 8, 16, 24)])
        vl = DashedLine(ax2.c2p(2.5, -1.2), ax2.c2p(2.5, 1.2), color=INK, stroke_width=3)
        vt = T("t = 2.5 h", 20, INK, BOLD).next_to(vl, UP, buff=0.1)
        ll = VGroup(T("sin, 8-hour period", 20, PC, BOLD), T("sin, 24-hour period", 20, OC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax2, DOWN, buff=0.55).align_to(ax2, LEFT)
        vec = VGroup(T("time vector at 2.5 h", 22, INK, BOLD),
                     T("8 h:  sin 0.92,  cos −0.38", 22, PC), T("24 h:  sin 0.61,  cos 0.79", 22, OC)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([4.6, 0.45, 0])
        self.play(Create(ax2), FadeIn(xl), run_time=0.6)
        self.play(Create(w8), Create(w24), FadeIn(ll), run_time=1.2)
        self.play(Create(vl), FadeIn(vt), run_time=0.5)
        self.play(FadeIn(vec, shift=LEFT * 0.1), run_time=0.7)
        self.rest(3.0)
        # 6. ECG patches
        self.cap("Dense signals are cut into patches, as in Week 6: ten one-second patches of 500 samples.", hold=0)
        self.play(FadeOut(VGroup(ax2, w8, w24, xl, vl, vt, ll, vec)), run_time=0.6)
        f = ecg_fn(10, hr=96, seed=5)
        PW = 1.2
        P = VGroup(*[wave(f, k, k + 1, PW, 0.9).shift(RIGHT * (-6.0 + k * PW) + UP * 0.7) for k in range(10)])
        bx = VGroup(*[Rectangle(width=PW, height=1.5, stroke_color=EC, stroke_width=2).move_to([-6.0 + (k + 0.5) * PW, 1.0, 0]) for k in range(10)])
        n1 = T("500 samples per second × 10 s = 5,000 samples → 10 tokens of 500 samples each", 22, INK).move_to([0, -0.6, 0])
        n2 = T("(the Week 6 notebook used 250 Hz only so it would run faster)", 20, GREY).next_to(n1, DOWN, buff=0.25)
        self.play(Create(P, rate_func=linear), run_time=1.6)
        self.play(LaggedStart(*[Create(b) for b in bx], lag_ratio=0.08), run_time=0.8)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.6)
        self.rest(3.0)
        # 7. summary
        self.cap("Every clinical data type can become tokens; each choice decides what the model can see.", hold=0)
        self.play(FadeOut(VGroup(P, bx, n1, n2)), run_time=0.6)
        rows = [("events and codes", "tokens (codes split into parts)", EVC), ("lab values", "quantile tokens", LBC),
                ("time", "interval tokens, or a time embedding", INC), ("missing values", "a mask, or simply no token", GREY), ("dense signals", "patches", HRC)]
        TB = VGroup(*[VGroup(T(a, 24, c, BOLD), T("→", 24, INK), T(b, 24, INK)) for a, b, c in rows])
        for r in TB:
            r[0].move_to([-2.2, 0, 0], aligned_edge=RIGHT); r[1].move_to([-1.6, 0, 0]); r[2].move_to([-1.0, 0, 0], aligned_edge=LEFT)
        TB.arrange(DOWN, buff=0.38).move_to([0, 0.5, 0])
        for r in TB:
            r[0].align_to(np.array([-2.2, 0, 0]), RIGHT); r[1].set_x(-1.6); r[2].align_to(np.array([-1.0, 0, 0]), LEFT)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in TB], lag_ratio=0.25), run_time=1.8)
        self.rest(3.4)
