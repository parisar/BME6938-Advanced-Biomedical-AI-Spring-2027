from kit import *
THO, ACT, OBS, BAD = "#7C3AED", "#B45309", "#0F766E", "#DC2626"   # thought, action, observation (as in clip 2), failure red
FILLS = {THO: "#EDE9FE", ACT: "#FEF3C7", OBS: "#CCFBF1", UF: "#E0E7FF", BAD: "#FEE2E2", GREY: "#F3F4F6"}
P95, P99 = "#9CA3AF", UF                                          # bar colors for 0.95 and 0.99 per step
BASE, H = -2.0, 3.6                                               # bar baseline and the height of a probability of 1
def vbar(x, p, color, w=0.9):
    b = Rectangle(width=w, height=p * H, stroke_width=0, fill_color=color, fill_opacity=0.9).move_to([x, BASE + p * H / 2, 0])
    return VGroup(b, T(f"{p:.2f}", 22, INK, BOLD).next_to(b, UP, buff=0.1))
class C3(Clip):
    TITLE = "Errors compound over steps"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. every step can fail
        self.cap("Every step of an agent can fail.", hold=0)
        steps = ["get_labs", "read result", "get_meds", "compare", "answer"]
        S = VGroup(*[box(f"{k + 1}. {s}", 2.2, 0.7, FILLS[ACT] if s.startswith("get") else FILLS[THO], 22, ACT if s.startswith("get") else THO) for k, s in enumerate(steps)]).arrange(RIGHT, buff=0.5).move_to([0, 1.9, 0])
        SA = VGroup(*[Arrow(S[k].get_right(), S[k + 1].get_left(), buff=0.04, color=GREY, max_tip_length_to_length_ratio=0.5, stroke_width=3) for k in range(4)])
        fails = [("wrong tool", "get_meds instead of get_labs"), ("wrong argument", "P-010 instead of P-001"),
                 ("misread result", "5.6 read as 5.0"), ("loop", "calls get_labs again and again")]
        F = VGroup(*[VGroup(T(a, 22, BAD, BOLD), T(b, 22, INK)).arrange(RIGHT, buff=0.2) for a, b in fails]).arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.35), col_alignments="ll").move_to([0, 0.15, 0])
        nt = T("In ReAct, 47% of failures were reasoning errors, including repeated steps (clip 2).", 22, GREY).move_to([0, -1.55, 0])
        self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.1) for s in S], *[GrowArrow(a) for a in SA], lag_ratio=0.12), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in F], lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.4)
        # 2. 0.95 per step
        self.cap("If each step succeeds with probability 0.95, n steps succeed with 0.95ⁿ.", hold=0)
        self.play(FadeOut(VGroup(S, SA, F, nt)), run_time=0.6)
        axis = Line([-5.4, BASE, 0], [5.4, BASE, 0], color=GREY, stroke_width=3)
        xs = [-3.5, 0.0, 3.5]
        gl = VGroup(*[T(f"{n} steps", 22, INK).move_to([x, BASE - 0.35, 0]) for n, x in zip((5, 10, 20), xs)])
        fm = T("P(task succeeds) = pⁿ", 28, INK, BOLD).move_to([-2.6, 2.45, 0])
        asn = T("assumes steps fail independently (illustrative)", 20, GREY).next_to(fm, DOWN, buff=0.15).align_to(fm, LEFT)
        b95 = VGroup(*[vbar(x - 0.5, 0.95 ** n, P95) for n, x in zip((5, 10, 20), xs)])
        lg95 = VGroup(Square(0.3, stroke_width=0, fill_color=P95, fill_opacity=0.9), T("p = 0.95 per step", 22, INK)).arrange(RIGHT, buff=0.15).move_to([3.0, 2.6, 0], aligned_edge=LEFT)
        self.play(Create(axis), FadeIn(gl), FadeIn(fm), FadeIn(asn), run_time=0.8)
        self.play(FadeIn(lg95), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in b95], lag_ratio=0.35), run_time=1.6)
        self.rest(3.0)
        # 3. 0.99 per step
        self.cap("At 0.99 per step: 0.90 for 10 steps and 0.82 for 20.", hold=0)
        b99 = VGroup(*[vbar(x + 0.5, 0.99 ** n, P99) for n, x in zip((5, 10, 20), xs)])
        lg99 = VGroup(Square(0.3, stroke_width=0, fill_color=P99, fill_opacity=0.9), T("p = 0.99 per step", 22, INK)).arrange(RIGHT, buff=0.15).next_to(lg95, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(lg99), LaggedStart(*[AnimationGroup(GrowFromEdge(b[0], DOWN), FadeIn(b[1])) for b in b99], lag_ratio=0.35), run_time=1.6)
        gap = T("20 steps: 0.36 → 0.82", 24, UF, BOLD).move_to([3.5, 1.6, 0])
        self.play(FadeIn(gap, shift=UP * 0.1), run_time=0.6)
        self.rest(3.0)
        # 4. tools
        self.cap("Check results, and give the agent read-only tools.", hold=0)
        self.play(FadeOut(VGroup(axis, gl, fm, asn, b95, b99, lg95, lg99, gap)), run_time=0.6)
        ck = VGroup(T("Check results", 26, OBS, BOLD),
                    T("after get_labs, re-read the lab table", 22, INK),
                    T("4.6, 5.1, 5.6 mmol/L: matches", 22, OBS),
                    T("a mismatch stops the task", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.6, 0.5, 0])
        rows = [("get_labs", "reads", True), ("get_meds", "reads", True), ("place_order", "writes", False), ("send_message", "writes", False)]
        tl = VGroup(T("Tools the agent is given", 26, ACT, BOLD))
        for name, kind, ok in rows:
            nm = T(name, 22, INK if ok else GREY)
            r = VGroup(nm, T(kind, 22, GREY), T("given" if ok else "not given", 22, OBS if ok else BAD, BOLD)).arrange(RIGHT, buff=0.35)
            if not ok: r.add(Line(nm.get_left(), nm.get_right(), color=BAD, stroke_width=3))
            tl.add(r)
        tl.arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.0, 0.5, 0])
        self.play(FadeIn(ck[0]), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in ck[1:]], lag_ratio=0.3), run_time=1.4)
        self.play(FadeIn(tl[0]), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tl[1:]], lag_ratio=0.25), run_time=1.4)
        self.rest(2.8)
        # 5. human checkpoint
        self.cap("Any action that changes care waits for a clinician's approval.", hold=0)
        self.play(FadeOut(ck), FadeOut(tl), run_time=0.6)
        pr = box("agent proposes: repeat potassium and an ECG", 6.2, 0.8, FILLS[ACT], 24, ACT).move_to([0, 2.0, 0])
        cp = box("checkpoint: a clinician reviews", 5.2, 0.8, FILLS[UF], 24, UF).move_to([0, 0.5, 0])
        ok = box("approve: the order is placed", 4.6, 0.75, FILLS[OBS], 22, OBS).move_to([-3.3, -1.1, 0])
        no = box("reject: nothing happens", 4.6, 0.75, FILLS[BAD], 22, BAD).move_to([3.3, -1.1, 0])
        A = VGroup(Arrow(pr.get_bottom(), cp.get_top(), buff=0.1, color=GREY), Arrow(cp.get_bottom(), ok.get_top(), buff=0.1, color=GREY), Arrow(cp.get_bottom(), no.get_top(), buff=0.1, color=GREY))
        nt = T("reading the record runs on its own; orders and messages never do", 22, GREY).move_to([0, -2.25, 0])
        self.play(FadeIn(pr, shift=DOWN * 0.1), run_time=0.6)
        self.play(GrowArrow(A[0]), FadeIn(cp), run_time=0.6)
        self.play(GrowArrow(A[1]), GrowArrow(A[2]), FadeIn(ok), FadeIn(no), run_time=0.8)
        self.play(FadeIn(nt), run_time=0.5)
        self.rest(2.8)
        # 6. summary
        self.cap("Retrieval grounds answers, tools let the model act, and every step can fail.", hold=0)
        self.play(FadeOut(VGroup(pr, cp, ok, no, A, nt)), run_time=0.6)
        items = [("Retrieval", "grounds answers in sources, and can decline without one", OBS, "clip 1"),
                 ("Tools", "let the model act on real data through text it writes", ACT, "clip 2"),
                 ("Steps", "each one is another chance to fail: check, limit, ask", BAD, "clip 3")]
        R = VGroup()
        for a, b, c, d in items:
            R.add(VGroup(box(a, 2.4, 0.7, FILLS[c], 24, c), T(b, 24, INK), T(d, 20, GREY)).arrange(RIGHT, buff=0.4))
        R.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.4, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in R], lag_ratio=0.35), run_time=1.8)
        self.rest(3.4)
