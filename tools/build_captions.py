"""Build the WebVTT captions for one week's narrated clips.

    python tools/build_captions.py week06                 captions for every clip of the week
    python tools/build_captions.py week06 --clip clip2     one clip only
    python tools/build_captions.py week06 --verify         also check the result against the mp4
    python tools/build_captions.py week06 --no-copy        do not copy to "copy_clips_to"
    python tools/build_captions.py week06 --force-marks    recompute the timings from scratch

What it does, and why it works this way

    Timing. A narrated mp4 is not the segments' audio joined end to end. build_clips.py
    delays each segment's narration to the start time the kit recorded in
    marks_<clip>.json, and the gap between two segments also holds that segment's
    animation, so adding up the audio lengths would put the last cue of a long clip
    several seconds early. This script regenerates those exact marks by replaying the
    scene in narration mode with Manim's --dry_run, which writes no video and makes no
    API call: Manim's clock does not depend on resolution, so the marks come out
    identical to the ones the video was built with. They are cached in .cache/marks.

    A segment's speech therefore occupies [start, start + length of its narration mp3],
    and the silence between segments carries no cue.

    Within a segment, each cue boundary starts from a guess at how much of the spoken
    text the cue holds, and is then moved onto a pause in the narration audio (ffmpeg
    silencedetect). All the boundaries of a segment are chosen together, so cue changes
    follow the pauses in order rather than each one grabbing the nearest pause.

    Text. The caption text is the spoken narration, since captions have to match the
    audio, with the pronunciation respellings and the spelled-out numbers turned back
    into normal writing: see caption_text.py.

    Cues. At most two lines of about 42 characters, broken at clause boundaries, each on
    screen for at least 1.5 s.

Needs: ffmpeg and ffprobe on PATH, manim, the narration audio already in .cache/audio
(it is, for any clip that has been built), and local_config.json for the voice settings
that name the cache entries. It never calls ElevenLabs.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caption_text import convert

CACHE = os.path.join(ROOT, ".cache", "audio")
MARKS = os.path.join(ROOT, ".cache", "marks")

LINE, CUE_MAX, MIN_CUE = 42, 84, 1.5
WEIGHT_MAX = 105      # a cue of about CUE_MAX plain characters, allowing for a few digits
TAIL = 0.85           # how far a segment's last cue may run into the silence after it
PAUSE_MIN = 0.18      # a gap this long in the narration counts as a break between phrases
PAUSE_DB = -32        # below this level the narration counts as silent

# where a clause can break, strongest first
SOFT = [" and ", " but ", " so ", " because ", " which ", " where ", " that ", " then ",
        " with ", " from ", " for ", " to ", " of ", " in ", " on "]


def die(msg):
    sys.exit("ERROR: " + msg)


def config():
    cfg = {"voice_id": "", "model": "eleven_multilingual_v2", "stability": 0.5,
           "similarity": 0.75, "copy_clips_to": ""}
    path = os.path.join(ROOT, "local_config.json")
    if os.path.exists(path):
        cfg.update(json.load(open(path, encoding="utf-8")))
    if not cfg["voice_id"]:
        die("no voice_id in local_config.json: the audio cache is keyed by the voice settings")
    return cfg


def duration(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         path]).decode().strip())


def cached_mp3(text, cfg):
    """The cache entry build_clips.py would have written for this narration line."""
    blob = json.dumps([text, cfg["voice_id"], cfg["model"], cfg["stability"], cfg["similarity"]],
                      ensure_ascii=False)
    return os.path.join(CACHE, hashlib.sha1(blob.encode("utf-8")).hexdigest() + ".mp3")


# ---------------------------------------------------------------- timings
def marks(week, clip, cfg, force=False):
    """Segment start times and narration lengths for one clip, from .cache/marks."""
    os.makedirs(MARKS, exist_ok=True)
    dest = os.path.join(MARKS, f'{week}_{clip["id"]}.json')
    if os.path.exists(dest) and not force:
        m = json.load(open(dest, encoding="utf-8"))
        if len(m["segments"]) == len(clip["segments"]):
            return m
    wdir = os.path.join(ROOT, "lectures", week)
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(ROOT, "lectures", "_shared") + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    with tempfile.TemporaryDirectory(prefix="marks_") as tmp:
        adir = os.path.join(tmp, "audio"); os.makedirs(adir)
        for i, s in enumerate(clip["segments"]):
            src = cached_mp3(s["text"], cfg)
            if not os.path.exists(src):
                die(f'{week} {clip["id"]}: no cached narration for segment {i + 1}. '
                    f'Build the clip first (tools/build_clips.py {week} --clip {clip["id"]}).')
            shutil.copyfile(src, os.path.join(adir, f'{clip["id"]}_s{i + 1:02d}.mp3'))
        r = subprocess.run([sys.executable, "-m", "manim", "-ql", "--dry_run", "--disable_caching",
                            "--media_dir", os.path.join(tmp, "media"),
                            os.path.join(wdir, clip["scene_file"]), clip["scene"]],
                           cwd=tmp, env=dict(env, NARRATION_AUDIO=adir),
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                           encoding="utf-8", errors="replace")
        mf = os.path.join(tmp, f'marks_{clip["id"]}.json')
        if r.returncode != 0 or not os.path.exists(mf):
            die(f'{week} {clip["id"]}: replaying the scene failed\n' + r.stdout[-2500:])
        m = json.load(open(mf, encoding="utf-8"))
        m["durs"] = [duration(os.path.join(adir, s["file"])) for s in m["segments"]]
    json.dump(m, open(dest, "w", encoding="utf-8"), indent=1)
    return m


def pauses(path):
    """Midpoints of the gaps in one narration file, in seconds from its start."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                        f"silencedetect=noise={PAUSE_DB}dB:d={PAUSE_MIN}", "-f", "null", "-"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out, start = [], None
    for line in r.stdout.splitlines():
        m = re.search(r"silence_start: ([\d.]+)", line)
        if m: start = float(m.group(1))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and start is not None:
            out.append((start + float(m.group(1))) / 2); start = None
    return out


