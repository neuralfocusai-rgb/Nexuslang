with open('nexuslang.py', 'r') as f:
    c = f.read()

# 1. Clase ServidorWeb a nivel de modulo
c = c.replace(
    "# ==================== TESTS",
    '''# ==================== WEB SERVER (APIs tipo Flask) ====================
class ServidorWeb:
    def __init__(self, puerto=8080):
        self.puerto = puerto
        self.rutas = {}
    def ruta(self, path, funcion):
        self.rutas[path] = funcion
        return f"Ruta {path} registrada"
    def iniciar(self):
        from http.server import HTTPServer, BaseHTTPRequestHandler
        rutas = self.rutas
        class H(BaseHTTPRequestHandler):
            def do_GET(s):
                if s.path in rutas:
                    r = rutas[s.path]()
                    s.send_response(200)
                    s.send_header('Content-Type', 'application/json')
                    s.end_headers()
                    s.wfile.write(json.dumps(r, ensure_ascii=False).encode())
                else:
                    s.send_response(404)
                    s.end_headers()
            def log_message(s, *a): pass
        HTTPServer(('localhost', self.puerto), H).serve_forever()

# ==================== TESTS'''
)

# 2. Registrar en el namespace
c = c.replace(
    "ns['print'] = self._print",
    "ns['servidor_web'] = ServidorWeb\n        ns['web'].servidor = ServidorWeb\n        ns['print'] = self._print"
)

# 3. Test 19
c = c.replace(
    'check("18. HTTP support", hasattr(NexusLang(mostrar=False).ns[\'web\'], \'obtener\'))',
    'check("18. HTTP support", hasattr(NexusLang(mostrar=False).ns[\'web\'], \'obtener\'))\n    check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns[\'web\'], \'servidor\'))'
)
c = c.replace("(18 tests)", "(19 tests)")

with open('nexuslang.py', 'w') as f:
    f.write(c)
print("✅ SERVIDOR WEB AGREGADO")
