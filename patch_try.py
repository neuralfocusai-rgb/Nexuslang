src = open('nexuslang_v11.py', encoding='utf-8').read()
ok = True

old1 = "'نہیں':'NOT','not':'NOT'}"
new1 = "'نہیں':'NOT','not':'NOT','کوشش':'try','try':'try','intentar':'try','پکڑو':'catch','catch':'catch','capturar':'catch'}"
if old1 in src: src = src.replace(old1, new1, 1)
else: ok = False

old2 = "        if ty=='for': return s.forstmt()"
new2 = old2 + "\n        if ty=='try': return s.trystmt()"
if old2 in src: src = src.replace(old2, new2, 1)
else: ok = False

old3 = "    def expr(s): return s.orx()"
new3 = "    def trystmt(s):\n        s.next(); b=s.block()\n        s.expect('catch')\n        s.expect('LP'); err=s.expect('IDENT')[1]; s.expect('RP')\n        return ('try',b,err,s.block())\n" + old3
if old3 in src: src = src.replace(old3, new3, 1)
else: ok = False

old4 = "    elif t=='return': raise RT(ev(node[1],env) if node[1] else None)"
new4 = old4 + "\n    elif t=='try':\n        try:\n            run(node[1],env)\n        except Exception as e:\n            ne=Env(env)\n            ne.decl(node[2],str(e))\n            run(node[3],ne)"
if old4 in src: src = src.replace(old4, new4, 1)
else: ok = False

if ok:
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('try/catch trilingue OK')
else:
    print('NO se encontro alguna ancla')
