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
