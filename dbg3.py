src = open('nexusshop/v20.nx').read()
old = '    devolver T(pagina_tienda_nueva(sl))'
new = '    imprimir("DYN: " + sl + " tiene=" + texto(shop.tiendas.get(sl) != None))\n    devolver T(pagina_tienda_nueva(sl))'
print('dbg3 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
