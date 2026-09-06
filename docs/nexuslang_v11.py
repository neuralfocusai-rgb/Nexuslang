#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re

KW = {
 'متغیر':'VAR','variable':'VAR','var':'VAR',
 'لکھو':'PRINT','escribir':'PRINT','print':'PRINT',
 'اگر':'IF','si':'IF','if':'IF',
 'ورنہ':'ELSE','sino':'ELSE','else':'ELSE',
 'جبکہ':'WHILE','mientras':'WHILE','while':'WHILE',
 'برائے':'FOR','para':'FOR','for':'FOR',
 'طریقہ':'DEF','funcion':'DEF','def':'DEF','function':'DEF',
 'واپس':'RETURN','retornar':'RETURN','return':'RETURN',
 'کلاس':'CLASS','clase':'CLASS','class':'CLASS',
 'خود':'SELF','esto':'SELF','self':'SELF',
 'نیا':'NEW','nuevo':'NEW','new':'NEW',
 'کوشش':'TRY','intentar':'TRY','try':'TRY',
 'پکڑو':'CATCH','capturar':'CATCH','catch':'CATCH',
 'توڑو':'BREAK','romper':'BREAK','break':'BREAK',
 'جاری':'CONTINUE','continuar':'CONTINUE','continue':'CONTINUE',
 'صحيح':'TRUE','verdadero':'TRUE','true':'TRUE',
 'غلط':'FALSE','falso':'FALSE','false':'FALSE',
 'خالی':'NONE','nulo':'NONE','null':'NONE','none':'NONE',
}

TOKENS = [
 ('STRING', r'"[^"]*"|\'[^\']*\''),
 ('NUMBER', r'\d+(?:\.\d+)?'),
 ('IDENT', r'[A-Za-z_\u0600-\u06FF][A-Za-z0-9_\u0600-\u06FF]*'),
 ('OP2', r'==|!=|<=|>=|&&|\|\|'),
 ('ASSIGN', r'='),
 ('OP1', r'[+\-*/%<>!]'),
 ('LPAREN', r'\('), ('RPAREN', r'\)'),
 ('LBRACE', r'\{'), ('RBRACE', r'\}'),
 ('COMMA', r','), ('SEMI', r';'), ('DOT', r'\.'),
 ('WS', r'\s+'),
]

def tokenize(code):
    code = re.sub(r'//[^\n]*', '', code)
    rx = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKENS))
    tokens = []; line = 1
    for m in rx.finditer(code):
        kind = m.lastgroup; val = m.group()
        if kind == 'WS':
            line += val.count('\n'); continue
        if kind == 'IDENT' and val in KW: kind = KW[val]
        elif kind == 'NUMBER': val = float(val) if '.' in val else int(val)
        elif kind == 'STRING': val = val[1:-1]
        elif kind in ('OP1', 'OP2'): kind = 'OP'
        tokens.append({'kind': kind, 'value': val, 'line': line})
    tokens.append({'kind': 'EOF', 'value': None, 'line': line})
    return tokens

class ReturnExc(Exception):
    def __init__(self, v): self.v = v
class BreakExc(Exception): pass
class ContExc(Exception): pass

