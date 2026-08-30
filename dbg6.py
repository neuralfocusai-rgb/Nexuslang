src = open('nexusshop/v20.nx').read()
old = 'def tienda_dyn(ruta) {'
new = '''def tienda_dyn(ruta) {
    imprimir("DYN2 mem=" + texto(shop.slugs) + " disco=" + texto(db.nexusshop.slugs.get()))'''
print('dbg6 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
