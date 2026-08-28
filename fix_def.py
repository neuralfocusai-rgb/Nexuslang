src = open('nexuslang.py').read()
old = """                if ruta in rutas:
                    r = rutas[ruta]()"""
new = """                if ruta not in rutas:
                    for _k in list(rutas):
                        if str(_k) == str(ruta):
                            rutas[ruta] = rutas[_k]
                            break
                if ruta in rutas:
                    r = rutas[ruta]()"""
print('fix ->', src.count(old))
src = src.replace(old, new, 1)
src = src.replace("""                else:
                    print("DBG404:", repr(ruta), repr([k for k in rutas if 'comprar/p' in k]))
                    s.send_response(404)
                    s.end_headers()""", """                else:
                    s.send_response(404)
                    s.end_headers()""", 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
src = open('nexusshop/v20.nx').read()
src = src.replace('imprimir("KEYS: " + texto(s.rutas.keys()))\ns.iniciar()', 's.iniciar()', 1)
open('nexusshop/v20.nx','w').write(src)
print('LIMPIO OK')
