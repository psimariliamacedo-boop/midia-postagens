# Story "Meta x Realidade" da balinha (IMG_7855, 60 fps) em câmera lenta 0,6x, com 2º texto entrando na hora da balinha na mão.
# Uso: python3 -I story_balinha.py WORKDIR VIDEO   (usa overlay/grade de stories_video.py)
import sys, subprocess, numpy as np
sys.argv = [sys.argv[0], sys.argv[1], "/dev/null", sys.argv[2]]
W, _, SRC = sys.argv[1:4]
src = open(__file__.replace("story_balinha.py", "stories_video.py")).read().split("video(\"4a30")[0]
exec(src)
from PIL import Image, ImageDraw
def caixa(txt, y):
    oc, oa = overlay(txt, None, y); return oc, oa
m_c, m_a = caixa("Meta: comprar balinha gostosa pros pacientes.", 300)
r_c, r_a = caixa("Realidade: eu comendo todas.", 640)
SLOW = 1 / 0.6; T_REAL = 1.15 * SLOW          # entra quando a balinha já está na mão (1,15 s do original)
vf = TM.replace("fps=30", f"setpts={SLOW}*PTS,fps=30")
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-vf", vf, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                        f"{W}/out/Story 2026-11-27 manha.mp4"], stdin=subprocess.PIPE)
n = 1080 * 1920 * 3; i = 0
while (b := dec.stdout.read(n)) and len(b) == n:
    f = grade(np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)).astype(np.float32)
    f = f * (1 - m_a) + m_c * m_a
    t = i / 30
    if t >= T_REAL:
        k = min(1, (t - T_REAL) / 0.2) * r_a           # entra com fade de 0,2 s
        f = f * (1 - k) + r_c * k
    enc.stdin.write(f.astype(np.uint8).tobytes()); i += 1
enc.stdin.close(); enc.wait(); dec.wait(); print(i / 30, "s")
