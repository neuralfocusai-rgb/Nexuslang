# NexusLang v11 - Interprete propio (lexer + parser + AST tree-walk)
import sys

KW={'متغیر':'var','var':'var','variable':'var','طریقہ':'fun','fun':'fun','funcion':'fun','اگر':'if','if':'if','si':'if','ورنہ':'else','else':'else','sino':'else','جبکہ':'while','while':'while','mientras':'while','برائے':'for','for':'for','para':'for','واپس':'return','return':'return','اور':'AND','and':'AND','یا':'OR','or':'OR','نہیں':'NOT','not':'NOT'}

def lex(src):
    toks=[]; i=0; n=len(src)
    while i<n:
        c=src[i]
        if src.startswith('//',i):
            j=src.find('\n',i); i=n if j<0 else j; continue
        if c in ' \t\r\n': i+=1; continue
        if c=='"':
            j=i+1
            while j<n and src[j]!='"': j+=1
            toks.append(('STR',src[i+1:j])); i=j+1; continue
        if c.isdigit():
            j=i
            while j<n and (src[j].isdigit() or src[j]=='.'): j+=1
            v=src[i:j]; toks.append(('NUM',float(v) if '.' in v else int(v))); i=j; continue
        if c.isalpha() or c=='_' or '؀'<=c<='ۿ':
            j=i
            while j<n and (src[j].isalnum() or src[j]=='_' or '؀'<=src[j]<='ۿ'): j+=1
            w=src[i:j]; toks.append((KW[w],w) if w in KW else ('IDENT',w)); i=j; continue
        hit=False
        for name,pat in [('EQ','=='),('NE','!='),('LE','<='),('GE','>='),('ASSIGN','='),('LT','<'),('GT','>'),('PLUS','+'),('MINUS','-'),('MUL','*'),('DIV','/'),('LBR','{'),('RBR','}'),('LP','('),('RP',')'),('SEMI',';'),('COMMA',',')]:
            if src.startswith(pat,i):
                toks.append((name,pat)); i+=len(pat); hit=True; break
        if not hit: raise Exception('⛔ غلطی: غیر متوقع علامت: '+c)
    return toks

