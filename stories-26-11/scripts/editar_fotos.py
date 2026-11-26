# Edição das fotos pessoais (JPEG do iPhone): exposição automática, pele uniforme, brilho quente, nitidez.
# Uso: python3 -I editar_fotos.py PASTA_ENTRADA PASTA_SAIDA
import sys, os, glob, numpy as np, cv2
from PIL import Image, ImageOps
IN, OUT = sys.argv[1:3]; os.makedirs(OUT, exist_ok=True)
def edit(rgb):
    u8 = rgb.copy()
    lab = cv2.cvtColor(u8, cv2.COLOR_RGB2LAB).astype(np.float32); L = lab[..., 0] / 255
    g = np.clip(np.log(0.56) / np.log(max(np.median(L), 0.05)), 0.7, 1.1)    # leva o meio-tom para ~56%
    L = L ** g
    L = L + 0.10 * (1 - L) ** 3                                              # abre sombras (rosto)
    L = 0.5 + (L - 0.5) * 1.05
    lab[..., 0] = np.clip(L * 255, 0, 255)
    lab[..., 1] = (lab[..., 1] - 128) * 0.95 + 128.5                         # pele menos avermelhada
    lab[..., 2] = (lab[..., 2] - 128) * 1.05 + 133                           # tom mais quente
    u8 = cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    # pele: separação de frequências (suaviza manchas, mantém textura fina)
    f = u8.astype(np.float32); low = cv2.bilateralFilter(u8, 15, 35, 15).astype(np.float32)
    detail = f - cv2.GaussianBlur(f, (0, 0), 1.2)
    f = 0.55 * f + 0.45 * (low + detail * 0.8)
    # brilho suave (glow) nas luzes
    glow = cv2.GaussianBlur(f, (0, 0), 25); f = 255 - (255 - f) * (255 - glow * 0.18) / 255
    u8 = np.clip(f, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV).astype(np.float32); s = hsv[..., 1] / 255
    hsv[..., 1] = np.clip((s + 0.12 * s * (1 - s)) * 255, 0, 255)
    u8 = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2RGB)
    return cv2.addWeighted(u8, 1.35, cv2.GaussianBlur(u8, (0, 0), 1.4), -0.35, 0)
for p in sorted(glob.glob(f"{IN}/*.jpg")):
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    Image.fromarray(edit(np.asarray(im))).save(f"{OUT}/{os.path.basename(p)}", quality=95)
