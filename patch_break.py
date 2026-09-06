src = open('nexuslang_v11.py', encoding='utf-8').read()
ok = True

o1 = "'capturar':'catch'}"
n1 = "'capturar':'catch','توڑو':'break','break':'break','romper':'break','جاری':'continue','continue':'continue','continuar':'continue'}"
if o1 in src: src = src.replace(o1, n1, 1)
else: ok = False

o2 = "class RT(Exception): pass"
n2 = o2 + "\nclass Brk(Exception): pass\nclass Cont(Exception): pass"
if o2 in src: src = src.replace(o2, n2, 1)
else: ok = False

o3 = "        if ty=='try': return s.trystmt()"
n3 = o3 + "\n        if ty=='break':\n            s.next(); s.expect('SEMI'); return ('break',)\n        if ty=='continue':\n            s.next(); s.expect('SEMI'); return ('continue',)"
if o3 in src: src = src.replace(o3, n3, 1)
else: ok = False

o4 = "    elif t=='while':\n        while truthy(ev(node[1],env)): run(node[2],env)"
n4 = "    elif t=='while':\n        while truthy(ev(node[1],env)):\n            try: run(node[2],env)\n            except Brk: break\n            except Cont: continue"
if o4 in src: src = src.replace(o4, n4, 1)
else: ok = False

o5 = "    elif t=='for':\n        run(node[1],env)\n        while truthy(ev(node[2],env)):\n            run(node[4],env)\n            env.set(node[3][0],ev(node[3][1],env))"
n5 = "    elif t=='for':\n        run(node[1],env)\n        while truthy(ev(node[2],env)):\n            try: run(node[4],env)\n            except Brk: break\n            except Cont: pass\n            env.set(node[3][0],ev(node[3][1],env))"
if o5 in src: src = src.replace(o5, n5, 1)
else: ok = False

o6 = "    elif t=='try':"
n6 = "    elif t=='break': raise Brk()\n    elif t=='continue': raise Cont()\n" + o6
if o6 in src: src = src.replace(o6, n6, 1)
else: ok = False

if ok:
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('break/continue trilingue OK')
else:
    print('NO se encontro alguna ancla')
