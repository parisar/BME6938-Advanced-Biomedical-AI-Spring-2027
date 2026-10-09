from manim import *
import numpy as np
import os, json, subprocess
import glob
try:                                   # use the bundled Inter font so clips look the same on every machine
    import manimpango
    for _f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "*.otf")):
        manimpango.register_font(_f)
except Exception:
    pass
config.background_color = "#FFFFFF"
FONT = "Inter"
INK, GREY, UF = "#111827", "#6B7280", "#0021A5"
QC, KC, VC = "#E4572E", "#2E9E5B", "#3B6FD4"      # query red, key green, value blue (as in the Spring 2026 deck)
EC, PC, OC, AMB = "#64748B", "#8B5CF6", "#D4A017", "#F59E0B"

def T(s, size=24, color=INK, weight=NORMAL, **k):
    return Text(s, font=FONT, font_size=size, color=color, weight=weight, **k)

class Clip(Scene):
    TITLE = ""
    PACE = 1.0                         # multiplies the run_time passed to play() (above 1 is slower); waits are not affected
    HOLD = 0.0                         # extra seconds each caption stays before the next step
    def play(self, *a, **k):
        if "run_time" in k: k["run_time"] *= self.PACE
        super().play(*a, **k)
    def setup(self):
        self.title = T(self.TITLE, 28, UF, BOLD).to_corner(UL, buff=0.35)
        self.add(self.title)
        self._cap = None
        # Narration mode: if NARRATION_AUDIO points to a folder with <clip>_sNN.mp3 files, each caption
        # stays on screen at least as long as its narration, and the start times are written to marks_<clip>.json.
        self._clip = getattr(self, "CLIP_ID", None) or "clip" + self.__class__.__name__[1:]
        self._durs, self._marks, self._t0 = None, [], None
        adir = os.environ.get("NARRATION_AUDIO")
        if adir:
            files = sorted(f for f in os.listdir(adir) if f.startswith(self._clip + "_s") and f.endswith(".mp3"))
            self._durs = [float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(adir, f)]).decode().strip()) for f in files]
            self._files = files
        inner = self.construct
        def wrapped():
            inner(); self._finish_segment(tail=0.9)
            if self._durs is not None:
                assert len(self._marks) == len(self._durs), (self._clip, len(self._marks), len(self._durs))
                json.dump({"clip": self._clip, "segments": [{"file": f, "start": round(t, 3)} for f, t in zip(self._files, self._marks)]}, open(f"marks_{self._clip}.json", "w"), indent=1)
        self.construct = wrapped
    def _finish_segment(self, tail=0.45):
        """In narration mode, wait until the narration of the current caption has finished."""
        if self._durs is None or self._t0 is None: return
        need = self._durs[len(self._marks) - 1] + tail - (self.renderer.time - self._t0)
        if need > 0.03: self.wait(need)
    def cap(self, s, hold=3.2, size=30):
        """Caption at the bottom; replaces the previous one."""
        new = T(s, size, INK)
        if new.width > 13.2: new.scale_to_fit_width(13.2)
        new.move_to(DOWN * 3.45)
        self._finish_segment()
        if self._cap is None: t0 = self.renderer.time; self.play(FadeIn(new, shift=UP * 0.15), run_time=0.5)
        else: self.play(FadeOut(self._cap, run_time=0.3)); t0 = self.renderer.time; self.play(FadeIn(new, shift=UP * 0.15), run_time=0.4)
        self._cap = new
        if self._durs is not None: self._t0 = t0 + 0.15; self._marks.append(self._t0)
        if hold: self.wait(hold + self.HOLD)

def vdots(color=GREY, r=0.045, gap=0.11):
    """Vertical ellipsis drawn as dots (Inter has no ⋮ glyph)."""
    return VGroup(*[Dot(radius=r, color=color) for _ in range(3)]).arrange(DOWN, buff=gap)

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

# ---- synthetic ECG (no patient data): P, QRS, and T waves as Gaussian bumps
def ecg_fn(dur=10, hr=72, af=False, seed=0):
    """Returns y(t) for a single-lead ECG of `dur` seconds. af=True: irregular beats, no P waves, fibrillatory baseline."""
    rng = np.random.default_rng(seed); b = [rng.uniform(0.25, 0.55)]
    while b[-1] < dur + 1: b.append(b[-1] + (rng.uniform(0.42, 0.95) if af else 60 / hr * rng.uniform(0.97, 1.03)))
    ph = rng.uniform(0, 6.28, 2)
    def y(t):
        t = np.asarray(t, float); out = np.zeros_like(t)
        g = lambda c, a, w: a * np.exp(-0.5 * ((t - c) / w) ** 2)
        for c in b:
            if not af: out += g(c - 0.17, 0.13, 0.025)
            out += g(c - 0.03, -0.12, 0.009) + g(c, 1.0, 0.011) + g(c + 0.035, -0.28, 0.011) + g(c + 0.28, 0.27, 0.045)
        if af: out += 0.045 * np.sin(2 * np.pi * 6.3 * t + ph[0]) + 0.03 * np.sin(2 * np.pi * 8.9 * t + ph[1])
        return out
    return y

def wave(fn, t0, t1, width, height, color=INK, sw=3, n_per_s=160):
    """Polyline of fn over [t0, t1]: left end at x=0, baseline at y=0, so place it with .shift(), not .move_to()."""
    ts = np.linspace(t0, t1, max(40, int((t1 - t0) * n_per_s)))
    pts = [np.array([(t - t0) / (t1 - t0) * width, v * height, 0]) for t, v in zip(ts, fn(ts))]
    return VMobject(stroke_color=color, stroke_width=sw).set_points_as_corners(pts)
