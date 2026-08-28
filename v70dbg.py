src = open('nexusshop/v20.nx').read()
old = 's.iniciar()'
new = 'imprimir("TOTAL_RUTAS: " + texto(len(s.rutas)))\ns.iniciar()'
print('dbg ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('DBG OK')
