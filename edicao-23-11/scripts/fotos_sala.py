import sys,numpy as np,cv2,os
from PIL import Image,ImageFilter,ImageEnhance,ImageDraw,ImageFont
SRC,OUT=sys.argv[1],sys.argv[2]
SEL=[("42","sala-inteira",0.55),("43","sala-poltronas",0.45),("17","canto-terracota",0.5),("41","poltrona-acolhimento",0.55),
     ("16","poltrona-janela",0.6),("47","sala-mesinhas",0.55),("14","cafe-de-cima",0.5),("5","cantinho-cafe",0.55),
     ("9","mesinha-infantil",0.5),("11","prateleira",0.5)]
def enhance(im):
    a=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2LAB).astype(np.float32)
    L=a[...,0]; lo,hi=np.percentile(L,0.8),np.percentile(L,99.6)
    a[...,0]=np.clip((L-lo)/(hi-lo)*250+2,0,255)
    clahe=cv2.createCLAHE(clipLimit=1.4,tileGridSize=(8,8))
    a[...,0]=clahe.apply(a[...,0].astype(np.uint8)).astype(np.float32)*0.5+a[...,0]*0.5
    im=Image.fromarray(cv2.cvtColor(np.clip(a,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB))
    im=ImageEnhance.Color(im).enhance(1.06)
    return im.filter(ImageFilter.UnsharpMask(radius=1.6,percent=55,threshold=2))
def crop(im,W,H,c):
    r=max(W/im.width,H/im.height); im2=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    if im2.width>W: x=int((im2.width-W)*c); return im2.crop((x,0,x+W,H))
    y=int((im2.height-H)*c); return im2.crop((0,y,W,y+H))
for n,name,c in SEL:
    im=enhance(Image.open(f"{SRC}/foto_{n}.jpg").convert("RGB"))
    d=f"{OUT}"; kw=dict(quality=92,optimize=True)
    crop(im,1200,1200,c).save(f"{d}/ads-quadrado_{name}.jpg",**kw)
    crop(im,960,1200,c).save(f"{d}/ads-vertical-4x5_{name}.jpg",**kw)
    if name in ("cafe-de-cima","sala-inteira","sala-poltronas","canto-terracota"):
        crop(im,1200,628,c).save(f"{d}/ads-horizontal_{name}.jpg",**kw)
    if im.width<im.height: crop(im,1080,1920,0.5).save(f"{d}/destaque-sala_{name}.jpg",**kw)
# capa do destaque
F="/home/user/midia-postagens/edicao-23-11/scripts/fonts/" if os.path.exists("/home/user/midia-postagens/edicao-23-11/scripts/fonts/") else "fonts/"
cv=Image.new("RGB",(1080,1920),(26,33,70)); d=ImageDraw.Draw(cv)
d.ellipse((240,660,840,1260),outline=(244,184,96),width=10)
# poltrona simples em linha
g=(244,184,96); w=12
d.rounded_rectangle((400,800,680,1000),40,outline=g,width=w)
d.rounded_rectangle((360,900,720,1060),40,outline=g,width=w)
d.line((410,1060,400,1120),fill=g,width=w); d.line((670,1060,680,1120),fill=g,width=w)
f=ImageFont.truetype(F+"dm-sans-latin-700-normal.ttf",64); t="SALA"; b=f.getbbox(t); d.text(((1080-(b[2]-b[0]))//2,1150),t,font=f,fill=g)
cv.save(f"{OUT}/capa-destaque-sala.jpg",quality=95)
print(len(os.listdir(OUT)))
