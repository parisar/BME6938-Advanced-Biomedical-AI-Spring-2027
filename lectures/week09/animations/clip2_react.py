from kit import *
THO, ACT, OBS = "#7C3AED", "#B45309", "#0F766E"            # thought purple, action amber, observation teal
FILLS = {THO: "#EDE9FE", ACT: "#FEF3C7", OBS: "#CCFBF1", UF: "#E0E7FF", GREY: "#F3F4F6"}
def tag(s, color, w=2.2):
    return box(s, w, 0.5, FILLS[color], size=20, stroke=color)
def line(kind, color, texts, y, size=22):
    """One transcript entry: a colored tag and one or more lines of text to its right."""
    t = tag(kind, color).move_to([-5.6, y, 0])
    tx = VGroup(*[T(s, size, INK) for s in texts]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    tx.next_to(t, RIGHT, buff=0.3).align_to(t, UP).shift(DOWN * 0.07)
    return VGroup(t, tx)
def hbars(rows, y0, unit, x0=-1.4, gap=0.62, hi=()):
    """Horizontal bars: label right-aligned at x0, bar from x0, value after the bar; rows in `hi` drawn in UF blue."""
    g = VGroup()
    for i, (lab, v, s) in enumerate(rows):
        y = y0 - i * gap
        l = T(lab, 22, INK).move_to([x0 - 0.25, y, 0], aligned_edge=RIGHT)
        b = Rectangle(width=v * unit, height=0.4, stroke_width=0, fill_color=UF if i in hi else "#9CA3AF", fill_opacity=0.85).move_to([x0 + v * unit / 2, y, 0])
        g.add(VGroup(l, b, T(s, 22, INK, BOLD).next_to(b, RIGHT, buff=0.15)))
    return g
class C2(Clip):
    TITLE = "Reason, act, observe: tool calls"
    PACE, HOLD = 1.1, 0.4
    def construct(self):
        # 1. the loop
        self.cap("An agent repeats a cycle: thought, action, observation.", hold=0)
        task = VGroup(T("Task: is P-001's potassium rising, and is it abnormal?", 26, INK, BOLD), T("synthetic patient", 20, GREY)).arrange(DOWN, buff=0.12).move_to([0, 2.35, 0])
        nodes = VGroup(box("Thought", 2.6, 0.7, FILLS[THO], 24, THO).move_to([0, 0.85, 0]),
                       box("Action", 2.6, 0.7, FILLS[ACT], 24, ACT).move_to([2.6, -1.25, 0]),
                       box("Observation", 2.6, 0.7, FILLS[OBS], 24, OBS).move_to([-2.6, -1.25, 0]))
        arcs = VGroup(CurvedArrow(nodes[0].get_right() + RIGHT * 0.1, nodes[1].get_top() + UP * 0.1, angle=-PI / 3, color=GREY),
                      CurvedArrow(nodes[1].get_bottom() + DOWN * 0.1 + LEFT * 0.4, nodes[2].get_bottom() + DOWN * 0.1 + RIGHT * 0.4, angle=-PI / 3, color=GREY),
                      CurvedArrow(nodes[2].get_top() + UP * 0.1, nodes[0].get_left() + LEFT * 0.1, angle=-PI / 3, color=GREY))
        self.play(FadeIn(task, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(n), Create(a)) for n, a in zip(nodes, arcs)], lag_ratio=0.4), run_time=1.8)
        self.rest(2.4)
        # 2. thought and action
        self.cap("Thought, then action: the model writes the tool call as JSON.", hold=0)
        self.play(FadeOut(nodes), FadeOut(arcs), task.animate.scale(0.85).move_to([0, 2.6, 0]), run_time=0.7)
        L1 = line("Thought", THO, ["I need the last three potassium results."], 1.75)
        L2 = line("Action", ACT, ['{"tool": "get_labs",', ' "args": {"patient_id": "P-001", "test": "potassium", "last": 3}}'], 1.0)
        self.play(FadeIn(L1, shift=RIGHT * 0.1), run_time=0.7)
        self.play(FadeIn(L2, shift=RIGHT * 0.1), run_time=0.8)
        self.rest(3.0)
        # 3. observation
        self.cap("Observation: the program runs the tool and adds the result to the context.", hold=0)
        L3 = line("Observation", OBS, ["potassium: 4.6, 5.1, 5.6 mmol/L"], -0.15)
        ax = Axes(x_range=[0, 4, 1], y_range=[4, 6, 0.5], x_length=3.0, y_length=1.8, tips=False,
                  axis_config={"color": GREY, "stroke_width": 2, "include_ticks": False}).move_to([4.4, -0.55, 0])
        pts = [ax.c2p(k + 1, v) for k, v in enumerate([4.6, 5.1, 5.6])]
        lim = DashedLine(ax.c2p(0, 5.0), ax.c2p(4, 5.0), color="#DC2626", stroke_width=3)
        ll = T("upper limit ≈ 5.0", 20, "#DC2626").next_to(lim, LEFT, buff=0.15)
        pl = VGroup(VMobject(color=OBS, stroke_width=4).set_points_as_corners(pts), *[Dot(p, radius=0.08, color=OBS) for p in pts])
        self.play(FadeIn(L3, shift=RIGHT * 0.1), run_time=0.8)
        self.play(Create(ax), Create(pl), run_time=1.0)
        self.play(Create(lim), FadeIn(ll), run_time=0.6)
        self.rest(2.8)
        # 4. thought and finish
        self.cap("Thought: rising, and 5.6 is above the usual upper limit of about 5.0.", hold=0)
        L4 = line("Thought", THO, ["Rising, and 5.6 is above the usual upper limit of about 5.0."], -1.1)
        L5 = line("Action", ACT, ['finish("Potassium is rising: 4.6, 5.1, 5.6 mmol/L;', ' 5.6 is above the upper limit.")'], -1.85)
        self.play(FadeOut(VGroup(ax, pl, lim, ll)), run_time=0.4)
        self.play(FadeIn(L4, shift=RIGHT * 0.1), run_time=0.8)
        self.play(FadeIn(L5, shift=RIGHT * 0.1), run_time=0.8)
        self.rest(2.8)
        # 5. a tool call is text
        self.cap("A tool call is just text in an agreed format; ReAct learned it from a few examples.", hold=0)
        self.play(FadeOut(VGroup(task, L1, L2, L3, L4, L5)), run_time=0.6)
        m = box("language model", 3.0, 0.8, "#F3F4F6", 24).move_to([-4.7, 1.3, 0])
        js = box('{"tool": "get_labs", …}', 3.6, 0.8, FILLS[ACT], 22, ACT).move_to([0.6, 1.3, 0])
        pg = box("program: parse, run get_labs", 4.0, 0.8, "#F3F4F6", 22).move_to([0.6, -0.3, 0])
        db = box("lab results", 2.4, 0.8, FILLS[OBS], 22, OBS).move_to([5.2, -0.3, 0])
        rs = box("4.6, 5.1, 5.6", 2.6, 0.8, FILLS[OBS], 22, OBS).move_to([-4.7, -0.3, 0])
        A = VGroup(Arrow(m.get_right(), js.get_left(), buff=0.1, color=GREY), Arrow(js.get_bottom(), pg.get_top(), buff=0.1, color=GREY),
                   DoubleArrow(pg.get_right(), db.get_left(), buff=0.1, color=GREY, tip_length=0.2), Arrow(pg.get_left(), rs.get_right(), buff=0.1, color=GREY),
                   Arrow(rs.get_top(), m.get_bottom(), buff=0.1, color=GREY))
        lab = VGroup(T("writes text", 20, GREY).next_to(A[0], UP, buff=0.1), T("appended to the context", 20, GREY).next_to(A[4], RIGHT, buff=0.15))
        notes = VGroup(T("ReAct (2022): a few worked examples in the prompt of PaLM 540B, no training", 22, INK),
                       T("Today: models are post-trained to write tool calls (Week 5)", 22, UF)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([0, -1.95, 0])
        self.play(FadeIn(m), run_time=0.4)
        self.play(GrowArrow(A[0]), FadeIn(js), FadeIn(lab[0]), run_time=0.7)
        self.play(GrowArrow(A[1]), FadeIn(pg), run_time=0.6)
        self.play(GrowArrow(A[2]), FadeIn(db), run_time=0.6)
        self.play(GrowArrow(A[3]), FadeIn(rs), GrowArrow(A[4]), FadeIn(lab[1]), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in notes], lag_ratio=0.4), run_time=1.0)
        self.rest(2.8)
        # 6. ALFWorld
        self.cap("ALFWorld: ReAct succeeded 71% of the time, versus 45% for acting without thoughts.", hold=0)
        self.play(FadeOut(VGroup(m, js, pg, db, rs, A, lab, notes)), run_time=0.6)
        hd = T("ALFWorld: 134 text-based household tasks, success rate", 22, INK, BOLD).move_to([0, 2.3, 0])
        B = hbars([("Act, best of 6 prompts", 45, "45%"), ("ReAct, best of 6 prompts", 71, "71%"), ("ReAct, worst of 6 prompts", 48, "48%")], 1.35, 0.075, x0=-0.9, hi=(1,))
        nt = T("Even the worst ReAct prompt beat the best acting-only prompt.", 22, UF).move_to([0, -0.9, 0])
        src = T("Yao et al., ICLR 2023; PaLM 540B, few-shot prompting", 20, GREY).move_to([0, -2.3, 0])
        self.play(FadeIn(hd), LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in B], lag_ratio=0.3), run_time=1.6)
        self.play(FadeIn(nt), FadeIn(src), run_time=0.6)
        self.rest(3.0)
        # 7. HotpotQA
        self.cap("HotpotQA: ReAct alone trailed chain of thought; combining the two did best.", hold=0)
        self.play(FadeOut(VGroup(hd, B, nt)), run_time=0.6)
        hd2 = T("HotpotQA: multi-hop questions answered from Wikipedia, exact match", 22, INK, BOLD).move_to([0, 2.3, 0])
        B2 = hbars([("ReAct", 27.4, "27.4"), ("chain of thought", 29.4, "29.4"), ("chain of thought, self-consistency", 33.4, "33.4"),
                    ("ReAct, then CoT-SC if stuck", 35.1, "35.1")], 1.4, 0.15, x0=0.0, hi=(3,))
        self.play(FadeIn(hd2), LaggedStart(*[AnimationGroup(FadeIn(b[0]), GrowFromEdge(b[1], LEFT), FadeIn(b[2])) for b in B2], lag_ratio=0.3), run_time=1.8)
        self.rest(3.2)
        # 8. failure modes
        self.cap("Grounding removed hallucinations, but ReAct failed through reasoning errors instead.", hold=0)
        self.play(FadeOut(VGroup(hd2, B2)), run_time=0.6)
        hd3 = T("Causes of failure, hand-labelled in 50 failed HotpotQA runs per method", 22, INK, BOLD).move_to([0, 2.3, 0])
        rows = [("", "ReAct", "chain of thought"), ("hallucinated facts", "0%", "56%"), ("reasoning error (e.g. repeated steps)", "47%", "16%"),
                ("search returned nothing useful", "23%", "–"), ("label ambiguity", "29%", "28%")]
        tb = VGroup()
        for i, r in enumerate(rows):
            y = 1.5 - 0.6 * i
            w = BOLD if i == 0 else NORMAL
            tb.add(VGroup(T(r[0], 22, INK, w).move_to([-0.6, y, 0], aligned_edge=RIGHT),
                          T(r[1], 22, UF if i else INK, BOLD).move_to([1.3, y, 0]),
                          T(r[2], 22, INK, w).move_to([3.9, y, 0])))
        hl = VGroup(*[RoundedRectangle(corner_radius=0.08, width=11.0, height=0.52, color=AMB, stroke_width=3).move_to([-0.45, tb[k].get_y(), 0]) for k in (1, 2)])
        self.play(FadeIn(hd3), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tb], lag_ratio=0.2), run_time=1.6)
        self.play(Create(hl[0]), run_time=0.6)
        self.play(Create(hl[1]), run_time=0.6)
        self.rest(3.2)
