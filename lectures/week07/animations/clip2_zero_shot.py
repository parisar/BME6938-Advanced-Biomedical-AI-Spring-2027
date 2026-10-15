from kit import *
IMC, TXC, BMC = "#0F766E", "#B45309", "#0F766E"    # image side, text side, BiomedCLIP bars
CLASSES = ["colorectal adenocarcinoma", "tumor stroma", "complex stroma", "lymphocytes", "necrotic debris", "normal colon mucosa", "adipose tissue", "background"]
P_TUMOR = [0.57, 0.03, 0.15, 0.03, 0.00, 0.00, 0.00, 0.22]   # real BiomedCLIP softmax for he_tumor.png, prompt "an H&E image of {class}."
PROMPTS = ["“an H&E image of …”", "“this is an image of …”", "“a histopathology image of …”"]
ZS_CLIP, ZS_BIO = [5.6, 15.1, 11.2], [38.6, 33.9, 36.4]       # zero-shot accuracy (%) on all 5,000 Kather tiles, per prompt
PROBE = [64.0, 76.5]                                          # linear probe, 10 labels per class: CLIP, BiomedCLIP
def capbox(s, size=20):
    t = T(s, size, TXC)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.3, height=0.44, stroke_color=TXC, stroke_width=2, fill_color="#FEF3C7", fill_opacity=1)
    return VGroup(r, t.move_to(r))
