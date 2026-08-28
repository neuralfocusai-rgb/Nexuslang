src = open('nexuslang.py').read()

HELP = '''    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h', 'help', 'ayuda'):
        print("NEXUSLANG v%s - lenguaje bilingue (es/en)" % VERSION)
        print("USO / USAGE:")
        print("  nexus archivo.nx       ejecutar app / run app")
        print("  nexus -i               interactivo / interactive REPL")
        print("  nexus --demo [es|en]   demo bilingue / bilingual demo")
        print("  nexus --test           probar / run tests")
        print("  nexus --help           ayuda / help")
        print("SINTAXIS / SYNTAX:")
        print("  imprimir|print  clase|class  devolver|return")
        print("  si|if  sino|else  para|for  mientras|while")
        sys.exit(0)
'''
src = src.replace('if __name__ == "__main__":\n', 'if __name__ == "__main__":\n' + HELP, 1)

old_demo = """    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        NexusLang().ejecutar(DEMO_CODE)
        sys.exit(0)"""
new_demo = """    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        modo = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ('es', 'en') else 'es'
        codigo = DEMO_CODE
        if modo == 'en':
            codigo = DEMO_CODE.replace('imprimir(', 'print(').replace('Clases/OOP:', 'Classes/OOP:').replace('Base de datos:', 'Database:').replace('"IA: "', '"AI: "').replace('Demo completo - listo para produccion', 'Demo complete - production ready')
        NexusLang().ejecutar(codigo)
        sys.exit(0)"""
src = src.replace(old_demo, new_demo, 1)

old_repl = """            if buffer.count('{') > buffer.count('}'): continue
            lang.ejecutar(buffer)
            buffer = ''"""
new_repl = """            if buffer.count('{') > buffer.count('}'): continue
            linea = buffer.strip()
            es_expr = bool(linea) and '=' not in linea and not linea.startswith('#') and linea.split()[0] not in ('imprimir','print','clase','class','si','if','para','for','mientras','while','devolver','return','async','usar')
            try:
                lang.ejecutar('imprimir(' + linea + ')' if es_expr else buffer)
            except Exception as e:
                print("⛔ " + type(e).__name__ + ": " + str(e).split('(')[0].strip())
            buffer = ''"""
src = src.replace(old_repl, new_repl, 1)

old_file = """        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            lang.ejecutar(f.read())"""
new_file = """        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            try:
                lang.ejecutar(f.read())
            except Exception as e:
                print("⛔ Error en tu app / in your app -> " + type(e).__name__ + ": " + str(e).split('(')[0].strip())
                sys.exit(1)"""
src = src.replace(old_file, new_file, 1)

open('nexuslang.py','w').write(src)
print('PATCH v5.4 OK')
