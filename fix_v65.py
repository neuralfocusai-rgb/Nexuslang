import re
src = open('nexuslang.py', encoding='utf-8').read()

# 1) builtins urdu: متن=str, لمبائی=len
old1 = "  (r'\\bیا\\b', 'or'), (r'\\bنہیں\\b', 'not'),"
new1 = old1 + "\n  (r'\\bمتن\\b', 'str'), (r'\\bلمبائی\\b', 'len'),"
print('builtins ->', src.count(old1))
src = src.replace(old1, new1, 1)

# 2) bypass urdu en el intérprete principal
pat = re.compile(r'^([ \t]*)with open\(sys\.argv\[1\], "r", encoding="utf-8"\) as f:', re.M)
m = pat.search(src)
if m:
    ind = m.group(1)
    inj = (ind + "_urdu_src = open(sys.argv[1], encoding='utf-8').read() if os.path.exists(sys.argv[1]) else ''\n"
         + ind + "if re.search('[\\u0600-\\u06FF]', _urdu_src):\n"
         + ind + "    _urdu_code = _urdu_src\n"
         + ind + "    for _p, _r in KEYWORDS:\n"
         + ind + "        _urdu_code = re.sub(_p, _r, _urdu_code)\n"
         + ind + "    exec(compile(_urdu_code, sys.argv[1], 'exec'))\n"
         + ind + "    sys.exit(0)\n")
    src = src[:m.start()] + inj + src[m.start():]
    print('bypass -> OK')
else:
    print('bypass -> ANCHOR NO ENCONTRADO')

open('nexuslang.py', 'w', encoding='utf-8').write(src)
print('MOTOR v6.5 OK')
