import sys, subprocess, numpy as np
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
for f in sys.argv[1:]:
    raw=subprocess.run(["ffmpeg","-v","error","-i",f,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
    a=np.frombuffer(raw,np.float32)
    segs,_=m.transcribe(a,language="pt",word_timestamps=True,initial_prompt="Psicóloga Marília, terapia, Cosmópolis, WhatsApp, avaliação neuropsicológica.")
    print("=====",f.split('/')[-1],flush=True)
    for s in segs:
        print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
        print("   W:", " ".join(f"{w.word.strip()}|{w.start:.2f}|{w.end:.2f}" for w in s.words),flush=True)
