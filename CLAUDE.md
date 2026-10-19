# Advanced Biomedical AI (BME 6938), Spring 2027

Course repository for a graduate course at the University of Florida taught by Dr. Parisa Rashidi.
Tuesdays are a short lecture with animation clips, Thursdays are student-led paper sessions, and there is a term project.
The weekly plan is in `README.md`.

## Layout

| Path | What it is |
|---|---|
| `README.md` | Course overview and dated schedule |
| `syllabus/`, `papers/`, `presentations/`, `project/` | Syllabus PDF, reading list, rubrics, project guidelines |
| `lectures/weekNN/` | One folder per week: `clips.json`, `animations/`, `clips/`, `slides/` (deck PDF), a README |
| `lectures/notebooks/` | Ungraded reference notebooks, one per lecture |
| `lectures/_shared/kit.py` | Shared Manim kit used by every clip (colors, caption bar, token boxes, matrices) |
| `assets/banners/` | Course and week banner images, shared with the Canvas course map and modules |
| `tools/build_clips.py` | Builds a week's clips end to end |
| `local_config.json` | Local only, never committed: ElevenLabs voice ID and an optional copy destination |

Slide decks (PowerPoint) are built and kept outside this repository, in the instructor's Dropbox course folder. A
PDF of each deck, exported without the embedded clips, is committed to `lectures/weekNN/slides/` so that students have
the slides alongside the clips and notebooks. Re-export that PDF whenever a deck changes.

## Building clips

```
python tools/build_clips.py week06            # all clips of the week, silent and narrated
python tools/build_clips.py week06 --clip clip2
python tools/build_clips.py week06 --quality l   # fast preview
python tools/build_clips.py week06 --dry-run     # shows how many characters would be sent to ElevenLabs
```

The script generates narration audio (ElevenLabs), renders each scene with Manim, merges the audio, and writes only
finished videos to `lectures/weekNN/clips/silent` and `lectures/weekNN/clips/narrated`. Intermediate files go to a
temporary folder that is deleted. Narration audio is cached in `.cache/audio` (ignored by git) keyed by the text and
voice, so only new or reworded lines are generated again.

Before building, run `--dry-run` and tell the user the character count if it is more than a few thousand.
The API key comes from the `ELEVENLABS_API_KEY` environment variable. Never print it, write it to a file, or commit it.

## Adding a new week of clips

1. Create `lectures/weekNN/animations/clipK_<topic>.py`. Start with `from kit import *` and subclass `Clip`.
   Name the scene classes `C1`, `C2`, ... (the clip id is derived from the class name: `C2` is `clip2`).
2. Call `self.cap("...")` for every on-screen caption. Each caption is one narration segment.
3. Add the clip to `lectures/weekNN/clips.json` with `id`, `scene_file`, `scene`, `output`, and one `segments` entry
   per caption, in order. The number of segments must equal the number of `self.cap` calls.
4. Preview with `--quality l`, look at frames from the result, fix layout problems, then build at full quality.
5. Build the captions: `python tools/build_captions.py weekNN --verify` (see below).
6. Build the transcripts: `python tools/build_transcripts.py weekNN` (see below).
7. Update `lectures/weekNN/README.md` and the table in `lectures/README.md`.

Use `lectures/week06` as the reference for all of this.

## Captions

Every narrated clip needs a WebVTT caption file next to its video, for accessibility:
`lectures/weekNN/clips/narrated/<output>-narrated.vtt`. A new or reworded narrated clip is not finished until its
`.vtt` is rebuilt the same way, and the file is committed with the video.

```
python tools/build_captions.py week06            all clips of the week, and copy to "copy_clips_to"
python tools/build_captions.py week06 --verify   also check the cues against the mp4's own audio
```

The script makes no API call. It takes the cue text from the narration in `clips.json`, undoing the pronunciation
respellings and writing the spelled-out numbers as digits, because captions are read rather than heard
(`tools/caption_text.py` holds the glossary and the per-clip exceptions; add to it rather than hand-editing a `.vtt`).

The cue times come from the same segment start times the kit records when the narrated video is built, which the
script regenerates by replaying the scene with Manim's `--dry_run`. Do not time captions by adding up the narration
lengths: a narrated video is not the segments joined end to end, and the gaps hold the animations, so the error grows
to several seconds by the end of a clip.

## Transcripts

Every clip also needs a plain-text transcript at `lectures/weekNN/clips/transcripts/<output>.md`: the clip title as a
heading, then the narration, one paragraph per segment, in order and without timestamps. The silent version has no
audio, so the transcript is its text alternative (WCAG 2.1 criterion 1.2.1), and students use it to revise.

```
python tools/build_transcripts.py week06            every clip, and copy to "copy_clips_to"
python tools/build_transcripts.py week06 --readme   print the table for the week README
```

It reads `clips.json` and the scene files only: no audio, no Manim, no API call. The text goes through the same
`caption_text.py` glossary as the captions, so a transcript and the `.vtt` beside it always say the same words. A new
or reworded clip is not finished until its transcript is rebuilt and committed, like its captions.

