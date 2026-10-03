#!/usr/bin/env python3
"""
ClipForge renderer - turns images + per-scene voiceovers into a vertical 1080x1920 Short.
100% free: only needs ffmpeg + python3 (no paid render API).

Usage (called by n8n "Execute Command" nodes):
  python3 render.py sheet  <runId>   -> builds sheet.jpg (storyboard contact sheet)
  python3 render.py render <runId>   -> builds final.mp4

Folder layout (created by n8n):
  /data/clipforge/runs/<runId>/scenes.json   (written by n8n)
  /data/clipforge/runs/<runId>/img_1.jpg ... (Pollinations images)
  /data/clipforge/runs/<runId>/audio_1.mp3 ..(ElevenLabs voiceovers)
Optional: /data/clipforge/assets/music.mp3  -> looped background music, auto-ducked under the voice.
"""
import json, os, subprocess, sys, math

ROOT = os.environ.get("CLIPFORGE_DIR", "/data/clipforge")
W, H, FPS, PAD = 1080, 1920, 30, 0.25


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"ffmpeg failed: {' '.join(cmd[:6])} ...")
    return r.stdout


def duration(path):
    out = sh(["ffprobe", "-v", "error", "-show_entries", "format=duration",
              "-of", "default=nw=1:nk=1", path])
    return float(out.strip())


def ass_time(t):
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def esc(txt):
    return txt.replace("\\", "").replace("{", "(").replace("}", ")").replace("\n", " ")


def make_sheet(run):
    n = len([f for f in os.listdir(run) if f.startswith("img_") and f.endswith(".jpg")])
    cols = 5
    rows = max(1, math.ceil(n / cols))
    sh(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-start_number", "1",
        "-i", os.path.join(run, "img_%d.jpg"),
        "-vf", f"scale=216:384:force_original_aspect_ratio=increase,crop=216:384,tile={cols}x{rows}:padding=6:color=black",
        "-frames:v", "1", os.path.join(run, "sheet.jpg")])
    print(f"sheet.jpg ok ({n} frames)")


def make_clip(run, i, dur):
    frames = max(1, int(round(dur * FPS)))
    inc = 0.22 / frames  # total zoom travel ~22% regardless of clip length
    if i % 2 == 1:   # zoom in
        z = f"min(zoom+{inc:.6f},1.22)"
    else:            # zoom out
        z = f"if(eq(on,1),1.22,max(zoom-{inc:.6f},1.0))"
    vf = (f"[0:v]scale={int(W*1.5)}:{int(H*1.5)}:force_original_aspect_ratio=increase,"
          f"crop={int(W*1.5)}:{int(H*1.5)},"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p[v];[1:a]apad=pad_dur={PAD}[a]")
    out = os.path.join(run, f"clip_{i}.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error",
        "-i", os.path.join(run, f"img_{i}.jpg"), "-i", os.path.join(run, f"audio_{i}.mp3"),
        "-filter_complex", vf, "-map", "[v]", "-map", "[a]", "-t", f"{dur:.3f}",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
        "-c:a", "aac", "-ar", "44100", "-ac", "2", out])
    return out


def build_ass(scenes, durs, voiced, path):
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,DejaVu Sans,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,7,2,2,60,60,430,1
Style: Kw,DejaVu Sans,64,&H0000D7FF,&H0000D7FF,&H00000000,&H64000000,-1,0,0,0,100,100,2,0,1,6,2,8,60,60,230,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    lines, t0 = [], 0.0
    for sc, dur, vo in zip(scenes, durs, voiced):
        kw = esc(str(sc.get("keyword", ""))).upper()
        if kw:
            lines.append(f"Dialogue: 1,{ass_time(t0)},{ass_time(t0 + min(1.6, dur))},Kw,,0,0,0,,{{\\fad(150,200)}}{kw}")
        words = esc(str(sc.get("narration", ""))).split()
        if words:
            weights = [len(w) + 2 for w in words]
            total, t = sum(weights), t0
            starts = []
            for w in weights:
                starts.append(t)
                t += vo * w / total
            ends = starts[1:] + [t0 + vo]
            for ci in range(0, len(words), 3):  # show 3 words at a time, highlight the spoken one
                chunk = list(range(ci, min(ci + 3, len(words))))
                for cur in chunk:
                    txt = " ".join(
                        ("{\\c&H0000D7FF&}" + words[k] + "{\\c&H00FFFFFF&}") if k == cur else words[k]
                        for k in chunk)
                    lines.append(f"Dialogue: 0,{ass_time(starts[cur])},{ass_time(ends[cur])},Cap,,0,0,0,,{txt}")
        t0 += dur
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "\n".join(lines) + "\n")


def render(run):
    data = json.load(open(os.path.join(run, "scenes.json"), encoding="utf-8"))
    scenes = data["scenes"] if isinstance(data, dict) else data
    clips, durs, voiced = [], [], []
    for i, sc in enumerate(scenes, start=1):
        a = duration(os.path.join(run, f"audio_{i}.mp3"))
        voiced.append(a)
        clip = make_clip(run, i, a + PAD)
        durs.append(duration(clip))
        clips.append(clip)
    lst = os.path.join(run, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{c}'\n" for c in clips)
    concat = os.path.join(run, "concat.mp4")
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", concat])
    ass = os.path.join(run, "captions.ass")
    build_ass(scenes, durs, voiced, ass)
    out = os.path.join(run, "final.mp4")
    music = os.path.join(ROOT, "assets", "music.mp3")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", concat]
    if os.path.exists(music):
        cmd += ["-stream_loop", "-1", "-i", music, "-filter_complex",
                f"[0:v]ass={ass}[v];[0:a]asplit=2[vo][sc];[1:a]volume=0.5[m];"
                "[m][sc]sidechaincompress=threshold=0.04:ratio=10:attack=20:release=500[duck];"
                "[vo][duck]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "[v]", "-map", "[a]", "-shortest"]
    else:
        cmd += ["-vf", f"ass={ass}", "-map", "0:v", "-map", "0:a"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    sh(cmd)
    for c in clips:
        os.remove(c)
    print(f"final.mp4 ok ({sum(durs):.1f}s, {os.path.getsize(out)/1e6:.1f} MB)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("sheet", "render"):
        raise SystemExit("usage: render.py sheet|render <runId>")
    run_dir = os.path.join(ROOT, "runs", sys.argv[2])
    make_sheet(run_dir) if sys.argv[1] == "sheet" else render(run_dir)
