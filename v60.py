src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("    def transpilar(self, codigo):", '''    def _llaves(self, s):
        s = s.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))
        code = ''
        quote = None
        for c in s:
            if quote:
                if c == quote: quote = None
            elif c in '"\\'': quote = c
            elif c == '#': break
            else: code += c
        return code.count('{') - code.count('}')

    def transpilar(self, codigo):''', 'metodo_llaves')

rep("        quote = None\n        for c in linea:", "        linea = linea.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))\n        quote = None\n        for c in linea:", 'esc_traducir')

rep("        return result", "        return result.replace(chr(1), chr(92)+chr(34)).replace(chr(2), chr(92)+chr(39))", 'restore_traducir')

rep("        out = []\n        quote = None", "        linea = linea.replace(chr(92)+chr(34), chr(1)).replace(chr(92)+chr(39), chr(2))\n        out = []\n        quote = None", 'esc_comentarios')

rep("        return ''.join(out).rstrip()", "        return ''.join(out).replace(chr(1), chr(92)+chr(34)).replace(chr(2), chr(92)+chr(39)).rstrip()", 'restore_comentarios')

rep("            if not s: continue", "            if not s: py.append(''); continue", 'lineas_reales')

rep("            if buffer.count('{') > buffer.count('}'): continue", "            if self._llaves(buffer) > 0: continue", 'repl_consciente')

rep("    return failed == 0", '''    I.ejecutar('imprimir("v6a:#{}()")')
    check('string_blindada', 'v6a:#{}()' in ''.join(I.output))
    codigo = 'imprimir("v6b:di' + chr(92) + chr(34) + 'jo")'
    I.ejecutar(codigo)
    check('escapes', 'v6b:di"jo' in ''.join(I.output))
    return failed == 0''', 'tests_v6')

rep('VERSION = "5.4.0"', 'VERSION = "6.0.0"', 'version')

open('nexuslang.py','w').write(src)
print('PATCH v6.0 OK')