class C2(Clip):
    TITLE = "Zero-shot classification, and where it breaks"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        ys = [2.25 - 0.52 * k for k in range(8)]
        # 1. one prompt per class
        self.cap("Zero-shot classification starts with one text prompt per class.", hold=0)
        P = VGroup(*[capbox(f"“an H&E image of {c}”").move_to([-6.6, y, 0], aligned_edge=LEFT) for c, y in zip(CLASSES, ys)])
        hd = T("8 tissue classes, 8 prompts", 22, TXC, BOLD).next_to(P, UP, buff=0.2).align_to(P, LEFT)
        self.play(FadeIn(hd), LaggedStart(*[FadeIn(p, shift=RIGHT * 0.15) for p in P], lag_ratio=0.12), run_time=1.6)
        self.rest(2.6)
        # 2. prompts -> class vectors = classifier weights
        self.cap("The text encoder turns the prompts into class vectors: a linear classifier written in text.", hold=0)
        te = box("Text\nencoder", 1.3, 4.3, "#FEF3C7", size=24, stroke=TXC).move_to([0.5, 0.43, 0])
        ar = VGroup(*[Arrow([P.get_right()[0] + 0.05, y, 0], [te.get_left()[0], y, 0], buff=0.05, stroke_width=2.5, color=INK, max_tip_length_to_length_ratio=0.3) for y in ys])
        V = VGroup(*[mat(1, 5, TXC, cell=0.3, seed=20 + k).move_to([2.2, y, 0]) for k, y in enumerate(ys)])
        vo = VGroup(*[Arrow([te.get_right()[0], y, 0], [1.42, y, 0], buff=0.03, stroke_width=2.5, color=INK, max_tip_length_to_length_ratio=0.3) for y in ys])
        VL = VGroup(*[T(c, 20, INK).next_to(v, RIGHT, buff=0.2) for c, v in zip(CLASSES, V)])
        wl = T("one weight vector per class", 20, TXC, BOLD).next_to(V, UP, buff=0.2).align_to(V, LEFT)
        self.play(LaggedStart(*[GrowArrow(a) for a in ar], lag_ratio=0.05), FadeIn(te), run_time=0.9)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(o), FadeIn(v), FadeIn(l)) for o, v, l in zip(vo, V, VL)], lag_ratio=0.08), FadeIn(wl), run_time=1.3)
        self.rest(2.8)
        # 3. match a tile against every class vector
        self.cap("A tile is compared with every class vector, and the softmax picks a class: no training needed.", hold=0)
        self.play(FadeOut(VGroup(P, hd, ar, te, vo, V, wl, VL)), run_time=0.6)
        tl = ImageMobject(he_image("he_tumor.png", 240)).set_height(1.7).move_to([-5.7, 0.45, 0])
        tll = T("tumor tile", 20, INK, BOLD).next_to(tl, DOWN, buff=0.15)
        ie = box("Image\nencoder", 1.6, 1.2, "#CCFBF1", size=22, stroke=IMC).move_to([-3.45, 0.45, 0])
        z = mat(5, 1, IMC, cell=0.3, seed=7).move_to([-1.95, 0.45, 0])
        a1 = Arrow(tl.get_right(), ie.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        a2 = Arrow(ie.get_right(), z.get_left(), buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.3)
        a3 = Arrow(z.get_right(), [-0.1, 0.45, 0], buff=0.1, stroke_width=3, color=INK, max_tip_length_to_length_ratio=0.25)
        a3l = VGroup(T("cosine with", 20, INK), T("each class,", 20, INK), T("softmax", 20, INK)).arrange(DOWN, buff=0.05).next_to(a3, DOWN, buff=0.15).shift(RIGHT * 0.2)
        bx = 3.25                                        # left edge of the bars
        bars = VGroup(*[Rectangle(width=max(3.6 * p, 0.03), height=0.34, stroke_width=0, fill_color=BMC if k == 0 else "#9CA3AF", fill_opacity=1).move_to([bx, y, 0], aligned_edge=LEFT) for k, (p, y) in enumerate(zip(P_TUMOR, ys))])
        bl = VGroup(*[T(c, 20, INK).next_to(np.array([bx - 0.12, y, 0]), LEFT, buff=0) for c, y in zip(CLASSES, ys)])
        bn = VGroup(*[T(f"{p:.2f}", 20, INK, BOLD if k == 0 else NORMAL).next_to(b, RIGHT, buff=0.1) for k, (p, b) in enumerate(zip(P_TUMOR, bars))])
        src = T("BiomedCLIP, real output for this tile", 20, GREY).move_to([3.0, -2.45, 0])
        cr = T(HE_CREDIT, 20, GREY).move_to([-4.2, -2.45, 0])
        self.play(FadeIn(tl), FadeIn(tll), FadeIn(cr), GrowArrow(a1), FadeIn(ie), run_time=0.8)
        self.play(GrowArrow(a2), FadeIn(z), GrowArrow(a3), FadeIn(a3l), run_time=0.8)
        self.play(FadeIn(bl), LaggedStart(*[AnimationGroup(GrowFromEdge(b, LEFT), FadeIn(n)) for b, n in zip(bars, bn)], lag_ratio=0.1), FadeIn(src), run_time=1.3)
        self.rest(3.0)
        # 4. CLIP on ImageNet
        self.cap("On ImageNet, CLIP's best model reaches 76.2% zero-shot, matching a supervised ResNet-50.", hold=0)
        self.play(FadeOut(Group(tl, tll, ie, z, a1, a2, a3, a3l, bars, bl, bn, src, cr)), run_time=0.6)
        k1 = VGroup(T("76.2%", 48, UF, BOLD), T("CLIP, zero-shot on ImageNet", 24, INK), T("no ImageNet labels used", 22, GREY)).arrange(DOWN, buff=0.15).move_to([-3.3, 0.6, 0])
        k2 = VGroup(T("≈ 76%", 48, GREY, BOLD), T("ResNet-50, supervised", 24, INK), T("1.28 million labeled images", 22, GREY)).arrange(DOWN, buff=0.15).move_to([3.3, 0.6, 0])
        nt = T("The same paper reports that CLIP is weak on lymph node tumor detection (PatchCamelyon).", 20, GREY).move_to([0, -1.6, 0])
        rf = T("Radford et al., ICML 2021", 20, GREY).move_to([0, -2.45, 0])
        self.play(FadeIn(k1, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(k2, shift=UP * 0.15), run_time=0.7)
        self.play(FadeIn(nt), FadeIn(rf), run_time=0.6)
        self.rest(3.0)
        # 5. general CLIP on the Kather tiles
        self.cap("On 5,000 H&E tiles in 8 classes, general CLIP scores 5.6 to 15.1%; chance is 12.5%.", hold=0)
        self.play(FadeOut(VGroup(k1, k2, nt, rf)), run_time=0.6)
        y0, sc = -1.95, 0.042                              # chart baseline and height per percentage point
        ax = Line([-6.4, y0, 0], [6.4, y0, 0], color=INK, stroke_width=2)
        def group(vals, cx, color, ops):
            bs = VGroup(*[Rectangle(width=0.7, height=v * sc, stroke_width=0, fill_color=color, fill_opacity=o).move_to([cx + (k - (len(vals) - 1) / 2) * 0.95, y0, 0], aligned_edge=DOWN) for k, (v, o) in enumerate(zip(vals, ops))]).shift(RIGHT * 0)
            ns = VGroup(*[T(f"{v:.1f}%".replace(".0%", "%"), 20, INK, BOLD).next_to(b, UP, buff=0.08) for v, b in zip(vals, bs)])
            return bs, ns
        OPS = [1.0, 0.65, 0.35]
        cb, cn = group(ZS_CLIP, -4.2, "#6B7280", OPS)
        ch = DashedLine([-6.4, y0 + 12.5 * sc, 0], [6.4, y0 + 12.5 * sc, 0], color=AMB, stroke_width=3, dash_length=0.12)
        chl = T("chance: 12.5%", 20, AMB, BOLD).move_to([5.9, y0 + 12.5 * sc + 0.85, 0])
        chp = Arrow(chl.get_bottom(), [5.9, y0 + 12.5 * sc + 0.05, 0], buff=0.05, stroke_width=2.5, color=AMB, max_tip_length_to_length_ratio=0.25)
        g1 = T("general CLIP\nzero-shot", 20, INK, BOLD).move_to([-4.2, y0 - 0.45, 0])
        lg = VGroup(*[VGroup(Square(0.26, stroke_width=0, fill_color="#6B7280", fill_opacity=o), T(p, 20, INK)).arrange(RIGHT, buff=0.15) for p, o in zip(PROMPTS, OPS)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.3, 2.35, 0])
        lgt = T("prompt wording", 20, GREY).next_to(lg, LEFT, buff=0.3).align_to(lg, UP)
        self.play(Create(ax), FadeIn(lg), FadeIn(lgt), run_time=0.6)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in cb], lag_ratio=0.2), FadeIn(cn), FadeIn(g1), run_time=1.0)
        self.play(Create(ch), FadeIn(chl), GrowArrow(chp), run_time=0.7)
        lo = SurroundingRectangle(VGroup(cb[0], cn[0]), color=AMB, buff=0.1, stroke_width=4)
        bc = T("below chance", 20, AMB, BOLD).next_to(lo, UP, buff=0.1).align_to(lo, RIGHT)
        self.play(Create(lo), FadeIn(bc), run_time=0.5)
        self.rest(3.2)
        # 6. BiomedCLIP
        self.cap("BiomedCLIP, trained on biomedical figures, scores 34 to 39%: better, but far from reliable.", hold=0)
        bb, bnn = group(ZS_BIO, -0.6, BMC, OPS)
        g2 = T("BiomedCLIP\nzero-shot", 20, BMC, BOLD).move_to([-0.6, y0 - 0.45, 0])
        self.play(FadeOut(lo), FadeOut(bc), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.2), FadeIn(bnn), FadeIn(g2), run_time=1.1)
        self.rest(3.2)
        # 7. a few labels
        self.cap("A linear probe with only 10 labels per class reaches 64% with CLIP and 77% with BiomedCLIP.", hold=0)
        pb = VGroup(Rectangle(width=0.62, height=PROBE[0] * sc, stroke_width=0, fill_color="#6B7280", fill_opacity=1).move_to([3.35, y0, 0], aligned_edge=DOWN),
                    Rectangle(width=0.62, height=PROBE[1] * sc, stroke_width=0, fill_color=BMC, fill_opacity=1).move_to([4.1, y0, 0], aligned_edge=DOWN))
        pn = VGroup(*[T(s, 20, INK, BOLD).next_to(b, UP, buff=0.08) for s, b in zip(["64%", "77%"], pb)])
        pl = VGroup(T("CLIP", 20, INK), T("Biomed", 20, BMC)).arrange(RIGHT, buff=0.15).move_to([3.72, y0 - 0.25, 0])
        g3 = T("linear probe, 10 labels/class", 20, INK, BOLD).move_to([3.72, y0 - 0.6, 0])
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in pb], lag_ratio=0.3), FadeIn(pn), FadeIn(pl), FadeIn(g3), run_time=1.1)
        self.rest(3.4)
