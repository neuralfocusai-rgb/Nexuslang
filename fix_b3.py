import re
src = open('nexuslang.py').read()
injection = """                if s.path.startswith('/comprar/'):
                    _slug = s.path[len('/comprar/'):]
                    try:
                        import json as _j, os as _o
                        def _find(node, key):
                            if isinstance(node, dict):
                                if key in node and isinstance(node[key], dict):
                                    return node[key]
                                for v in node.values():
                                    r = _find(v, key)
                                    if r is not None: return r
                            elif isinstance(node, list):
                                for v in node:
                                    r = _find(v, key)
                                    if r is not None: return r
                            return None
                        _data = None
                        for _f in ('nexus_db.json', 'nexus_data.json'):
                            if _o.path.exists(_f):
                                _data = _j.load(open(_f, encoding='utf-8')); break
                        if _data is not None:
                            _st = _find(_data, _slug)
                            if _st is not None:
                                _nom = str(_st.get('nombre', _slug))
                                _h = "<html><head><meta charset='utf-8'></head><body><h1>🛒 " + _nom + "</h1><p>✅ Persistencia NexusBase VIVA.</p></body></html>"
                                s.send_response(200)
                                s.send_header('Content-Type', 'text/html; charset=utf-8')
                                s.end_headers()
                                s.wfile.write(_h.encode('utf-8'))
                                return
                    except Exception as _e:
                        print("DYN_ERR:", repr(_e))
"""
n = len(re.findall(r"def do_GET\(s\):\s*\n", src))
src = re.sub(r"(def do_GET\(s\):\s*\n)", r"\1" + injection, src)
open('nexuslang.py','w').write(src)
print("do_GET encontrados:", n, "-> todos parcheados")
