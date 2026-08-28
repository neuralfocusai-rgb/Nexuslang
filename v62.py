src = open('nexuslang.py').read()
def rep(old, new, tag):
    global src
    n = src.count(old)
    print(tag, '->', n)
    if n == 1: src = src.replace(old, new, 1)

rep("        self.rutas = {}", '''        self.rutas = {}
        self._datos = {}
    def recibir_datos(self):
        return self._datos
    def redirigir(self, ruta):
        return 'REDIRIGIR:' + ruta
    def _parsear(self, cuerpo):
        datos = {}
        try:
            if cuerpo.strip().startswith('{'):
                datos = json.loads(cuerpo)
            else:
                from urllib.parse import unquote_plus
                datos = {k: unquote_plus(v) for k, v in (p.split('=', 1) for p in cuerpo.split('&') if '=' in p)}
        except Exception:
            pass
        return datos''', 'api_post')

rep("        rutas = self.rutas", "        rutas = self.rutas\n        serv = self", 'serv_ref')

rep("            def log_message(s, *a): pass", '''            def do_POST(s):
                n = int(s.headers.get('Content-Length', 0))
                cuerpo = s.rfile.read(n).decode('utf-8') if n else ''
                serv._datos = serv._parsear(cuerpo)
                if s.path in rutas:
                    r = rutas[s.path]()
                    if isinstance(r, str) and r.startswith('REDIRIGIR:'):
                        s.send_response(302)
                        s.send_header('Location', r[10:])
                        s.end_headers()
                        return
                    s.send_response(200)
                    s.send_header('Content-Type', 'text/html; charset=utf-8')
                    s.end_headers()
                    s.wfile.write(str(r).encode())
                else:
                    s.send_response(404)
                    s.end_headers()
            def log_message(s, *a): pass''', 'do_post')

rep("    return failed == 0", '''    nxc = ServidorWeb()
    d = nxc._parsear('nombre=Lucas&tienda=Mi%20Shop')
    check('post_form', d.get('tienda') == 'Mi Shop')
    nxd = ServidorWeb()
    check('redirigir', nxd.redirigir('/ok') == 'REDIRIGIR:/ok')
    nxe = ServidorWeb()
    dj = nxe._parsear('{"a": 1}')
    check('post_json', dj.get('a') == 1)
    return failed == 0''', 'tests_v62')

rep('VERSION = "6.1.0"', 'VERSION = "6.2.0"', 'version')

open('nexuslang.py','w').write(src)
print('PATCH v6.2 OK')
