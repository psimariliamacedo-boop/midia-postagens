import json,subprocess,re,sys
S=sys.argv[1]
def bounds(n):
    r=subprocess.run(["ffmpeg","-i",f"{S}/brutos/IMG_{n}.MOV","-af","silencedetect=n=-38dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
    ev=[(m.group(1),float(m.group(2))) for m in re.finditer(r"silence_(start|end): ([0-9.]+)",r)]
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{S}/brutos/IMG_{n}.MOV"],capture_output=True,text=True).stdout)
    on=next(t for k,t in ev if k=="end" and t>0.05) if ev and ev[0]==("start",0.0) else 0.05
    return on,[t for k,t in ev if k=="start"],d
FIX={"Gertrudis,":"Gertrudes,"}
def seg(n):
    on,starts,d=bounds(n); ws=[]
    for l in open(f"{S}/tr/IMG_{n}.MOV.txt"):
        if not l.strip().startswith("W:"): continue
        for tok in l.strip()[3:].split():
            w,a,b=tok.rsplit("|",2); ws.append([FIX.get(w,w),float(a)+0.15,float(b)+0.15])
    m=[]
    for w in ws:
        if m and m[-1][0]=="12" and w[0].startswith(".30"): m[-1]=["1230,",m[-1][1],w[2]]
        else: m.append(w)
    ws=m; ws[0][1]=on
    lw=ws[-1][2]-0.15; c=[t for t in starts if t>=lw-0.4]; off=min(c) if c else d-0.05
    for k in range(1,len(ws)): ws[k][1]=max(ws[k][1],ws[k-1][1]+0.08)
    return dict(file=n,**{"in":round(max(0,on-0.11),2),"out":round(min(d,off+0.14),2)},words=ws)
V={
 "c2":dict(takes=[7948,7954,7963],title="Esperando sobrar tempo?",cta="Me chama no WhatsApp",keys=["sobrar","mesma,","Cosmópolis","noite.","WhatsApp","rotina."]),
 "tdah":dict(takes=[7967,7968,7971,7972,7975,7976],title="Sempre se achou desorganizada?",cta="Me chama no WhatsApp",keys=["esquecida,","desorganizada,","confusão?","hora","investigação","diagnóstico.","calma","Cosmópolis","Brasil.","WhatsApp"]),
 "avaliacao":dict(takes=[8007,8014,8017,8026,8029,8032],title="Avaliação de TDAH é uma prova?",cta="Me chama no WhatsApp",keys=["prova,","escola.","adiando","certo","errado","ritmo.","atenção","funciona","diagnóstico.","caminho","entender."]),
 "primeira":dict(takes=[8061,8063,8073,8077],title="Medo da primeira sessão?",cta="Salva pra quando decidir começar",keys=["terapia","mostrar","poltrona","história.","certo,","errado,","tempo.","perguntas","sala.","dito"]),
 "cosmopolis":dict(takes=[8088,8091,8096],title="Terapia em Cosmópolis",cta="Me chama no WhatsApp",keys=["Cosmópolis","terapia?","Gertrudes,","Rodrigo.","online.","WhatsApp."]),
}
for k,v in V.items():
    segs=[seg(n) for n in v["takes"]]
    c=dict(segs=segs,title=v["title"],hook=[v["title"]],hook_end=3.0,label="",resumos=[],cta=v["cta"],keys=v["keys"],
           chunk_starts=[[i,0] for i in range(len(segs))],cta_seg=len(segs)-1)
    json.dump(c,open(f"{k}.json","w"),ensure_ascii=False,indent=0)
    tot=sum(s["out"]-s["in"] for s in segs)
    print(k,f"{tot:.1f}s",[(s["file"],s["in"],s["out"]) for s in segs])
