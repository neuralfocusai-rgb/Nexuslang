with open('nexuslang.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Corregir test 22 linea por linea (garantizado)
lines = c.split('\n')
for i, l in enumerate(lines):
    if 'async funcion async_test' in l:
        lines[i] = '    l.ejecutar(\'async funcion async_test() {\\n    devolver "async works"\\n}\\nresultado = async_run(async_test())\\nimprimir(resultado)\')'
c = '\n'.join(lines)

# 2. Soportar } capturar (e) { y } finalmente { (si no esta ya)
old_branch = """            if s.startswith('}') and ('sino' in s or 'else' in s):
                indent = max(0, indent - 1)
                py.append('    ' * indent + 'else:')
                indent += 1
                continue"""
new_branch = """            if s.startswith('}') and ('sino' in s or 'else' in s or 'capturar' in s or 'except' in s or 'finalmente' in s or 'finally' in s):
                indent = max(0, indent - 1)
                head = s[1:].strip()
                if head.endswith('{'): head = head[:-1].strip()
                m = re.match(r'(?:capturar|except)\\s*\\(\\s*(\\w+)\\s*\\)', head)
                if m:
                    py.append('    ' * indent + f'except Exception as {m.group(1)}:')
                elif head.startswith('capturar') or head.startswith('except'):
                    py.append('    ' * indent + 'except Exception:')
                elif head.startswith('finalmente') or head.startswith('finally'):
                    py.append('    ' * indent + 'finally:')
                else:
                    py.append('    ' * indent + 'else:')
                indent += 1
                continue"""
if old_branch in c:
    c = c.replace(old_branch, new_branch)
    print("✅ Branch capturar agregado")

with open('nexuslang.py', 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ FIX FINAL APLICADO")
