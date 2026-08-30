src = open('nexuslang.py').read()
old = """                else:
                    s.send_response(404)
                    s.end_headers()"""
new = """                else:
                    r = None
                    if hasattr(serv, 'fallback'):
                        r = serv.fallback(ruta)
                    if r is not None:
                        s.send_response(200)
                        s.send_header('Content-Type', 'text/html; charset=utf-8')
                        s.end_headers()
                        s.wfile.write(str(r).encode())
                    else:
                        s.send_response(404)
                        s.end_headers()"""
print('dyn ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')

src = open('nexusshop/v20.nx').read()
old = 's.ruta("/crear", lambda: T(pagina_crear()))'
new = '''def tienda_dyn(ruta) {
    si ruta.find("/comprar/") != 0 {
        devolver None
    }
    sl = ruta.replace("/comprar/", "")
    si shop.tiendas.get(sl) == None {
        devolver None
    }
    devolver T(pagina_tienda_nueva(sl))
}
s.fallback = tienda_dyn
s.ruta("/crear", lambda: T(pagina_crear()))'''
print('fallback ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('MARKETPLACE OK')
