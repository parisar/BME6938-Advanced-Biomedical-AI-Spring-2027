from kit import *
FRZ, FRZF = "#0369A1", "#E0F2FE"                  # frozen: ice blue
TRN, TRNF = "#B45309", "#FEF3C7"                  # trainable: amber
NRM = "#0F766E"                                   # normal sinus rhythm (AF uses PC, as in clip 2)
def lock(s=1.0, color=FRZ):
    body = RoundedRectangle(corner_radius=0.05, width=0.5, height=0.4, stroke_width=0, fill_color=color, fill_opacity=1)
    sh = Arc(radius=0.16, start_angle=0, angle=PI, stroke_color=color, stroke_width=6).next_to(body, UP, buff=-0.02)
    return VGroup(sh, body).scale(s)
def tag(s, color, fill, size=20):
    return tok(s, color, w=1.0, h=0.42, size=size, fill=fill)
class C3(Clip):
    TITLE = "Linear probing: what did the encoder learn?"
    def construct(self):
        enc = box("Pretrained encoder", 4.2, 1.6, "#E2E8F0", size=30, stroke=EC).move_to(UP * 0.4)
        self.play(FadeIn(enc), run_time=0.6)
        lk = lock(1.3).next_to(enc, UP, buff=0.25)
        fz = T("frozen", 26, FRZ, BOLD).next_to(lk, RIGHT, buff=0.25)
        self.play(enc[0].animate.set_fill(FRZF).set_stroke(FRZ), FadeIn(lk, shift=DOWN * 0.2), FadeIn(fz), run_time=0.8)
        self.cap("Take the pretrained encoder and freeze its weights.", hold=2.6)
        # small labeled set
        ys = [2.1, 1.3, 0.5, -0.3, -1.1, -1.9]; af = [True, False, True, False, False, True]
        encS = box("Frozen\nencoder", 1.5, 3.8, FRZF, size=24, stroke=FRZ).move_to(RIGHT * -2.75 + UP * 0.1)
        self.play(FadeOut(fz), Transform(enc, encS), lk.animate.scale(0.75).move_to(RIGHT * -2.75 + UP * 2.4), run_time=0.8)
        St = VGroup(*[wave(ecg_fn(4, hr=70 + 4 * i, af=a, seed=40 + i), 0.2, 3.2, 1.9, 0.42, sw=2.5).move_to(RIGHT * -5.7 + UP * y) for i, (a, y) in enumerate(zip(af, ys))])
        Tg = VGroup(*[(tag("AF", PC, "#EDE9FE") if a else tag("Normal", NRM, "#CCFBF1")).move_to(RIGHT * -4.2 + UP * y) for a, y in zip(af, ys)])
        self.play(LaggedStart(*[AnimationGroup(Create(s), FadeIn(t)) for s, t in zip(St, Tg)], lag_ratio=0.15), run_time=1.6)
        self.cap("Now use a small labeled set: atrial fibrillation versus normal sinus rhythm.", hold=3.2)
        # embeddings
        pl = Rectangle(width=4.0, height=4.4, stroke_color=GREY, stroke_width=2).move_to(RIGHT * 0.6 + UP * 0.1)
        oa = Arrow(enc.get_right(), pl.get_left(), buff=0.06, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.35)
        rng = np.random.default_rng(9); mid = np.array([0.6, 0.1, 0]); u = np.array([0.74, -0.67, 0]); nrm = np.array([0.67, 0.74, 0])
        def pts(n, side):
            out = []
            while len(out) < n:
                p = mid + side * nrm * rng.uniform(0.45, 1.5) + u * rng.uniform(-1.4, 1.4)
                if abs(p[0] - 0.6) < 1.8 and abs(p[1] - 0.1) < 2.0: out.append(p)
            return out
        pa, pn = pts(8, 1), pts(8, -1)
        main = [pa.pop() if a else pn.pop() for a in af]
        Dm = VGroup(*[Dot(p, radius=0.12, color=PC if a else NRM) for p, a in zip(main, af)])
        Dx = VGroup(*[Dot(p, radius=0.12, color=PC) for p in pa], *[Dot(p, radius=0.12, color=NRM) for p in pn])
        col = mat(6, 1, EC, cell=0.36, seed=81).move_to(RIGHT * -0.6 + UP * 0.1)
        cl = T("z: 256 numbers", 22, EC, BOLD).next_to(col, RIGHT, buff=0.25)
        pll = T("each point: one embedding, drawn in 2D", 20, GREY).next_to(pl, DOWN, buff=0.15)
        self.play(GrowArrow(oa), Create(pl), FadeIn(pll), run_time=0.7)
        self.play(Indicate(St[0], color=PC), FadeIn(col, shift=RIGHT * 0.3), FadeIn(cl), run_time=0.9)
        self.play(Transform(col, Dm[0]), FadeOut(cl), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in [*Dm[1:], *Dx]], lag_ratio=0.08), run_time=1.2)
        self.cap("The frozen encoder turns each ECG into a 256-dimensional embedding.", hold=3.0)
        # linear head
        hr = RoundedRectangle(corner_radius=0.12, width=3.8, height=1.5, stroke_color=TRN, stroke_width=3, fill_color=TRNF, fill_opacity=1).move_to(RIGHT * 4.85 + UP * 0.6)
        ht = VGroup(T("Linear head", 24, TRN, BOLD), T("p(AF) = σ( w·z + b )", 24, INK)).arrange(DOWN, buff=0.15).move_to(hr)
        head = VGroup(hr, ht)
        hn = T("256 weights + 1 bias", 22, GREY).next_to(hr, DOWN, buff=0.25)
        ha = Arrow(pl.get_right() + UP * 0.5, hr.get_left(), buff=0.06, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.35)
        self.play(GrowArrow(ha), FadeIn(head), run_time=0.7); self.play(FadeIn(hn), run_time=0.4)
        self.cap("Add one linear prediction head: a weighted sum of the embedding plus a bias.", hold=3.2)
        # gradients stop at the encoder
        gp = VMobject(stroke_color=AMB, stroke_width=5).set_points_as_corners([hr.get_top() + UP * 0.05, RIGHT * hr.get_center()[0] + UP * 2.85, RIGHT * -1.55 + UP * 2.85])
        tip = Triangle(fill_color=AMB, fill_opacity=1, stroke_width=0).scale(0.13).rotate(PI / 2).move_to(RIGHT * -1.6 + UP * 2.85)
        gl = T("gradient", 22, TRN, BOLD).move_to(RIGHT * 3.6 + UP * 2.55)
        xx = VGroup(Line(UL, DR), Line(DL, UR)).scale(0.17).set_stroke(QC, 6).move_to(RIGHT * -2.0 + UP * 2.85)
        ng = T("no gradient", 22, QC, BOLD).move_to(RIGHT * -0.55 + UP * 2.55)
        self.play(Create(gp), FadeIn(gl), run_time=1.0)
        self.play(FadeIn(tip), Create(xx), FadeIn(ng), Indicate(lk, color=FRZ, scale_factor=1.3), run_time=0.8)
        self.cap("Training updates only the head; the encoder gets no gradient.", hold=3.0)
        # decision boundary
        ln = Line(mid - 1.95 * u, mid + 1.95 * u, color=INK, stroke_width=5).rotate(1.1, about_point=mid)
        self.play(Create(ln), run_time=0.5)
        self.play(Rotate(ln, -1.1, about_point=mid), run_time=1.4)
        sa = T("AF", 24, PC, BOLD).move_to(RIGHT * 2.2 + UP * 2.0)
        sn = T("Normal", 24, NRM, BOLD).move_to(RIGHT * -0.7 + DOWN * 1.8)
        self.play(FadeIn(sa), FadeIn(sn), run_time=0.5)
        self.cap("If one line separates the classes, the information is already in the embedding.", hold=3.4)
        # probe versus fine-tuning
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.title, self._cap)], run_time=0.7)
        def panel(name, cx, enc_frozen, count):
            e = box("Encoder", 2.3, 1.2, FRZF if enc_frozen else TRNF, size=26, stroke=FRZ if enc_frozen else TRN).move_to(RIGHT * (cx - 1.25) + UP * 0.3)
            h = box("Head", 1.5, 1.2, TRNF, size=26, stroke=TRN).move_to(RIGHT * (cx + 1.55) + UP * 0.3)
            a = Arrow(e.get_right(), h.get_left(), buff=0.08, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
            el = T("frozen" if enc_frozen else "trainable", 22, FRZ if enc_frozen else TRN, BOLD).next_to(e, DOWN, buff=0.2)
            hl = T("trainable", 22, TRN, BOLD).next_to(h, DOWN, buff=0.2)
            g = VGroup(T(name, 30, INK, BOLD).move_to(RIGHT * cx + UP * 2.0), e, h, a, el, hl, T(count, 24, INK).move_to(RIGHT * cx + DOWN * 1.6))
            if enc_frozen: g.add(lock(0.8).next_to(e, UP, buff=0.12).align_to(e, RIGHT))
            return g
        L = panel("Linear probe", -3.55, True, "257 trainable weights")
        R = panel("Fine-tuning", 3.55, False, "every weight is trainable")
        dv = DashedLine(UP * 2.4, DOWN * 2.2, color=GREY, stroke_width=2)
        self.play(FadeIn(L), run_time=0.8); self.play(Create(dv), FadeIn(R), run_time=0.8)
        self.cap("Fine-tuning updates the encoder too, so a probe is the cleaner test of pretraining.", hold=3.6)
        # the same probe for pathology
        self.play(FadeOut(VGroup(L, R, dv)), run_time=0.6)
        tum = ImageMobject(he_image("he_tumor.png", 320)).set_height(1.7).move_to([-5.2, 1.25, 0])
        muc = ImageMobject(he_image("he_mucosa.png", 320)).set_height(1.7).move_to([-5.2, -1.1, 0])
        tl = T("tumor", 22, INK, BOLD).next_to(tum, DOWN, buff=0.15)
        ml = T("normal mucosa", 22, INK, BOLD).next_to(muc, DOWN, buff=0.15)
        enc3 = box("Frozen\nencoder", 2.0, 2.6, FRZF, size=26, stroke=FRZ).move_to([-1.3, 0.05, 0])
        lk3 = lock(0.9).next_to(enc3, UP, buff=0.12)
        i1 = Arrow(tum.get_right(), enc3.get_left() + UP * 0.6, buff=0.12, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.2)
        i2 = Arrow(muc.get_right(), enc3.get_left() + DOWN * 0.6, buff=0.12, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.2)
        hd3 = box("Linear head", 2.6, 0.9, TRNF, size=24, stroke=TRN).move_to([2.1, 0.05, 0])
        o1 = Arrow(enc3.get_right(), hd3.get_left(), buff=0.1, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.25)
        out = T("tumor / normal", 26, INK, BOLD).move_to([5.5, 0.05, 0])
        o2 = Arrow(hd3.get_right(), out.get_left(), buff=0.12, stroke_width=3.5, color=INK, max_tip_length_to_length_ratio=0.3)
        cr = T(HE_CREDIT, 20, GREY).move_to([3.6, -2.4, 0])
        self.play(FadeIn(tum), FadeIn(muc), FadeIn(tl), FadeIn(ml), FadeIn(cr), run_time=0.7)
        self.play(GrowArrow(i1), GrowArrow(i2), FadeIn(enc3), FadeIn(lk3), run_time=0.8)
        self.play(GrowArrow(o1), FadeIn(hd3), GrowArrow(o2), FadeIn(out), run_time=0.8)
        self.cap("The same probe works for pathology: tumor versus normal mucosa.", hold=3.4)
