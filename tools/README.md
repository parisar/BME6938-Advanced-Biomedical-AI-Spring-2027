# Tools

## build_clips.py

Builds the animation clips for one week: narration audio, a silent video and a narrated video per clip.

```
python tools/build_clips.py week06
```

See the top of the script for all options, and `CLAUDE.md` in the repository root for the conventions.

## build_captions.py

Writes the WebVTT caption file for each narrated clip of a week, beside its video.

```
python tools/build_captions.py week06 --verify
```

It makes no ElevenLabs call: the cue text comes from the narration in `clips.json` (with the pronunciation
respellings undone by `caption_text.py`), and the cue times come from the segment start times the kit recorded when
the video was built, which the script regenerates by replaying the scene with Manim's `--dry_run`. The timings are
cached in `.cache/marks`. `--verify` reports whether each cue change lands on a break in the narration audio.

## One-time setup

1. Install Python 3.10 or later, Manim and ffmpeg:

   ```
   pip install -r tools/requirements.txt
   winget install ffmpeg        # Windows; on macOS use: brew install ffmpeg
   ```

2. Copy `local_config.example.json` to `local_config.json` and fill in your ElevenLabs `voice_id`.
   Optionally set `copy_clips_to` to a folder that should also receive the finished videos
   (they are copied to `<folder>/Week NN/clips/`).
3. Store your ElevenLabs API key in the `ELEVENLABS_API_KEY` environment variable.
   On Windows, double-click `save_api_key.bat`.

`local_config.json` and the audio cache are ignored by git.
