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
