import subprocess, numpy as np, cv2, sys
from PIL import Image, ImageDraw, ImageFont
# color stats reuse
REF_M=np.array([122.6,139.5,146.7]); REF_S=np.array([43.9,7.0,9.2])
cap=cv2.VideoCapture("c1/base.mp4"); samp=[]
for fi in range(0,523,60):
    cap.set(cv2.CAP_PROP_POS_FRAMES,fi); ok,fr=cap.read(); samp.append(cv2.cvtColor(fr[500:1300,220:660],cv2.COLOR_BGR2LAB).reshape(-1,3).astype(np.float32))
s=np.concatenate(samp); M=s.mean(0); S=s.std(0); MIX=np.array([0.5,0.9,0.9])
TM="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=rgb24,scale=1080:1920"
f=ImageFont.truetype("fonts/lora-latin-500-normal.ttf",84)
for k,(src,t) in enumerate([("7893",0.35),("7901",0.6),("7897",0.9)]):
    raw=subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",f"src/IMG_{src}.MOV","-vf",TM,"-frames:v","1","-f","rawvideo","-"],capture_output=True).stdout
    rgb=np.frombuffer(raw,np.uint8).reshape(1920,1080,3)
    lab=cv2.cvtColor(rgb,cv2.COLOR_RGB2LAB).astype(np.float32); lab=lab*(1-MIX)+((lab-M)*(REF_S/S)+REF_M)*MIX
    im=Image.fromarray(cv2.cvtColor(np.clip(lab,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)).convert("RGBA")
    lines=["Sem tempo","pra terapia?"]; d=ImageDraw.Draw(im)
    asc=f.getbbox("Ág"); lh=asc[3]-asc[1]; w=max(f.getbbox(l)[2] for l in lines)+80; h=len(lines)*(lh+18)+50
    x,y=70,1250; d.rectangle((x,y,x+w,y+h),fill="white")
    yy=y+25
    for l in lines: d.text((x+40,yy-asc[1]),l,font=f,fill=(26,26,26)); yy+=lh+18
    im.convert("RGB").save(f"out/Capa_C1_{k+1}.jpg",quality=94)
