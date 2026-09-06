src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "('DOT','.')]):"
new = "('DOT','.')]: "
new = new.strip()
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Parentesis corregido OK')
else:
    print('NO se encontro')
