src = open('nexuslang.py').read()
old = """                if ruta not in rutas:
                    for _k in list(rutas):
                        if str(_k) == str(ruta):
                            rutas[ruta] = rutas[_k]
                            break

                if ruta in rutas:"""
new = """                if ruta.startswith('/comprar/'):
                    r = None
                    if hasattr(serv, 'fallback'):
                        r = serv.fallback(ruta)
                    if r is not None:
                        if es_html(r):
                            s.send_response(200)
                            s.send_header('Content-Type', 'text/html; charset=utf-8')
                            s.end_headers()
                            s.wfile.write(str(r).encode())
                        else:
                            s.send_response(200)
                            s.send_header('Content-Type', 'application/json')
                            s.end_headers()
                            s.wfile.write(json.dumps(r, ensure_ascii=False).encode())
                        continue
                if ruta in rutas:"""
print('final ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
