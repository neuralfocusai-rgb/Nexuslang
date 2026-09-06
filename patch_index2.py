src = open('nexuslang_v11.py', encoding='utf-8').read()
res = {}

o1 = "('SEMI',';'),('COMMA',',')]:"
n1 = "('SEMI',';'),('COMMA',','),('LSQ','['),('RSQ',']')]:"
res['o1'] = o1 in src
if res['o1']: src = src.replace(o1, n1, 1)

oA = "    def primary(s):\n        tok=s.next()\n        if tok[0]=='NUM': return ('num',tok[1])"
nA = "    def primary(s):\n        tok=s.next()\n        if tok[0]=='LSQ':\n            els=[]\n            while s.peek()[0]!='RSQ':\n                els.append(s.expr())\n                if s.peek()[0]=='COMMA': s.next()\n            s.expect('RSQ'); return ('arr',els)\n        if tok[0]=='NUM': return ('num',tok[1])"
res['oA'] = oA in src
if res['oA']: src = src.replace(oA, nA, 1)

oB = "    def unary(s):"
nB = "    def postfix(s,base):\n        while s.peek()[0]=='LSQ':\n            s.next(); idx=s.expr(); s.expect('RSQ'); base=('index',base,idx)\n        return base\n" + oB
res['oB'] = oB in src
if res['oB']: src = src.replace(oB, nB, 1)

oC = "        return s.primary()"
nC = "        return s.postfix(s.primary())"
res['oC'] = oC in src
if res['oC']: src = src.replace(oC, nC, 1)

o3 = "    if t=='str': return node[1]"
n3 = o3 + "\n    if t=='arr': return [ev(e,env) for e in node[1]]\n    if t=='index': return ev(node[1],env)[ev(node[2],env)]"
res['o3'] = o3 in src
if res['o3']: src = src.replace(o3, n3, 1)

o4 = "        if ty=='continue':\n            s.next(); s.expect('SEMI'); return ('continue',)"
n4 = o4 + "\n        if ty=='IDENT' and s.i+1<len(s.t) and s.t[s.i+1][0]=='LSQ':\n            name=s.next()[1]; s.next(); idx=s.expr(); s.expect('RSQ'); s.expect('ASSIGN'); val=s.expr(); s.expect('SEMI'); return ('setindex',name,idx,val)"
res['o4'] = o4 in src
if res['o4']: src = src.replace(o4, n4, 1)

o5 = "    elif t=='break': raise Brk()"
n5 = o5 + "\n    elif t=='setindex':\n        env.get(node[1])[ev(node[2],env)]=ev(node[3],env)"
res['o5'] = o5 in src
if res['o5']: src = src.replace(o5, n5, 1)

print(res)
if all(res.values()):
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Indexing + literales OK')
else:
    print('FALLARON:', [k for k,v in res.items() if not v])
