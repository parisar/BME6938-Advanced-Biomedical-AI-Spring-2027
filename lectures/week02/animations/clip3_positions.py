from kit import *
POS, INP = "#EA580C", "#334155"                    # position vector (orange), input vector (dark slate)
SPEEDS = [1.0, 0.45, 0.2, 0.08]                    # sine speeds of the four dimension pairs drawn (pair 1 is exact)
def swatch(color, s):
    return VGroup(Square(0.3, stroke_width=0, fill_color=color, fill_opacity=1), T(s, 22, INK)).arrange(RIGHT, buff=0.15)
def m(v):
    return f"{v:.2f}".replace("-", "−")
class C3(Clip):
    TITLE = "Giving tokens a position"
    PACE, HOLD = 1.2, 0.6
    def construct(self):
        # 1. attention ignores order
        A = ["chest", "pain", ",", "no", "pressure"]
        perm = [3, 1, 2, 0, 4]                     # where each token of row A sits in "no pain, chest pressure"
        xs = [-3.0 + k * 1.75 for k in range(5)]; ya, yb = 2.1, -0.35
        RA = VGroup(*[tok(w, INK, w=1.62, h=0.55, size=22).move_to([x, ya, 0]) for w, x in zip(A, xs)])
        OA = VGroup(*[mat(3, 1, OC, cell=0.36, seed=200 + i).move_to([x, ya - 0.95, 0]) for i, x in enumerate(xs)])
        la = T("Patient 1", 22, INK, BOLD).move_to([-5.4, ya, 0]); lb = T("Patient 2", 22, INK, BOLD).move_to([-5.4, yb, 0])
        lo = T("attention outputs", 20, "#A16207", BOLD).move_to([-5.4, ya - 0.95, 0])
        self.play(FadeIn(la), LaggedStart(*[FadeIn(b, shift=DOWN * 0.2) for b in RA], lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(lo), LaggedStart(*[FadeIn(o) for o in OA], lag_ratio=0.1), run_time=0.9)
        RB, OB = RA.copy(), OA.copy()
        self.play(FadeIn(lb), *[RB[i].animate.move_to([xs[perm[i]], yb, 0]) for i in range(5)],
                  *[OB[i].animate.move_to([xs[perm[i]], yb - 0.95, 0]) for i in range(5)], run_time=1.8)
        nt = T("same five output vectors, only reordered", 22, GREY).move_to([0.5, -2.45, 0])
        self.play(FadeIn(nt), Indicate(VGroup(OB[0], OB[3]), color=OC, scale_factor=1.15), run_time=1.0)
        self.cap("Attention ignores word order.", hold=2.6)
        # 2. add a position vector
        self.play(*[FadeOut(x) for x in (RA, OA, RB, OB, la, lb, lo, nt)], run_time=0.6)
        TK = ["The", "patient", "has", "a", "cold"]; gx = [-5.0, -2.5, 0.0, 2.5, 5.0]; yv = 0.85
        W = VGroup(*[tok(t, INK, w=1.6, h=0.55, size=24).move_to([x, 2.3, 0]) for t, x in zip(TK, gx)])
        tv = VGroup(*[mat(4, 1, EC, cell=0.36, seed=300 + i).move_to([x - 0.9, yv, 0]) for i, x in enumerate(gx)])
        pv = VGroup(*[mat(4, 1, POS, cell=0.36, seed=400 + i).move_to([x, yv, 0]) for i, x in enumerate(gx)])
        iv = VGroup(*[mat(4, 1, INP, cell=0.36, seed=500 + i).move_to([x + 0.9, yv, 0]) for i, x in enumerate(gx)])
        ops = VGroup(*[VGroup(T("+", 26, INK, BOLD).move_to([x - 0.45, yv, 0]), T("=", 26, INK, BOLD).move_to([x + 0.45, yv, 0])) for x in gx])
        pl = VGroup(*[T(f"position {i + 1}", 20, POS, BOLD).move_to([x, -0.2, 0]) for i, x in enumerate(gx)])
        lg = VGroup(swatch(EC, "token vector"), T("+", 24, INK), swatch(POS, "position vector"), T("=", 24, INK), swatch(INP, "input vector")).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.3)
        self.play(FadeIn(W), LaggedStart(*[FadeIn(v) for v in tv], lag_ratio=0.1), run_time=1.0)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(o[0]), FadeIn(p), FadeIn(l)) for o, p, l in zip(ops, pv, pl)], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(o[1]), FadeIn(v, shift=RIGHT * 0.2)) for o, v in zip(ops, iv)], lag_ratio=0.15), FadeIn(lg), run_time=1.2)
        self.cap("Fix: add a position vector to each token embedding.", hold=2.8)
        # 3. learned table
        self.play(*[FadeOut(x) for x in (W, tv, pv, iv, ops, pl, lg)], run_time=0.6)
        rows = ["1", "2", "3", "4", "5", None, "512"]; x0 = -2.4; ty = [1.9 - 0.45 * i for i in range(8)]
        R = VGroup(); L = VGroup()
        for i, r in enumerate(rows):
            if r is None: L.add(vdots(r=0.035, gap=0.07).move_to([x0, ty[i], 0])); continue
            rr = mat(1, 4, POS, cell=0.42, seed=600 + i)[0].move_to([x0, ty[i], 0]).set_opacity(0.35)
            R.add(rr); L.add(T(r, 22, GREY).next_to(rr, LEFT, buff=0.25))
        tt = T("learned position table: 512 rows (BERT)", 22, POS, BOLD).move_to([x0 + 1.4, 2.55, 0])
        self.play(FadeIn(tt), FadeIn(R), FadeIn(L), run_time=0.8)
        five = VGroup(*R[:5])
        self.play(five.animate.set_opacity(1), run_time=0.8)
        hb = SurroundingRectangle(five, color=POS, buff=0.08, stroke_width=4)
        hn = T("“The patient has a cold” uses rows 1 to 5", 22, INK).next_to(hb, RIGHT, buff=0.4)
        self.play(Create(hb), FadeIn(hn), run_time=0.7)
        r513 = Rectangle(width=1.68, height=0.42, stroke_color=GREY, stroke_width=2, fill_color="#F3F4F6", fill_opacity=1).move_to([x0, ty[7], 0])
        l513 = T("513?", 22, INK, BOLD).next_to(r513, LEFT, buff=0.25)
        xx = VGroup(Line(r513.get_corner(UL), r513.get_corner(DR)), Line(r513.get_corner(DL), r513.get_corner(UR))).set_stroke(INK, 4)
        n513 = T("longer input: no row to look up", 22, GREY).next_to(r513, RIGHT, buff=0.4)
        self.play(FadeIn(r513), FadeIn(l513), run_time=0.6)
        self.play(Create(xx), FadeIn(n513), run_time=0.7)
        self.cap("Option 1: learn one vector per position (BERT).", hold=2.8)
        # 4. sine waves
        self.play(*[FadeOut(x) for x in (tt, R, L, hb, hn, r513, l513, xx, n513)], run_time=0.6)
        wy = [1.9, 0.7, -0.5, -1.7]; amp = 0.42
        px = lambda p: -4.6 + p * 1.6
        Wv = VGroup(); Ax = VGroup(); Dt = []
        for w, y in zip(SPEEDS, wy):
            ts = np.linspace(0, 6.2, 320)
            Wv.add(VMobject(stroke_color=POS, stroke_width=4).set_points_smoothly([np.array([px(t), y + amp * np.sin(w * t), 0]) for t in ts]))
            Ax.add(Line([px(0), y, 0], [px(6.2), y, 0], color="#E5E7EB", stroke_width=2))
            Dt.append([Dot([px(p), y + amp * np.sin(w * p), 0], radius=0.09, color=INK).set_z_index(3) for p in range(1, 6)])
        WL = VGroup(*[T(s, 20, GREY).move_to([-4.85, y, 0], aligned_edge=RIGHT) for s, y in zip(("pair 1 (fast)", "pair 2", "pair 3", "pair 4 (slow)"), wy)])
        PN = VGroup(*[T(str(p), 22, INK, BOLD).move_to([px(p), -2.45, 0]) for p in range(1, 6)])
        pn = T("position", 20, GREY).move_to([-4.85, -2.45, 0], aligned_edge=RIGHT)
        self.play(FadeIn(Ax), FadeIn(WL), LaggedStart(*[Create(w) for w in Wv], lag_ratio=0.25), run_time=1.8)
        self.play(FadeIn(PN), FadeIn(pn), *[LaggedStart(*[FadeIn(d, scale=0.5) for d in row], lag_ratio=0.1) for row in Dt], run_time=1.0)
        self.cap("Option 2: compute positions from waves (original transformer).", hold=2.8)
        # 5. reading positions off the waves
        ln = DashedLine([px(1), 2.45, 0], [px(1), -2.15, 0], color=INK, stroke_width=3)
        rd = T(f"position 1: pair 1 = (sin, cos) = ({m(np.sin(1))}, {m(np.cos(1))})", 24, INK, BOLD).move_to([1.4, 2.75, 0])
        self.play(Create(ln), FadeIn(rd), *[d[0].animate.set_color(AMB).scale(1.5) for d in Dt], run_time=0.8)
        self.cap("Fast waves separate neighbors; slow waves separate distant positions.", hold=1.2)
        for p in range(2, 6):
            self.play(ln.animate.move_to([px(p), ln.get_center()[1], 0]),
                      Transform(rd, T(f"position {p}: pair 1 = (sin, cos) = ({m(np.sin(p))}, {m(np.cos(p))})", 24, INK, BOLD).move_to([1.4, 2.75, 0])),
                      *[d[p - 2].animate.set_color(INK).scale(1 / 1.5) for d in Dt], *[d[p - 1].animate.set_color(AMB).scale(1.5) for d in Dt], run_time=0.9)
            self.wait(0.6)
        self.wait(1.0)
        # 6. added once, at the input
        self.play(*[FadeOut(x) for x in (Wv, Ax, WL, PN, pn, ln, rd, *[d for row in Dt for d in row])], run_time=0.6)
        inp = box("token + position", 2.9, 0.9, "#E2E8F0", size=24, stroke=INP).move_to([-4.7, 0.3, 0])
        B = [box(s, 1.9, 0.9, "#DBEAFE", size=24, stroke=UF).move_to([x, 0.3, 0]) for s, x in (("Block 1", -1.6), ("Block 2", 0.8), ("Block 12", 4.6))]
        dots = T("…", 32, UF, BOLD).move_to([2.7, 0.3, 0])
        ar = [Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.25) for a, b in ((inp, B[0]), (B[0], B[1]))]
        ar.append(Arrow(B[1].get_right(), [2.35, 0.3, 0], buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.4))
        ar.append(Arrow([3.05, 0.3, 0], B[2].get_left(), buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.4))
        ad = T("position added once, here", 22, POS, BOLD).next_to(inp, UP, buff=0.3)
        cf = T("every later layer has to carry it forward", 22, GREY).move_to([1.5, -0.75, 0])
        self.play(FadeIn(inp), FadeIn(ad), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(x) for x in (ar[0], B[0], ar[1], B[1], ar[2], dots, ar[3], B[2])], lag_ratio=0.15), run_time=1.4)
        self.play(FadeIn(cf), run_time=0.5)
        self.cap("Both are added once, at the input.", hold=3.2)
