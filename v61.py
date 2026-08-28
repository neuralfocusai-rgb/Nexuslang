src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("        py = []\n        indent = 0", "        py = []\n        indent = 0\n        in_triple = None", 'triple_init')

rep("            s = self._quitar_comentarios(raw).strip()", '''            if in_triple:
                py.append(raw)
                if raw.count(in_triple) % 2 == 1: in_triple = None
                continue
            tq = None
            for q in ('"""', "''" + "'"):
                if raw.count(q) % 2 == 1: tq = q; break
            if tq:
                in_triple = tq
                py.append(raw)
                continue
            mu = re.match(r'^usar\\s+["\\'](.+?)["\\']$', raw.strip())
            if mu:
                py.append(raw[:len(raw) - len(raw.lstrip())] + 'usar("' + mu.group(1) + '")')
                continue
            s = self._quitar_comentarios(raw).strip()''', 'triple_usar_loop')

rep("    def _llaves(self, s):", '''    def _usar(self, ruta):
        if not ruta.endswith('.nx'): ruta += '.nx'
        if not hasattr(self, '_mods'): self._mods = set()
        if ruta in self._mods: return
        self._mods.add(ruta)
        with open(ruta, 'r', encoding='utf-8') as f:
            codigo = f.read()
        py = self.transpilar(codigo)
        exec(compile(py, ruta, 'exec'), self.ns)

    def _llaves(self, s):''', 'metodo_usar')

rep("    def _setup_namespace(self):", '''    def _setup_namespace(self):
        if not hasattr(self, 'ns'): self.ns = {}
        self.ns['usar'] = self._usar
        import types as _nts
        self.ns['nexus'] = _nts.SimpleNamespace(texto=_nts.SimpleNamespace(mayusculas=lambda t: t.upper(), minusculas=lambda t: t.lower(), largo=lambda t: len(t), contiene=lambda t, x: x in t, invertir=lambda t: t[::-1]), lista=_nts.SimpleNamespace(ordenar=sorted, largo=len, primero=lambda l: l[0], ultimo=lambda l: l[-1], sumar=sum, invertir=lambda l: l[::-1]), fecha=_nts.SimpleNamespace(hoy=lambda: __import__('datetime').date.today().isoformat(), ahora=lambda: __import__('datetime').datetime.now().strftime('%H:%M')))''', 'stdlib')

rep("    return failed == 0", '''    nx8 = NexusLang()
    nx8.ejecutar('imprimir(nexus.texto.mayusculas("v61"))')
    check('stdlib_texto', 'V61' in ''.join(nx8.output))
    nx9 = NexusLang()
    nx9.ejecutar('imprimir(nexus.lista.sumar([1, 2, 3]))')
    check('stdlib_lista', '6' in ''.join(nx9.output))
    nxa = NexusLang()
    nxa.ejecutar('x = """<div>\\n<h1>hola</h1>\\n</div>"""\\nimprimir("v61ml:" + x)')
    check('triple_string', '</div>' in ''.join(nxa.output))
    nxb = NexusLang()
    nxb.ejecutar('usar "nx_temp_mod.nx"\\nimprimir(doble(21))')
    check('modulos', '42' in ''.join(nxb.output))
    return failed == 0''', 'tests_v61')

rep('VERSION = "6.0.0"', 'VERSION = "6.1.0"', 'version')

open('nexuslang.py','w').write(src)
print('PATCH v6.1 OK')
