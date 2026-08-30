src = open('nexuslang.py').read()
old = """                if ruta.startswith('/comprar/'):
                    import builtins as _bld
                    _ns = getattr(_bld, '_NX_NS', None)
                    if _ns is not None:"""
new = """                if ruta.startswith('/comprar/'):
                    if True:"""
print('open ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
