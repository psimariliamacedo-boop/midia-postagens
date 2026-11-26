# Artes de stories (1080x1920): foto/quadro real + frase em caixa branca (Lora) + linha de apoio opcional.
# Uso: python3 stories.py pasta_brutos pasta_fotos pasta_saida   (rodar dentro da pasta work, com fonts/)
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
RAW, FOT, OUT = sys.argv[1:4]
NAVY = (26, 33, 70); GOLD = (244, 184, 96)
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=rgb24,scale=1080:1920")
def grade(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = (lab[..., 0] - 143.8) * 1.12 + 128; lab[..., 1] = (lab[..., 1] - 128) * 0.92 + 126; lab[..., 2] += 8
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
def frame(name, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f"{RAW}/{name}", "-vf", TM, "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True).stdout
    return Image.fromarray(grade(np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)))
def photo(name): return Image.open(f"{FOT}/{name}").convert("RGB").resize((1080, 1920))
FL = ImageFont.truetype("fonts/lora-latin-600-normal.ttf", 74); FS = ImageFont.truetype("fonts/dm-sans-latin-700-normal.ttf", 44)
def wrap(f, txt, w):
    L, cur = [], ""
    for x in txt.split():
        t = (cur + " " + x).strip()
        if f.getlength(t) > w and cur: L.append(cur); cur = x
        else: cur = t
    return L + [cur]
def story(bg, txt, sub, out, y=330):
    im = bg.copy(); d = ImageDraw.Draw(im); L = wrap(FL, txt, 820); asc = FL.getbbox("ÁgÇ"); lh = asc[3] - asc[1] + 18
    w = int(max(FL.getlength(l) for l in L)) + 100; h = len(L) * lh + 60; x = (1080 - w) // 2
    d.rectangle((x, y, x + w, y + h), fill="white"); yy = y + 30
    for l in L: d.text(((1080 - FL.getlength(l)) // 2, yy - asc[1]), l, font=FL, fill=NAVY); yy += lh
    if sub:
        sw = int(FS.getlength(sub)) + 60; sb = FS.getbbox(sub); sx = (1080 - sw) // 2; sy = y + h + 24
        d.rounded_rectangle((sx, sy, sx + sw, sy + (sb[3] - sb[1]) + 40), 18, fill=NAVY)
        d.text((sx + 30, sy + 20 - sb[1]), sub, font=FS, fill=GOLD)
    im.save(out, quality=92)
def pausa(out):
    im = Image.new("RGB", (1080, 1920), NAVY); d = ImageDraw.Draw(im)
    big = ImageFont.truetype("fonts/lora-latin-700-normal.ttf", 150); mid = ImageFont.truetype("fonts/dm-sans-latin-700-normal.ttf", 58)
    sm = ImageFont.truetype("fonts/dm-sans-latin-500-normal.ttf", 42)
    for t, f, c, y in [("Checklist gratuito", mid, (255, 255, 255), 640), ("da pausa", mid, (255, 255, 255), 720), ("PAUSA", big, GOLD, 860),
                       ("Manda essa palavra no meu direct", sm, (255, 255, 255), 1080), ("que eu te envio.", sm, (255, 255, 255), 1140),
                       ("Marília Macêdo · Psicóloga · CRP 06/229488", sm, (200, 200, 215), 1560)]:
        d.text(((1080 - f.getlength(t)) // 2, y), t, font=f, fill=c)
    im.save(out, quality=92)
J = [("2026-11-26 manha", photo("destaque-sala_prateleira.jpg"), "Avaliação neuropsicológica não é prova.", "Hoje às 19h eu te explico"),
     ("2026-11-26 tarde CAIXINHA", frame("IMG_8081.MOV", 1.6), "Qual a sua dúvida sobre avaliação de TDAH?", None, 1180),
     ("2026-11-27 manha", photo("destaque-sala_poltrona-acolhimento.jpg"), "É aqui que a sua história começa a ser ouvida.", "Hoje às 17h: medo da primeira sessão?"),
     ("2026-11-27 tarde ENQUETE", photo("destaque-sala_poltrona-janela.jpg"), "Você já fez terapia?", None),
     ("2026-11-28 manha", frame("IMG_6231.MOV", 3.0), "Em outubro, essa sala era assim.", "Hoje às 19h: o depois"),
     ("2026-11-28 tarde ENQUETE", photo("destaque-sala_sala-inteira.jpg"), "Você está recomeçando alguma coisa?", None),
     ("2026-11-29 manha", photo("destaque-sala_cantinho-cafe.jpg"), "Domingo também é dia de não resolver nada.", None),
     ("2026-11-29 tarde ENQUETE", frame("IMG_7912.MOV", 0.8), "Seu domingo foi de descanso?", None),
     ("2026-11-30 manha", photo("destaque-sala_canto-terracota.jpg"), "Esquecida? Desorganizada? Nem sempre é falta de esforço.", "Hoje às 18h"),
     ("2026-11-30 tarde CAIXINHA", photo("destaque-sala_sala-mesinhas.jpg"), "O que você mais esquece no dia a dia?", None)]
for n, bg, t, s, *y in J: story(bg, t, s, f"{OUT}/Story {n}.jpg", *y)
pausa(f"{OUT}/Story 2026-11-29 noite PAUSA.jpg")
print(len(J) + 1)
