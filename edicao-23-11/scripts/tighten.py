# Corta pausas internas (> GAP s) e trechos de fala marcados para sair.
# Uso: python3 tighten.py entrada.json saida.json [cta] [seg:w0-w1 ...]  (palavras w0..w1 inclusive saem)
import json, sys
GAP, PRE, POST = 0.30, 0.10, 0.16
c = json.load(open(sys.argv[1])); cta = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else None
drop = set()
for d in sys.argv[4:]:
    s, r = d.split(":"); a, b = map(int, r.split("-")); drop |= {(int(s), k) for k in range(a, b + 1)}
segs = []; cta_new = None
for si, s in enumerate(c["segs"]):
    if si == c["cta_seg"]: cta_new = len(segs)
    W = s["words"]; cur = []
    def flush(last):
        if not cur: return
        a = s["in"] if cur[0] == 0 else W[cur[0]][1] - PRE
        b = s["out"] if last else W[cur[-1]][2] + POST
        segs.append({"file": s["file"], "in": round(a, 3), "out": round(b, 3), "words": [W[k] for k in cur]})
    for k in range(len(W)):
        if (si, k) in drop: flush(False); cur = []; continue
        if cur and W[k][1] - W[cur[-1]][2] > GAP: flush(False); cur = []
        cur.append(k)
    flush(cur and cur[-1] == len(W) - 1)
c["segs"] = segs; c["cta_seg"] = cta_new; c["chunk_starts"] = [[i, 0] for i in range(len(segs))]
if cta: c["cta"] = cta
json.dump(c, open(sys.argv[2], "w"), ensure_ascii=False)
print(sys.argv[2], len(segs), "trechos", round(sum(s["out"] - s["in"] for s in segs), 1), "s")
