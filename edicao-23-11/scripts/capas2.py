# Capas no padrão aprovado: foto real + caixa branca com texto escuro em Lora, dentro do recorte 3:4 da grade.
# Capas da semana de 02/12. Uso: python3 capas2.py pasta_brutos pasta_fotos pasta_saida   (rodar dentro da pasta work, com fonts/ e base_*/)
import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
RAW, FOT, OUT = sys.argv[1:4]
TM = ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
      "zscale=t=bt709:m=bt709:r=tv,format=rgb24,scale=1080:1920")
def grade(rgb):
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[..., 0] = (lab[..., 0] - 143.8) * 1.12 + 128; lab[..., 1] = (lab[..., 1] - 128) * 0.92 + 126; lab[..., 2] += 8
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
def frame(path, t, hdr=True):
    vf = TM if hdr else "format=rgb24,scale=1080:1920"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-vf", vf, "-frames:v", "1", "-f", "rawvideo", "-"], capture_output=True).stdout
    rgb = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3)
    return Image.fromarray(grade(rgb) if hdr else rgb)
def photo(name):
    im = Image.open(f"{FOT}/{name}").convert("RGB"); r = max(1080 / im.width, 1920 / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - 1080) // 2, (im.height - 1920) // 2; return im.crop((x, y, x + 1080, y + 1920))
f = ImageFont.truetype("fonts/lora-latin-600-normal.ttf", 86)
def capa(bg, lines, out, y=1180):
    im = bg.convert("RGB"); d = ImageDraw.Draw(im); asc = f.getbbox("ÁgÇ"); lh = asc[3] - asc[1]
    w = int(max(f.getlength(l) for l in lines)) + 96; h = len(lines) * (lh + 20) + 56; x = (1080 - w) // 2
    d.rectangle((x, y, x + w, y + h), fill="white"); yy = y + 28
    for l in lines: d.text(((1080 - f.getlength(l)) // 2, yy - asc[1]), l, font=f, fill=(26, 33, 70)); yy += lh + 20
    im.save(out, quality=94)
J = [("2026-12-02 Psicologa chora", frame("../extra/B.mov", 12.5, False), ["Psicóloga chora", "com o paciente?"]),
     ("2026-12-03 Quem cuida de voce", photo("foto_1.jpg"), ["Quem cuida", "de você?"]),
     ("2026-12-04 Preguica ou sobrecarga", frame(f"{RAW}/IMG_8083.MOV", 9.0), ["Preguiça ou", "sobrecarga?"]),
     ("2026-12-05 Frases da infancia", frame(f"{RAW}/IMG_7859.MOV", 1.0), ["Que frase ainda", "mora em você?"]),
     ("2026-12-06 Domingo a noite", photo("foto_41.jpg"), ["Seu domingo à", "noite é assim?"])]
for name, bg, lines in J: capa(bg, lines, f"{OUT}/Capa {name}.jpg")
print(len(J))
