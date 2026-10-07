# Narration for the Week 1 clips (ElevenLabs)

## Everyday use

1. **Once per computer:** double-click `1 - Save API key (run once).bat` and paste your ElevenLabs API key. It is saved for your Windows account, not in this folder.
2. **Whenever you need audio:** double-click `2 - Generate narration.bat`. It generates every narration line that does not have an mp3 yet and saves it in `audio/`.

No typing of folders, keys, or voice IDs is needed after step 1.

## Files

| File | Purpose |
|---|---|
| narration.json | The spoken script: one line per on-screen caption, for all four clips |
| voice_config.json | Voice ID, model, and voice settings. Edit this to change the voice |
| make_voice.py | Sends each line to ElevenLabs and saves one mp3 per line in `audio/` |

## Changing a line

Edit its `text` in narration.json, delete (or rename) that line's mp3 in `audio/`, and double-click `2 - Generate narration.bat` again. Lines that already have audio are skipped, so nothing is generated twice.

## From a terminal (optional)

```powershell
python make_voice.py --dry-run          # show the script and character count, no API call
python make_voice.py --clip clip2       # one clip only
python make_voice.py --list-voices      # your voices and their IDs
python make_voice.py --force            # regenerate everything
```

## Notes

- Numbers and symbols are spelled out in the script ("two hundred fifty-six", "Q times K transpose") so they are read correctly.
- To remove the saved key later: Windows Settings, search "environment variables", delete ELEVENLABS_API_KEY under user variables.
