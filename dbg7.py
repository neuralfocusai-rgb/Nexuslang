src = open('nexusshop/v20.nx').read()
old = '    imprimir("DYN2 mem=" + texto(shop.slugs) + " disco=" + texto(db.nexusshop.slugs.get()))'
new = '    imprimir("DYN3 tiendasmem=" + texto(list(shop.tiendas.keys())) + " tiendasdf=" + texto(list(db.nexusshop.tiendas.get().keys())))'
print('dbg7 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
