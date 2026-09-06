src = open('nexuslang_v11.py', encoding='utf-8').read()
old = """if __name__=='__main__':
    src=open(sys.argv[1],encoding='utf-8').read()
    try:
        run(P(lex(src)).program(),Env())
    except Exception as e:
        print(str(e))"""
new = """def repl():
    env=Env()
    print('NexusLang v11 REPL — salir: خروج')
    buf=''
    while True:
        try:
            line=input('... ' if buf else '>> ')
        except EOFError:
            break
        if line.strip() in ('exit','خروج'):
            break
        buf+=line+'\\n'
        if buf.count('{')>buf.count('}'):
            continue
        try:
            run(P(lex(buf)).program(),env)
        except Exception as e:
            print(str(e))
        buf=''

if __name__=='__main__':
    if len(sys.argv)>1:
        src=open(sys.argv[1],encoding='utf-8').read()
        try:
            run(P(lex(src)).program(),Env())
        except Exception as e:
            print(str(e))
    else:
        repl()"""
if old in src:
    src = src.replace(old, new, 1)
    open('nexuslang_v11.py','w',encoding='utf-8').write(src)
    print('REPL agregado OK')
else:
    print('NO se encontro')
