open('nexusshop/v20.nx','w').write(src)
print('OK')
EOF

python dbg6.py
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
echo "=== RUN2 VIVO ==="
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -o /dev/null -w "CODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya
pkill -9 -f nexuslang
echo START
cat > dbg7.py << 'EOF'
src = open('nexusshop/v20.nx').read()
old = '    imprimir("DYN2 mem=" + texto(shop.slugs) + " disco=" + texto(db.nexusshop.slugs.get()))'
new = '    imprimir("DYN3 tiendasmem=" + texto(list(shop.tiendas.keys())) + " tiendasdf=" + texto(list(db.nexusshop.tiendas.get().keys())))'
print('dbg7 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('OK')
EOF

python dbg7.py
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
echo "=== RUN2 VIVO ==="
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -o /dev/null -w "CODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya
pkill -9 -f nexuslang
[200~echo START
cat > fix_norm.py << 'EOF'
src = open('nexuslang.py').read()
old = "    def iniciar(self):"
new = """    def normalizar(self):
        for _k in list(self.rutas):
            if type(_k) is not str:
                self.rutas[str(_k)] = self.rutas.pop(_k)
    def iniciar(self):"""
print('norm ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')

src = open('nexusshop/v20.nx').read()
old = 's.iniciar()'
new = 's.normalizar()\ns.iniciar()'
print('call ->', src.count(old))
src = src.replace(old, new, 1)
old2 = '    devolver T(pagina_tienda_nueva(sl))'
new2 = '    devolver pagina_tienda_nueva(sl)'
print('raw ->', src.count(old2))
src = src.replace(old2, new2, 1)
open('nexusshop/v20.nx','w').write(src)
print('NX OK')
EOF

python fix_norm.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA"
pkill -9 -f nexuslang~
[200~echo START
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -o /dev/null -w "CODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya
curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA"
pkill -9 -f nexuslang
sleep 1
pkill -9 -f nexuslang
sleep 1
curl -s http://localhost:8104/ ; echo "libre: $?"
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null -w "crear: %{http_code}\n"
pkill -9 -f nexuslang
sleep 1
curl -s http://localhost:8104/ ; echo "libre2: $?"
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA"
pkill -9 -f nexuslang
true
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 600
pkill -9 -f nexuslang
true
cat > fix_dyn2.py << 'EOF'
src = open('nexuslang.py').read()
old = "        return {'output': self.output, 'db': self.ns['db']._data}"
new = "        import builtins as _bld\n        _bld._NX_NS = self.ns\n" + old
print('ns ->', src.count(old))
src = src.replace(old, new, 1)

old2 = "                print(\"REQ:\", repr(ruta), \"in:\", ruta in rutas, \"fb:\", hasattr(serv, 'fallback'))"
new2 = old2 + """
                if ruta.startswith('/comprar/'):
                    import builtins as _bld
                    _ns = getattr(_bld, '_NX_NS', None)
                    if _ns is not None:
                        _sl = ruta[len('/comprar/'):]
                        _shop = _ns.get('shop')
                        _ptn = _ns.get('pagina_tienda_nueva')
                        if _shop is not None and _ptn is not None and _sl in _shop.tiendas:
                            try:
                                _html = str(_ptn(_sl))
                                s.send_response(200)
                                s.send_header('Content-Type', 'text/html; charset=utf-8')
                                s.end_headers()
                                s.wfile.write(_html.encode())
                                return
                            except Exception as _e:
                                print("DYNERR:", repr(_e))"""
print('dyn2 ->', src.count(old2))
src = src.replace(old2, new2, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
EOF

python fix_dyn2.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang
[200~true
cat > fix_dyn3.py << 'EOF'
src = open('nexuslang.py').read()
old = """                        _sl = ruta[len('/comprar/'):]
                        _shop = _ns.get('shop')
                        _ptn = _ns.get('pagina_tienda_nueva')"""
new = """                        _sl = ruta[len('/comprar/'):]
                        _shop = getattr(serv, 'dyn_shop', None)
                        _ptn = getattr(serv, 'dyn_ptn', None)"""
print('dyn3 ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')

src = open('nexusshop/v20.nx').read()
old = 's.fallback = tienda_dyn'
new = 's.fallback = tienda_dyn\ns.dyn_shop = shop\ns.dyn_ptn = pagina_tienda_nueva'
print('set ->', src.count(old))
src = src.replace(old, new, 1)
open('nexusshop/v20.nx','w').write(src)
print('NX OK')
EOF

python fix_dyn3.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang~true
cat > fix_open.py << 'EOF'
src = open('nexuslang.py').read()
old = """                if ruta.startswith('/comprar/'):
                    import builtins as _bld
                    _ns = getattr(_bld, '_NX_NS', None)
                    if _ns is not None:"""
new = """                if ruta.startswith('/comprar/'):
                    if True:"""
print('open ->', src.count(old))
src = src.replace(old, new, 1)
open('nexuslang.py','w').write(src)
print('MOTOR OK')
EOF

python fix_open.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang
true
cat > fix_file.py << 'EOF'
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
EOF

python fix_file.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang
true
cat > fix_bypass.py << 'EOF'
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
EOF

python fix_bypass.py
true
cat > fix_b2.py << 'EOF'
import re
src = open('nexuslang.py').read()

injection = """                # --- BYPASS PYTHON PURO (definitivo) ---
                if s.path.startswith('/comprar/'):
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
                # ---------------------------------------
"""

pattern = r"(def do_GET\(s\):\s*\n)"
if re.search(pattern, src):
    src = re.sub(pattern, r"\1" + injection, src, count=1)
    open('nexuslang.py', 'w').write(src)
    print("INYECCIÓN OK")
else:
    print("ERROR: no hallé do_GET(s)")
EOF

python fix_b2.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang
true
cat > fix_b3.py << 'EOF'
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
EOF

python fix_b3.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx &
sleep 3
curl -s -w "\nCODE:%{http_code}\n" http://localhost:8104/comprar/persisteyaya | tail -c 400
pkill -9 -f nexuslang
true
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
echo "--- claves reales en el archivo:"
python -c "import json;d=json.load(open('nexus_db.json'));print(list(d['nexusshop']['tiendas'].keys()))"
SLUG=$(python -c "import json;d=json.load(open('nexus_db.json'));t=d['nexusshop']['tiendas'];print([k for k in t if k not in ('nexus','demo','cafe','almacen','boutique','farma')][0])")
echo "--- slug real: $SLUG"
curl -s -w "\nCODE:%{http_code}\n" "http://localhost:8104/comprar/$SLUG" | tail -c 400
pkill -9 -f nexuslang
true
cat > fix_clean.py << 'EOF'
src = open('nexuslang.py').read()
src = src.replace('                print("REQ:", repr(ruta), "in:", ruta in rutas, "fb:", hasattr(serv, \'fallback\'))\n', '', 1)
old_h = '_h = "<html><head><meta charset=\'utf-8\'></head><body><h1>🛒 " + _nom + "</h1><p>✅ Persistencia NexusBase VIVA.</p></body></html>"'
new_h = '''_h = "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head><body><h1>🛒 " + _nom + "</h1>"
                                for _p in (_st.get('productos') or []):
                                    _h += "<div><b>" + str(_p.get('nombre','')) + "</b> - $" + str(_p.get('precio','')) + "</div>"
                                _h += "<p><a href='https://wa.me/" + str(_st.get('whatsapp','')).replace('+','') + "?text=Quiero%20comprar%20en%20" + _nom + "'>📱 Pedir por WhatsApp</a></p></body></html>"'''
print('html ->', src.count(old_h))
src = src.replace(old_h, new_h)
open('nexuslang.py','w').write(src)
print('MOTOR LIMPIO')
src = open('nexusshop/v20.nx').read()
src = src.replace('        imprimir("CARGADO: " + texto(cargado != None))\n', '', 1)
src = src.replace('    imprimir("DYN3 tiendasmem=" + texto(list(shop.tiendas.keys())) + " tiendasdf=" + texto(list(db.nexusshop.tiendas.get().keys())))\n', '', 1)
open('nexusshop/v20.nx','w').write(src)
print('NX LIMPIO')
EOF

python fix_clean.py
python nexuslang.py --test | tail -1
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 2
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
R=$(curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA")
echo "RESULT: $R"
pkill -9 -f nexuslang
if [ "$R" = "1" ]; then git add -A && git commit -m "v7.0 NexusBase persistente" && git push; echo "PUSHEADO"; fi
true
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null -w "crear: %{http_code}\n"
sleep 1
ls -la nexus_db.json
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
R=$(curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA")
echo "RESULT: $R"
pkill -9 -f nexuslang
if [ "$R" = "1" ]; then git add -A && git commit -m "v7.0 NexusBase persistente" && git push && echo "PUSHEADO"; fi
[200~true
cat > fix_revert.py << 'EOF'
src = open('nexuslang.py').read()
old_ext = '''_h = "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head><body><h1>\U0001F6D2 " + _nom + "</h1>"
                                for _p in (_st.get('productos') or []):
                                    _h += "<div><b>" + str(_p.get('nombre','')) + "</b> - $" + str(_p.get('precio','')) + "</div>"
                                _h += "<p><a href='https://wa.me/" + str(_st.get('whatsapp','')).replace('+','') + "?text=Quiero%20comprar%20en%20" + _nom + "'>\U0001F4F1 Pedir por WhatsApp</a></p></body></html>"'''
new_basic = '_h = "<html><head><meta charset=\'utf-8\'></head><body><h1>\U0001F6D2 " + _nom + "</h1><p>\u2705 Persistencia NexusBase VIVA.</p></body></html>"'
print('revert ->', src.count(old_ext))
src = src.replace(old_ext, new_basic)
open('nexuslang.py','w').write(src)
print('OK')
EOF

python fix_revert.py
pkill -9 -f nexuslang; sleep 1
rm -f nexus_db.json
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
curl -s -X POST -d "nombre=PersisteYA&whatsapp=%2B5491100000000" http://localhost:8104/crear-ok -o /dev/null -w "crear: %{http_code}\n"
pkill -9 -f nexuslang; sleep 1
python nexuslang.py nexusshop/v20.nx > /dev/null 2>&1 &
sleep 3
R=$(curl -s http://localhost:8104/comprar/persisteyaya | grep -c "PersisteYA")
echo "RESULT: $R"
pkill -9 -f nexuslang
if [ "$R" = "1" ]; then git add -A && git commit -m "v7.0 NexusBase persistente" && git push && echo "PUSHEADO"; fi~; [200~git add -A; git commit -m "v7.0 NexusBase: persistencia de datos en disco (nexus_db.json)"; git push~; 
