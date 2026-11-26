# Stories em vídeo (iPhone HLG -> SDR + ajuste LAB da skill + caixa de texto). Uso: python3 -I stories_video.py WORKDIR UPLOADS
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
W, U = sys.argv[1:3]; FN = f"{W}/fonts"; NAVY = (26, 33, 70); GOLD = (244, 184, 96)
FL = ImageFont.truetype(f"{FN}/lora-latin-600-normal.woff", 74); FS = ImageFont.truetype(f"{FN}/dm-sans-latin-700-normal.woff", 44)
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=rgb24,scale=1080:1920,fps=30")
def wrap(f, txt, w):
    L, cur = [], ""
    for x in txt.split():
        t = (cur + " " + x).strip()
        if f.getlength(t) > w and cur: L.append(cur); cur = x
        else: cur = t
    return L + [cur]
def overlay(txt, sub, y):
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    L = wrap(FL, txt, 820); asc = FL.getbbox("ÁgÇ"); lh = asc[3] - asc[1] + 18
    w = int(max(FL.getlength(l) for l in L)) + 100; h = len(L) * lh + 60; x = (1080 - w) // 2
    d.rectangle((x, y, x + w, y + h), fill="white"); yy = y + 30
    for l in L: d.text(((1080 - FL.getlength(l)) // 2, yy - asc[1]), l, font=FL, fill=NAVY); yy += lh
    if sub:
        sw = int(FS.getlength(sub)) + 60; sb = FS.getbbox(sub); sx = (1080 - sw) // 2; sy = y + h + 24
        d.rounded_rectangle((sx, sy, sx + sw, sy + (sb[3] - sb[1]) + 40), 18, fill=NAVY)
        d.text((sx + 30, sy + 20 - sb[1]), sub, font=FS, fill=GOLD)
    a = np.asarray(im).astype(np.float32); return a[..., :3], a[..., 3:] / 255
def grade(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = (lab[..., 0] - 143.8) * 1.12 + 128; lab[..., 1] = (lab[..., 1] - 128) * 0.92 + 126; lab[..., 2] += 8
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
def video(src, t0, dur, txt, sub, y, out):
    oc, oa = overlay(txt, sub, y)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", f"{U}/{src}", "-vf", TM, "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "19", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{W}/out/{out}"], stdin=subprocess.PIPE)
    n = 1080 * 1920 * 3
    while (b := dec.stdout.read(n)) and len(b) == n:
        f = grade(np.frombuffer(b, np.uint8).reshape(1920, 1080, 3)).astype(np.float32)
        enc.stdin.write((f * (1 - oa) + oc * oa).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
video("4a304090-IMG_7859.mov", 0, 6.5, "Por fora ela já está pronta.", "Às 19h: o antes e depois", 330, "Story 2026-11-28 manha.mp4")
video("e3a09414-IMG_7855.mov", 0, 3.6, "Você já fez terapia?", "Hoje às 17h", 330, "Story 2026-11-27 tarde ENQUETE.mp4")
