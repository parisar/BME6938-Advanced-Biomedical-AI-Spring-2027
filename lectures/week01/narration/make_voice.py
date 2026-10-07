"""Generate narration audio for the animation clips with the ElevenLabs API.

Uses only the Python standard library.

- The API key is read from the ELEVENLABS_API_KEY environment variable (saved once
  per computer with "1 - Save API key (run once).bat"). It is never written to this folder.
- The voice ID and voice settings are read from voice_config.json in this folder.

  python make_voice.py                    generate every segment that has no audio yet
  python make_voice.py --clip clip2       one clip only
  python make_voice.py --dry-run          show what would be generated and the character count
  python make_voice.py --list-voices      show your voices and their IDs
  python make_voice.py --voice-id ID      use a different voice for this run

Audio is saved as audio/<segment id>.mp3 next to this script. Existing files are
skipped, so you can re-run after editing narration.json; delete or rename a file
(or use --force) to regenerate it.
"""
import argparse, json, os, sys, urllib.request, urllib.error

API = "https://api.elevenlabs.io/v1"
HERE = os.path.dirname(os.path.abspath(__file__))


def call(path, key, body=None):
    req = urllib.request.Request(API + path, headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "*/*"},
                                 data=json.dumps(body).encode("utf-8") if body is not None else None,
                                 method="POST" if body is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f"ElevenLabs returned HTTP {e.code} for {path}:\n{e.read().decode('utf-8', 'replace')[:800]}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach ElevenLabs: {e.reason}")


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key and sys.platform == "win32":          # saved with setx but this window was opened before that
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                key = winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0]
        except OSError:
            key = None
    return (key or "").strip()


def main():
    cfg_path = os.path.join(HERE, "voice_config.json")
    cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--voice-id", default=cfg.get("voice_id")); ap.add_argument("--clip", help="only this clip, for example clip2")
    ap.add_argument("--model", default=cfg.get("model", "eleven_multilingual_v2"))
    ap.add_argument("--format", default="mp3_44100_128")
    ap.add_argument("--stability", type=float, default=cfg.get("stability", 0.5)); ap.add_argument("--similarity", type=float, default=cfg.get("similarity", 0.75))
    ap.add_argument("--list-voices", action="store_true"); ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    clips = json.load(open(os.path.join(HERE, "narration.json"), encoding="utf-8"))["clips"]
    if a.clip:
        clips = [c for c in clips if c["clip"] == a.clip]
        if not clips: sys.exit(f"No clip named {a.clip} in narration.json")
    segs = [(c["clip"], i, c["segments"]) for c in clips for i in range(len(c["segments"]))]
    chars = sum(len(s[i]["text"]) for _, i, s in segs)

    if a.dry_run:
        for _, i, s in segs: print(f'{s[i]["id"]}  ({len(s[i]["text"])} chars)  {s[i]["text"]}')
        print(f"\n{len(segs)} segments, {chars} characters in total.")
        return

    key = api_key()
    if not key: sys.exit('No API key found. Double-click "1 - Save API key (run once).bat" first.')

    if a.list_voices:
        for v in json.loads(call("/voices", key)).get("voices", []):
            print(f'{v["voice_id"]}  {v["name"]}  ({v.get("category", "")})')
        return
    if not a.voice_id: sys.exit("No voice ID. Put one in voice_config.json or pass --voice-id (use --list-voices to see your voices).")
    print("Voice:", a.voice_id, "| model:", a.model)

    out = os.path.join(HERE, "audio"); os.makedirs(out, exist_ok=True)
    made = 0
    for _, i, s in segs:
        f = os.path.join(out, s[i]["id"] + ".mp3")
        if os.path.exists(f) and not a.force:
            print("skip (exists)", s[i]["id"]); continue
        body = {"text": s[i]["text"], "model_id": a.model,
                "voice_settings": {"stability": a.stability, "similarity_boost": a.similarity}}
        if i > 0: body["previous_text"] = s[i - 1]["text"]            # keeps intonation consistent across segments
        if i < len(s) - 1: body["next_text"] = s[i + 1]["text"]
        audio = call(f"/text-to-speech/{a.voice_id}?output_format={a.format}", key, body)
        open(f, "wb").write(audio); made += 1
        print("wrote", s[i]["id"], f"({len(audio) // 1000} kB)")
    print(f"\nDone: {made} new files in {out}")


if __name__ == "__main__":
    main()
