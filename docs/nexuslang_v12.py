#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusLang v12 - Full Implementation
Classes, Arrays, For Loops, Try/Catch, Stdlib
اردو · Español · English
"""

import sys, re

# ============================================================================
# KEYWORDS
# ============================================================================
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
    'درآمد':'IMPORT','importar':'IMPORT','import':'IMPORT',
}

# ============================================================================
# TOKENS
# ============================================================================
TOKENS = [
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('NUMBER', r'\d+(?:\.\d+)?'),
    ('IDENT', r'[A-Za-z_\u0600-\u06FF][A-Za-z0-9_\u0600-\u06FF]*'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('OP2', r'==|!=|<=|>=|&&|\|\|'),
    ('ASSIGN', r'='),
    ('OP1', r'[+\-*/%<>!]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r','),
    ('SEMI', r';'),
    ('DOT', r'\.'),
    ('WS', r'\s+'),
]

def tokenize(code):
    code = re.sub(r'//[^\n]*', '', code)
    rx = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKENS))
    tokens = []
    line = 1
    for m in rx.finditer(code):
        kind = m.lastgroup
        val = m.group()
        if kind == 'WS':
            line += val.count('\n')
            continue
        if kind == 'IDENT' and val in KW:
            kind = KW[val]
        elif kind == 'NUMBER':
            val = float(val) if '.' in val else int(val)
        elif kind == 'STRING':
            val = val[1:-1]
        elif kind in ('OP1', 'OP2'):
            kind = 'OP'
        tokens.append({'kind': kind, 'value': val, 'line': line})
    tokens.append({'kind': 'EOF', 'value': None, 'line': line})
    return tokens

# ============================================================================
# EXCEPTIONS
# ============================================================================
class ReturnExc(Exception):
    def __init__(self, v): self.v = v
class BreakExc(Exception): pass
class ContExc(Exception): pass
class NexusError(Exception):
    def __init__(self, msg, line):
        self.msg = msg
        self.line = line
        super().__init__(f"\n⛔ غلطی لائن {line}: {msg}\nError en línea {line}: {msg}\nLine {line} error: {msg}")

# ============================================================================
# STANDARD LIBRARY
# ============================================================================
STDLIB = {
    'input': lambda: input(),
    'len': lambda x: len(x) if isinstance(x, (str, list)) else 0,
    'str': str,
    'int': lambda x: int(x) if x else 0,
    'float': float,
    'range': lambda *args: list(range(*args)),
    'print': print,
}

# ============================================================================
# INTERPRETER
# ============================================================================
class Interp:
    def __init__(self):
        self.vars = {}
        self.functions = {}
        self.classes = {}
        self.tokens = []
        self.pos = 0
        self.output = []
        self.scope = {}
        
    def cur(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else {'kind':'EOF','value':None,'line':0}
    
    def peek(self, n=1):
        return self.tokens[self.pos+n] if self.pos+n < len(self.tokens) else {'kind':'EOF','value':None,'line':0}
    
    def consume(self, kind=None):
        t = self.cur()
        if kind and t['kind'] != kind:
            raise NexusError(f"متوقع {kind} مگر ملا {t['kind']}", t['line'])
        self.pos += 1
        return t
    
    def parse(self):
        while self.cur()['kind'] != 'EOF':
            self.statement()
    
    def statement(self):
        k = self.cur()['kind']
        if k == 'VAR':
            self.var_decl()
        elif k == 'PRINT':
            self.print_stmt()
        elif k == 'IF':
            self.if_stmt()
        elif k == 'WHILE':
            self.while_stmt()
        elif k == 'FOR':
            self.for_stmt()
        elif k == 'DEF':
            self.func_decl()
        elif k == 'CLASS':
            self.class_decl()
        elif k == 'RETURN':
            self.return_stmt()
        elif k == 'TRY':
            self.try_stmt()
        elif k == 'IMPORT':
            self.import_stmt()
        elif k == 'BREAK':
            self.consume('BREAK')
            self.eat_semi()
            raise BreakExc()
        elif k == 'CONTINUE':
            self.consume('CONTINUE')
            self.eat_semi()
            raise ContExc()
        elif k == 'LBRACE':
            self.block()
        elif k == 'SEMI':
            self.pos += 1
        elif k == 'IDENT' and self.peek()['kind'] == 'ASSIGN':
            name = self.consume('IDENT')['value']
            self.consume('ASSIGN')
            v = self.expression()
            self.eat_semi()
            if name in self.vars:
                self.vars[name] = v
            else:
                raise NexusError(f"متغیر {name} پہلے سے موجود نہیں", self.cur()['line'])
        else:
            self.expression()
            self.eat_semi()
    
    def eat_semi(self):
        if self.cur()['kind'] == 'SEMI':
            self.pos += 1
    
    def var_decl(self):
        self.consume('VAR')
        name = self.consume('IDENT')['value']
        self.consume('ASSIGN')
        v = self.expression()
        self.eat_semi()
        self.vars[name] = v
    
    def print_stmt(self):
        self.consume('PRINT')
        v = self.expression()
        self.eat_semi()
        self.output.append(str(v))
    
    def skip_block(self):
        self.consume('LBRACE')
        d = 1
        while d > 0 and self.cur()['kind'] != 'EOF':
            if self.cur()['kind'] == 'LBRACE':
                d += 1
            elif self.cur()['kind'] == 'RBRACE':
                d -= 1
            self.pos += 1
    
    def block(self):
        self.consume('LBRACE')
        while self.cur()['kind'] != 'RBRACE' and self.cur()['kind'] != 'EOF':
            self.statement()
        self.consume('RBRACE')
    
    def if_stmt(self):
        self.consume('IF')
        self.consume('LPAREN')
        cond = self.expression()
        self.consume('RPAREN')
        if cond:
            self.block()
            if self.cur()['kind'] == 'ELSE':
                self.consume('ELSE')
                self.skip_block()
        else:
            self.skip_block()
            if self.cur()['kind'] == 'ELSE':
                self.consume('ELSE')
                self.block()
    
    def while_stmt(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        cond_start = self.pos
        self.expression()
        self.consume('RPAREN')
        body_start = self.pos
        self.skip_block()
        body_end = self.pos
        while True:
            self.pos = cond_start
            cond = self.expression()
            self.consume('RPAREN')
            if not cond:
                break
            self.pos = body_start
            try:
                self.block()
            except BreakExc:
                break
            except ContExc:
                pass
        self.pos = body_end
    
    def for_stmt(self):
        self.consume('FOR')
        self.consume('LPAREN')
        
        # Init - NO consumir SEMI manualmente
        if self.cur()['kind'] == 'VAR':
            self.consume('VAR')
            name = self.consume('IDENT')['value']
            self.consume('ASSIGN')
            v = self.expression()
            self.vars[name] = v
        elif self.cur()['kind'] == 'IDENT' and self.peek()['kind'] == 'ASSIGN':
            name = self.consume('IDENT')['value']
            self.consume('ASSIGN')
            v = self.expression()
            self.vars[name] = v
        
        # Consumir primer SEMI
        if self.cur()['kind'] == 'SEMI':
            self.pos += 1
        
        # Condition
        cond_start = self.pos
        cond_expr = self.expression()
        
        # Consumir segundo SEMI
        if self.cur()['kind'] == 'SEMI':
            self.pos += 1
        
        # Increment
        inc_start = self.pos
        self.expression()
        
        # Consumir RPAREN
        self.consume('RPAREN')
        
        body_start = self.pos
        self.skip_block()
        body_end = self.pos
        
        # Execute loop
        while True:
            self.pos = cond_start
            cond = self.expression()
            if self.cur()['kind'] == 'SEMI':
                self.pos += 1
            if not cond:
                break
            self.pos = body_start
            try:
                self.block()
            except BreakExc:
                break
            except ContExc:
                pass
            self.pos = inc_start
            self.expression()
        self.pos = body_end
    
    def func_decl(self):
        self.consume('DEF')
        name = self.consume('IDENT')['value']
        self.consume('LPAREN')
        params = []
        if self.cur()['kind'] != 'RPAREN':
            params.append(self.consume('IDENT')['value'])
            while self.cur()['kind'] == 'COMMA':
                self.pos += 1
                params.append(self.consume('IDENT')['value'])
        self.consume('RPAREN')
        start = self.pos
        self.skip_block()
        self.functions[name] = {'params': params, 'start': start, 'end': self.pos}
    
    def class_decl(self):
        self.consume('CLASS')
        name = self.consume('IDENT')['value']
        self.consume('LBRACE')
        methods = {}
        while self.cur()['kind'] != 'RBRACE' and self.cur()['kind'] != 'EOF':
            if self.cur()['kind'] == 'DEF':
                self.consume('DEF')
                mname = self.consume('IDENT')['value']
                self.consume('LPAREN')
                params = []
                if self.cur()['kind'] != 'RPAREN':
                    params.append(self.consume('IDENT')['value'])
                    while self.cur()['kind'] == 'COMMA':
                        self.pos += 1
                        params.append(self.consume('IDENT')['value'])
                self.consume('RPAREN')
                start = self.pos
                self.skip_block()
                methods[mname] = {'params': params, 'start': start, 'end': self.pos}
            else:
                self.pos += 1
        self.classes[name] = methods
    
    def return_stmt(self):
        self.consume('RETURN')
        v = self.expression()
        self.eat_semi()
        raise ReturnExc(v)
    
    def import_stmt(self):
        self.consume('IMPORT')
        mod = self.consume('IDENT')['value']
        self.eat_semi()
        if mod in STDLIB:
            self.vars[mod] = STDLIB[mod]
        else:
            raise NexusError(f"ماڈیول {mod} موجود نہیں", self.cur()['line'])
    
    def try_stmt(self):
        self.consume('TRY')
        self.consume('LBRACE')
        try_start = self.pos
        brace_count = 1
        while brace_count > 0 and self.cur()['kind'] != 'EOF':
            if self.cur()['kind'] == 'LBRACE':
                brace_count += 1
            elif self.cur()['kind'] == 'RBRACE':
                brace_count -= 1
            self.pos += 1
        try_end = self.pos - 1
        
        if self.cur()['kind'] == 'CATCH':
            self.consume('CATCH')
            self.consume('LPAREN')
            exc_var = self.consume('IDENT')['value']
            self.consume('RPAREN')
            self.consume('LBRACE')
            catch_start = self.pos
            brace_count = 1
            while brace_count > 0 and self.cur()['kind'] != 'EOF':
                if self.cur()['kind'] == 'LBRACE':
                    brace_count += 1
                elif self.cur()['kind'] == 'RBRACE':
                    brace_count -= 1
                self.pos += 1
            catch_end = self.pos - 1
            
            # Execute try block
            save_pos = self.pos
            self.pos = try_start
            try:
                while self.pos < try_end:
                    self.statement()
            except Exception as e:
                self.vars[exc_var] = str(e)
                self.pos = catch_start
                while self.pos < catch_end:
                    self.statement()
            self.pos = save_pos
    
    def call_function(self, name, args):
        if name in self.functions:
            f = self.functions[name]
            if len(args) != len(f['params']):
                raise NexusError(f"Function {name} expects {len(f['params'])} args, got {len(args)}", 0)
            old = self.vars.copy()
            for p, a in zip(f['params'], args):
                self.vars[p] = a
            save = self.pos
            self.pos = f['start']
            result = None
            try:
                self.block()
            except ReturnExc as e:
                result = e.v
            self.vars = old
            self.pos = save
            return result
        elif name in self.classes:
            # Constructor call
            cls = self.classes[name]
            obj = {'__class__': name, '__data__': {}}
            if '__init__' in cls:
                init = cls['__init__']
                if len(args) != len(init['params']):
                    raise NexusError(f"Constructor expects {len(init['params'])} args", 0)
                old = self.vars.copy()
                self.vars['self'] = obj
                for p, a in zip(init['params'], args):
                    self.vars[p] = a
                save = self.pos
                self.pos = init['start']
                brace = 1
                while brace > 0 and self.pos < init['end']:
                    if self.cur()['kind'] == 'LBRACE':
                        brace += 1
                    elif self.cur()['kind'] == 'RBRACE':
                        brace -= 1
                    if brace > 0:
                        self.statement()
                self.vars = old
                self.pos = save
            return obj
        else:
            raise NexusError(f"Function {name} not defined", 0)
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        left = self.or_expr()
        if self.cur()['kind'] == 'ASSIGN':
            self.pos += 1
            right = self.assignment()
            if isinstance(left, str) and left in self.vars:
                self.vars[left] = right
                return right
            elif isinstance(left, dict) and '__class__' in left and 'prop' in left:
                left['__data__'][left['prop']] = right
                return right
            elif isinstance(left, list) and 'index' in left:
                left[left['index']] = right
                return right
        return left
    
    def or_expr(self):
        left = self.and_expr()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] == '||':
            self.pos += 1
            left = left or self.and_expr()
        return left
    
    def and_expr(self):
        left = self.equality()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] == '&&':
            self.pos += 1
            left = left and self.equality()
        return left
    
    def equality(self):
        left = self.comparison()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('==', '!='):
            op = self.consume()['value']
            right = self.comparison()
            left = (left == right) if op == '==' else (left != right)
        return left
    
    def comparison(self):
        left = self.term()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('<', '>', '<=', '>='):
            op = self.consume()['value']
            right = self.term()
            if op == '<': left = left < right
            elif op == '>': left = left > right
            elif op == '<=': left = left <= right
            else: left = left >= right
        return left
    
    def term(self):
        left = self.factor()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('+', '-'):
            op = self.consume()['value']
            right = self.factor()
            if op == '+':
                left = str(left) + str(right) if isinstance(left, str) or isinstance(right, str) else left + right
            else:
                left = left - right
        return left
    
    def factor(self):
        left = self.unary()
        while self.cur()['kind'] == 'OP' and self.cur()['value'] in ('*', '/', '%'):
            op = self.consume()['value']
            right = self.unary()
            if op == '*': left = left * right
            elif op == '/': left = left / right
            else: left = left % right
        return left
    
    def unary(self):
        if self.cur()['kind'] == 'OP' and self.cur()['value'] in ('-', '!'):
            op = self.consume()['value']
            v = self.unary()
            return -v if op == '-' else (not v)
        return self.call()
    
    def call(self):
        expr = self.primary()
        while True:
            if self.cur()['kind'] == 'LPAREN':
                self.pos += 1
                args = []
                if self.cur()['kind'] != 'RPAREN':
                    args.append(self.expression())
                    while self.cur()['kind'] == 'COMMA':
                        self.pos += 1
                        args.append(self.expression())
                self.consume('RPAREN')
                if isinstance(expr, str) and expr in self.functions:
                    expr = self.call_function(expr, args)
                elif isinstance(expr, str) and expr in STDLIB:
                    expr = STDLIB[expr](*args)
                elif isinstance(expr, dict) and '__class__' in expr and 'name' in expr:
                    # Method call
                    cls = self.classes[expr['__class__']]
                    mname = expr['name']
                    if mname in cls:
                        m = cls[mname]
                        if len(args) != len(m['params']):
                            raise NexusError(f"Method {mname} expects {len(m['params'])} args", 0)
                        old = self.vars.copy()
                        self.vars['self'] = expr
                        for p, a in zip(m['params'], args):
                            self.vars[p] = a
                        save = self.pos
                        self.pos = m['start']
                        result = None
                        try:
                            brace = 1
                            while brace > 0 and self.pos < m['end']:
                                if self.cur()['kind'] == 'LBRACE':
                                    brace += 1
                                elif self.cur()['kind'] == 'RBRACE':
                                    brace -= 1
                                if brace > 0:
                                    self.statement()
                        except ReturnExc as e:
                            result = e.v
                        self.vars = old
                        self.pos = save
                        expr = result
                    else:
                        raise NexusError(f"Method {mname} not found", 0)
                else:
                    raise NexusError(f"{expr} is not callable", 0)
            elif self.cur()['kind'] == 'DOT' and isinstance(expr, dict) and '__class__' in expr:
                self.pos += 1
                mname = self.consume('IDENT')['value']
                expr = {'__class__': expr['__class__'], 'name': mname}
            elif self.cur()['kind'] == 'LBRACKET' and isinstance(expr, list):
                self.pos += 1
                idx = self.expression()
                self.consume('RBRACKET')
                if isinstance(idx, int) and 0 <= idx < len(expr):
                    expr = expr[idx]
                else:
                    raise NexusError(f"Index {idx} out of bounds", 0)
            else:
                break
        return expr
    
    def primary(self):
        t = self.cur()
        if t['kind'] == 'NUMBER':
            self.pos += 1
            return t['value']
        if t['kind'] == 'STRING':
            self.pos += 1
            return t['value']
        if t['kind'] == 'TRUE':
            self.pos += 1
            return True
        if t['kind'] == 'FALSE':
            self.pos += 1
            return False
        if t['kind'] == 'NONE':
            self.pos += 1
            return None
        if t['kind'] == 'LBRACKET':
            self.pos += 1
            arr = []
            if self.cur()['kind'] != 'RBRACKET':
                arr.append(self.expression())
                while self.cur()['kind'] == 'COMMA':
                    self.pos += 1
                    arr.append(self.expression())
            self.consume('RBRACKET')
            return arr
        if t['kind'] == 'NEW':
            self.pos += 1
            cname = self.consume('IDENT')['value']
            if cname in self.classes:
                return {'__class__': cname}
            else:
                raise NexusError(f"Class {cname} not defined", t['line'])
        if t['kind'] == 'IDENT':
            self.pos += 1
            name = t['value']
            if name in self.vars:
                return self.vars[name]
            if name in self.functions:
                return name
            raise NexusError(f"Variable {name} not defined", t['line'])
        if t['kind'] == 'LPAREN':
            self.pos += 1
            v = self.expression()
            self.consume('RPAREN')
            return v
        raise NexusError(f"Unexpected token: {t['value']}", t['line'])

def run_code(code):
    try:
        it = Interp()
        it.tokens = tokenize(code)
        it.parse()
        return '\n'.join(it.output)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python nexuslang_v12.py <file.nx>")
        sys.exit(1)
    with open(sys.argv[1], encoding='utf-8') as f:
        code = f.read()
    print(run_code(code))
