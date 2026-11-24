# Vídeo da sala (Google Meu Negócio / apresentação): cenas reais + textos curtos + cartão final.
# Uso: python3 sala.py pasta_brutos pasta_fotos saida.mp4 [narracao.m4a]
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
RAW, FOT, OUT = sys.argv[1:4]; NARR = sys.argv[4] if len(sys.argv) > 4 else None
W, H, FPS = 1080, 1920, 30
FD = sys.path[0] + "/../../edicao-23-11/scripts/fonts/"
FD = "fonts/"
NAVY = (26, 33, 70); GOLD = (244, 184, 96)
def F(n, s): return ImageFont.truetype(FD + n, s)
DM = "dm-sans-latin-500-normal.ttf"; DMB = "dm-sans-latin-700-normal.ttf"
TONE = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920,fps=30")
def grade(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = (lab[..., 0] - 143.8) * 1.12 + 128
    lab[..., 1] = (lab[..., 1] - 128) * 0.92 + 126
    lab[..., 2] = lab[..., 2] + 8
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
# (tipo, fonte, início, duração, texto, zoom inicial, zoom final)
SHOTS = [
    ("v", "IMG_7865.MOV", 0.5, 2.5, "Cosmópolis · Bela Vista IV", 1.0, 1.0),
    ("v", "IMG_7859.MOV", 0.2, 3.0, "Consultório novo", 1.0, 1.0),
    ("v", "IMG_7861.MOV", 0.5, 6.0, "Um lugar pensado para você parar", 1.0, 1.0),
    ("f", "foto_42.jpg", 0, 2.5, "Sem pressa. No seu tempo.", 1.0, 1.06),
    ("f", "foto_41.jpg", 0, 2.0, None, 1.05, 1.0),
    ("v", "IMG_7856.MOV", 0.3, 2.7, "Um cafezinho te esperando", 1.0, 1.0),
    ("f", "foto_13.jpg", 0, 2.0, None, 1.0, 1.06),
    ("f", "foto_8.jpg", 0, 2.5, "Atendimento infantil e adulto", 1.06, 1.0),
    ("v", "IMG_8081.MOV", 0.3, 3.0, "Rua Santa Gertrudes, 1230", 1.0, 1.0),
]
import os
END = {"sorriso": ("v", "IMG_8081.MOV", 0.3, 3.0, "Rua Santa Gertrudes, 1230", 1.0, 1.0),
       "cafe": ("f", "foto_1.jpg", 0, 3.0, "Rua Santa Gertrudes, 1230", 1.0, 1.05),
       "sala": ("f", "foto_17.jpg", 0, 3.0, "Rua Santa Gertrudes, 1230", 1.06, 1.0)}
if os.environ.get("FINAL") in END: SHOTS[-1] = END[os.environ["FINAL"]]
CARD = int(2.0 * FPS)
def caption(txt):
    f = F(DMB, 50); b = f.getbbox(txt); w = b[2] - b[0]; h = b[3] - b[1]; px, py = 40, 26
    im = Image.new("RGBA", (w + 2 * px, h + 2 * py), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, im.width - 1, im.height - 1), 20, fill=NAVY + (240,))
    d.text((px - b[0], py - b[1]), txt, font=f, fill="white"); return im
def paste(fr, img, x, y):
    a = np.asarray(img).astype(np.float32); h, w = a.shape[:2]
    sub = fr[y:y + h, x:x + w].astype(np.float32); al = a[..., 3:4] / 255.
    fr[y:y + h, x:x + w] = (sub * (1 - al) + a[..., :3] * al).astype(np.uint8)
def photo_frames(path, n, z0, z1):
    im = Image.open(path).convert("RGB"); r = max(W / im.width, H / im.height)
    base = im.resize((int(im.width * r * 1.08) + 2, int(im.height * r * 1.08) + 2), Image.LANCZOS)
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1); cw, ch = W * 1.08 / z, H * 1.08 / z
        cx, cy = base.width / 2, base.height / 2
        crop = base.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2)))
        yield np.asarray(crop.resize((W, H), Image.BILINEAR))
def video_frames(name, ss, n):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", f"{RAW}/{name}", "-frames:v", str(n), "-vf", TONE,
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    last = None
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        last = grade(np.frombuffer(b, np.uint8).reshape(H, W, 3)); yield last
    p.stdout.close(); p.wait()
tot = sum(int(s[3] * FPS) for s in SHOTS) + CARD
audio = ["-f", "lavfi", "-t", f"{tot / FPS:.3f}", "-i", "anullsrc=r=48000:cl=stereo"] if not NARR else ["-i", NARR]
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        *audio, "-map", "0:v", "-map", "1:a", "-t", f"{tot / FPS:.3f}", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
prev = None; last = None; k = 0
for kind, src, ss, dur, txt, z0, z1 in SHOTS:
    n = int(dur * FPS)
    gen = photo_frames(f"{FOT}/{src}", n, z0, z1) if kind == "f" else video_frames(src, ss, n)
    cap = caption(txt) if txt else None
    for i, fr in enumerate(gen):
        fr = fr.copy()
        if prev is not None and i < 8: a = (i + 1) / 9; fr = (fr * a + prev * (1 - a)).astype(np.uint8)
        if cap is not None and i >= 6:
            al = min(1, (i - 6) / 6); c = cap.copy(); c.putalpha(c.split()[3].point(lambda v: int(v * al)))
            paste(fr, c, (W - cap.width) // 2, 1500)
        enc.stdin.write(fr.tobytes()); last = fr; k += 1
    prev = last.astype(np.float32)
# cartão final
im = Image.fromarray(last).filter(ImageFilter.GaussianBlur(22)); a = np.asarray(im).astype(np.float32) * 0.45 + np.array(NAVY) * 0.35
card = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(card); y = 720
for t, f, c in [("Marília Macêdo", F(DMB, 64), (255, 255, 255)), ("Psicóloga · Neuropsicóloga", F(DM, 40), (255, 255, 255)),
                ("Presencial em Cosmópolis", F(DMB, 46), GOLD), ("Online para todo o Brasil", F(DMB, 46), GOLD),
                ("Rua Santa Gertrudes, 1230 · Bela Vista IV", F(DM, 36), (255, 255, 255)),
                ("CRP 06/229488 · @mariliamacedo.psi", F(DM, 34), (255, 255, 255))]:
    b = f.getbbox(t); d.text(((W - (b[2] - b[0])) // 2, y), t, font=f, fill=c); y += f.size + 34
cd = np.asarray(card)
for i in range(CARD):
    a = min(1, (i + 1) / 9); enc.stdin.write((cd * a + last * (1 - a)).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print("done", OUT, f"{tot / FPS:.1f}s")
