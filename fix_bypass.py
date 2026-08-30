import re
src = open('nexuslang.py').read()

injection = """
            # --- BYPASS PYTHON NATIVO PARA RUTAS DINÁMICAS ---
            if self.path.startswith('/comprar/'):
                _slug = self.path[len('/comprar/'):]
                try:
                    import json, os
                    _dbf = 'nexus_db.json' if os.path.exists('nexus_db.json') else 'nexus_data.json'
                    if os.path.exists(_dbf):
                        with open(_dbf, 'r', encoding='utf-8') as _f:
                            _db = json.load(_f)
                        _tiendas = _db.get('nexusshop', {}).get('tiendas', {})
                        if _slug in _tiendas:
                            _nombre = _tiendas[_slug].get('nombre', _slug)
                            _html = "<html><head><meta charset='utf-8'></head><body><h1>🛒 " + str(_nombre) + "</h1><p>✅ Persistencia NexusBase VIVA.</p></body></html>"
                            self.send_response(200)
                            self.send_header('Content-Type', 'text/html; charset=utf-8')
                            self.end_headers()
                            self.wfile.write(_html.encode('utf-8'))
                            return
                except Exception as _e:
                    print("DYN_ERR:", _e)
            # --------------------------------------------------
"""

pattern = r"(def do_GET\(self\):\s*\n)"
if re.search(pattern, src):
    src = re.sub(pattern, r"\1" + injection, src, count=1)
    open('nexuslang.py', 'w').write(src)
    print("INYECCIÓN QUIRÚRGICA EXITOSA")
else:
    print("ERROR: No se encontró do_GET")
