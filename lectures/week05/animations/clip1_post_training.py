from kit import *
BASE, POST = GREY, UF                              # base model (grey), post-trained model (UF blue)
WRONG = "#B45309"                                  # marks a wrong answer (amber)
PFILL, AFILL = "#F3F4F6", "#DBEAFE"                # prompt tokens (not counted), answer tokens (counted)
def panel(head, lines, color, x, y=1.0, size=22):
    """A heading and a few lines of model text, left-aligned at x."""
    h = T(head, 22, color, BOLD)
    body = VGroup(*[T(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    return VGroup(h, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([x, y, 0], aligned_edge=UL)
class C1(Clip):
    TITLE = "From pretrained model to clinical assistant"
    PACE, HOLD = 1.2, 0.5
    def construct(self):
        # 1. a pretrained model only continues text
        self.cap("A pretrained model only continues the text it is given.", hold=0)
        pr = box("Discharge summary: The patient denies chest pain.", 9.4, 0.7, "#E2E8F0", 24).move_to([0, 1.9, 0])
        cont = panel("Qwen3-0.6B-Base continues (real output)",
                     ["The patient is a 65-year-old woman with a history of",
                      "hypertension and diabetes. She has been experiencing",
                      "fatigue and shortness of breath for the …"], BASE, -4.7, 0.9, 24)
        self.play(FadeIn(pr, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(cont[0]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in cont[1]], lag_ratio=0.4), run_time=1.8)
        self.rest(2.6)
        # 2. given a question, the base model writes more quiz
        self.cap("Given a question, the base model just keeps writing a quiz.", hold=0)
        self.play(FadeOut(cont), FadeOut(pr), run_time=0.4)
        q = VGroup(T("Note: The patient denies chest pain.", 24, INK), T("Question: Does the patient report chest pain?", 24, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        qb = SurroundingRectangle(q, color=GREY, buff=0.2, corner_radius=0.1, fill_color="#E2E8F0", fill_opacity=1, stroke_width=2)
        Q = VGroup(qb, q).move_to([0, 2.0, 0])
        base = panel("Base model (real output)",
                     ["(Yes/No)", "Answer: No", "Question: Does the patient report", "shortness of breath? (Yes/No)", "Answer: Yes", "Question: …"], BASE, -6.6, 0.85)
        self.play(FadeIn(Q, shift=DOWN * 0.15), run_time=0.7)
        self.play(FadeIn(base[0]), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.1) for l in base[1]], lag_ratio=0.3), run_time=1.8)
        bn = T("invents new questions", 22, BASE).next_to(base, DOWN, buff=0.25).align_to(base, LEFT)
        self.play(FadeIn(bn), run_time=0.5)
        self.rest(2.4)
        # 3. the post-trained model answers, here wrongly
        self.cap("The post-trained model answers like an assistant, but here it is wrong.", hold=0)
        post = panel("Post-trained Qwen3-0.6B (real output)", ["Yes, the patient reports chest pain."], POST, 0.6, 0.85, 24)
        x = T("wrong: the note says denies", 22, WRONG, BOLD).next_to(post, DOWN, buff=0.3).align_to(post, LEFT)
        fx = T("clips 3 and 4 show two ways to fix this", 22, GREY).next_to(x, DOWN, buff=0.2).align_to(post, LEFT)
        self.play(FadeIn(post[0]), run_time=0.4)
        self.play(FadeIn(post[1], shift=RIGHT * 0.1), run_time=0.7)
        self.play(FadeIn(x), run_time=0.5)
        self.play(FadeIn(fx), run_time=0.5)
        self.rest(2.4)
        # 4. four training stages
        self.cap("Post-training adds stages after pretraining.", hold=0)
        self.play(*[FadeOut(m) for m in (Q, base, bn, post, x, fx)], run_time=0.5)
        names = [("Pretraining", "next token, web text", "Week 3"),
                 ("Supervised\nfine-tuning", "instruction + answer", "clips 1 and 2"),
                 ("Preference\ntuning", "chosen vs rejected", "clip 3"),
                 ("RL with\nverifiable rewards", "checkable answers", "clip 4")]
        fills = ["#E2E8F0", "#DBEAFE", "#DBEAFE", "#F3F4F6"]
        S = VGroup(*[box(n, 2.9, 1.1, f, 22) for (n, _, _), f in zip(names, fills)]).arrange(RIGHT, buff=0.45).move_to([0, 0.9, 0])
        AR = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=3, color=GREY, max_tip_length_to_length_ratio=0.4) for a, b in zip(S, S[1:])])
        D = VGroup(*[T(d, 20, INK).next_to(s, DOWN, buff=0.25) for (_, d, _), s in zip(names, S)])
        W = VGroup(*[T(w, 20, UF, BOLD).next_to(d, DOWN, buff=0.18) for (_, _, w), d in zip(names, D)])
        tl = VGroup(S, AR, D, W)
        tl[0][3].set_opacity(0.35); D[3].set_opacity(0.35); W[3].set_opacity(0.35)   # stage 4 greyed until clip 4
        self.play(LaggedStart(*[FadeIn(VGroup(S[i], D[i], W[i]), shift=RIGHT * 0.15) for i in range(4)], lag_ratio=0.3), LaggedStart(*[GrowArrow(a) for a in AR], lag_ratio=0.3), run_time=2.0)
        br = Brace(VGroup(S[1], S[3]), UP, color=POST)
        bl = T("post-training", 22, POST, BOLD).next_to(br, UP, buff=0.1)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.7)
        self.rest(2.6)
        # 5. SFT: instruction and answer pairs in a chat template
        self.cap("Supervised fine-tuning trains on instruction and answer pairs in a chat template.", hold=0)
        top = VGroup(S, AR)
        self.play(FadeOut(D), FadeOut(W), FadeOut(br), FadeOut(bl), run_time=0.4)
        self.play(top.animate.scale(0.8).move_to([0, 2.05, 0]), run_time=0.8)
        hl = SurroundingRectangle(S[1], color=POST, buff=0.06, stroke_width=4)
        self.play(Create(hl), run_time=0.4)
        rows = [("<|im_start|>user", PFILL, "role marker"),
                ("Note: The patient denies chest pain.\nQuestion: Does the patient report chest pain?", PFILL, "instruction"),
                ("<|im_end|>  <|im_start|>assistant", PFILL, "role marker"),
                ("No. The note says the patient denies chest pain.", AFILL, "answer"),
                ("<|im_end|>", AFILL, "end of answer")]
        R = VGroup(*[box(s, 8.4, 0.85 if "\n" in s else 0.5, f, 21, stroke=GREY) for s, f, _ in rows]).arrange(DOWN, buff=0.1).move_to([-1.9, -0.75, 0])
        RL = VGroup(*[T(l, 20, GREY).next_to(r, RIGHT, buff=0.25) for (_, _, l), r in zip(rows, R)])
        self.play(LaggedStart(*[FadeIn(VGroup(r, l), shift=UP * 0.1) for r, l in zip(R, RL)], lag_ratio=0.25), run_time=1.8)
        self.rest(2.6)
        # 6. the loss counts only the answer tokens
        self.cap("The loss is the same next-token loss, counted only on the answer tokens.", hold=0)
        for i in range(3): R[i].generate_target(); R[i].target.set_opacity(0.4)
        self.play(*[MoveToTarget(R[i]) for i in range(3)], *[RL[i].animate.set_opacity(0.4) for i in range(3)], run_time=0.6)
        ab = SurroundingRectangle(VGroup(R[3], R[4]), color=POST, buff=0.08, stroke_width=4)
        nl = VGroup(T("not counted", 22, GREY, BOLD).next_to(R[1], RIGHT, buff=0.35), T("counted in the loss", 22, POST, BOLD).next_to(ab, RIGHT, buff=0.25))
        self.play(FadeOut(RL), run_time=0.3)
        self.play(Create(ab), FadeIn(nl), run_time=0.8)
        self.rest(2.6)
        # 7. same architecture, same loss, new data
        self.cap("Same architecture and same loss: only the training data changes.", hold=0)
        self.play(*[FadeOut(m) for m in (R, ab, nl, hl, top)], run_time=0.5)
        cmp = VGroup(VGroup(T("Pretraining", 24, INK, BOLD), T("Supervised fine-tuning", 24, POST, BOLD)),
                     VGroup(T("architecture", 22, GREY), T("decoder blocks", 24, INK), T("same blocks", 24, INK)),
                     VGroup(T("loss", 22, GREY), T("next token", 24, INK), T("next token, answer only", 24, INK)),
                     VGroup(T("data", 22, GREY), T("raw text", 24, INK), T("instruction and answer pairs", 24, POST, BOLD)))
        for i, r in enumerate(cmp):                      # three columns: row name, pretraining, fine-tuning
            y = 0.5 - 0.62 * i
            if i == 0: r[0].move_to([-2.7, y, 0], aligned_edge=LEFT); r[1].move_to([1.0, y, 0], aligned_edge=LEFT)
            else: r[0].move_to([-4.8, y, 0], aligned_edge=LEFT); r[1].move_to([-2.7, y, 0], aligned_edge=LEFT); r[2].move_to([1.0, y, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in cmp], lag_ratio=0.3), run_time=1.6)
        self.rest(2.8)
