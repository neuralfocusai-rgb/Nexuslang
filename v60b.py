src = open('nexuslang.py').read()
old = """    I.ejecutar('imprimir("v6a:#{}()")')
    check('string_blindada', 'v6a:#{}()' in ''.join(I.output))
    codigo = 'imprimir("v6b:di' + chr(92) + chr(34) + 'jo")'
    I.ejecutar(codigo)
    check('escapes', 'v6b:di"jo' in ''.join(I.output))"""
new = """    nx6 = NexusLang()
    nx6.ejecutar('imprimir("v6a:#{}()")')
    check('string_blindada', 'v6a:#{}()' in ''.join(nx6.output))
    nx7 = NexusLang()
    codigo = 'imprimir("v6b:di' + chr(92) + chr(34) + 'jo")'
    nx7.ejecutar(codigo)
    check('escapes', 'v6b:di"jo' in ''.join(nx7.output))"""
print('fix ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('FIX OK')
