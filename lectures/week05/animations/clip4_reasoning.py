from kit import *
TH = PC                                            # thinking text (purple)
OKC, BAD = "#0F766E", "#B45309"                    # correct (teal), wrong (amber)
def qbox(lines, size=22, w=None):
    """A grey question box with left-aligned lines."""
    q = VGroup(*[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    b = SurroundingRectangle(q, color=GREY, buff=0.2, corner_radius=0.1, fill_color="#E2E8F0", fill_opacity=1, stroke_width=2)
    return VGroup(b, q)
ECG_Q = ["A 58-year-old man has crushing chest pain.", "ECG: ST elevation in leads II, III, and aVF.", "What is the most likely occluded artery?",
         "A) left anterior descending   B) right coronary", "C) left circumflex   D) left main"]
class C4(Clip):
    TITLE = "Reasoning models"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. thinking before the answer
        self.cap("A reasoning model writes out its thinking before it answers.", hold=0)
        Q = qbox(ECG_Q).move_to([-3.4, 0.6, 0])
        th = VGroup(T("<think>", 22, TH, BOLD),
                    T("ST elevation in II, III, and aVF", 22, TH), T("points to the inferior wall.", 22, TH),
                    T("The inferior wall is usually supplied", 22, TH), T("by the right coronary artery.", 22, TH),
                    T("</think>", 22, TH, BOLD), T("Answer: B", 24, INK, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([0.9, 0.6, 0], aligned_edge=LEFT)
        il = T("illustrative output", 20, GREY).next_to(th, DOWN, buff=0.25).align_to(th, LEFT)
        self.play(FadeIn(Q, shift=RIGHT * 0.15), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in th], lag_ratio=0.25), run_time=2.2)
        self.play(FadeIn(il), run_time=0.4)
        self.rest(2.4)
        # 2. rule-based rewards (DeepSeek-R1)
        self.cap("DeepSeek-R1 learned this with rule-based rewards that a program can check.", hold=0)
        self.play(FadeOut(th), FadeOut(il), Q.animate.scale(0.8).move_to([-3.95, 0.95, 0]), run_time=0.7)
        stages = ["Pretraining", "Supervised\nfine-tuning", "Preference\ntuning", "RL with\nverifiable rewards"]
        TL = VGroup(*[box(s, 2.3, 0.8, "#DBEAFE" if i == 3 else "#F3F4F6", 18) for i, s in enumerate(stages)]).arrange(RIGHT, buff=0.25).scale(0.75).move_to([2.6, 2.6, 0])
        for i in range(3): TL[i].set_opacity(0.4)
        TLh = SurroundingRectangle(TL[3], color=UF, buff=0.05, stroke_width=4)
        rw = VGroup(VGroup(T("accuracy reward", 24, UF, BOLD), T("1 if the final letter is correct, else 0", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                    VGroup(T("format reward", 24, UF, BOLD), T("1 if the reasoning is inside <think> tags", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0.6, 0.75, 0], aligned_edge=UL)
        nz = VGroup(T("R1-Zero: reinforcement learning only, from the base model", 21, GREY),
                    T("R1: a small set of long reasoning examples (SFT) first, then RL", 21, GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-6.4, -1.6, 0], aligned_edge=UL)
        self.play(FadeIn(TL), Create(TLh), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rw], lag_ratio=0.4), run_time=1.2)
        self.play(FadeIn(nz), run_time=0.6)
        self.rest(2.6)
        # 3. GRPO: sample a group
        self.cap("GRPO samples a group of answers to the same question and scores each one.", hold=0)
        self.play(FadeOut(rw), FadeOut(nz), FadeOut(Q), run_time=0.4)
        picks = [("B", 1), ("A", 0), ("C", 0), ("D", 0)]
        cards = VGroup(*[box(f"sample {i + 1}\n… Answer: {p}", 2.4, 1.1, "#FFFFFF", 22, stroke=GREY) for i, (p, _) in enumerate(picks)]).arrange(RIGHT, buff=0.35).move_to([0.6, 0.2, 0])
        rl = VGroup(*[T(f"reward {r}", 24, OKC if r else BAD, BOLD).next_to(c, DOWN, buff=0.25) for c, (_, r) in zip(cards, picks)])
        gn = T("4 samples here; DeepSeek-R1 used 16 per question", 20, GREY).next_to(rl, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in cards], lag_ratio=0.25), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(r) for r in rl], lag_ratio=0.25), run_time=1.0)
        self.play(FadeIn(gn), run_time=0.4)
        self.rest(2.4)
        # 4. group-relative advantage
        self.cap("Each reward is compared with its own group: (reward − mean) ÷ std.", hold=0)
        self.play(FadeOut(gn), run_time=0.4)
        st = VGroup(T("mean = 0.25", 24, INK), T("std = 0.433", 24, INK)).arrange(RIGHT, buff=0.8).move_to([0.6, 1.55, 0])
        adv = [(1 - 0.25) / 0.4330127, (0 - 0.25) / 0.4330127]
        av = VGroup(*[T(f"{adv[0]:+.2f}" if r else f"{adv[1]:+.2f}".replace("-", "−"), 28, OKC if r else BAD, BOLD).next_to(l, DOWN, buff=0.2) for l, (_, r) in zip(rl, picks)])
        al = T("advantage", 20, GREY).next_to(av, LEFT, buff=0.4)
        nc = T("no separate critic model is needed", 20, GREY).next_to(av, DOWN, buff=0.35)
        self.play(FadeIn(st), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in av], lag_ratio=0.2), FadeIn(al), run_time=1.0)
        self.play(FadeIn(nc), run_time=0.4)
        self.rest(2.4)
        # 5. update direction
        self.cap("Answers above their group's average become more likely, the others less likely.", hold=0)
        self.play(FadeOut(nc), run_time=0.3)
        arr = VGroup(*[Arrow(c.get_top() + DOWN * 0.05, c.get_top() + UP * 0.75, buff=0, stroke_width=6, color=OKC) if r else Arrow(c.get_top() + UP * 0.75, c.get_top() + DOWN * 0.05, buff=0, stroke_width=4, color=BAD) for c, (_, r) in zip(cards, picks)])
        self.play(FadeOut(st), run_time=0.3)
        self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2), cards[0][0].animate.set_stroke(OKC, 5), run_time=1.0)
        self.rest(2.4)
        # 6. thinking at test time (real Qwen3-0.6B outputs)
        self.cap("Thinking longer at test time can fix an error, at the cost of more tokens.", hold=0)
        self.play(*[FadeOut(m) for m in (cards, rl, av, al, arr, TL, TLh)], run_time=0.5)
        nq = qbox(["Note: The patient denies chest pain.", "Question: Does the patient report chest pain?"], 24).move_to([0, 1.85, 0])
        off = VGroup(T("Qwen3-0.6B, thinking off", 22, GREY, BOLD), T("“Yes, the patient reports chest pain.”", 24, INK), T("9 tokens, wrong", 22, BAD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-6.6, 0.45, 0], aligned_edge=UL)
        on = VGroup(T("Qwen3-0.6B, thinking on", 22, TH, BOLD), T("“The patient does not report chest pain.”", 24, INK), T("119 tokens, correct", 22, OKC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([0.3, 0.45, 0], aligned_edge=UL)
        rr = T("real outputs; on a CPU, 0.9 s vs 11.4 s", 20, GREY).move_to([0, -1.55, 0])
        self.play(FadeIn(nq), run_time=0.6)
        self.play(FadeIn(off, shift=RIGHT * 0.1), run_time=0.8)
        self.play(FadeIn(on, shift=RIGHT * 0.1), run_time=0.8)
        self.play(FadeIn(rr), run_time=0.4)
        self.rest(2.6)
        # 7. Med-PaLM 2: ensemble refinement
        self.cap("Med-PaLM 2 samples several reasoning paths, then refines them into one answer.", hold=0)
        self.play(*[FadeOut(m) for m in (nq, off, on, rr)], run_time=0.5)
        q7 = box("medical\nquestion", 2.0, 1.1, "#E2E8F0", 22).move_to([-5.3, 0.6, 0])
        paths = VGroup(*[box(f"reasoning path {i + 1}", 2.9, 0.6, "#EDE9FE", 20, stroke=TH) for i in range(3)]).arrange(DOWN, buff=0.25).move_to([-1.6, 0.6, 0])
        ref = box("refine:\nread all paths", 2.4, 1.1, "#DBEAFE", 22).move_to([1.9, 0.6, 0])
        ans = box("final\nanswer", 1.6, 1.1, "#FFFFFF", 22).move_to([4.6, 0.6, 0])
        a1 = VGroup(*[Arrow(q7.get_right(), p.get_left(), buff=0.08, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.12) for p in paths])
        a2 = VGroup(*[Arrow(p.get_right(), ref.get_left(), buff=0.08, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.12) for p in paths])
        a3 = Arrow(ref.get_right(), ans.get_left(), buff=0.08, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.25)
        sc = VGroup(T("MedQA accuracy:", 24, INK), T("Med-PaLM 67.2%", 24, GREY, BOLD), T("→", 24, INK), T("Med-PaLM 2 86.5%", 24, UF, BOLD)).arrange(RIGHT, buff=0.25).move_to([0, -1.35, 0])
        sn = T("from a stronger base model, medical fine-tuning, and ensemble refinement together", 20, GREY).next_to(sc, DOWN, buff=0.2)
        self.play(FadeIn(q7), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(p)) for a, p in zip(a1, paths)], lag_ratio=0.3), run_time=1.2)
        self.play(*[GrowArrow(a) for a in a2], FadeIn(ref), run_time=0.8)
        self.play(GrowArrow(a3), FadeIn(ans), run_time=0.6)
        self.play(FadeIn(sc), FadeIn(sn), run_time=0.7)
        self.rest(2.6)
        # 8. a fluent rationale is not proof (real Qwen3-0.6B outputs)
        self.cap("A fluent explanation is not proof: thinking can also lead a model to a wrong answer.", hold=0)
        self.play(*[FadeOut(m) for m in (q7, paths, ref, ans, a1, a2, a3, sc, sn)], run_time=0.5)
        Q8 = qbox(ECG_Q, 20).move_to([-3.6, 1.5, 0])
        o1 = VGroup(T("Qwen3-0.6B, thinking off", 22, GREY, BOLD), T("Answer: B, right coronary", 24, INK), T("correct", 22, OKC, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([0.6, 2.25, 0], aligned_edge=UL)
        o2 = VGroup(T("Qwen3-0.6B, thinking on", 22, TH, BOLD),
                    T("“ST elevation in the inferior leads is most commonly due to a blockage", 22, INK),
                    T("in the left anterior descending artery.”", 22, INK),
                    T("after 1,500 tokens: still unsure, leaning to A (wrong)", 22, BAD, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([-6.6, -0.05, 0], aligned_edge=UL)
        rr8 = T("real outputs; checking reasoning returns in Week 12 on evaluation", 20, GREY).move_to([0, -2.3, 0])
        self.play(FadeIn(Q8), run_time=0.6)
        self.play(FadeIn(o1, shift=RIGHT * 0.1), run_time=0.8)
        self.play(FadeIn(o2, shift=RIGHT * 0.1), run_time=1.0)
        self.play(FadeIn(rr8), run_time=0.4)
        self.rest(2.8)
