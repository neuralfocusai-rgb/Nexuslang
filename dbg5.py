src = open('nexusshop/v20.nx').read()
old = '        cargado = db.nexusshop.tiendas.get()'
new = '        cargado = db.nexusshop.tiendas.get()\n        imprimir("CARGADO: " + texto(cargado != None))'
print('dbg5 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
