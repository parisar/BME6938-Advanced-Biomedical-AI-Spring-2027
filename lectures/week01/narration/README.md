# Narration for the Week 1 clips (ElevenLabs)

## What is here

| File | Purpose |
|---|---|
| narration.json | The spoken script: one line per on-screen caption, for all four clips |
| make_voice.py | Sends each line to ElevenLabs and saves one mp3 per line in `audio/` |

## Steps (Windows PowerShell)

1. Open PowerShell in this folder.
2. Set your API key for this window only (it is not saved anywhere):

   ```powershell
   $env:ELEVENLABS_API_KEY = "paste-your-key-here"
   ```

3. Check the script and the character count, without calling the API:

   ```powershell
   python make_voice.py --dry-run
   ```

4. List your voices and copy the ID of the one you want:

   ```powershell
   python make_voice.py --list-voices
   ```

5. Test on one clip first:

   ```powershell
   python make_voice.py --voice-id YOUR_VOICE_ID --clip clip2
   ```

6. Listen to the files in `audio/`. If a line sounds wrong, edit its `text` in narration.json, delete that mp3, and run the command again. Existing files are skipped.
7. When you are happy, generate the rest:

   ```powershell
   python make_voice.py --voice-id YOUR_VOICE_ID
   ```

Then tell Claude the audio is ready. The clips are re-rendered so each caption stays on screen for as long as its narration, and the audio is merged in.

## Notes

- Numbers and symbols are spelled out in the script ("two hundred fifty-six", "Q times K transpose") so they are read correctly.
- The default model is `eleven_multilingual_v2`. Use `--model` to choose another.
- `--stability` and `--similarity` adjust the voice settings (defaults 0.5 and 0.75).
