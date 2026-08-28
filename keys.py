src = open('nexusshop/v20.nx').read()
old = 's.iniciar()'
new = 'imprimir("KEYS: " + texto(s.rutas.keys()))\ns.iniciar()'
print('keys ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
