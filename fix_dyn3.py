src = open('nexuslang.py').read()
old = """                        _sl = ruta[len('/comprar/'):]
                        _shop = _ns.get('shop')
                        _ptn = _ns.get('pagina_tienda_nueva')"""
new = """                        _sl = ruta[len('/comprar/'):]
                        _shop = getattr(serv, 'dyn_shop', None)
                        _ptn = getattr(serv, 'dyn_ptn', None)"""
print('dyn3 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')

src = open('nexusshop/v20.nx').read()
old = 's.fallback = tienda_dyn'
new = 's.fallback = tienda_dyn\ns.dyn_shop = shop\ns.dyn_ptn = pagina_tienda_nueva'
print('set ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('NX OK')
