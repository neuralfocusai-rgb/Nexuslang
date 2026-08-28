from nexuslang import NexusLang
lang = NexusLang()
lang.ejecutar('''
contenido = web.parrafo("The first bilingual programming language with built-in AI") + web.parrafo("El primer lenguaje bilingue con IA integrada") + web.boton("pip install nexuslang") + web.caja("12/12 tests passed - Production Ready - MIT License - Zero dependencies")
html = web.pagina("NexusLang v5.0 - Launch", contenido)
imprimir(web.guardar("launch", html))
''')
