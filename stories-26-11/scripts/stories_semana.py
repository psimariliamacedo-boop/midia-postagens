# Artes de stories 26/11 a 02/12/2026 (padrão skill stories-marilia). Uso: python3 -I stories_semana.py WORKDIR
import sys, os
from PIL import Image, ImageDraw, ImageFont
W = sys.argv[1]; FOT = f"{W}/fotos"; OUT = f"{W}/out"; FN = f"{W}/fonts"
NAVY = (26, 33, 70); GOLD = (244, 184, 96)
FL = ImageFont.truetype(f"{FN}/lora-latin-600-normal.woff", 74); FS = ImageFont.truetype(f"{FN}/dm-sans-latin-700-normal.woff", 44)
def wrap(f, txt, w):
    L, cur = [], ""
    for x in txt.split():
        t = (cur + " " + x).strip()
        if f.getlength(t) > w and cur: L.append(cur); cur = x
        else: cur = t
    return L + [cur]
def story(bg, txt, sub, out, y=330):
    im = Image.open(f"{FOT}/{bg}").convert("RGB").resize((1080, 1920)); d = ImageDraw.Draw(im)
    L = wrap(FL, txt, 820); asc = FL.getbbox("ÁgÇ"); lh = asc[3] - asc[1] + 18
    w = int(max(FL.getlength(l) for l in L)) + 100; h = len(L) * lh + 60; x = (1080 - w) // 2
    d.rectangle((x, y, x + w, y + h), fill="white"); yy = y + 30
    for l in L: d.text(((1080 - FL.getlength(l)) // 2, yy - asc[1]), l, font=FL, fill=NAVY); yy += lh
    if sub:
        sw = int(FS.getlength(sub)) + 60; sb = FS.getbbox(sub); sx = (1080 - sw) // 2; sy = y + h + 24
        d.rounded_rectangle((sx, sy, sx + sw, sy + (sb[3] - sb[1]) + 40), 18, fill=NAVY)
        d.text((sx + 30, sy + 20 - sb[1]), sub, font=FS, fill=GOLD)
    im.save(f"{OUT}/{out}", quality=92)
def pausa(out):
    im = Image.new("RGB", (1080, 1920), NAVY); d = ImageDraw.Draw(im)
    big = ImageFont.truetype(f"{FN}/lora-latin-700-normal.woff", 150); mid = ImageFont.truetype(f"{FN}/dm-sans-latin-700-normal.woff", 58)
    sm = ImageFont.truetype(f"{FN}/dm-sans-latin-500-normal.woff", 42)
    for t, f, c, y in [("Checklist gratuito", mid, (255, 255, 255), 640), ("da pausa", mid, (255, 255, 255), 720), ("PAUSA", big, GOLD, 860),
                       ("Manda essa palavra no meu direct", sm, (255, 255, 255), 1080), ("que eu te envio.", sm, (255, 255, 255), 1140),
                       ("Marília Macêdo · Psicóloga · CRP 06/229488", sm, (200, 200, 215), 1560)]:
        d.text(((1080 - f.getlength(t)) // 2, y), t, font=f, fill=c)
    im.save(f"{OUT}/{out}", quality=92)
J = [("2026-11-26 tarde CAIXINHA", "prateleira.jpg", "Qual a sua dúvida sobre a avaliação de TDAH?", "Hoje às 19h"),
     ("2026-11-27 tarde ENQUETE", "poltrona-acolhimento.jpg", "Você já fez terapia?", "Hoje às 17h"),
     ("2026-11-28 tarde ENQUETE", "sala-inteira.jpg", "Você está recomeçando alguma coisa?", "Hoje às 19h"),
     ("2026-11-29 tarde ENQUETE", "poltrona-janela.jpg", "Seu domingo está sendo de descanso?", "Hoje às 18h"),
     ("2026-11-30 tarde CAIXINHA", "sala-mesinhas.jpg", "O que você mais esquece no dia a dia?", "Hoje às 18h"),
     ("2026-12-01 tarde ENQUETE", "cantinho-cafe.jpg", "Café ou água?", "Hoje às 20h"),
     ("2026-12-02 tarde CAIXINHA", "poltrona-acolhimento.jpg", "Qual a sua maior curiosidade sobre terapia?", "Hoje às 20h")]
for n, bg, t, s in J: story(bg, t, s, f"Story {n}.jpg")
pausa("Story 2026-11-29 noite PAUSA.jpg")
