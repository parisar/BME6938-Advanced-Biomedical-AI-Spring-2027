# Tools

## build_clips.py

Builds the animation clips for one week: narration audio, a silent video and a narrated video per clip.

```
python tools/build_clips.py week01
```

See the top of the script for all options, and `CLAUDE.md` in the repository root for the conventions.

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
