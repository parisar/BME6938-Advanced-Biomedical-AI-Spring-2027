from kit import *
TS, NP = 3.6, 4                                    # tile size on screen, patches per side
def he_tile(n=320, seed=3):
    """Synthetic H&E tile: pink stroma, purple nuclei, denser nuclei in one corner. Not patient data."""
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:n, 0:n]
    img = np.zeros((n, n, 3)); img[:] = [246, 205, 222]
    f = np.sin(xx / 23 + 2 * np.sin(yy / 41)) + 0.6 * np.sin(yy / 17 + xx / 53)
    img[f > 0.9] = [234, 166, 200]
    img[(f > 0.2) & (f < 0.35)] = [240, 184, 210]
    for k in range(190):
        if k < 70: cx, cy = rng.uniform(0.55 * n, n), rng.uniform(0, 0.45 * n)      # crowded region
        else: cx, cy = rng.uniform(0, n, 2)
        a, b, t = rng.uniform(5, 10), rng.uniform(3.5, 6.5), rng.uniform(0, np.pi)
        dx, dy = xx - cx, yy - cy
        u = (dx * np.cos(t) + dy * np.sin(t)) / a; v = (-dx * np.sin(t) + dy * np.cos(t)) / b
        img[u * u + v * v < 1] = np.array([88, 42, 128]) * rng.uniform(0.85, 1.15)
    return np.clip(img, 0, 255).astype(np.uint8)
class C3(Clip):
    TITLE = "Vision transformer: an image as a sequence of patches"
    PACE, HOLD = 1.2, 0.8
    def construct(self):
        arr = he_tile(); n = arr.shape[0]; ps = n // NP; cp = TS / NP
        ctr = np.array([-3.4, 0.1, 0])
        tile = ImageMobject(arr).set_height(TS).move_to(ctr)
        tl = T("H&E pathology tile (synthetic)", 22, GREY).next_to(tile, DOWN, buff=0.25)
        self.play(FadeIn(tile), FadeIn(tl), run_time=0.8)
        self.cap("A vision transformer reads an image as a sequence of patches.", hold=2.6)
        x0, y0 = ctr[0] - TS / 2, ctr[1] + TS / 2
        grid = VGroup(*[Line([x0 + k * cp, y0, 0], [x0 + k * cp, y0 - TS, 0]) for k in range(1, NP)],
                      *[Line([x0, y0 - k * cp, 0], [x0 + TS, y0 - k * cp, 0]) for k in range(1, NP)]).set_stroke(WHITE, 5)
        self.play(Create(grid), run_time=0.9)
        self.cap("Cut the pathology tile into a 4 × 4 grid of patches.", hold=2.4)
        P = [ImageMobject(arr[r * ps:(r + 1) * ps, c * ps:(c + 1) * ps]).set_height(cp).move_to([x0 + (c + 0.5) * cp, y0 - (r + 0.5) * cp, 0]) for r in range(NP) for c in range(NP)]
        self.add(*P); self.remove(tile)
        self.play(*[p.animate.shift((RIGHT * 0.14 * ((k % 4) - 1.5) + DOWN * 0.14 * ((k // 4) - 1.5))) for k, p in enumerate(P)], FadeOut(grid), run_time=0.6)
        # sequence of tokens: slot 0 is reserved for [CLS]
        xs = [-6.05] + [-5.3 + k * 0.66 for k in range(16)]; YP, YV, YN = 2.15, 0.95, 0.05
        self.play(FadeOut(tl), *[p.animate.set_height(0.55).move_to([xs[k + 1], YP, 0]) for k, p in enumerate(P)], run_time=1.6)
        lp = T("16 patches", 20, GREY, BOLD).move_to([5.15, YP, 0], aligned_edge=LEFT)
        self.play(FadeIn(lp), run_time=0.4)
        self.cap("The 16 patches line up into a sequence of 16 tokens.", hold=2.4)
        V = [mat(3, 1, EC, cell=0.36, seed=100 + k).move_to([xs[k + 1], YV, 0]) for k in range(16)]
        lv = T("projection", 20, EC, BOLD).move_to([5.15, YV, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(v, shift=DOWN * 0.25) for v in V], lag_ratio=0.06), FadeIn(lv), run_time=1.4)
        self.cap("A linear projection turns each patch into a d-dimensional vector.", hold=2.6)
        PN = [T(str(k + 1), 20, PC, BOLD).move_to([xs[k + 1], YN, 0]) for k in range(16)]
        ln = T("+ position", 20, PC, BOLD).move_to([5.15, YN, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(t) for t in PN], lag_ratio=0.05), FadeIn(ln), run_time=1.0)
        self.cap("A position vector tells the model where each patch came from.", hold=2.8)
        cls = tok("CLS", UF, w=0.85, h=0.55, size=20, fill="#DBEAFE").move_to([xs[0], YP, 0])
        cv = mat(3, 1, UF, cell=0.36, seed=99).move_to([xs[0], YV, 0])
        cn = T("0", 20, PC, BOLD).move_to([xs[0], YN, 0])
        self.play(FadeIn(cls, shift=RIGHT * 0.3), FadeIn(cv), FadeIn(cn), run_time=0.8)
        self.cap("A learnable [CLS] token is added at the front of the sequence.", hold=2.6)
        enc = box("Transformer encoder, unchanged from text", 11.3, 0.8, "#DBEAFE", size=26, stroke=UF).move_to([(xs[0] + xs[16]) / 2, -1.0, 0])
        self.play(FadeIn(enc, shift=DOWN * 0.2), run_time=0.8)
        self.cap("The sequence of 17 tokens enters a standard transformer encoder.", hold=2.6)
        a1 = Arrow([xs[0], enc.get_bottom()[1], 0], [xs[0], -1.95, 0], buff=0.05, stroke_width=4, color=UF, max_tip_length_to_length_ratio=0.3)
        ov = mat(1, 3, OC, cell=0.36, seed=7).move_to([xs[0] + 0.25, -2.25, 0])
        head = box("Head: tumor / normal", 3.2, 0.6, "#FEF3C7", size=22, stroke="#B45309").move_to([-2.4, -2.25, 0])
        a2 = Arrow(ov.get_right(), head.get_left(), buff=0.1, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.2)
        self.play(GrowArrow(a1), FadeIn(ov), run_time=0.6)
        self.play(GrowArrow(a2), FadeIn(head), run_time=0.7)
        self.cap("The [CLS] output feeds a prediction head: tumor or normal.", hold=2.6)
        fact = VGroup(T("224 × 224 image, 16 × 16 patches", 22, INK, BOLD), T("14 × 14 = 196 tokens, plus [CLS]", 22, INK)).arrange(DOWN, buff=0.12).move_to([3.4, -2.2, 0])
        self.play(FadeIn(fact), run_time=0.6)
        self.cap("A 224 × 224 image with 16 × 16 patches gives 196 tokens.", hold=3.2)
