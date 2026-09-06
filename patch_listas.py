src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "'گرد':round}"
new = "'گرد':round,'فہرست':lambda *a: list(a),'شامل':lambda l,x: (l.append(x) or l),'نکالو':lambda l: l.pop(),'ترتیب':lambda l: (l.sort() or l),'الٹو':lambda l: (l.reverse() or l),'عنصر':lambda l,i: l[i]}"
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Listas Urdu agregadas OK')
else:
    print('NO se encontro')
