import re

code = open('nexuslang_v12.py', 'r', encoding='utf-8').read()

# Reemplazar el for_stmt completo
old_for = '''    def for_stmt(self):
        self.consume('FOR')
        self.consume('LPAREN')
        
        # Init
        if self.cur()['kind'] == 'VAR':
            self.var_decl()
        elif self.cur()['kind'] == 'IDENT':
            name = self.consume('IDENT')['value']
            if self.peek()['kind'] == 'ASSIGN':
                self.consume('ASSIGN')
                v = self.expression()
                self.vars[name] = v
            self.eat_semi()
        else:
            self.expression()
            self.eat_semi()
        
        # Condition
        cond_start = self.pos
        self.expression()
        self.consume('SEMI')
        
        # Increment
        inc_start = self.pos
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
            self.pos = inc_start
            self.expression()
        self.pos = body_end'''

new_for = '''    def for_stmt(self):
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
        self.pos = body_end'''

code = code.replace(old_for, new_for)

open('nexuslang_v12.py', 'w', encoding='utf-8').write(code)
print("✅ For loop fixed")