class Interp:
    def __init__(self):
        self.vars = {}; self.functions = {}; self.tokens = []; self.pos = 0; self.output = []
    def cur(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else {'kind':'EOF','value':None,'line':0}
    def peek(self): return self.tokens[self.pos+1] if self.pos+1 < len(self.tokens) else {'kind':'EOF','value':None,'line':0}
    def consume(self, kind=None):
        t = self.cur()
        if kind and t['kind'] != kind:
            raise Exception(f"لائن {t['line']}: متوقع {kind} مگر ملا {t['kind']}")
        self.pos += 1; return t
    def parse(self):
        while self.cur()['kind'] != 'EOF':
            self.statement()
    def statement(self):
        k = self.cur()['kind']
        if k == 'VAR': self.var_decl()
        elif k == 'PRINT': self.print_stmt()
        elif k == 'IF': self.if_stmt()
        elif k == 'WHILE': self.while_stmt()
        elif k == 'DEF': self.func_decl()
        elif k == 'RETURN': self.return_stmt()
        elif k == 'BREAK': self.consume('BREAK'); self.eat_semi(); raise BreakExc()
        elif k == 'CONTINUE': self.consume('CONTINUE'); self.eat_semi(); raise ContExc()
        elif k == 'LBRACE': self.block()
        elif k == 'SEMI': self.pos += 1
        elif k == 'IDENT' and self.peek()['kind'] == 'ASSIGN':
            name = self.consume('IDENT')['value']; self.consume('ASSIGN')
            v = self.expression(); self.eat_semi(); self.vars[name] = v
        else:
            self.expression(); self.eat_semi()
    def eat_semi(self):
        if self.cur()['kind'] == 'SEMI': self.pos += 1
    def var_decl(self):
        self.consume('VAR'); name = self.consume('IDENT')['value']
        self.consume('ASSIGN'); v = self.expression(); self.eat_semi()
        self.vars[name] = v
    def print_stmt(self):
        self.consume('PRINT'); v = self.expression(); self.eat_semi()
        self.output.append(str(v))
    def skip_block(self):
        self.consume('LBRACE'); d = 1
        while d > 0 and self.cur()['kind'] != 'EOF':
            if self.cur()['kind'] == 'LBRACE': d += 1
            elif self.cur()['kind'] == 'RBRACE': d -= 1
            self.pos += 1
    def block(self):
        self.consume('LBRACE')
        while self.cur()['kind'] != 'RBRACE' and self.cur()['kind'] != 'EOF':
            self.statement()
        self.consume('RBRACE')
    def if_stmt(self):
        self.consume('IF'); self.consume('LPAREN')
        cond = self.expression(); self.consume('RPAREN')
        if cond:
            self.block()
            if self.cur()['kind'] == 'ELSE':
                self.consume('ELSE'); self.skip_block()
        else:
            self.skip_block()
            if self.cur()['kind'] == 'ELSE':
                self.consume('ELSE'); self.block()
    def while_stmt(self):
        self.consume('WHILE'); self.consume('LPAREN')
        cond_start = self.pos
        self.expression(); self.consume('RPAREN')
        body_start = self.pos
        self.skip_block(); body_end = self.pos
        while True:
            self.pos = cond_start
            cond = self.expression(); self.consume('RPAREN')
            if not cond: break
            self.pos = body_start
            try:
                self.block()
            except BreakExc: break
            except ContExc: pass
        self.pos = body_end
    def func_decl(self):
        self.consume('DEF'); name = self.consume('IDENT')['value']
        self.consume('LPAREN'); params = []
        if self.cur()['kind'] != 'RPAREN':
            params.append(self.consume('IDENT')['value'])
            while self.cur()['kind'] == 'COMMA':
                self.pos += 1; params.append(self.consume('IDENT')['value'])
        self.consume('RPAREN')
        start = self.pos; self.skip_block()
        self.functions[name] = {'params': params, 'start': start, 'end': self.pos}
    def return_stmt(self):
        self.consume('RETURN'); v = self.expression(); self.eat_semi()
        raise ReturnExc(v)
    def call_function(self, name, args):
        f = self.functions[name]
        old = self.vars.copy()
        for p, a in zip(f['params'], args): self.vars[p] = a
        save = self.pos; self.pos = f['start']
        result = None
        try:
            self.block()
        except ReturnExc as e:
            result = e.v
        self.vars = old; self.pos = save
        return result
    def expression(self): return self.or_expr()
    def or_expr(self):
        left = self.and_expr()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] == '||':
            self.pos += 1; left = left or self.and_expr()
        return left
    def and_expr(self):
        left = self.equality()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] == '&&':
            self.pos += 1; left = left and self.equality()
        return left
    def equality(self):
        left = self.comparison()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('==', '!='):
            op = self.consume()['value']; right = self.comparison()
            left = (left == right) if op == '==' else (left != right)
        return left
    def comparison(self):
        left = self.term()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('<', '>', '<=', '>='):
            op = self.consume()['value']; right = self.term()
            if op == '<': left = left < right
            elif op == '>': left = left > right
            elif op == '<=': left = left <= right
            else: left = left >= right
        return left
    def term(self):
        left = self.factor()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('+', '-'):
            op = self.consume()['value']; right = self.factor()
            if op == '+':
                left = str(left) + str(right) if isinstance(left, str) or isinstance(right, str) else left + right
            else: left = left - right
        return left
    def factor(self):
        left = self.unary()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('*', '/', '%'):
            op = self.consume()['value']; right = self.unary()
            if op == '*': left = left * right
            elif op == '/': left = left / right
            else: left = left % right
        return left
    def unary(self):
        if self.cur()['kind'] == 'OP' and self.cur()['value'] in ('-', '!'):
            op = self.consume()['value']; v = self.unary()
            return -v if op == '-' else (not v)
        return self.call()
    def call(self):
        expr = self.primary()
        while True:
            if self.cur()['kind'] == 'LPAREN' and isinstance(expr, str) and expr in self.functions:
                self.pos += 1; args = []
                if self.cur()['kind'] != 'RPAREN':
                    args.append(self.expression())
                    while self.cur()['kind'] == 'COMMA':
                        self.pos += 1; args.append(self.expression())
                self.consume('RPAREN')
                expr = self.call_function(expr, args)
            elif self.cur()['kind'] == 'DOT' and isinstance(expr, dict):
                self.pos += 1; expr = expr.get(self.consume('IDENT')['value'])
            else: break
        return expr
    def primary(self):
        t = self.cur()
        if t['kind'] == 'NUMBER': self.pos += 1; return t['value']
        if t['kind'] == 'STRING': self.pos += 1; return t['value']
        if t['kind'] == 'TRUE': self.pos += 1; return True
        if t['kind'] == 'FALSE': self.pos += 1; return False
        if t['kind'] == 'NONE': self.pos += 1; return None
        if t['kind'] == 'IDENT':
            self.pos += 1; name = t['value']
            if name in self.vars: return self.vars[name]
            if name in self.functions: return name
            raise Exception(f"نام موجود نہیں: {name}")
        if t['kind'] == 'LPAREN':
            self.pos += 1; v = self.expression(); self.consume('RPAREN'); return v
        raise Exception(f"لائن {t['line']}: غیر متوقع علامت {t['value']}")

def run_code(code):
    try:
        it = Interp(); it.tokens = tokenize(code); it.parse()
        return '\n'.join(it.output)
    except Exception as e:
        return '⛔ ' + str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python nexuslang_v11.py <file.nx>"); sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        code = f.read()
    print(run_code(code))
