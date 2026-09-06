src = open('nexuslang_v11.py', encoding='utf-8').read()
old = "'عنصر':lambda l,i: l[i]}"
new = "'عنصر':lambda l,i: l[i]}\nBUILTINS.update({'list':BUILTINS['فہرست'],'lista':BUILTINS['فہرست'],'append':BUILTINS['شامل'],'agregar':BUILTINS['شامل'],'pop':BUILTINS['نکالو'],'sacar':BUILTINS['نکالو'],'sort':BUILTINS['ترتیب'],'ordenar':BUILTINS['ترتیب'],'reverse':BUILTINS['الٹو'],'invertir':BUILTINS['الٹو'],'item':BUILTINS['عنصر'],'elemento':BUILTINS['عنصر'],'len':BUILTINS['لمبائی'],'longitud':BUILTINS['لمبائی'],'sqrt':BUILTINS['جذر'],'raiz':BUILTINS['جذر'],'max':BUILTINS['بڑا'],'maximo':BUILTINS['بڑا'],'min':BUILTINS['چھوٹا'],'minimo':BUILTINS['چھوٹا'],'abs':BUILTINS['مطلق'],'absoluto':BUILTINS['مطلق'],'round':BUILTINS['گرد'],'redondear':BUILTINS['گرد'],'str':BUILTINS['متن'],'texto':BUILTINS['متن'],'int':BUILTINS['عدد'],'entero':BUILTINS['عدد'],'input':BUILTINS['پڑھو'],'leer':BUILTINS['پڑھو']})"
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('NexusLang 100% trilingue OK')
else:
    print('NO se encontro')
