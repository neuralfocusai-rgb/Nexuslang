src = open('nexuslang_v11.py', encoding='utf-8').read()
ok = True

o1 = "('SEMI',';'),('COMMA',',')]:"
n1 = "('SEMI',';'),('COMMA',','),('LSQ','['),('RSQ',']')]:"
if o1 in src: src = src.replace(o1, n1, 1)
else: ok = False

o2 = """    def primary(s):
        tok=s.next()
        if tok[0]=='NUM': return ('num',tok[1])
        if tok[0]=='STR': return ('str',tok[1])
        if tok[0]=='IDENT':
            if s.peek()[0]=='LP':
                s.next(); args=[]
                while s.peek()[0]!=('RP'):
                    args.append(s.expr())
                    if s.peek()[0]=='COMMA': s.next()
                s.expect('RP'); return ('call',tok[1],args)
            return ('var',tok[1])
        if tok[0]=='LP':
            e=s.expr(); s.expect('RP'); return e
        raise Exception('⛔ غلطی: غیر متوقع ٹوکن '+str(tok[0]))"""
n2 = """    def primary(s):
        tok=s.next()
        base=None
        if tok[0]=='NUM': base=('num',tok[1])
        elif tok[0]=='STR': base=('str',tok[1])
        elif tok[0]=='LSQ':
            els=[]
            while s.peek()[0]!='RSQ':
                els.append(s.expr())
                if s.peek()[0]=='COMMA': s.next()
            s.expect('RSQ'); base=('arr',els)
        elif tok[0]=='IDENT':
            if s.peek()[0]=='LP':
                s.next(); args=[]
                while s.peek()[0]!='RP':
                    args.append(s.expr())
                    if s.peek()[0]=='COMMA': s.next()
                s.expect('RP'); base=('call',tok[1],args)
            else: base=('var',tok[1])
        elif tok[0]=='LP':
            e=s.expr(); s.expect('RP'); base=e
        else: raise Exception('⛔ غلطی: غیر متوقع ٹوکن '+str(tok[0]))
        while s.peek()[0]=='LSQ':
            s.next(); idx=s.expr(); s.expect('RSQ'); base=('index',base,idx)
        return base"""
if o2 in src: src = src.replace(o2, n2, 1)
else: ok = False

o3 = "    if t=='str': return node[1]"
n3 = o3 + "\n    if t=='arr': return [ev(e,env) for e in node[1]]\n    if t=='index': return ev(node[1],env)[ev(node[2],env)]"
if o3 in src: src = src.replace(o3, n3, 1)
else: ok = False

o4 = "        if ty=='continue':\n            s.next(); s.expect('SEMI'); return ('continue',)"
n4 = o4 + "\n        if ty=='IDENT' and s.i+1<len(s.t) and s.t[s.i+1][0]=='LSQ':\n            name=s.next()[1]; s.next(); idx=s.expr(); s.expect('RSQ'); s.expect('ASSIGN'); val=s.expr(); s.expect('SEMI'); return ('setindex',name,idx,val)"
if o4 in src: src = src.replace(o4, n4, 1)
else: ok = False

o5 = "    elif t=='break': raise Brk()"
n5 = o5 + "\n    elif t=='setindex':\n        env.get(node[1])[ev(node[2],env)]=ev(node[3],env)"
if o5 in src: src = src.replace(o5, n5, 1)
else: ok = False

if ok:
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Indexing + literales OK')
else:
    print('NO se encontro alguna ancla')
