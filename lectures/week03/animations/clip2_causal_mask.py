from kit import *
TK = ["The", "patient", "denies", "chest", "pain"]
S = [[1.2, .4, .3, .2, .5], [.6, 1.4, .5, .3, .2], [.3, 1.1, 1.0, .4, .6], [.2, .5, .9, 1.2, 1.5], [.1, .4, 1.3, 1.4, 1.0]]   # scores from the slides
W = [[1.00], [0.31, 0.69], [0.19, 0.43, 0.38], [0.14, 0.19, 0.28, 0.39], [0.08, 0.11, 0.28, 0.32, 0.21]]               # masked softmax, as on the slides
C, X0, Y0 = 1.05, -4.6, 2.0                        # cell size, center of the top-left cell
def at(i, j):
    return RIGHT * (X0 + j * C) + UP * (Y0 - i * C)
class C2(Clip):
    TITLE = "The causal mask"
    PACE, HOLD = 1.6, 2.5
    def construct(self):
        self.cap("Attention scores for five tokens: one row per query, one column per key.", hold=0)
        cells = [[Square(C, stroke_color=WHITE, stroke_width=2, fill_color=EC, fill_opacity=0.1 + 0.55 * S[i][j] / 1.5).move_to(at(i, j)) for j in range(5)] for i in range(5)]
        nums = [[T(f"{S[i][j]:.1f}", 24, INK).move_to(at(i, j)) for j in range(5)] for i in range(5)]
        rl = VGroup(*[T(t, 22, QC, BOLD).next_to(cells[i][0], LEFT, buff=0.18) for i, t in enumerate(TK)])
        cl = VGroup(*[T(t, 20, KC, BOLD).next_to(cells[0][j], UP, buff=0.15) for j, t in enumerate(TK)])
        lg = VGroup(T("rows: queries", 22, QC), T("columns: keys", 22, KC)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(RIGHT * 5.4 + UP * 2.75)
        allc = VGroup(*[c for r in cells for c in r]); alln = VGroup(*[n for r in nums for n in r])
        self.play(FadeIn(allc), FadeIn(rl), FadeIn(cl), FadeIn(lg), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(VGroup(*nums[i])) for i in range(5)], lag_ratio=0.3), run_time=1.4)
        self.rest(2.8)
        self.cap("“patient” must not see the words that come after it.", hold=0)
        fut = SurroundingRectangle(VGroup(*cells[1][2:]), color=AMB, buff=0.03, stroke_width=5)
        ft = T("future tokens", 22, "#B45309", BOLD).next_to(fut, RIGHT, buff=0.25)
        self.play(Create(fut), FadeIn(ft), run_time=0.7)
        self.rest(3.0)
        self.cap("The causal mask sets every score above the diagonal to minus infinity.", hold=0)
        M = [(i, j) for i in range(5) for j in range(5) if j > i]
        mi = [T("−∞", 24, WHITE, BOLD).move_to(at(i, j)) for i, j in M]
        self.play(FadeOut(fut), FadeOut(ft), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(cells[i][j].animate.set_fill(INK, 1), FadeOut(nums[i][j]), FadeIn(m)) for (i, j), m in zip(M, mi)], lag_ratio=0.08), run_time=1.6)
        self.rest(3.0)
        # softmax
        self.cap("After softmax, each row sums to 1 over allowed tokens; masked cells get 0.", hold=0)
        new = []
        for i in range(5):
            for j in range(5):
                if j <= i:
                    new.append(cells[i][j].animate.set_fill(AMB, 0.12 + 0.85 * W[i][j]))
                    new.append(Transform(nums[i][j], T(f"{W[i][j]:.2f}", 24, INK, BOLD if W[i][j] >= 0.3 else NORMAL).move_to(at(i, j))))
                else:
                    new.append(cells[i][j].animate.set_fill("#F3F4F6", 1))
        zs = [T("0", 24, GREY).move_to(at(i, j)) for i, j in M]
        sm = T("softmax per row", 22, INK, BOLD).move_to(RIGHT * 2.1 + UP * 2.75)
        self.play(FadeIn(sm), run_time=0.4)
        self.play(*new, *[ReplacementTransform(m, z) for m, z in zip(mi, zs)], run_time=1.6)
        sums = VGroup(*[T("sum = 1", 22, GREY).next_to(cells[i][4], RIGHT, buff=0.3) for i in range(5)])
        self.play(FadeIn(sums), run_time=0.5)
        self.rest(3.2)
        self.cap("“chest” attends only to The, patient, denies, and itself.", hold=0)
        rh = SurroundingRectangle(VGroup(rl[3], *cells[3]), color=QC, buff=0.05, stroke_width=4)
        self.play(Create(rh), run_time=0.5)
        self.rest(2.6)
        # every position is a training example
        self.cap("One forward pass trains every position to predict its next token.", hold=0)
        nxt = ["patient", "denies", "chest", "pain", "(next)"]
        tg = VGroup(*[T(f"→ predicts “{n}”" if n[0] != "(" else "→ predicts the next", 22, "#B45309", BOLD).move_to(RIGHT * 1.75 + UP * (Y0 - i * C), aligned_edge=LEFT) for i, n in enumerate(nxt)])
        self.play(FadeOut(rh), FadeOut(sm), sums.animate.set_opacity(0.0), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tg], lag_ratio=0.2), run_time=1.4)
        self.rest(3.4)