class P:
    def __init__(s,t): s.t=t; s.i=0
    def peek(s): return s.t[s.i] if s.i<len(s.t) else ('EOF','')
    def next(s): tok=s.peek(); s.i+=1; return tok
    def expect(s,ty):
        tok=s.next()
        if tok[0]!=ty: raise Exception('⛔ غلطی: ترکیب کی غلطی — توقع تھی '+ty)
        return tok
    def program(s):
        st=[]
        while s.peek()[0]!='EOF': st.append(s.stmt())
        return ('block',st)
    def block(s):
        s.expect('LBR'); st=[]
        while s.peek()[0]!='RBR': st.append(s.stmt())
        s.expect('RBR'); return ('block',st)
    def stmt(s):
        ty=s.peek()[0]
        if ty=='var':
            s.next(); name=s.expect('IDENT')[1]; s.expect('ASSIGN'); e=s.expr(); s.expect('SEMI'); return ('vardecl',name,e)
        if ty=='fun': return s.fundef()
        if ty=='if': return s.ifstmt()
        if ty=='while':
            s.next(); s.expect('LP'); c=s.expr(); s.expect('RP'); return ('while',c,s.block())
        if ty=='for': return s.forstmt()
        if ty=='return':
            s.next(); e=None
            if s.peek()[0]!='SEMI': e=s.expr()
            s.expect('SEMI'); return ('return',e)
        if ty=='IDENT' and s.i+1<len(s.t) and s.t[s.i+1][0]=='ASSIGN':
            name=s.next()[1]; s.next(); e=s.expr(); s.expect('SEMI'); return ('assign',name,e)
        e=s.expr(); s.expect('SEMI'); return ('expr',e)
    def fundef(s):
        s.next(); name=s.expect('IDENT')[1]; s.expect('LP'); params=[]
        while s.peek()[0]!='RP':
            params.append(s.expect('IDENT')[1])
            if s.peek()[0]=='COMMA': s.next()
        s.expect('RP'); return ('fun',name,params,s.block())
    def ifstmt(s):
        s.next(); s.expect('LP'); c=s.expr(); s.expect('RP'); b=s.block(); e=None
        if s.peek()[0]=='else':
            s.next()
            if s.peek()[0]=='if': e=('block',[s.ifstmt()])
            else: e=s.block()
        return ('if',c,b,e)
    def forstmt(s):
        s.next(); s.expect('LP')
        if s.peek()[0]=='var':
            s.next(); nme=s.expect('IDENT')[1]; s.expect('ASSIGN'); e=s.expr(); s.expect('SEMI'); init=('vardecl',nme,e)
        else:
            nme=s.expect('IDENT')[1]; s.expect('ASSIGN'); e=s.expr(); s.expect('SEMI'); init=('assign',nme,e)
        c=s.expr(); s.expect('SEMI')
        sn=s.expect('IDENT')[1]; s.expect('ASSIGN'); se=s.expr(); s.expect('RP')
        return ('for',init,c,(sn,se),s.block())
    def expr(s): return s.orx()
    def orx(s):
        l=s.andx()
        while s.peek()[0]=='OR': s.next(); l=('or',l,s.andx())
        return l
    def andx(s):
        l=s.cmp()
        while s.peek()[0]=='AND': s.next(); l=('and',l,s.cmp())
        return l
    def cmp(s):
        l=s.add()
        while s.peek()[0] in ('EQ','NE','LT','GT','LE','GE'):
            op=s.next()[0]; l=('cmp',op,l,s.add())
        return l
    def add(s):
        l=s.mul()
        while s.peek()[0] in ('PLUS','MINUS'):
            op=s.next()[0]; l=('bin',op,l,s.mul())
        return l
    def mul(s):
        l=s.unary()
        while s.peek()[0] in ('MUL','DIV'):
            op=s.next()[0]; l=('bin',op,l,s.unary())
        return l
    def unary(s):
        if s.peek()[0]=='NOT': s.next(); return ('not',s.unary())
        if s.peek()[0]=='MINUS': s.next(); return ('neg',s.unary())
        return s.primary()
    def primary(s):
        tok=s.next()
        if tok[0]=='NUM': return ('num',tok[1])
        if tok[0]=='STR': return ('str',tok[1])
        if tok[0]=='IDENT':
            if s.peek()[0]=='LP':
                s.next(); args=[]
                while s.peek()[0]!='RP':
                    args.append(s.expr())
                    if s.peek()[0]=='COMMA': s.next()
                s.expect('RP'); return ('call',tok[1],args)
            return ('var',tok[1])
        if tok[0]=='LP':
            e=s.expr(); s.expect('RP'); return e
        raise Exception('⛔ غلطی: غیر متوقع ٹوکن '+str(tok[0]))

class RT(Exception): pass
class Env:
    def __init__(s,parent=None): s.d={}; s.p=parent
    def get(s,n):
        e=s
        while e:
            if n in e.d: return e.d[n]
            e=e.p
        raise Exception('⛔ غلطی: یہ نام موجود نہیں: '+n)
    def set(s,n,v):
        e=s
        while e:
            if n in e.d: e.d[n]=v; return
            e=e.p
        s.d[n]=v
    def decl(s,n,v): s.d[n]=v

BUILTINS={'لکھو':lambda *a: print(' '.join(str(x) for x in a)),'print':lambda *a: print(' '.join(str(x) for x in a)),'imprimir':lambda *a: print(' '.join(str(x) for x in a)),'پڑھو':lambda *a: input(),'متن':str,'عدد':int,'لمبائی':len,'جذر':lambda x:x**0.5,'بڑا':max,'چھوٹا':min,'مطلق':abs,'گرد':round,'فہرست':lambda *a: list(a),'شامل':lambda l,x: (l.append(x) or l),'نکالو':lambda l: l.pop(),'ترتیب':lambda l: (l.sort() or l),'الٹو':lambda l: (l.reverse() or l),'عنصر':lambda l,i: l[i]}
BUILTINS.update({'list':BUILTINS['فہرست'],'lista':BUILTINS['فہرست'],'append':BUILTINS['شامل'],'agregar':BUILTINS['شامل'],'pop':BUILTINS['نکالو'],'sacar':BUILTINS['نکالو'],'sort':BUILTINS['ترتیب'],'ordenar':BUILTINS['ترتیب'],'reverse':BUILTINS['الٹو'],'invertir':BUILTINS['الٹو'],'item':BUILTINS['عنصر'],'elemento':BUILTINS['عنصر'],'len':BUILTINS['لمبائی'],'longitud':BUILTINS['لمبائی'],'sqrt':BUILTINS['جذر'],'raiz':BUILTINS['جذر'],'max':BUILTINS['بڑا'],'maximo':BUILTINS['بڑا'],'min':BUILTINS['چھوٹا'],'minimo':BUILTINS['چھوٹا'],'abs':BUILTINS['مطلق'],'absoluto':BUILTINS['مطلق'],'round':BUILTINS['گرد'],'redondear':BUILTINS['گرد'],'str':BUILTINS['متن'],'texto':BUILTINS['متن'],'int':BUILTINS['عدد'],'entero':BUILTINS['عدد'],'input':BUILTINS['پڑھو'],'leer':BUILTINS['پڑھو']})

