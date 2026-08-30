src = open('nexuslang.py').read()
old = "                if ruta not in rutas:"
new = """                if ruta.startswith('/comprar/') and hasattr(serv, 'fallback'):
                    _r = serv.fallback(ruta)
                    if _r is not None:
                        s.send_response(200)
                        s.send_header('Content-Type', 'text/html; charset=utf-8')
                        s.end_headers()
                        s.wfile.write(str(_r).encode())
                        return
                if ruta not in rutas:"""
print('f2 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
