"""Write a plain-text transcript of every clip of one week.

    python tools/build_transcripts.py week06              every clip of the week
    python tools/build_transcripts.py week06 --clip clip2  one clip only
    python tools/build_transcripts.py week06 --no-copy     do not copy to "copy_clips_to"
    python tools/build_transcripts.py week06 --readme      print the table for the week README

One Markdown file per clip at lectures/weekNN/clips/transcripts/<output>.md: the clip title
as a heading, then the narration, one paragraph per segment, in the order the segments appear
in clips.json. No timestamps, so it reads as prose.

Why the narration and not the on-screen caption line: the caption line is a label of a few
words, while the narration is the clip's full explanation, which is what a student revising
needs and what makes the transcript a usable text alternative for the silent version. The
text goes through the same caption_text.py glossary the captions use, so the pronunciation
respellings are undone and the spelled-out numbers are written as digits.

The title comes from the TITLE of the scene class, so it is the title drawn in the clip
itself and the one the README table uses.

Needs nothing but clips.json and the scene files: no audio, no Manim, no API call.
"""
import argparse, json, os, re, shutil, sys, textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caption_text import convert

WRAP = 100          # the repository wraps prose rather than keeping one long line per paragraph


def fill(s):
    """Wrap to WRAP columns, never inside a word: a break inside a file name would break a link."""
    return "\n".join(textwrap.wrap(s, WRAP, break_long_words=False, break_on_hyphens=False))


def die(msg):
    sys.exit("ERROR: " + msg)


def config():
    cfg = {"copy_clips_to": ""}
    path = os.path.join(ROOT, "local_config.json")
    if os.path.exists(path):
        cfg.update(json.load(open(path, encoding="utf-8")))
    return cfg


def title(wdir, clip):
    """The TITLE of the clip's scene class, which is the title drawn in the clip."""
    src = open(os.path.join(wdir, clip["scene_file"]), encoding="utf-8").read()
    body = src.split(f'class {clip["scene"]}(')
    if len(body) < 2:
        die(f'{clip["scene_file"]}: no class {clip["scene"]}')
    m = re.search(r'^\s*TITLE\s*=\s*(["\'])(.*?)\1', body[1], re.M)
    if not m:
        die(f'{clip["scene_file"]}: class {clip["scene"]} has no TITLE')
    return m.group(2)


def transcript(week, wdir, clip, n, total):
    """The Markdown for one clip."""
    wk = int(re.fullmatch(r"week(\d+)", week).group(1))
    out = clip["output"]
    head = (f'Week {wk}, clip {n} of {total}. This is the narration of the clip, which an '
            f'AI-generated voice reads in the [narrated version](../narrated/{out}-narrated.mp4); '
            f'the [silent version](../silent/{out}.mp4) shows the same steps with on-screen '
            f'captions only.')
    paras = [f'# {title(wdir, clip)}', fill(head)]
    for s in clip["segments"]:
        paras.append(fill(convert(s["text"])))
    return "\n\n".join(paras) + "\n"


def table(wdir, clips):
    """The transcripts table for the week README."""
    rows = [f'| {n}. {title(wdir, c)} | [{c["output"]}.md](clips/transcripts/{c["output"]}.md) |'
            for n, c in enumerate(clips, 1)]
    return "\n".join(["| Clip | Transcript |", "|---|---|"] + rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", help="for example week06")
    ap.add_argument("--clip", action="append", help="clip id from clips.json; repeat for several")
    ap.add_argument("--no-copy", action="store_true")
    ap.add_argument("--readme", action="store_true", help="print the table for the week README")
    a = ap.parse_args()

    wdir = os.path.join(ROOT, "lectures", a.week)
    mpath = os.path.join(wdir, "clips.json")
    if not os.path.exists(mpath): die(f"{mpath} not found")
    all_clips = json.load(open(mpath, encoding="utf-8"))["clips"]
    if a.readme:
        print(table(wdir, all_clips))
        return 0

    clips = all_clips
    if a.clip:
        unknown = set(a.clip) - {c["id"] for c in clips}
        if unknown: die(f"unknown clip id(s): {sorted(unknown)}")
        clips = [c for c in clips if c["id"] in a.clip]

    written = []
    for c in clips:
        n = [x["id"] for x in all_clips].index(c["id"]) + 1
        text = transcript(a.week, wdir, c, n, len(all_clips))
        out = os.path.join(wdir, "clips", "transcripts", c["output"] + ".md")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8", newline="\n").write(text)
        written.append(out)
        words = sum(len(convert(s["text"]).split()) for s in c["segments"])
        print(f'- {c["id"]}: {len(c["segments"])} paragraphs, {words} words')

    cfg = config()
    if cfg.get("copy_clips_to") and not a.no_copy:
        m = re.fullmatch(r"week(\d+)", a.week)
        dest = os.path.join(cfg["copy_clips_to"],
                            f"Week {int(m.group(1)):02d}" if m else a.week, "clips", "transcripts")
        os.makedirs(dest, exist_ok=True)
        for f in written: shutil.copy2(f, dest)
        print("copied to", dest)
    print(f"done: {len(written)} transcript(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
