src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "            s.next(); p=s.expect('STR')[1]; s.expect('SEMI'); return ('import',p)"
new = "            s.next()\n            if s.peek()[0]=='LP': s.next(); p=s.expect('STR')[1]; s.expect('RP')\n            else: p=s.expect('STR')[1]\n            s.expect('SEMI'); return ('import',p)"
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Import con parentesis OK')
else:
    print('NO se encontro')
