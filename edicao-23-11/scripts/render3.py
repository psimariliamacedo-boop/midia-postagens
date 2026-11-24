import sys, json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
# Uso: python3 render2.py config.json basic|dynamic pasta_base saida.mp4 [preview]
CFG=json.load(open(sys.argv[1])); STYLE=sys.argv[2]; BASE=sys.argv[3]; OUT=sys.argv[4]; PREVIEW=len(sys.argv)>5
W,H,FPS=1080,1920,30
FD=sys.path[0]+"/fonts/" if False else "fonts/"
def F(n,s): return ImageFont.truetype(FD+n,s)
MB="montserrat-latin-700-normal.ttf"; MEB="montserrat-latin-800-normal.ttf"; MEBI="montserrat-latin-800-italic.ttf"; MSB="montserrat-latin-600-normal.ttf"
NAVY=(26,33,70); PINK=(26,33,70); GOLD=(244,184,96)
DM="dm-sans-latin-500-normal.ttf"; DMB="dm-sans-latin-700-normal.ttf"
EMO=ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",109)
# ---------- timeline ----------
words=[]; seg_start=[]; off=0.0; gidx={}
for si,s in enumerate(CFG["segs"]):
    seg_start.append(off)
    for wi,(w,a,b) in enumerate(s["words"]):
        gidx[(si,wi)]=len(words); words.append([w,max(a,s["in"]+0.03)-s["in"]+off,b-s["in"]+off])
    off+=s["out"]-s["in"]
TEND=off; NB=int(round(TEND*FPS)); CARD=45; NT=NB+CARD
KEYS=set(CFG["keys"])
# blocos da legenda básica: 2 a 4 palavras, quebra em pontuação e em troca de corte
BLOCKS=[]; i=0
segof=[si for si,s in enumerate(CFG["segs"]) for _ in s["words"]]
while i<len(words):
    j=i
    while j<len(words) and j-i<4:
        j+=1
        if words[j-1][0][-1] in ",.?!" or (j<len(words) and segof[j]!=segof[i]): break
        if j-i>=3 and j<len(words) and len(words[j][0])>8: break
    if j<len(words) and j-i<4 and len(words)-j==1 and segof[j]==segof[i]: j+=1
    h=None
    for k in range(i,j):
        if words[k][0] in KEYS: h=k-i
    BLOCKS.append((i,j,h)); i=j
CHUNKS=[]; cs=[gidx[tuple(x)] for x in CFG["chunk_starts"]]+[len(words)]
for a,b in zip(cs,cs[1:]): CHUNKS.append((a,b))
CTA_T=CFG.get("cta_t",seg_start[CFG["cta_seg"]])
# ---------- zoom: alterna plano aberto e fechado a cada corte ----------
CX,CY=540,620
def zoom(t):
    si=max(k for k,s0 in enumerate(seg_start) if s0<=t+1e-6); u=t-seg_start[si]
    return (1.0+0.004*u) if si%2==0 else (1.07+0.004*u)
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
def wrapl(f,txt,maxw):
    L=[];cur=""
    for w in txt.split():
        t=(cur+" "+w).strip()
        if tw(f,t)>maxw and cur: L.append(cur); cur=w
        else: cur=t
    return L+[cur]
def title_box(txt):
    b,_=shadowed(rounded_box(wrapl(F(DMB,70),txt,820),F(DMB,70),(255,255,255,252),NAVY+(255,),pad=(46,30),r=26,lsp=10),14,110,(0,6)); return b
def title_box_old(txt):
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
dec=subprocess.Popen(["ffmpeg","-v","error","-i",BASE+"/base.mp4","-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
enc=subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",BASE+"/base.wav",
 "-filter_complex","[1:a]apad[a]","-map","0:v","-map","[a]","-t",f"{NT/FPS:.3f}","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","256k","-ar","48000","-movflags","+faststart",OUT],stdin=subprocess.PIPE)
