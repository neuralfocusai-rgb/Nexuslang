# NexusLang Urdu runner (v6.4-urdu)
import re, sys
src = open('nexuslang.py', encoding='utf-8').read()
a = src.index('KEYWORDS = [')
b = src.index('\n]', a)
KW = eval(src[a+len('KEYWORDS = '):b+2])
code = open(sys.argv[1], encoding='utf-8').read()
for pat, rep in KW:
    code = re.sub(pat, rep, code)
exec(compile(code, 'urdu', 'exec'))
