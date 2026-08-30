#!/usr/bin/env python3
# NexusLang Compiler — ETAPA 3+4: CODEGEN + NexusVM (v8.2/v8.3)
import sys, pickle
from nexus_parser import P, build_lines

BUILTINS = {'print': print, 'str': str, 'len': len, 'int': int, 'float': float}
OPS = {'ADD': lambda a,b: a+b, 'SUB': lambda a,b: a-b, 'MUL': lambda a,b: a*b, 'DIV': lambda a,b: a/b,
       'EQ': lambda a,b: a==b, 'NE': lambda a,b: a!=b, 'LT': lambda a,b: a<b, 'GT': lambda a,b: a>b,
       'LE': lambda a,b: a<=b, 'GE': lambda a,b: a>=b, 'AND': lambda a,b: a and b, 'OR': lambda a,b: a or b}

def gen_expr(n, out):
    t = n[0]
    if t in ('num','str','bool'): out.append(('CONST', n[1]))
    elif t == 'none': out.append(('CONST', None))
    elif t == 'ident': out.append(('LOAD', n[1]))
    elif t == 'list':
        for x in n[1]: gen_expr(x, out)
        out.append(('LIST', len(n[1])))
    elif t == 'bin':
        gen_expr(n[2], out); gen_expr(n[3], out)
        out.append(({'+':'ADD','-':'SUB','*':'MUL','/':'DIV','==':'EQ','!=':'NE','<':'LT','>':'GT','<=':'LE','>=':'GE','and':'AND','or':'OR'}[n[1]],))
    elif t == 'call':
        out.append(('LOADB', n[1]) if n[1] in BUILTINS else ('LOAD', n[1]))
        for a in n[2]: gen_expr(a, out)
        out.append(('CALL', len(n[2])))

def gen_stmt(n, out):
    t = n[0]
    if t == 'func':
        body = []
        for s in n[3]: gen_stmt(s, body)
        out.append(('MAKEFUNC', n[1], n[2], body)); out.append(('STORE', n[1]))
    elif t == 'assign': gen_expr(n[2], out); out.append(('STORE', n[1]))
    elif t == 'expr': gen_expr(n[1], out); out.append(('POP',))
    elif t == 'return':
        if n[1] is not None: gen_expr(n[1], out)
        else: out.append(('CONST', None))
        out.append(('RETURN',))
    elif t == 'if':
        gen_expr(n[1], out); out.append(('JZ', 0)); jz = len(out)-1
        for s in n[2]: gen_stmt(s, out)
        if n[3]:
            out.append(('JMP', 0)); jmp = len(out)-1
            out[jz] = ('JZ', len(out))
            for s in n[3]: gen_stmt(s, out)
            out[jmp] = ('JMP', len(out))
        else:
            out[jz] = ('JZ', len(out))
    elif t == 'while':
        st = len(out)
        gen_expr(n[1], out); out.append(('JZ', 0)); jz = len(out)-1
        for s in n[2]: gen_stmt(s, out)
        out.append(('JMP', st)); out[jz] = ('JZ', len(out))
    elif t == 'for':
        gen_expr(n[2], out); out.append(('ITER',))
        st = len(out); out.append(('FORNEXT', 0)); fx = len(out)-1
        out.append(('STORE', n[1]))
        for s in n[3]: gen_stmt(s, out)
        out.append(('JMP', st)); out[fx] = ('FORNEXT', len(out))

def run(code, env):
    stack = []; pc = 0
    while pc < len(code):
        ins = code[pc]; op = ins[0]
        if op == 'CONST': stack.append(ins[1])
        elif op == 'LOAD': stack.append(env.get(ins[1]))
        elif op == 'LOADB': stack.append(BUILTINS[ins[1]])
        elif op == 'STORE': env[ins[1]] = stack.pop()
        elif op == 'POP': stack.pop()
        elif op == 'LIST':
            n = ins[1]; items = stack[len(stack)-n:] if n else []
            if n: del stack[len(stack)-n:]
            stack.append(items)
        elif op in OPS:
            b = stack.pop(); a = stack.pop(); stack.append(OPS[op](a, b))
        elif op == 'JZ':
            if not stack.pop(): pc = ins[1]; continue
        elif op == 'JMP': pc = ins[1]; continue
        elif op == 'ITER': stack.append(iter(stack.pop()))
        elif op == 'FORNEXT':
            try: stack.append(next(stack[-1]))
            except StopIteration:
                stack.pop(); pc = ins[1]; continue
        elif op == 'MAKEFUNC': stack.append(('fn', ins[1], ins[2], ins[3], env))
        elif op == 'CALL':
            n = ins[1]
            args = stack[len(stack)-n:] if n else []
            if n: del stack[len(stack)-n:]
            f = stack.pop()
            if callable(f): stack.append(f(*args))
            else:
                e2 = dict(f[4])
                for p, a in zip(f[2], args): e2[p] = a
                stack.append(run(f[3], e2))
        elif op == 'RETURN': return stack.pop()
        pc += 1
    return None

if __name__ == '__main__':
    src = open(sys.argv[1], encoding='utf-8').read()
    ast = P(build_lines(src)).program()
    code = []
    for s in ast[1]: gen_stmt(s, code)
    with open(sys.argv[1].replace('.nx', '.nxb'), 'wb') as f:
        pickle.dump(code, f)
    run(code, {})
    print('BYTECODE:', len(code), 'ops | VM: NexusVM v8.3')
