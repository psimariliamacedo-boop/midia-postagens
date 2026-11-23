# Monta base.mp4 (1080x1920, 30 fps, cor aprovada) e base.wav (som original, só ganho) a partir de cortes.
# Uso: python3 build_base.py config.json pasta_brutos pasta_saida
import json, subprocess, sys, re, os
cfg = json.load(open(sys.argv[1])); RAW = sys.argv[2]; OUT = sys.argv[3]
os.makedirs(OUT, exist_ok=True)
TONE = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,fps=30")
parts = []
for i, s in enumerate(cfg["segs"]):
    src = f"{RAW}/IMG_{s['file']}.MOV"; d = s["out"] - s["in"]
    v = f"{OUT}/v{i}.mp4"; a = f"{OUT}/a{i}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-i", src, "-t", f"{d:.3f}",
                    "-vf", TONE, "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", v], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['in']:.3f}", "-i", src, "-t", f"{d:.3f}", "-vn",
                    "-af", f"afade=t=in:d=0.012,afade=t=out:st={d-0.012:.3f}:d=0.012", "-ar", "48000", "-ac", "2", a], check=True)
    parts.append((v, a))
with open(f"{OUT}/lv.txt", "w") as f: f.write("".join(f"file '{os.path.abspath(v)}'\n" for v, _ in parts))
with open(f"{OUT}/la.txt", "w") as f: f.write("".join(f"file '{os.path.abspath(a)}'\n" for _, a in parts))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/lv.txt", "-c", "copy", f"{OUT}/base.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{OUT}/la.txt", f"{OUT}/raw.wav"], check=True)
# ganho linear até pico de -1,2 dB (sem filtro, EQ ou compressor)
r = subprocess.run(["ffmpeg", "-i", f"{OUT}/raw.wav", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
peak = float(re.search(r"max_volume: (-?[0-9.]+) dB", r).group(1)); g = -1.2 - peak
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT}/raw.wav", "-af", f"volume={g:.2f}dB", f"{OUT}/base.wav"], check=True)
print(f"base ok, ganho {g:+.1f} dB")
