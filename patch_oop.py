src = open('nexuslang_v11.py', encoding='utf-8').read()
res = {}

o1 = "'importar':'import'}"
n1 = "'importar':'import','کلاس':'class','class':'class','clase':'class'}"
res['o1'] = o1 in src
if res['o1']: src = src.replace(o1, n1, 1)

o2 = "('LSQ','['),('RSQ',']')]:"
n2 = "('LSQ','['),('RSQ',']'),('DOT','.')]):"
res['o2'] = o2 in src
if res['o2']: src = src.replace(o2, n2, 1)

o3 = """    def postfix(s,base):
        while s.peek()[0]=='LSQ':
            s.next(); idx=s.expr(); s.expect('RSQ'); base=('index',base,idx)
        return base"""
n3 = """    def postfix(s,base):
        while s.peek()[0] in ('LSQ','DOT'):
            if s.peek()[0]=='LSQ':
                s.next(); idx=s.expr(); s.expect('RSQ'); base=('index',base,idx)
            else:
                s.next(); attr=s.expect('IDENT')[1]
                if s.peek()[0]=='LP':
                    s.next(); args=[]
                    while s.peek()[0]!='RP':
                        args.append(s.expr())
                        if s.peek()[0]=='COMMA': s.next()
                    s.expect('RP'); base=('method',base,attr,args)
                else: base=('member',base,attr)
        return base"""
res['o3'] = o3 in src
if res['o3']: src = src.replace(o3, n3, 1)

o4 = "    def trystmt(s):"
n4 = "    def classstmt(s):\n        s.next(); name=s.expect('IDENT')[1]; s.expect('LBR'); methods={}\n        while s.peek()[0]!='RBR':\n            if s.peek()[0]=='fun':\n                f=s.fundef(); methods[f[1]]=(f[2],f[3])\n            else: s.next()\n        s.expect('RBR'); return ('class',name,methods)\n" + o4
res['o4'] = o4 in src
if res['o4']: src = src.replace(o4, n4, 1)

o5 = "        if ty=='try': return s.trystmt()"
n5 = "        if ty=='class': return s.classstmt()\n" + o5
res['o5'] = o5 in src
if res['o5']: src = src.replace(o5, n5, 1)

o6 = "            name=s.next()[1]; s.next(); idx=s.expr(); s.expect('RSQ'); s.expect('ASSIGN'); val=s.expr(); s.expect('SEMI'); return ('setindex',name,idx,val)"
n6 = o6 + "\n        if ty=='IDENT' and s.i+1<len(s.t) and s.t[s.i+1][0]=='DOT':\n            save=s.i; name=s.next()[1]; s.next(); attr=s.expect('IDENT')[1]\n            if s.peek()[0]=='ASSIGN':\n                s.next(); val=s.expr(); s.expect('SEMI'); return ('setmember',name,attr,val)\n            if s.peek()[0]=='LP':\n                s.next(); args=[]\n                while s.peek()[0]!='RP':\n                    args.append(s.expr())\n                    if s.peek()[0]=='COMMA': s.next()\n                s.expect('RP'); s.expect('SEMI'); return ('expr',('method',('var',name),attr,args))\n            s.i=save"
res['o6'] = o6 in src
if res['o6']: src = src.replace(o6, n6, 1)

o7 = "    if t=='index': return ev(node[1],env)[ev(node[2],env)]"
n7 = o7 + "\n    if t=='member': return ev(node[1],env)[node[2]]\n    if t=='method':\n        b=ev(node[1],env); cls=b['__class__']; f=cls[2][node[2]]\n        args=[ev(a,env) for a in node[3]]\n        ne=Env(f[3]); ne.decl('خود',b); ne.decl('self',b)\n        for p,a in zip(f[1],args): ne.decl(p,a)\n        try: run(f[2],ne)\n        except RT as r: return r.args[0] if r.args else None\n        return None"
res['o7'] = o7 in src
if res['o7']: src = src.replace(o7, n7, 1)

o8 = "    elif t=='import':"
n8 = "    elif t=='class':\n        m={}\n        for k,v in node[2].items(): m[k]=('fn',v[0],v[1],env)\n        env.decl(node[1],('cls',node[1],m))\n    elif t=='setmember':\n        env.get(node[1])[node[2]]=ev(node[3],env)\n" + o8
res['o8'] = o8 in src
if res['o8']: src = src.replace(o8, n8, 1)

o9 = "        f=env.get(name)"
n9 = o9 + "\n        if isinstance(f,tuple) and f[0]=='cls':\n            inst={'__class__':f}\n            if 'نیا' in f[2]:\n                cf=f[2]['نیا']; ne=Env(cf[3]); ne.decl('خود',inst); ne.decl('self',inst)\n                for p,a in zip(cf[1],args): ne.decl(p,a)\n                try: run(cf[2],ne)\n                except RT: pass\n            return inst"
res['o9'] = o9 in src
if res['o9']: src = src.replace(o9, n9, 1)

print(res)
if all(res.values()):
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('OOP clases OK')
else:
    print('FALLARON:', [k for k,v in res.items() if not v])