# ---------------------------------------------------------------- cue text
def spoken_weight(cue):
    """Roughly how long a cue takes to say, in units of written characters.

    A digit is read as a whole word ("38,455" is six characters and about two seconds),
    so digits and the percent sign count for more than the letters around them.
    """
    return len(cue) + 5 * sum(c.isdigit() for c in cue) + 6 * cue.count("%")


def wrap(cue):
    """One or two lines, each at most LINE characters, broken as evenly as possible."""
    if len(cue) <= LINE: return [cue]
    best = None
    for m in re.finditer(r" ", cue):
        a, b = m.start(), len(cue) - m.end()
        if a <= LINE and b <= LINE and (best is None or abs(a - b) < best[0]):
            best = (abs(a - b), m.start())
    if best is None:                                  # cannot fit two lines: break near LINE
        k = cue.rfind(" ", 0, LINE + 1)
        k = k if k > 0 else LINE
        return [cue[:k].strip(), cue[k:].strip()]
    return [cue[:best[1]].strip(), cue[best[1] + 1:].strip()]


def fits(cue):
    return max(len(l) for l in wrap(cue)) <= LINE


def chunks(text):
    """Split into clause-sized pieces, none longer than CUE_MAX."""
    parts = [p for p in re.split(r"(?<=[.,;:!?])\s+", text.strip()) if p]
    # glue short pieces to the next one, so a list of items or values is not broken
    # between its items ("the, patient, has, a, and cold.")
    glued, buf = [], ""
    for p in parts:
        buf = (buf + " " + p).strip() if buf else p
        if len(buf) >= 14:
            glued.append(buf); buf = ""
    if buf:
        if glued: glued[-1] += " " + buf
        else: glued.append(buf)
    out = []
    for p in glued:
        while len(p) > CUE_MAX:
            cut = None
            for s in SOFT:                            # strongest break that fits, nearest the middle
                best = None
                for m in re.finditer(re.escape(s), p):
                    if 12 < m.start() <= CUE_MAX:
                        d = abs(m.start() - len(p) // 2)
                        if best is None or d < best[0]: best = (d, m.start() + 1)
                if best:
                    cut = best[1]; break
            if cut is None:                           # no clause break: last space that fits
                cut = p.rfind(" ", 0, CUE_MAX + 1)
                if cut <= 0: break
            out.append(p[:cut].strip()); p = p[cut:].strip()
        if p: out.append(p)
    return out


def pack(text):
    """Pack clause pieces into cues that fit two lines and are not too long to say."""
    cues = []
    for c in chunks(text):
        merged = (cues[-1] + " " + c) if cues else c
        if cues and len(merged) <= CUE_MAX and spoken_weight(merged) <= WEIGHT_MAX and fits(merged):
            cues[-1] = merged
        else:
            cues.append(c)
    out = []
    for c in cues:                                    # split anything still too wide or too long
        stack = [c]
        while stack:
            c = stack.pop(0)
            if (fits(c) and spoken_weight(c) <= WEIGHT_MAX) or " " not in c:
                out.append(c); continue
            k = min((abs(m.start() - len(c) // 2), m.start()) for m in re.finditer(r" ", c))[1]
            stack = [c[:k].strip(), c[k:].strip()] + stack
    return out or [text]


# ---------------------------------------------------------------- cue timing
def place(cues, t0, dur, breaks, tail):
    """Time the cues of one segment across [t0, t0 + dur + tail].

    The boundaries are chosen together, by dynamic programming over the pauses, so the
    cue changes follow the pauses in order instead of each boundary taking whichever
    pause is nearest to it.
    """
    if len(cues) == 1:
        return [(t0, t0 + dur + tail, wrap(cues[0]))]
    total = sum(map(spoken_weight, cues))
    guess, acc = [], 0.0
    for c in cues[:-1]:
        acc += spoken_weight(c) / total
        guess.append(acc * dur)

    pauseset = {round(b, 3) for b in breaks}
    pool = [b for b in sorted(pauseset | {round(g, 3) for g in guess})
            if MIN_CUE <= b <= dur - 0.7]
    k = len(guess)

    def fallback():
        out, prev = [], 0.0
        for n, g in enumerate(guess):
            prev = min(max(g, prev + MIN_CUE), dur - MIN_CUE * (k - n))
            out.append(prev)
        return out

    if len(pool) < k:
        bounds = fallback()
    else:
        INF = float("inf")
        cost = [[INF] * len(pool) for _ in range(k)]
        back = [[-1] * len(pool) for _ in range(k)]
        for n in range(k):
            for a, b in enumerate(pool):
                own = (b - guess[n]) ** 2 + (0.0 if round(b, 3) in pauseset else 0.3)
                if n == 0:
                    cost[n][a] = own
                else:
                    for p in range(a):
                        if b - pool[p] >= MIN_CUE and cost[n - 1][p] + own < cost[n][a]:
                            cost[n][a] = cost[n - 1][p] + own; back[n][a] = p
        end = min(range(len(pool)),
                  key=lambda a: cost[k - 1][a] if dur - pool[a] >= MIN_CUE else INF)
        bounds, a, ok = [None] * k, end, True
        for n in range(k - 1, -1, -1):
            bounds[n] = pool[a]; a = back[n][a]
            if a < 0 and n: ok = False; break
        if not ok or any(b is None for b in bounds):
            bounds = fallback()

    edges = [0.0] + bounds + [dur + tail]
    return [(t0 + edges[n], t0 + edges[n + 1], wrap(c)) for n, c in enumerate(cues)]


def split_segment(text, t0, dur, breaks, tail):
    """Cues for one narration segment, none shorter than MIN_CUE where that is possible."""
    cues = pack(text)
    while len(cues) > 1:
        total = sum(map(spoken_weight, cues))
        secs = [dur * spoken_weight(c) / total for c in cues]
        for i in sorted(range(len(cues)), key=lambda k: secs[k]):
            if secs[i] >= MIN_CUE:
                return place(cues, t0, dur, breaks, tail)
            j = i - 1 if i == len(cues) - 1 else i + 1
            lo, hi = min(i, j), max(i, j)
            merged = cues[lo] + " " + cues[hi]
            if fits(merged):
                cues[lo:hi + 1] = [merged]; break
        else:
            break                                     # nothing left that can legally merge
    return place(cues, t0, dur, breaks, tail)


def ts(t):
    h, r = divmod(max(t, 0.0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def build(week, clip, cfg, force=False):
    m = marks(week, clip, cfg, force)
    segs = clip["segments"]
    if len(m["segments"]) != len(segs):
        die(f'{week} {clip["id"]}: {len(segs)} narration lines but {len(m["segments"])} captions '
            f'in the scene')
    cues, starts = [], [x["start"] for x in m["segments"]]
    for n, (s, start, dur) in enumerate(zip(segs, starts, m["durs"])):
        mp3 = cached_mp3(s["text"], cfg)
        if not os.path.exists(mp3):
            die(f'{week} {clip["id"]}: no cached narration for segment {n + 1}')
        # the on-screen caption stays up through the silence before the next segment,
        # so a segment's last cue may use a little of it
        nxt = starts[n + 1] if n + 1 < len(starts) else start + dur + TAIL + 0.2
        tail = max(0.0, min(TAIL, nxt - 0.2 - (start + dur)))
        cues += split_segment(convert(s["text"]), start, dur, pauses(mp3), tail)
    mp4 = os.path.join(ROOT, "lectures", week, "clips", "narrated", clip["output"] + "-narrated.mp4")
    if os.path.exists(mp4):                           # never run a cue past the end of the video
        a, b, body = cues[-1]
        cues[-1] = (a, min(b, duration(mp4) - 0.02), body)
    lines = ["WEBVTT", "", f'NOTE {clip["output"]}',
             "NOTE Narration read by an AI-generated voice.", ""]
    for n, (a, b, body) in enumerate(cues, 1):
        lines += [str(n), f"{ts(a)} --> {ts(b)}", *body, ""]
    return "\n".join(lines), cues


# ---------------------------------------------------------------- checking
def levels(mp4, spans):
    """Mean volume in dB over each (start, end) window of the mp4's audio."""
    out = []
    for a, b in spans:
        if b <= a:
            out.append(None); continue
        r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}",
                            "-i", mp4, "-map", "0:a", "-af", "volumedetect", "-f", "null", "-"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", r.stdout)
        out.append(float(m.group(1)) if m else None)
    return out


def check(week, clip, cues, deep=False):
    """Structural checks, and optionally whether cue changes land on breaks in speech."""
    mp4 = os.path.join(ROOT, "lectures", week, "clips", "narrated", clip["output"] + "-narrated.mp4")
    problems = []
    vd = duration(mp4) if os.path.exists(mp4) else None
    for n, (a, b, body) in enumerate(cues):
        if b <= a: problems.append(f"cue {n+1}: ends before it starts")
        if b - a < MIN_CUE - 0.01: problems.append(f"cue {n+1}: only {b-a:.2f}s on screen")
        if n and a < cues[n - 1][1] - 0.001: problems.append(f"cue {n+1}: overlaps cue {n}")
        if vd and b > vd + 0.01: problems.append(f"cue {n+1}: ends past the video")
        if len(body) > 2: problems.append(f"cue {n+1}: {len(body)} lines")
        if any(len(l) > LINE for l in body):
            problems.append(f"cue {n+1}: line of {max(len(l) for l in body)} characters")
    note = ""
    if deep and vd:
        edge = [x for x in levels(mp4, [(b - 0.12, b + 0.12) for _, b, _ in cues[:-1]])]
        body = [x for x in levels(mp4, [(a + 0.15, b - 0.15) for a, b, _ in cues])]
        ref = sorted(x for x in body if x is not None)[len(body) // 2]
        on_break = sum(1 for x in edge if x is not None and x < ref - 5)
        over_speech = sum(1 for x in body if x is not None and x > ref - 8)
        note = (f" | speech {ref:.1f} dB | cue changes on a break in speech: "
                f"{on_break}/{len(edge)} | cues over speech: {over_speech}/{len(body)}")
    return problems, note


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", help="for example week06")
    ap.add_argument("--clip", action="append", help="clip id from clips.json; repeat for several")
    ap.add_argument("--verify", action="store_true", help="also check the cues against the mp4 audio")
    ap.add_argument("--no-copy", action="store_true")
    ap.add_argument("--force-marks", action="store_true")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool): die(f"{tool} not found on PATH")
    cfg = config()
    wdir = os.path.join(ROOT, "lectures", a.week)
    mpath = os.path.join(wdir, "clips.json")
    if not os.path.exists(mpath): die(f"{mpath} not found")
    clips = json.load(open(mpath, encoding="utf-8"))["clips"]
    if a.clip:
        unknown = set(a.clip) - {c["id"] for c in clips}
        if unknown: die(f"unknown clip id(s): {sorted(unknown)}")
        clips = [c for c in clips if c["id"] in a.clip]

    written, bad = [], 0
    for c in clips:
        text, cues = build(a.week, c, cfg, a.force_marks)
        out = os.path.join(wdir, "clips", "narrated", c["output"] + "-narrated.vtt")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8", newline="\n").write(text)
        written.append(out)
        problems, note = check(a.week, c, cues, a.verify)
        bad += len(problems)
        widest = max(max(len(l) for l in body) for _, _, body in cues)
        short = min(b - a2 for a2, b, _ in cues)
        print(f'- {c["id"]}: {len(cues)} cues, longest line {widest}, shortest cue '
              f'{short:.2f}s{note}')
        for p in problems: print("    ", p)

    if cfg.get("copy_clips_to") and not a.no_copy:
        m = re.fullmatch(r"week(\d+)", a.week)
        dest = os.path.join(cfg["copy_clips_to"],
                            f"Week {int(m.group(1)):02d}" if m else a.week, "clips", "narrated")
        os.makedirs(dest, exist_ok=True)
        for f in written: shutil.copy2(f, dest)
        print("copied to", dest)
    print(f"done: {len(written)} caption file(s)" + (f", {bad} problem(s)" if bad else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
