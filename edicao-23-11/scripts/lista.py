# Reels sem fala, em formato de lista: cenas reais + título + um item por vez + CTA + cartão final.
# Uso: python3 lista.py config.json pasta_brutos pasta_fotos saida.mp4
import sys, json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
CFG = json.load(open(sys.argv[1])); RAW, FOT, OUT = sys.argv[2:5]
W, H, FPS = 1080, 1920, 30
NAVY = (26, 33, 70); GOLD = (244, 184, 96)
FD = "fonts/"
def F(n, s): return ImageFont.truetype(FD + n, s)
DM = "dm-sans-latin-500-normal.ttf"; DMB = "dm-sans-latin-700-normal.ttf"
TONE = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
        "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,scale=1080:1920")
def grade(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = (lab[..., 0] - 143.8) * 1.12 + 128; lab[..., 1] = (lab[..., 1] - 128) * 0.92 + 126; lab[..., 2] += 8
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
def wrap(txt, f, maxw):
    lines, cur = [], ""
    for w in txt.split():
        t = (cur + " " + w).strip()
        if f.getlength(t) > maxw and cur: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
def box(txt, size, fill, color, maxw=900, num=None):
    f = F(DMB, size); lines = wrap(txt, f, maxw); asc = f.getbbox("ÁgÇ"); lh = asc[3] - asc[1]
    px, py, gap = 46, 30, 14; nw = 0
    if num is not None: fn = F(DMB, int(size * 1.25)); nt = f"{num}"; nw = int(fn.getlength(nt)) + 34
    w = int(max(f.getlength(l) for l in lines)) + 2 * px + nw; h = len(lines) * lh + (len(lines) - 1) * gap + 2 * py
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 26, fill=fill)
    if num is not None:
        bn = fn.getbbox(nt); d.text((px - bn[0], (h - (bn[3] - bn[1])) // 2 - bn[1]), nt, font=fn, fill=GOLD)
    y = py
    for l in lines: d.text((px + nw, y - asc[1]), l, font=f, fill=color); y += lh + gap
    sh = Image.new("RGBA", (w + 60, h + 60), (0, 0, 0, 0)); m = Image.new("RGBA", (w, h), (0, 0, 0, 0)); m.putalpha(im.split()[3].point(lambda v: v * 110 // 255))
    sh.paste(m, (30, 36), m); sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(im, (30, 30)); return sh
def paste(fr, img, x, y, al=1.0):
    a = np.asarray(img).astype(np.float32); h, w = a.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    sub = a[y0 - y:y1 - y, x0 - x:x1 - x]; m = sub[..., 3:4] / 255. * al
    fr[y0:y1, x0:x1] = (fr[y0:y1, x0:x1] * (1 - m) + sub[..., :3] * m).astype(np.uint8)
def photo(path, n, z0, z1):
    im = Image.open(path).convert("RGB"); r = max(W / im.width, H / im.height) * 1.08
    base = im.resize((int(im.width * r) + 2, int(im.height * r) + 2), Image.LANCZOS)
    for i in range(n):
        z = z0 + (z1 - z0) * i / max(1, n - 1); cw, ch = W * 1.08 / z, H * 1.08 / z; cx, cy = base.width / 2, base.height / 2
        yield np.asarray(base.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR))
def video(name, ss, n, speed):
    vf = TONE + (f",setpts={1/speed:.4f}*PTS" if speed != 1 else "") + ",fps=30"
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", f"{RAW}/{name}", "-vf", vf, "-frames:v", str(n),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    for _ in range(n):
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield grade(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    p.kill()
# timeline de texto
TY = CFG.get("text_y", 1180)
ev = []; t = 0.0
ev.append((t, t + CFG["title_dur"], box(CFG["title"], 74, (255, 255, 255, 250), NAVY))); t += CFG["title_dur"]
for k, it in enumerate(CFG["items"]):
    ev.append((t, t + CFG["item_dur"], box(it, 68, NAVY + (245,), (255, 255, 255), num=(k + 1) if CFG.get("numbered", True) else None))); t += CFG["item_dur"]
if CFG.get("end_line"): ev.append((t, t + CFG["end_dur"], box(CFG["end_line"], 70, (255, 255, 255, 250), NAVY))); t += CFG["end_dur"]
ev.append((t, t + CFG["cta_dur"], box(CFG["cta"], 62, NAVY + (245,), GOLD))); t += CFG["cta_dur"]
TOTAL = t; NB = int(TOTAL * FPS); CARD = int(1.8 * FPS)
# fundo
frames = []
def bg():
    for s in CFG["shots"]:
        n = int(s["dur"] * FPS)
        g = photo(f"{FOT}/{s['src']}", n, s.get("z0", 1.0), s.get("z1", 1.06)) if s["src"].endswith(".jpg") else video(s["src"], s.get("ss", 0), n, s.get("speed", 1.0))
        for fr in g: yield fr
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-f", "lavfi", "-t", f"{(NB + CARD) / FPS:.3f}", "-i", "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a",
                        "-t", f"{(NB + CARD) / FPS:.3f}", "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
g = bg(); last = None; prev = None; snaps = []
for i in range(NB):
    try: fr = next(g).copy()
    except StopIteration: fr = last.copy()
    last = fr.copy(); tt = i / FPS
    for a, b, im in ev:
        if a <= tt < b:
            al = min(1, (tt - a) / 0.25, (b - tt) / 0.2); paste(fr, im, (W - im.width) // 2, TY - im.height // 2, max(0, al))
    hd = F("montserrat-latin-700-normal.ttf", 38); dd = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    enc.stdin.write(fr.tobytes())
    if i % int(3 * FPS) == 15: Image.fromarray(fr).save(f"{OUT}.f{i}.jpg", quality=80)
# cartão final
im = Image.fromarray(last).filter(ImageFilter.GaussianBlur(22)); a = np.asarray(im).astype(np.float32) * 0.45 + np.array(NAVY) * 0.35
card = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(card); y = 760
for tx, f, c in [("Me chama no WhatsApp", F(DMB, 60), (255, 255, 255)), ("Presencial em Cosmópolis", F(DMB, 44), GOLD), ("Online para todo o Brasil", F(DMB, 44), GOLD),
                 ("Rua Santa Gertrudes, 1230 · Bela Vista IV", F(DM, 36), (255, 255, 255)), ("Marília Macêdo · Psicóloga · Neuropsicóloga", F(DM, 34), (255, 255, 255)),
                 ("CRP 06/229488 · @mariliamacedo.psi", F(DM, 34), (255, 255, 255))]:
    d.text(((W - f.getlength(tx)) // 2, y), tx, font=f, fill=c); y += f.size + 32
cd = np.asarray(card)
for i in range(CARD): a = min(1, (i + 1) / 9); enc.stdin.write((cd * a + last * (1 - a)).astype(np.uint8).tobytes())
enc.stdin.close(); enc.wait(); print("done", OUT, f"{(NB + CARD) / FPS:.1f}s")
