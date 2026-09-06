src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "'جذر':lambda x:x**0.5}"
new = "'جذر':lambda x:x**0.5,'بڑا':max,'چھوٹا':min,'مطلق':abs,'گرد':round}"
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Biblioteca estandar Urdu agregada OK')
else:
    print('NO se encontro')
