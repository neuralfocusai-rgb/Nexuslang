#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, json, os

# ==========================================
# 1. CARGA DINÁMICA DE LANGUAGE PACKS
# ==========================================
LANG_PACKS = {}
LANG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang_packs')

def load_lang_packs():
    if not os.path.exists(LANG_DIR):
        print(f"⚠️ Carpeta '{LANG_DIR}' no encontrada. Usando keywords por defecto.")
        return
    for filename in os.listdir(LANG_DIR):
        if filename.endswith('.json'):
            lang_name = filename.replace('.json', '')
            filepath = os.path.join(LANG_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    pack = json.load(f)
                    LANG_PACKS[lang_name] = pack.get('keywords', {})
            except Exception as e:
                print(f"⚠️ Error cargando {filename}: {e}")

load_lang_packs()

# Keywords base (Inglés + Español + Urdu/Turco esenciales)
DEFAULT_KW = {
    'var': 'VAR', 'variable': 'VAR', 'متغیر': 'VAR',
    'print': 'PRINT', 'escribir': 'PRINT', 'لکھو': 'PRINT', 'yazdır': 'PRINT', 'imprimir': 'PRINT',
    'if': 'IF', 'si': 'IF', 'اگر': 'IF', 'eğer': 'IF',
    'else': 'ELSE', 'sino': 'ELSE', 'ورنہ': 'ELSE', 'yoksa': 'ELSE',
    'while': 'WHILE', 'mientras': 'WHILE', 'جبکہ': 'WHILE', 'sürece': 'WHILE',
    'for': 'FOR', 'para': 'FOR', 'برائے': 'FOR',
    'def': 'DEF', 'function': 'DEF', 'funcion': 'DEF', 'طریقہ': 'DEF', 'fonksiyon': 'DEF',
    'return': 'RETURN', 'retornar': 'RETURN', 'واپس': 'RETURN', 'döndür': 'RETURN',
    'class': 'CLASS', 'clase': 'CLASS', 'کلاس': 'CLASS', 'sınıf': 'CLASS',
    'self': 'SELF', 'esto': 'SELF', 'خود': 'SELF', 'kendisi': 'SELF',
    'new': 'NEW', 'nuevo': 'NEW', 'نیا': 'NEW', 'yeni': 'NEW',
    'try': 'TRY', 'intentar': 'TRY', 'کوشش': 'TRY', 'dene': 'TRY',
    'catch': 'CATCH', 'capturar': 'CATCH', 'پکڑو': 'CATCH', 'yakala': 'CATCH',
    'break': 'BREAK', 'romper': 'BREAK', 'توڑو': 'BREAK', 'kır': 'BREAK',
    'continue': 'CONTINUE', 'continuar': 'CONTINUE', 'جاری': 'CONTINUE', 'devam': 'CONTINUE',
    'true': 'TRUE', 'verdadero': 'TRUE', 'صحيح': 'TRUE', 'doğru': 'TRUE',
    'false': 'FALSE', 'falso': 'FALSE', 'غلط': 'FALSE', 'yanlış': 'FALSE',
    'null': 'NONE', 'none': 'NONE', 'nulo': 'NONE', 'خالی': 'NONE', 'boş': 'NONE',
    'import': 'IMPORT', 'importar': 'IMPORT', 'درآمد': 'IMPORT', 'içe_aktar': 'IMPORT',
}

# Fusionar: Los JSON tienen prioridad
KEYWORD_MAP = DEFAULT_KW.copy()
for lang, keywords in LANG_PACKS.items():
    KEYWORD_MAP.update(keywords)

print(f"✅ NexusLang v12 cargado. {len(KEYWORD_MAP)} keywords reconocidas ({len(LANG_PACKS)} packs extra).")

# ==========================================
# 2. TOKENS (Regex actualizado para Unicode completo)
# ==========================================
TOKENS = [
    ('STRING', r'"[^"]*"|\'[^\']*\''),
    ('NUMBER', r'\d+(?:\.\d+)?'),
    ('COMMA', r',|،'),
    ('SEMI', r';|؛'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('OP2', r'==|!=|<=|>=|&&|\|\|'),
    ('ASSIGN', r'='),
    ('OP1', r'[+\-*/%<>!]'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('DOT', r'\.'),
    ('IDENT', r'[^\W\d_]\w*'),
    ('WS', r'\s+'),
]

# ==========================================
# 3. TOKENIZER
# ==========================================
def tokenize(code):
    code = re.sub(r'//[^\n]*', '', code)
    code = re.sub(r'#[^\n]*', '', code)
    rx = re.compile('|'.join(f'(?P<{n}>{p})' for n, p in TOKENS))
    tokens = []
    line = 1
    for m in rx.finditer(code):
        kind = m.lastgroup
        val = m.group()
        if kind == 'WS':
            line += val.count('\n')
            continue
        if kind == 'IDENT' and val in KEYWORD_MAP:
            kind = KEYWORD_MAP[val]
        elif kind == 'NUMBER':
            val = float(val) if '.' in val else int(val)
        elif kind == 'STRING':
            val = val[1:-1]
        elif kind in ('OP1', 'OP2'):
            kind = 'OP'
        tokens.append({'kind': kind, 'value': val, 'line': line})
    tokens.append({'kind': 'EOF', 'value': None, 'line': line})
    return tokens

# ==========================================
# 4. EXCEPCIONES
# ==========================================
class ReturnExc(Exception):
    def __init__(self, v): self.v = v
class BreakExc(Exception): pass
class ContExc(Exception): pass
class NexusError(Exception):
    def __init__(self, msg, line):
        self.msg = msg
        self.line = line
        super().__init__(f"\n⛔ غلطی لائن {line}: {msg}\nError en línea {line}: {msg}\nLine {line} error: {msg}")

# ==========================================
# 5. STDLIB
# ==========================================
STDLIB = {
    'input': lambda: input(),
    'len': lambda x: len(x) if isinstance(x, (str, list)) else 0,
    'str': str,
    'int': lambda x: int(x) if x else 0,
    'float': float,
    'range': lambda *args: list(range(*args)),
    'print': print,
}

# ==========================================
# 6. INTÉRPRETE
# ==========================================
class Interp:
    def __init__(self):
        self.vars = {}
        self.functions = {}
        self.classes = {}
        self.tokens = []
        self.pos = 0
        self.output = []
        
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
        elif k == 'SELF' and self.peek()['kind'] == 'DOT':
            self.consume('SELF')
            self.consume('DOT')
            prop = self.consume('IDENT')['value']
            self.consume('ASSIGN')
            v = self.expression()
            self.eat_semi()
            obj = self.vars.get('self')
            if isinstance(obj, dict):
                obj['__data__'][prop] = v
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
        print(str(v))
    
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
        if self.cur()['kind'] == 'SEMI':
            self.pos += 1
        cond_start = self.pos
        self.expression()
        if self.cur()['kind'] == 'SEMI':
            self.pos += 1
        inc_start = self.pos
        self.expression()
        self.consume('RPAREN')
        body_start = self.pos
        self.skip_block()
        body_end = self.pos
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
            cls = self.classes[name]
            obj = {'__class__': name, '__data__': {}}
            if 'init' in cls:
                init = cls['init']
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
                elif isinstance(expr, str) and expr in self.classes:
                    expr = self.call_function(expr, args)
                elif isinstance(expr, dict) and '__class__' in expr and 'name' in expr:
                    cls = self.classes[expr['__class__']]
                    mname = expr['name']
                    if mname in cls:
                        m = cls[mname]
                        if len(args) != len(m['params']):
                            raise NexusError(f"Method {mname} expects {len(m['params'])} args", 0)
                        old = self.vars.copy()
                        if 'obj' in expr:
                            self.vars['self'] = expr['obj']
                        else:
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
                if self.cur()['kind'] == 'LPAREN':
                    expr = {'__class__': expr['__class__'], 'name': mname, 'obj': expr}
                else:
                    if mname in expr['__data__']:
                        expr = expr['__data__'][mname]
                    else:
                        raise NexusError(f"Property {mname} not found", 0)
            elif self.cur()['kind'] == 'LBRACKET' and isinstance(expr, (list, str)):
                self.pos += 1
                idx = self.expression()
                self.consume('RBRACKET')
                if isinstance(expr, list):
                    expr = expr[idx]
                else:
                    expr = expr[idx]
            else:
                break
        return expr
    
    def primary(self):
        t = self.cur()
        if t['kind'] == 'NUMBER':
            self.pos += 1
            return t['value']
        elif t['kind'] == 'STRING':
            self.pos += 1
            return t['value']
        elif t['kind'] == 'TRUE':
            self.pos += 1
            return True
        elif t['kind'] == 'FALSE':
            self.pos += 1
            return False
        elif t['kind'] == 'NONE':
            self.pos += 1
            return None
        elif t['kind'] == 'IDENT':
            self.pos += 1
            name = t['value']
            if name in self.vars:
                return self.vars[name]
            elif name in self.functions:
                return name
            elif name in self.classes:
                return {'__class__': name}
            else:
                raise NexusError(f"Variable {name} not defined", t['line'])
        elif t['kind'] == 'LPAREN':
            self.pos += 1
            v = self.expression()
            self.consume('RPAREN')
            return v
        elif t['kind'] == 'LBRACKET':
            self.pos += 1
            arr = []
            if self.cur()['kind'] != 'RBRACKET':
                arr.append(self.expression())
                while self.cur()['kind'] == 'COMMA':
                    self.pos += 1
                    arr.append(self.expression())
            self.consume('RBRACKET')
            return arr
        else:
            raise NexusError(f"Unexpected token: {t['kind']} ({t['value']})", t['line'])

# ==========================================
# 7. EJECUCIÓN
# ==========================================
def run_file(filepath):
    if not os.path.exists(filepath):
        print(f" Archivo no encontrado: {filepath}")
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    tokens = tokenize(code)
    interp = Interp()
    interp.tokens = tokens
    try:
        interp.parse()
    except NexusError as e:
        print(e)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python3 nexuslang_v12.py <archivo.nx>")
        print("Ejemplo: python3 nexuslang_v12.py examples/urdu/001_hello.nx")
        sys.exit(1)
    run_file(sys.argv[1])
