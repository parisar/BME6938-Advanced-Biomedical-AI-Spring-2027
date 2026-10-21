"""Check whether the narration already describes the picture, for WCAG 2.1 criterion 1.2.5.

    python tools/check_description.py                 every week
    python tools/check_description.py week07          one week
    python tools/check_description.py --verbose       also list the long tail of unspoken text
    python tools/check_description.py --strict        exit 1 if anything in the first two
                                                      categories is unspoken, for a gate

Criterion 1.2.5, Audio Description (Prerecorded), is Level AA and asks for a description
track on prerecorded video. It does not apply when all of the important information in the
picture is already in the audio: W3C's note is "Where all of the video information is already
provided in existing audio", no further description is needed. The narrated clips are written
that way on purpose, because the narration says the caption's idea in fuller spoken form
rather than reading the caption out, so the claim is plausible. This script tests it instead
of assuming it.

The test is deliberately crude and one-directional: it finds text that is drawn on screen and
never spoken. It cannot judge whether a picture needs words at all, so it never says a clip
passes, only which on-screen text a listener would not hear. Three categories matter, in
order:

  caveat    A label such as "illustrative", "schematic" or "real output". These carry the most
            risk of the three, and the risk is academic rather than legal: a listener who does
            not hear "illustrative numbers" may take a teaching figure for a published result.
  citation  An "X et al." credit whose first author is never named in the narration.
  colour    Narration that identifies something by colour alone ("the red one"), which a
            listener cannot resolve and which is also criterion 1.4.1.
  other     Everything else drawn on screen and not spoken, which is mostly headings, axis
            labels and structural text that the caption line already carries. Shown only with
            --verbose, and expected to be long.

On-screen text comes from the string constants of the scene file, read with ast so that
docstrings and f-string fragments are left out. The narration goes through caption_text.convert
first, so "twelve of sixteen" in the script matches "12 of 16" on screen and the numbers do not
produce a page of false hits.

OK below holds the on-screen text that is deliberately not spoken. Add to it rather than
rewording a clip to satisfy the script.
"""
import argparse, ast, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from caption_text import convert

# On-screen text that is fine to leave unspoken, as {week: {text, ...}}. A licence line is a
# credit required by the licence rather than something a listener needs; the running-example
# sentence is read out in full elsewhere in the same clip.
OK = {
    "week03": {"Kather et al. 2016, CC BY 4.0"},
}

CAVEAT = re.compile(r"illustrative|schematic|stylized|stylised|real output|drawn for this clip", re.I)
CITE = re.compile(r"\b([A-Z][a-z]+)\s+et\s+al\.?")
# A colour word next to a demonstrative or an article is a colour used as a name.
COLOUR_NAME = re.compile(
    r"\b(?:the|this|that|these|those|one)\s+(red|green|blue|orange|purple|yellow|gr[ae]y|pink|teal)\s+"
    r"(?:one|ones|curve|line|box|cell|row|column|dot|dots|point|points|bar|bars|area|region|part)\b",
    re.I,
)
MIN_WORDS = 3          # below this, on-screen text is a label, not a statement


def die(msg):
    sys.exit("ERROR: " + msg)


def screen_text(path):
    """Every string constant drawn in a scene file, without docstrings or f-string fragments.

    ast gives the constants directly, which is what keeps the helper docstrings in the shared
    kit out of the results: a docstring is the first statement of its module, class or function,
    so it is reachable and has to be removed by hand.
    """
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except SyntaxError as e:
        die(f"{path}: {e}")
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            first = node.body[0] if node.body else None
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                    and isinstance(first.value.value, str):
                docs.add(id(first.value))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docs:
            out.append(node.value)
        elif isinstance(node, ast.JoinedStr):
            # An f-string: keep its literal pieces, drop the {...} holes, which are values that
            # only exist once the scene runs.
            out.extend(v.value for v in node.values
                       if isinstance(v, ast.Constant) and isinstance(v.value, str))
    return out


