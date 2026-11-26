# Artes da manhã 26/11 a 02/12 com as fotos dela. Uso: python3 -I stories_manha.py WORKDIR
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
W = sys.argv[1]; FN = f"{W}/fonts"; NAVY = (26, 33, 70); GOLD = (244, 184, 96)
FL = ImageFont.truetype(f"{FN}/lora-latin-600-normal.woff", 74); FS = ImageFont.truetype(f"{FN}/dm-sans-latin-700-normal.woff", 44)
def wrap(f, txt, w):
    L, cur = [], ""
    for x in txt.split():
        t = (cur + " " + x).strip()
        if f.getlength(t) > w and cur: L.append(cur); cur = x
        else: cur = t
    return L + [cur]
def story(src, txt, sub, out, y, cx=0.5):
    im = ImageOps.fit(ImageOps.exif_transpose(Image.open(f"{W}/pessoais_editadas/{src}")).convert("RGB"), (1080, 1920), centering=(cx, 0.5), method=Image.LANCZOS)
    d = ImageDraw.Draw(im); L = wrap(FL, txt, 820); asc = FL.getbbox("ÁgÇ"); lh = asc[3] - asc[1] + 18
    w = int(max(FL.getlength(l) for l in L)) + 100; h = len(L) * lh + 60; x = (1080 - w) // 2
    d.rectangle((x, y, x + w, y + h), fill="white"); yy = y + 30
    for l in L: d.text(((1080 - FL.getlength(l)) // 2, yy - asc[1]), l, font=FL, fill=NAVY); yy += lh
    if sub:
        sw = int(FS.getlength(sub)) + 60; sb = FS.getbbox(sub); sx = (1080 - sw) // 2; sy = y + h + 24
        d.rounded_rectangle((sx, sy, sx + sw, sy + (sb[3] - sb[1]) + 40), 18, fill=NAVY)
        d.text((sx + 30, sy + 20 - sb[1]), sub, font=FS, fill=GOLD)
    im.save(f"{W}/out/{out}", quality=92)
J = [("carro-chuva.jpg", "Spoiler: ninguém tira nota.", "Hoje às 19h eu explico", "2026-11-26 manha", 1180),
     ("retrato-cortina.jpg", "Sexta de sala aberta.", "Às 17h: como é a primeira sessão", "2026-11-27 manha", 1180, 0.55),
     ("escada.jpg", "Segunda pela escada.", "Hoje às 18h", "2026-11-30 manha", 250),
     ("cafe-copinho.jpg", "Primeiro café de dezembro.", "Às 20h: a primeira sessão aqui", "2026-12-01 manha", 1120),
     ("selfie-parede.jpg", "Quarta, cara lavada e sorriso.", "Às 20h eu respondo a caixinha", "2026-12-02 manha", 1230)]
for src, t, s, n, y, *c in J: story(src, t, s, f"Story {n}.jpg", y, *c)
