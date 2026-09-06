src = open('nexuslang_v11.py', encoding='utf-8').read()
res = {}

o1 = "'continuar':'continue'}"
n1 = "'continuar':'continue','درآمد':'import','import':'import','importar':'import'}"
res['o1'] = o1 in src
if res['o1']: src = src.replace(o1, n1, 1)

o2 = "        if ty=='try': return s.trystmt()"
n2 = o2 + "\n        if ty=='import':\n            s.next(); p=s.expect('STR')[1]; s.expect('SEMI'); return ('import',p)"
res['o2'] = o2 in src
if res['o2']: src = src.replace(o2, n2, 1)

o3 = "    elif t=='setindex':"
n3 = "    elif t=='import':\n        run(P(lex(open(node[1],encoding='utf-8').read())).program(),env)\n" + o3
res['o3'] = o3 in src
if res['o3']: src = src.replace(o3, n3, 1)

o4 = "'unir':lambda sep,l: sep.join(str(x) for x in l)})"
n4 = o4 + "\nBUILTINS.update({'پڑھ_فائل':lambda p: open(p,encoding='utf-8').read(),'read_file':lambda p: open(p,encoding='utf-8').read(),'leer_archivo':lambda p: open(p,encoding='utf-8').read(),'لکھ_فائل':lambda p,t: open(p,'w',encoding='utf-8').write(t),'write_file':lambda p,t: open(p,'w',encoding='utf-8').write(t),'escribir_archivo':lambda p,t: open(p,'w',encoding='utf-8').write(t)})"
res['o4'] = o4 in src
if res['o4']: src = src.replace(o4, n4, 1)

print(res)
if all(res.values()):
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Modulos + file IO OK')
else:
    print('FALLARON:', [k for k,v in res.items() if not v])
