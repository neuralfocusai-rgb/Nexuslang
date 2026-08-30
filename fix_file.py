src = open('nexuslang.py').read()
old = "                print(\"REQ:\", repr(ruta), \"in:\", ruta in rutas, \"fb:\", hasattr(serv, 'fallback'))"
new = old + """
                if ruta.startswith('/comprar/'):
                    _sl = ruta[len('/comprar/'):]
                    try:
                        import json as _j
                        _d = _j.load(open(_NEXUS_DB_FILE, encoding='utf-8'))
                        _t = (_d.get('nexusshop') or {}).get('tiendas') or {}
                        if _sl in _t:
                            _st = _t[_sl]
                            _h = "<html><head><meta charset='utf-8'><title>" + str(_st.get('nombre')) + "</title></head><body><h1>🛒 " + str(_st.get('nombre')) + "</h1>"
                            for _p in (_st.get('productos') or []):
                                _h += "<div><b>" + str(_p.get('nombre')) + "</b> — $" + str(_p.get('precio')) + "</div>"
                            _h += "<p>📱 WhatsApp: " + str(_st.get('whatsapp')) + "</p></body></html>"
                            s.send_response(200)
                            s.send_header('Content-Type', 'text/html; charset=utf-8')
                            s.end_headers()
                            s.wfile.write(_h.encode())
                            return
                    except Exception as _e:
                        print("DYNERR:", repr(_e))"""
print('file ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
