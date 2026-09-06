#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NexusLang v11 - Trilingual Programming Language
اردو · Español · English
"""

import sys
import re
import json

# ============================================================================
# PALABRAS CLAVE / KEYWORDS / کلیدی الفاظ
# ============================================================================
KW = {
    'متغیر': 'VAR', 'variable': 'VAR', 'var': 'VAR',
    'لکھو': 'PRINT', 'escribir': 'PRINT', 'print': 'PRINT',
    'اگر': 'IF', 'si': 'IF', 'if': 'IF',
    'ورنہ': 'ELSE', 'sino': 'ELSE', 'else': 'ELSE',
    'جبکہ': 'WHILE', 'mientras': 'WHILE', 'while': 'WHILE',
    'برائے': 'FOR', 'para': 'FOR', 'for': 'FOR',
    'طریقہ': 'DEF', 'funcion': 'DEF', 'def': 'DEF', 'function': 'DEF',
    'واپس': 'RETURN', 'retornar': 'RETURN', 'return': 'RETURN',
    'کلاس': 'CLASS', 'clase': 'CLASS', 'class': 'CLASS',
    'خود': 'SELF', 'esto': 'SELF', 'self': 'SELF',
    'نیا': 'NEW', 'nuevo': 'NEW', 'new': 'NEW',
    'کوشش': 'TRY', 'intentar': 'TRY', 'try': 'TRY',
    'پکڑو': 'CATCH', 'capturar': 'CATCH', 'catch': 'CATCH',
    'توڑو': 'BREAK', 'romper': 'BREAK', 'break': 'BREAK',
    'جاری': 'CONTINUE', 'continuar': 'CONTINUE', 'continue': 'CONTINUE',
    'صحيح': 'TRUE', 'verdadero': 'TRUE', 'true': 'TRUE',
    'غلط': 'FALSE', 'falso': 'FALSE', 'false': 'FALSE',
    'خالی': 'NONE', 'nulo': 'NONE', 'null': 'NONE', 'none': 'NONE',
    'درآمد': 'IMPORT', 'importar': 'IMPORT', 'import': 'IMPORT',
}

# ============================================================================
# TOKENS
# ============================================================================
TOKENS = {
    'VAR': r'متغیر|variable|var',
    'PRINT': r'لکھو|escribir|print',
    'IF': r'اگر|si|if',
    'ELSE': r'ورنہ|sino|else',
    'WHILE': r'جبکہ|mientras|while',
    'FOR': r'برائے|para|for',
    'DEF': r'طریقہ|funcion|def|function',
    'RETURN': r'واپس|retornar|return',
    'CLASS': r'کلاس|clase|class',
    'SELF': r'خود|esto|self',
    'NEW': r'نیا|nuevo|new',
    'TRY': r'کوشش|intentar|try',
    'CATCH': r'پکڑو|capturar|catch',
    'BREAK': r'توڑو|romper|break',
    'CONTINUE': r'جاری|continuar|continue',
    'TRUE': r'صحيح|verdadero|true',
    'FALSE': r'غلط|falso|false',
    'NONE': r'خالی|nulo|null|none',
    'IMPORT': r'درآمد|importar|import',
    'IDENT': r'[a-zA-Z_\u0600-\u06FF][a-zA-Z0-9_\u0600-\u06FF]*',
    'NUMBER': r'\d+(\.\d+)?',
    'STRING': r'"[^"]*"|\'[^\']*\'',
    'OP': r'\+\+|--|\*\*|//|==|!=|<=|>=|&&|\|\||[+\-*/%<>=!&|]',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'LBRACKET': r'\[',
    'RBRACKET': r'\]',
    'COMMA': r',',
    'SEMI': r';',
    'DOT': r'\.',
    'ASSIGN': r'=',
    'COLON': r':',
    'NEWLINE': r'\n',
    'COMMENT': r'//[^\n]*|/\*.*?\*/',
    'SKIP': r'[ \t]+',
}

# ============================================================================
# TOKENIZER
# ============================================================================
def tokenize(code):
    tokens = []
    pos = 0
    line = 1
    
    # Pattern combinado
    pattern = '|'.join(f'(?P<{name}>{regex})' for name, regex in TOKENS.items())
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
    
    for match in regex.finditer(code):
        kind = match.lastgroup
        value = match.group()
        
        if kind == 'NEWLINE':
            line += 1
        elif kind == 'COMMENT':
            pass  # Skip comments
        elif kind == 'SKIP':
            pass  # Skip whitespace
        elif kind == 'IDENT' and value in KW:
            kind = KW[value]
        elif kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'STRING':
            value = value[1:-1]  # Remove quotes
        
        if kind not in ('SKIP', 'COMMENT', 'NEWLINE'):
            tokens.append({'kind': kind, 'value': value, 'line': line})
    
    tokens.append({'kind': 'EOF', 'value': None, 'line': line})
    return tokens

# ============================================================================
# PARSER & INTERPRETER
# ============================================================================
class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}
        self.classes = {}
        self.pos = 0
        self.tokens = []
        self.output = []
    
    def error(self, msg, line=None):
        if line:
            raise Exception(f"⛔ غلطی لائن {line}: {msg}")
        raise Exception(f"⛔ غلطی: {msg}")
    
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else {'kind': 'EOF'}
    
    def consume(self, kind=None):
        tok = self.current()
        if kind and tok['kind'] != kind:
            self.error(f"متوقع {kind} مگر ملا {tok['kind']}", tok['line'])
        self.pos += 1
        return tok
    
    def parse(self):
        while self.current()['kind'] != 'EOF':
            self.statement()
    
    def statement(self):
        tok = self.current()
        
        if tok['kind'] == 'VAR':
            self.var_decl()
        elif tok['kind'] == 'PRINT':
            self.print_stmt()
        elif tok['kind'] == 'IF':
            self.if_stmt()
        elif tok['kind'] == 'WHILE':
            self.while_stmt()
        elif tok['kind'] == 'FOR':
            self.for_stmt()
        elif tok['kind'] == 'DEF':
            self.func_decl()
        elif tok['kind'] == 'CLASS':
            self.class_decl()
        elif tok['kind'] == 'RETURN':
            self.return_stmt()
        elif tok['kind'] == 'TRY':
            self.try_stmt()
        elif tok['kind'] == 'BREAK':
            self.consume('BREAK')
            self.consume('SEMI')
        elif tok['kind'] == 'CONTINUE':
            self.consume('CONTINUE')
            self.consume('SEMI')
        elif tok['kind'] == 'LBRACE':
            self.block()
        elif tok['kind'] == 'SEMI':
            self.consume('SEMI')
        else:
            # Expression statement
            self.expression()
            if self.current()['kind'] == 'SEMI':
                self.consume('SEMI')
    
    def var_decl(self):
        self.consume('VAR')
        name = self.consume('IDENT')['value']
        self.consume('ASSIGN')
        value = self.expression()
        self.consume('SEMI')
        self.vars[name] = value
    
    def print_stmt(self):
        self.consume('PRINT')
        value = self.expression()
        self.consume('SEMI')
        self.output.append(str(value))
    
    def if_stmt(self):
        self.consume('IF')
        self.consume('LPAREN')
        cond = self.expression()
        self.consume('RPAREN')
        
        if cond:
            self.block()
            if self.current()['kind'] == 'ELSE':
                self.consume('ELSE')
                self.block()
        else:
            self.block()
            if self.current()['kind'] == 'ELSE':
                self.consume('ELSE')
                self.consume('LBRACE')
                while self.current()['kind'] != 'RBRACE':
                    self.statement()
                self.consume('RBRACE')
    
    def while_stmt(self):
        self.consume('WHILE')
        self.consume('LPAREN')
        
        while True:
            # Re-evaluate condition
            pos_save = self.pos
            cond = self.expression()
            self.consume('RPAREN')
            
            if not cond:
                break
            
            self.block()
            self.pos = pos_save  # Reset to re-evaluate condition
    
    def for_stmt(self):
        self.consume('FOR')
        self.consume('LPAREN')
        
        # Init
        if self.current()['kind'] == 'VAR':
            self.var_decl()
        else:
            self.expression()
            self.consume('SEMI')
        
        # Condition
        cond_start = self.pos
        cond = self.expression()
        self.consume('SEMI')
        
        # Increment
        inc_start = self.pos
        
        self.block()
        
        # This is simplified - full implementation would loop
    
    def func_decl(self):
        self.consume('DEF')
        name = self.consume('IDENT')['value']
        self.consume('LPAREN')
        
        params = []
        if self.current()['kind'] != 'RPAREN':
            params.append(self.consume('IDENT')['value'])
            while self.current()['kind'] == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('IDENT')['value'])
        
        self.consume('RPAREN')
        self.consume('LBRACE')
        
        # Save function body
        body_start = self.pos
        brace_count = 1
        while brace_count > 0 and self.current()['kind'] != 'EOF':
            if self.current()['kind'] == 'LBRACE':
                brace_count += 1
            elif self.current()['kind'] == 'RBRACE':
                brace_count -= 1
            self.pos += 1
        
        body_end = self.pos - 1
        self.functions[name] = {'params': params, 'body': body_start, 'end': body_end}
    
    def class_decl(self):
        self.consume('CLASS')
        name = self.consume('IDENT')['value']
        self.consume('LBRACE')
        
        methods = {}
        while self.current()['kind'] != 'RBRACE' and self.current()['kind'] != 'EOF':
            if self.current()['kind'] == 'DEF':
                self.consume('DEF')
                mname = self.consume('IDENT')['value']
                self.consume('LPAREN')
                
                params = []
                if self.current()['kind'] != 'RPAREN':
                    params.append(self.consume('IDENT')['value'])
                    while self.current()['kind'] == 'COMMA':
                        self.consume('COMMA')
                        params.append(self.consume('IDENT')['value'])
                
                self.consume('RPAREN')
                self.consume('LBRACE')
                
                body_start = self.pos
                brace_count = 1
                while brace_count > 0 and self.current()['kind'] != 'EOF':
                    if self.current()['kind'] == 'LBRACE':
                        brace_count += 1
                    elif self.current()['kind'] == 'RBRACE':
                        brace_count -= 1
                    self.pos += 1
                
                methods[mname] = {'params': params, 'body_start': body_start}
            else:
                self.pos += 1
        
        self.classes[name] = methods
    
    def return_stmt(self):
        self.consume('RETURN')
        value = self.expression()
        self.consume('SEMI')
        raise ReturnException(value)
    
    def try_stmt(self):
        self.consume('TRY')
        self.consume('LBRACE')
        try:
            while self.current()['kind'] != 'RBRACE':
                self.statement()
        except Exception as e:
            if self.current()['kind'] == 'CATCH':
                self.consume('CATCH')
                self.consume('LPAREN')
                self.consume('IDENT')  # Exception variable
                self.consume('RPAREN')
                self.consume('LBRACE')
                while self.current()['kind'] != 'RBRACE':
                    self.statement()
    
    def block(self):
        self.consume('LBRACE')
        while self.current()['kind'] != 'RBRACE':
            self.statement()
        self.consume('RBRACE')
    
    def expression(self):
        return self.assignment()
    
    def assignment(self):
        left = self.or_expr()
        
        if self.current()['kind'] == 'ASSIGN':
            self.consume('ASSIGN')
            right = self.assignment()
            
            if isinstance(left, str) and left in self.vars:
                self.vars[left] = right
                return right
            elif isinstance(left, dict) and 'obj' in left and 'prop' in left:
                left['obj'][left['prop']] = right
                return right
        
        return left
    
    def or_expr(self):
        left = self.and_expr()
        while self.current()['kind'] == 'OP' and self.current()['value'] == '||':
            self.consume()
            right = self.and_expr()
            left = left or right
        return left
    
    def and_expr(self):
        left = self.equality()
        while self.current()['kind'] == 'OP' and self.current()['value'] == '&&':
            self.consume()
            right = self.equality()
            left = left and right
        return left
    
    def equality(self):
        left = self.comparison()
        
        while self.current()['kind'] == 'OP' and self.current()['value'] in ('==', '!='):
            op = self.consume()['value']
            right = self.comparison()
            if op == '==':
                left = left == right
            else:
                left = left != right
        
        return left
    
    def comparison(self):
        left = self.term()
        
        while self.current()['kind'] == 'OP' and self.current()['value'] in ('<', '>', '<=', '>='):
            op = self.consume()['value']
            right = self.term()
            if op == '<':
                left = left < right
            elif op == '>':
                left = left > right
            elif op == '<=':
                left = left <= right
            else:
                left = left >= right
        
        return left
    
    def term(self):
        left = self.factor()
        
        while self.current()['kind'] == 'OP' and self.current()['value'] in ('+', '-'):
            op = self.consume()['value']
            right = self.factor()
            if op == '+':
                left = left + right
            else:
                left = left - right
        
        return left
    
    def factor(self):
        left = self.power()
        
        while self.current()['kind'] == 'OP' and self.current()['value'] in ('*', '/', '%'):
            op = self.consume()['value']
            right = self.power()
            if op == '*':
                left = left * right
            elif op == '/':
                left = left / right
            elif op == '%':
                left = left % right
        
        return left
    
    def power(self):
        left = self.unary()
        
        if self.current()['kind'] == 'OP' and self.current()['value'] == '**':
            self.consume()
            right = self.power()
            return left ** right
        
        return left
    
    def unary(self):
        if self.current()['kind'] == 'OP' and self.current()['value'] in ('-', '!'):
            op = self.consume()['value']
            operand = self.unary()
            if op == '-':
                return -operand
            else:
                return not operand
        return self.call()
    
    def call(self):
        expr = self.primary()
        
        while True:
            if self.current()['kind'] == 'LPAREN':
                # Function call
                self.consume('LPAREN')
                args = []
                if self.current()['kind'] != 'RPAREN':
                    args.append(self.expression())
                    while self.current()['kind'] == 'COMMA':
                        self.consume('COMMA')
                        args.append(self.expression())
                self.consume('RPAREN')
                
                if isinstance(expr, str) and expr in self.functions:
                    expr = self.call_function(expr, args)
                else:
                    self.error(f"Function {expr} not defined")
            
            elif self.current()['kind'] == 'DOT':
                # Property access
                self.consume('DOT')
                prop = self.consume('IDENT')['value']
                if isinstance(expr, dict):
                    expr = expr.get(prop)
                else:
                    self.error(f"Cannot access property on {type(expr)}")
            
            else:
                break
        
        return expr
    
    def primary(self):
        tok = self.current()
        
        if tok['kind'] == 'NUMBER':
            self.consume()
            return tok['value']
        
        elif tok['kind'] == 'STRING':
            self.consume()
            return tok['value']
        
        elif tok['kind'] == 'TRUE':
            self.consume()
            return True
        
        elif tok['kind'] == 'FALSE':
            self.consume()
            return False
        
        elif tok['kind'] == 'NONE':
            self.consume()
            return None
        
        elif tok['kind'] == 'IDENT':
            self.consume()
            name = tok['value']
            
            if name in self.vars:
                return self.vars[name]
            elif name in self.functions:
                return name  # Return function name for later call
            elif name in self.classes:
                return {'class': name}
            else:
                self.error(f"Undefined variable: {name}", tok['line'])
        
        elif tok['kind'] == 'NEW':
            self.consume('NEW')
            class_name = self.consume('IDENT')['value']
            if class_name in self.classes:
                return {'__class__': class_name, '__data__': {}}
            else:
                self.error(f"Class {class_name} not defined")
        
        elif tok['kind'] == 'LPAREN':
            self.consume('LPAREN')
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        
        else:
            self.error(f"Unexpected token: {tok['kind']} {tok['value']}", tok['line'])
    
    def call_function(self, name, args):
        func = self.functions[name]
        if len(args) != len(func['params']):
            self.error(f"Function {name} expects {len(func['params'])} args")
        
        # Save current vars
        old_vars = self.vars.copy()
        
        # Set parameters
        for param, arg in zip(func['params'], args):
            self.vars[param] = arg
        
        # Execute body
        pos_save = self.pos
        self.pos = func['body']
        
        try:
            while self.pos < func['end']:
                if self.current()['kind'] == 'RETURN':
                    self.return_stmt()
                else:
                    self.statement()
            result = None
        except ReturnException as e:
            result = e.value
        
        # Restore vars
        self.vars = old_vars
        self.pos = pos_save
        
        return result

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# ============================================================================
# MAIN
# ============================================================================
def run_code(code):
    try:
        tokens = tokenize(code)
        interp = Interpreter()
        interp.tokens = tokens
        interp.parse()
        return '\n'.join(str(x) for x in interp.output)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python nexuslang_v11.py <file.nx>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        code = f.read()
    
    result = run_code(code)
    if result:
        print(result)
