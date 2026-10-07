from manim import *
import numpy as np
config.background_color = "#FFFFFF"
FONT = "Inter"
INK, GREY, UF = "#111827", "#6B7280", "#0021A5"
QC, KC, VC = "#E4572E", "#2E9E5B", "#3B6FD4"      # query red, key green, value blue (as in the Spring 2026 deck)
EC, PC, OC, AMB = "#64748B", "#8B5CF6", "#D4A017", "#F59E0B"
TOK = ["My", "name", "is", "John"]

def T(s, size=24, color=INK, weight=NORMAL, **k):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **k)

class Clip(Scene):
    TITLE = ""
    def setup(self):
        self.title = T(self.TITLE, 28, UF, BOLD).to_corner(UL, buff=0.35)
        self.add(self.title)
        self._cap = None
    def cap(self, s, hold=3.2, size=30):
        """Caption at the bottom; replaces the previous one."""
        new = T(s, size, INK)
        if new.width > 13.2: new.scale_to_fit_width(13.2)
        new.move_to(DOWN * 3.45)
        if self._cap is None: self.play(FadeIn(new, shift=UP * 0.15), run_time=0.5)
        else: self.play(FadeOut(self._cap, run_time=0.3)); self.play(FadeIn(new, shift=UP * 0.15), run_time=0.4)
        self._cap = new
        if hold: self.wait(hold)

def tok(s, color=INK, w=1.35, h=0.5, size=22, fill="#F3F4F6"):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=color, stroke_width=2, fill_color=fill, fill_opacity=1)
    return VGroup(r, T(s, size, color).move_to(r))

def mat(rows, cols, color, cell=0.3, seed=0, vals=None):
    """Grid of cells; opacity encodes an (illustrative) value. Returns VGroup of row VGroups."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for i in range(rows):
        row = VGroup()
        for j in range(cols):
            a = vals[i][j] if vals is not None else rng.uniform(0.18, 0.95)
            sq = Square(cell, stroke_color=WHITE, stroke_width=1.5, fill_color=color, fill_opacity=float(a))
            sq.move_to(RIGHT * j * cell + DOWN * i * cell)
            row.add(sq)
        g.add(row)
    return g.move_to(ORIGIN)

def rowlabels(m, labels, size=18, color=GREY, side=LEFT):
    return VGroup(*[T(l, size, color).next_to(m[i], side, buff=0.15) for i, l in enumerate(labels)])

def box(s, w, h, fill, size=20, stroke=INK):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=stroke, stroke_width=2, fill_color=fill, fill_opacity=1)
    t = T(s, size, INK)
    if t.width > w - 0.2: t.scale_to_fit_width(w - 0.2)
    return VGroup(r, t.move_to(r))

def heat(vals, cell=0.62, color=KC, size=17, labels_r=None, labels_c=None, mask=None):
    n, m = len(vals), len(vals[0]); g = VGroup(); cells = VGroup(); nums = VGroup()
    for i in range(n):
        for j in range(m):
            masked = mask is not None and mask[i][j]
            sq = Square(cell, stroke_color=WHITE, stroke_width=2, fill_color=("#111827" if masked else color), fill_opacity=(1 if masked else 0.12 + 0.8 * vals[i][j]))
            sq.move_to(RIGHT * j * cell + DOWN * i * cell); cells.add(sq)
            txt = "−∞" if masked else (f"{vals[i][j]:.2f}".rstrip("0").rstrip(".") if vals[i][j] in (0, 1) else f"{vals[i][j]:.2f}")
            nums.add(T(txt, size, WHITE if masked else INK, BOLD if (not masked and vals[i][j] > 0.4) else NORMAL).move_to(sq))
    g.add(cells, nums)
    lab = VGroup()
    if labels_r: lab.add(*[T(l, 18, QC).next_to(cells[i * m], LEFT, buff=0.15) for i, l in enumerate(labels_r)])
    if labels_c: lab.add(*[T(l, 18, KC).next_to(cells[j], UP, buff=0.12) for j, l in enumerate(labels_c)])
    g.add(lab)
    return g.move_to(ORIGIN)

def wsub(sub, color, size=22):
    w = T("× W", size, color, BOLD); s = T(sub, int(size * 0.68), color, BOLD).next_to(w, RIGHT, buff=0.03).shift(DOWN * 0.1)
    return VGroup(w, s)
