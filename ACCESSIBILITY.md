# Accessibility of the lecture clips

Advanced Biomedical AI (BME 6938), University of Florida. Last reviewed 21 October 2026.

This file records what has been done for the 37 animation clips, against WCAG 2.1, and the one
question that is still open. It covers the clips only. The GitHub Pages site that plays them has
not been audited, and neither have the slide decks or the notebooks.

Every clip exists in two versions: a silent one, with no audio track at all, and a narrated one,
whose voice is AI-generated from a script written for the course. Both are published, and the
narration being synthetic is stated wherever the clips appear.

## Where each criterion stands

| Criterion | Level | Applies to | State |
|---|---|---|---|
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | Silent clips | Met. Each has a transcript. |
| 1.2.2 Captions (Prerecorded) | A | Narrated clips | Met. 37 WebVTT files, one per clip. |
| 1.2.3 Audio Description or Media Alternative | A | Narrated clips | Met by the text alternative. |
| 1.2.5 Audio Description (Prerecorded) | AA | Narrated clips | Exemption claimed, see below. |
| 1.4.1 Use of Colour | A | Both | Met. |

A silent clip is video-only, so its text alternative is a transcript, which is
`lectures/weekNN/clips/transcripts/<output>.md`. A narrated clip is synchronized media, so it
needs captions, which are the `.vtt` file beside the video, and either a description or a full
text alternative. The transcript is the full text alternative, which is what satisfies 1.2.3 at
Level A.

1.2.5 is the one that is not settled. It asks for a description track at Level AA, and choosing
the text alternative at Level A does not carry over to it. It does not apply, however, when the
picture holds nothing the audio does not already say: W3C's note is "Where all of the video
information is already provided in existing audio."

## The case for the 1.2.5 exemption

The clips are written in a way that makes the exemption plausible rather than convenient. The
caption line on screen is a label of a few words, and the narration is not that line read out. It
restates the idea in full spoken form, averaging 35 words per segment across 252 segments, and it
speaks the quantities rather than pointing at them: "six of the ten patches are masked out", "here
twelve of sixteen", "a ninety-five percent interval from minus four to eight and a P value of zero
point six zero". A listener who never sees the picture still hears the argument, the numbers and
the conclusion.

`tools/check_description.py` tests this instead of asserting it. It reads the string constants
drawn by each scene, normalises the narration's spelled-out numbers to digits through
`tools/caption_text.py`, and reports the on-screen text that is never spoken. It is
one-directional and deliberately crude: it cannot judge whether a picture needs words at all, so
it never reports that a clip passes, only what a listener would not hear.

```
python tools/check_description.py                 every week
python tools/check_description.py week07 --verbose
python tools/check_description.py --strict        exit 1 on caveat, citation or colour
```

As of this review, across all 37 clips:

| Category | Count | What it is |
|---|---|---|
| caveat | 0 | A label such as "illustrative", "schematic" or "real output" |
| citation | 0 | An "X et al." credit whose first author is never named aloud |
| colour | 0 | Something the narration identifies by colour alone |
| other | 325 | Headings, axis labels and structural text |

The 325 in the last category are the reason the number looks large and mostly do not matter: a
slide heading, an axis label, a formula that the narration states in words instead of symbols. The
caption line already carries that content.

The first three categories were not zero when the check was first run on 21 October 2026. There
were 25 caveat labels, 13 citations and one colour-only reference, and they were closed the same
day by rewording 32 narration segments across 17 clips.

The caveat labels were the ones worth closing, and the reason was academic rather than legal.
Several clips use invented numbers to teach a method and mark them on screen as illustrative, so a
listener who does not hear that label may take a teaching figure for a published result. In a
graduate course that reads primary literature that is a worse failure than the compliance
question. The colour case was in `week13 clip2`, where the narration said "the red one is really
much smaller" of two curves; it now names the sepsis curve and lets the colour reinforce it, which
is how the rest of the course does it, as in "its query vector, in red, is compared with the key
vector of every token, in green".

## The position taken

The course treats the narration as satisfying 1.2.5 under the exemption above, on the evidence in
this file. That is a reading of the criterion rather than a ruling from UF's accessibility office,
and anyone who reads it differently is welcome to raise it, in which case the remedy is a
description track for 37 clips.

One caveat about the counts above. They are read from `clips.json`, which is the narration script,
and the 21 October rewording is in it. The published videos, their `.vtt` files and their
transcripts still carry the previous wording until the 17 affected clips are rendered again, which
regenerates only the changed narration lines, since the audio cache is keyed by text. Until that
render lands, the check reports zero and the files on disk do not yet agree with it.
