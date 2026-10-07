import json, subprocess, sys
names = {1: "week01-clip1-tokenization-and-embeddings", 2: "week01-clip2-query-key-value-attention", 3: "week01-clip3-encoder-block", 4: "week01-clip4-encoder-vs-decoder-and-masking"}
for k, name in names.items():
    m = json.load(open(f"marks_clip{k}.json"))["segments"]
    vid = f"media_n/videos/c{k}/1080p30/C{k}.mp4"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", vid]).decode())
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", vid]
    filt = []
    for i, s in enumerate(m):
        cmd += ["-i", "audio/" + s["file"]]
        ms = int(round(s["start"] * 1000))
        filt.append(f"[{i+1}:a]aresample=44100,aformat=channel_layouts=stereo,adelay={ms}|{ms}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(m))) + f"amix=inputs={len(m)}:normalize=0:dropout_transition=0,apad=whole_dur={dur:.3f}[mix]")
    out = f"out_n/{name}-narrated.mp4"
    cmd += ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[mix]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", "-t", f"{dur:.3f}", "-movflags", "+faststart", out]
    subprocess.check_call(cmd)
    # check: last narration ends before the video does, and segments do not overlap
    ends = []
    for s in m:
        d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "audio/" + s["file"]]).decode())
        ends.append(s["start"] + d)
    overlap = [round(ends[i] - m[i + 1]["start"], 2) for i in range(len(m) - 1) if ends[i] > m[i + 1]["start"]]
    print(name, f"video {dur:.1f}s, last narration ends {ends[-1]:.1f}s, overlaps {overlap}")
