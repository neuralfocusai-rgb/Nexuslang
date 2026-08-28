with open('nexuslang.py', 'r') as f:
    c = f.read()

old = """            def do_GET(s):
                if s.path in rutas:
                    r = rutas[s.path]()
                    s.send_response(200)
                    s.send_header('Content-Type', 'application/json')
                    s.end_headers()
                    s.wfile.write(json.dumps(r, ensure_ascii=False).encode())
                else:
                    s.send_response(404)
                    s.end_headers()"""

new = """            def do_GET(s):
                if s.path in rutas:
                    r = rutas[s.path]()
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
                else:
                    s.send_response(404)
                    s.end_headers()"""

assert old in c, "do_GET no encontrado"
c = c.replace(old, new)

c = c.replace(
    "# ==================== WEB SERVER",
    "def es_html(t):\n    return isinstance(t, str) and t.strip().startswith('<')\n\n# ==================== WEB SERVER"
)

c = c.replace(
    "ns['servidor_web'] = ServidorWeb",
    "ns['servidor_web'] = ServidorWeb\n        ns['es_html'] = es_html"
)

c = c.replace(
    'check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns[\'web\'], \'servidor\'))',
    'check("19. Web server (APIs)", hasattr(NexusLang(mostrar=False).ns[\'web\'], \'servidor\'))\n    check("20. Full-stack HTML+JSON", es_html("<html>x</html>") and not es_html({"a": 1}))'
)
c = c.replace("(19 tests)", "(20 tests)")

with open('nexuslang.py', 'w') as f:
    f.write(c)
print("✅ FULL-STACK AGREGADO")