## Banners

`assets/banners/` holds the course banner and one per week, the same artwork Canvas shows on the course map and at
the top of each module, so the repository and the Canvas course look like one course. `tools/build_banners.py`
rewrites the visual course map in `lectures/README.md` from that file's own index table, and puts each week's banner
under the heading of its week README. Run it after changing a week's title or links; it is idempotent, so running it
twice changes nothing.

The banner on a week README repeats the heading beside it, so its alt text describes the drawing instead. In the
course map the banner is a link, so its alt names the week and topic it leads to. The top-level README's banner
repeats the title and instructor underneath it and has empty alt, which is what stops a screen reader saying all of
it twice. `assets/banners/alt.json` holds the descriptions. The week banners have a light background and will look
like a bright panel in GitHub's dark theme.

## Clip conventions

- Two or three clips per session, each on one concept. Clarity comes first: about one minute silent and two minutes narrated is a guide, not a limit, so let a clip run longer when the explanation needs it.
- White background, Inter font (bundled in `lectures/_shared/fonts`), title at top left, caption at the bottom.
- Text only: do not use `MathTex` or `Tex`, so LaTeX is never required. Write formulas with Unicode, for example `softmax( Q·Kᵀ / √d ) · V`.
- Colors carry meaning and stay fixed across the course: queries red (`QC`), keys green (`KC`), values blue (`VC`), UF blue for titles.
- Every example must be biomedical (clinical text, ECG, pathology, imaging, EHR). Never use generic examples such as translation sentences. Reuse the running example of the matching lecture ("The patient has a cold" for the transformer review; a single-lead ECG and pathology tiles for self-supervised learning).
- Make everything large enough for a lecture hall projector: matrix cells at least 0.36 units, labels at least 20 pt.
- Captions are one sentence, plain and exact. Every caption must be readable for at least three seconds.
- After rendering, always inspect frames for overlapping or clipped elements before calling a clip finished.
- Caption first: start each segment with `self.cap("...", hold=0)`, then play that segment's animations (including fading out the previous ones), then `self.rest(h)`. The narration of a segment starts with its caption, so this keeps every picture under its own narration and avoids a silent lag at the start.
- To reach the target length, set the optional class settings on the scene instead of editing every timing: `PACE` multiplies
  every `run_time` passed to `play()`, and `HOLD` adds seconds after every caption. Waits are not affected.
- Kit helpers: `ecg_fn()` and `wave()` draw a synthetic ECG; `vdots()` draws a vertical ellipsis (Inter has no `⋮` glyph).

## Narration conventions

- One narration line per caption. It says the caption's idea in fuller spoken form, not the caption word for word.
- Spell out what a voice would stumble on: "two hundred fifty-six", "Q times K transpose", "the square root of d", "G P T".
- Respell words the voice mispronounces, in the narration only (captions keep the normal spelling): "co-sine", "rope" for RoPE, "Alibi" for ALiBi, "Kwen" for Qwen, "Modern BERT".
- Aim for 15 to 35 words per line.
- The narration is an AI-generated voice. Say so wherever narrated clips are published.

## Writing style for anything students or colleagues will read

- No em-dashes. Use commas, colons, or separate sentences.
- Use standard AI/ML terminology (encoder, prediction head, fine-tuning, linear probe), not vague lay verbs.
- All examples in slides, clips, notebooks, and rubrics are biomedical.
- Keep the syllabus general; put term-specific details (team size, dates, specific topics) in the READMEs.
- The final two weeks of the term are reserved for project presentations: no lectures or paper sessions.
- Weeks 4 and 5 (modern LLM architectures; post-training and reasoning) draw on Sebastian Raschka's Ahead of AI articles and his
  LLMs-from-scratch repository. His code is Apache 2.0: it may be adapted into notebooks with a credit line and link. His figures
  have no reuse license: redraw them in the course style with biomedical examples and cite him; never paste his figures.

## Notebooks

Notebooks are ungraded reference code in `lectures/notebooks/`, one per lecture. Each follows its lecture step by step,
names the slide each section matches, uses the same running example and numbers as the slides, explains every step in
text before the code, and comments every line. They must run on Google Colab and on HiPerGator on CPU. Use open data or
synthetic data only. Never commit patient data, credentials, or credentialed datasets.

## Git

Commit finished clips, source, and manifests. Do not commit `local_config.json`, `.cache/`, or Manim `media/` folders.
Ask before pushing if the user has not asked for it. The repository is private for now and will be made public in January 2027, before the term. Keep everything in it
safe to publish: no student names, group assignments, or grades (those stay on Canvas); no paper PDFs, only links;
no API keys or local config; no slide decks with third-party figures unless the instructor has reviewed them.
Each notebook starts with an Open in Colab badge (added by `add_badge.py` in the build folder); the badges work for
students once the repository is public.