last=None; snaps=set([0]+[int(x*FPS) for x in [2.0,5.0,9.0,14.0,19.0,24.0]]+[NB-20])
for fi in range(NB):
    buf=dec.stdout.read(W*H*3)
    if len(buf)<W*H*3:
        if last is None: break
        fr=last.copy()
    else:
        fr=np.frombuffer(buf,np.uint8).reshape(H,W,3)
        fr=fr if CFG.get("no_grade") else grade(fr)
        z=zoom(fi/FPS)
        if z!=1.0:
            M2=np.float32([[z,0,CX*(1-z)],[0,z,CY*(1-z)]]); fr=cv2.warpAffine(fr,M2,(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
        fr=fr.copy(); last=fr.copy()
    t=fi/FPS
    if STYLE=="basic":
        if t<CFG["hook_end"]:
            tb=layer("title",lambda:title_box(CFG["title"])); paste(fr,tb,(W-tb.width)//2,CFG.get("cap_y",1270)-70-tb.height+42)
        bi=None
        for k,(a,b,h) in enumerate(BLOCKS):
            st=words[a][1]; en=words[b][1] if b<len(words) else TEND
            if st-0.05<=t<en: bi=k
        if bi is not None:
            c=layer(("cb",bi),lambda:cap_basic(bi)); paste(fr,c,(W-c.width)//2,CFG.get("cap_y",1270)-c.height//2)
        if t>=CTA_T:
            p=layer("cta",lambda:rounded_box(wrapl(F(DMB,46),CFG["cta"],CFG.get("cta_w",760)),F(DMB,46),NAVY+(245,),GOLD+(255,),pad=(36,20),r=20,lsp=6)); paste(fr,p,(W-p.width)//2,CFG.get("cta_y",1440))
    else:
        fr=(fr.astype(np.float32)*(1-40/255.)).astype(np.float32)
        fr=(fr*(1-grad)).astype(np.uint8)
        if t<CFG["hook_end"]:
            g,gp=layer("gancho",lambda:shadowed(rounded_box(CFG["hook"],F(DMB,84),(255,255,255,255),NAVY+(255,)),14,120,(0,6)))
            paste(fr,g,(W-g.width)//2,880-gp)
        elif t<CTA_T or True:
            rs=[k for k,r in enumerate(CFG["resumos"]) if r[0]<=t]
            if rs:
                k=rs[-1]; r,rp=layer(("r",k),lambda:resumo(CFG["resumos"][k][1],CFG["resumos"][k][2]))
                paste(fr,r,(W-r.width)//2,900-rp)
        ci=None
        for k,(a,b) in enumerate(CHUNKS):
            st=words[a][1]; en=words[b][1] if b<len(words) else 99
            if st-0.05<=t<en: ci=k
        if ci is not None:
            a,b=CHUNKS[ci]; n=sum(1 for i in range(a,b) if words[i][1]<=t+0.02); n=max(n,1)
            c,cp=layer(("wc",ci,n),lambda:wordcap(ci,n)); paste(fr,c,(W-c.width)//2,1250-cp)
        if t>=CTA_T:
            p,pp=layer("ctad",lambda:shadowed(rounded_box(["Manda pra amiga","que descansa trabalhando"],F(DMB,46),NAVY+(255,),(255,255,255,255),r=18),12,120,(0,5)))
            paste(fr,p,(W-p.width)//2,1540-pp)
        else:
            hd,hp=layer("hd",lambda:shadowed(_hh(),6,160,(0,2))); paste(fr,hd,(W-hd.width)//2,1555-hp)
    enc.stdin.write(fr.tobytes())
    if PREVIEW and fi in snaps: Image.fromarray(fr).save(f"{OUT}.f{fi}.jpg",quality=80)
card=make_card(last)
if PREVIEW: Image.fromarray(card).save(f"{OUT}.card.jpg",quality=80)
for _ in range(CARD): enc.stdin.write(card.tobytes())
enc.stdin.close(); enc.wait(); dec.kill(); print("done",OUT, f"{NT/FPS:.1f}s")
