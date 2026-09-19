import subprocess,tempfile,os,sys,json
EX=[["hello", "لکھو(\"hello world\")\n"], ["var", "متغیر name = \"NexusLang\"\nلکھو(name)\n"], ["if", "متغیر n = 5\nاگر (n > 3) {\nلکھو(\"pass\")\n} ورنہ {\nلکھو(\"fail\")\n}\n"], ["while", "متغیر i = 1\nجبکہ (i < 4) {\nلکھو(i)\n i = i + 1\n}\n"]]
bad=0
for n,c in EX:
    t=tempfile.NamedTemporaryFile("w",suffix=".nx",delete=False,encoding="utf-8");t.write(c);t.close()
    r=subprocess.run([sys.executable,"nexuslang_v12.py",t.name],capture_output=True,text=True);os.unlink(t.name)
    o=(r.stderr+r.stdout).lower();ok=r.returncode==0 and "error" not in o and "not defined" not in o
    print("PASS" if ok else "FAIL",n);bad+=not ok
sys.exit(1 if bad else 0)
