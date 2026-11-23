import sys, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
STYLE=sys.argv[1]; OUT=sys.argv[2]; PREVIEW=len(sys.argv)>3
W,H,FPS=1080,1920,30
FD="fonts/"
def F(n,s): return ImageFont.truetype(FD+n,s)
MB="montserrat-latin-700-normal.ttf"; MEB="montserrat-latin-800-normal.ttf"; MEBI="montserrat-latin-800-italic.ttf"; MSB="montserrat-latin-600-normal.ttf"; CG="cormorant-garamond-latin-700-normal.ttf"
NAVY=(26,33,70); PINK=(26,33,70); PINKL=(244,184,96); GOLD=(244,184,96)
DM="dm-sans-latin-500-normal.ttf"; DMB="dm-sans-latin-700-normal.ttf"
EMO=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
# ---------- timeline ----------
segs=[(1.20,0.0),(1.52,5.266667),(6.62,10.233333),(9.62,12.0)]
raw={0:[("A",1.62,1.80),("falta",1.80,2.04),("de",2.04,2.26),("tempo",2.26,2.70),("não",2.70,2.94),("é",2.94,3.14),("mais",3.14,3.38),("uma",3.38,3.56),("desculpa",3.56,4.04),("para",4.04,4.20),("você,",4.20,4.62),("nem",5.04,5.30),("a",5.30,5.52),("distância.",5.52,6.26)],
 1:[("Eu",1.62,1.72),("atendo",1.72,2.02),("online",2.02,2.54),("para",2.54,2.86),("todo",2.86,3.16),("o",3.16,3.34),("Brasil",3.34,3.78),("e",3.78,4.22),("presencialmente",4.22,5.20),("em",5.20,5.50),("Cosmópolis.",5.50,6.34)],
 2:[("Eu",6.76,6.80),("estou",6.80,6.88),("com",6.88,7.04),("o",7.04,7.14),("meu",7.14,7.16),("consultório",7.16,7.72),("novo,",7.72,8.00)],
 3:[("perto",9.58,9.92),("da",9.92,10.12),("Praça",10.12,10.40),("do",10.40,10.56),("Rodrigo,",10.56,11.20),("e",11.50,11.58),("vai",11.58,11.68),("ser",11.68,11.80),("uma",11.80,11.94),("satisfação",11.94,12.82),("atender",12.82,13.22),("você.",13.22,13.56)]}
SHIFT={0:0.0,1:0.0,2:0.25,3:0.12}
words=[]
for k,(i0,o) in enumerate(segs):
    for w,a,b in raw[k]: words.append([w,max(a+SHIFT[k],i0+0.05)-i0+o,b+SHIFT[k]-i0+o])
NB=486; CARD=45; NT=NB+CARD; TEND=NB/FPS
# basic blocks: (word index range, highlight word idx within block or None)
def blk(spec):
    out=[];i=0
    for n,h in spec: out.append((i,i+n,h)); i+=n
    return out
BLOCKS=blk([(4,3),(4,None),(3,0),(3,2),(3,2),(4,3),(2,1),(2,1),(5,None),(2,1),(3,2),(2,None),(4,None),(1,0),(2,1)])
assert BLOCKS[-1][1]==len(words), (BLOCKS[-1],len(words))
CHUNKS=[(0,11),(11,14),(14,21),(21,25),(25,32),(32,37),(37,len(words))]
# ---------- zoom ----------
CX,CY=430,760
CTA_T=[w for w in words if w[0]=="satisfação"][0][1]-0.1
def zoom(t):
    if t<3.84: return 1.0+0.012*t/3.84
    if t<5.2667: return 1.05
    if t<10.2333: return 1.08+0.012*(t-5.2667)/5
    if t<12.0: return 1.0+0.008*(t-10.2333)/1.77
    return 1.06
# ---------- color ----------
def grade(rgb):
    lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32)
    lab[...,0]=(lab[...,0]-143.8)*1.12+128
    lab[...,1]=(lab[...,1]-128)*0.92+128-2
    lab[...,2]=(lab[...,2]-128)*1.0+128+8
    return cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
# ---------- text helpers ----------
def tw(font,txt): b=font.getbbox(txt); return b[2]-b[0]
def emoji_img(ch,h):
    im=Image.new("RGBA",(160,160),(0,0,0,0)); ImageDraw.Draw(im).text((0,0),ch,font=EMO,embedded_color=True)
    im=im.crop(im.getbbox()); r=h/im.height; return im.resize((int(im.width*r),h),Image.LANCZOS)
