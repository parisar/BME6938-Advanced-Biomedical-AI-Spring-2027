"""Build the animation clips for one week: narration audio, silent and narrated videos.

    python tools/build_clips.py week01                 build every clip of week 1
    python tools/build_clips.py week01 --clip clip2    one clip only
    python tools/build_clips.py week01 --only silent   skip narration (no API call)
    python tools/build_clips.py week01 --quality l     fast low-resolution preview
    python tools/build_clips.py week01 --dry-run       show the plan and the characters to be sent to ElevenLabs

What it does
    1. Reads lectures/<week>/clips.json (scene files and the narration line for every caption).
    2. Gets the audio for each narration line from the local cache, or from ElevenLabs if the line is new or changed.
    3. Renders each scene with Manim: once silent, once timed to the narration.
    4. Merges the narration into the narrated render.
    5. Writes only the finished videos to lectures/<week>/clips/silent and lectures/<week>/clips/narrated
       (and copies them to "copy_clips_to" from local_config.json, if set).
All intermediate files live in a temporary folder that is removed at the end.

Needs: Python 3.10+, manim, ffmpeg and ffprobe on PATH. Narration also needs local_config.json (voice_id)
and the ELEVENLABS_API_KEY environment variable (tools/save_api_key.bat stores it on Windows).
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "audio")
API = "https://api.elevenlabs.io/v1"
QUALITY = {"h": ["-qh", "--fps", "30"], "m": ["-qm"], "l": ["-ql"]}


def die(msg):
    sys.exit("ERROR: " + msg)


def run(cmd, **kw):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        die("command failed: " + " ".join(map(str, cmd[:6])) + " ...\n" + r.stdout[-3000:])
    return r.stdout


def duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key and sys.platform == "win32":      # saved with setx after this terminal was opened
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
                key = winreg.QueryValueEx(k, "ELEVENLABS_API_KEY")[0]
        except OSError:
            key = None
    return (key or "").strip()


def seg_hash(text, cfg):
    blob = json.dumps([text, cfg["voice_id"], cfg["model"], cfg["stability"], cfg["similarity"]], ensure_ascii=False)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()


def tts(text, prev, nxt, cfg, key):
    body = {"text": text, "model_id": cfg["model"], "voice_settings": {"stability": cfg["stability"], "similarity_boost": cfg["similarity"]}}
    if prev: body["previous_text"] = prev
    if nxt: body["next_text"] = nxt
    req = urllib.request.Request(f'{API}/text-to-speech/{cfg["voice_id"]}?output_format=mp3_44100_128', method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "*/*"},
                                 data=json.dumps(body).encode("utf-8"))
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        die(f"ElevenLabs returned HTTP {e.code}:\n{e.read().decode('utf-8', 'replace')[:800]}")
    except urllib.error.URLError as e:
        die(f"could not reach ElevenLabs: {e.reason}")


def render(scene_file, scene, quality, media_dir, cwd, env):
    cmd = [sys.executable, "-m", "manim", *QUALITY[quality], "--disable_caching", "--media_dir", media_dir, scene_file, scene]
    run(cmd, cwd=cwd, env=env)
    hits = [os.path.join(d, f) for d, _, fs in os.walk(os.path.join(media_dir, "videos")) for f in fs if f == scene + ".mp4" and "partial_movie_files" not in d]
    if not hits: die(f"Manim produced no video for {scene}")
    return hits[0]


def encode(args_in, out):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".part.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", *args_in, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20", "-movflags", "+faststart", tmp])
    os.replace(tmp, out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("week", help="for example week01")
    ap.add_argument("--clip", action="append", help="clip id from clips.json; repeat for several")
    ap.add_argument("--only", choices=["silent", "narrated"])
    ap.add_argument("--quality", choices=list(QUALITY), default="h")
    ap.add_argument("--no-cache", action="store_true", help="regenerate all narration audio and do not keep it")
    ap.add_argument("--seed-audio", metavar="DIR", help="import existing <clip>_sNN.mp3 files into the cache instead of calling the API")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    wdir = os.path.join(ROOT, "lectures", a.week)
    mpath = os.path.join(wdir, "clips.json")
    if not os.path.exists(mpath): die(f"{mpath} not found")
    clips = json.load(open(mpath, encoding="utf-8"))["clips"]
    if a.clip:
        unknown = set(a.clip) - {c["id"] for c in clips}
        if unknown: die(f"unknown clip id(s): {sorted(unknown)}")
        clips = [c for c in clips if c["id"] in a.clip]
    do_silent, do_narr = a.only != "narrated", a.only != "silent"

    cfg = {"voice_id": "", "model": "eleven_multilingual_v2", "stability": 0.5, "similarity": 0.75, "copy_clips_to": ""}
    cpath = os.path.join(ROOT, "local_config.json")
    if os.path.exists(cpath): cfg.update(json.load(open(cpath, encoding="utf-8")))

    # ---- plan the narration audio
    todo = []
    if do_narr:
        if not cfg["voice_id"]: die("no voice_id. Copy local_config.example.json to local_config.json and fill it in.")
        for c in clips:
            for i, s in enumerate(c["segments"]):
                s["_hash"] = seg_hash(s["text"], cfg)
                s["_cached"] = os.path.join(CACHE, s["_hash"] + ".mp3")
                if a.seed_audio:
                    src = os.path.join(a.seed_audio, f'{c["id"]}_s{i + 1:02d}.mp3')
                    if os.path.exists(src) and not os.path.exists(s["_cached"]):
                        os.makedirs(CACHE, exist_ok=True); shutil.copyfile(src, s["_cached"])
                if a.no_cache or not os.path.exists(s["_cached"]): todo.append((c, i))
    chars = sum(len(c["segments"][i]["text"]) for c, i in todo)
    print(f'{a.week}: {len(clips)} clip(s); narration lines to generate: {len(todo)} ({chars} characters)')
    if a.dry_run:
        for c, i in todo: print(f'  {c["id"]} line {i + 1}: {c["segments"][i]["text"]}')
        return

    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool): die(f"{tool} not found on PATH (Windows: winget install ffmpeg, then open a new terminal)")
    if subprocess.run([sys.executable, "-m", "manim", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        die("manim is not installed for this Python (pip install manim)")

    key = api_key() if todo else None
    if todo and not key: die("no ElevenLabs API key. Run tools/save_api_key.bat (Windows) or set ELEVENLABS_API_KEY.")

    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.join(ROOT, "lectures", "_shared") + os.pathsep + env.get("PYTHONPATH", "")
    env["PYTHONIOENCODING"] = "utf-8"
    env.pop("NARRATION_AUDIO", None)
    results = []
    with tempfile.TemporaryDirectory(prefix="clips_") as tmp:
        for c in clips:
            scene_file = os.path.join(wdir, c["scene_file"]); print(f'- {c["id"]} ({c["scene"]})')
            if do_silent:
                v = render(scene_file, c["scene"], a.quality, os.path.join(tmp, c["id"] + "_s"), tmp, env)
                out = os.path.join(wdir, "clips", "silent", c["output"] + ".mp4")
                encode(["-i", v, "-an"], out); results.append(out); print(f"    silent   {duration(out):6.1f} s")
            if do_narr:
                adir = os.path.join(tmp, c["id"] + "_audio"); os.makedirs(adir)
                segs = c["segments"]
                for i, s in enumerate(segs):
                    dst = os.path.join(adir, f'{c["id"]}_s{i + 1:02d}.mp3')
                    if a.no_cache or not os.path.exists(s["_cached"]):
                        audio = tts(s["text"], segs[i - 1]["text"] if i else None, segs[i + 1]["text"] if i < len(segs) - 1 else None, cfg, key)
                        open(dst, "wb").write(audio)
                        if not a.no_cache:
                            os.makedirs(CACHE, exist_ok=True); shutil.copyfile(dst, s["_cached"])
                        print(f"    generated narration line {i + 1}")
                    else:
                        shutil.copyfile(s["_cached"], dst)
                work = os.path.join(tmp, c["id"] + "_n"); os.makedirs(work)
                v = render(scene_file, c["scene"], a.quality, os.path.join(work, "media"), work, dict(env, NARRATION_AUDIO=adir))
                marks = json.load(open(os.path.join(work, f'marks_{c["id"]}.json')))["segments"]
                if len(marks) != len(segs): die(f'{c["id"]}: {len(segs)} narration lines but the scene shows {len(marks)} captions')
                dur = duration(v); ins, filt = ["-i", v], []
                for i, m in enumerate(marks):
                    ins += ["-i", os.path.join(adir, m["file"])]; ms = int(round(m["start"] * 1000))
                    filt.append(f"[{i + 1}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]")
                filt.append("".join(f"[a{i}]" for i in range(len(marks))) + f"amix=inputs={len(marks)}:normalize=0:dropout_transition=0,apad=whole_dur={dur:.3f}[mix]")
                out = os.path.join(wdir, "clips", "narrated", c["output"] + "-narrated.mp4")
                encode([*ins, "-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[mix]", "-c:a", "aac", "-b:a", "160k", "-t", f"{dur:.3f}"], out)
                results.append(out); print(f"    narrated {duration(out):6.1f} s")
    if cfg.get("copy_clips_to"):
        m = re.fullmatch(r"week(\d+)", a.week)
        dest = os.path.join(cfg["copy_clips_to"], f"Week {int(m.group(1)):02d}" if m else a.week, "clips")
        for f in results:
            d = os.path.join(dest, os.path.basename(os.path.dirname(f))); os.makedirs(d, exist_ok=True); shutil.copy2(f, d)
        print("copied to", dest)
    print(f"done: {len(results)} video(s) in {os.path.join(wdir, 'clips')}")


if __name__ == "__main__":
    main()
