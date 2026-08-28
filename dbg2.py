src = open('nexuslang.py').read()
old = """                else:
                    s.send_response(404)
                    s.end_headers()"""
new = """                else:
                    print("DBG404:", repr(ruta), repr([k for k in rutas if 'comprar/p' in k]))
                    s.send_response(404)
                    s.end_headers()"""
print('dbg ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('OK')
