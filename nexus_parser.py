#!/usr/bin/env python3
# NexusLang Compiler — ETAPA 2: PARSER -> AST (v8.1)
import re, sys, json
from nexus_lexer import KEYWORDS, MULTI, TOKEN_SPEC

_tok_re = re.compile('|'.join('(?P<%s>%s)' % p for p in TOKEN_SPEC))

def tokenize_line(line):
    toks = []
    for m in _tok_re.finditer(line):
        kind = m.lastgroup; val = m.group()
        if kind in ('SKIP', 'COMMENT', 'NEWLINE'): continue
        if kind == 'IDENT' and val in KEYWORDS: toks.append(('KW', KEYWORDS[val]))
        elif kind == 'MISMATCH': raise SyntaxError('caracter inesperado: %r' % val)
        else: toks.append((kind, val))
    return toks

def build_lines(src):
    for a, b in MULTI: src = src.replace(a, b)
    lines = []
    for raw in src.split('\n'):
        if not raw.strip(): continue
        toks = tokenize_line(raw.strip())
        if not toks: continue
        lines.append((len(raw) - len(raw.lstrip(' ')), toks))
    return lines

PREC = {'or':1,'and':2,'==':3,'!=':3,'<':3,'>':3,'<=':3,'>=':3,'+':4,'-':4,'*':5,'/':5}

class E:
    def __init__(self, toks): self.t = toks; self.i = 0
    def peek(self): return self.t[self.i] if self.i < len(self.t) else ('EOF','')
    def next(self): x = self.peek(); self.i += 1; return x
    def parse(self, minp=1):
        left = self.atom()
        while True:
            op = self.peek()[1]
            if op not in PREC or PREC[op] < minp: break
            self.next()
            left = ('bin', op, left, self.parse(PREC[op]+1))
        return left
    def args_until(self, close):
        args = []
        while not (self.peek()[0]=='PUNCT' and self.peek()[1]==close):
            args.append(self.parse(1))
            if self.peek()[1] == ',': self.next()
        self.next()
        return args
    def atom(self):
        t = self.next()
        if t[0]=='NUMBER': return ('num', float(t[1]) if '.' in t[1] else int(t[1]))
        if t[0]=='STRING': return ('str', t[1][1:-1])
        if t[0]=='KW' and t[1] in ('True','False'): return ('bool', t[1]=='True')
        if t[0]=='KW' and t[1]=='None': return ('none',)
        if t[0] in ('IDENT','KW') and self.peek()==('PUNCT','('):
            self.next(); return ('call', t[1], self.args_until(')'))
        if t[0]=='IDENT': return ('ident', t[1])
        if t[0]=='PUNCT' and t[1]=='(':
            e = self.parse(1); self.next(); return e
        if t[0]=='PUNCT' and t[1]=='[':
            return ('list', self.args_until(']'))
        raise SyntaxError('token inesperado: %s' % (t,))

def expr(toks): return E(toks).parse(1)

class P:
    def __init__(self, lines): self.L = lines; self.i = 0
    def eof(self): return self.i >= len(self.L)
    def cur(self): return self.L[self.i]
    def program(self): return ('program', self.block(self.L[0][0]))
    def block(self, level):
        stmts = []
        while not self.eof() and self.cur()[0] == level:
            stmts.append(self.stmt())
        return stmts
    def child_block(self, ind):
        if self.eof() or self.cur()[0] <= ind:
            raise SyntaxError('bloque con sangria esperado')
        return self.block(self.cur()[0])
    def stmt(self):
        ind, t = self.cur()
        k = t[0]
        if k==('KW','def'):
            name = t[1][1]
            params = [x[1] for x in t if x[0]=='IDENT'][1:]
            self.i += 1
            return ('func', name, params, self.child_block(ind))
        if k==('KW','if'):
            self.i += 1
            node = ('if', expr(t[1:-1]), self.child_block(ind), [])
            if not self.eof() and self.cur()[0]==ind and self.cur()[1][0]==('KW','else'):
                self.i += 1
                node = ('if', node[1], node[2], self.child_block(ind))
            return node
        if k==('KW','while'):
            self.i += 1
            return ('while', expr(t[1:-1]), self.child_block(ind))
        if k==('KW','for'):
            var = t[1][1]
            self.i += 1
            return ('for', var, expr(t[3:-1]), self.child_block(ind))
        if k==('KW','return'):
            self.i += 1
            return ('return', expr(t[1:]) if len(t) > 1 else None)
        if len(t) >= 3 and t[0][0]=='IDENT' and t[1]==('OP','='):
            self.i += 1
            return ('assign', t[0][1], expr(t[2:]))
        self.i += 1
        return ('expr', expr(t))

if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8').read()
    ast = P(build_lines(src)).program()
    print(json.dumps(ast, ensure_ascii=False)[:600])
    print('STMTS:', len(ast[1]), [n[0] for n in ast[1]])
