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
| 1.4.1 Use of Colour | A | Both | Met, with one exception noted below. |

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
| caveat | 25 | A label such as "illustrative", "schematic" or "real output" |
| citation | 13 | An "X et al." credit whose first author is never named aloud |
| colour | 1 | Something the narration identifies by colour alone |
| other | 317 | Headings, axis labels and structural text |

The 317 in the last category are the reason the number looks alarming and mostly do not matter: a
slide heading, an axis label, a formula that the narration states in words instead of symbols. The
caption line already carries that content.

The first two categories are the real residual, and the caveat labels are the ones worth closing.
The risk there is academic rather than legal. Several clips use invented numbers to teach a method
and mark them on screen as illustrative, and a listener who does not hear that label may take a
teaching figure for a published result. In a graduate course that reads primary literature, that
is a worse failure than the compliance question. Four clips do say it aloud, which shows the fix
is a sentence, not a redesign.

The colour case is `week13 clip2`, where the narration says "the red one is really much smaller"
of two curves. The sentence makes red and sepsis line up by implication, but it is the one place
where colour does the naming, and it is also the single 1.4.1 exception. Everywhere else the
narration names the thing and treats colour as reinforcement, as in "its query vector, in red, is
compared with the key vector of every token, in green".

## The open question

Whether the narration already counts as audio description under 1.2.5 is a judgement for UF's
accessibility office, not something more files can settle. The evidence above is what they need in
order to answer it, and the answer decides between two outcomes: the clips conform at AA as they
are, or 37 clips need a separate description track.

Closing the caveat and citation gaps is worth doing whichever way that goes, and it is a bounded
job. It means rewording about 15 clips in `clips.json`, regenerating the narration audio for the
changed lines only, since the cache is keyed by text, re-rendering those narrated videos, and
rebuilding their captions and transcripts.
