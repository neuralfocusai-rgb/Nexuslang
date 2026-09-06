src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "'leer':BUILTINS['پڑھو']})"
new = "'leer':BUILTINS['پڑھو']})\nBUILTINS.update({'قاموس':lambda: {},'dict':lambda: {},'diccionario':lambda: {},'درج':lambda d,k,v: (d.__setitem__(k,v) or d),'put':lambda d,k,v: (d.__setitem__(k,v) or d),'poner':lambda d,k,v: (d.__setitem__(k,v) or d),'کلیدیں':lambda d: list(d.keys()),'keys':lambda d: list(d.keys()),'claves':lambda d: list(d.keys()),'قدریں':lambda d: list(d.values()),'values':lambda d: list(d.values()),'valores':lambda d: list(d.values()),'بالا':lambda s: s.upper(),'upper':lambda s: s.upper(),'mayus':lambda s: s.upper(),'زیر':lambda s: s.lower(),'lower':lambda s: s.lower(),'minus':lambda s: s.lower(),'بدلو':lambda s,a,b: s.replace(a,b),'replace':lambda s,a,b: s.replace(a,b),'reemplazar':lambda s,a,b: s.replace(a,b),'کاٹو':lambda s,sep=' ': s.split(sep),'split':lambda s,sep=' ': s.split(sep),'dividir':lambda s,sep=' ': s.split(sep),'جوڑو':lambda sep,l: sep.join(str(x) for x in l),'join':lambda sep,l: sep.join(str(x) for x in l),'unir':lambda sep,l: sep.join(str(x) for x in l)})"
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('Diccionarios + texto trilingue OK')
else:
    print('NO se encontro')
