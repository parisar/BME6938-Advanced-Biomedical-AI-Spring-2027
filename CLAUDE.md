# Advanced Biomedical AI (BME 6938), Spring 2027

Course repository for a graduate course at the University of Florida taught by Dr. Parisa Rashidi.
Tuesdays are a short lecture with animation clips, Thursdays are student-led paper sessions, and there is a term project.
The weekly plan is in `README.md`.

## Layout

| Path | What it is |
|---|---|
| `README.md` | Course overview and dated schedule |
| `syllabus/`, `papers/`, `presentations/`, `project/` | Syllabus PDF, reading list, rubrics, project guidelines |
| `lectures/weekNN/` | One folder per week: `clips.json`, `animations/`, `clips/`, a README |
| `lectures/notebooks/` | Ungraded reference notebooks, one per lecture |
| `lectures/_shared/kit.py` | Shared Manim kit used by every clip (colors, caption bar, token boxes, matrices) |
| `tools/build_clips.py` | Builds a week's clips end to end |
| `local_config.json` | Local only, never committed: ElevenLabs voice ID and an optional copy destination |

Slide decks (PowerPoint) are kept outside this repository in the instructor's Dropbox course folder.

## Building clips

```
python tools/build_clips.py week04            # all clips of the week, silent and narrated
python tools/build_clips.py week04 --clip clip2
python tools/build_clips.py week04 --quality l   # fast preview
python tools/build_clips.py week04 --dry-run     # shows how many characters would be sent to ElevenLabs
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
5. Update `lectures/weekNN/README.md` and the table in `lectures/README.md`.

Use `lectures/week04` as the reference for all of this.

## Clip conventions

- Two or three clips per session, each on one concept, about one minute silent and under two minutes narrated.
- White background, Inter font (bundled in `lectures/_shared/fonts`), title at top left, caption at the bottom.
- Text only: do not use `MathTex` or `Tex`, so LaTeX is never required. Write formulas with Unicode, for example `softmax( Q·Kᵀ / √d ) · V`.
- Colors carry meaning and stay fixed across the course: queries red (`QC`), keys green (`KC`), values blue (`VC`), UF blue for titles.
- Every example must be biomedical (clinical text, ECG, pathology, imaging, EHR). Never use generic examples such as translation sentences. Reuse the running example of the matching lecture ("The patient has a cold" for the transformer review; a single-lead ECG and pathology tiles for self-supervised learning).
- Make everything large enough for a lecture hall projector: matrix cells at least 0.36 units, labels at least 20 pt.
- Captions are one sentence, plain and exact. Every caption must be readable for at least three seconds.
- After rendering, always inspect frames for overlapping or clipped elements before calling a clip finished.
- To reach the target length, set the optional class settings on the scene instead of editing every timing: `PACE` multiplies
  every `run_time` passed to `play()`, and `HOLD` adds seconds after every caption. Waits are not affected.
- Kit helpers: `ecg_fn()` and `wave()` draw a synthetic ECG; `vdots()` draws a vertical ellipsis (Inter has no `⋮` glyph).

## Narration conventions

- One narration line per caption. It says the caption's idea in fuller spoken form, not the caption word for word.
- Spell out what a voice would stumble on: "two hundred fifty-six", "Q times K transpose", "the square root of d", "G P T".
- Aim for 15 to 35 words per line.
- The narration is an AI-generated voice. Say so wherever narrated clips are published.

## Writing style for anything students or colleagues will read

- No em-dashes. Use commas, colons, or separate sentences.
- Use standard AI/ML terminology (encoder, prediction head, fine-tuning, linear probe), not vague lay verbs.
- All examples in slides, clips, notebooks, and rubrics are biomedical.
- Keep the syllabus general; put term-specific details (team size, dates, specific topics) in the READMEs.
- The final two weeks of the term are reserved for project presentations: no lectures or paper sessions.

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