def spoken(clip):
    """The clip's narration and captions as one lowercase string, numbers written as digits."""
    said = " ".join(s["text"] for s in clip["segments"])
    shown = " ".join(s["caption"] for s in clip["segments"])
    return (convert(said) + " " + shown).lower()


def is_spoken(text, said):
    """True if the on-screen text, or nearly all of its content words, is in the narration."""
    t = text.lower().strip(" “”\"'.,:;()")
    if not t:
        return True
    if t in said:
        return True
    words = re.findall(r"[a-z]{4,}", t)
    return bool(words) and sum(1 for w in words if w in said) / len(words) >= 0.75


def check(week):
    """Every unspoken on-screen string of one week, as a list of (clip, category, text)."""
    wdir = os.path.join(ROOT, "lectures", week)
    manifest = os.path.join(wdir, "clips.json")
    if not os.path.exists(manifest):
        die(f"no clips.json for {week}")
    found = []
    for clip in json.load(open(manifest, encoding="utf-8"))["clips"]:
        scene = os.path.join(wdir, clip["scene_file"])
        if not os.path.exists(scene):
            die(f'{week} {clip["id"]}: no {clip["scene_file"]}')
        said = spoken(clip)
        said_digits = convert(" ".join(s["text"] for s in clip["segments"])).lower()

        # Colour used as a name, which is a problem in the narration itself rather than on screen.
        for m in COLOUR_NAME.finditer(" ".join(s["text"] for s in clip["segments"])):
            found.append((clip["id"], "colour", m.group(0).strip()))

        seen = set()
        for text in screen_text(scene):
            text = text.strip()
            if text in OK.get(week, ()) or text in seen:
                continue
            seen.add(text)
            if CAVEAT.search(text) and not is_spoken(text, said):
                # A caveat counts as spoken if its own keyword is, anywhere in the clip: one
                # "these numbers are illustrative" covers the labels on the same picture.
                word = CAVEAT.search(text).group(0).lower()
                if word not in said:
                    found.append((clip["id"], "caveat", text))
                continue
            m = CITE.search(text)
            if m and m.group(1).lower() not in said_digits:
                found.append((clip["id"], "citation", text))
                continue
            if len(text.split()) >= MIN_WORDS and not is_spoken(text, said):
                found.append((clip["id"], "other", text))
    return found


def main():
    ap = argparse.ArgumentParser(description="Check the narration against the picture (WCAG 1.2.5).")
    ap.add_argument("week", nargs="?", help="week folder, for example week07; default every week")
    ap.add_argument("--verbose", action="store_true", help='also list the "other" category')
    ap.add_argument("--strict", action="store_true", help="exit 1 on any caveat, citation or colour")
    args = ap.parse_args()

    weeks = [args.week] if args.week else \
        sorted(os.path.basename(os.path.dirname(p))
               for p in glob.glob(os.path.join(ROOT, "lectures", "week*", "clips.json")))
    if not weeks:
        die("no weeks found")

    order = ["caveat", "citation", "colour", "other"]
    totals = dict.fromkeys(order, 0)
    clips = 0
    for week in weeks:
        rows = check(week)
        clips += len(json.load(open(os.path.join(ROOT, "lectures", week, "clips.json"),
                                    encoding="utf-8"))["clips"])
        for cat in order:
            hits = [r for r in rows if r[1] == cat]
            totals[cat] += len(hits)
            if not hits or (cat == "other" and not args.verbose):
                continue
            print(f"{week}  {cat}")
            for cid, _, text in hits:
                print(f"    {cid:7} {text}")

    print()
    print(f"{clips} clips in {len(weeks)} week(s)")
    for cat in order:
        tail = "" if cat != "other" or args.verbose else "  (--verbose to list)"
        print(f"  {cat:9} {totals[cat]:4}{tail}")
    print()
    print("A listener hears none of the above. caveat and citation are worth closing;")
    print("other is mostly headings and labels the caption line already carries.")
    if args.strict and any(totals[c] for c in ("caveat", "citation", "colour")):
        sys.exit(1)


if __name__ == "__main__":
    main()