def truthy(v): return bool(v)

def ev(node,env):
    t=node[0]
    if t=='num': return node[1]
    if t=='str': return node[1]
    if t=='var': return env.get(node[1])
    if t=='bin':
        l=ev(node[2],env); r=ev(node[3],env)
        if node[1]=='PLUS': return str(l)+str(r) if (isinstance(l,str) or isinstance(r,str)) else l+r
        if node[1]=='MINUS': return l-r
        if node[1]=='MUL': return l*r
        if node[1]=='DIV':
            if r==0: raise Exception('⛔ غلطی: صفر پر تقسیم ممکن نہیں')
            return l/r
    if t=='cmp':
        l=ev(node[2],env); r=ev(node[3],env); op=node[1]
        if op=='EQ': return l==r
        if op=='NE': return l!=r
        if op=='LT': return l<r
        if op=='GT': return l>r
        if op=='LE': return l<=r
        if op=='GE': return l>=r
    if t=='and': return truthy(ev(node[1],env)) and truthy(ev(node[2],env))
    if t=='or': return truthy(ev(node[1],env)) or truthy(ev(node[2],env))
    if t=='not': return not truthy(ev(node[1],env))
    if t=='neg': return -ev(node[1],env)
    if t=='call':
        name=node[1]; args=[ev(a,env) for a in node[2]]
        if name in BUILTINS: return BUILTINS[name](*args)
        f=env.get(name)
        if isinstance(f,tuple) and f[0]=='fn':
            ne=Env(f[3])
            for p,a in zip(f[1],args): ne.decl(p,a)
            try: run(f[2],ne)
            except RT as r: return r.args[0] if r.args else None
            return None
        raise Exception('⛔ غلطی: یہ فنکشن نہیں: '+name)
    raise Exception('⛔ غلطی: نامعلوم ایکسپریشن '+t)

def run(node,env):
    t=node[0]
    if t=='block':
        for s in node[1]: run(s,env)
    elif t=='vardecl': env.decl(node[1],ev(node[2],env))
    elif t=='assign': env.set(node[1],ev(node[2],env))
    elif t=='expr': ev(node[1],env)
    elif t=='if':
        if truthy(ev(node[1],env)): run(node[2],env)
        elif node[3]: run(node[3],env)
    elif t=='while':
        while truthy(ev(node[1],env)): run(node[2],env)
    elif t=='for':
        run(node[1],env)
        while truthy(ev(node[2],env)):
            run(node[4],env)
            env.set(node[3][0],ev(node[3][1],env))
    elif t=='fun': env.decl(node[1],('fn',node[2],node[3],env))
    elif t=='return': raise RT(ev(node[1],env) if node[1] else None)

def repl():
    env=Env()
    print('NexusLang v11 REPL — salir: خروج')
    buf=''
    while True:
        try:
            line=input('... ' if buf else '>> ')
        except EOFError:
            break
        if line.strip() in ('exit','خروج'):
            break
        buf+=line+'\n'
        if buf.count('{')>buf.count('}'):
            continue
        try:
            run(P(lex(buf)).program(),env)
        except Exception as e:
            print(str(e))
        buf=''

if __name__=='__main__':
    if len(sys.argv)>1:
        src=open(sys.argv[1],encoding='utf-8').read()
        try:
            run(P(lex(src)).program(),Env())
        except Exception as e:
            print(str(e))
    else:
        repl()
