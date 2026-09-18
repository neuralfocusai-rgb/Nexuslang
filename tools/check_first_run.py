#!/usr/bin/env python3
# pre-release gate: todo ejemplo debe correr en el core (audit P0 #2)
import subprocess, tempfile, os, sys, json
EX = [["سلام دنیا", "چھاپو(\"سلام دنیا\")\n"], ["پہلا پروگرام", "ریغتم سلام = \"السلام علیکہ\"\nچھاپو(سلام)\n"], ["شرط", "ریغتم نمرہ = 5\nاگر (نمرہ > 3) {\nچھاپو(\"پاس\")\n} ورنہ {\nچھاپو(\"فیل\")\n}\n"], ["لوپ", "ریغتم ع = 1\nجبکہ (ع < 4) {\nچھاپو(ع)\nع = ع + 1\n}\n"], ["فنکشن", "فنکشن سلام(نام) {\nواپس \"سلام \" + نام\n}\nچھاپو(سلام(\"پاکستان\"))\n"]]
bad = 0
for n, c in EX:
    with tempfile.NamedTemporaryFile("w", suffix=".nx", delete=False, encoding="utf-8") as f:
        f.write(c); p = f.name
    r = subprocess.run([sys.executable, "nexuslang_v12.py", p], capture_output=True, text=True)
    os.unlink(p)
    print("PASS" if r.returncode == 0 else "FAIL", n)
    bad += r.returncode != 0
sys.exit(1 if bad else 0)
