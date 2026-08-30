#!/usr/bin/env python3
# NexusLang Compiler — ETAPA 1: LEXER (v8.0)
import re, sys

MULTI = [('جب تک', '__UR_WHILE__'), ('آخر میں', '__UR_FINALLY__')]

KEYWORDS = {
  # ES
  'si':'if','sino':'else','mientras':'while','para':'for','hen':'in',
  'devolver':'return','funcion':'def','clase':'class','romper':'break',
  'continuar':'continue','intentar':'try','atrapar':'except','finalmente':'finally',
  'verdad':'True','falso':'False','nulo':'None','imprimir':'print','mostrar':'print',
  # EN
  'if':'if','else':'else','while':'while','for':'for','in':'in',
  'return':'return','def':'def','class':'class','break':'break',
  'continue':'continue','try':'try','except':'except','finally':'finally',
  'true':'True','false':'False','null':'None','print':'print',
  # UR
  '__UR_WHILE__':'while','__UR_FINALLY__':'finally',
  'اگر':'if','ورنہ':'else','ہر':'for','میں':'in','واپس':'return',
  'فعل':'def','کلاس':'class','توڑو':'break','جاری':'continue',
  'کوشش':'try','پکڑو':'except','درست':'True','غلط':'False',
  'خالی':'None','دکھاؤ':'print',
}

TOKEN_SPEC = [
    ('COMMENT',  r'#[^\n]*'),
    ('STRING',   r'"[^"]*"|\'[^\']*\''),
    ('NUMBER',   r'\d+(?:\.\d+)?'),
    ('IDENT',    r'[A-Za-z_\u0600-\u06FF][A-Za-z0-9_\u0600-\u06FF]*'),
    ('OP',       r'==|!=|<=|>=|&&|\|\||<|>|\+|-|\*|/|='),
    ('PUNCT',    r'[()\[\]{},:]'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]
_tok_re = re.compile('|'.join('(?P<%s>%s)' % p for p in TOKEN_SPEC))

def lex(src):
    for a, b in MULTI:
        src = src.replace(a, b)
    tokens = []
    for m in _tok_re.finditer(src):
        kind = m.lastgroup
        val = m.group()
        if kind in ('SKIP', 'COMMENT'):
            continue
        if kind == 'IDENT' and val in KEYWORDS:
            tokens.append(('KW', KEYWORDS[val]))
        elif kind == 'MISMATCH':
            raise SyntaxError('caracter inesperado: %r' % val)
        else:
            tokens.append((kind, val))
    return tokens

if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8').read()
    toks = lex(src)
    print('TOKENS:', len(toks))
    for t in toks[:20]:
        print(t)