cache={}
def layer(key,fn):
    if key not in cache: cache[key]=fn()
    return cache[key]
def paste(frame,img,x,y):
    a=np.asarray(img).astype(np.float32); h,w=a.shape[:2]
    x0,y0=max(0,x),max(0,y); x1,y1=min(W,x+w),min(H,y+h)
    if x1<=x0 or y1<=y0: return
    sub=a[y0-y:y1-y,x0-x:x1-x]; al=sub[...,3:4]/255.
    frame[y0:y1,x0:x1]=(frame[y0:y1,x0:x1]*(1-al)+sub[...,:3]*al).astype(np.uint8)
def shadowed(img,r=10,alpha=150,off=(0,4)):
    pad=r*3; base=Image.new("RGBA",(img.width+2*pad,img.height+2*pad),(0,0,0,0))
    sh=Image.new("RGBA",img.size,(0,0,0,alpha)); sh.putalpha(img.split()[3].point(lambda v:v*alpha//255))
    base.paste(sh,(pad+off[0],pad+off[1]),sh); base=base.filter(ImageFilter.GaussianBlur(r))
    base.alpha_composite(img,(pad,pad)); return base,pad
# ---- basic ----
def title_box(txt):
    f=F(DMB,48); w=tw(f,txt); bh=84; im=Image.new("RGBA",(w+60,bh),NAVY+(255,)); d=ImageDraw.Draw(im)
    b=f.getbbox(txt); d.text(((w+60-w)//2-b[0],(bh-(b[3]-b[1]))//2-b[1]),txt,font=f,fill="white"); return im
def cap_basic(bi):
    a,b,h=BLOCKS[bi]; toks=[(words[i][0].strip(",."),j==h) for j,i in enumerate(range(a,b))]
    size=92
    while True:
        fA=F(DM,size); fB=F(DMB,size); sp=tw(fA," "); padx=18
        tot=sum(tw(fB if hl else fA,t)+(2*padx if hl else 0) for t,hl in toks)+sp*(len(toks)-1)
        if tot<=940 or size<=60: break
        size-=4
    W2=tot+80; H2=size+80; txt=Image.new("RGBA",(W2,H2),(0,0,0,0)); d=ImageDraw.Draw(txt); x=40; y=30
    asc=fB.getbbox("dÁg")
    boxes=Image.new("RGBA",(W2,H2),(0,0,0,0)); db=ImageDraw.Draw(boxes)
    for t,hl in toks:
        if hl:
            bb=fB.getbbox(t); db.rounded_rectangle((x,y+asc[1]-14,x+bb[2]+2*padx,y+asc[3]+12),14,fill=NAVY+(255,))
            d.text((x+padx,y),t,font=fB,fill=GOLD); x+=bb[2]+2*padx+sp
        else:
            d.text((x,y),t,font=fA,fill="white"); x+=tw(fA,t)+sp
    sh=Image.new("RGBA",(W2,H2),(0,0,0,0)); m=Image.alpha_composite(boxes,txt).split()[3]
    sh.putalpha(m.point(lambda v:int(v*0.7))); sh=sh.filter(ImageFilter.GaussianBlur(9))
    out=Image.new("RGBA",(W2,H2),(0,0,0,0)); out.alpha_composite(sh,(0,4)); out.alpha_composite(boxes); out.alpha_composite(txt); return out
def pink_box(txt,size=54,pad=(36,22)):
    f=F(DMB,size); w=tw(f,txt); b=f.getbbox(txt); im=Image.new("RGBA",(w+2*pad[0],(b[3]-b[1])+2*pad[1]),PINK+(255,))
    ImageDraw.Draw(im).text((pad[0]-b[0],pad[1]-b[1]),txt,font=f,fill="white"); return im
# ---- dynamic ----
def rounded_box(lines,font,fill,txtc,pad=(44,28),r=22,lsp=8):
    ws=[tw(font,l) for l in lines]; asc=font.getbbox("Ág")[3]-font.getbbox("Ág")[1]
    bw=max(ws)+2*pad[0]; bh=len(lines)*asc+(len(lines)-1)*lsp+2*pad[1]
    im=Image.new("RGBA",(bw,bh),(0,0,0,0)); d=ImageDraw.Draw(im); d.rounded_rectangle((0,0,bw-1,bh-1),r,fill=fill)
    y=pad[1]
    for l,w in zip(lines,ws):
        d.text(((bw-w)//2,y-font.getbbox("Ág")[1]),l,font=font,fill=txtc); y+=asc+lsp
    return im
def label_top(txt):
    f=F(MSB,30); sp=5; w=sum(tw(f,c)+sp for c in txt); im=Image.new("RGBA",(w+20,50),(0,0,0,0)); d=ImageDraw.Draw(im); x=10
    for c in txt: d.text((x,5),c,font=f,fill="white"); x+=tw(f,c)+sp
    return shadowed(im,6,160,(0,2))
def resumo(lines,emoji):
    f=F(MEBI,70); asc=f.getbbox("Ág")[3]-f.getbbox("Ág")[1]; ws=[tw(f,l) for l in lines]
    em=emoji_img(emoji,64); ws[-1]+=em.width+16; bw=max(ws)+30; bh=len(lines)*(asc+14)+20
    im=Image.new("RGBA",(bw,bh),(0,0,0,0)); d=ImageDraw.Draw(im); y=6
    for i,l in enumerate(lines):
        x=(bw-ws[i])//2; xx=x
        for wd in l.split(" "):
            c=GOLD if (wd.isupper() and len(wd)>1) else (255,255,255)
            d.text((xx,y-f.getbbox("Ág")[1]),wd,font=f,fill=c); xx+=tw(f,wd+" ")
        if i==len(lines)-1: im.alpha_composite(em,(x+tw(f,l)+16,y+(asc-em.height)//2))
        y+=asc+14
    return shadowed(im,8,170,(0,3))
def wordcap(ci,n):
    a,b=CHUNKS[ci]; ws=[words[i][0] for i in range(a,b)][:n]
    f=F(DM,80); lines=[];cur=""
    allw=[words[i][0] for i in range(a,b)]
    # layout with full chunk so lines don't jump
    full=[];cur=""
    for w in allw:
        tst=(cur+" "+w).strip()
        if tw(f,tst)>900 and cur: full.append(cur.split()); cur=w
        else: cur=tst
    full.append(cur.split())
    im=Image.new("RGBA",(1000,3*100),(0,0,0,0)); d=ImageDraw.Draw(im); y=0; k=0
    for L in full:
        lw=tw(f," ".join(L)); x=(1000-lw)//2; s=""
        for w in L:
            if k<n: d.text((x+tw(f,s),y),w,font=f,fill="white")
            s+=w+" "; k+=1
        y+=96
    return shadowed(im.crop((0,0,1000,y+20)),8,170,(0,3))
def handle(): return shadowed(Image.open(_h()) if False else _hh(),6,160,(0,2))
def _hh():
    f=F(MB,40); t="@mariliamacedo.psi"; im=Image.new("RGBA",(tw(f,t)+20,60),(0,0,0,0)); ImageDraw.Draw(im).text((10,5),t,font=f,fill="white"); return im
grad=np.zeros((H,W,1),np.float32)
for y in range(1050,H): grad[y]=150*(y-1050)/(H-1050)/255.
def wa_box(): return rounded_box(["Me chama","no WhatsApp"],F(DMB,58),NAVY+(255,),(255,255,255,255),r=18)
# ---------- card ----------
def make_card(last):
    im=Image.fromarray(last).filter(ImageFilter.GaussianBlur(22)); a=np.asarray(im).astype(np.float32)
    a=a*0.45+np.array(NAVY)*0.35; card=Image.fromarray(np.clip(a,0,255).astype(np.uint8)).convert("RGBA"); d=ImageDraw.Draw(card)
    if STYLE=="basic":
        b=pink_box("Me chama no WhatsApp",56); card.alpha_composite(b,((W-b.width)//2,760))
    else:
        b=rounded_box(["Me chama","no WhatsApp"],F(DMB,64),NAVY+(255,),(255,255,255,255),r=18); card.alpha_composite(b,((W-b.width)//2,700))
    y=1000
    for t,f,c in [("Clica no botão e agenda",F(DMB,44),GOLD),("Rua Santa Gertrudes, 1230 · Cosmópolis",F(DM,36),(255,255,255)),("Online para todo o Brasil",F(DM,36),(255,255,255)),("Marília Macêdo · Psicóloga · Neuropsicóloga",F(DM,34),(255,255,255)),("CRP 06/229488 · @mariliamacedo.psi",F(DM,34),(255,255,255))]:
        d.text(((W-tw(f,t))//2,y),t,font=f,fill=c); y+=f.size+26
    return np.asarray(card.convert("RGB"))
# ---------- main loop ----------
dec=subprocess.Popen(["ffmpeg","-v","error","-i","c1/base.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","c1/base.wav",
 "-filter_complex","[1:a]apad[a]","-map","0:v","-map","[a]","-t",f"{NT/FPS:.3f}","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000","-movflags","+faststart",OUT],stdin=subprocess.PIPE)
last=None
for fi in range(NB):
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3: break
    t=fi/FPS; fr=np.frombuffer(buf,np.uint8).reshape(H,W,3)
    fr=grade(fr)
    z=zoom(t)
    if z!=1.0:
        M2=np.float32([[z,0,CX*(1-z)],[0,z,CY*(1-z)]]); fr=cv2.warpAffine(fr,M2,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    fr=fr.copy(); last=fr.copy()
    cur=[i for i,w in enumerate(words) if w[1]<=t+0.02]
    if STYLE=="basic":
        tb=layer("title",lambda:title_box("Sem tempo pra terapia?")); paste(fr,tb,(W-tb.width)//2,250-tb.height//2)
        bi=None
        for k,(a,b,h) in enumerate(BLOCKS):
            st=words[a][1]; en=words[b][1] if b<len(words) else words[-1][2]+0.35
            if st-0.05<=t<en: bi=k
        if bi is not None:
            c=layer(("cb",bi),lambda:cap_basic(bi)); paste(fr,c,(W-c.width)//2,1270-c.height//2)
        if t>=CTA_T:
            p=layer("cta",lambda:pink_box("Me chama no WhatsApp",48)); paste(fr,p,(W-p.width)//2,1440)
    else:
        fr=(fr.astype(np.float32)*(1-40/255.)).astype(np.float32)
        fr=(fr*(1-grad)).astype(np.uint8)
        L,pd=layer("lab",lambda:label_top("CONSULTÓRIO NOVO EM COSMÓPOLIS")); paste(fr,L,(W-L.width)//2,250-L.height//2)
        if t<3.2:
            g,gp=layer("gancho",lambda:shadowed(rounded_box(["Sem tempo","pra terapia?"],F(DMB,84),(255,255,255,255),NAVY+(255,)),14,120,(0,6)))
            paste(fr,g,(W-g.width)//2,330-gp)
        elif t<CTA_T:
            key="r1" if t<10.2333 else "r2"
            r,rp=layer(key,lambda:resumo(["Tempo e distância","NÃO são desculpa"],"⏳") if key=="r1" else resumo(["Consultório NOVO","em Cosmópolis"],"🏡"))
            paste(fr,r,(W-r.width)//2,360-rp)
        else:
            r,rp=layer("wa",lambda:shadowed(wa_box(),12,120,(0,5))); paste(fr,r,(W-r.width)//2,340-rp)
        ci=None
        for k,(a,b) in enumerate(CHUNKS):
            st=words[a][1]; en=words[b][1] if b<len(words) else 99
            if st-0.05<=t<en: ci=k
        if ci is not None:
            a,b=CHUNKS[ci]; n=sum(1 for i in range(a,b) if words[i][1]<=t+0.02); n=max(n,1)
            c,cp=layer(("wc",ci,n),lambda:wordcap(ci,n)); paste(fr,c,(W-c.width)//2,1250-cp)
        hd,hp=layer("hd",lambda:shadowed(_hh(),6,160,(0,2))); paste(fr,hd,(W-hd.width)//2,1555-hp)
    enc.stdin.write(fr.tobytes())
    if PREVIEW and fi in (15,60,130,200,330,400,470,510): Image.fromarray(fr).save(f"{OUT}.f{fi}.jpg",quality=80)
card=make_card(last)
if PREVIEW: Image.fromarray(card).save(f"{OUT}.card.jpg",quality=80)
for _ in range(CARD): enc.stdin.write(card.tobytes())
enc.stdin.close(); enc.wait(); dec.wait(); print("done",OUT)
